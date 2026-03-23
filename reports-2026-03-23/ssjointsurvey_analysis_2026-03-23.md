# SSJointSurvey.dll Analysis Report
**Date:** 2026-03-23  
**Analyst:** Subagent (id=agent:main:subagent:c00e0f1e-8549-4379-9afe-6615d0f095f1)  
**IDB:** `D:\EPS2026G\SSJointSurvey.dll.i64`  
**MCP Server:** idalib-mcp @ port 12006  

---

## 1. Binary Overview

| Property | Value |
|----------|-------|
| **Module** | SSJointSurvey.dll |
| **Architecture** | 32-bit (x86) |
| **Imagebase** | 0x10000000 |
| **Image Size** | 0x2d0000 (2,864,640 bytes ≈ 2.73 MB) |
| **MD5** | 59d927a15551f1e5c9f6ce3c8c97df17 |
| **Segments** | .text (rx), .idata (r), .rdata (r), .data (rw) |
| **Total Functions** | 5,584 (2,813 named, 2,747 unnamed) |
| **Total Strings** | 5,666 |

**Dependencies (Imported DLLs):**
- `SSRuntimeDialog` — Runtime dialog support
- `SSDataXCore` / `SSDataX` — Data exchange core
- `SScriptCore` / `SScript` — Script engine (VBScript)
- `SSFuncLib` — Function library
- `SSProject` — Project management (`CSDLInterface`)
- `SSMapView` — Map view rendering
- `FunctionCore` — Core geometric functions
- Standard MFC/ATL (CDC, CWnd, CString, etc.)
- ADO (CAdoRecordset, CAdoCommand, CAdoRecord) — Database access

---

## 2. Core Plugin Architecture

### 2.1 Main Interface Class: `CSSJointSurveyInterface`

The DLL's entry point is `CSSJointSurveyInterface` — an EPS plugin COM-style class inheriting from `CDlgBase` (dialog base class). It exposes the standard EPS plugin interface through these key methods:

| Method | Address | Purpose |
|--------|---------|---------|
| `??0CSSJointSurveyInterface@@QAE@XZ` (ctor) | 0x1004c401 | Constructor |
| `ExecFunction` | 0x10055c46 | **Main command dispatcher** — routes all SSJointSurvey commands |
| `ExecFunction_CheckFunction` | 0x1004fd44 | Command existence validator |
| `OnCallBackMessage` | 0x10055c7e | Async callback message handler |
| `OnDraw` | 0x10055d92 | Map drawing callback |
| `BeforeDrawMap` | 0x1004ea6c | Pre-map-draw hook |
| `RegisterCommand` / `RegisterCommand1` | 0x100567a6 / 0x10056774 | Register plugin commands |
| `OnSelectChange` | 0x1005615d | Selection change handler |
| `OnUpdateCmdUI` | 0x100561bd | UI update (ribbon enable/disable) |
| `AddRibbonCategory` / `RemoveRibbonCategory` | 0x1004e858 / 0x1005690e | Ribbon UI integration |
| `RegisterCheckModel` | 0x10056740 | Register quality check models |
| `ShowLinkOutputBar` | 0x10058741 | Output window display |
| `OnAfterLoadData` | 0x10055bb0 | Post-data-load hook |

### 2.2 Command Registration System

Commands are registered in the EPS command system via the string format:
```
$SDL,SSJointSurvey,<CommandName>
```
This is handled by `CSDLInterface::RegisterCmd` (imported from `SSProject`).

---

## 3. Key Classes & Data Managers

### 3.1 Class Hierarchy

```
CSSJointSurveyInterface  (Plugin interface - vtable @ 0x1024e2ed)
├── CDlgBase             (Base dialog, EPS plugin base)
├── CHouseManager        (0x1024e107 - House/building data manager)
├── CLandManager         (0x1024e14a - Land/parcel data manager)
├── ZDParamManager       (0x1024c867 - Survey point parameter manager)
├── FS_ZD_DATA           (0x1024e445 - Field survey ZD data container)
├── FSCM_ZDTK_INFO       (ZDTK map sheet info, vtable @ 0x1024e42c)
├── FSCM_ZDTK_INFOS     (Collection of ZDTK sheets)
├── CSSDatabase          (DAO database wrapper)
├── CDBRecordset         (DAO recordset)
├── CAdoRecordset        (ADO database recordset - ActiveX Data Objects)
├── CProjectBase / CSSLocalDB (Project/project database)
├── CHouseZiRZ           (House self-use area)
├── CHouseLouC / CHouseLouCs (Floor data)
├── CGLDC                (Map display context)
└── CSScriptHandle / CSScriptObject (Script execution)
```

### 3.2 Data Manager Roles

