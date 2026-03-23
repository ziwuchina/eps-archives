# ArcGIS/SDE 分析报告 - 更新版
**日期**: 2026-03-23

---

## SSArcSDEUpdate.dll 分析结论

**模块规模**: 6770 函数 / 5957 字符串

### DLL 依赖
```
SSArcSDEUpdate.dll imports:
  SSAdoBase, SSDaoBase, SSDataX, SSDataXCore, SSDatabaseCore
  SSEdit, SSEditBase, SSExtend, SSGLDC, SSGeoProcess
  SSInterfaceLib, SSMap, SSMapView, SSObject, SSProject
  SSRETools, SScript, SScriptCore, SSymbolParse
  SunwaySDE (自定义SDE封装)
  NETAPI32, WS2_32 (Socket API - 无WinInet/WinHTTP!)
```

### 核心类

| 类 | 说明 |
|---|---|
| `CSSGisDB` | GIS数据库抽象层 |
| `CSDEWorkspaceManager` | SDE工作空间管理 |
| `CSDEFeature` | SDE要素封装 |
| `CArcSDELogInfo` | 计算机名/IP/MAC日志 |
| `CArcSDEGISDBLinkInfo` | GIS数据库链接信息 |

### 关键函数

| 地址 | 函数 | 说明 |
|------|------|------|
| `0x10004364` | `CSSGisDB::GetServerName` | 返回GIS服务器名（存this+12） |
| `0x1000437f` | `CSSGisDB::GetDataBaseName` | 返回数据库名 |
| `0x100043b5` | `CSSGisDB::GetLoggingPassword` | 获取日志密码 |
| `0x1013bca9` | `CSDEWorkspaceManager::GetFirstFeatureGUID` | 获取第一个Feature的GUID（构建SQL） |
| `0x1013baac` | `CSDEWorkspaceManager::CheckFeatureInSDE` | 检查Feature是否存在SDE中 |
| `0x1013b0f7` | `CSDEWorkspaceManager::InitSpatialReference` | 初始化空间参考 |
| `0x1013b182` | `CSDEWorkspaceManager::GetSpatialReference` | 获取空间参考 |
| `0x1018ebe2` | `CSDEWorkspaceManager::ExecuteSQL` | **执行SQL（通过COM ICommandText）** |
| `0x101ce8c0` | `CSDEWorkspaceManager::OpenMapServerLayer` | 打开地图服务器图层 |

### SQL执行流程（ArcSDE COM）
```cpp
CSDEWorkspaceManager::ExecuteSQL
  → CString::AllocSysString (转BSTR)
  → this[38] + 20 = COM接口指针
  → ICommandText::Execute()  ← ArcSDE COM API
  → SysFreeString()
```

### 重要结论

**HTTP调用不在SSArcSDEUpdate.dll里！**
- 无 WinInet / WinHTTP / URLDownload 等HTTP API导入
- 只有 NETAPI32 + WS2_32（底层Socket）
- **ArcGIS Server HTTP调用是通过ASP.NET中间层进行的，不是直接从DLL发出**

### ArcGIS Server架构
```
EPS Client (SSERPTools/SSArcSDEUpdate)
  → ASP.NET Web Service (erp.gis.arcgisserverhelper.interfaceentry)
  → ArcGIS Server REST API
  → SDE数据库
  → 返回JSON (TFH/DJH/ZL)
```

**JK101/JK102是ASP.NET Web Service的方法名，不是客户端直接发出的HTTP URL**

### Fiddler已确认
```
POST https://218.104.177.240/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate
_namespace=erp.gis.arcgisserverhelper.interfaceentry
methodname=JK101
geometry={rings: [[[710227.10, 2535174.87], ...]]}
outFields=TFH
```

### 待继续分析
1. **SSERPTools.exe** 中的HTTP请求构建（仍未找到WinHTTP调用）
2. **SSAdoBase.dll** - ADO数据库封装（可能是HTTP请求出处）
3. **SSInterfaceLib.dll** - 可能有网络接口封装
4. 实际HTTP请求发送位置仍未定位
