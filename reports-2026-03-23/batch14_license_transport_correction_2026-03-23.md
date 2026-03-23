# Batch14 重大发现汇总（2026-03-23 深夜）

## 🔥 颠覆性发现：SSCore32 直接 WININET + urlmon

SSCore32.dll 的导入表证实：
- `WININET.dll!GetUrlCacheEntryInfoA`
- `urlmon.dll!URLDownloadToCacheFileA`

更关键的字符串证据（地址 0x16447c）：
```
%s?usbkeyid=%d&token=%s&vercode=%s
```
这说明 **SSCore32 在构造一个带 usbkeyid/token/vercode 参数的 URL**！

---

## 关键证据汇总

### 1. SSCore32 — EPS网络层的直接HTTP调用者
| 证据 | 地址 |
|------|------|
| `WININET.dll!GetUrlCacheEntryInfoA` | 导入表 |
| `urlmon.dll!URLDownloadToCacheFileA` | 导入表 |
| `%s?usbkeyid=%d&token=%s&vercode=%s` | 0x16447c |
| `token error` | 0x164428 |
| `NH_TCPIP` | 0x1636dc |
| `NH_SERVER_ADDR` | 0x1636e8 |
| `GetUsbKeyID` | 0x10038379 |

**结论**：SSCore32 不仅仅是加密层，它直接参与构建含身份凭证的HTTP请求，是EPS网络架构中**真正发起HTTP调用的底层模块之一**。

---

### 2. hasp_windows — 直接 socket API
| 证据 | 地址 |
|------|------|
| `socket` | 0x3db22d, 0x3e5374 |
| `closesocket` | 0x3db249, 0x3e53c8 |
| `ioctlsocket` | 0x3e53ec |
| `connect` | 0x3db255, 0x3e5418 |
| `cannot init sockets` | 0x3e1a8e |
| `Authorization: Basic` | 0x3e24ce |
| `Connection: Keep-Alive` | 0x3e254a |

**结论**：HASP runtime **直接调用 socket API** 连接授权服务器（不是通过WinHTTP封装）。

---

### 3. AdjustBase — NetHASP 网络配置
| 证据 | 地址 |
|------|------|
| `HLSERVER` / `hlserver` | 0x979c4/0x979d4 |
| `NH_TCPIP.NH_SERVER_ADDR` | 0x9783c |
| `NH_TCPIP.NH_SERVER_NAME` | 0x97884 |
| `NH_TCPIP.NH_SEND_RCV` | 0x9786c |
| `NETBIOS()` | 0x97994 |
| `socket` / `closesocket` / `ioctlsocket` | 0x97594+ |
| `API_NH_GET_CURRENT_SERVER` | 0x8bf48 |
| `<serveraddress><protocol>%s</protocol><address>%s</address></serveraddress>` | XML配置 |

---

### 4. ArcSDEControl — SDE 业务操作链（无裸网络导入）
| 证据 | 说明 |
|------|------|
| `ConnectToSde` | 连接SDE |
| `UploadDataToSdeW` / `method UploadDataToSde` | 上传数据 |
| `DownloadSdeDataW` / `method DownloadSdeData` | 下载数据 |
| `DisableSdeConnectiond` | 断开连接 |
| `ArcSDEControl.SdeDataXHandle` | COM类 |

**结论**：ArcSDEControl 是 ArcObjects COM 封装，不直接发起 socket 调用。

---

## EPS 网络架构（修正版）

```
EPS主程序
  │
  ├─ SSCore32.dll ★ 直接HTTP层 ★
  │    ├─ WININET (GetUrlCacheEntryInfoA)
  │    ├─ urlmon (URLDownloadToCacheFileA)
  │    └─ USBkey/auth HTTP请求构造
  │         └─ "%s?usbkeyid=%d&token=%s&vercode=%s"
  │
  ├─ hasp_windows_82156.dll ★ 直接socket层 ★
  │    ├─ socket/connect/closesocket
  │    ├─ Authorization: Basic
  │    └─ NetHASP授权协议
  │
  └─ AdjustBase.dll ★ NetHASP配置 ★
       ├─ HLSERVER/NH_TCPIP
       ├─ API_NH_GET_CURRENT_SERVER
       └─ serveraddress XML配置
```

**关键结论**：EPS 网络架构是**双通道**：
- **授权通道**：hasp_windows → socket API → HASP License Server
- **业务通道**：SSCore32 → WININET/urlmon → ASP.NET中间层
