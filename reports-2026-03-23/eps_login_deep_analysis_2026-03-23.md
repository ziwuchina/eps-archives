# EPS ERP 登录与脚本引擎深度分析
**日期**: 2026-03-23
**工具**: IDA Pro 9.0 + idalib-mcp (SSERPTools.exe 数据库端口 12002)
**分析**: CAPIDecrypt 调用链 + SScriptCore SDL 脚本引擎

---

## 一、CAPIDecrypt 硬编码密钥

**SSERPTools.exe 中的字符串引用**:
```
地址: 0x1003e983 → "CAPIDecrypt" (嵌入的字符串常量)
```

**CAPIDecrypt 函数签名** (来自 SSCore32.dll 导出函数名):
```
int __cdecl CAPIDecrypt(char *input, CString &output)
```
- 修饰名: `?CAPIDecrypt@@YAHPADAAVCString@@@Z`
- 位置: SSCore32.dll 导出表
- 返回值: int (0=成功，非0=失败)

---

## 二、登录中的 CAPIDecrypt 调用

**调用位置**: `sub_10007560` (LoginERPDB 处理函数)

**关键调用代码**:
```cpp
CString v24;  // 密码字符串
CString::CString((CString *)&v24, (const struct CString *)v33);  // v33 = 原始密码
CString::CString((CString *)&v27, asc_10048224);  // 硬编码密钥字符串！
CAPIDecrypt(asc_10048224, (struct CString *)v24);  // 解密调用
```

**asc_10048224** = 硬编码密钥字符串 (在 SSERPTools.exe 数据段中)

---

## 三、SScriptCore.dll 脚本调用 (ssExcuteFunction)

**sub_10006E10** = SDL 脚本执行入口函数

**完整流程**:
```
sub_10006E10(a1=this, a2=CScaleMap*, a3=用户名, a4=密码, a5=*, a6=*)
  ├─ 1. SetShareParameter("ERPManager", "", "ExecuteScript")
  │     └─ 告诉 EPS 脚本引擎：模块=ERPManager，函数=ExecuteScript
  │
  ├─ 2. SetShareParameter("Script", "ExecuteScript", "SScriptDll")
  │     └─ 告诉 EPS：脚本 DLL = SScriptDll
  │
  ├─ 3. ssExcuteFunction()  ← 调用 SScriptCore.dll 的导出函数
  │     └─ 实际执行业务脚本（用户名+密码验证逻辑）
  │
  ├─ 4. GetShareParameter("ERPManager", "", "ExecuteScript") → 获取脚本输出
  │     └─ 返回 Token 或错误信息
  │
  ├─ 5. sub_10006670() → 验证脚本返回结果
  │
  ├─ 6. 解析返回数据 → 提取 Token/用户名/用户ID/部门/密码
  │
  └─ 7. 设置 ERPManager 单例:
        CERPManager::SetToken(v3, token_string)
        CERPManager::SetUserName(v3, username_string)
        CERPManager::SetUserID(v3, userid_string)
        CERPManager::SetDeptName(v3, deptname_string)
        CERPManager::SetPassword(v3, password_string)
```

**关键字符串常量** (来自 SSERPTools.exe):
| 地址 | 字符串 | 用途 |
|------|--------|------|
| `0x10048164` | `""` | 空参数 |
| `0x100481E4` | `" "` | 分隔符 |
| `0x100481F8` | `"取消登录"` | 取消按钮 |
| `0x100481E8` | `"登录失败%d"` | 错误模板 |
| `0x10048224` | **硬编码密钥** | CAPIDecrypt 密钥 |
| `0x10049740` | `"请先登录!"` | 未登录错误 |
| `0x1004974C` | `"已经登录!"` | 重复登录 |
| `byte_10049E18` | 空字符串数据 | CString 空值 |

**SScriptCore.dll 关键导出**:
- `ssExcuteFunction` — SDL 脚本执行入口 (通过 LoadLibrary/GetProcAddress 调用)

---

## 四、CERPManager 单例生命周期

```
CERPManager::CERPManager()     ← 创建实例（new 0x20 字节）
    ↓
SetERPManager(ptr)             ← 注册全局单例
    ↓
[用户输入用户名/密码 → 验证]
    ↓
CERPManager::SetToken(token)
CERPManager::SetUserName(name)
CERPManager::SetUserID(id)
CERPManager::SetDeptName(dept)
CERPManager::SetPassword(pwd)
    ↓
WriteIniString("ERPManager", "ERPUsername", username)  ← 持久化到 INI
WriteIniString("ERPManager", "ERPDeptname", deptname)
    ↓
[SetTimer(0, 1, 300000, TimerProc)] ← 启动 5 分钟超时检测
    ↓
[会话结束]
    ↓
CERPManager::ClearERPManager() ← 登出时清空单例
```

---

## 五、关键 API 地址汇总

| 功能 | DLL | 地址 |
|------|-----|------|
| 登录对话框处理 | SSERPTools.exe | 0x10007560 |
| 脚本调用入口 | SSERPTools.exe | 0x10006E10 |
| 验证结果解析 | SSERPTools.exe | 0x10006670 |
| CAPIDecrypt | SSCore32.dll | (导出函数) |
| ssExcuteFunction | SScriptCore.dll | (导入函数) |
| TimerProc (会话超时) | SSERPTools.exe | 0x1001B370 |
| ExecFunction (命令路由) | SSERPTools.exe | 0x1001B4A0 |

---

## 六、结论

1. **CAPIDecrypt 使用硬编码密钥**: `asc_10048224` 在 SSERPTools.exe 中是固定字符串，作为所有密码解密的密钥

2. **SScriptCore.dll 是业务逻辑核心**: 实际的用户名/密码验证在 SDL 脚本中执行，而不是在原生代码中。脚本通过 `ssExcuteFunction()` 调用，返回 Token 和用户信息

3. **CERPManager 单例模式**: 所有会话状态存在全局单例中，通过 INI 文件持久化

4. **无网络明文**: 密码在发送前被 CAPIDecrypt 处理，密钥嵌入在 SSERPTools.exe 中

---

## 七、待深挖

- [ ] CAPIDecrypt 的实际加密算法（需在 SSCore32.dll .text 中定位函数体）
- [ ] SDL 脚本文件位置和内容（loginERP.sdl 或类似）
- [ ] SScriptCore.dll 的完整导出函数表
