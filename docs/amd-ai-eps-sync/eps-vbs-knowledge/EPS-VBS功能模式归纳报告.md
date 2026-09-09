---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 95ce5665a2763fbde4f792b4da682b54_d650074fa5fa11f1891f525400f8a581
    ReservedCode1: yaoa75o8O+DLYCq1Y9su6AEseJ+jBwKJs4znajjsDi1RRkstC8rMF7EWLYEdlUhOyfUqIimLrky6whN4nmavZMMm0/ToSFLLb8IycjlNVHZK9pOKIcxxnNvuhtCYh6L7QioZK6NIRD105BaQ0iH79D02pOknl+fIfIUCCrH0/Th5+cim79NXld9JYRI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 95ce5665a2763fbde4f792b4da682b54_d650074fa5fa11f1891f525400f8a581
    ReservedCode2: yaoa75o8O+DLYCq1Y9su6AEseJ+jBwKJs4znajjsDi1RRkstC8rMF7EWLYEdlUhOyfUqIimLrky6whN4nmavZMMm0/ToSFLLb8IycjlNVHZK9pOKIcxxnNvuhtCYh6L7QioZK6NIRD105BaQ0iH79D02pOknl+fIfIUCCrH0/Th5+cim79NXld9JYRI=
---

# EPS-VBS 功能模式归纳报告（第二阶段）

> 分析对象：`C:\Users\Administrator\Desktop\EPS-VBS知识库`
> 分析口径：4783 个 VBS 脚本 → MD5 内容去重后 **1794 个唯一脚本**
> 聚类方法：以**脚本文件名+目录路径**为主信号（业务动作通常直接体现在命名中）、**脚本正文关键词**为辅信号，进行业务动作聚类；并对聚类结果抽样读取正文验证（取号/上传/下载/入库/出图/检查/建业务/撤单/数据转换等代表脚本均已通读骨架）。
> 与网络报告关系：本报告承接《EPS-VBS网络服务器深度分析报告.md》，从"功能模式"维度横向归纳整个脚本库；网络交互细节（JK 系列、Token、SSArcSDE、WebFiler 等）以网络报告为准。

---

## 一、业务动作聚类总览

按脚本内真实业务逻辑（而非目录名）归并后，1794 个唯一脚本分为 **21 个聚类**：

| 聚类名 | 脚本数 | 占比 | 宏观分层（主归属） |
|---|---:|---:|---|
| 数据转换类 | 365 | 20.3% | 数据采集层 / 数据处理层 |
| 检查质检类 | 320 | 17.8% | 质量控制层 |
| 入库类 | 222 | 12.4% | 系统集成层 |
| 出图成果类 | 190 | 10.6% | 成果输出层 |
| 属性处理类 | 115 | 6.4% | 数据处理层 |
| 编辑处理类 | 93 | 5.2% | 数据处理层 |
| 工具辅助类 | 87 | 4.8% | 工具辅助层 |
| 系统消息类（事件钩子） | 66 | 3.7% | 系统集成层 |
| 查询浏览类 | 63 | 3.5% | 工具辅助层 / 数据采集层 |
| 面积计算类 | 57 | 3.2% | 数据处理层 |
| 图层控制类 | 35 | 2.0% | 工具辅助层 |
| 报表统计类 | 31 | 1.7% | 成果输出层 |
| 上传类 | 30 | 1.7% | 系统集成层 |
| 取号类 | 27 | 1.5% | 系统集成层 |
| 拓扑构面类 | 25 | 1.4% | 数据处理层 |
| 下载类 | 16 | 0.9% | 数据采集层 / 系统集成层 |
| 坐标转换类 | 15 | 0.8% | 数据处理层 |
| 建业务接单类 | 14 | 0.8% | 系统集成层 |
| 文件管理类 | 13 | 0.7% | 数据采集层 / 工具辅助层 |
| 加密解密类 | 8 | 0.4% | 工具辅助层 |
| 撤单类 | 6 | 0.3% | 系统集成层 |

> 说明：边界聚类存在交叉（如"数据转换类"既包含外部数据调入（采集）也包含成果图输出（输出）；"下载类"既是数据采集入口也是系统集成通道），分层占比按主归属统计，交叉在第五章说明。

---

## 二、聚类详解

### 1. 取号类（27 个）

- **典型脚本示例**
  - `佛山基础地形测绘(外网)\Script\玮哥专用脚本\违法宗地取号.vbs` / `违法宗地取号2.vbs` / `违法宗地取号3.vbs`
  - `佛山基础地形测绘(外网)\Script\玮哥专用脚本\选择宗地范围获取宗地号或版本号.vbs`
  - `内网入库专用\Script\业务流程\选择勘界宗地范围获取勘界宗地号或版本号.vbs`
  - `南海农房\Script\业务流程\佛山取号.vbs`
  - `南海农房\Script\房产处理\连库申请幢下所有户预编不动产单元号（顺德）.vbs`
