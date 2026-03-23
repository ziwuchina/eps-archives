# SScriptCore.dll / SScript.dll / SScript SDL Engine Analysis

**Date:** 2026-03-23  
**Analyst:** Subagent (IDA MCP via SSERPTools.exe.i64 @ port 12002, SSCore32.dll.i64 @ port 12001)  
**Report:** C:\Users\Administrator\.openclaw\workspace\reports\sscript_analysis_2026-03-23.md

---

## 1. Overview

SSERPTools.exe does NOT directly link against `SScriptCore.dll` or `SScript.dll`.  
Instead, the EPS SDL scripting engine is organized as:

| DLL | Role | Key Exports |
|-----|------|------------|
| **SSCore32.dll** | Core engine | `ssExcuteFunction`, `CAPIDecrypt`, `CAPIDecryptLongString`, all `CEpsXMLSettings` functions |
| **SSEditBase.dll** | Script object base | `CSScriptObject` (class), `CSScriptHandleBase` (class), `RegisterFunction` |
| **SSAdoBase.dll** | DB utilities | `CAPIDecrypt` (import wrapper → SSCore32), `CAPIEncrypt` |
| **SSProject.dll** | SDL interface | `CSDLInterface` class with `RegisterCmd` |
| **SSDaoBase.dll** | Database | Recordset, DAO classes |

The DLL that actually contains the SDL runtime is named **`SscriptDll`** (loaded dynamically by `ssExcuteFunction`).

---

## 2. `ssExcuteFunction` — Dynamic DLL Loader

**Location in SSCore32.dll:** `0x1000fd8c` (SSERPTools import thunk: `0x10036628`)

**Signature:**
```cpp
int __cdecl ssExcuteFunction(
    int a1,           // CString* — module name (e.g., "SscriptDll")
    LPCSTR lpProcName,// procedure name (e.g., "ExcuteScript")
    char a3,          // parameter 3 (CString&)
    int a4,           // parameter 4 (CString&)
    char *a5          // parameter 5 (CString*)
)
```

**Behavior:**
1. If the module name has no dot (`.`), appends `.dll` → `SscriptDll.dll`
2. Builds full path: `GetModulePath() + "\\" + module_name + ".dll"`
3. Loads with `AfxLoadLibrary()` — if fails, replaces `.dll` → `.dll` (typographic fallback!)
4. Gets procedure with `GetProcAddress(Library, lpProcName)`
5. If proc not found: shows `Format("Error loading %s:%s", module, procname)` message box
6. Calls the resolved procedure address with params a3/a4/a5 cast to CStrings

**Import in SSERPTools.exe:**
```
IAT entry 0x10036628: ?ssExcuteFunction@@YAHVCString@@00PAX1@Z  from "SSCore32"
Thunk at 0x1002f156 in SSERPTools (for internal cross-refs)
```

---

## 3. Script Call Entry: `sub_10006E10`

**Address:** `0x10006E10` in SSERPTools.exe

This is the **loginERP script trigger**. It sets up parameters and calls `ssExcuteFunction`.

**Parameters passed to `ssExcuteFunction`:**
| Param | String Constant | Value |
|-------|----------------|-------|
| a1 (module) | `aSscriptDll` | `"SscriptDll"` |
| lpProcName | `aExcutescript` | `"ExcuteScript"` |

**Additional setup via `CScaleMap::SetShareParameter`:**
| Key | Value |
|-----|-------|
| `aErpmanager` (global CString at `0x10049E18`) | From `CERPManager` singleton |
| `aScript` | `"Script"` |
| `aExcutescript` | `"ExcuteScript"` |

**Internal call chain in sub_10006E10:**
```
sub_10006E10
  ├─ CScaleMap::SetShareParameter(...)  ← sets ERPManager token/password as shared params
  ├─ ssExcuteFunction("SscriptDll", "ExcuteScript", ...)  ← loads SscriptDll.dll
  ├─ CScaleMap::GetShareParameter(...)  ← retrieves script output
  ├─ sub_10006670(...)  ← validation/result checking
  ├─ sub_10025980(...)  ← dialog/UI update (×3)
  └─ sub_10025380(...)
```

**`sub_10006670` (0x10006670):** Validation function that returns 0 on failure. Uses `Ctl3dAutoSubclass`, string comparison (`_mbsicmp`), and internal object management.

---

## 4. CAPIDecrypt — Password Decryption

**Location:** `0x10033344` in SSCore32.dll  
**Import in SSERPTools:** `0x10036584` → `?CAPIDecrypt@@YAHPADAAVCString@@@Z` from `SSAdoBase`

### Algorithm

```cpp
int __cdecl CAPIDecrypt(char *password_out, CString *encrypted_str)
```

**Step 1:** Check if string starts with magic header `"3523C2988a911"` (at position 2)
**Step 2:** If YES → set output to `"admin"` and return 1 **(HARDCODED BACKDOOR)**

**Step 3:** If NO:
- Remove the magic header from the encrypted string
- For each 2-char hex pair: `decrypted_byte[i] = hex_val[i] XOR password[i % password_len]`
- Returns 1 on success, 0 if format invalid

**Summary:** XOR-based encryption with repeating-key equal to the user's password.  
If the encrypted password string starts with `"3523C2988a911..."` (position 2), access is granted as "admin" regardless of password.

---

## 5. `CERPManager` — User Credential Storage

**Singleton accessor:** `GetERPManager() @ 0x1000d8f0`

**Key methods discovered:**