| Manager | Role |
|---------|------|
| **CHouseManager** | Manages house units, floor data, FCT/CGT layers, design areas |
| **CLandManager** | Manages land parcels, ZDT map sheets, cadastral data |
| **ZDParamManager** | Manages ZD (survey point) parameters, grid calculations, TuKuang (plot frame) |
| **FS_ZD_DATA** | Container for individual field survey ZD records (JZD points, etc.) |
| **CSSDatabase** | DAO-based database access (OpenDaoDatabase, CreateRecordset, GetAllRecords) |
| **CAdoRecordset** | ADO-based database access for enterprise data (SQL Server likely) |

---

## 4. Joint Survey Data Flow

### 4.1 Field Data → EPS Database Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  FIELD DATA COLLECTION (GPS / TotalStation / 手簿)           │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  SSJointSurvey.ImportJZD()     [ImportJZD dialog]           │
│  CImportJZDDlg                 [CImportJZDDlg @ 0x1025e618] │
│  → Reads JZD (界址点/Boundary Point) records                │
│  → Fields: ZDGUID, ZDDM, BDCDYH, JZDHQ, JZDHZJ, JZDHZ,    │
│            LZQLRMC, LZZJR, BZZJR, JZQZRQ                   │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  SSJointSurvey.XiangMInfoImport()   [Project Info Import]   │
│  CEngProjectInfoDlg              [Engineering project info] │
│  → Project metadata: XiangMDZ, XiangMDW, XiangMXX         │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  SSJointSurvey.CreateJZDNote()   [JZD annotation creation]  │
│  FS_ZD_DATA::CreateJZDNote()                              │
│  → Auto-generates boundary point annotation labels         │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  CHouseManager / CLandManager  (Floor Data Management)      │
│  → CreateHouseFloorData / CreateFloorBoundGeoList           │
│  → AdjustSameOutlineFloorData / CopySameOutlineFloorData    │
│  → UpdateFloorDataRelation                                  │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  ZDParamManager (ZD Parameter / Grid Processing)             │
│  → CalJZDGridPolygon / CalJZDGridRowColCount               │
│  → FindTuKuang (Plot frame lookup)                          │
│  → FitTK / IsCanPlace                                       │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  CSSDatabase / CDBRecordset   (DAO EDB database)             │
│  → CreateRecordset("SELECT...")                             │
│  → GetAllRecords / UpdateRecord / AddRecord                 │
│  → SaveDatabase                                             │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  EPS EDB DATABASE (Geodatabase)                              │
│  Stored in: Project folder *.edb / *.mdb                    │
│  Tables: ZD__ (ZD records), House__, Land__, etc.           │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 JZD (界址点) Data Schema

**JZD** = 界址点 (Boundary Control Points) — the fundamental unit of cadastral survey

**Key Fields identified from string references:**
```
ID, ZDGUID, ZDDM, BDCDYH, JZDHQ, JZDHZJ, JZDHZ, 
LZQLRMC, LZZJR, BZZJR, JZQZRQ, JZDWSM, ZYQSJXZXSM
```
- `ZDGUID` — Feature globally unique ID
- `ZDDM` —ZD (survey point) code
- `BDCDYH` — 不动产单元号 (Real estate unit number)
- `JZDHQ/HZJ/HZ` — 界址点号 (Boundary point number variants)
- `LZQLRMC` — 邻接权类名称 (Adjacent rights name)
- `LZZJR/BZZJR` — 临宗/被执行人 (Neighbor/obligee)
- `JZQZRQ` — 界址所在区域 (Boundary location area)

---

## 5. Command Reference

All commands registered under `$SDL,SSJointSurvey,`:

