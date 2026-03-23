# EPS 命令调度链分析报告

**日期**: 2026-03-23
**目标**: Eps.exe 命令输入 → 命令解释 → SSERPTools/SScript 调度链
**IDB**: Eps.exe.i64 (x86, 端口 10000)
**置信度**: 高（基于 IDA MCP 直接反编译证据）

---

## 一、总体架构

EPS 命令系统采用 **三层调度架构**：

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: Eps.exe (UI / 命令窗口)                   │
│   BCGPMiniFrame 命令输入 Edit → 用户输入命令字符串    │
└──────────────────────┬──────────────────────────────┘
                       │ 调用
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 2: CSDLInterface (命令分发基类)               │
│   CSSERPToolsInterface 继承 CSDLInterface            │
│   虚函数: ExecFunction(Str1, id)  ← 字符串路由入口   │
└──────────────────────┬──────────────────────────────┘
                       │ CSDLInterface::ExecFunction 虚调用
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 3: CSSERPToolsInterface (命令实现)            │
│   ExecFunction: 大型 if-else 链, _mbsicmp 比对字符串│
│   RegisterCommand: 向 SDL 注册命令名 + ID            │
└─────────────────────────────────────────────────────┘
```

**关键 DLL**: SSERPTools.dll（SSERPTools.dll!CSSERPToolsInterface）
**相关 DLL**: SSCore32.dll, SScript.dll, SSMap.dll

---

## 二、四个目标命令的字符串引用

| 命令字符串 | 地址 (.rdata) | 数据 xref 数量 | xref 位置 (函数) |
|-----------|--------------|--------------|----------------|
| `LoginERPDB` | `0x10049558` | 4 | sub_100195E0, CSSERPToolsInterface::RegisterCommand, TimerProc, ExecFunction |
| `GetWorkList` | `0x100496d4` | 2 | CSSERPToolsInterface::RegisterCommand, ExecFunction |
| `WorkSubmit` | `0x10049698` | 2 | CSSERPToolsInterface::RegisterCommand, ExecFunction |
| `CancelAcceptWork` | `0x10049678` | 2 | CSSERPToolsInterface::RegisterCommand, ExecFunction |

### 最小可复现证据

```python
# IDA Strings 查询结果（已验证）
list_strings(pattern="LoginERPDB") → 0x10049558: "LoginERPDB"
list_strings(pattern="GetWorkList") → 0x100496d4: "GetWorkList"
list_strings(pattern="WorkSubmit") → 0x10049698: "WorkSubmit"
list_strings(pattern="CancelAcceptWork") → 0x10049678: "CancelAcceptWork"
```

---

## 三、函数级调用链（地址 + 重命名建议）

### 3.1 命令注册链（启动时执行一次）

#### CSSERPToolsInterface 构造 → RegisterCommand
- **0x1001B020** `??0CSSERPToolsInterface@@QAE@XZ` (ctor)
  - 重命名建议: `CSSERPToolsInterface::CSSERPToolsInterface`
  - 调用: `CSDLInterface::CSDLInterface`, `SetModulName("SSERPTools.dll")`, `RegisterCommand()`
  - 设置 vtable → `CSSERPToolsInterface::vftable`

- **0x1001B120** `?RegisterCommand@CSSERPToolsInterface@@AAEXXZ`
  - 重命名建议: `CSSERPToolsInterface::RegisterCommand`
  - 签名: `void __thiscall CSSERPToolsInterface::RegisterCommand(CSSERPToolsInterface *this)`
  - 关键逻辑: 循环调用 `CSDLInterface::RegisterCmd(this, cmdString, cmdId)` 注册 10 个命令:
    - ID=0: `"LoginERPDB"` (0x10049558)
    - ID=1: `"LogoutERPDB"` (字符串 ID 0x10049700)
    - ID=2: `"GetWorkList"` (0x100496d4)
    - ID=3: `"CheckRecordUpl"` (0x100496c4)
    - ID=4: `"WorkSubmit"` (0x10049698)
    - ID=5: `"CancelAcceptWork"` (0x10049678)
    - ID=6: `"WorkProgressReport"` (0x10049668)
    - ID=7: `"GetUserRoles"` (0x10049644)
    - ID=8: `"NewWork"` (0x10049628)
    - ID=9: `"WorkInfoSet"` (0x10049618)

- **0x1002EF1C** `?RegisterCmd@CSDLInterface@@IAEXVCString@@0@Z`
  - 重命名建议: `CSDLInterface::RegisterCmd` (private)
  - 签名: `int __thiscall CSDLInterface::RegisterCmd(CSDLInterface *this, CString cmdName, CString cmdId)`
  - 功能: 将命令名+ID对存入 SDL 命令表（具体表结构待进一步分析）

### 3.2 命令执行链（每次命令调用时）

#### 入口 → CSSERPToolsInterface::ExecFunction
- **虚表调度** (数据段 0x100346F2 等)
  - CScaleMap 继承 CSDLInterface，通过 vtable 调用 `CSDLInterface::ExecFunction`
  - CSSERPToolsInterface 重写此虚函数 → 路由到 `CSSERPToolsInterface::ExecFunction`

- **0x1001B4A0** `?ExecFunction@CSSERPToolsInterface@@UAEPAXVCString@@AAV2@I@Z`
  - 重命名建议: `CSSERPToolsInterface::ExecFunction`
  - 签名: `int __thiscall CSSERPToolsInterface::ExecFunction(CScaleMap **this, unsigned __int8 *Str1, int a3, int a4)`
  - **参数**: `Str1` = 命令名字符串, `a3` = 命令ID（来自RegisterCommand）
  - 关键分支条件（使用 `_mbsicmp` 大小写不敏感比较）:

```
if (!_mbsicmp(Str1, "LoginERPDB"))         → sub_10007560(LoginERPDB处理)
if (!_mbsicmp(Str1, "LogoutERPDB"))        → CERPManager::ClearERPManager
if (!_mbsicmp(Str1, "GetWorkList"))        → sub_10011130
if (!_mbsicmp(Str1, "CheckRecordUpl"))     → sub_10009FE0
if (!_mbsicmp(Str1, "WorkSubmit"))         → WorkSubmit对话框 + sub_1001DC40
if (!_mbsicmp(Str1, "CancelAcceptWork"))   → sub_1000EC00
if (!_mbsicmp(Str1, "WorkProgressReport")) → sub_10017E00
if (!_mbsicmp(Str1, "GetUserRoles"))       → sub_1000F7C0
if (!_mbsicmp(Str1, "NewWork"))            → NewWork对话框 + GetWorkInfo + sub_10014330
if (!_mbsicmp(Str1, "WorkInfoSet"))       → WorkInfoSet对话框
```

### 3.3 各命令具体处理器

#### LoginERPDB 完整链
```
CSSERPToolsInterface::ExecFunction (0x1001B4A0)
  └─判断 _mbsicmp(Str1, "LoginERPDB") == 0
       ├─若 ERPManager 已存在 → AfxMessageBox("已登录")
       └─若未登录 → sub_10007560(0x10007560)  [Login对话框+CAPIDecrypt+SetERPManager]
            ├─调用: CAPIDecrypt(asc_10048224, ...)  ← 硬编码加密字符串（可能是API密钥）
            ├─调用: sub_10006E10 (参数: username, password, dept, ...)
            ├─调用: sub_100071B0
            └─设置: SetERPManager(new CERPManager)
