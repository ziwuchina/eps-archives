# EPS DLL 系统化拆解计划
**日期**: 2026-03-23
**目标**: 系统化拆解 EPS 全系列 130+ DLL

---

## 一、当前进度

### 已完成 ✅
| DLL | 规模 | 核心发现 |
|-----|------|----------|
| SSCore32.dll | 25.6MB | CAPIDecrypt算法(0x10033344)/HASP导入/CGCS2000坐标加密 |
| SSMap.dll | 32MB | EDB属性读取/Code字段(0x1015D454)/GetObjAttrTable |
| SSERPTools.exe | 6.1MB | 命令链(ExecFunction@0x1001B4A0)/登录/sub_10006E10/SDL调用 |
| SScriptCore.dll | 0.4MB | ⏳ 进行中... |

### 进行中 🔄
| Subagent | 目标 |
|----------|------|
| `f4a13ef9` | SSScriptCore.dll 脚本引擎 + SDL 脚本文件定位 |
| `a593f5cd` | HASP 加密狗系统 + regcode=54390 流程 |
| `df7942ed` | ArcGIS/SDE 接口 + JK101/JK102 调用链 |

---

## 二、DLL 优先级排序（按功能重要性）

### 🔴 P0 - 核心未分析（最大/最关键）

| 优先级 | DLL | i64大小 | 预估功能 |
|--------|-----|---------|---------|
| P0-1 | **SSDwgX.dll** | 419.8MB | DWG看图引擎（最大！内核） |
| P0-2 | **SSRETools.dll** | 47.6MB | RE相关工具 |
| P0-3 | **SSJointSurvey.dll** | 56.4MB | 联合测绘（核心业务） |
| P0-4 | **SSArcSDEUpdate.dll** | 61.7MB | ArcSDE数据库更新（政务GIS） |
| P0-5 | **SSPipe.dll** | 43.3MB | 管线系统 |
| P0-6 | **SSEdit.dll** | 37.7MB | 编辑器核心 |
| P0-7 | **SScript.dll** | 27.6MB | SDL脚本运行时 |
| P0-8 | **SSCheck.dll** | 23.3MB | 检查系统 |
| P0-9 | **SSForestry.dll** | 34.8MB | 林业模块 |
| P0-10 | **SSExchange.dll** | 26.6MB | 数据交换 |

### 🟡 P1 - 重要业务模块

| DLL | i64大小 | 预估功能 |
|-----|---------|---------|
| SSCadastre.dll | 14.6MB | 地籍/不动产 |
| SSProject.dll | 18.5MB | 项目管理 |
| SSEditBase.dll | ~7MB | 编辑基础 |
| SSDeformation.dll | 17.6MB | 变形监测 |
| SSHouse.dll | 17.5MB | 房产 |
| SSWorkSpace.dll | ~8MB | 工作空间 |
| SSEngineering.dll | ~3MB | 工程测量 |
| SSRoad.dll | ~6MB | 道路 |
| SSDtm.dll | 12.4MB | 数字地面模型 |
| SSImage.dll | 6.4MB | 影像处理 |

### 🟢 P2 - 工具/支撑模块

| DLL | 功能 |
|-----|------|
| hasp_windows_82156.dll | HASP加密狗驱动(49.1MB) |
| SSSymbolParse.dll | 符号解析 |
| SSMapView.dll | 地图视图 |
| SS3DEngine.dll | 三维引擎 |
| SSGLDC.dll | 图层显示 |
| SSFuncLib.dll | 函数库 |
| SSMath.dll | 数学库 |
| SSTotalStation.dll | 全站仪驱动 |
| SSGps.dll | GPS驱动 |

---

## 三、网络架构（已知）

```
认证服务器: getnumber.shunde.gov.cn
ArcGIS空间服务器: 218.104.177.240
SSWEBGIS Web端: 219.130.221.6 (www.xnschy.com)
```

---

## 四、下一步行动（并行子agent策略）

### 第一批（3个并发）🔄
1. SSScriptCore.dll 脚本引擎 ✅
2. HASP 加密狗系统 ✅
3. ArcGIS/SDE 接口 ✅

### 第二批（P0 核心DLL，3个并发）
建议顺序：
1. **SSArcSDEUpdate.dll** - ArcSDE更新（关联218.104.177.240）
2. **SSJointSurvey.dll** - 联合测绘（核心业务）
3. **SSRETools.dll** - RE工具（47.6MB）

### 第三批（P0续）
4. **SScript.dll** - SDL脚本运行时（关联登录验证）
5. **SSCheck.dll** - 检查系统
6. **SSDwgX.dll** - DWG看图引擎（最大！）

### 第四批（P1重要模块）
7. SSCadastre.dll - 地籍
8. SSProject.dll - 项目管理
9. SSEdit.dll - 编辑器
10. SSPipe.dll - 管线

---

## 五、已知关键函数索引（持续更新）

### SSCore32.dll (base=0x10000000)
| 地址 | 函数 | 功能 |
|------|------|------|
| 0x10033344 | CAPIDecrypt | XOR+HEX解密 |
| 0x100335bd | CAPIDecryptLongString | 长串解密 |
| 0x100331ff | CAPIEncrypt | 加密 |
| 0x1003801d | EncryptCoord | 坐标加密 |
| 0x10038044 | DecryptCoord | 坐标解密 |
| 0x1003824f | GetCefKeyString | CEF密钥 |
| 0x100b9f40 | hasp_login | HASP登录(导入) |
| 0x100b9f52 | hasp_login_scope | HASP范围登录(导入) |

### SSMap.dll (base=0x10000000)
| 地址 | 函数 | 功能 |
|------|------|------|
| 0x100445B0 | GetObjAttrTable | 对象→属性表映射 |
| 0x1002F1F7 | GetCodeAttrTable | Code→属性表 |
| 0x1008BA4A | GetFeatureSQLexpression | SQL总调度 |
| 0x1008BC92 | GetFeatureSelectSQLexpression | Feature SQL |
| 0x1008C376 | GetScriptSelectSQLexpression | Script SQL |
| 0x1004B76C | GetFieldCodeMap | 字段码映射 |
| 0x1015D454 | (字符串) | "Code"字段 |

### SSERPTools.exe (base=0x10000000)
| 地址 | 函数 | 功能 |
|------|------|------|
| 0x1001B4A0 | CSSERPToolsInterface::ExecFunction | 命令分发 |
| 0x10007560 | sub_10007560 | LoginERPDB处理 |
| 0x10006E10 | sub_10006E10 | 脚本调用入口 |
| 0x1001B370 | TimerProc | 会话超时检测 |

---

## 六、Fiddler 已确认 API 清单

| API | Method | Server | 功能 |
|-----|--------|--------|------|
| CommonOperate | POST | getnumber.shunde.gov.cn | userlogin/gettoken |
| erp.pro.sdgtj.GeTimeToken | GET | getnumber.shunde.gov.cn | 时间戳Token |
| erp.pro.sdgtj.GetUnitUserMessages | GET | getnumber.shunde.gov.cn | 单位人员列表 |
| erp.neto.netofficehelper.validepsregcode | POST | 218.104.177.240 | HASP在线验证 |
| erp.gis.arcgisserverhelper.interfaceentry | POST | 218.104.177.240 | JK101/JK102空间查询 |
