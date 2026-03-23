# Batch 7: Eps.exe + Main Geometry DLLs Analysis
**Date:** 2026-03-23 | **Analyst:** subagent | **Ports:** 12027, 12028✗, 12029✗, 12030✓, 12031✓, 12032✓

---

## ⚠️ Critical Finding: DgnV8.dll.i64 and SuperMapX.dll.i64 DO NOT EXIST

### Files Present in D:\EPS2026G\
| File | Size | Status |
|------|------|--------|
| `Eps.exe.i64` | 22.4MB | ✅ Analyzed (port 12027) |
| `DgnV8.dll` | **NOT PRESENT** | ❌ Only `SSDgnAdapter.dll` (24KB adapter) exists |
| `SuperMapX.dll` | 1.3MB | ⚠️ Raw DLL exists, i64 created (port 12031) |
| `SSuperMapAdapter.dll` | 148KB | ✅ Analyzed (port 12032) |
| `SSDgnAdapter.dll.i64` | 265KB | ✅ Analyzed (port 12030) |

**Conclusion:** DgnV8.dll is a proprietary Bentley Systems library not present in the EPS installation. DGN support is handled via the thin SSDgnAdapter.dll shim. SuperMapX.dll itself was successfully analyzed.

---

## 1. Eps.exe — Main Executable (Port 12027) ✅

### Binary Metadata
| Property | Value |
|----------|-------|
| **Architecture** | 32-bit PE |
| **Image Base** | 0x400000 |
| **Image Size** | 0x26d000 (~2.5MB code/data) |
| **Entry Point** | `??0CArea@@QAE@AAV0@@Z` (constructor, not WinMain) |
| **WinMain** | 0x42c702 → calls `AfxWinMain` |
| **MD5** | 887467d385c639845418eab5ed71b821 |
| **Functions** | 2,374 total (1,649 named) |
| **Strings** | 2,573 cached |

### Startup Flow
```
WinMain(0x42c702)
  └─> AfxWinMain (thunk → MFC DLL import)
        └─> MFC Framework:
              InitApplication()   [CWinApp virtual]
              InitInstance()      [CEpsApp override]
              Run()               [message loop]
              ExitInstance()      [cleanup]
```

### MFC Architecture
- **Framework:** MFC (Microsoft Foundation Classes) with **BCGControlBar** (CBCGP*) UI toolkit
- **Application Class:** `CEpsApp` (via `theApp` global — mangled name contains CEpsPointCloud, CEpsImage, etc.)
- **UI:** Uses Ribbon Bar (`CBCGPRibbonBar`), Status Bar (`CBCGPEpsStatusBar`), Frame Windows

### Key Imported Modules
| Module | Purpose |
|--------|---------|
| `SSCtrlBar` | Custom control bars |
| `SSDaoBase` | DAO database access |
| `SSGLDC` | OpenGL display context (CAD rendering) |
| `SSInterfaceLib` | Core interface library |
| `SSMapView` | Map view rendering |
| `SSObject` | Geographic object model |
| `SSymbolParse` | Symbol parsing/rendering |
| `Interface` | Internal interface (CInterfaceView) |

### Key Classes Found
- `CEpsPointCloud` — 3D point cloud data handling (`Load`, `SearchPoint`, `SearchBlock`, `DrawBlock`)
- `CEpsImage` — image data with geo-reference (`SetPixelPerMeter`, `GetImageLeftBottomPos`)
- `CEpsProcessVar` — process-level variables
- `CBCGPEpsStatusBar` — EPS status bar
- `CSSTransCoordinate` — SuperMap coordinate transformation (shared with SuperMapX.dll)
- `CGLDC::TransCoordinate` — OpenGL display coordinate transformation

### Company & Version Information
| Item | Value |
|------|-------|
| **Company** | `Sunway Survey` |
| **Version** | `Eps2016` (string at 0x45a280) |
| **Update URL** | `http://www.sunwaysurvey.com.cn/update` |
| **Registration** | `SoftRegister` registry-based licensing system |
| **License Helper** | `RegisterHelpler` |
| **License Config** | `UseLicFile%d`, `\License` |

### Interesting Configuration Strings
- `EpsMenuScheme` — menu customization scheme
- `UseSystemMenu` — system menu usage
- `CurrentSchemeName` — active UI scheme
- `ProjectWizard` — project creation wizard
- `ApplicationLook` — application visual style
- `DispScale` — display scale settings
- `ExcuteScript` — script execution

