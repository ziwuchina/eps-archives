# SScriptCore COM Script Pipeline (Deep Dive)
Date: 2026-03-23
Target: `SScriptCore.dll` (port 12021)

## Binary facts
- Module: `SScriptCore.dll`
- Arch: x86
- Functions: 98
- Strings: 47
- Core class: `ScriptEngineFactory`

## Exported core API (ordinals)
- `?Instance@ScriptEngineFactory@@QAEPAV1@XZ` @ `0x10001785`
- `?InitializeScriptEngine@ScriptEngineFactory@@QAEXVCString@@@Z` @ `0x10001955`
- `?LoadScript@ScriptEngineFactory@@QAEHVCString@@@Z` @ `0x10001ca5`
- `?RunScript@ScriptEngineFactory@@QAEHVCString@@@Z` @ `0x10001b85`
- `?GetIDOfFunction@ScriptEngineFactory@@QAEHVCString@@PAJ@Z` @ `0x10001e7b`
- `?GetErrorMessages@ScriptEngineFactory@@QAEPAVCStringArray@@XZ` @ `0x10001ca1`

## Confirmed COM pipeline

### 1) Engine initialization (`0x10001955`)
- Converts incoming script engine ProgID string to `BSTR`.
- Calls `CLSIDFromProgID(...)`.
- Calls `CoCreateInstance(...)`.
- Queries script interfaces and binds host site.
- Initializes parser/engine state.
- Uses `HRVerify(...)` on each COM step.

### 2) Script loading (`0x10001ca5`)
- Converts script text to `BSTR`.
- Calls parser entry (`this+76` interface slot, vtable+20).
- On success, calls engine state transition (`this+72`, vtable+20 with arg=2).
- Retrieves script dispatch object (`this+72`, vtable+40 -> `this+80`).
- Attaches dispatch to `COleDispatchDriver`.

### 3) Script execution (`0x10001b85`)
- Parses command script text again via parser interface.
- Runs engine (`this+72`, vtable+20, run-state=2).
- Releases parser/engine COM objects after run.

### 4) Error handling (`0x100017ca`)
`HRVerify` behavior:
- If `HRESULT >= 0`: success.
- Else: formats `COM Error: 0x%08lx`, appends context, stores in internal `CStringArray`.

## Strong evidence this is COM-hosted scripting
Imports include:
- `CLSIDFromProgID`
- `CoCreateInstance`
- `VariantClear`
- `SysFreeString`
- `COleDispatchDriver::AttachDispatch`

Important runtime strings:
- `Scripting Engine Parser not available` @ `0x100040d4`
- `Scripting Engine (` @ `0x10004128`
- `Error running the script` @ `0x1000414c`
- `Error parsing script text` @ `0x1000417c`

## Integration with ERP command chain
`SSERPTools -> ssExcuteFunction (SSCore32) -> SScriptCore ScriptEngineFactory -> COM script runtime`

This explains why HTTP endpoint literals are hard to locate in `SSERPTools`: command execution is delegated into script runtime (COM-hosted), and business request composition happens there.