```

#### GetWorkList 完整链
```
CSSERPToolsInterface::ExecFunction (0x1001B4A0)
  └─判断 _mbsicmp(Str1, "GetWorkList") == 0
       ├─若 ERPManager 不存在 → AfxMessageBox("请先登录")
       └─若已登录 → sub_10011130(0x10011130)  [获取工单列表]
```

#### WorkSubmit 完整链
```
CSSERPToolsInterface::ExecFunction (0x1001B4A0)
  └─判断 _mbsicmp(Str1, "WorkSubmit") == 0
       ├─若 ERPManager 不存在 → AfxMessageBox("请先登录")
       └─若已登录 → WorkSubmit对话框
            ├─调用: GetWorkInfo() 获取参数
            ├─调用: sub_1001CDA0 初始化提交数据
            ├─调用: sub_1001DC40(this[14], params...)  ← 实际提交
            └─调用: CBCGPDialog::DoModal 显示提交对话框
```

#### CancelAcceptWork 完整链
```
CSSERPToolsInterface::ExecFunction (0x1001B4A0)
  └─判断 _mbsicmp(Str1, "CancelAcceptWork") == 0
       ├─若 ERPManager 不存在 → AfxMessageBox("请先登录")
       └─若已登录 → sub_1000EC00(0x1000EC00) + sub_1000EBF0
