# EPS 系统完整架构图
**日期**: 2026-03-23
**版本**: v3.0 (综合所有分析)

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    Eps.exe (主程序)                     │
│               CERPApp::InitInstance                    │
│                    12027端口                           │
└────────────────────┬──────────────────────────────────┘
                     │ SSERPTools::ExecFunction
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SSERPTools.exe (业务分发)                 │
│         ExecFunction @ 0x1001B4A0 (命令路由)           │
│         LoginERPDB @ 0x10007560                       │
│         WorkProgressReport @ 0x10017E00                │
│              12002端口                                │
└────┬──────────────┬───────────────┬───────────────────┘
     │              │               │
     │ Login        │ Work          │ Script调用
     ▼              ▼               ▼
┌──────────┐  ┌──────────┐  ┌──────────────────┐
│ SSCore32  │  │ ssExecute│  │ SScriptCore.dll  │
│ 12001    │  │ Function │  │ (COM脚本引擎)     │
│ HASP/CAPI│  └────┬─────┘  │ 12021            │
│ Decrypt  │       │         └────────┬─────────┘
└──────────┘       │                   │
                  │ LoadLibrary      │ CoCreateInstance
                  ▼                   ▼
         ┌──────────────────┐  (VBScript Runtime)
         │   SScript.dll     │
         │  (1.3MB)         │
         │  SDL脚本文件(.sdl)│
         │  53个脚本         │
         └──────────────────┘
                  │
                  │ XMLHTTP组件
                  ▼ HTTP请求
         ┌──────────────────────────┐
         │  ASP.NET中间层           │
         │  getnumber.shunde.gov.cn  │
         │  218.104.177.240        │
         │  erp.gis.arcgisserverhelper│
         └──────────┬───────────────┘
                    │
                    │ JK101/JK102
                    ▼
         ┌──────────────────────────┐
         │   ArcGIS Server          │
         │   218.104.177.240       │
         │   SDE数据库              │
         └──────────────────────────┘
```

---

## 二、数据层（DAO/ADO双路径）

```
┌─────────────────────────────────────────────────────┐
│          SSERPTools.exe (12002)                    │
│  SSERPTools::GetFeatureSQLexpression @ 0x1008BA4A│
│  SSERPTools::GetObjAttrTable @ 0x100445B0        │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│       SSMap.dll (12003) - 地图/属性               │
│  GetObjAttrTable @ 0x100445B0                     │
│  GetCodeAttrTable @ 0x1002F1F7                    │
│  DecryptCoord @ 0x10038044                        │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│    SSDataXCore.dll (12026) - 属性表注册            │
│  CDataXCore::AddAttrTableDef @ 0x1001e33a        │
└───────────┬────────────────────┬───────────────────┘
            │                    │
┌───────────▼──────┐  ┌────────▼──────────────────────┐
│ SSDatabaseCore    │  │  SSDataXCore              │
│ (12025)           │  │  属性表注册               │
│ SSDBDriver多态    │  │  EPS对象类型→DB表名映射   │
│ ├─ADO后端         │  └──────────────────────────┘
│ └─DAO后端          │
└───────┬───────────┴────────────────────────────────┐
        │                                            │
┌───────▼────────────┐  ┌────────────────────────────▼─┐
│  SSAdoBase.dll     │  │  SSDaoBase.dll (12024)     │
│  (12023)           │  │  platform.mdb (本地)         │
│  SQLOLEDB/Jet OLEDB│  │  CSSDatabase::InsertRecord  │
│  CSSAdoBase::      │  │  @ 0x1000fe8c              │
│  ExecuteSQL        │  │  CDBRecordset::OpenRecordset│
│  @ 0x10005276     │  │  @ 0x1000afe0              │
└────────────────────┘  └─────────────────────────────┘

