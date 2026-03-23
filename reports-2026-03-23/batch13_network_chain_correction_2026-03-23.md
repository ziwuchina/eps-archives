# Batch13 网络链路勘误（2026-03-23）

在继续复核时，发现 Batch13 初稿结论需要修正：

## 勘误点

### 1) ArcSDEX.dll 实际存在网络相关导入
通过 `pefile` 直接解析导入表：
- `WS2_32.dll`
  - `WSAStartup`
  - `WSACleanup`
  - `gethostname`
  - `gethostbyname`
  - `inet_ntoa`
- `NETAPI32.dll`
  - `Netbios`

这说明 ArcSDEX 至少包含主机解析/NetBIOS 发现能力（不是完全“无网络导入”）。

### 2) AdjustBase.dll 存在明确 NetHASP/网络授权痕迹（字符串证据）
- `classic_get_sesskeyinfo: LowAPI (API_NH_GET_CURRENT_SERVER) status %u`
- `<serveraddress><protocol>%s</protocol><address>%s</address></serveraddress>`
- `-HLSERVER*`, `HLSERVER`, `hlserver`
- `NH_TCPIP.NH_SERVER_ADDR`, `NH_TCPIP.NH_SERVER_NAME`, `NH_COMMON.NH_NETBIOS`
- `socket`, `gethostname`, `gethostbyname`, `gethostbyaddr`

这指向 Sentinel/NetHASP 的网络授权发现与会话流程。

### 3) ArcSDEControl.dll 未见裸 socket/HTTP 导入，但有明确 SDE COM 接口字符串
- `ConnectToSde`
- `DisableSdeConnection`
- `DownloadSdeData`
- `UploadDataToSde`

这更像 COM/ArcObjects 层封装，不是模块内直连 HTTP。

## 修正后结论
- ArcSDE 侧模块以 ArcObjects/SDE 语义调用为主，URL/token 字面量仍未直接提取。
- 授权网络链路证据更强，集中在 AdjustBase + HASP/NetHASP 相关配置与字符串。
- 后续应重点追踪：`API_NH_GET_CURRENT_SERVER`、`HLSERVER`、`NH_TCPIP` 在运行时如何被调用。
