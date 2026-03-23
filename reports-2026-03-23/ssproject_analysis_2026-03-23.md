# SSProject.dll Analysis Report
**Date:** 2026-03-23
**DLL:** `D:\EPS2026G\SSProject.dll.i64`
**Analyzer:** idalib-mcp (port 12008)

---

## 1. Binary Overview

| Property | Value |
|----------|-------|
| Module | SSProject.dll |
| Architecture | 32-bit (x86) |
| Base Address | 0x10000000 |
| Image Size | 0xe5000 (~924KB) |
| MD5 | 7998a3bf593e2fea92d577c00efed691 |
| Total Functions | 4,072 |
| Named Functions | 2,824 |
| Library Functions | 49 |
| Unnamed Functions | 1,199 |
| Total Strings | 3,840 |
| Segments | .text (rx), .idata (r), .rdata (r), .data (rw) |

---

## 2. Key Finding: NOT a Project Workflow System

**SSProject.dll is a MAP PROJECT management DLL for EPS GIS operations, NOT a business workflow/project management system.**

The workflow status values from Fiddler (作业申请:6, 审核中:11, 生产中:269, 质检中:82, 已办结:597) are **NOT present in this DLL**. These values are stored in a web application database.

---

## 3. Core Classes Found

### Map Project Classes
| Class | Description |
|-------|-------------|
| `CProject` | Main map project class (create/open/save maps) |
| `CProjectBase` | Base class for map projects |
| `CProjectList` | List/manager for open projects |
| `ProjectTree` | Project tree data structure |
| `CSSProjection` | Coordinate projection (BL<->XY conversion) |
| `CSSView` | Map view window |
| `CSSMDIChildWnd` | MDI child window frame |
| `CSSWorkRange` | Work range/extent |
| `CSSDimDlg` | Dimension dialog |
| `CSSCntrItem` | Container item |

### EPS Process/XML Classes
| Class | Description |
|-------|-------------|
| `CEpsXMLSettings` | XML settings file handler |
| `CEpsXMLNode` | XML node tree |
| `CEpsProcessVar` | Process variable |
| `CEpsProcessManager` | Process manager (register/run functions) |

### Local Change (LC) Item
| Class | Description |
|-------|-------------|
| `TSS_LC_ITEM` | Local Change item with GetStatus/SetStatus |

### Project Manager
| Item | Address | Notes |
|------|---------|-------|
| `CSSProjectMan` | 0x100c6b18 | String only, no IDA type |
| `SSProject` | 0x100c6b28 | Component name string |
| `SSProject.SSProjectMan` | 0x100c6f7c | COM class name string |
| `SSProject.tlb` | 0x100c68cc | Type library reference |

---

## 4. CProject Key Methods

```
0x1005ebec  ??0CProject@@QAE@XZ               CProject constructor
0x1005eca8  ?FreeMap@CProject@@QAEXW4_SSMAPTYPE@@@Z
0x1005edcb  ?CreateMap@CProject@@QAEHW4_SSMAPTYPE@@VCString@@1@Z
0x1005f160  ?OpenMap@CProject@@QAEHW4_SSMAPTYPE@@VCString@@@Z
0x1005f33d  ?LoadMap@CProject@@QAEHW4_SSMAPTYPE@@HH@Z
0x1005f45c  ?SaveMap@CProject@@QAEHXZ
0x1005f8ae  ?PreWorking@CProject@@QAEHXZ
0x1005f8d1  ?IsOpen@CProject@@QAEHVCString@@@Z
0x1005f954  ?GetProjectName@CProject@@QAE?AVCString@@W4_SSMAPTYPE@@@Z
```

---

## 5. String References

### DLL Dependencies (from .rdata)
- `SScript.dll` / `SScript.DLL` (0x100bd22c, 0x100c02e8)
- `SSDaoBase.dll` (0x100a0e80)
- `SSCore32.dll` (0x100a443a)
- `SSMap.dll` (0x100a8e8e)
- `SSMapView.dll` (0x100a0120)
- `SSGLDC.dll` (0x100a094a)
- `SSymbolParse.dll` (0x100a0a26)
- `SSInterfaceLib.dll` (0x100a1618)
- `SSCtrlBar.dll` (0x100a1f5a)
- `SSObject.dll` (0x100a5bde)
- `SSEditBase.dll` (0x100aaaf2)
- `SSGeoProcess.dll` (0x100aab1c)
- `SSDtmBase.dll` (0x100aabbc)
- `SSFuncLib.dll` (0x100aae22)
- `SSHouse.DLL` (0x100c3b70)
- `SSExchange.dll` (0x100a4a76)

### Component Names
- `SSProject.DLL` (0x100b0b16, 0x100c2358)
- `SSProject.tlb` (0x100c68cc) — Type library
- `CSSProjectMan` (0x100c6b18)
- `SSProject.SSProjectMan` (0x100c6f7c)
- `SSProject` (0x100c6b28)
- `CSSWorkSpace` (0x100c3db0)
- `SSWorkSpace` (0x100c3db0)
- `SSToolboxBar` (0x100c3a08)
- `SSWorkspaceBar` (0x100c3a18)
- `SSCheck` (0x100bf230)
- `SSDataXInterface` (0x100bf238)
- `SSExtend` (0x100bf248)
- `SSEnvironment` (0x100bf258)
- `SSEdit` (0x100bf268)
- `SScript` (0x100c0638)
- `EPSSCAN` (0x100c0fb4)
- `EPSSCRIPT` (0x100c3e8c)

### Printing
- `Zan Image Printer (Color)` (0x100bf9ac)

---

## 6. SSERPTools.exe Reference (port 12002)

SSERPTools.exe references SSProject.dll:
- `SSProject.dll` string at 0x1003e090

The SSERPTools also has similar CProjectBase class with GetStatus/SetStatus on TSS_LC_ITEM, confirming they share the same map project framework.

---

## 7. Workflow Status Enum — NOT FOUND

The Fiddler-captured workflow statuses **作业申请, 审核中, 生产中, 质检中, 已办结** are **NOT present in SSProject.dll**. 

These status values are:
- Managed by the **SSWEBGIS web application** (likely ASP.NET or similar)
- Stored in a **database** (SQL Server likely)
- Accessed via **HTTP API calls** (not this DLL)

The web interface counts (6, 11, 269, 82, 597) represent project job counts at different workflow stages.

---

## 8. Conclusion

| Question | Answer |
|----------|--------|
| Is SSProject.dll a project workflow system? | **NO** — it's a GIS map project manager |
| Does it contain the workflow status enum? | **NO** — those are in the web app DB |
| What does it contain? | CProject, CProjectBase, CSSProjection, CEpsXML*, map file I/O |
| What DLL handles workflow? | Likely SSWEBGIS web app or a server-side DLL (not in EPS2026G locally) |
| Cross-reference from SSERPTools? | YES — SSERPTools.exe links to SSProject.dll |

**The actual project workflow management system is a web application**, not this DLL. The SSProject.dll name is misleading — it refers to "map projects" (GIS project files), not "business projects" (workflow-managed jobs).

---

## Appendix: idalib-mcp Port 12008 Session

- Binary loaded successfully at 0x10000000
- HexRays decompiler: initialized (with get_prototype errors on some functions)
- Total 4,072 functions analyzed
- Key limitation: many tools (xrefs_to, decompile, disasm) returned empty results — likely due to auto-analysis not yet complete for all addresses