无网络DB代理！全部本地执行
```

---

## 三、业务模块层

```
┌─────────────────────────────────────────────────────┐
│ SSJointSurvey.dll (12006) - 联合测绘              │
│ ImportJZD → BDCDYH关联 → DAO写入                 │
│ 命令: ImportJZD, XiangMInfoImport, CreateJZDNote   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SSRETools.dll (12011) - 房产管理                   │
│ CHouseHu/CHouseZiRZ/CHouseLouC/CZongD             │
│ OnlineGetBDCDYH* → RegisterBDCDYHZRZ              │
│ EMCreateHu, EMCreateFloorData                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SSCheck.dll (12007) - 质检引擎                    │
│ CCheckModel::ExecuteCheck @ 0x100a740c           │
│ ReadDesign → ExecuteCheck → RegisterErrorReport    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SSPipe.dll (12010) - 管线网络                     │
│ CPipeNet + CPipeGeoOperator                       │
│ GXID唯一标识 / CLineObject/CPointObject           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SSArcSDEUpdate.dll (12005) - ArcSDE空间查询       │
│ CSSGisDB::GetServerName @ 0x10004364             │
│ CSDEWorkspaceManager::ExecuteSQL @ 0x1018ebe2     │
│ GetFirstFeatureGUID @ 0x1013bca9                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SSExchange.dll (12020) - 数据交换引擎             │
│ CDxfFile(读) / CDxfOut(写) / CTransDxf14(R14)    │
│ CEF格式导入导出 / Vector格式                       │
│ ExportDxf @ 0x10027750                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SSProject.dll (12008) - GIS地图项目管理           │
│ CProject / CSSProjection / CEpsXMLSettings         │
│ .epj文件管理 / 坐标投影变换                       │
└─────────────────────────────────────────────────────┘
```

---

## 四、关键函数索引（精选20个）

| 地址 | 模块 | 函数 | 作用 |
|------|------|------|------|
| 0x1000B4A0 | SSERPTools | ExecFunction | 命令分发总入口 |
| 0x10007560 | SSERPTools | LoginERPDB | ERP登录 |
| 0x10017E00 | SSERPTools | WorkProgressReport | 进度上报 |
| 0x1000FD8C | SSCore32 | ssExcuteFunction | 脚本执行 |
| 0x10033344 | SSCore32 | CAPIDecrypt | XOR+HEX解密 |
| 0x1000E740 | SSCore32 | GetToken | 获取ACCESS_TOKEN |
| 0x10038379 | SSCore32 | GetUsbKeyID | 读HASP狗序列号 |
| 0x1008BA4A | SSERPTools | GetFeatureSQLexpression | SQL总调度 |
| 0x100445B0 | SSMap | GetObjAttrTable | EDB属性读取 |
| 0x1002F1F7 | SSMap | GetCodeAttrTable | Code字段读取 |
| 0x1001E33A | SSDataXCore | AddAttrTableDef | 属性表注册 |
| 0x10005276 | SSAdoBase | ExecuteSQL | ADO执行SQL |
| 0x1000FE8C | SSDaoBase | InsertRecord | DAO插入记录 |
| 0x1000AFE0 | SSDaoBase | OpenRecordset | DAO查询 |
| 0x1018EBE2 | SSArcSDEUpdate | ExecuteSQL | SDE执行SQL |
| 0x100A740C | SSCheck | ExecuteCheck | 执行质检 |
| 0x100A752C | SSCheck | ReadDesign | 读取质检设计 |
| 0x10027750 | SSExchange | ExportDxf | DXF导出 |
| 0x10070120 | SSExchange | ImportCEF | CEF导入 |
| 0x10004364 | SSArcSDEUpdate | GetServerName | GIS服务器名 |

---

## 五、MCP端口总表

| 端口 | DLL | 函数规模 | 核心职责 |
|------|-----|---------|---------|
| 12001 | SSCore32.dll | 4975 | 核心/HASP/CAPI |
| 12002 | SSERPTools.exe | 1631 | 命令分发 |
| 12003 | SSMap.dll | 5119 | 地图/属性 |
| 12005 | SSArcSDEUpdate.dll | 6770 | ArcSDE |
| 12006 | SSJointSurvey.dll | 5584 | 联合测绘 |
| 12007 | SSCheck.dll | 3501 | 质检 |
| 12008 | SSProject.dll | 4072 | 项目管理 |
| 12009 | SSCadastre.dll | 3063 | 地籍 |
| 12010 | SSPipe.dll | 6448 | 管线 |
| 12011 | SSRETools.dll | 4702 | 房产 |
| 12013 | hasp_windows_82156.dll | 6449 | HASP驱动 |
| 12015 | BCGCBPRO940d.dll | 29491 | BCG UI框架 |
| 12016 | SSEdit.dll | ~25000 | 编辑器 |
| 12017 | SSForestry.dll | ~20000 | 林业 |
| 12019 | SSFuncLib.dll | 2685 | Excel/图层 |
| 12020 | SSExchange.dll | 4274 | 格式转换 |
| 12021 | SScriptCore.dll | 98 | COM脚本引擎 |
| 12023 | SSAdoBase.dll | 374 | ADO抽象 |
| 12024 | SSDaoBase.dll | 801 | DAO抽象 |
| 12025 | SSDatabaseCore.dll | 660 | DB驱动抽象 |
| 12026 | SSDataXCore.dll | 1376 | 属性表注册 |

---

## 六、已知URL端点（从配置文件）

| 来源 | URL |
|------|-----|
| EpsGlobal.ini | https://getnumber.shunde.gov.cn/EPSUPDATE |
| EpsGlobal.ini | http://getnumber.shunde.gov.cn/EPSUPDATE |
| 大型配置文件 | http://59.39.61.178:8081/epsupdate |

**ERP WEB服务**（Fiddler确认）:
- `https://getnumber.shunde.gov.cn` — 登录/Token
- `https://218.104.177.240/sg_erp_sdqtqh/` — 业务API

---

## 七、SDL脚本文件（53个）

| 脚本 | 大小 | 用途 |
|------|------|------|
| SSSuperMapUpdate.sdl | 2.7MB | 超图数据库更新 |
| SSCommTools.SDL | 1.1MB | 通用工具 |
| SSGISQuery.SDL | 483KB | GIS查询 |
| SS3DView.sdl | 348KB | 3D视图 |
| LandDispatch.SDL | 422KB | 土地Dispatch |

---

*最后更新: 2026-03-23 20:40*
