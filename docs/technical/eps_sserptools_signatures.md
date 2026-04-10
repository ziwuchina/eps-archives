# EPS SSERPTools 函数签名恢复报告

## 任务结果
- IDA MCP 连接检查：`check_connection => ok=true, count=4`
- 实例选择：`select_instance(port=10003) => selected_port=10003`
- 已反编译：
  - `0x1001B4A0` (`ExecFunction` 主分发)
  - `0x1002F156` (`ssExcuteFunction`，thunk)
  - 以及 `ExecFunction` 相关 top callees 和关键路由函数（LoginERPDB/GetWorkList/WorkSubmit 相关）
- 已产出头文件：`reports/eps_sserptools_signatures.h`

## 关键路由结论
- `LoginERPDB`：`ExecFunction(0x1001B4A0)` -> `sub_10007560` -> `SetTimer/KillTimer` + `InvalidateRect`
- `GetWorkList`：`ExecFunction(0x1001B4A0)` -> `sub_10011130`
- `WorkSubmit`：`ExecFunction(0x1001B4A0)` -> `GetWorkInfo` -> `sub_1001CDA0` -> `sub_1001DC40` -> `DoModal`
- `RegisterCommand`：定位到 `0x1001B120`，注册上述命令字符串到统一分发入口
- `ssExcuteFunction`：`0x1002F156` 为 thunk，转发到导入符号 `?ssExcuteFunction@@YAHVCString@@00PAX1@Z`

## xrefs_from 与 top10 decompile 说明
- 直接 `xrefs_from(0x1001B4A0)` 以控制流边为主，不能完整表示 call 图。
- 对“被调用函数集合”采用 `get_callees(0x1001B4A0)` 补充，并按 `call_count` 优先反编译 top 10。

## 产出头文件（完整）