- **解决的业务问题**：在业务作业前，向服务器申请宗地号/版本号/预编不动产单元号等"官方编号"，是测绘成果与不动产登记库建立关联的第一环。取号结果决定后续作业文件的命名与业务挂接。
- **通用脚本骨架**（依据《违法宗地取号.vbs》真实代码归纳）：
  1. `OnInitScript()` 入口：可选登录/加密狗校验（`SSERPTool.IsLogin`、`getdogrw(dogcode)` 读取狗号）→ `SSProcess.ShowScriptDlg mode,title` 弹出提示对话框；
  2. 用户右键选择宗地/违法界线要素触发；
  3. `geterpaddress URLnew` 从配置获取 ERP 服务地址；`SSERPTool.GetTokenAndInvalidTime Token,InvalidTime` 获取访问令牌；
  4. 构造 ArcGIS REST 式查询串（`where/geometry/outFields/returnCountOnly/f=pjson`），经 `encodestr` 编码后封装 `_namespace=erp.gis.arcgisserverhelper.interfaceentry&access_token=...&methodname=JK接口名&parameter=...`；
  5. `Microsoft.XMLHTTP` POST 请求 → 解析返回 JSON（`getHTTPcount`/`getHTTPattr` 提取 count 与要素属性）→ 判断是否可取号 → 回写宗地属性/提示结果。
- **网络特征**：走 ERP 统一接口网关（JK 系列接口 + Token 鉴权），属于**系统集成层**的"申请类"接口调用。

---

### 2. 上传类（30 个）

- **典型脚本示例**
  - `顺德基础测绘\Script\业务流程\宗地图（不动产宗地、勘界、违法、其他）上传资料到业务OA系统.vbs`
  - `佛山基础地形测绘(外网)\Script\玮哥专用脚本\上传宗地图.vbs`
  - `内网入库专用\Script\业务流程\上传预售所有成果数据.vbs`
  - `工程测量\Script\业务流程\上传资料到业务OA系统.vbs`
  - `内网入库专用\Script\业务流程\上传成果块图edb.vbs`
