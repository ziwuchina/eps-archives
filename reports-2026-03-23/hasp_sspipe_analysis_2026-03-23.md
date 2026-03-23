# HASP + SSPipe DLL Analysis Report
**Date:** 2026-03-23
**Analyst:** Subagent (idalib-mcp via ports 12013 & 12010)

---

## Part 1: hasp_windows_82156.dll (Port 12013)

### 1.1 Binary Survey — Confirmed as Real HASP Vendor DLL ✅

| Property | Value |
|---|---|
| **Path** | `D:\EPS2026G\hasp_windows_82156.dll.i64` |
| **Type** | 32-bit DLL (Vendor/Driver DLL) |
| **Base Address** | 0x2000000 |
| **Image Size** | 0x476000 (~4.6 MB, not 64MB as described) |
| **MD5** | f1756a15de5ce810f0fa0c70b983114b |
| **SHA256** | 220501551d705e4c6b0ed82fb30a7795cbee423b7a5f9b34e2d671d0acb385d1 |
| **Total Functions** | 6449 |
| **Named Functions** | 935 |
| **Library Functions** | 234 |
| **Total Strings** | 11300 |
| **Segments** | .text (rx), .idata (r), .rdata (r), .data (rw) |

**This is definitively the REAL HASP implementation DLL** — not thin wrappers/stubs. The `hasp_*` functions have real code at predictable export ordinal addresses.

### 1.2 Function Query Results

| Function | Address | Size | Notes |
|---|---|---|---|
| `hasp_login` | 0x22911fb | 0x6d | Main login entry point |
| `hasp_login_port` | 0x22488ed | 0x1e | Network port login |
| `hasp_login_ex` | 0x22212df | 0x36 | Extended login |
| `hasp_login_scope` | 0x21832f2 | 0x3c | Scope-based login |
| `hasp_logout` | 0x2283ebd | 0x14 | Logout |
| `hasp_encrypt` | 0x21fdd5d | 0x26 | Encryption |
| `hasp_decrypt` | 0x2277043 | N/A | Decryption (separate from ordinal entry) |
| `hasp_read` | 0x22784c0 | 0x31 | Memory read |
| `hasp_write` | (export ord 17) | — | Memory write |
| `hasp_get_rtc` | 0x2200f54 | 0x3b | Real-time clock |
| `hasp_get_version` | 0x2139e24 | 0x23 | Version query |
| `hasp_free` | 0x218266f | — | Memory free |
| `hasp_update` | 0x21ba8f0 | — | Dongle update |
| `hasp_get_sessioninfo` | 0x215264e | — | Session info |
| `hasp_hasptime_to_datetime` | 0x21df7ac | — | Time conversion |
| `hasp_datetime_to_hasptime` | 0x21a4cf3 | — | Time conversion |
| `hasp_legacy_encrypt/decrypt` | — | — | Legacy DES-based crypto |

### 1.3 String Search Results

**Sentinel / Aladdin Branding:**
- `"Sentinel HASP"` at 0x23d5980, 0x23d59b0
- `"Global\SafeNet-SentinelSMEM"` (shared memory mutex)
- `"Local\SafeNet-SentinelSMEM0-3"` (local shared memory)
- `"\\.\pipe\SafeNet-SentinelPIPE-%u-%u"` (named pipe)
- `"Global\SafeNet-SentinelHID-"` (HID device)
- `"Aladdin Knowledge Systems\HASP\Driver\Installer"` (installer registry path)
- `"Software\Aladdin\winehasp"` (Linux WINE registry path)
- `"Aladdin\Vid0529&Pid0001&HaspHL"` — **Vendor ID = 529** (confirmed Aladdin)

**HASP HL Constants (hardware lock):**
- `HL_ACCINF`, `HL_AVAIL`, `HL_LOGIN`, `HL_LOGOUT`, `HL_LMLOGIN` (LAN modem login)
- `HL_MEMINF`, `HL_PORTINF`, `HL_RD`, `HL_READ`, `HL_READBL`
- `HL_ABORT`, `HL_CALC`, `HL_CODE`, `HL_ERRMSG`
- `HL_ON`, `HL_OFF`

