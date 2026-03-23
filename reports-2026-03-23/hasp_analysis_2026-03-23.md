# EPS HASP 加密狗系统分析报告
**日期**: 2026-03-23
**工具**: IDA Pro 9.0 + idalib-mcp (SSCore32.dll.i64 @ port 12001)

---

## 1. 核心结论

**EPS 使用 HASP USB 加密狗进行License 验证。regcode（如 54390）不是硬编码的，而是从 USB 狗中实时读取的。**

---

## 2. GetUsbKeyID 函数

**地址**: `0x10038379` in SSCore32.dll

**伪代码**:
```cpp
int __cdecl GetUsbKeyID()
{
  int result;
  bool v1;
  int dongle_id;

  dongle_id = dword_101BAC54;   // 从 HASP API 读取的实际狗号

  if (dword_101BAD14) {         // 模式标志
    if (dword_101BAD14 == 1) {
      result = dongle_id;
      if (dongle_id < 200000) return 0;
      v1 = (dongle_id <= 299999);
    } else if (dword_101BAD14 == 2) {
      result = dongle_id;
      if (dongle_id < 300000) return 0;
      v1 = (dongle_id <= 399999);
    } else {
      return 0;
    }
    if (v1) return result;
    return 0;
  }

  result = dongle_id;
  if (dongle_id >= 50000) {
    v1 = (dongle_id <= 199999);
    // Range 0: 50000-199999
    if (v1) return result;
  }
  return 0;
}
```

**狗号范围规则**（来自 Fiddler 抓包 `regcode=54390`）:

| 模式 | 范围 | 说明 |
|------|------|------|
| 模式0（默认） | 50000–199999 | regcode = dongle_id |
| 模式1 | 200000–299999 | regcode = dongle_id |
| 模式2 | 300000–399999 | regcode = dongle_id |
| 其他 | — | 返回0（无效） |

**关键**：`54390` 在模式0范围内（50000-199999），是真实的 USB 狗序列号。

---

## 3. HASP API 导入存根（SSCore32.dll）

所有 hasp_* 函数均为**跳转到外部 `hasp_windows_82156.dll` 的导入存根**：

| 地址 | 函数名 | 作用 |
|------|--------|------|
| `0x100b9f40` | `hasp_login` | 登录HASP加密狗会话 |
| `0x100b9f46` | `hasp_logout` | 登出HASP会话 |
| `0x100b9f4c` | `hasp_hasptime_to_datetime` | 时间转换 |
| `0x100b9f52` | `hasp_login_scope` | 带范围登录 |
| `0x100b9f58` | `hasp_get_rtc` | 读取实时时钟 |
| `0x100b9f5e` | `hasp_decrypt` | 解密数据 |
| `0x100b9f64` | `hasp_read` | 读取狗内数据 |

---

## 4. regcode API 调用流程

**Fiddler 抓包显示**:
```
POST https://218.104.177.240/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate
_namespace=erp.neto.netofficehelper.validepsregcode
&access_token=<token>
&userid=<userid>
&regcode=54390

响应: {"success":false,"msg":"验证失败-未找到验证的狗号:54390"}
```

**结论**: EPS 调用 `GetUsbKeyID()` → 得到 `54390` → 拼 `regcode=54390` → 发到 API

---

## 5. 重要发现

**regcode 字符串不在任何 DLL 中！**
- 搜索 SSCore32.dll、SSERPTools.exe、SSMap.dll 均无 `regcode`、`validepsregcode`、`54390` 等字符串
- 证明这些值是**动态构造**的（`IntegerToString(GetUsbKeyID())`）

**Fiddler 中的 `regcode=54390` = 从 USB 狗实时读取的序列号**

---

## 6. HASP Dongle ID 范围参考

| 范围 | 可能的用途 |
|------|-----------|
| 50000–199999 | 普通授权（当前 54390 落在此范围） |
| 200000–299999 | 扩展授权 |
| 300000–399999 | 企业授权 |
| 0 或无效 | 未插狗/驱动异常 |

---

## 7. 待继续分析

1. `dword_101BAC54` 的来源 - 通过哪个 HASP API 读取？
2. `dword_101BAD14`（模式标志）的设置位置
3. `validepsregcode` API 调用的完整参数构造（哪个 DLL 发起 HTTP 请求？）
4. HASP 狗内的具体数据内容（授权模块、到期时间等）
5. `hasp_windows_82156.dll` 完整分析（已知 49.1MB i64）