- **解决的业务问题**：将测绘作业成果（宗地图 EDB、成果块图、资料文件）按业务编号上传至 OA/业务系统，供登记、审批、入库环节使用；是"成果提交"的关键动作。
- **通用脚本骨架**（依据《上传宗地图.vbs》真实代码归纳）：
  1. `OnClick()`：`SSProcess.ClearInputParameter/AddInputParameter/ShowInputParameterDlg` 弹出"成果图类型"参数对话框（不动产宗地图/勘界图/违法图/其他宗地）；
  2. 按类型分支进入对应上传函数；
  3. 身份与业务上下文：`SSERPTool.GetTokenAndInvalidTime` + `SSERPTool.GetCurWorkInfo` + `SSERPTool.GetUserInfo`；校验 `Token=""`（未登录）、`WorkIID=""`（未接单）则退出；
  4. 检查工程作业信息：`SSProcess.ReadEpsDBIni("采集单位信息","测量员/绘图员/检查员/...")`，缺失则提示先设置；
  5. `reGetWork(WorkIID,Token,UserID,WorkWIID,"作业登记",0)` 重新接单确认业务状态；
  6. 复制当前 EDB 到 `upload\` 目录 → `uploadZDCGfile` 上传文件 → 删除临时目录；
  7. 读 EDB 数据库提取地籍号/版本号（`GetGLTableValue`）→ 按编号规则构造服务器目录路径 → 上传资料文件；
  8. `MsgBox` 提示结果。
- **网络特征**：`SSFileUploadControl` 分块上传 + `workflowsubmit`/`CommonOperate` 提交，属系统集成层"成果上报"通道。

---

### 3. 下载类（16 个）

- **典型脚本示例**
  - `内网入库专用\Script\业务流程\下载数据函数.vbs`
  - `内网入库专用\Script\业务流程\下载数据.vbs`
  - `内网入库专用\Script\业务流程\自动下载申请数据.vbs`
  - `内网入库专用\Script\接口调用\下载数据.vbs`
  - `佛山基础地形测绘(外网)\Script\玮哥专用脚本\输入宗地号下载宗地和房屋.vbs`
- **解决的业务问题**：从 SDE 现势库/南方权籍库等服务器数据源，按宗地号（+自然幢号/层号/房屋 ID）下载宗地、界址点线、幢、户等不动产要素到本地工程，是作业的"取数"环节，支持多源回退（本地库无则回源权籍库）。
- **通用脚本骨架**（依据《下载数据函数.vbs》真实代码归纳）：
  1. `OnClick()`：设置查询条件（宗地号 ZDH、自然幢号 ZRZH、层号 CH、房屋 ID FWID）；
  2. `SSArcSDE.ConnectToTablespace("SDBDC")` 连接服务器表空间；
  3. 主函数 `DownLoadBDCDate` 分三种情况：
     - 情况1：`SSArcSDE.SearchFeatureAttr` 在 `SDBDC.SHIYQZDJBXX` 按 `DJH=宗地号` 查 ZDGUID → 命中则 `SSArcSDE.DownloadSDEDBToLocalDB` 依次下载宗地、界址点 JZD、界址线 JZX，再递归下载幢（ZRZ）、房屋面（FWMJK、FWWQX、FWFHZQX、FWLC、FWH、FangCZJ 等）；
     - 情况2：本地库查不到 → 调 `ISCBDCWEBSERVER(ZDH,...)` 回源**南方权籍库 Web 服务**，解析坐标串并绘制宗地范围；
     - 情况3：两库皆无 → 按范围下载 `SHIYQZDJBXX,QiTZD_500,JZD,JZX` 全部要素。
- **网络特征**：SSArcSDE 直连表空间 + Web 服务双源回退，属系统集成层"取数"通道，也是数据采集入口。

---

### 4. 检查质检类（320 个）

- **典型脚本示例**
  - `南海农房\Script\不动产相关数据检查\必填信息检查.vbs`
  - `规范性核实\Script\GH规划核实检查\面积块必填检查.vbs`、`FC_层必填检查.vbs`、`属性必填检查.vbs`
  - `佛山基础地形测绘(外网)\Script\不动产相关数据检查\FDCQ1房地产权信息表必填及异常数据检查.vbs`、`GUID不合法数据检查.vbs`、`各种面积进位检查.vbs`
  - `佛山基础地形测绘(专网)\Script\数据检查\分摊功能区合法性检查.vbs`、`零碎线面检查.vbs`、`最小面积检查.vbs`
- **解决的业务问题**：成果上交前的**数据自检/质检**——必填项、字段合法性、面积进位、拓扑关系、分层图与房产簿一致性、GUID 合法性、权籍信息表一致性等，把人工质检规则固化为可重复执行的脚本。
- **通用脚本骨架**（依据《必填信息检查.vbs》真实代码归纳）：
  1. `OnClick()`：`SSProcess.RemoveCheckRecord "属性项检查","必填信息检查"` 清除旧检查记录；
  2. 构造选择条件：`ClearSelection/ClearSelectCondition` → `SetSelectCondition("SSObj_Type","==","AREA")`、`SetSelectCondition("SSObj_Code","==","6801053,...")` → `SelectFilter` 过滤要素；
  3. 遍历 `GetSelGeoCount/GetSelGeoValue`，逐要素读取属性（`[业务编号][宗地代码][使用权人][发证面积]...`）做规则判断（长度/非空/枚举）；
  4. 不满足则 `SSProcess.AddCheckRecord` 登记检查问题（带地物 ID、坐标、类型），供用户在检查窗口中定位、跳转、逐条修改；
  5. 检查结果进入 EPS 统一检查面板，而非弹窗堆砌。
- **价值**：形成"规则库+检查面板"闭环，是质量控制层的核心。

---

### 5. 出图成果类（190 个）

- **典型脚本示例**
  - `佛山基础地形测绘(专网)\Script\地籍处理\输出勘界图.vbs`、`输出违法图.vbs`、`输出宗地楼幢示意图.vbs`
  - `联合测绘\Script\报表输出\输出佛山市建设工程联合测绘成果报告.vbs`
  - `存量房测绘\Script\报表输出\输出佛山市建设工程联合测绘成果报告1030.vbs`
  - `佛山基础地形测绘(外网)\Script\业务成果输出\用地红线图输出.vbs`
  - `佛山市国土资源业务\Script\业务图件输出\图廓-排序-条形码-裁切.vbs`、`生成条形码.vbs`
- **解决的业务问题**：把测绘数据变成**可交付的图件/报告**——勘界图、宗地图、违法图、用地红线图、分层分户图、联合测绘成果报告（Word/PDF）等，含图廓、比例尺、条形码、审图要素等出版级处理。
- **通用脚本骨架**（依据《输出勘界图.vbs》真实代码归纳）：
  1. 全局声明图廓参数（纸张、比例尺、外接矩形、图廓坐标）；
  2. `OnInitScript()`：`SSProcess.ReadEpsDBIni("ERPManager","ERP_UserName/ERP_DeptName/...")` 读取作业人员信息；`SetDlgIni` 初始化出图对话框（比例尺、绘制人、日期等）；
  3. 用户选择出图要素/纸张（B5/A4/A3/A2，横/纵），`GetTKinfo` 按纸张设置图廓边距；
  4. 读取宗地属性（权利人 QLR、坐落 ZL、用途、面积、发证情况等 Dfields 数组）→ 出图排版 → 绘制图廓、注记、图例；
  5. 报告类（联合测绘成果报告）则批量读库（ADODB/EDB 数据）→ 填表 → Word/PDF 输出。
- **价值**：成果输出层主体，支撑"一张图"交付与登记发证材料。

---

### 6. 入库类（222 个）

- **典型脚本示例**
  - `内网入库专用\Script\PDB出入库\宗地入库.vbs`、`勘界违法数据入库.vbs`、`修测范围线入库.vbs`
  - `内网入库专用\Script\PDB出入库\ArcGIS PDB调入.vbs`、`ArcGIS PDB输出.vbs`
  - `内网入库专用\Script\PDB出入库\范围线内认可冲突数据.vbs`、`选择问题点认可本地数据.vbs`
  - `存量房测绘\Script\PDB出入库\生成出入库脚本.vbs`
- **解决的业务问题**：本地测绘成果（宗地、房屋、修测范围）**写回服务器现势库**，包含冲突检测（相交/包含）、历史库推挤、人工认可冲突数据等入库冲突治理流程。
- **通用脚本骨架**（依据《宗地入库.vbs》真实代码归纳）：
  1. `OnClick()`：`SSDbSynTools.IsExistRemoteDBTable` 检查是否已登录数据库；
  2. `ClearSelection/SetSelectCondition/SelectFilter` 选择待入库宗地面（校验唯一）；
  3. `isxjbh(id,5/kobjectids)` 判断本地宗地与库中宗地**相交/包含**关系；
  4. 无冲突 → `MsgBox` 确认入库；有冲突 → 提示"相交包含库宗地将推入历史库，本地选择宗地入现势库"；
  5. 冲突库宗地 `deleteksj` 推历史 → `SSParameter.SetParameterSTR "GetEPSFeature","ImportEpsIDList",epsObjIDs` 指定入库要素；
  6. `SSDbSynTools.UploadLocalDBToRemoteDB(connectionHandle,layerName,updateMode)` 上传入库（0 自动检测/1 新增/2 历史）→ `MsgBox "入库成功"`。
- **价值**：系统集成层最大的聚类，体现"本地作业库 ↔ 服务器现势库"双向同步能力。

---

### 7. 建业务接单类（14 个）

- **典型脚本示例**
  - `内网入库专用\Script\业务流程\新建业务.vbs`
  - `内网入库专用\Script\业务流程\创建宗地图子业务.vbs`
  - `内网入库专用\Script\业务流程\当前宗地图创建业务并接单.vbs`
  - `内网入库专用\Script\业务流程\宗地图（不动产宗地、勘界、违法、其他）创建业务.vbs`
  - `内网入库专用\Script\接口调用\接单处理.vbs`
- **解决的业务问题**：在业务 OA/ERP 中**创建/认领作业任务**（接单），把当前 EDB 工程与服务器端业务实例（IID/WIID）绑定，是后续取号、上传、撤单的前提。
- **通用脚本骨架**（依据《新建业务.vbs》真实代码归纳）：
  1. `OnClick()`：读 `ERPManager/ERP_IID`，已接单则提示"可使用本工程撤单功能"退出；
  2. `SSERPTool.GetNewWorkInfo WorkInfo` 获取服务器下发的待办业务列表；
  3. 解析 WorkInfo 提取工程名/IID/WIID；
  4. 构造 `_namespace=erp.pro.unithelper.unitaccept&access_token=...&iid=...&wiid=...`，POST 到 `URLT & "/CommonOperate"`；
  5. 响应写入 `SSParameter.SetParameterSTR "ERPManager","AcceptWorkList",str`；
  6. `SSProcess.WriteEpsDBIni "ERPManager","ERP_IID/ERP_Name/ERP_WIID"...` 将业务上下文持久化到工程配置。
- **网络特征**：`erp.pro.unithelper.unitaccept` + `/CommonOperate`，与撤单（`getunitinfobysd`）成对，是业务生命周期管理的两端。

---

### 8. 撤单类（6 个）

- **典型脚本示例**
  - `内网入库专用\Script\业务流程\本工程撤单.vbs`
  - `内网入库专用\Script\接口调用\当前工程有条件撤单.vbs`
  - `内网入库专用\Script\接口调用\撤单处理.vbs`
  - `工程测量\Script\接口调用\当前工程有条件撤单.vbs`
  - `房地一体\Script\成果提交流程\接单撤单.vbs`
- **解决的业务问题**：释放已接单任务（未提交/超时/交接），清空工程内 ERP 业务上下文，使工程可重新接单。
- **通用脚本骨架**（依据《当前工程有条件撤单.vbs》真实代码归纳）：
  1. `OnClick()` → `autocancel()`；
  2. `SSERPTool.IsLogin` 校验登录 → 读 `ERPManager/ERP_IID`；
  3. `SSERPTool.GetTokenAndInvalidTime` 取 Token；
  4. POST `_namespace=erp.pro.unithelper.getunitinfobysd&...&iid=WorkIID&fields=FIRST_ACCEPTED_TIME` 查询接单状态；
  5. 若服务器返回"未受理/未接受"（`first_accepted_time` 为空）→ `SSERPTool.ClearWorkInfo()` + `WriteEpsDBIni` 逐项清空 IID/Name/WIID/Acceptedtime 等。
- **价值**：与建业务接单类构成完整的"业务实例生命周期"闭环（创建→接单→作业→提交→撤单）。

---

### 9. 数据转换类（365 个）

- **典型脚本示例**
  - `三维测图\Script\CASS转换\CASS9数据导入.vbs` / `CASS9数据输出.vbs`
  - `三维测图\Script\SHP出入库\Shp调入.vbs` / `Shp输出.vbs`
  - `三维测图\Script\输出MDB\MDB调入.vbs` / `MDB输出.vbs`
  - `联合测绘\Script\数据转换\ArcGIS PDB调入2k.vbs` / `规划、房产成果图输出dwg.vbs`
  - `佛山基础地形测绘(专网)\Script\数据转换\ZDB库宗地数据标准转换.vbs`、`地形数据标准批文件转换.vbs`
- **解决的业务问题**：跨格式/跨标准数据互通——CASS/DWG/SHP/MDB/PDB/ZDB/二调数据等外部格式的调入与输出，以及老版本数据到现行标准的升级转换（编码、线型、点型标准化）。
- **通用脚本骨架**（依据《ZDB库宗地数据标准转换.vbs》真实代码归纳）：
  1. `OnClick()`：`SSProcess.SelectFileName` 文件选择对话框选源文件；
  2. `ADODB.Connection` 打开外部库（`PROVIDER=microsoft.jet.oledb.4.0`）→ `Recordset` 逐条读记录（宗地编码/宗地号/比例尺/图形信息）；
  3. 对每条：`SetSelectCondition/SelectFilter/DeleteSelectionObj` 清空 EDB 旧数据 → `SetMapScale` 设比例尺 → `SetDataXParameter("DataType","22")` + `ImportDataFromStream` 导入图形；
  4. 遍历要素按地物编码（5110/5124/5231/5155...）修正点型/线型/编码（`SetSelGeoValue "SSObj_PointType(n)"`）；
  5. 保存、循环下一条。
- **价值**：最大聚类（20.3%），是软件"数据生态兼容性"的体现——EPS 以此对接 CASS 等历史数据资产。

---

### 10. 坐标转换类（15 个）

- **典型脚本示例**
  - `内网入库专用\Script\123\选择54(109)-2000(109).vbs`
  - `工程测量\Script\缩编\2000比例尺符号换码.vbs`
- **解决的业务问题**：不同坐标基准（北京54/西安80/国家2000）与不同中央子午线带之间的转换、符号换码。
- **骨架特征**：选择源坐标系 → 遍历要素批量换算坐标/换码 → 回写。

---

### 11. 面积计算类（57 个）

- **典型脚本示例**
  - `内网入库专用\Script\系统消息\预测面积到实测面积（临时）.vbs`
  - `佛山市国土资源业务\Script\变更处理\图斑面积平差.vbs`
  - `房地一体\Script\面积块赋值\面积块赋值.vbs`
  - `内网入库专用\Script\房产处理\分摊变更面积计算.vbs`
- **解决的业务问题**：房产面积计算、公摊分摊、面积平差、预测/实测面积映射等——房产测绘的核心计算逻辑。
- **骨架特征**：遍历面积块/图斑要素 → 读取面积属性与分摊规则 → 计算/平差 → 回写属性并校验比率和。

---

### 12. 拓扑构面类（25 个）

- **典型脚本示例**
  - `佛山市国土资源业务\Script\变更处理\行政区拓扑构面处理.vbs`、`图斑分割变更.vbs`、`图斑合并变更.vbs`、`图斑构面.vbs`
  - `佛山基础地形测绘(专网)\Script\房产处理\房产面积块拓扑构面.vbs`
- **解决的业务问题**：由线/弧段构面、图斑分割合并、拓扑检查与重建，支撑变更调查业务。
- **骨架特征**：选择边界线 → `TopProcess`/`SearchOuterObjIDs` 拓扑构面 → 面要素属性赋值 → 与原图斑比较。

---

### 13. 属性处理类（115 个）

- **典型脚本示例**
  - `房地一体\Script\房屋属性提取\无层高房屋属性赋值.vbs` / `有层高房屋属性赋值.vbs`
  - `房地一体\Script\宗地点线赋值\界址点线赋值.vbs`
  - `存量房测绘\Script\规划分层\面积块属性录入.vbs`
  - `三维测图\Script\编辑处理\绘制房屋面后属性录入.vbs`
- **解决的业务问题**：批量属性赋值/提取/补录（房屋属性、界址点线属性、面积块属性、坐落户号等），降低人工录入成本。
- **骨架特征**：选择目标要素 → 读取来源（图形/外部 Excel/已有属性）→ `SetSelGeoValue/SetNewObjValue/SetObjectAttr` 批量赋值 → 统计反馈。

---

### 14. 编辑处理类（93 个，含原"未识别"中按正文确认的图面编辑脚本）

- **典型脚本示例**
  - `三维测图\Script\数据编辑\去白模.vbs`、`等高线清除9999.vbs`、`棚房节点取舍.vbs`
  - `三维测图\Script\编辑处理\AfterAddLine.vbs`、`AfterAddPoint.vbs`（**绘制事件联动**）
  - `工程测量\Script\缩编\删除坐标为0的点和注记.vbs`、`删除地下室.vbs`
  - `佛山基础地形测绘(专网)\Script\佛山市测绘\自动消隐处理.vbs`
- **解决的业务问题**：图形数据日常编辑、图面清理、节点取舍、消隐、缩编，以及**绘制过程中的事件联动**（加线/加点后自动处理）。
- **骨架特征**：EPS 事件回调（AfterAddLine/AfterAddPoint/AfterSelectionItemChange）或右键菜单 → 遍历新增/选中要素 → 按规则增删改 → 刷新。

---

### 15. 系统消息类（事件钩子，66 个）

- **典型脚本示例**
  - `内网入库专用\Script\系统消息\BeforeImportProjectData.vbs`（导入工程前钩子）
  - `佛山基础地形测绘(外网)\Script\系统消息\AfterOpenEdb.vbs`（打开 EDB 后钩子）
  - `内网入库专用\Script\系统消息\AfterUpdateLocalREProjectToSDE.vbs`（本地工程同步 SDE 后钩子）
  - `内网入库专用\Script\系统消息\BdcProjectMan_GetScriptMenuItem.vbs` / `BdcProjectMan_GetScriptMenuCmds.vbs`（动态菜单注入）
  - `存量房测绘\Script\系统消息\匹配预售excel.vbs`、`佛山业务取号.vbs`
- **解决的业务问题**：在 EPS 关键生命周期节点（打开工程、导入数据、同步 SDE、提交检查）**自动注入业务逻辑**，实现"开图即取号""入库后自动同步属性""动态菜单"等系统级扩展。
- **骨架特征**：函数名即事件点（Before/After 前缀）→ 事件触发时执行批量属性/网络/检查逻辑 → 无 UI 或极简提示。
- **价值**：这是 EPS 扩展性的"事件驱动层"，让业务规则无需改主程序即可挂接到系统流程。

---

### 16. 查询浏览类（63 个）

- **典型脚本示例**
  - `内网入库专用\Script\信息中心测管所临时使用\SDE查询定位.vbs`、`宗地号查询定位.vbs`、`房产楼盘查询.vbs`
  - `佛山基础地形测绘(专网)\Script\地籍处理\浏览图片点挂接图片.vbs`
- **解决的业务问题**：按宗地号/业务号/空间位置查询定位要素、挂接浏览图片资料。
- **骨架特征**：输入查询条件 → `SearchFeatureAttr`/SDE 查询 → 定位/高亮 → 展示结果。

---

### 17. 报表统计类（31 个）

- **典型脚本示例**
  - `内网入库专用\Script\报表输出\宗地部分报表输出.vbs`、`房屋户部分报表输出.vbs`
  - `工程测量\Script\土方\生成地块汇总统计表.vbs`、`土方成果自动比对.vbs`
  - `存量房测绘\Script\系统消息\匹配预售excel.vbs`
- **解决的业务问题**：台账/清单/统计表（Excel/Word）生成，土方成果自动比对。
- **骨架特征**：遍历要素/读库 → 聚合统计 → 写 Excel（`excel` 对象/ADODB）→ 保存。

---

### 18. 图层控制类（35 个）

- **典型脚本示例**
  - `存量房测绘\Script\图层显示控制\图层显示（自然幢）.vbs`
  - `佛山基础地形测绘(专网)\Script\图层显示控制\图层关闭（逻辑幢）.vbs`
  - `内网入库专用\Script\图层显示控制\图层显示（不动产/地形/宗地）.vbs`
- **解决的业务问题**：按业务场景一键显隐图层，辅助编辑与检查。
- **骨架特征**：`SetLayerVisible`/图层枚举 → 批量设置显隐。

---

### 19. 文件管理类（13 个）

- **典型脚本示例**
  - `内网入库专用\Script\37服务器资料规整\违法资料根据oracle库重命名并另存.vbs`、`宗地根据oracle改名另存.vbs`
  - `存量房测绘\Script\佛山市测绘\压缩文件.vbs`、`联合测绘\Script\数据转换\解压缩.vbs`
- **解决的业务问题**：服务器资料规整（按 Oracle 库内容重命名/归类另存）、压缩解压。
- **骨架特征**：`FileSystemObject`/压缩组件 → 遍历文件 → 按规则复制/改名 → 落盘。

---

### 20. 加密解密类（8 个）

- **典型脚本示例**
  - `内网入库专用\Script\圆周率加密\文件加密.vbs`、`实体加密.vbs`
- **解决的业务问题**：成果文件/实体的数据保护（圆周率加密等自定义算法）。
- **骨架特征**：选择文件/实体 → 读取二进制 → 加密算法变换 → 写回。

---

### 21. 工具辅助类（87 个）

- **典型脚本示例**
  - `联合测绘\Script\公共函数\WordVbsFunc.vbs`、`公共函数\FileFolderOperateFunc.vbs`
  - `房地一体\Script\信息录入功能DLG\功能参数设置.vbs`
  - `三维测图\Script\帮助\在线帮助.vbs`
  - `佛山基础地形测绘(专网)\Script\公共函数\processbar.vbs`
- **解决的业务问题**：公共函数库（Word/文件操作/进度条/JSON 解析）、参数设置、帮助文档，被各业务脚本 `#include` 复用。
- **价值**：脚本库的"基础设施层"，大量业务脚本顶部 `#include ".\接口调用\Function_JK.vbs"` 等即依赖此类。