**Dongle Status Strings:**
- `"UNKNOWN_DONGLE"` at 0x23fa584, 0x23fb140
- `"NO_DONGLE"` at 0x23fa610, 0x23fb1e0

**Cryptographic:**
- `"Microsoft Base Cryptographic Provider v1.0"` — uses Windows CryptoAPI
- `CryptAcquireContextA`, `CryptReleaseContext`, `CryptGenRandom` imported from ADVAPI32
- XML config: `<aes/>` tag, `<keyspec>`, `<keycaps>`

**Login Format Strings:**
- `"haspid=%llu,vendorid=%d,productid=%d,file=%s"`
- `"haspid=%llu,vendorid=%d,file=%s"`
- `"<host_fingerprint type=\"%s\" vendorid=\"%s\" crc=\"%s\">%s</host_fingerprint>"`
- `"filter_vendorid"` — vendor filtering logic

**Port Types (from XML):**
- `<type>USB</type>` at 0x23ce06c
- `<type>serial</type>` at 0x23ce0b4
- `<type>parallel</type>` at 0x23ce0fc

**API Function Names (export table strings):**
`hasp_cleanup`, `hasp_detach`, `hasp_enable_trace`, `hasp_get_info`, `hasp_get_trace`, `hasp_get_size`, `hasp_legacy_set_idletime`, `hasp_legacy_set_rtc`

### 1.4 Decompilation Attempt — Obfuscated Code

Both `hasp_login` (0x22911fb) and `hasp_decrypt` (0x2277043) returned **"Decompilation failed"** from Hex-Rays. This is significant:

- The code appears to use **heavy control-flow obfuscation** (encrypted jump tables, indirect dispatch)
- The `hasp_login` disassembly shows heavy use of `jz/jnz` to opaque predicates and indirect jumps through jump tables (`jpt_*`)
- This is typical of commercial dongle drivers that encrypt/decrypt their own code at runtime to prevent reverse engineering
- The function `hasp_login` uses a **448-byte stack frame** (sub esp, 1B4h) suggesting significant local state

### 1.5 Hardcoded Vendor ID / Encryption Keys

**Vendor ID: 529 (0x211)**
- String: `"Aladdin\Vid0529&Pid0001&HaspHL"` at 0x23e1e99
- PID 0001 = HASP HL product line
- This is the **real Aladdin vendor ID** (529 = Aladdin Knowledge Systems)

**No hardcoded encryption keys found as plaintext strings.** The DLL:
- Uses Windows CryptoAPI (`Microsoft Base Cryptographic Provider v1.0`) for all crypto
- No AES S-box tables visible in string searches
- Likely derives session keys dynamically from dongle challenge-response

### 1.6 Imports (145 total from KERNEL32)

Key imports indicating functionality:
- `CreateFileMappingA`, `MapViewOfFile`, `UnmapViewOfFile` — shared memory IPC
- `OpenSemaphoreA`, `CreateMutexA`, `OpenMutexA` — synchronization for Sentinel SMEM
- `QueryPerformanceCounter`, `GetTickCount` — timing checks (anti-debugging/timing validation)
- `CreateFiberEx`, `ConvertThreadToFiber` — fiber-based execution (code obfuscation)
- `FindFirstFileA`, `GetModuleFileNameA` — system probing
- `GetComputerNameExW`, `GetVersionExA` — machine fingerprinting

### 1.7 Key Findings

1. **This is the REAL HASP encryption DLL**, not a stub. The actual cryptographic operations happen here.
2. **Vendor ID = 529** (Aladdin), PID = 0001 (HASP HL)
3. **Crypto is delegated to Windows CryptoAPI** — no custom crypto algorithms embedded
4. **The code is heavily obfuscated** — decompilation fails, only raw disassembly available
5. **Sentinel SafeNet branding** — SafeNet acquired Aladdin HASP; this DLL bridges both eras
6. **Supports USB, serial, parallel, and network (LM login)** — full HASP HL feature set
7. **Named pipe + shared memory IPC** for inter-process communication with Sentinel drivers

