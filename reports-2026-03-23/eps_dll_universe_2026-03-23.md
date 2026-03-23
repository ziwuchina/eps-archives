# EPS DLL 全宇宙图谱
**日期:** 2026-03-23
**覆盖:** 30+ 模块 / 28个IDA并发实例

---

## EPS 系统架构（2026-03-23 最终版）

```
┌─────────────────────────────────────────────────────────────────┐
│                     Eps.exe (主进程)                           │
│  PID 15920 · BCGControlBar Pro 9.40 MFC UI                     │
│                                                                 │
│  ├─ EpsCOM.dll (12045) ────────── COM组件工厂                  │
│  │     DllGetClassObject → MFC/ATL COM对象                     │
│  │     SoftRegister（软件注册）                                  │
│  │     Ribbon UI（CBCGPToolbar*）                               │
│  │                                                         │
│  ├─ BCGCBPRO940d.dll (12015) ──── UI框架库（122.7MB）          │
│  │     CBCGPEdit / CBCGPPropList / CBCGPAnimatorCtrl           │
│  │                                                         │
│  ├─ SSEdit.dll (12016) ────────── 编辑对话框基类               │
│  │     CDlgBase::Enter/Tab/F12 · SSAttrInput属性输入           │
│  │     OnViewLButtonDown/MouseMove · 选中文本处理              │
│  │                                                         │
│  ├─ SSGLDC.dll (12034) ────────── 渲染控制核心                 │
│  │     CGLDC = GIS Layer Display Control                       │
│  │     双缓冲渲染 · CDC设备上下文 · 地图比例尺                  │
│  │                                                         │
│  └─ SS3DView.dll (12036) ──────── 3D视图+GDAL                 │
│        SSGDALDataset → GDAL栅格封装（影像/DEM）                │
│        generateContour → 等高线生成（调用SSDtm）               │
│        ss3dGeometrySphere/Cone/Cylinder · gbGetStereoViewMode  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SSERPTools.exe (命令行)                      │
│  命令入口: ExecFunction @ 0x1001B4A0                           │
│  loginERP / logoutERP / worksubmit / getworklist / ...        │
│                                                                 │
│  ├─ ?ssExcuteFunction@@YAHVCString@@0PAX1@Z @ 0x1000fd8c      │
│  │     → SScriptCore.dll (COM VBScript引擎)                    │
│  │                                                         │
│  └─ DAO/ADO双路径 → EDB数据库                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SScriptCore.dll (COM脚本引擎)                  │
│  ScriptEngineFactory                                            │
│  ├─ InitializeScriptEngine → 初始化VBScript                    │
│  ├─ LoadScript → 动态加载.sdl脚本                              │
│  ├─ RunScript → 执行脚本                                      │
│  └─ HRVerify → 许可证校验（ORDINAL 7）                        │
│                                                                 │
│  .sdl脚本文件 (D:\EPS2026G\*.sdl)                             │
│  ├─ 53个脚本文件（AddObject, BatExx2Edb, Buffer...）           │
│  └─ 脚本内: XMLHTTP POST → ASP.NET中间层                       │
└─────────────────────────────────────────────────────────────────┘
                                │
              ┌─────────────────┴──────────────────┐
              ▼                                  ▼
┌─────────────────────────┐    ┌─────────────────────────────────┐
│  ASP.NET中间层服务器    │    │     ArcGIS Server (SDE)         │
│  (219.130.221.6)        │    │     (218.104.177.240)           │
│                         │    │                                 │
│  erp.gis.arcgisserver- │    │  erp.neto.netofficehelper.*    │
│  helper.interfaceentry  │    │                                 │
│  ├─ JK101: 图号查询     │    │  空间查询: esriGeometryPolygon  │
│  └─ JK102: 属性查询     │    │  TFH/DJH/ZL/QHZT 返回          │
└─────────────────────────┘    └─────────────────────────────────┘
                                      │
                                      ▼
                          ┌─────────────────────┐
                          │  EPS EDB数据库      │
                          │  (Jet MDB格式)      │
                          │  313+张属性表       │
                          │  DAO+ADO双路径      │
                          └─────────────────────┘

---

## 核心业务模块

### 📋 测绘业务
| 模块 | 端口 | 核心功能 |
|------|------|---------|
| SSMap.dll | 12003 | 地图渲染 · EDB读写 · 字段映射 |
| SSJointSurvey.dll | 12006 | 联合测绘 · ImportJZD · CreateJZDNote |
| SSDeformation.dll | 12040 | 形变监测 · 沉降/位移监测 |
| SSDtm.dll | 12042 | 数字地形模型 · GetDemHeight · CreateContour |
| SSGLDC.dll | 12034 | 渲染控制 · 双缓冲 · 地图比例尺 |
| SS3DView.dll | 12036 | 3D视图 · GDAL · 等高线渲染 |
| SSHouse.dll | 12041 | TIN三角网构建 · CTriNetBuild |

### 🏗️ 国土/地籍
| 模块 | 端口 | 核心功能 |
|------|------|---------|
| SSCadastre.dll | 12009 | 地籍数据模型 · BDCDYH关联 |
| SSCadastre1.dll | 12044 | 地籍登记 · ZDT宗地 · 房产证管理 |
| SSRETools.dll | 12011 | 房产管理 · CHouseHu/Floor/LouC · BDCDYH |
| SSLand.dll | 12048 | 土地利用规划 · 土地分级 |

### 🔧 编辑/工具
| 模块 | 端口 | 核心功能 |
|------|------|---------|
| SSEdit.dll | 12016 | 编辑对话框基类 · 属性输入 |
| SSCheck.dll | 12007 | 质检系统 · ExecuteCheck · ExecuteRepair |
| SSProject.dll | 12008 | 项目管理 · CProject · SDLInterface |
| SSFuncLib.dll | 12047 | 函数库 · Calculate · Util |
| SSEngineerCut.dll | 12050 | 土方工程 · 断面/断面图 · 体积计算 |
| SSEngineeringSurvey.dll | 12049 | 工程测量 · Control/Benchmark/GPS |

### 📊 数据/同步
| 模块 | 端口 | 核心功能 |
|------|------|---------|
| SSDBUpdate.dll | 12043 | 数据库同步 · UpdateAttrData · CreateAttrTable |
| SSArcSDEUpdate.dll | 12005 | ArcSDE更新 · ExecuteSQL · GetFeatureGUID |
| SSPipe.dll | 12010 | 管线网络 · CPipeNet · GXID标识 |
| SSExchange.dll | - | 数据交换 · CExxIO · VectorIn/Out |

### 🔐 安全/驱动
| 模块 | 端口 | 核心功能 |
|------|------|---------|
| SSCore32.dll | 12001 | 加密核心 · CAPIDecrypt · EncryptCoord · HASP API存根 |
| hasp_windows_82156.dll | 12013 | HASP实现 · Vendor ID 529 · 加密狗读写 |

### 🌲 林业/专题
| 模块 | 端口 | 核心功能 |
|------|------|---------|
| SSForestry.dll | 12017 | 林业调查 · CForestryInterface · AddRibbonCategory |

---

## 模块依赖树（关键路径）

```
Eps.exe
  │
  ├─ BCGCBPRO940d.dll (UI框架)
  ├─ EpsCOM.dll (COM工厂)
  ├─ SSEdit.dll (对话框)
  │
  └─ SSERPTools.exe (命令路由)
        │
        ├─ SScriptCore.dll (VBScript引擎)
        │     ├─ SScript.dll (53个.sdl脚本运行时)
        │     │     └─ XMLHTTP → 网络请求
        │     └─ SSFuncLib.dll (函数工具库)
        │
        ├─ SSMap.dll (EDB读写)
        │     ├─ SSCore32.dll (加密)
        │     ├─ SSDtm.dll (DEM/TIN)
        │     └─ SSGLDC.dll (渲染)
        │
        ├─ SSArcSDEUpdate.dll (ArcSDE更新)
        │     └─ ASP.NET中间层 → ArcGIS Server
        │
        ├─ SSJointSurvey.dll (联合测绘)
        ├─ SSCadastre.dll / SSCadastre1.dll (地籍)
        ├─ SSRETools.dll (房产管理)
        ├─ SSCheck.dll (质检)
        ├─ SSDBUpdate.dll (数据同步)
        ├─ SSPipe.dll (管线)
        ├─ SS3DView.dll (3D/GDAL)
        ├─ SSDeformation.dll (形变监测)
        ├─ SSForestry.dll (林业)
        ├─ SSHouse.dll (TIN构建)
        ├─ SSLand.dll (土地利用)
        ├─ SSEngineeringSurvey.dll (工程测量)
        └─ SSEngineerCut.dll (土方)