---

## 三、通用架构模式归纳

对 1794 个唯一脚本的通读与抽样验证表明：**EPS 业务脚本遵循高度统一的"五段式"架构**，只是各段权重不同：

```
┌─ 1. 入口与上下文 ─────────────────────────────┐
│  Sub OnClick() / OnInitScript() / OnOK()      │  ← EPS 事件入口
│  SSProcess.ShowScriptDlg / ShowInputParameterDlg│  ← 对话框（参数/提示）
│  SSProcess.ReadEpsDBIni("ERPManager",...)     │  ← 读工程上下文(作业信息)
│  SSProcess.GetProjectFileName                 │  ← 当前工程文件
├─ 2. 参数获取与身份校验 ────────────────────────┤
│  SSProcess.AddInputParameter/GetInputParameter│  ← 用户输入参数
│  SSERPTool.GetTokenAndInvalidTime Token,InvalidTime│ ← 获取访问令牌
│  SSERPTool.IsLogin / GetUserInfo / GetCurWorkInfo│ ← 登录/接单校验
│  getdogrw(dogcode)（加密狗）/ 单位信息校验     │
├─ 3. 数据选择与业务处理 ────────────────────────┤
│  ClearSelection/SetSelectCondition/SelectFilter│  ← 过滤要素
│  GetSelGeoCount/GetSelGeoValue/GetObjectAttr   │  ← 遍历要素/读属性
│  SSArcSDE.SearchFeatureAttr（库查询）         │
│  SSDbSynTools.IsExistRemoteDBTable（库检查）   │
├─ 4. 服务器交互 ───────────────────────────────┤
│  XMLHTTP POST：_namespace=erp.*&access_token=…│  ← ERP/业务接口网关
│    （CommonOperate / interfaceentry / JK接口） │
│  SSArcSDE.DownloadSDEDBToLocalDB（下载）      │
│  SSDbSynTools.UploadLocalDBToRemoteDB（入库）  │
│  SSFileUploadControl/uploadZDCGfile（上传）    │
├─ 5. 结果处理与 UI 反馈 ───────────────────────┤
│  instr/mid 解析 JSON 响应（返回码/数据）      │
│  AddCheckRecord（检查记录）/ SetObjectAttr     │
│  WriteEpsDBIni / SSParameter.SetParameterSTR   │  ← 持久化
│  MsgBox 提示 / CloseScriptDlg 关闭            │
└───────────────────────────────────────────────┘
```

