# EPS ERP 命令链完整分析报告
**日期**: 2026-03-23
**工具**: IDA Pro 9.0 + idalib-mcp (SSERPTools.exe 数据库)
**分析**: CSSERPToolsInterface::ExecFunction + LoginERPDB 完整调用链

---

## 一、整体架构

```
EPS 命令输入窗口
    ↓ WM_SETTEXT("loginERP")
    ↓
CSSERPToolsInterface::ExecFunction(0x1001B4A0)
    ↓ _mbsicmp 路由
    ├─ "LoginERPDB"    → sub_10007560()
    ├─ "LogoutERPDB"  → CERPManager::ClearERPManager()
    ├─ "GetWorkList"  → sub_10011130()
    ├─ "WorkSubmit"    → sub_1001DC40()
    ├─ "CancelAcceptWork" → sub_1000EC00()
    ├─ "WorkProgressReport" → sub_10017E00()
    ├─ "GetUserRoles"  → sub_1000F7C0()
    ├─ "NewWork"       → sub_10014330() + DoModal()
    └─ "WorkInfoSet"   → sub_1001CA00() + DoModal()
```

**注意**: 所有命令之前必须先成功执行 `LoginERPDB`，否则弹"请先登录"错误框。

---

## 二、主分发器: CSSERPToolsInterface::ExecFunction (0x1001B4A0)

**函数签名**:
```cpp
int __thiscall CSSERPToolsInterface::ExecFunction(
    CScaleMap **this,    // this指针
    unsigned __int8 *Str1,  // 命令字符串
    int a3, int a4)
```

**关键伪代码逻辑**:
```cpp
ERPManager = GetERPManager();   // 获取全局单例

// === 命令路由 (case-insensitive MBCS compare) ===

if (!_mbsicmp(Str1, "LoginERPDB")) {
    if (ERPManager) {
        AfxMessageBox("已经登录!");  // 已登录则弹框
        goto LABEL_48;
    }
    sub_10007560(this[14]);        // 调用登录处理
    if (GetERPManager())
        SetTimer(0, 1, 300000, CSSERPToolsInterface::TimerProc); // 启动会话超时检测
    else
        KillTimer(0, 1);
    goto LABEL_7;
}

if (!_mbsicmp(Str1, "LogoutERPDB")) {
    if (ERPManager)
        CERPManager::ClearERPManager(ERPManager); // 登出
    goto LABEL_7;
}

if (!_mbsicmp(Str1, "GetWorkList")) {
    if (ERPManager) {
        sub_10011130(this[14]);   // 获取工单列表
        goto LABEL_48;
    }
    goto LABEL_38;  // 未登录 → 弹错误框
}

if (!_mbsicmp(Str1, "WorkSubmit")) {
    if (ERPManager) {
        // 构造工单信息对话框参数
        sub_1001DC40(this[14], v12, v13[0]); // 工单提交
        CBCGPDialog::DoModal(...);  // 弹出提交对话框
        goto LABEL_48;
    }
    goto LABEL_38;
}

if (!_mbsicmp(Str1, "CancelAcceptWork")) {
    if (ERPManager) {
        sub_1000EC00(v19);
        sub_1000EBF0(v19);  // 取消接单
        goto LABEL_48;
    }
    goto LABEL_38;
}

if (!_mbsicmp(Str1, "WorkProgressReport")) {
    if (ERPManager) {
        sub_10017E00(this[14]);
        goto LABEL_48;
    }
    goto LABEL_38;
}

if (!_mbsicmp(Str1, "GetUserRoles")) {
    if (ERPManager) {
        sub_1000F7C0(v19);   // 获取用户角色
        sub_1000EBF0(v19);
        goto LABEL_48;
    }
    goto LABEL_38;
}

if (!_mbsicmp(Str1, "NewWork")) {
    if (!ERPManager) goto LABEL_38;
    // 构造新工单 → sub_10014330() → DoModal()
    goto LABEL_48;
}

if (!_mbsicmp(Str1, "WorkInfoSet")) {
    sub_1001CA00(0);  // 工单信息设置
    CBCGPDialog::DoModal(...);
    goto LABEL_48;
}

// === 未登录错误 ===
LABEL_38:
    AfxMessageBox("请先登录!");  // 未登录所有命令都弹此框
LABEL_48:
    return 0;
```

**结论**: 这是一个**纯字符串 if-else 路由表**，无任何反射或插件机制。

---

## 三、登录流程: sub_10007560 (LoginERPDB 处理)

**函数签名**: `int __cdecl sub_10007560(CScaleMap *a1)`

