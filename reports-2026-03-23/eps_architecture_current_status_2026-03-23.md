# EPS 系统架构现状总报告
**日期**: 2026-03-23 晚间
**综合所有逆向 + 抓包分析**

---

## 一、已建立的核心架构

```
┌─────────────────────────────────────────────────────────┐
│  EPS 客户端 (Eps.exe + SSERPTools.exe)                 │
│  ├─ 登录: userlogin → gettoken → ACCESS_TOKEN (10h)   │
│  ├─ HASP验证: GetUsbKeyID → regcode=54390             │
│  └─ 业务请求 → HTTP POST (via MFC CInternetSession)    │
│         ↓                                               │
│  ASP.NET Web Service (getnumber.shunde.gov.cn +         │
│     218.104.177.240/sg_erp_sdqtqh/)                    │
│         ├─ userlogin / gettoken / validepsregcode       │
│         └─ erp.gis.arcgisserverhelper.interfaceentry   │
│                ├─ JK101 (图号查询 TFH)                   │
│                └─ JK102 (完整属性 DJH/ZL/QHZT)          │
│                     ↓                                   │
│           ArcGIS Server (218.104.177.240)               │
│                ↓                                        │
│           SDE数据库 (CGCS2000坐标系)                    │
└─────────────────────────────────────────────────────┘
```

---

## 二、已确认的 DLL 职责

| DLL | 职责 |
|-----|------|
| **SSERPTools.exe** | 命令分发(ExecFunction)、登录处理、CERPManager单例 |
| **SSCore32.dll** | CAPIDecrypt/HASP/坐标加密/GCGIS2000 |
| **SSMap.dll** | EDB属性读取/Code字段/SQL组装 |
| **SSArcSDEUpdate.dll** | ArcSDE工作空间/Spatial Reference/Feature查询 |
| **SScriptCore.dll (SscriptDll.dll)** | SDL脚本执行(动态加载) |

---

## 三、关键函数索引（已钉死）

### 登录链
| 地址 | 函数 | 位置 |
|------|------|------|
| 0x1001B4A0 | ExecFunction (命令分发) | SSERPTools |
| 0x10007560 | LoginERPDB处理 | SSERPTools |
| 0x10006E10 | 脚本调用入口 | SSERPTools |
| 0x1000fd8c | ssExcuteFunction (动态加载SscriptDll) | SSCore32 |
| 0x10033344 | CAPIDecrypt (XOR+HEX, 后门!) | SSCore32 |
| 0x1000e740 | GetToken | SSCore32 |
| 0x10038379 | GetUsbKeyID (读HASP狗序列号) | SSCore32 |

### SQL/属性
| 地址 | 函数 | 位置 |
|------|------|------|
| 0x1008BA4A | GetFeatureSQLexpression (SQL总调度) | SSERPTools |
| 0x1008BC92 | GetFeatureSelectSQLexpression | SSERPTools |
| 0x1008C376 | GetScriptSelectSQLexpression | SSERPTools |
| 0x1015D454 | "Code"字段字符串 | SSERPTools |
| 0x100445B0 | GetObjAttrTable | SSMap |
| 0x1002F1F7 | GetCodeAttrTable | SSMap |
| 0x1004B76C | GetFieldCodeMap | SSMap |

### ArcSDE/GIS
| 地址 | 函数 | 位置 |
|------|------|------|
| 0x10004364 | CSSGisDB::GetServerName | SSArcSDEUpdate |
| 0x1018ebe2 | CSDEWorkspaceManager::ExecuteSQL | SSArcSDEUpdate |
| 0x1013bca9 | GetFirstFeatureGUID | SSArcSDEUpdate |
| 0x1013b0f7 | InitSpatialReference | SSArcSDEUpdate |

### 坐标
| 地址 | 函数 | 位置 |
|------|------|------|
| 0x1003801d | EncryptCoord | SSCore32 |
| 0x10038044 | DecryptCoord | SSCore32 |
| 0x1003824f | GetCefKeyString | SSCore32 |

---

## 四、Fiddler API 汇总

| API | Method | Server | 关键参数 |
|-----|--------|--------|---------|
| CommonOperate | POST | getnumber.shunde.gov.cn | _namespace=userlogin, loginname, password |
| erp.pro.sdgtj.GeTimeToken | GET | getnumber.shunde.gov.cn | timestamp |
| CommonOperate | POST | 218.104.177.240 | _namespace=validepsregcode, regcode=54390 |
| CommonOperate | POST | 218.104.177.240 | _namespace=...interfaceentry, methodname=JK101, geometry, outFields=TFH |
| CommonOperate | POST | 218.104.177.240 | methodname=JK102, outFields=DJH,BBH,ZL,QHZT |

---

## 五、待继续分析

1. **HTTP请求构建**（SSERPTools无明文URL，可能通过MFC CInternetSession动态构建）
2. **SSJointSurvey.dll** - 联合测绘 (subagent跑中)
3. **SSCheck.dll** - 质检系统 (subagent跑中)
4. **SSProject.dll** - 项目管理 (subagent跑中)
5. **hasp_windows_82156.dll** - HASP驱动(49.1MB，已建i64)
6. **SSDwgX.dll** - DWG引擎(419.8MB，最大)

---

## 六、MCP端口现状

| 端口 | 数据库 | 函数规模 |
|------|--------|---------|
| 12001 | SSCore32.dll | 4975 |
| 12002 | SSERPTools.exe | 1631 |
| 12003 | SSMap.dll | 5119 |
| 12005 | SSArcSDEUpdate.dll | 6770 |