**要点解读**

1. **事件入口统一**：绝大多数脚本以 `OnClick`（菜单/按钮触发）、`OnInitScript/OnExitScript`（脚本生命周期）、`OnOK/OnRButtonDown`（对话框/右键）为入口；另有系统级事件钩子（`AfterOpenEdb`、`BeforeImportProjectData` 等）供全局挂接。
2. **身份鉴权标准化**：凡涉及服务器交互的脚本，第一步几乎都是 `SSERPTool.GetTokenAndInvalidTime Token,InvalidTime` 取 Token，配合 `IsLogin`/`GetUserInfo`/`GetCurWorkInfo` 校验登录与接单状态——鉴权逻辑已固化为模板。
3. **要素遍历三板斧**：`SetSelectCondition` + `SelectFilter` 过滤 → `GetSelGeoCount` 计数 → `GetSelGeoValue(i,字段)` 逐条读/写，是本地数据处理的标准循环体。
4. **网络交互双通道**：业务级交互走 `XMLHTTP` + `erp.*` 命名空间（`/CommonOperate` 通用操作、`erp.gis.arcgisserverhelper.interfaceentry` 地图服务、`erp.pro.unithelper.*` 业务助手）；数据级交互走 `SSArcSDE`（表空间直连）/`SSDbSynTools`（远程库同步）/`SSFileUploadControl`（文件上传）。
5. **结果反馈三形态**：检查类用 `AddCheckRecord` 进检查面板；数据类用 `WriteEpsDBIni`/`SetParameterSTR` 持久化；交互类用 `MsgBox` 即时提示。
6. **代码复用**：大量脚本通过 `#include ".\接口调用\Function_JK.vbs"`、`#include ".\接口调用\erpnetaddress.vbs"` 复用公共函数（取地址、发请求、解析 JSON、加密狗），形成模块化基础库。