**完整调用链**:
```
sub_10007560()
  ├─ CBCGPDialog::DoModal()           → 弹出登录对话框（用户名/密码输入）
  │                                    → 对话框资源: v29[108字节] = CBCGPDialog局部变量
  ├─ operator new(0x20)               → 分配 CERPManager 实例
  ├─ CERPManager::CERPManager()       → 构造 ERP 管理器
  ├─ SetERPManager()                   → 注册全局单例
  ├─ CAPIDecrypt(asc_10048224, password)  → 解密密码 (SSCore32.dll)
  ├─ sub_10006E10()                    → 调用 SScriptCore 执行脚本验证
  │   ├─ CScaleMap::SetShareParameter("ERPManager", "script", "ExecuteScript")
  │   ├─ ssExcuteFunction()            → 实际调用 SScriptCore.dll 的脚本引擎
  │   └─ CScaleMap::GetShareParameter() → 获取脚本执行结果
  ├─ CERPManager::SetToken()           → 存储会话 Token
  ├─ CERPManager::SetUserName()        → 存储用户名
  ├─ CERPManager::SetUserID()          → 存储用户ID
  ├─ CERPManager::SetDeptName()        → 存储部门名称
  ├─ CERPManager::SetPassword()        → 存储密码
  ├─ CScaleMap::WriteIniString("ERPManager", "ERPUsername", username)
  └─ CScaleMap::WriteIniString("ERPManager", "ERPDeptname", deptname)
```

**关键字符串常量** (地址基于 SSERPTools.exe i64):
| 地址 | 字符串 | 用途 |
|------|--------|------|
| `0x10048164` | `""` (空) | 脚本参数 |
| `0x100481E4` | `" "` (空格) | 连接符 |
| `0x100481F8` | `"取消登录"` | 取消按钮文本 |
| `0x100481E8` | `"登录失败%d"` | 失败格式化模板 |
| `0x10048224` | **hardcoded key** | CAPIDecrypt 密钥 |
| `0x10049740` | `"请先登录!"` | 未登录错误 |
| `0x1004974C` | `"已经登录!"` | 重复登录提示 |
| `0x10049720` | 工单提交相关? | 消息框文本 |

---

## 四、CERPManager 单例

**存储内容** (INI 持久化到 EPS 安装目录):
```
[ERPManager]
ERPUsername = <用户名>
ERPDeptname = <部门>
ERPToken    = <会话Token>      ← sub_10006E10 执行后从脚本引擎返回
ERPPassword = <密码(加密)>
```

**核心方法**:
| 方法 | 地址 | 说明 |
|------|------|------|
| `CERPManager()` | 构造函数 | 分配实例 |
| `ClearERPManager()` | 登出 | 清空单例 |
| `SetToken()` | 设置Token | 脚本验证成功后 |
| `SetUserName()` | 设置用户名 | |
| `SetUserID()` | 设置用户ID | |
| `SetDeptName()` | 设置部门 | |
| `SetPassword()` | 设置密码 | |
| `GetERPManager()` | 获取单例 | 全局访问点 |

---

## 五、SScriptCore.dll 脚本调用 (sub_10006E10)

**关键调用**:
```cpp
// 设置脚本参数
CScaleMap::SetShareParameter(a2,
    "ERPManager",      // 模块名
    "",                 // 空字符串
    "ExecuteScript"     // 函数名
);

// 调用脚本执行 (SScriptCore.dll 导出)
ssExcuteFunction();  // ← 这里是 SDL 脚本实际执行入口

// 获取结果
CScaleMap::GetShareParameter(..., &result_string);
```

**结论**: `sub_10006E10` 是通往 SScriptCore.dll 脚本引擎的桥梁。登录验证的实际逻辑在 SDL 脚本里（可能是 `loginERP.sdl` 或类似脚本）。

---

## 六、会话超时检测: CSSERPToolsInterface::TimerProc (0x1001B370)

```cpp
void __stdcall CSSERPToolsInterface::TimerProc(HWND a1, UINT a2, UINT_PTR a3, DWORD a4)
{
    ERPManager = GetERPManager();
    if (ERPManager) {
        TickCount = COleDateTime::GetTickCount();
        // 检测 Token 是否过期
        // 超时则调用 ClearERPManager() 登出
    }
}
```

登录成功后 `SetTimer(0, 1, 300000, TimerProc)` 以 5 分钟间隔检测会话。

---

## 七、关键 API 地址汇总

| 功能 | SSERPTools 地址 | SSCore32 地址 |
|------|----------------|---------------|
| 主分发器 ExecFunction | 0x1001B4A0 | - |
| LoginERPDB 处理 | 0x10007560 | - |
| 脚本调用入口 | 0x10006E10 | - |
| GetWorkList | 0x10011130 | - |
| WorkSubmit | 0x1001DC40 | - |
| CancelAcceptWork | 0x1000EC00 | - |
| CAPIDecrypt | - | (SSCore32 中) |
| hasp_login | - | 0x100B9F40 |
| hasp_login_scope | - | 0x100B9F52 |

---

## 八、关键发现

1. **命令字符串直接硬编码**: ExecFunction 中使用 `_mbsicmp` 直接比较，无加密或变形
2. **CAPIDecrypt 使用硬编码密钥**: `asc_10048224` 为固定密钥，在 SSCore32.dll 中
3. **SDL 脚本执行通过 SScriptCore**: `ssExcuteFunction()` 是实际验证入口
4. **ERPManager 单例模式**: 所有会话状态存储在 CERPManager 全局单例，INI 持久化
5. **登录失败有明确的错误提示**: 对话框 + 格式化错误消息 "登录失败%d"