```c
#ifndef EPS_SSERPTOOLS_SIGNATURES_H
#define EPS_SSERPTOOLS_SIGNATURES_H

/*
 * SSERPTools.exe signature recovery (IDA MCP, instance port 10003)
 * Sample: D:\EPS2026G\SSERPTools.exe (x86)
 *
 * Notes:
 * - These are reverse-engineered prototypes for static analysis and hook stubs.
 * - Some signatures are inferred from call sites and mangled names.
 */

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Opaque MFC/BCG classes used by recovered prototypes. */
typedef struct CString CString;
typedef struct CWnd CWnd;
typedef struct CDialog CDialog;
typedef struct CBCGPDialog CBCGPDialog;
typedef struct CScaleMap CScaleMap;
typedef struct CERPManager CERPManager;
typedef struct CSDLInterface CSDLInterface;
typedef struct CSSERPToolsInterface CSSERPToolsInterface;

/* Lightweight Windows handle aliases used in this module. */
typedef void* HWND_HANDLE;
typedef void* TIMER_HANDLE;

/* Command routing context inferred from ExecFunction command branches. */
typedef struct EPS_CommandRouteContext {
    CSSERPToolsInterface* self;
    CScaleMap* runtime_ctx;       /* typically this[14] in decompilation */
    CERPManager* erp;             /* from GetERPManager() */
    const uint8_t* command_ascii; /* compared via _mbsicmp */
    uint32_t flags;               /* last scalar arg observed in dispatcher */
} EPS_CommandRouteContext;

/* WorkSubmit/NewWork staging values from GetWorkInfo and dialog pipeline. */
typedef struct EPS_WorkSubmitArgs {
    CString* err_msg;
    CString* work_id;
    CString* extra;
    void* submit_dialog;          /* sub_1001CDA0 return object */
} EPS_WorkSubmitArgs;

/* [0x1001B120] CSSERPToolsInterface::RegisterCommand
 * Register all command strings into CSDLInterface::RegisterCmd.
 */
void __thiscall EPS_RegisterCommand(CSSERPToolsInterface* self);

/* [0x1001B4A0] CSSERPToolsInterface::ExecFunction
 * Main command dispatcher for LoginERPDB/GetWorkList/WorkSubmit/... branches.
 */
int __thiscall EPS_ExecFunction(
    CSSERPToolsInterface* self,
    const uint8_t* command_ascii,
    int reserved_arg,
    uint32_t flags
);

/* [0x1002F156] ssExcuteFunction thunk -> import ?ssExcuteFunction@@YAHVCString@@00PAX1@Z
 * Inferred readable form: execute script bridge with 3 CString-like args + 2 context pointers.
 */
int __cdecl EPS_ssExcuteFunction(
    CString* arg1,
    CString* arg2,
    CString* arg3,
    void* ctx_in,
    void* ctx_out
);

/* [0x1000D8F0] GetERPManager */
CERPManager* __cdecl EPS_GetERPManager(void);

/* [0x1000EA50] CERPManager::ClearERPManager */
void __thiscall EPS_ClearERPManager(CERPManager* self);

/* [0x10007560] sub_10007560
 * LoginERPDB branch core flow.
 */
int __cdecl sub_10007560(CScaleMap* runtime_ctx);

/* [0x10011130] sub_10011130
 * GetWorkList branch core flow.
 */
void __cdecl sub_10011130(CScaleMap* runtime_ctx);

/* [0x1001CDA0] sub_1001CDA0
 * WorkSubmit dialog object construction (CWnd owner observed).
 */
void* __thiscall sub_1001CDA0(void* self, CWnd* owner);

/* [0x1001DC40] sub_1001DC40
 * WorkSubmit route target, consumes parsed work fields and launches submit dialog flow.
 */
void __thiscall sub_1001DC40(void* self, int work_id_like, char a3, char a4);

/* [0x10014330] sub_10014330
 * NewWork route target, similar staging path as WorkSubmit.
 */
int __thiscall sub_10014330(void* self, int a2, CWnd* owner);

/* [0x1001CF70] sub_1001CF70
 * WorkSubmitList/WorkSubmitParameter downstream parser and ERP script bridge.
 */
void __thiscall sub_1001CF70(CBCGPDialog* self);

/* [0x10009FE0] sub_10009FE0 - CheckRecordUpload route */
void __cdecl sub_10009FE0(CScaleMap* runtime_ctx);

/* [0x1000EC00] sub_1000EC00 - CancelAcceptWorkOrder route */
void __cdecl sub_1000EC00(void* ctx);

/* [0x10017E00] sub_10017E00 - WorkProgressReview route */
void __cdecl sub_10017E00(CScaleMap* runtime_ctx);

/* [0x1000F7C0] sub_1000F7C0 - GetUserRoles route */
void __cdecl sub_1000F7C0(void* ctx);

/* [0x1001CA00] sub_1001CA00 - WorkInfoSet route */
void* __thiscall sub_1001CA00(void* self_or_null);

#ifdef __cplusplus
}
#endif

#endif /* EPS_SSERPTOOLS_SIGNATURES_H */
```

## 产物路径
- `reports/eps_sserptools_signatures.h`
- `reports/eps_sserptools_signatures.md`
- 原始采集数据：
  - `reports/eps_sserptools_sig_raw.json`
  - `reports/eps_sserptools_sig_extra_raw.json`

## 下一步建议（3条）
1. 对 `?ssExcuteFunction@@YAHVCString@@00PAX1@Z` 目标 DLL 入口继续逆向，确认 3 个 `CString` 参数是值传递还是引用传递，收敛为最终 ABI。  
2. 在 IDA 中给 `sub_10007560 / sub_10011130 / sub_1001DC40 / sub_10014330` 批量补类型（`set_function_prototype`），再回看 `ExecFunction` 伪代码可读性会明显提升。  
3. 增加 `LoginERPDB/GetWorkList/WorkSubmit` 的动态 hook 日志（入参/返回值/耗时），验证本头文件在真实运行中的签名一致性。
