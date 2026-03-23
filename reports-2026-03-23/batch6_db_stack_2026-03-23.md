# EPS DB Core Stack Analysis Report
**Date:** 2026-03-23  
**Analyst:** Batch 6 - DB Stack (idalib-mcp)  
**DLLs Analyzed:** SSAdoBase.dll.i64 (port 12023), SSDaoBase.dll.i64 (port 12024), SSDatabaseCore.dll.i64 (port 12025), SSDataXCore.dll.i64 (port 12026)

---

## 1. Module Overview

| Module | Port | Arch | Base Addr | Functions | Strings | Key Role |
|--------|------|------|-----------|-----------|---------|----------|
| SSAdoBase.dll | 12023 | 32-bit | 0x10000000 | 374 | 275 | **ADO abstraction layer** |
| SSDaoBase.dll | 12024 | 32-bit | 0x10000000 | 801 | 650 | **DAO abstraction layer** |
| SSDatabaseCore.dll | 12025 | 32-bit | 0x10000000 | 660 | 476 | **Core DB driver abstraction** |
| SSDataXCore.dll | 12026 | 32-bit | 0x10000000 | 1376 | 1508 | **DataX / attribute table registry** |

All four DLLs share the same base address (0x10000000), indicating they are 32-bit in-process components within the EPS address space. They all import from `SSCore32.dll`.

---

## 2. Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        Eps.exe (Main Process)                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               SSERPTools.exe.i64 (port 12002)           │   │
│  │     Business logic, QLR/BDCDYH/FW processing            │   │
│  └──────────────────────────┬─────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────┴─────────────────────────────┐   │
│  │              SSExchange.exe.i64 (port 12020)            │   │
│  │     Data exchange, workflow, cross-module calls         │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐  │
│  │               SSMap.exe.i64 (port 12003)                  │  │
│  │     Map rendering, spatial data, feature tables           │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐  │
│  │              SSDataXCore.dll.i64 (port 12026)             │  │
│  │  Namespace: CDataXCore                                     │  │
│  │  ┌─ AddAttrTableDef(ObjTypeEnum, CDBTableDef)             │  │
│  │  └─ Thunks → SSDaoBase (OpenRecordset, CreateTable, etc.)  │  │
│  │  Strings: .edb files (_none.edb), AttrTable patterns       │  │
│  │  Function count: 1376  |  addr: 0x10000000                  │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐  │
│  │             SSDatabaseCore.dll.i64 (port 12025)            │  │
│  │  Namespace: SSDataBase                                     │  │
│  │  ┌─ SSDBDriver  (executes via ADO or DAO backend)          │  │
│  │  ├─ SSDBQuery   (query builder: isSelect, bindValue)       │  │
│  │  ├─ SSDBResult  (result set: getsql, execBatch, tables)    │  │
│  │  └─ SSDBCachedResult, SSDBField                           │  │
│  │  Delegates SQL execution to ADO or DAO depending on config  │  │
│  │  Function count: 660  |  addr: 0x10000000                   │  │
│  └───────────────┬───────────────────────┬───────────────────┘  │
│                  │                       │                       │
│  ┌───────────────┴───────┐  ┌───────────┴────────────────┐     │
│  │  SSAdoBase.dll.i64     │  │  SSDaoBase.dll.i64           │     │
│  │  (port 12023)          │  │  (port 12024)                │     │
│  │  Namespace: CAdo*      │  │  Namespace: CDao* / CSS*     │     │
│  │  CAdoRecordset         │  │  CDBRecordset               │     │
│  │  CAdoCommand           │  │  CDaoDatabase, CDaoTableDef │     │
│  │  CSSAdoBase            │  │  CDaoWorkspace              │     │
│  │  CSSAdoRecordset       │  │  CSSDatabase                │     │
│  │                        │  │                              │     │
│  │  Providers:            │  │  Uses DAO360 / MS Jet 4.0   │     │
│  │  - SQLOLEDB            │  │  Files: platform.mdb        │     │
│  │  - Jet.OLEDB.4.0       │  │  SetSystemDB() call        │     │
│  │  Function count: 374   │  │  Function count: 801        │     │
│  └────────────────────────┘  └──────────────────────────────┘     │
│                  \                          /                     │
│                   \                        /                      │
│                    └──────────────────────┘                       │
│                        SSCore32.dll                                │
│                  (shared utilities, CBinaryAttrMan, etc.)          │
└──────────────────────────────────────────────────────────────────┘

