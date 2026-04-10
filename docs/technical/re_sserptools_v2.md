# SSERPTools.exe 命令路由逆向（port 10003）

## 0) 目标与环境
- 目标函数：`ExecFunction` @ `0x1001B4A0`
- IDA MCP 代理：`127.0.0.1:11339/mcp`
- 实例端口：`10003`
- 样本：`D:\EPS2026G\SSERPTools.exe`（x86/32-bit）

## 1) check_connection
- `check_connection` 返回：`ok=true, count=4`
- `select_instance(port=10003)` 返回：`selected_port=10003`
- 结论：10003 在线且可访问。

## 2) ExecFunction(0x1001B4A0) 伪代码（提炼版）
```c
int CSSERPToolsInterface::ExecFunction(CString cmd, ..., unsigned int flags)
{
    guard_init();
    erp = GetERPManager();

    if (cmd == "LoginERPDB") {
        if (erp) { AfxMessageBox("already login"); goto out; }
        sub_10007560(this->ctx);                 // 登录流程
        if (GetERPManager()) SetTimer(...TimerProc); else KillTimer(...);
        InvalidateRect(GetGLDC(0)->wnd, ...);
        goto out;
    }

    if (cmd == "LogoutERPDB") {
        if (erp) CERPManager::ClearERPManager(erp);
        InvalidateRect(GetGLDC(0)->wnd, ...);
        goto out;
    }

    if (cmd == "GetWorkList") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        sub_10011130(this->ctx);
        goto out;
    }

    if (cmd == "CheckRecordUpload") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        sub_10009FE0(this->ctx);
        goto out;
    }

    if (cmd == "WorkSubmit") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        GetWorkInfo(...);
        if (has_error) { AfxMessageBox(...); goto out; }
        sub_1001CDA0(0);
        sub_1001DC40(this->ctx, ...);            // 提交流程
        DoModal(...);
        goto out;
    }

    if (cmd == "CancelAcceptWorkOrder") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        sub_1000EC00(...);                       // 取消受理
        goto out;
    }

    if (cmd == "WorkProgressReview") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        sub_10017E00(this->ctx);
        goto out;
    }

    if (cmd == "GetUserRoles") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        sub_1000F7C0(...);
        goto out;
    }

    if (cmd == "NewWork") {
        if (!erp) { AfxMessageBox("not login"); goto out; }
        GetWorkInfo(...);
        if (!has_error) sub_10014330(this->ctx, ...);  // 新建工单入口
        DoModal(...);
        goto out;
    }

    if (cmd == "WorkInfoSet") {
        sub_1001CA00(0);
        DoModal(...);
    }

out:
    guard_fini();
    return 0;
}
```

## 3) ExecFunction 调用边（分发相关）
> 说明：`xrefs_from(0x1001B4A0)` 对函数入口仅返回内部流向；真实 call 边通过 `get_callees(0x1001B4A0)` 提取。

核心分发调用（去除大部分析构/GUI清理噪声）：
- `LoginERPDB` -> `sub_10007560`
- `LogoutERPDB` -> `CERPManager::ClearERPManager`
- `GetWorkList` -> `sub_10011130`
- `CheckRecordUpload` -> `sub_10009FE0`
- `WorkSubmit` -> `GetWorkInfo` -> `sub_1001CDA0` -> `sub_1001DC40`
- `CancelAcceptWorkOrder` -> `sub_1000EC00`
- `WorkProgressReview` -> `sub_10017E00`
- `GetUserRoles` -> `sub_1000F7C0`
- `NewWork` -> `GetWorkInfo` -> `sub_10014330`
- `WorkInfoSet` -> `sub_1001CA00`

## 4) 字符串检索 + xrefs_to 路由定位
### LoginERPDB
- string: `LoginERPDB` @ `0x10049558`
- xrefs_to: `0x100195F9`, `0x1001B15C`, `0x1001B429`, `0x1001B4EF`
- 所属函数：
  - `0x1001B4EF` -> `ExecFunction`（实际分发判断）
  - `0x1001B15C` -> `RegisterCommand`（命令注册）
  - `0x1001B429` -> `TimerProc`
  - `0x100195F9` -> `sub_100195E0`