---

## 四、宏观分层：生产系统全景

将 21 个聚类按"数据采集 → 数据处理 → 质量控制 → 成果输出 → 系统集成 → 工具辅助"六层组织（占比按 1794 个唯一脚本计算）：

| 宏观层 | 包含聚类 | 脚本数 | 占比 | 业务含义 |
|---|---|---:|---:|---|
| **数据采集层** | 下载类(16)、数据转换类-调入侧(≈330)、文件管理类(13) | ≈394 | **22.0%** | 从外部格式（CASS/DWG/SHP/MDB/PDB/ZDB）与服务器库（SDE/权籍库）把数据"拿进来" |
| **数据处理层** | 属性处理类(115)、编辑处理类(93)、面积计算类(57)、拓扑构面类(25)、坐标转换类(15)、数据转换类-转换侧(≈35) | ≈340 | **19.0%** | 图形/属性/面积/坐标的加工、赋值、构面、标准化 |
| **质量控制层** | 检查质检类(320) | 320 | **17.8%** | 必填、合法性、一致性、面积进位等检查，固化质检规则 |
| **成果输出层** | 出图成果类(190)、报表统计类(31) | 221 | **12.3%** | 勘界图/宗地图/红线图/联合测绘报告/台账等可交付成果 |
| **系统集成层** | 入库类(222)、系统消息类(66)、上传类(30)、取号类(27)、下载类(16)、建业务接单类(14)、撤单类(6) | ≈381 | **21.2%** | 与 ERP/OA/SDE/权籍库的业务流、数据流双向对接（本层与数据采集层有交叉） |
| **工具辅助层** | 工具辅助类(87)、查询浏览类(63)、图层控制类(35)、加密解密类(8) | 193 | **10.8%** | 公共函数、定位浏览、图层显隐、数据保护等支撑能力 |