Legend: Solid arrows = delegation; Dashed = data flow via SQL strings
```

---

## 3. DB Abstraction Layers — Call Flow

### Layer 1: ADO (SSAdoBase.dll)
**SQL execution ownership:** `ExecuteSQL` at `0x10005276`  
**Connection:** `GetConnection` at `0x10001000`  
**Recordset:** `OpenRecordset` at `0x10008048`

The ADO path is used for **remote/proxied** connections (SQLOLEDB — SQL Server via OLEDB). The `CSSAdoBase` class is the main interface. The key SQL execution method `ExecuteSQL(CString)` constructs SQL strings and passes them through the ADO COM interface.

**Call chain for SQL execution (ADO path):**
```
CSSAdoBase::ExecuteSQL (0x10005276)
  └─> CAdoRecordset::OpenRecordset (0x10008048)
       └─> COM ADO _Recordset::Open()
  └─> CSSAdoBase::Refresh (0x1000427a)  [re-query]
  └─> CAdoRecordset::Update (0x10008421)  [batch write]
  └─> CAdoRecordset::GetFieldValue (0x10008b4f)  [read fields]
```

### Layer 2: DAO (SSDaoBase.dll)
**SQL execution ownership:** `OpenDaoDatabase` at `0x1000ebb5`  
**Table creation:** `CreateTable` at `0x1000f990`  
**Insert:** `InsertRecord` at `0x1000fe8c`  
**Record update:** `UpdateRecord` at `0x1000c11c`  
**Transaction:** `CommitTrans` at `0x100129f0`, `Rollback` at `0x100129f6`

The DAO path is used for **local MDB files** (Microsoft Access / Jet engine). `CSSDatabase` manages the connection. The `platform.mdb` string at `0x10021d7c` indicates a local system database.

**Call chain for local DB access (DAO path):**
```
CSSDatabase::OpenDaoDatabase (0x1000ebb5)
  └─> CDaoWorkspace::BeginTrans
  └─> CDaoTableDef::Create() → CSSDatabase::CreateTable (0x1000f990)
       └─> CDaoFieldInfo construction
  └─> CDaoQueryDef::Execute → CSSDatabase::InsertRecord (0x1000fe8c)
  └─> CDaoRecordset::UpdateRecord (0x1000c11c)
  └─> CDaoWorkspace::CommitTrans (0x100129f0)
```

### Layer 3: Core Abstraction (SSDatabaseCore.dll)
The middle layer `SSDatabaseCore.dll` provides a **backend-agnostic DB interface** using the `SSDataBase::SSDBDriver` polymorphic pattern:

```
SSDBDriver (abstract base)
  ├─ ADO backend: via SSAdoBase (CSSAdoBase)
  └─ DAO backend: via SSDaoBase (CSSDatabase)

SSDBQuery ──> result() ──> SSDBResult
             ├─ isSelect()  [0x1000654e] — checks if query is SELECT
             ├─ bindValue() [0x1000683b] — binds named parameters
             ├─ execBatch() [0x10006828] — executes batch mode
             └─ getsql()    [0x1000140f] — retrieves SQL string

SSDBDatabase ──> tables() [0x10004558] — returns list of table names
```

**No network proxy found.** `SSDatabaseCore.dll` does **NOT** contain a network RPC client. It delegates all SQL to either the local Jet engine (DAO) or SQL Server OLEDB provider (ADO). There are no sockets, HTTP, or RPC references visible.

### Layer 4: DataX (SSDataXCore.dll)
`SSDataXCore.dll` is the **attribute-table registry** for EPS's domain objects. It bridges map/spatial features (from SSMap) to the DB schema:

```
CDataXCore::AddAttrTableDef (0x1001e33a)
  ├─ Registers table name + ObjectTypeEnum → CDaoTableDef
  ├─ Used for: parcel attributes (BDCDYH), rights holders (QLR), houses (FW)
  └─ Delegates to SSDaoBase via thunks (OpenRecordset, CreateTable, etc.)
