# EPS AddClip Safe Replay Runbook

## Goal
Safely replay one call of:
- `SScript.dll!?AddClipBoardObjToMap@CSSProcess@@QAEJNN@Z`

without using hook-internal reentry (reduces EPS crash risk).

## Preconditions
- Keep only one active EPS UI process if possible.
- Use a PID that is attachable by Frida.
- User can click the target function button once after monitor starts.

## Command
```powershell
python scripts/eps_safe_addclip_replay_once.py --pid <PID> --max-replay 1 --timeout 300 --out D:\EPS2026G\Temp\safe_addclip_replay_once_result_<PID>.json
```

Example:
```powershell
python scripts/eps_safe_addclip_replay_once.py --pid 19476 --max-replay 1 --timeout 300 --out D:\EPS2026G\Temp\safe_addclip_replay_once_result_19476.json
```

## Expected Success Signals
- Event sequence includes:
  - `ADDCLIP_ENTER` with `shouldReplay: true`
  - `ADDCLIP_RET` with `ret: 0x1`
  - `DEFER_REPLAY_OK`
  - then another `ADDCLIP_ENTER/RET` pair (`shouldReplay: false`)
- Final state in JSON:
  - `replayCount: 1`
  - `replayOk: 1`
  - `replayErr: 0`
  - `fusedOff: false`

## Safety Controls
- One-shot replay (`--max-replay 1` default).
- Replay only when original call returns success (`ret == 0x1`).
- If replay throws, fuse is set (`fusedOff=true`) and further replay stops.

## Known Pitfall
- Running when monitor window has ended will capture nothing.
- Re-run command, then click target button again.

## Zero-click Trigger (After One Capture)
When a recent context file exists (contains `ADDCLIP_ENTER` with `thisp/tid`), you can trigger AddClip without clicking UI again.

Command:
```powershell
python scripts/eps_zero_click_trigger_once.py --pid <PID> --tid <UI_TID> --context D:\EPS2026G\Temp\auto_replay_inhook_<PID>.json --out D:\EPS2026G\Temp\eps_zero_click_trigger_once_result.json
```

Example (verified on PID 19932):
```powershell
python scripts/eps_zero_click_trigger_once.py --pid 19932 --tid 18612
```

Success criteria:
- Console shows `success True`
- Output JSON `winner.call.ret == "1"`
- Output JSON `winner.hitAddClipRet1 == true`

## One-command Auto PID (recommended)
If EPS PID may change after restart, use auto wrapper:

```powershell
python scripts/eps_zero_click_resident_auto.py --timeout 300 --post-success-wait 5
```

What it does:
- Finds the main `eps.exe` process automatically (highest RSS)
- Verifies Frida attachability
- Starts resident bridge (`eps_zero_click_resident.py`) with safe defaults
- Writes result/context JSON to `D:\EPS2026G\Temp\`

## True One-click (no manual button click)
Use direct trigger wrapper to execute AddClip without clicking the toolbar button:

```powershell
python scripts/eps_oneclick_direct_auto.py --max-candidates 300 --max-tries 120 --out D:\EPS2026G\Temp\eps_oneclick_direct_result.json
```

How it works:
- Auto-select EPS pid + UI thread
- Scan runtime candidates for valid `thisp`
- Try candidates in UI thread until first `ret=1`
- Stop immediately on first success and write detailed attempts JSON

Verified artifacts:
- Seeded success: `D:\EPS2026G\Temp\eps_oneclick_direct_result_test.json`
- No-seed success: `D:\EPS2026G\Temp\eps_oneclick_direct_result_noseed.json`