> 分层口径说明：下载类在"数据采集"与"系统集成"间有交叉（按主归属计入数据采集层，网络报告中计入系统集成层）；入库类、上传类、取号类等与网络服务强相关，是"系统集成层"骨架，占比约 21%。

**全景解读**

1. **这是一套完整的"地籍/房产测绘生产管理系统"**：采集（外部数据+服务器取数）→ 加工（属性/面积/拓扑）→ 质检（规则检查）→ 输出（图件/报告）→ 集成（ERP 业务流+服务器库同步）→ 工具（公共能力）。六个环节由脚本全部覆盖，说明 EPS 在佛山/顺德等地被深度定制为"生产流水线"而非单纯绘图软件。
2. **系统集成层与网络报告互相印证**：约 21% 的脚本直接与服务器交互（取号 27、上传 30、下载 16、入库 222、建业务 14、撤单 6、事件钩子 66），其中入库类高达 222 个——"本地作业库 ↔ SDE 现势库"的双向同步是核心集成场景，与网络报告中的 SSArcSDE、Token、WebFiler、JK 系列证据完全对应。
3. **质量控制被脚本化**：17.8% 的脚本是检查类，说明用户把大量登记审查规则（必填、一致性、面积进位）沉淀为可重复执行的自动检查，直接降低人工质检成本。
4. **事件钩子体现扩展性**：66 个系统消息脚本证明 EPS 提供了"打开工程/导入数据/同步 SDE/提交检查"等生命周期钩子，用户无需改主程序即可挂接业务规则——这是 EPS 扩展性的关键机制之一。
5. **重复率高是"版本化定制"的结果**：原始 4783 个脚本中约 78% 为重复/副本，原因是同一功能在不同模块（顺德基础测绘/内网入库专用/南海农房/存量房测绘等）各保留一份演化版本（如《输出佛山市建设工程联合测绘成果报告》存在 1007/1008/1017/1030 等十余个版本），反映"按项目拷贝定制、未回灌公共库"的维护模式。

