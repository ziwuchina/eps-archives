# Batch16 NetHASP/License Transport Chain Proof (2026-03-23)

## 0) Scope and Evidence Basis

Analyzed modules:
- `D:\EPS2026G\AdjustBase.dll`
- `D:\EPS2026G\hasp_windows_82156.dll` (plus prior i64 reverse notes)
- `D:\EPS2026G\SSCore32.dll`
- Cross-reference: `D:\EPS2026G\ArcSDEX.dll`

Raw machine extract is saved at:
- `reports/batch16_nethasp_transport_raw_2026-03-23.json`

---

## 1) Imports and API Surface Related to Network/License

## 1.1 AdjustBase.dll

- Static imports do **not** include `WS2_32.dll` / `NETAPI32.dll` / `SETUPAPI.dll`.
- Static imports include `KERNEL32.dll!LoadLibraryA` + `GetProcAddress`.
- This matches a **delayed/dynamic API resolution** pattern.

Observed dynamic-network related symbol strings in module data:
- `socket`, `sendto`, `recvfrom`, `closesocket`, `ioctlsocket`
- `SetupDiGetClassDevsA`

Interpretation: AdjustBase likely resolves socket/SetupAPI entrypoints dynamically at runtime instead of through static IAT.

## 1.2 hasp_windows_82156.dll

- Static imports are mainly from `KERNEL32.dll` (no direct static `WS2_32.dll` import in this sample).
- Prior deep analysis confirms exported HASP API set includes:
  - `hasp_login`, `hasp_login_scope`, `hasp_login_ex`, `hasp_login_port`
  - `hasp_get_info`, `hasp_encrypt`, `hasp_decrypt`, `hasp_read`, `hasp_logout`
- Similar to AdjustBase, network stack identifiers appear in strings, indicating runtime dispatch or internal transport abstraction.

Observed dynamic-network related symbol strings:
- `socket`, `sendto`, `recvfrom`, `closesocket`, `ioctlsocket`
- `gethostbyname`, `gethostbyaddr`, `WSAStartup`

## 1.3 SSCore32.dll

- SSCore32 imports `hasp_windows_82156.dll` **by ordinal**, not by name.
- Resolved ordinal mapping from export table evidence:
  - `ord_13` -> `hasp_login`
  - `ord_14` -> `hasp_logout`
  - `ord_15` -> `hasp_read`
  - `ord_2` -> `hasp_decrypt`
  - `ord_23` -> `hasp_login_scope`
  - `ord_5` -> `hasp_get_rtc`
  - `ord_8` -> `hasp_hasptime_to_datetime`

This demonstrates SSCore32 as a **wrapper/bridge layer** into hasp runtime for session and crypto/time primitives.

## 1.4 ArcSDEX.dll (cross-reference)

- Static imports explicitly include:
  - `WS2_32.dll`: `WSAStartup`, `WSACleanup`, `gethostname`, `gethostbyname`
  - `NETAPI32.dll`: `Netbios`

This confirms real network host discovery capabilities exist elsewhere in EPS stack too, but ArcSDEX appears auxiliary/cross-reference for this task.

---

## 2) Required String Evidence (Quoted)

Confirmed in `AdjustBase.dll` / `hasp_windows_82156.dll` string corpus:

- `classic_get_sesskeyinfo: LowAPI (API_NH_GET_CURRENT_SERVER) status %u`
- `HLSERVER` / `-HLSERVER*` / `hlserver`
- `NH_TCPIP.NH_SERVER_ADDR`
- `NH_TCPIP.NH_SERVER_NAME`
- `<serveraddress>` and `</serveraddress>`
- `NH_COMMON.NH_NETBIOS`
- `NH_COMMON.NH_TCPIP`

These strings are strong NetHASP network-discovery and server-binding indicators.

---

## 3) SSCore32 Wrapper Mapping -> hasp_windows Behavior

Observed practical call relation:

1. SSCore32 imports hasp runtime as `hasp_windows_82156.dll` by ordinal.
2. Ordinal resolution proves SSCore32 directly uses:
   - session open/close (`hasp_login`, `hasp_logout`, `hasp_login_scope`)
   - token memory read (`hasp_read`)
   - crypto primitive (`hasp_decrypt`)
   - RTC/time conversion (`hasp_get_rtc`, `hasp_hasptime_to_datetime`)
3. Prior export inventory of `hasp_windows_82156.dll` confirms availability of higher-level calls:
   - `hasp_get_info`, `hasp_encrypt`, `hasp_decrypt`, `hasp_login*`

So the wrapper model is:
- **SSCore32 = EPS-facing wrapper/session manager**
- **hasp_windows_82156 = actual Sentinel/HASP implementation and transport core**

Note on `hasp_get_info`/`hasp_encrypt` in SSCore32:
- In this sample, SSCore32 IAT resolution visibly confirms `hasp_login` + `hasp_decrypt` class of calls by ordinal.
- `hasp_get_info`/`hasp_encrypt` are confirmed exported and used in EPS ecosystem, but not directly surfaced in the specific SSCore32 ordinal subset seen in this dump.

---

## 4) Corrected Capability Boundary (What is and is not possible)

## 4.1 What can be LAN-shared

- NetHASP server discovery/selection over LAN is supported (`HLSERVER`, `NH_TCPIP.NH_SERVER_ADDR/NAME`, `NH_COMMON.NH_NETBIOS`, serveraddress XML).
- Concurrent client-side login to server-managed license slots is supported (`hasp_login_scope`, classic current-server query path).

## 4.2 What cannot be remotely delegated (without protocol-level proxying)

- The local EPS process cannot "delegate" arbitrary dongle crypto session to a random remote host through simple API forwarding.
- HASP session handle semantics are local-process/local-runtime state; handle reuse across process/network boundaries is not a native feature.
- Blind replacement with only `regcode`/serial is insufficient; runtime challenge-response/session integrity is still enforced by hasp runtime.

## 4.3 What depends on local dongle session/runtime state

- `hasp_login`-created session validity and handle lifecycle.
- Subsequent protected operations (`hasp_decrypt`, memory read, RTC/time conversion) bound to successful authenticated session context.
- Vendor-scope/license-scope filtering and seat/accounting enforced in runtime (not just app-layer checks).

In short: **License seats can be LAN-consumed, but cryptographic/session trust is anchored in HASP runtime state, not freely remoted by app logic.**

---

## 5) Practical Verification Checklist (Ops, 5 steps)

1. On client, force known server target and compare behavior:
   - set `HLSERVER` / server address config, then launch EPS.
2. Capture baseline license login path:
   - verify app reaches `hasp_login` success (via logs/trace if available) and records server endpoint.
3. Disconnect/alter LAN path (or wrong server):
   - confirm fallback/search logic triggers and login failure is deterministic.
4. Reconnect to valid NetHASP server:
   - verify `hasp_decrypt`/protected feature path resumes only after fresh successful login.
5. Validate non-delegability assumption:
   - attempt using stale session context after runtime restart; confirm session-dependent operations fail until re-login.

---

## 6) Bottom Line

- NetHASP transport evidence is solid: `HLSERVER`, `API_NH_GET_CURRENT_SERVER`, `NH_TCPIP.*`, `<serveraddress>`.
- SSCore32 is not the full transport engine; it bridges to `hasp_windows_82156.dll` by ordinal for session/crypto/time operations.
- Correct boundary: **LAN license sharing yes; remote delegation of trust/session no (without full HASP-compatible proxy semantics).**
