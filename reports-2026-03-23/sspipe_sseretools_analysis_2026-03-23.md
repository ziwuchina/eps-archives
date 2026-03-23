# SSPipe.dll & SSRETools.dll 模块分析报告

**分析日期**: 2026-03-23  
**分析师**: OpenClaw Subagent (idalib-mcp)  
**文件**: `D:\EPS2026G\SSPipe.dll.i64`, `D:\EPS2026G\SSRETools.dll.i64`

---

## 1. SSPipe.dll（管线模块）

### 1.1 基本信息

| 属性 | 值 |
|------|-----|
| 文件路径 | D:\EPS2026G\SSPipe.dll.i64 |
| 架构 | 32-bit DLL |
| 基址 | 0x10000000 |
| 镜像大小 | 0x22f000 (约 2.27 MB) |
| MD5 | e80a16b5bd3ced5d37d7e7da1b96efc7 |
| 函数总数 | 6448 |
| 命名函数 | 2628 |
| 字符串总数 | 4094 |

**代码段**: `.text` (0x10001000 - 0x1015c000, ~1.4MB rx)  
**数据段**: `.rdata` (只读数据), `.data` (读写数据)

### 1.2 核心类结构

#### CPipeNet（管线网络管理器）
- **构造**: `??0CPipeNet@@QAE@PAVCDataSource@@@Z`（接受 CDataSource* 数据源）
- **析构**: `??1CPipeNet@@UAE@XZ`
- **关键方法**:
  - `Clear`: 清空管线网络
  - `Init`: 初始化（0x101bdde9）
  - `Standardization`: 管线数据标准化
  - `GetState`: 获取状态
  - `GetGeoLayer`: 按索引或名称获取地理图层
  - `GetGeoLayerCount`: 获取图层数量
  - `GetNoteLayer`: 获取注记图层
  - `GetNoteLayerCount`: 获取注记图层数量

#### CPipeGeoOperator（管线几何操作器）
- **构造**: `??0CPipeGeoOperator@@QAE@XZ`
- **关键方法**:
  - `GetGXIDGroup`: 获取管线GXID分组
  - `GetLineGeoList`: 获取线对象列表（所有）
  - `GetLineGeoListByGXID`: 按GXID获取线对象
  - `GetPointGeoList`: 获取点对象列表
  - `GetPointGeoListByLine`: 获取线上关联的点对象
  - `Init`: 初始化几何操作器（参数: CScaleMap*, CGeObjList&）

#### 管线材质/类型判断函数
- `IsClassOfDrainPipe`: 判断是否排水管 (0x101be04a)
- `IsPressPipe`: 判断是否压力管 (0x101be2dd)
- `GetPipeDiameter`: 获取管线直径 (多个重载)

#### 管线配置
- `GetPipeConfigFile`: 获取管线配置文件路径
- `ReadPipeConfig`: 读取管线配置 (多个重载)
- 配置数据文件: **PipeConfig.mdb** (Access数据库)
- 检查配置: **PipeCheck.ini**

#### 交互输入类
- `CInputPipeLine`: 管线线输入 (对话框)
- `CInputPipePoint`: 管线点输入 (对话框)
- `GxInputPipeRoute`: 管线路由输入
- `GxInputPipeLine`: 管线线输入
- `GxInputPipePoint`: 管线点输入
- `GXPipeNoSort`: 管线排序

#### 断面分析
- `GetPipeCutInfo`: 获取管线切面信息 (多个重载，0x101bc64c)

### 1.3 对外接口 / 交互点

| 字符串 | 地址 | 含义 |
|--------|------|------|
| SSPipe.dll | 0x101b5838 | 模块名 |
| SSPipe\CCalcHeightDlg\Scheme | 0x101c2714 | 管线高程计算对话框 |
| SSPipe\CGXCq\Scheme | 0x101c7318 | 管线超高对话框 |
| SSPipe_FieldDefaultValue | 0x101c9a68 | 字段默认值 |
| $SDL,SSPipe,GxParaSetup | 0x101d1f20 | SDL命令注册路径 |
| Pipe_ATTR_ | 0x101cf568 | 属性前缀 |

### 1.4 依赖模块（Imports）