---

## Part 2: SSPipe.dll (Port 12010)

### 2.1 Binary Survey — Confirmed as Pipeline/GIS Module ✅

| Property | Value |
|---|---|
| **Path** | `D:\EPS2026G\SSPipe.dll.i64` |
| **Type** | 32-bit DLL |
| **Base Address** | 0x10000000 |
| **Image Size** | 0x22f000 (~2.2 MB) |
| **MD5** | e80a16b5bd3ced5d37d7e7da1b96efc7 |
| **SHA256** | 3ac04818fb0a866e1120dff16d74f7750d82b2f10fe983f7407616e6a229414b |
| **Total Functions** | 6448 |
| **Named Functions** | 2628 |
| **Library Functions** | 20 |
| **Total Strings** | 4094 |

### 2.2 Core Data Model — Pipeline Classes

**Primary Class: `CPipeNet`** (at 0x10113d11)
- Constructor: `??0CPipeNet@@QAE@PAVCDataSource@@@Z` — takes a `VCDataSource` (data source connection)
- Destructor: `??1CPipeNet@@UAE@XZ`
- Key methods:
  - `Clear()` — clear network
  - `GetState()` — get network state
  - `Init(GeObjList, MarkNoteList)` — initialize with geometry + annotation
  - `GetGeoLayer(int index)` / `GetGeoLayer(CString name)` — get geometry layer by index or name
  - `GetNoteLayer(int index)` / `GetNoteLayer(CString name)` — get annotation/note layer
  - `GetGeoLayerCount()` / `GetNoteLayerCount()` — layer counts
  - `Standardization()` — standardize pipeline network

**Geometry Operator: `CPipeGeoOperator`** (at 0x10116891)
- `Init(ScaleMap, GeObjList)` — initialize geo operator
- `GetGXIDGroup(CStringArray&)` — get all GXID values (pipeline feature IDs)
- `GetLineGeoList(GeObjList&)` — get all line geometries
- `GetLineGeoListByGXID(GeObjList&, CString)` — get line by GXID
- `GetPointGeoList(GeObjList&)` — get all point geometries
- `GetPointGeoListByLine(GeObjList&, GeObjList)` — get points on a line

**Pipeline Cross-Section: `CPipeHdmItem`** (referenced in `GetPipeCutInfo`)
- Used by: `GetPipeCutInfo(CArray<VCPoint3D>&, CSSPtrArray<CPipeHdmItem>&)` — pipeline cut profile
- `VCPoint3D` — 3D point for cross-section

**Scripting: `CPipeScript`** (at 0x101d2ca8)

### 2.3 Function Query Results — Pipeline Feature Functions

| Query | Matches | Key Functions |
|---|---|---|
| `Pipe` | 25+ | `CPipeNet`, `CPipeGeoOperator`, `CPipeScript`, `GetPipeDiameter`, `GetPipeCutInfo`, `GetPipeConfigFile`, `ReadPipeConfig`, `IsPressPipe` |
| `Drain` / `DrainPipe` | 2 | `IsClassOfDrainPipe(CString)`, `IsClassOfDrainPipe(VCGeoBase*)` |
| `Diameter` | 5 | `GetPipeDiameter(CString,CString,PH)` — get pipe diameter |
| `Well` | 3 | `CGxPointOnWell`, `GxPointOnWell` — well-related point features |
| `Hdm` | 10 | `GetPipeCutInfo`, `CPipeHdmItem`, HDM flags and frames |

### 2.4 String Search Results

**Pipeline Feature Classes (MFC/ATL C++ naming):**
- `CGeoBase` — base geometry class (base for all geo objects)
- `CGeoObject` — geo object wrapper
- `CPointObject` — point feature (manholes, valves as points)
- `CLineObject` — line feature (pipes as lines)
- `CLinePos`, `CLinePosIndex` — line position/index helpers
- `CFeatureList` — feature collection
- `CFeatureCode` — feature type code