```

---

## 四、Eps.exe 内 vs DLL（SSERPTools/SScriptCore）分工

### 在 Eps.exe (Eps.exe.i64) 内完成
| 功能 | 地址/函数 | 说明 |
|------|----------|------|
| 命令注册 | `CSSERPToolsInterface::RegisterCommand` (0x1001B120) | 注册10个命令名+ID |
| 命令分发入口 | `CSSERPToolsInterface::ExecFunction` (0x1001B4A0) | if-else 路由 |
| LoginERPDB 处理 | `sub_10007560` (0x10007560) | 登录对话框+API调用 |
| GetWorkList 处理 | `sub_10011130` (0x10011130) | 工单列表获取 |
| WorkSubmit 处理 | `sub_1001DC40` (0x1001DC40) | 提交数据处理 |
| CancelAcceptWork | `sub_1000EC00` (0x1000EC00) | 取消接单处理 |
| ERPManager 管理 | `GetERPManager` (0x1000D8F0) / `SetERPManager` | 全局单例管理 |
| CERPManager 类 | 整个 CERPManager 类 | 用户token/密码/角色管理 |
| UI 框架 | BCGPNativeUI 类 | 对话框/Dialog 托管 |

### 转发到 SSERPTools.dll
| 功能 | 说明 |
|------|------|
| 模块名设置 | `CSDLInterface::SetModulName("SSERPTools.dll")` |
| 注册命令到 SDL | `CSDLInterface::RegisterCmd` → 存入 SDL 命令表 |
| 命令执行虚派发 | CSDLInterface vtable → CSSERPToolsInterface::ExecFunction |

> **注意**: Eps.exe.i64 是主程序，SSERPTools.dll 是插件模块，通过 COM 式虚表继承（CSDLInterface → CSSERPToolsInterface）集成。

### 与 SScript/SScriptCore 的关系（置信度: 中）
基于已有报告，SScript.dll 主要负责：
- 脚本解释执行（SDL 命令解释）
- `CSScriptHandleBase::RunScript` 等脚本运行函数
- SScriptCore 可能提供加密/HASP验证

当前分析显示 EPS 命令系统**不直接走 SScript 解释器**，而是直接调用 C++ 类成员函数。SScript 可能用于更底层的脚本或地图脚本。

---

## 五、关键地址速查表

| 地址 | 函数名 | 用途 |
|------|--------|------|
| 0x1001B020 | `CSSERPToolsInterface::CSSERPToolsInterface` | 构造函数，调用 RegisterCommand |
| 0x1001B120 | `CSSERPToolsInterface::RegisterCommand` | 注册10个命令（LoginERPDB=0, GetWorkList=2, WorkSubmit=4, CancelAcceptWork=5） |
| 0x1001B4A0 | `CSSERPToolsInterface::ExecFunction` | **核心分发函数**（102基本块，5300+字节） |
| 0x1002EF1C | `CSDLInterface::RegisterCmd` | SDL内部注册 |
| 0x10007560 | `sub_10007560` | LoginERPDB 实际处理（登录对话框+CAPIDecrypt+API调用） |
| 0x10011130 | `sub_10011130` | GetWorkList 处理（获取工单列表） |
| 0x1001DC40 | `sub_1001DC40` | WorkSubmit 核心提交 |
| 0x1000EC00 | `sub_1000EC00` | CancelAcceptWork 核心处理 |
| 0x1000D8F0 | `GetERPManager` | 获取全局 ERPManager 单例（返回 dword_10049E5C） |
| 0x1002EF28 | `GetGLDC` | 获取 CGLDC 设备上下文（→ SSMap.dll） |
| 0x10049558 | (data) | LoginERPDB 字符串 |
| 0x100496d4 | (data) | GetWorkList 字符串 |
| 0x10049698 | (data) | WorkSubmit 字符串 |
| 0x10049678 | (data) | CancelAcceptWork 字符串 |
| 0x10037668 | (data) | CSSERPToolsInterface vtable 数据指针 |

---

## 六、ExecFunction 反编译片段（核心分支证据）

```cpp
// 0x1001B4A0 - CSSERPToolsInterface::ExecFunction
// 参数: (CScaleMap **this, unsigned __int8 *Str1, int a3, int a4)
// Str1 = 命令名字符串