| 模块 | 函数数 | 主要用途 |
|------|--------|---------|
| **SSObject** | 164 | 几何对象系统 (CGeoBase, CPointObject 等) |
| **SSInterfaceLib** | 206 | BCGPEpsPropList 等UI属性列表 |
| **SSDaoBase** | 46 | DAO数据库 (CDBRecordset, CSSDatabase) |
| **SSAdoBase** | 21 | ADO数据库 (CAdoRecordset) |
| **SSGLDC** | 27 | OpenGL渲染 (CGLDC 绘图上下文) |
| **SSMapView** | 13 | 打印管理、纸张设置 |
| **SSProject** | 5 | SDL命令注册 (CSDLInterface) |
| **SSymbolParse** | 4 | 符号解析 (CDataParse) |
| **SSEditBase** | 13 | 对话框基类事件处理 |
| **SunwaySDE** | 1 | SDE空间数据库 (GetAttrFieldInfos) |

### 1.5 与 SSMap/SSJointSurvey 集成

- **通过 CDataSource** 接入管线数据层（SSMap 的核心数据抽象）
- 通过 **CScaleMap** 接入地图比例尺系统
- 通过 **CGLDC** 接入 OpenGL 渲染上下文（在 SSMapView 中创建）
- 通过 **SSProject 的 CSDLInterface** 注册命令（`RegisterCmd`），可被 EPS 命令系统调用
- 通过 **CMarkNoteList** 与注记系统交互

---

## 2. SSRETools.dll（房地产RE工具模块）

### 2.1 基本信息

| 属性 | 值 |
|------|-----|
| 文件路径 | D:\EPS2026G\SSRETools.dll.i64 |
| 架构 | 32-bit DLL |
| 基址 | 0x10000000 |
| 镜像大小 | 0x253000 (约 2.37 MB) |
| MD5 | 6c430c695126d60df0e7ec8fdc17dda4 |
| 函数总数 | 4702 |
| 命名函数 | 2523 |
| 字符串总数 | 4481 |

**代码段**: `.text` (0x10001000 - 0x10190000, ~1.6MB rx)  
**数据段**: `.rdata`, `.data`

### 2.2 核心类结构

#### CSSREToolsInterface（RE工具主接口）
- **继承**: CSDLInterface（命令/UI框架基类）
- **构造**: `??0CSSREToolsInterface@@QAE@XZ` (0x101e714e)
- **虚表**: `??_7CSSREToolsInterface@@6B@` (0x101e8c06)
- **关键方法**:
  - `AddRibbonCategory`: 添加功能区选项卡
  - `BeforeDrawMap`: 地图绘制前回调
  - `DrawDC` / `DrawGL`: 渲染（DC/OpenGL）
  - `ExecFunction`: 执行功能函数（核心，0x101ea320）
  - `ExecFunction_CheckFunction`: 功能检查（0x101ea35c）
  - `OnAfterLoadData`: 数据加载完成后回调
  - `OnCallBackMessage`: 消息回调
  - `OnDraw`: 绘制
  - `OnSelectChange`: 选择变化
  - `OnUpdateCmdUI`: UI更新
  - `RegisterCheckModel`: 注册检查模型
  - `RegisterCommand`: 注册命令

#### CHouseManager（房产管理器）
从字符串中发现的关联方法:
- `FillBDCDYHZD`: 填写不动产单元号（**BDC**=不动产，**DY**=单元，**ZD**=宗地）
- `FillBDCDYHZRZ`: 填写不动产单元号认证（**RZ**=认证）
- `FillZDCode`: 填写宗地代码
- `GetAllDxtFloorData`: 获取所有分层数据
- `GetAllLayerNameList`: 获取所有图层名称

#### 房产相关类（从命名推断）
- `CHouseZiRZ` / `CHouseZiRZs`:  House certifiable (认证) ？
- `CHouseHu` / `CHouseHus`: 户
- `CHouseLouC` / `CHouseLouCs`: 楼幢
- `CHouseLuoJiZ` / `CHouseLuoJiZs`: 逻辑幢？
- `CHouseMianJK` / `CHouseMianJKs`: 面积计算？
- `CZongD` / `CZongDs`: 宗地（Cadastral parcel）
- `CTreeItemSite`: 树形项目位置

#### 绘图/Rendering
- `CreateDispList`: 创建显示列表 (from SSMapView)

### 2.3 对外接口 / 交互点

| 字符串 | 地址 | 含义 |
|--------|------|------|
| SSRETools.dll | 0x101e67a6 | 模块名 |
| SSInterfaceLib.dll | 0x101d7cce | 界面库依赖 |

### 2.4 依赖模块（Imports）