| Command Name | String Address | Purpose |
|-------------|---------------|---------|
| `EMOutputFSCGT` | 0x10263d9c | Output FS CGT data |
| `CalDesignArea` | 0x10263dc8 | Calculate design area |
| `CreateDiagram` | 0x10263df4 | Create survey diagram |
| `ProjectInfoEdit` | 0x10263e1c | Edit project info |
| `EMCompressCGT` | 0x10263e54 | Compress CGT data |
| `EMCompressFCT` | 0x10263e9c | Compress FCT data |
| `EMFCVALUEDIM` | 0x10263ecc | FC value dimension |
| `EMCreateDistNote` | 0x10263efc | Create distance annotation |
| `EMCreateSelectHu` | 0x10263f30 | Create selected house |
| `EMCopySelectionObjToFloor` | 0x10263f74 | Copy selection to floor |
| `EMCopyFloorDataToOther` | 0x10263fcc | Copy floor data to other |
| `CreateMidWall` | 0x10264018 | Create mid-wall |
| `EMHideFloorData` | 0x10264070 | Hide floor data |
| `EMShowFloorData` | 0x102640b8 | Show floor data |
| `EMDisplay3DHouse` | 0x10264100 | 3D house display |
| `EMApportionAreaCal` | 0x10264170 | Apportionment area calc |
| `EMApportionEdit` | 0x102641b8 | Edit apportionment |
| `EMOpenFloorData` | 0x102641ec | Open floor data |
| `EMCreateFloorData1` | 0x10264234 | Create floor data (variant 1) |
| `EMCreateFloorData` | 0x10264288 | Create floor data |
| `ZDTEdit` | 0x102642f8 | ZDT (总图) editor |
| `ADDJPGTIAREA` | 0x10264330 | Add JPG TIArea |
| `CMCompressZDT` | 0x10264370 | Compress ZDT |
| `CMJFZDPH` | 0x102643b8 | JZDFZ batch processing |
| `CMADJUSTZDPOS` | 0x102643f8 | Adjust ZD positions |
| `CreateJZDNote` | 0x1026443c | Create JZD annotations |
| `CMJZDJFPH` | 0x1026447c | JZD JF batch processing |
| `CMJZDDZPH` | 0x102644c0 | JZD DZ batch processing |
| `CMCREATEJZD` | 0x102644fc | Create JZD batch |
| `CMOutputZHT` | 0x1026452c | Output ZHT |
| `CMOutputCQShiYQZDT` | 0x10264568 | Output CQ ShiYQ ZDT |
| `CMOutputLinQZDT` | 0x102645b8 | Output LinQ ZDT |
| `CMOutputShiYQZDT` | 0x102645fc | Output ShiYQ ZDT |
| `CMOutputSYQZDT` | 0x10264644 | Output SYQ ZDT |
| `CMDJDCInfoInput` | 0x10264688 | DJDC info input |
| `FloorDispControl` | 0x1026487c | Floor display control |
| `REProjectManager` | 0x102648c0 | Project manager refresh |
| `RESet` | 0x1026498c | Reset |
| `ImportJZD` | 0x10266060 | **★ Import JZD boundary points** |
| `XiangMInfoImport` | 0x10265f84 | **★ Import project info** |

---

## 6. GPS/TotalStation Integration

**Finding: No direct GPS/TotalStation protocol parsing in SSJointSurvey.dll**

- No strings matching "GPS", "GNSS", "RTK", "TotalStation", "全站仪", "GPRMC", "NMEA"
- No direct communication with GPS receivers or total stations
- Instead, field data arrives through **imported files** (likely CSV, TXT, or proprietary formats from field instruments)
- The `ImportJZD` function imports pre-processed boundary point data into the EPS database
- Coordinate transformation handled by `CSSTransCoordinate` class (@ 0x1024c47b)
- Coordinate system handling: `IsEncryptCoord` (@ 0x10255669), `m_nCoordBit` / `m_noCoord` / `m_bCoord` globals

**Conclusion:** SSJointSurvey is NOT directly responsible for raw GPS/TotalStation data collection. It handles the **post-collection import and processing** phase — receiving boundary point data files and integrating them into the cadastral database.

---

## 7. Scripting Support

The DLL integrates with EPS's VBScript scripting engine:
- `ScriptEngineFactory` (@ 0x1023790c) — Singleton script engine manager
- `CSScriptHandle::RunScript` (@ 0x10237a3c) — Execute VBScript
- `CSScriptHandle::RunScriptEx` (@ 0x10237aa0) — Extended script execution
- Script files referenced: `EngProjectInfoEdit.vbs` (@ 0x10280006), `ExportEDB_PMT.vbs` (@ 0x1027f7ad)

---

## 8. SSERPTools Cross-Reference

**SSERPTools.exe (port 12002, 1631 functions) does NOT directly reference SSJointSurvey.dll.**

No strings matching `JointSurvey`, `SSJointSurvey`, `JZD`, `ImportJZD`, `FS_ZD`, `ZDTK`, or `ZDParam` were found in SSERPTools.

**Conclusion:** SSERPTools and SSJointSurvey operate as independent modules. They likely communicate through the shared EPS project database (EDB) rather than direct module calls.

---

## 9. Summary

### What SSJointSurvey.dll Does
SSJointSurvey.dll is the **Joint Survey (联合测绘) core module** for the EPS cadastral survey system. It provides:

1. **JZD Boundary Point Management** — Import, create, annotate 界址点 (boundary control points)
2. **Floor Data Management** — Create and manage floor data (分层数据) for house units
3. **Cadastral Map Production** — Generate ZDT (总图/cadastral maps) and associated annotations
4. **Project Info Integration** — Import engineering project metadata
5. **Database Integration** — Read/write cadastral data to EPS EDB geodatabase via DAO/ADO

### What It Does NOT Do
- Raw GPS/TotalStation data collection (no NMEA, RTCM, or proprietary instrument protocols)
- Direct hardware communication
- Direct integration with SSERPTools

### Data Flow
```
Field File Import (CSV/TXT) → ImportJZD/XiangMInfoImport → 
  CHouseManager/CLandManager → CSSDatabase → EPS EDB Database
```

### Key Entry Points
- `CSSJointSurveyInterface::ExecFunction` @ **0x10055c46** — main command router
- `CSSJointSurveyInterface` vtable @ **0x1024e2ed**
- `ImportJZD` function reference @ **0x10264ce4** / command string @ **0x10266060**
- `CreateJZDNote` @ **0x10264ef8** / command string @ **0x10266014**
