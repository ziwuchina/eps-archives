# EPS ERP Login Function Chain Analysis Report

**Date:** 2026-03-23  
**Target:** Eps.exe (D:\EPS2026G\Eps.exe) via IDA MCP port 10000  
**Analysis:** Complete function chain for LoginERPDB ERP login workflow

---

## ⚠️ Critical Finding: Target Addresses NOT FOUND

The task specified the following addresses which **do NOT exist** in the current Eps.exe IDB:

| Address | Function | Status |
|---------|----------|--------|
| `0x10007560` | LoginERPDB entry | ❌ NOT FOUND |
| `0x1001B4A0` | ExecFunction dispatcher | ❌ NOT FOUND |

### Evidence

```
IDB Address Range: 0x401000 – 0x430C92
Target Addresses:  0x10007560, 0x1001B4A0  ← These are OUT OF RANGE
```

The target addresses (0x100xxxx) are **far outside** the 0x40xxxx–0x43xxxx range of this Eps.exe binary. The addresses 0x100xxxx are typical for:
- A DLL with imagebase 0x10000000 (e.g., SSCore32.dll, SSMap.dll, SScript.dll)
- A different version/build of Eps.exe compiled with a different base address
- A different EPS module entirely

---

## IDB Metadata

```
File:      D:\EPS2026G\Eps.exe
Arch:      x86 (32-bit)
Hash:      290607dd830f8143964e0d41e5647d195564fb6b375b5562b9938a5697da255c
Functions: 2374 total
Address Range: .text = 0x401000 – 0x432000 (200,704 bytes)
```

---

## Binary Segments

| Segment | Start | End | Size | Perm |
|---------|-------|-----|------|------|
| `.text` | 0x401000 | 0x432000 | 200,704 | r-x |
| `.idata` | 0x432000 | 0x433BF0 | 7,152 | r-- |
| `.rdata` | 0x433BF0 | 0x454000 | 132,112 | r-- |
| `.data` | 0x454000 | 0x45C000 | 32,768 | rw- |

---

## Function Search Results

### Target Functions (NOT FOUND in this IDB)

| Function Name | Address | Found? |
|--------------|---------|--------|
| LoginERPDB | 0x10007560 | ❌ No |
| ExecFunction | 0x1001B4A0 | ❌ No |
| GetWorkList | — | ❌ No |
| WorkSubmit | — | ❌ No |
| CancelAcceptWork | — | ❌ No |

### Name-Based Search Across All 2374 Functions

Pattern searches were performed across all function names for ERP-related keywords:

```
Pattern "login":  0 matches
Pattern "ERPDB":  0 matches
Pattern "ERP":    0 matches
Pattern "GetWorkList": 0 matches
Pattern "WorkSubmit":  0 matches
Pattern "CancelAccept": 0 matches
```

**Note:** All function names in this IDB are MSVC C++ mangled names (e.g., `?SetOccDialogInfo@CWnd@@MAEHPAU_AFX_OCC_DIALOG_INFO@@@Z`). There are no functions with plain-text names like `LoginERPDB`, `ExecFunction`, etc.

---

## What WAS Found in This IDB

### Database-Related Functions
- `?CloseDatabase@CSSDatabase@@QAEHXZ` — CSSDatabase::CloseDatabase
- `?OpenDaoDatabase@CSSDatabase@@QAEHPBD@Z` — Open DAO database
- `?IsEncryptCoord@CSSDatabase@@QAEHXZ` — Encrypted coordinate check
- `?LoadDatabase@CScaleMap@@QAEHABVCDblRect@@VCString@@W4ObjecTypeEnum@@@Z` — Load database
- `?OpenDatabase@CDataSource@@QAEHVCString@@@Z` — Open data source

### String: Eps Database Format
```
0x45A680: "Eps Database(*.edb)|*.edb|"
```
This confirms `.edb` is the EPS proprietary database format.

### Password-Related Function
```
0x453005: ?SetPassword@CStringInput@@QAEXVCString@@@Z
```
Part of `CStringInput` class — likely used in login dialog.

### Relevant Import Modules
- **BCGCBPRO940** — BCGControlBar Pro (UI framework for MFC dialogs/ribbons)
- **SSGLDC.dll** — Graphics library (used for map rendering)
- **SSMapView.dll** — Map view component
- **USER32.dll** — Windows user interface

---

## EPS Command System Context

Based on the broader EPS environment:

### Known EPS Commands (from prior analysis)
- `loginERP` — Login to EPS ERP system (NOT `LoginERPDB`)
- `logoutERP` — Logout from EPS

### Known EPS Classes (present in this IDB)
- `CSSDatabase` — Database management
- `CSSLocalDB` — Local database
- `CStringInput` — String input control (used for login fields)
- `CDBRecordset` — Database recordset with SQL support
- `CScaleMap` — Map/scale management

---

## Analysis of Login-Related XRefs

The closest login-related function found:

**0x42A916** — `?SetOccDialogInfo@CDialog@@MAEHPAU_AFX_OCC_DIALOG_INFO@@@Z`  
(MFC CDialog::SetOccDialogInfo — NOT the ERP login function)

**XRefs TO 0x42A916:** 14 cross-references from .rdata string table entries (not code)  
**XRef FROM 0x42A916:** Points to 0x432DA8 (data section)

---

## Conclusion

### Why the Target Functions Were Not Found

1. **Address range mismatch:** The target addresses (0x10007560, 0x1001B4A0) are in the 0x100xxxx range, but this Eps.exe only uses addresses 0x401000–0x430C92. This suggests the task was written based on a **different binary or database**.

2. **The functions likely reside in a DLL:** The 0x100xxxx address range is typical for DLLs (imagebase 0x10000000). The EPS ERP logic may be in **SSCore32.dll**, **SSMap.dll**, or **SScript.dll** — but those IDA instances are not currently running (ports 10001–10003 are not accessible).

3. **Different naming convention:** The task expects clean function names (`LoginERPDB`, `ExecFunction`, `GetWorkList`), but this IDB uses only MSVC C++ mangled names. The actual function implementations may exist but under different names.

### Recommended Next Steps

1. **Open SSCore32.dll (port 10001)** — the core library is most likely to contain `LoginERPDB` and `ExecFunction`
2. **Open SSMap.dll (port 10002)** — map-related ERP workflow functions
3. **Open SScript.dll (port 10003)** — script engine with 1641 SDL commands
4. **Check if a newer IDB exists** for Eps.exe with the 0x100xxxx address range

---

## Appendix: Tool Invocation Log

All IDA MCP tools were tested and confirmed functional:

```
get_metadata         ✅ Returns correct IDB metadata
list_functions       ✅ 2374 functions, paginated
get_function_signature ❌ "function not found" for 0x10007560, 0x1001B4A0
get_callers          ❌ "function not found" for target addresses
get_callees          ❌ "function not found" for target addresses
xrefs_to             ✅ Returns empty xref list for out-of-range addresses
get_basic_blocks     ❌ "function not found" for target addresses
decompile            ❌ "function not found" for target addresses
list_strings         ✅ 2573 total strings, pattern search works
list_imports         ✅ 1762 imports
list_exports         ✅ 422 exports
list_segments        ✅ 4 segments
```