### Project/Data Format Strings (from .rdata)
- `EXF(1.0, 2.0)...` — SuperMap Exchange Format versions
- `$SDL,SSProject,Project.Unload` — SDL project commands
- `Project.InsertGridNet` — grid net insertion
- `Project.InsertOuterDs` — outer datasource insertion
- `mapsheet.CreateInnerMapborderLine` — cartographic output
- `$SDL,SuperMapX,SMDataView` — SuperMap data view
- `lay.LinePointXY`, `lay.PointZ`, `lay.DEM` — layer types

### Startup Behavior (Analysis)
**At startup, Eps.exe:**
1. Calls `AfxWinMain` → MFC framework
2. `CWinApp::InitApplication()` — registers window classes, OLE factories
3. `CEpsApp::InitInstance()` — creates the main frame window
4. Shows the main frame with BCGControlBar ribbon UI
5. **No login dialog found** in main executable — login is likely in a DLL or handled by the ERP integration command (`loginERP`)
6. Loads the `SSMapView`, `SSGLDC`, and `SSObject` modules for CAD/GIS display
7. `SoftRegister` system validates license at startup

**EPS command interface:** Uses a command-line style input (Edit control at 0x000B1C2C) for `loginERP`, `logoutERP`, etc.

---

## 2. DgnV8.dll — MicroStation DGN Support

### Status: NOT PRESENT ❌

