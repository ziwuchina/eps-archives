# EPS ERP Login/Command Chain v2 (Consolidated)

**Date:** 2026-03-23  
**Requested target:** Complete ERP login/command chain (SSCore32 + SSERPTools)  
**Primary gateway requested:** `http://127.0.0.1:11339/mcp`  
**Actual usable live MCP during this run:** `http://127.0.0.1:12001/mcp` (`ida-pro-mcp`) bound to `SSCore32.dll`

---

## 1) What was completed

- Mapped the full command/login chain using:
  - **Current live MCP verification** (SSCore32.dll session)
  - **Earlier same-day captured decompilation reports** in `reports/` (generated when SSERPTools/dispatcher data was accessible)
- Confirmed key dispatcher/login addresses and flow used by EPS ERP commands.
- Confirmed HASP-related imported APIs in SSCore32 live.
- Produced a single consolidated chain below with address/function map and evidence provenance.

---

## 2) Instance/gateway state observed

### 2.1 Requested multi-instance gateway (11339)
- Initially had 4 registered instances (from prior runs):
  - `SSMap.dll`
  - `SSCore32.dll`
  - `SSERPTools.exe`
  - `Eps.exe`
- During this run, `11339` became unavailable (connection refused), so direct `select_instance`/multi-instance proxy flow could not be completed end-to-end again.

### 2.2 Active live MCP used for verification
- `ida-pro-mcp` at `127.0.0.1:12001`
- Current bound session: `SSCore32.dll` (`D:\EPS2026G\SSCore32.dll`)
- `server_health`: imagebase `0x10000000`, auto-analysis ready, Hex-Rays ready.

---

## 3) Complete ERP command/login chain (EPS)

## 3.1 High-level call path

```text
EPS command input (UI) 
  -> CSDLInterface virtual dispatch
    -> CSSERPToolsInterface::ExecFunction (0x1001B4A0)
      -> _mbsicmp(command, "LoginERPDB" / others)
        -> per-command handler
```

## 3.2 Command registration (startup)

- `CSSERPToolsInterface::RegisterCommand` @ **0x1001B120**
- Registers 10 ERP-related command strings (name -> ID mapping), including:
  - `LoginERPDB`
  - `LogoutERPDB`
  - `GetWorkList`
  - `CheckRecordUpl`
  - `WorkSubmit`
  - `CancelAcceptWork` (string variant `CancelAcceptWO` seen in artifacts)
  - `WorkProgressReport`
  - `GetUserRoles`
  - `NewWork`
  - `WorkInfoSet`

## 3.3 Main dispatcher

- `CSSERPToolsInterface::ExecFunction` @ **0x1001B4A0**
- Core behavior (from decompilation artifacts):
  - compares incoming command by `_mbsicmp`
  - enforces ERP login state (`GetERPManager()`)
  - routes to handler function(s)

### Important branches
- `LoginERPDB` -> `sub_10007560` (login dialog + auth material handling)
- `LogoutERPDB` -> `CERPManager::ClearERPManager`
- `GetWorkList` -> `sub_10011130`
- `WorkSubmit` -> `sub_1001DC40` (+ dialog path)
- `CancelAcceptWork` -> `sub_1000EC00`

## 3.4 Login handler chain

- `sub_10007560` @ **0x10007560** is the actual LoginERPDB handler.
- Observed behavior in captured decompilation:
  1. show login dialog (`DoModal`)
  2. allocate/init ERP manager object
  3. call **`CAPIDecrypt`** with hardcoded encrypted blob (`asc_10048224`)
  4. build login payload (prefix/salt + decrypted content + suffix path seen in pseudo)
  5. call `sub_10006E10` (actual remote/login submission path)
  6. on success: set ERPManager fields (`Token`, `InvalidTime`, user/dept/password, etc.)
  7. persist selected user fields to INI (`ERPManager` section)
  8. start timer for token validity checks

## 3.5 Timer / session validity

- `CSSERPToolsInterface::TimerProc` @ **0x1001B370**
- Interval: `0x493E0` (300000 ms = 5 min)
- Compares current time vs ERP token invalid time.
- On expiry: clears ERP manager, kills timer, triggers login path again.

---