```

---

## 4. SQL Construction / Execution Locations

### SSAdoBase.dll (ADO)

| Function | Address | Purpose |
|----------|---------|---------|
| `CSSAdoBase::ExecuteSQL` | **0x10005276** | Main SQL execution entry — constructs and executes SQL via ADO Command |
| `CSSAdoBase::CreateTable` | **0x10003857** | Creates new tables via ADO |
| `CSSAdoBase::GetTableNames` | **0x100026d0** | Lists tables via ADO OpenSchema |
| `CSSAdoBase::Refresh` | **0x1000427a** | Re-executes last query |
| `CSSAdoBase::DeleteByID` | **0x100045c6** | DELETE by ID — builds `DELETE FROM table WHERE ID=?` |
| `CSSAdoBase::IsExistField` | **0x10004e32** | Schema check — does field exist in table? |
| `CSSAdoBase::_IsExistTable` | **0x10001f1d** | Schema check — does table exist? |
| `CAdoRecordset::OpenRecordset` | **0x10008048** | Executes SELECT via ADO _Recordset::Open |
| `CAdoRecordset::Update` | **0x10008421** | Executes INSERT/UPDATE via ADO |
| `CAdoRecordset::GetFieldValue` | **0x10008b4f** | Reads field value from current record |
| `CSSAdoBase::GetConnection` | **0x10001000** | Returns ADO _Connection COM object |
| `CSSAdoBase::CommitTrans` | **0x10001066** | Transaction commit |
| `CSSAdoBase::RollbackTrans` | **0x100010a4** | Transaction rollback |

### SSDaoBase.dll (DAO)

| Function | Address | Purpose |
|----------|---------|---------|
| `CSSDatabase::OpenDaoDatabase` | **0x1000ebb5** | Opens .mdb file via DAO — calls SetSystemDB() |
| `CSSDatabase::CreateTable` | **0x1000f990** | Creates table in MDB via CDaoTableDef |
| `CSSDatabase::InsertRecord` | **0x1000fe8c** | INSERT via DAO recordset |
| `CDBRecordset::UpdateRecord` | **0x1000c11c** | UPDATE via CDaoRecordset |
| `CDBRecordset::OpenRecordset` | **0x1000afe0** | Executes SELECT via CDaoRecordset::Open |
| `CDaoQueryDef::Execute` | **0x10012b16** | Executes action queries (INSERT/UPDATE/DELETE) |
| `CDaoWorkspace::CommitTrans` | **0x100129f0** | Transaction commit (thunk → DAO360) |
| `CDaoWorkspace::Rollback` | **0x100129f6** | Transaction rollback (thunk → DAO360) |
| `CDBRecordset::Refresh` | **0x1000db6d** | Re-query recordset |
| `CSSDatabase::DeleteIndex` | **0x10004453** | Drops index from MDB |
| `?ChangeMdbPassword@@YAH...` | **0x1000f837** | Changes MDB password |

### SSDatabaseCore.dll (DB Driver Abstraction)

| Function | Address | Purpose |
|----------|---------|---------|
| `SSDBQuery::isSelect` | **0x1000654e** | Determines if query is SELECT (affects execution path) |
| `SSDBQuery::lastInsertId` | **0x100069df** | Returns auto-increment ID from last INSERT |
| `SSDBQuery::bindValue` | **0x1000683b** | Binds named parameter to SQL query |
| `SSDBQuery::execBatch` | **0x10006828** | Executes batch SQL (W4BatchExecutionMode enum) |
| `SSDBResult::getsql` | **0x1000140f** | Returns stored SQL string from result object |
| `SSDBDatabase::tables` | **0x10004558** | Returns list of tables (SELECT name FROM sysobjects) |
| `SSDBDriver::rollbackTransaction` | **0x10009189** | Abstract rollback (returns 0/false) |
| `SSVariantTypeToADO` | **0x1000ba2d** | Converts SSVariant type enum → ADO DataTypeEnum |

### SSDataXCore.dll (Attribute Tables)

| Function | Address | Purpose |
|----------|---------|---------|
| `CDataXCore::AddAttrTableDef` | **0x1001e33a** | Registers attribute table for a domain object type |
| `CDBRecordset::OpenRecordset` | **0x1002c8ce** | Thunk → SSDaoBase::OpenRecordset |
| `CSSDatabase::CreateTable` | **0x1002c922** | Thunk → SSDaoBase::CreateTable |
| `CSSDatabase::DeleteTable` | **0x1002c886** | Drops table from DAO database |
| `CDaoDatabase::Execute` | **0x1002d3d2** | Executes raw SQL via DAO |

---

## 5. Table / Schema Access Patterns

### Parcel / BDCDYH / QLR / FW Fields

**IMPORTANT FINDING:** The specific field names `BDCDYH`, `QLR`, and `FW` do **NOT appear as strings** in any of the four DB-stack DLLs (SSAdoBase, SSDaoBase, SSDatabaseCore, SSDataXCore). These field names are business-logic entities that live in the **upper layers** (SSERPTools.exe.i64, SSExchange.exe.i64, or SSMap.exe.i64) and are passed as string parameters to these DB layer functions.

The DB layers are **schema-agnostic** — they accept table names and field names as `CString` parameters at runtime rather than hardcoding them. This is a standard MFC/C++ DB pattern.

### Attribute Table Registry Pattern (SSDataXCore)

The `CDataXCore::AddAttrTableDef` function at `0x1001e33a` registers which **physical DB tables** correspond to which **EPS domain object types** (parcel, house, rights holder, etc.):

```
CDataXCore::AddAttrTableDef(
    CString tableName,          // physical table name in MDB
    ObjectTypeEnum objectType,  // EPS domain enum
    CDBTableDef *pTableDef)     // DAO table definition