### GetWorkList
- string: `GetWorkList` @ `0x100496D4`
- xrefs_to: `0x1001B1C9`, `0x1001B5AA`
- 所属函数：
  - `0x1001B5AA` -> `ExecFunction`（分发判断）
  - `0x1001B1C9` -> `RegisterCommand`（命令注册）

### WorkSubmit
- string: `WorkSubmit` @ `0x10049698`
- xrefs_to: `0x1001B233`, `0x1001B622`
- 所属函数：
  - `0x1001B622` -> `ExecFunction`（分发判断）
  - `0x1001B233` -> `RegisterCommand`（命令注册）

补充：
- `WorkSubmitList` @ `0x100497CC` 与 `WorkSubmitParameter` @ `0x100497FC` 仅见 `sub_1001CF70` 引用，不在 `ExecFunction` 一层直接分发。

## 5) 命令注册层（RegisterCommand）
`RegisterCommand` @ `0x1001B120` 明确注册以下命令字符串到统一命令入口：
- `LoginERPDB`
- `LogoutERPDB`
- `GetWorkList`
- `CheckRecordUpload`
- `WorkSubmit`
- `CancelAcceptWorkOrder`
- `WorkProgressReview`
- `GetUserRoles`
- `NewWork`
- `WorkInfoSet`

## 6) 分发树（文本图）
```text
RegisterCommand(0x1001B120)
  -> RegisterCmd("LoginERPDB")
  -> RegisterCmd("LogoutERPDB")
  -> RegisterCmd("GetWorkList")
  -> RegisterCmd("CheckRecordUpload")
  -> RegisterCmd("WorkSubmit")
  -> RegisterCmd("CancelAcceptWorkOrder")
  -> RegisterCmd("WorkProgressReview")
  -> RegisterCmd("GetUserRoles")
  -> RegisterCmd("NewWork")
  -> RegisterCmd("WorkInfoSet")

ExecFunction(0x1001B4A0)
  "LoginERPDB"           -> sub_10007560 -> (SetTimer/KillTimer) -> InvalidateRect
  "LogoutERPDB"          -> ClearERPManager -> InvalidateRect
  "GetWorkList"          -> sub_10011130
  "CheckRecordUpload"    -> sub_10009FE0
  "WorkSubmit"           -> GetWorkInfo -> sub_1001CDA0 -> sub_1001DC40 -> DoModal
  "CancelAcceptWorkOrder"-> sub_1000EC00
  "WorkProgressReview"   -> sub_10017E00
  "GetUserRoles"         -> sub_1000F7C0
  "NewWork"              -> GetWorkInfo -> sub_10014330 -> DoModal
  "WorkInfoSet"          -> sub_1001CA00 -> DoModal
```

## 7) 关键函数地址表
- `0x1001B4A0` - `CSSERPToolsInterface::ExecFunction`
- `0x1001B120` - `CSSERPToolsInterface::RegisterCommand`
- `0x1000D8F0` - `GetERPManager`
- `0x1000EA50` - `CERPManager::ClearERPManager`
- `0x10011130` - `GetWorkList` 分支目标
- `0x10009FE0` - `CheckRecordUpload` 分支目标
- `0x1001DC40` - `WorkSubmit` 提交流程核心
- `0x10017E00` - `WorkProgressReview` 分支目标
- `0x1000F7C0` - `GetUserRoles` 分支目标
- `0x10014330` - `NewWork` 分支目标
- `0x1001CA00` - `WorkInfoSet` 分支目标
- `0x1001CF70` - `WorkSubmitList/WorkSubmitParameter` 引用函数

---
数据落地：
- `reports/re_sserptools_v2_data.json`
- `reports/re_sserptools_v2_extra.json`
- `reports/re_sserptools_v2_funcmap.json`