**Data Layer Classes:**
- `CDataLayer` — generic data layer
- `CAttrRecordset`, `CAttrItem`, `CAttrItemList` — attribute recordset system
- `CMarkNoteList` — annotation/mark list
- `VCDataSource` — vector data source connection

**Database (DAO-based — SSDaoBase):**
- `CDaoDatabase`, `CDBRecordset` — DAO database access
- `CSSDatabase`, `CRecord` — custom SQL database wrapper
- Methods: `GetAllRecords`, `OpenRecordset`, `GetFieldVal`, `SetData`
- Uses DAO parameters and record arrays

**XML Configuration (TinyXML — TiXmlElement):**
- `TiXmlNode`, `TiXmlElement` — XML parsing for config files
- `GetAttribute`, `SetAttribute`, `FirstChildElement`, `NextSiblingElement`
- `GetPipeConfigFile()` returns config file path
- `ReadPipeConfig(CString, CStringArray, CSSPtrArray)` — reads pipeline config

**Symbol/Display (SSymbolParse):**
- `CDataParse`, `MakeNoteSymbolInsertString` — symbol parsing
- `FormatPointDisplayName` — formats display names for point features

### 2.5 Core Pipeline Data Model Summary

```
CPipeNet (Pipeline Network)
├── CDataLayer: GetGeoLayer(i)  → CGeoObject[]  (geometry features)
│   ├── CPointObject  (窨井/阀门/消火栓 as points)
│   ├── CLineObject   (管线/管道 as polylines)
│   └── CGeoBase      (base class with GetDistDir, GetArea, GetLayerName)
├── CDataLayer: GetNoteLayer(i)  → annotation/markup data
├── GXID (CString) — unique feature identifier for each pipe/point
└── CGeoObjList: geometry list

CPipeGeoOperator (Pipeline Geo Operations)
├── GetGXIDGroup() → all GXIDs in network
├── GetLineGeoList() → all pipe lines
├── GetPointGeoList() → all point features (wells, valves)
└── GetPipeDiameter() → diameter by GXID or geometry

CPipeHdmItem (Pipeline Cross-Section / Cut Profile)
└── GetPipeCutInfo() → VCPoint3D[] + CPipeHdmItem[] (断面数据)

Feature Types:
- 管线/管道 (Pipeline) → CLineObject
- 窨井 (Manhole) → CPointObject + CGxPointOnWell
- 阀门 (Valve) → CPointObject
- 给水/排水 (Water/Drainage) → distinguished by IsClassOfDrainPipe + GXID
```

### 2.6 Key Dependencies

**Internal EPS DLLs:**
- `SSProject` — project management, SDL interface
- `SSymbolParse` — symbol parsing and display
- `SSDaoBase` — DAO database abstraction

**No obvious external GIS dependencies** — this is a pure internal EPS pipeline engine using MFC-style C++ classes.

### 2.7 Key Findings

1. **SSPipe.dll is the pipeline calculation and topology engine** — handles pipe networks, geo-operations, and topology
2. **GXID is the central feature identifier** — all pipeline features are indexed by GXID (管线的唯一标识)
3. **DAO database layer** — reads pipeline features from database via SSDaoBase (supports multiple record formats)
4. **Supports drainage/water classification** via `IsClassOfDrainPipe` and `IsPressPipe`
5. **Cross-section/cut profile support** via `CPipeHdmItem` and `GetPipeCutInfo`
6. **Layered architecture**: Geometry layer (geo objects) + Note layer (annotations) separate from business data
7. **Config file support** — reads pipeline configuration via XML, with `GetPipeConfigFile` returning file path
8. **No Chinese strings found** — all text appears to use Unicode IDs or string tables, not embedded Chinese

---

## Appendix: IDA MCP Port Reference

| Port | DLL | Status |
|---|---|---|
| 12013 | hasp_windows_82156.dll.i64 | Active |
| 12010 | SSPipe.dll.i64 | Active |
| 11339 | Gateway (all instances) | Available |