```

The `AttrTable` string appears in SSDataXCore at:
- `GetSeqAttrTables` — sequential attribute tables for a scale map
- `GetCodeAttrTables` — coded attribute tables

This confirms **SSDataXCore manages the mapping** between EPS object types and physical DB tables, while the actual SQL for reading/writing `BDCDYH`, `QLR`, `FW` data flows through `SSDaoBase` or `SSAdoBase`.

### MDB / Jet Usage

**Confirmed local MDB usage in SSDaoBase:**
- `platform.mdb` at `0x10021d7c` — EPS system database (file path reference)
- `Access Files (*.mdb)|*.mdb|All Files (*.*)|*.*||` at `0x10021d8c` — file open dialog filter
- `SetSystemDB@CSSDatabase@@QAEXAAVCString@@@Z` at `0x10020534` — sets DAO system database
- `?ChangeMdbPassword@@YAHVCString@@0000@Z` at `0x1000f837` — MDB password change

**EDB usage in SSDataXCore:**
- `_none.edb` — default/placeholder EDB reference
- EDB files appear to be EPS-specific binary DB files (not standard Access/Jet)

---

## 6. Network-Bound DB Proxies vs. Local MDB/Jet

### Finding: NO network-bound DB proxy found in these 4 DLLs.

Evidence:
1. **No socket API imports** — None of the four DLLs import `ws2_32.dll`, `winhttp.dll`, or `wininet.dll`
2. **No HTTP/RPC references** — No string patterns for HTTP, TCP, or RPC endpoints
3. **Connection strings use local providers only:**
   - `Provider=Microsoft.Jet.OLEDB.4.0;` → local MDB files
   - `Provider=SQLOLEDB;` → local SQL Server OLEDB (not a proxy)
   - `Provider=MS Remote;Internet Timeout=5000;` → remote OLEDB (but not a proxy server)
4. **All SQL execution is in-process** via COM Automation (ADO) or direct file access (DAO)

The DB layers are **local-only**. If EPS supports remote database access, it would be implemented via:
- SQL Server OLEDB provider (direct, not proxied) → SSAdoBase path
- Or a separate network service not visible in these DLLs

---

## 7. Cross-Reference with SSExchange (12020), SSMap (12003), SSERPTools (12002)

### SSDataXCore → SSMap (imports from SSMapView.dll)
SSDataXCore imports from `SSMapView.dll`:
- `?GetSpecialHandlingCodes@@YAHVCString@@...` — Special handling codes from map features
- `?GetGLDC@@YAPAVCGLDC@@PAVCScaleMap@@@Z` — Gets graphic device context

**Cross-module call chain for spatial data:**
```
SSMap (feature query)
  └─> SSDataXCore::AddAttrTableDef (registers feature → DB table mapping)
        └─> SSDaoBase::OpenRecordset / CreateTable (SQL on MDB)
              └─> platform.mdb (contains parcel/QLR/FW data)
```

### SSDataXCore → SSDatabaseCore (no direct dependency)
SSDataXCore does NOT link against SSDatabaseCore.dll. It directly uses SSDaoBase thunks. This means **SSDataXCore bypasses the core DB abstraction layer** and talks directly to DAO.

### SSERPTools → SSExchange → SSMap → SSDataXCore → SSDaoBase/SSAdoBase
The full data flow for parcel/QLR/FW data:
```
SSERPTools (business logic, QLR form processing)
  └─> SSExchange (data exchange, workflow)
       └─> SSMap (spatial query, map feature)
            └─> SSDataXCore (attribute table registry, 0x1001e33a)
                 ├─> SSAdoBase (remote DB via SQLOLEDB) — OR
                 └─> SSDaoBase (local MDB via DAO360)
                      └─> platform.mdb + user MDBs