- `DgnV8.dll` does NOT exist in `D:\EPS2026G\`
- Only `SSDgnAdapter.dll` (24KB) exists — a thin shim/wrapper DLL
- `SSDgnAdapter.dll` imports only: `KERNEL32`, `MFC42`, `MSVCRT`
- `SSDgnAdapter.dll` exports: "SSDgnAdapter.dll" (version string only)

### Conclusion
**DGN v8 format support is NOT built into this EPS installation.** The SSDgnAdapter is just a placeholder. DGN files would need to be imported via external tools or a separate DGN import module.

---

## 3. SuperMapX.dll — SuperMap GIS Core (Port 12031) ✅

### Binary Metadata
| Property | Value |
|----------|-------|
| **Architecture** | 32-bit DLL |
| **Image Base** | 0x10000000 |
| **Image Size** | 0x14a000 (~1.3MB) |
| **Functions** | 4,205 total |
| **Strings** | 1,720 |
| **Built** | ~2012 (from DLL timestamp) |

### Imported Modules
| Module | Purpose |
|--------|---------|
| `SSCore32` | SuperMap core engine |
| `SSDaoBase` | Database access |
| `SSDataXCore` | Data exchange core |
| `SSGLDC` | OpenGL display |
| `SSMapView` | Map view rendering |
| `SSObject` | Geographic objects |
| `SSProject` | Project management |
| `SSymbolParse` | Symbol parsing |
| `SSAdoBase` | ADO database base |
| `SSGeoProcess` | Geometry processing |
| `SSInterfaceLib` | Interface library |
| `NETAPI32` | Network APIs |
| `WS2_32` | Windows Sockets |
| `SunwaySDE` | Sunway Spatial Database Engine |

### Key Classes & Functions
- `CSSTransCoordinate` — coordinate transformation engine
- `CDBRecordset` — database recordset for spatial queries
- `CAdoRecordset` — ADO recordset wrapper
- `CSSLocalDB::GetRecordsetHandle` — local database recordset access
- `CScaleMap::GetWorkSpace` — workspace access
- `CDlgBase::SetCoord` — base dialog coordinate setting
- `CGLDC` — OpenGL display context

### Key Strings
- `SuperMap` — multiple references (version/info)
- `Supermap.soStrings`, `Supermap.soRect`, `Supermap.soStyle` — SuperMap object library
- `Supermap.soQueryDef` — query definition objects
- `SuperMapX.DLL (SuperMap...` — DLL description
- `$SDL,SuperMapX,SMConflictObjColorSet` — SDL config items
- `$SDL,SuperMapX,SMShowCheckOutput` — check output window
- `$SDL,SuperMapX,SMCheckDataImp` — data import checking
- `$SDL,SuperMapX,SMDataView` — data view management

### Functionality
**SuperMapX.dll is the core SuperMap GIS library** providing:
- Spatial dataset management (`Dataset`, `Recordset`)
- Coordinate system transformation (`CSSTransCoordinate`)
- Database connectivity (ADO, SunwaySDE)
- Geometry processing (`SSGeoProcess`)
- Workspace management (`CSSWorkSpace`)
- Map view and display (`SSMapView`, `SSGLDC`)
- Symbol and style management (`soStyle`, `soStrings`)

---

## 4. SSuperMapAdapter.dll — EPS-SuperMap Bridge (Port 12032) ✅

### Binary Metadata
| Property | Value |
|----------|-------|
| **Architecture** | 32-bit DLL |
| **Image Base** | 0x10000000 |
| **Image Size** | 0x26000 (~150KB) |
| **Functions** | 1,185 |
| **Strings** | 769 |

### Imported Modules
| Module | Purpose |
|--------|---------|
| `SSMap` | SuperMap core map library |
| `SSMapView` | Map view rendering |
| `SSObject` | Geographic objects |
| `SSProject` | Project management |
| `SSCore32` | Core engine |
| `SSAdoBase` | ADO base |
| `SSEditBase` | Editing base |
| `SSCtrlBar` | Control bars |
| `SSGLDC` | OpenGL display |
| `SSymbolParse` | Symbol parsing |
| `SmEPSInterface` | **EPS-specific interface** |
| `SunwaySDE` | Sunway SDE |

### Key Classes
- `CSSTransCoordinate` — EPS-specific coordinate transformation
- `CDBRecordset` — SQL recordset (`GetSQLType`, `SetStrSQL`, `GetStrSQL`)
- `CSSLocalDB::GetRecordsetHandle` — local DB access
- `CScaleMap::GetWorkSpace` — workspace
- `CGLDC` — display context

### EPS-SuperMap Integration Points
```
SSuperMapAdapter.dll bridges EPS and SuperMapX:
  ├─ EPS commands: RegisterCmd, RegisterAllFunction, RegisterOneFunction
  ├─ SuperMap objects: Dataset, Recordset, Workspace
  ├─ EPS interface: SmEPSInterface (EPS-specific SuperMap window)
  └─ CEMCVHFUHFViewSuperMapWnd_Scene — 3D scene window class
     CEMCVHFUHFViewSuperMapWnd_WorkspaceTree1 — workspace tree control
```

### Key Strings
- `SuperMap` — multiple window/view references
- `CEMCVHFUHFViewSuperMapWnd_Scene` — 3D scene SuperMap window
- `CEMCVHFUHFViewSuperMapWnd_WorkspaceTree1` — workspace tree view
- `RegisterCmd@CSDLInterface` — SDL command registration
- `RegisterAllFunction@CEpsProcessManager` — EPS process manager function registration

---

## 5. SSDgnAdapter.dll — DGN Adapter (Port 12030) ✅

### Binary Metadata
| Property | Value |
|----------|-------|
| **Architecture** | 32-bit DLL |
| **Image Base** | 0x10000000 |
| **Functions** | 85 |
| **Strings** | 19 |

### Imports
- `KERNEL32`, `MFC42`, `MSVCRT` only

### Status
**This is a thin shim DLL** — not the actual DGN engine. It likely provides stub exports that delegate to DgnV8.dll (not present). Real DGN support would require the actual MicroStation DGN v8 library from Bentley Systems.

---

## Summary

| Component | Type | Functions | Key Finding |
|-----------|------|----------|-------------|
| **Eps.exe** | 32-bit MFC/BCG app | 2,374 | **Eps2016 by Sunway Survey** — no login dialog in main exe; uses command-line ERP login; BCG ribbon UI; CAD/GIS display via SS modules |
| **DgnV8.dll** | — | — | **NOT PRESENT** — DGN v8 support unavailable |
| **SuperMapX.dll** | 32-bit DLL | 4,205 | **Core SuperMap GIS library** — full spatial database, coordinate transform, dataset/recordset, workspace management |
| **SSuperMapAdapter.dll** | 32-bit DLL | 1,185 | **EPS-SuperMap bridge** — registers EPS commands, hosts SuperMap 3D scene and workspace tree windows |
| **SSDgnAdapter.dll** | 32-bit DLL | 85 | **Thin shim** — no real DGN functionality |