int __thiscall CSSERPToolsInterface::ExecFunction(CScaleMap **this, unsigned __int8 *Str1, int a3, int a4)
{
  CERPManager *ERPManager; // esi
  // ...
  ERPManager = GetERPManager();          // 0x1000D8F0

  if ( !_mbsicmp(Str1, (const unsigned __int8 *)aLoginerpdb) )  // 0x10049558
  {
    if ( ERPManager )
      AfxMessageBox(&byte_1004974C, 0, 0);  // "已登录" 提示
      goto LABEL_48;
    }
    sub_10007560(this[14]);              // ← LoginERPDB 处理
    if ( GetERPManager() )
      SetTimer(0, 1u, 0x493E0u, CSSERPToolsInterface::TimerProc);
    else
      KillTimer(0, 1u);
    goto LABEL_7;
  }
  if ( !_mbsicmp(Str1, (const unsigned __int8 *)aLogouterpdb) )
  {
    if ( ERPManager )
      CERPManager::ClearERPManager(ERPManager);  // 登出清理
    goto LABEL_7;
  }
  if ( !_mbsicmp(Str1, (const unsigned __int8 *)aGetworklist) )  // GetWorkList
  {
    if ( ERPManager )
    {
      sub_10011130(this[14]);            // ← GetWorkList 处理
      goto LABEL_48;
    }
LABEL_38:
    AfxMessageBox(&byte_10049740, 0, 0); // "请先登录"
    goto LABEL_48;
  }
  // ... CheckRecordUpl ...
  if ( _mbsicmp(Str1, (const unsigned __int8 *)aWorksubmit) )   // WorkSubmit
  {
    if ( !_mbsicmp(Str1, (const unsigned __int8 *)aCancelacceptwo) )  // CancelAcceptWork
    {
      if ( ERPManager )
      {
        std::locale::facet::facet((std::locale::facet *)v19, (unsigned int)this[14]);
        LOBYTE(v37) = 16;
        sub_1000EC00(v19);               // ← CancelAcceptWork 处理
        LOBYTE(v37) = 1;
        sub_1000EBF0(v19);
        goto LABEL_48;
      }
      goto LABEL_38;
    }
    // ...
  }
  else
  {
    if ( !ERPManager ) goto LABEL_38;
    // WorkSubmit 对话框序列
    CString::CString((CString *)&v15);
    GetWorkInfo((struct CString *)&v15, (struct CString *)v17, (struct CString *)&v16);
    sub_1001DC40(this[14], ...);         // ← WorkSubmit 提交
    CBCGPDialog::DoModal((CBCGPDialog *)v20);
    // ...
  }
LABEL_48:
  return ...;
}
```

---

## 七、尚未完全确认的环节（待后续分析）

1. **用户输入 → ExecFunction 的触发路径**: 命令Edit窗口的WM_COMMAND/EN_CHANGE消息如何路由到CScaleMap的CSDLInterface vtable调用尚未完全追踪
   - 置信度: **中-高**（ExecFunction被调用的call site在0x1001B517已确认，但调用者属于ExecFunction自身）
   - 推测: BCGPMiniFrame命令Edit控件通过MFC消息映射触发CScaleMap命令处理

2. **CSDLInterface::RegisterCmd 的内部表结构**: 具体的命令表数据结构未知，命令表在内存中如何存储待分析

3. **SScriptCore/SScript.dll 的交互**: 当前分析显示4个命令不经过SScript解释器，SScript可能用于其他地图脚本命令

---

## 八、结论

EPS 命令调度采用**字符串表驱动 + 虚函数分派**模式：

1. **启动时**: `CSSERPToolsInterface` 构造时通过 `RegisterCommand` 向 SDL 注册10个命令（名→ID映射）
2. **运行时**: 用户在命令窗口输入 → **CSDLInterface 虚表** → `CSSERPToolsInterface::ExecFunction` → `_mbsicmp` 字符串匹配 → 路由到对应 `sub_XXXXXX` 处理函数
3. **LoginERPDB 特殊路径**: 在 `ExecFunction` 中直接判断，若未登录则弹出登录对话框（含CAPIDecrypt），成功后设置全局 `ERPManager` 单例并启动心跳 Timer
4. **所有命令都需要 ERPManager 存在**（即需要先 LoginERPDB），否则弹窗"请先登录"

---

*报告生成: IDA MCP (端口10000) + Eps.exe.i64 反编译证据*
*分析者: OpenClaw Subagent (ida-eps-dispatch-deep)*