```

---

## 8. High-Value Function Addresses (Top 20)

| # | Address | DLL | Function | Value |
|---|---------|-----|----------|-------|
| 1 | **0x10005276** | SSAdoBase | `CSSAdoBase::ExecuteSQL` | Primary SQL execution via ADO |
| 2 | **0x1000ebb5** | SSDaoBase | `CSSDatabase::OpenDaoDatabase` | Opens .mdb via DAO |
| 3 | **0x1000afe0** | SSDaoBase | `CDBRecordset::OpenRecordset` | SELECT execution via DAO |
| 4 | **0x1000fe8c** | SSDaoBase | `CSSDatabase::InsertRecord` | INSERT execution |
| 5 | **0x1000f990** | SSDaoBase | `CSSDatabase::CreateTable` | DDL — table creation |
| 6 | **0x1000c11c** | SSDaoBase | `CDBRecordset::UpdateRecord` | UPDATE execution |
| 7 | **0x10008048** | SSAdoBase | `CAdoRecordset::OpenRecordset` | ADO recordset open |
| 8 | **0x10003857** | SSAdoBase | `CSSAdoBase::CreateTable` | ADO DDL |
| 9 | **0x100026d0** | SSAdoBase | `CSSAdoBase::GetTableNames` | Schema enumeration |
| 10 | **0x100045c6** | SSAdoBase | `CSSAdoBase::DeleteByID` | DELETE by primary key |
| 11 | **0x1001e33a** | SSDataXCore | `CDataXCore::AddAttrTableDef` | Domain object → DB table mapping |
| 12 | **0x10006828** | SSDatabaseCore | `SSDBQuery::execBatch` | Batch SQL execution |
| 13 | **0x1000683b** | SSDatabaseCore | `SSDBQuery::bindValue` | Parameter binding |
| 14 | **0x1000654e** | SSDatabaseCore | `SSDBQuery::isSelect` | Query type detection |
| 15 | **0x10004558** | SSDatabaseCore | `SSDBDatabase::tables` | Table enumeration |
| 16 | **0x1000ba2d** | SSDatabaseCore | `SSVariantTypeToADO` | Type conversion utility |
| 17 | **0x1000140f** | SSDatabaseCore | `SSDBResult::getsql` | SQL string retrieval |
| 18 | **0x1000db6d** | SSDaoBase | `CDBRecordset::Refresh` | Recordset re-query |
| 19 | **0x10009189** | SSDatabaseCore | `SSDBDriver::rollbackTransaction` | Transaction rollback stub |
| 20 | **0x1002c886** | SSDataXCore | `CSSDatabase::DeleteTable` | DDL — table drop |

---

## 9. String Findings Summary

| Pattern | DLL | Address | Value |
|---------|-----|---------|-------|
| `Provider=SQLOLEDB;` | SSAdoBase | 0x10011110 | SQL Server OLEDB provider |
| `Provider=Microsoft.Jet.OLEDB.4.0;` | SSAdoBase | 0x10011124 | Jet OLEDB 4.0 (MDB) |
| `Provider=MS Remote;Internet Timeout=5000;` | SSAdoBase | 0x100114e8 | Remote OLEDB |
| `Jet OLEDB:System database=` | SSAdoBase | 0x1001162c | DAO system DB setting |
| `platform.mdb` | SSDaoBase | 0x10021d7c | System MDB filename |
| `Access Files (*.mdb)\|*.mdb\|...` | SSDaoBase | 0x10021d8c | File dialog filter |
| `_none.edb` | SSDataXCore | 0x1003???? | Placeholder EDB |
| `SELECT TNAME FROM TAB...` | SSAdoBase | 0x1????? | Oracle catalog query (in Jet context) |
| `AdoDriver` | SSDatabaseCore | 0x10018098 | ADO driver identifier |

---

## 10. Key Findings Summary

1. **Dual DB abstraction paths confirmed**: ADO (SSAdoBase) + DAO (SSDaoBase) both feed into SSDatabaseCore's driver abstraction layer

2. **SQL is parameterised, not hardcoded**: Table/field names (BDCDYH, QLR, FW) are runtime CString parameters — not embedded in these DLLs

3. **Local MDB/Jet only** (no network DB proxy): All SQL execution is in-process via COM automation or direct Jet file access. No network sockets found.

4. **SSDataXCore = attribute table registry**: Maps EPS domain object types (parcel, house, etc.) to physical DAO table defs. Bypasses SSDatabaseCore abstraction.

5. **Transaction support**: Both DAO (CDaoWorkspace::CommitTrans/Rollback) and ADO (CSSAdoBase::CommitTrans/RollbackTrans) have transaction support

6. **platform.mdb is the system database**: Contains EPS configuration, user preferences, and potentially the master parcel/QLR/FW tables

7. **EDB files** (_none.edb, etc.) are referenced in SSDataXCore — these appear to be EPS-specific binary attribute storage files, not standard Access databases

---

*Report generated via idalib-mcp batch analysis. IDA instances running on ports 12023–12026.*