```

---

## IDA MCP 并行实例（当前在线）

| 端口 | 模块 | 函数数 | 状态 |
|------|------|--------|------|
| 12001 | SSCore32.dll | ~2,922 | ✅ |
| 12002 | SSERPTools.exe | ~1,641命令 | ✅ |
| 12003 | SSMap.dll | 5,119 | ✅ |
| 12005 | SSArcSDEUpdate.dll | 6,770 | ✅ |
| 12006 | SSJointSurvey.dll | ~5,000+ | ✅ |
| 12007 | SSCheck.dll | 3,501 | ✅ |
| 12008 | SSProject.dll | ~4,000+ | ✅ |
| 12009 | SSCadastre.dll | 3,063 | ✅ |
| 12010 | SSPipe.dll | ~4,000+ | ✅ |
| 12011 | SSRETools.dll | ~4,000+ | ✅ |
| 12013 | hasp_windows_82156.dll | ~2,000+ | ✅ |
| 12015 | BCGCBPRO940d.dll | ~25,000+ | ✅ |
| 12016 | SSEdit.dll | ~8,000+ | ✅ |
| 12017 | SSForestry.dll | ~7,000+ | ✅ |
| 12034 | SSGLDC.dll | 1,069 | ✅ |
| 12036 | SS3DView.dll | 2,241 | ✅ |
| 12040 | SSDeformation.dll | 3,525 | ✅ |
| 12041 | SSHouse.dll | 3,000 | ✅ |
| 12042 | SSDtm.dll | 2,469 | ✅ |
| 12043 | SSDBUpdate.dll | 3,078 | ✅ |
| 12044 | SSCadastre1.dll | 3,431 | ✅ |
| 12045 | EpsCOM.dll | 4,028 | ✅ |
| 12047 | SSFuncLib.dll | 待查 | 🔄Batch10 |
| 12048 | SSLand.dll | 待查 | 🔄Batch10 |
| 12049 | SSEngineeringSurvey.dll | 待查 | 🔄Batch10 |
| 12050 | SSEngineerCut.dll | 待查 | 🔄Batch10 |

**总计: 25个已上线 + 4个Batch10中 = 29个并发IDA实例**