---

## 五、关键发现与意义解读

1. **脚本库=业务规则的活文档**：每个 VBS 都是一条可追溯的业务规则（取号规则、检查规则、出图规则），1794 个唯一脚本构成"佛山/顺德不动产测绘业务规则全集"，对理解 EPS 落地形态有直接价值。
2. **扩展性体现在三个层次**：① 菜单脚本（OnClick 挂菜单）；② 事件钩子（Before/After 生命周期）；③ 公共函数库（#include 复用）。三者叠加使 EPS 从"通用测绘平台"变成"地籍房产生产专用系统"。
3. **服务器依赖集中且模式统一**：所有服务器交互收敛为 Token+XMLHTTP/SSArcSDE 两套通道，接口名（erp.* 命名空间、JK 系列）构成隐藏的"EPS 开放接口面"，网络报告已提取其中证据链，可作为后续接口逆向/文档化的索引。
4. **本报告为第三阶段（AI 深度分析/能力矩阵）提供聚类索引**：每类脚本的代表与骨架可直接用于"EPS 能做什么"的能力清单与"怎么做"的实现模式推导。

---

*报告生成时间：2026-09-01；数据源：EPS-VBS知识库（4783 个 VBS，去重后 1794 个唯一脚本）；配套中间产物：temp/func_cluster_v2.json（全量聚类明细）。*
*（内容由AI生成，仅供参考）*