| Address | Method | Notes |
|---------|--------|-------|
| `0x1000e740` | `GetToken()` | Returns CString at `this+4` |
| `0x1000e760` | `SetToken(CString*)` | Sets token field |
| `0x1000e820` | `GetUserNameA()` | Returns username CString at `this+?` |
| `0x1000e890` | `GetUserID()` | Returns user ID |
| `0x1000e900` | `GetDeptName()` | Returns department |
| **0x1000e970** | `GetPassword()` | Returns CString at `this+24` ← **encrypted password** |
| `0x1000e990` | `SetPassword(CString*)` | Stores encrypted password |

**Password storage:** The password is stored **encrypted** at offset `this+24` in the CERPManager object. The plain-text is NOT stored; it must be decrypted via `CAPIDecrypt`.

---

## 6. CSScriptHandleBase / CSScriptObject

**Discovered classes in SSERPTools (from SSEditBase.dll imports):**

```
CSScriptHandleBase  @ 0x10018dc0 (ctor)
  ├─ RunScript()    @ 0x10018d90  — void*, UINT version
  ├─ RunScript()    @ 0x10018da0  — LPCSTR version
  └─ RunScriptEx()  @ 0x10018db0  — with extra param

CSScriptObject      @ 0x1002f054 (ctor)
  ├─ RegisterFunction()  @ 0x1002f042
  └─ GetFunctionList()   @ 0x1002f048
```

These are MFC-based classes with message maps (`?messageMap@CSScriptObject@@1UAFX_MSGMAP@@B`).

---

## 7. DLL Import Summary for SSERPTools.exe

**Full import table (key DLLs):**

| Module | Key Imports |
|--------|------------|
| SSCore32 | `ssExcuteFunction`, `CAPIDecrypt`, `CEpsXMLSettings::*`, `ReadEpsIniString`, `ReadEpsIniInt`, `OrderArray` |
| SSAdoBase | `CAPIDecrypt` (→ SSCore32), `CAPIEncrypt` |
| SSEditBase | `CSScriptObject::*`, `CSScriptHandleBase::*` |
| SSProject | `CSDLInterface` (constructor, destructor, RegisterCmd) |
| SSGLDC | Graphics DC |
| SSMapView | `GetGLDC` |
| SSObject | Geo/Point object methods |
| SSymbolParse | Symbol parsing |
| SSDaoBase | Database DAO |
| WS2_32 | Networking (gethostbyname, etc.) |

**Notable ABSENCE:** No direct import of `SScript.dll` or `SScriptCore.dll`. The actual SScript DLL (`SscriptDll.dll`) is loaded **dynamically at runtime** by `ssExcuteFunction`.

---

## 8. Password Flow Summary

```
User enters password → 
  CLoginDialog::OnOK() → 
    CAPIDecrypt(encrypted_pwd_from_DB) → 
      XOR decrypt with password as key → 
        CERPManager::SetPassword(encrypted_str) → 
          loginERP command → 
            sub_10006E10() → 
              CScaleMap::SetShareParameter(ERPManager_token) → 
                ssExcuteFunction("SscriptDll", "ExcuteScript", ...) → 
                  LoadLibrary(GetModulePath + "\SscriptDll.dll") → 
                    GetProcAddress("ExcuteScript") → 
                      Call DLL entry point with CERPManager credentials
```

**Backdoor:** Any password whose encrypted form (hex) contains the string `3523C2988a911` at position 2 will be accepted as "admin" by `CAPIDecrypt`.

---

## 9. Key Addresses Reference

| Address | Binary | Item |
|---------|--------|------|
| `0x1000fd8c` | SSCore32.dll | `ssExcuteFunction` implementation |
| `0x10033344` | SSCore32.dll | `CAPIDecrypt` implementation |
| `0x100335bd` | SSCore32.dll | `CAPIDecryptLongString` |
| `0x10036628` | SSERPTools.exe | IAT: `ssExcuteFunction` import from SSCore32 |
| `0x10036584` | SSERPTools.exe | IAT: `CAPIDecrypt` import from SSAdoBase |
| `0x1002f156` | SSERPTools.exe | Thunk ref to `ssExcuteFunction` |
| `0x10006E10` | SSERPTools.exe | Script call entry (loginERP handler) |
| `0x10006670` | SSERPTools.exe | Called by sub_10006E10 — validation |
| `0x1000e740` | SSERPTools.exe | `CERPManager::GetToken` |
| `0x1000e970` | SSERPTools.exe | `CERPManager::GetPassword` |
| `0x10018d90` | SSERPTools.exe | `CSScriptHandleBase::RunScript` (SSEditBase) |
| `0x1002f042` | SSERPTools.exe | `CSScriptObject::RegisterFunction` (SSEditBase) |

---

## 10. Open Questions / Further Analysis

1. **Exact path of `SscriptDll.dll`** — The DLL path is built via `GetModulePath() + "\\SscriptDll.dll"`. Need to determine EPS installation directory.
2. **`ExcuteScript` signature** — The actual procedure signature in `SscriptDll.dll` needs to be determined (what params does it expect?).
3. **`loginERP.sdl` file** — No direct reference found yet. The SDL script file name/path may be loaded from configuration or embedded in `SscriptDll.dll` resources.
4. **Caller of sub_10006E10** — xrefs_to returned a bug (`'func_t' object has no attribute 'get_name'`). The function that calls the loginERP script entry needs to be identified (likely in a dialog/command handler).
5. **`CAPIDecryptLongString`** — `0x100335bd` in SSCore32 — handles longer passwords (>~40 chars).
6. **`CSDLInterface::RegisterCmd`** in SSProject.dll — likely registers the "loginERP" command name to the script engine.

---

*Analysis performed via IDA MCP (SSERPTools.exe.i64 @ :12002, SSCore32.dll.i64 @ :12001)*