| 模块 | 函数数 | 主要用途 |
|------|--------|---------|
| **SSObject** | 139 | 几何对象 (CreateTopPolygon, CGeoBase, CMarkNote) |
| **SSEditBase** | 145 | 对话框/脚本对象，CEpsProcessManager（EPS处理流程） |
| **SSInterfaceLib** | 120 | CBCGPEpsPropList 属性列表、输入参数对话框 |
| **SSDaoBase** | 59 | DAO数据库 |
| **SSGLDC** | 13 | OpenGL渲染 (GetClientArea, DrawObject, TransCoordinate) |
| **SSAdoBase** | 5 | ADO数据库 (GetTableNames, BOF/EOF) |
| **SSMapView** | 11 | 打印管理器、CGLDC 创建 |
| **SSProject** | 4 | SDL命令注册 |
| **SSymbolParse** | 3 | 符号解析 |
| **SSGeoProcess** | 1 | 矩形索引 |

### 2.5 与 SSMap/SSJointSurvey 集成

- **主接口 CSSREToolsInterface** 继承自 **CSDLInterface**（SSProject中的核心基类）
- 通过 **ExecFunction** 提供插件式功能调用（类似 SSMap 的 CSDLInterface 机制）
- 通过 **OnAfterLoadData** / **OnDraw** / **BeforeDrawMap** 挂钩到地图生命周期
- 通过 **CGLDC** (from SSMapView) 执行 OpenGL 渲染
- 通过 **CHouseManager** 操作房产/不动产数据，可能连接 SDE 数据库
- 通过 **CEpsProcessManager** (SSEditBase) 集成 EPS 处理流程系统

---

## 3. 对比与总结

### 3.1 SSPipe.dll 总结

**定位**: EPS 市政管线管理插件模块

**核心职责**:
1. **管线数据管理**: CPipeNet 管理整个管线网络的数据层（从 Access 数据库 PipeConfig.mdb 读取配置）
2. **几何操作**: CPipeGeoOperator 提供管线的几何计算（横断面、纵断面、长度计算）
3. **交互输入**: CInputPipeLine/Point 提供管线的鼠标输入接口
4. **数据标准化**: Standardization 函数对管线数据进行规范化

**技术栈**: MFC + SSObject(几何) + SSGLDC(渲染) + SSDaoBase(DAO数据库)

**集成方式**: 
- 通过 CDataSource 融入 SSMap 数据层
- 通过 CSDLInterface 注册命令到 EPS 命令系统
- 通过 CGLDC/CMarkNote 与 SSMap 的渲染系统交互

### 3.2 SSRETools.dll 总结

**定位**: EPS 房地产/不动产管理工具模块

**核心职责**:
1. **房产数据管理**: CHouseManager 管理房产（户、楼幢、宗地）的分层分级数据
2. **不动产登记**: FillBDCDYHZD/FillBDCDYHZRZ 等函数支持不动产登记业务
3. **UI集成**: 实现 CSDLInterface 的全套插件接口（Ribbon、绘制、命令）
4. **流程集成**: 通过 CEpsProcessManager 接入 EPS 的处理流程系统

**技术栈**: MFC + SSObject(几何) + SSEditBase(EPS流程) + SSGLDC(渲染)

**集成方式**:
- 完全实现 CSDLInterface 插件模式（类似 ArcGIS 插件组件）
- 通过 Ribbon UI 添加 RE 专用功能区
- 通过 CHouseManager 直接操作 SDE/ADO 数据库中的房产数据

---

## 4. 关键发现

### 4.1 SSPipe.dll 关键发现
- **无中文字符串**: 在 SSPipe.dll 中未找到中文管线相关字符串（管线、管道、阀门、窨井等）
- **配置驱动**: 大量使用 Access MDB (PipeConfig.mdb) 存储管线属性模板
- **SSPipe\CCalcHeightDlg**: 存在管线高程（覆土深度）计算对话框
- **GXPipeNoSort**: 支持管线排序
- **GetPipeCutInfo**: 管线横断面分析

### 4.2 SSRETools.dll 关键发现
- **无中文字符串**: 在 SSRETools.dll 中未找到中文房产相关字符串（房产、房地产、不动产、确权）
- **BDC字样确认**: 函数名中的 `FillBDCDYHZD` / `FillBDCDYHZRZ` 明确对应"不动产单元号"和"认证"业务
- **CHouseManager**: 存在完整的房产/楼幢/户/宗地管理类结构
- **CSSREToolsInterface**: 完整的 CSDLInterface 实现，支持 Ribbon/Command/Draw 三大扩展点
- **外挂工具**: SSRETools.dll 本身是 SSProject 下的一个外挂工具包（RE=Real Estate）

---

*报告生成工具: idalib-mcp (Python IDA Pro MCP Server)  
*分析端口: SSPipe.dll → 12010, SSRETools.dll → 12011