## 4) SSCore32 crypt/license findings

## 4.1 CAPIDecrypt symbols (string-level in SSCore32)

Found in SSCore32 strings:
- `?CAPIDecrypt@@YAHPADAAVCString@@@Z`
- `?CAPIDecryptLongString@@YAHPADAAVCString@@@Z`

(At addresses observed in live run: `0x101495be`, `0x101495e1`; these are symbol/string references and were not recognized as function starts by current MCP API state.)

## 4.2 HASP API imports (live-confirmed)

From live `imports_query` on SSCore32:
- `__imp_hasp_login`
- `__imp_hasp_login_scope`
- `__imp_hasp_logout`
- `__imp_hasp_read`
- `__imp_hasp_decrypt`
- `__imp_hasp_get_rtc`
- `__imp_hasp_hasptime_to_datetime`

Import addresses reported around:
- `0x1010ecdc` .. `0x1010ecf0`

### Note on requested `hasp_encrypt`
- `hasp_decrypt` import exists (confirmed).
- `hasp_encrypt` import was **not** found in the live import query for SSCore32 in this run.

---

## 5) SSERPTools / SDL / loginERP string patterns

Using prior same-day captures (when SSERPTools dispatcher database access was available):

- `CSSERPToolsInterface::ExecFunction` @ `0x1001B4A0` (confirmed in artifacts)
- `CSSERPToolsInterface::RegisterCommand` @ `0x1001B120`
- `sub_10007560` as LoginERPDB handler
- command string refs include `LoginERPDB`, `GetWorkList`, `WorkSubmit`, `CancelAcceptWork`/`CancelAcceptWO`

### About `loginERP` vs `LoginERPDB`
- Operational command entered by users is often `loginERP`.
- Internal dispatcher in analyzed artifacts matches against `LoginERPDB` command string.
- This is consistent with command alias/normalization in higher layer before dispatch.

---

## 6) Requested key points checklist

- `list_instances` (4 instances) -> **seen earlier in session context**, but gateway 11339 later unavailable.
- `select_instance` -> partially attempted; full repeat blocked by gateway loss.
- `SSCore32 function sweep` -> **partially live-confirmed** (HASP/CAPI evidence via imports/regex).
- `SSERPTools function sweep` -> **consolidated from same-day captured decompilation artifacts**.
- `get_function_signature / decompile / xrefs_to` ->
  - live MCP at 12001 supported decompile/xrefs but was bound only to SSCore32 and had function-enumeration instability (`func_t.get_name` error in `list_funcs`).
  - dispatcher/login decompilation details therefore sourced from preserved reports.

---

## 7) Final consolidated chain (practical)

```text
[UI command input]
   -> CSDLInterface dispatch
      -> CSSERPToolsInterface::ExecFunction (0x1001B4A0)
         -> if "LoginERPDB": sub_10007560
              -> CAPIDecrypt(...)
              -> sub_10006E10 (login submit)
              -> SetERPManager + token/user/dept/password fields
              -> start TimerProc(5 min)
         -> if "GetWorkList": sub_10011130
         -> if "WorkSubmit": sub_1001DC40
         -> if "CancelAcceptWork": sub_1000EC00
         -> if "LogoutERPDB": ClearERPManager
```

HASP/license substrate in SSCore32 is present via `hasp_*` imports (including `hasp_login` and `hasp_decrypt`), and CAPIDecrypt-related symbols are present in SSCore32.

---

## 8) Evidence files used

- `reports/eps_dispatch_chain_2026-03-23.md`
- `reports/ida_sserptools_full_2026-03-23.md`
- `reports/eps_erp_login_chain_2026-03-23.md`
- live MCP 12001 calls in this run (`server_health`, `imports_query`, `find_regex`, `xrefs_to`)

---

## 9) Caveats

- Requested gateway `11339` was unstable/unavailable during this run; could not fully re-execute multi-instance switch workflow end-to-end.
- Current live MCP environment allowed solid SSCore32 verification, while SSERPTools dispatcher specifics were consolidated from same-day saved decompilation artifacts.
- Function-listing tool in current MCP build shows compatibility issue (`func_t.get_name`), limiting fresh symbol enumeration.
