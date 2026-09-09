---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 95ce5665a2763fbde4f792b4da682b54_d711ee3ea5fa11f1891f525400f8a581
    ReservedCode1: JFWrVnwLP+csTYWaGKOGuCLHmcA7ZXTLPaS6Ccnpg+yr1SHpAJTKaBsk7n8bB20fReNm3yde1pgKhE0KUmU2rtMDek0jupOSWp77+baVlMMW8kELowPeCamaD5E8jnKA02UyFIzdu1CpelpyBq2O1K1nox6cetn2lLPKE9MhW8SsakEMyYrHbw3lMkc=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 95ce5665a2763fbde4f792b4da682b54_d711ee3ea5fa11f1891f525400f8a581
    ReservedCode2: JFWrVnwLP+csTYWaGKOGuCLHmcA7ZXTLPaS6Ccnpg+yr1SHpAJTKaBsk7n8bB20fReNm3yde1pgKhE0KUmU2rtMDek0jupOSWp77+baVlMMW8kELowPeCamaD5E8jnKA02UyFIzdu1CpelpyBq2O1K1nox6cetn2lLPKE9MhW8SsakEMyYrHbw3lMkc=
---

# EPS 扩展性深度分析报告（第三阶段）

> 分析对象：`C:\Users\Administrator\Desktop\EPS-VBS知识库`（4783 个 VBS，去重后 1794 个唯一脚本）+ 《EPS_VBS_API参考手册.md》（345 个 API 方法，含全库调用统计）
> 前置成果：本报告基于《EPS-VBS网络服务器深度分析报告.md》（网络/服务器专项）与《EPS-VBS功能模式归纳报告.md》（功能模式全景）两阶段结论，从"平台扩展性"维度回答：**EPS 能做什么、怎么做、为什么用 VBS 做、这些脚本意味着什么**。

---

## 一、SSProcess API 能力矩阵

依据官方《EPS_VBS_API参考手册》的调用统计（调用次数/使用文件数为全库真实扫描值），将 345 个 API 方法按能力域组织如下。**API 族**为同名系列方法，**代表方法**为全库调用量最高的方法（括号内为调用次数），**真实代码示例**全部取自知识库脚本/手册。

### 1. 要素选择与遍历（核心域，调用量最大）

| API 族 | 代表方法（调用次数） | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 选择条件 | `SetSelectCondition`(14935)、`ClearSelectCondition`(7515) | `SSProcess.SetSelectCondition "SSObj_Type","==","POINT,LINE,AREA"` | 一切按条件选要素的操作 |
| 过滤执行 | `SelectFilter`(6658) | `SSProcess.SelectFilter` | 按编码/类型/图层/数据标记过滤 |
| 遍历读取 | `GetSelGeoCount`(4514)、`GetSelGeoValue`(14437) | `For i=0 To count-1: id=SSProcess.GetSelGeoValue(i,"SSObj_ID"): Next` | 逐要素读属性（检查、赋值、统计） |
| 选择集管理 | `ClearSelection`(7520)、`UpdateSysSelection`、`DelSelGeo` | `SSProcess.ClearSelection` | 清空/刷新/删除选择集 |
| 坐标读取 | `GetSelGeoPoint`(2118)、`GetSelGeoPointCount` | `SSProcess.GetSelGeoPoint i, 0, xf, yf, z, ptype, name` | 获取要素首尾点/坐标串 |
| 批量改属性 | `ChangeSelectionObjAttr`(1395) | `SSProcess.ChangeSelectionObjAttr "SSObj_Code","7101023"` | 批量换码、批量赋值 |
| 选择集运算 | `SelectionObjMerge`、`ExplodeSelectionObj`、`SelectionObjClip`、`SelectionObjTopProcess` | `SSProcess.SelectionObjMerge` | 合并/炸开/裁剪/拓扑处理选中要素 |

**业务解读**：这是 EPS 脚本的"抓手"——90% 的本地业务脚本靠"条件过滤→遍历→读改"三板斧完成，功能模式报告中的检查类、属性处理类、面积计算类均构建于此。

### 2. 对象属性读写（含扩展属性）

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 属性读写 | `GetObjectAttr`、`SetObjectAttr`（含小写变体） | `SSProcess.GetObjectAttr id,"[采集人员]"` | 按对象 ID 读改业务字段 |
| 新建对象属性 | `SetNewObjValue` | `SSProcess.SetNewObjValue "[使用权人]","张三"` | 构面后批量赋值 |
| 属性复制 | `CopyObjectAttr`、`ChangeCodeCopy` | `SSProcess.CopyObjectAttr src, dst` | 复制编码/属性到新要素 |
| 二进制属性 | `GetObjectBinaryAttr`、`SetObjectBinaryAttr` | `SSProcess.SetObjectBinaryAttr id, field, bytes` | 存图片/二进制附件 |

### 3. 对象创建与删除

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 创建对象 | `CreateNewObj`、`CreateNewObjByCode`、`CreateNewObjByClass` | `SSProcess.CreateNewObjByCode "3103013"` | 画新地物 |
| 加点 | `AddNewObjPoint` | `SSProcess.AddNewObjPoint x,y,z` | 绘制多边形/线 |
| 入列保存 | `AddNewObjToSaveObjList`、`AddNewObjToSelObjList` | `SSProcess.AddNewObjToSaveObjList` | 新建要素入库 |
| 删除 | `DeleteObject`、`RepairUpdateObject` | `SSProcess.DeleteObject id` | 删除/修复对象 |

### 4. 几何编辑

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 节点编辑 | `SetSelGeoPoint`、`SetObjectPoint`、`DelSelGeoPoint`、`DeleteSelGeoPoint`、`FilterSelectionObjVertex`、`RemoveSelectionObjPoint` | `SSProcess.SetSelGeoPoint i, j, x, y, z, ptype` | 节点增删/调整（棚房节点取舍、等高线修改） |
| 对象变换 | `SelectionObjPartZ`、`SelectionObjOrderby`、`SelectionObjInnerInsertPoint`、`LockSelGeoPoint` | `SSProcess.LockSelGeoPoint` | 局部 Z 值、排序、插入点、锁点 |

### 5. 空间查询与几何计算

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 拓扑查询 | `SearchInnerObjIDs`、`SearchOuterObjIDs`、`SearchNearObjIDs`、`SearchRelatePolygonIDs`、`SearchInPolyObjIDs` | `SSProcess.SearchOuterObjIDs id, 0, outerIDs, count` | 宗地相交/包含冲突检测（入库类核心） |
| 几何判断 | `IsPtInPoly`、`IsPolygonInPolygon`、`IsPolylineInPolygon`、`IsClockwise` | `SSProcess.IsPtInPoly px, py, objID` | 点在面内、顺逆时针 |
| 距离计算 | `GetNearDist`、`LineParallelDist`、`GetDistDir`、`Cross_P`、`Perpend_P` | `SSProcess.GetNearDist x1,y1,x2,y2` | 线面距离、平行距 |

### 6. 坐标转换

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 国家2000 | `xy2000ToLongiLati`、`LongiLatiToxyCGCS2000` | `SSProcess.xy2000ToLongiLati x, y, L, B` | 2000 平面↔经纬度 |
| 北京54 | `xy54ToLongiLati`、`LongiLatiToxy54` | `SSProcess.xy54ToLongiLati x,y,L,B` | 54 平面↔经纬度 |
| 七参数/80 | `TransCoord_7pEx`、`LongiLatiToxyz80` | `SSProcess.TransCoord_7pEx x,y,z,param` | 七参数转换（坐标转换类脚本） |

### 7. 拓扑处理

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 拓扑工具 | `TopProcess`、`ObjectDeal`、`RebuildTopRelation` | `SSProcess.AddFunctionParameter "CreateTopArc=0": SSProcess.TopProcess topname` | 线转面、拓扑重建（拓扑构面类） |
| 构面合并 | `MergePolygon`、`MergeObjByCondition`、`SplitPolygon`、`MergeIslandAreaObj` | `SSProcess.MergePolygon objIDs, count` | 图斑合并/分割（变更处理） |
| 线处理 | `LineCrack`、`DangleCleanLineToLine` | `SSProcess.LineCrack lineID` | 线打断、悬挂清理 |

### 8. 图层控制与视图

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 图层状态 | `SetLayerStatus`、`GetLayerStatus`、`DeleteLayer`、`GetLayerCount`、`GetLayerName` | `SSProcess.SetLayerStatus layerName, 0/1` | 图层显隐（图层控制类） |
| 视图刷新 | `UpdateCurMap`、`RefreshView`、`SetMapScale`、`GetMapScale` | `SSProcess.SetMapScale 500` | 刷新/缩放（数据转换、出图） |
| 光标 | `SetCursorStatus`、`GetCursorStatus` | `SSProcess.SetCursorStatus 3` | 等待/十字光标 |

### 9. 图框与打印

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 图框创建 | `CreateMapFrame`、`CreateOneMapFrame`、`CreateMapFrameByRegion`、`SetCurMapFrame` | `SSProcess.CreateMapFrameByRegion regionID, scale` | 按区域生成图框（分幅出图） |
| 打印 | `PrintMapByCoord`、`FreeMapFrame` | `SSProcess.PrintMapByCoord x1,y1,x2,y2,scale` | 图廓打印（出图成果类） |

### 10. 数据库操作（Access/EDB 内置库）

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 打开/关闭 | `OpenAccessMdb`、`CloseAccessMdb`、`OpenAccessRecordset`、`CloseAccessRecordset` | `SSProcess.OpenAccessMdb edbname` | 工程库访问（上传宗地图读取地籍号） |
| 查询遍历 | `GetAccessRecordCount`、`AccessMoveFirst`、`AccessMoveNext`、`AccessIsEOF`、`GetAccessRecord` | `sql="select Memo From GeoAreaTB Where ...": GetGLTableValue fileName,sql,memo` | 读业务表（上传/下载/报表类） |
| 写操作 | `ExecuteAccessSql`、`AddAccessRecord`、`ModifyAccessRecord`、`DelAccessRecord` | `SSProcess.ModifyAccessRecord edbname, sql, "[字段]","新值"` | 台账更新、状态回写 |
| 外部库 | `ExecuteSql`、`IsExistentTable`、`GetAccessTableNames`、`GetAccessFieldInfo` | `SSProcess.ExecuteSql dbName, sql` | 直接操作外部 MDB/ZDB（数据转换类） |

### 11. 数据导入导出（跨格式核心）

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 转换参数 | `SetDataXParameter`(237145)、`ClearDataXParameter` | `SSProcess.SetDataXParameter "DataType","1": SSProcess.SetDataXParameter "ImportPathName",DWGfileName` | 配置 DWG/SHP/MIF/PDB 转换 |
| 执行导入 | `ImportData`、`ImportDataFromStream`、`GetImportFileName` | `SSProcess.ImportDataFromStream zdtgraphicinfo` | 文件/数据流导入（ZDB 标准转换） |
| 执行导出 | `ExportData`、`ExportDataToStream`、`ExportDataToStream4House` | `SSProcess.ExportData` | DWG/PDB/MDB 输出 |
| 数据库文件 | `OpenDatabase`、`CreateDatabase`、`CloseDatabase` | `SSProcess.CreateDatabase "模板.MDT", edbFileName` | EDB 创建/打开（批量调入） |
| 选择对话框 | `SelectFileName`、`SelectPathName` | `fileName=SSProcess.SelectFileName(1,"",0,"TXT Files(*.txt)|*.txt||")` | 用户选文件/目录 |

### 12. 文件操作与外部调用（扩展性关键）

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 外部程序 | `WinExec`(38) | `SSProcess.WinExec cmdLine, 0` | 调 ConvertToR14.exe 等外部转换器 |
| SDL 内置函数 | `ExecuteSDLFunction`(583) | `SSProcess.ExecuteSDLFunction "$SDL.SSProject.Display.RedrawExtend", 0` | 调用 EPS 原生功能（重绘/选择清空等） |
| 工具箱命令 | `ExecuteToolboxCommand`(24) | `SSProcess.ExecuteToolboxCommand "不动产","房产检查"` | 复用内置工具箱（检查、入库命令） |
| 回调 | `MapCallBackFunction`(357) | `SSProcess.MapCallBackFunction "SDLCommand","SSWorkSpace,SSWorkSpace",0` | 触发内置命令回调 |
| 系统路径 | `GetProjectFileName`、`GetSysPathName`、`GetScriptPath`、`GetTemplateFileName` | `SSProcess.GetSysPathName(0)` | 定位系统/模板/脚本目录 |
| 文件操作 | `MapMethod`、`Sleep` | `SSProcess.MapMethod "enumprinters", parameters` | 枚举打印机等系统调用 |

### 13. UI 交互

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 输入参数对话框 | `AddInputParameter`、`ShowInputParameterDlg`、`GetInputParameter`、`ClearInputParameter` | `SSProcess.AddInputParameter "成果图类型","不动产宗地图",0,"不动产宗地图,勘界图,违法图,其他宗地",""` | 上传类型选择、参数录入 |
| 脚本对话框 | `ShowScriptDlg`、`ShowScriptUserDefDlg`、`CloseScriptDlg` | `SSProcess.ShowScriptDlg mode, title` | 取号前提示、自定义对话框 |
| 网格对话框 | `CreateGridCtrl`、`SetGridCellInfo`、`ShowGridEditDlg`、`FillGridEditDlg` | `SSProcess.ShowGridEditDlg` | 列表选择（批量处理清单） |

### 14. 进度控制

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 进度条 | `EpsProgressCreate`(120)、`EpsProgressSetStep`(114)、`EpsProgressStepIt`(113)、`EpsProgressUpdateMsg`(113)、`EpsProgressDelete`(121) | `SSProcess.EpsProgressCreate 100,"导入": ... SSProcess.EpsProgressStepIt` | 长任务进度反馈（批量转换/入库） |

### 15. 检查记录（质检闭环）

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 检查记录 | `AddCheckRecord`、`RemoveCheckRecord`、`GetCheckRecordCount`、`GetCheckRecordValue`、`SaveCheckRecord`、`LoadCheckRecord`、`ShowCheckOutput` | `SSProcess.AddCheckRecord "属性项检查","必填信息检查","自定义脚本类->脚本编程检查","地物ID:...属性[业务编号]没填",x,y,z,ptype,id,""` | 检查类脚本全量使用，接入统一检查面板 |

### 16. 服务器通信与 ERP 集成（网络专项）

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 鉴权 | `SSERPTool.GetTokenAndInvalidTime`(961)、`SSERPTool.IsLogin`(289)、`SSERPTool.FormLogin`(6)、`SSERPTool.Login`(1)、`SSERPTool.Logout`(1) | `SSERPTool.GetTokenAndInvalidTime Token, InvalidTime` | 所有服务器请求前的 Token 获取 |
| 用户/工作信息 | `SSERPTool.GetUserInfo`(533)、`SSERPTool.GetCurWorkInfo`(124)、`SSERPTool.GetNewWorkInfo`(4)、`SSERPTool.ClearWorkInfo`(9) | `SSERPTool.GetUserInfo UserName, UserID, DeptName` | 取号/上传/接单的身份与业务上下文 |
| 通用 HTTP | `Microsoft.XMLHTTP`（COM，非 SSProcess 但全库标配） | `xmlhttp.Open "POST", URL, false: xmlhttp.Send "_namespace=erp.pro.unithelper.unitaccept&access_token=" & Token & "&iid=" & IID` | ERP 接口调用（取号/提交/撤单/查询） |
| SDE 同步 | `SSArcSDE.*`、`SSDbSynTools.*`（手册外、库内实际对象） | `SSArcSDE.ConnectToTablespace("SDBDC")`、`SSDbSynTools.UploadLocalDBToRemoteDB` | 远程库下载/入库（网络报告已详析） |
| 文件上传 | `SSFileUploadControl.*` | `SSFileUploadControl.SSUploadFileCtrl` | 分块上传 EDB 成果 |

### 17. 配置读写与参数管理

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 工程配置 | `ReadEpsDBIni`、`WriteEpsDBIni` | `IID=SSProcess.ReadEpsDBIni("ERPManager","ERP_IID","")` | 接单状态、作业信息持久化（贯穿所有业务脚本） |
| 全局配置 | `ReadEpsIni`、`WriteEpsIni`、`ReadEpsGlobalIni`、`ReadEpsTemplateIni`、`ReadEpsXMLIni` | `SSProcess.WriteEpsIni "section","key","value"` | 系统级/模板级配置 |
| 脚本参数 | `SSParameter.GetParameterSTR`(459)、`SetParameterSTR`(310)、`GetParameterINT`(155)、`SetParameterINT`(104) | `SSParameter.SetParameterSTR "ERPManager","AcceptWorkList",str` | 跨脚本传递业务数据（接单结果、要素 ID 列表） |

### 18. 加解密与注记/图形绘制

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 加解密 | `EncryptData`、`DecryptData` | `SSProcess.EncryptData str, key` | 成果加密（加密解密类，圆周率加密） |
| 注记 | `GetSelNoteValue`、`SetSelNoteValue`、`GetSelNoteCount`、`FindNoteClass` | `SSProcess.SetSelNoteValue i,"内容","新值"` | 注记批量读写（房屋注记转换） |
| 绘制 | `DrawLine`、`DrawText`、`PasteBackgroundImage`、`Arc3pToCenter` | `SSProcess.DrawLine x1,y1,x2,y2` | 辅助图形绘制 |

### 19. SSFunc 工具函数

| API 族 | 代表方法 | 真实代码示例 | 支撑业务场景 |
|---|---|---|---|
| 字符串/数组 | `SSFunc.ScanString`（全库使用最广）、`SSFunc.SortArrayByValue`、`SSFunc.atof` | `SSFunc.ScanString str,",",arr,count` | 解析逗号分隔串（坐标串/ID 串） |
| 图像 | `SSFunc.DrawToImage`、`SSFunc.OutputGraphToBmp` | `SSFunc.OutputGraphToBmp path, objIDs` | 出图转位图（宗地图 JPG 下载） |
| 其他 | `SSFunc.GetObjectRect`、`SSFunc.GetBinaryBitValue`、`SSFunc.ExcelSelectFile` | `SSFunc.GetObjectRect id, x1,y1,x2,y2` | 矩形范围、位运算、Excel 选择 |

---

## 二、EPS 平台能力边界

### 2.1 能做什么（已证实能力清单）

**A. 本地数据处理**
- 要素选择/遍历/批量改属性（选择集 API，全库调用超 5 万次）
- 几何编辑（节点增删、合并/炸开/裁剪、拓扑构面/打断/合并）
- 空间查询（内外/邻近/包含对象检索、点在面内判断）
- 面积计算与分摊、坐标转换（54/80/2000/经纬度/七参数）
- 注记批量处理、图形绘制、图框生成与打印
- 检查记录闭环（AddCheckRecord → 检查面板定位修改）

**B. 空间分析**
- 拓扑关系查询与重建（入库冲突检测：相交/包含推历史库）
- 图斑分割合并、构面（行政区/房产面积块拓扑构面）
- 距离/角度/垂直/平行计算

**C. 外部系统集成**
- ERP/OA 接口调用（Token 鉴权 + `erp.*` 命名空间 + /CommonOperate 网关）
- ArcGIS Server REST（JK 系列方法经网关转发）
- SDE 远程表空间直连（下载/入库/双库回源校验）
- 文件服务器上传（SSFileUploadControl 分块上传 EDB）
- 外部数据库（ADODB 直连 MDB/ZDB/Oracle 查询）
- 外部程序调用（WinExec）、SDK 内置功能（ExecuteSDLFunction）、工具箱命令（ExecuteToolboxCommand）
- 桌面生态（Excel/Word COM、FileSystemObject、XMLHTTP）

**D. 成果输出**
- DWG/SHP/MDB/PDB/ZDB/CASS 多格式导入导出
- 勘界图/宗地图/违法图/红线图/分层分户图出版级输出（图廓/条形码/审图要素）
- 联合测绘成果报告（Word/PDF）、台账/统计表（Excel）
- BMP/JPG 图像输出（宗地图下载、成果图快照）

### 2.2 不能做什么（脚本层面无法突破的限制）

1. **无独立线程/异步能力**：VBScript 无多线程；`XMLHTTP.Open "POST", URL, false` 全部同步阻塞，大批量网络请求时界面卡死（库内脚本普遍如此，无异步写法）。
2. **无调试器/IDE**：VBS 无断点调试、无类型检查，错误靠 `MsgBox` 和日志定位，脚本规模大时维护成本高（库内 1000+ 行脚本常见）。
3. **不能脱离 EPS 主程序运行**：SSProcess/SSERPTool/SSArcSDE 等对象仅存在于 EPS 进程内，脚本无法独立于 EPS 执行，不能做无人值守后台任务（需配合 Windows 计划任务启动 EPS）。
4. **无法直接访问 EPS 内部渲染/底层几何内核**：只能通过 SSProcess 暴露的 API 操作，未开放的底层能力（如复杂三维建模、空间分析高级算法）无法在脚本层触达。
5. **GUI 能力有限**：只能使用 EPS 提供的对话框模板（ShowScriptDlg/ShowInputParameterDlg/GridCtrl），不能创建任意 Windows 窗体控件。
6. **安全/凭据硬编码**：OA 硬编码凭证（infuser/infpwd）、`bjswkjgfyxgs/cnmdaohaob1` 等凭据明文存放，脚本层无加密保护机制（只有自定义圆周率加密，非标准强加密）。
7. **性能瓶颈**：解释执行 + 逐对象遍历，批量处理 10 万级要素时慢；库内用 5000 维数组（`dim getstrarr(5000)`）承载数据，说明作者已知容量限制并预留。
8. **无版本管理/依赖管理**：脚本间 `#include` 依赖路径脆弱（`.\接口调用\Function_JK.vbs`），目录移动即失效；库内大量"-副本.vbs"说明无版本控制流程。

### 2.3 扩展途径（除 VBS 外的扩展机制，含证据）

| 扩展机制 | 证据 | 说明 |
|---|---|---|
| **菜单/脚本管理器配置** | 全库脚本均以 `Sub OnClick()` 为入口挂菜单；`系统消息\BdcProjectMan_GetScriptMenuItem.vbs`、`BdcProjectMan_GetScriptMenuCmds.vbs` 动态注入菜单命令 | 业务功能通过脚本管理器注册到右键/菜单/工具栏，无需改主程序 |
| **事件钩子（系统消息）** | `AfterOpenEdb.vbs`、`BeforeImportProjectData.vbs`、`AfterUpdateLocalREProjectToSDE.vbs`、`BeforeCheckItemFinishInfo.vbs` 等 66 个 | EPS 在生命周期节点回调脚本，业务规则自动挂接 |
| **SDL 内置函数调用** | `SSProcess.ExecuteSDLFunction "$SDL.SSProject.Display.RedrawExtend", 0`（全库 583 次） | 脚本可直接调用 EPS 原生 SDL 命令，等于"脚本化主程序功能" |
| **工具箱命令复用** | `SSProcess.ExecuteToolboxCommand "不动产","房产检查"`（24 次） | 脚本可触发内置工具箱流程并与检查记录联动 |
| **外部程序调用** | `SSProcess.WinExec cmdLine, 0`（38 次，如调用 ConvertDwg\ConvertToR14.exe） | 可拉起任意外部 EXE（转换器、打印工具） |
| **COM 对象生态** | `Microsoft.XMLHTTP`、`ADODB.Connection`、`Scripting.FileSystemObject`、`Excel.Application`、`Word.Application`、`MSScriptControl`（内嵌 JScript 实现 encodeURI） | VBS 原生访问 Windows COM，网络/数据库/办公集成全开 |
| **公共函数库（#include）** | `#include ".\接口调用\Function_JK.vbs"`、`#include ".\接口调用\erpnetaddress.vbs"`、`WordVbsFunc.vbs` 等 | 模块化复用，形成私有 SDK |
| **脚本加密保护** | 主脚本 `@1234567890-` 头加密、圆周率加密脚本、加密狗校验（getdogrw） | EPS 支持脚本加密 + 加密狗授权，保护商业成果 |

---

## 三、"EPS 能做什么、怎么做"实操指南

### 3.1 编写路径总则（五步法）

任何新功能 = **① 明确入口与上下文 → ② 选要素/取参数 → ③ 业务处理 → ④ 服务器交互（如需）→ ⑤ 反馈与持久化**。对应可复用的现成模式：

| 步骤 | 复用哪个模式 | 来自哪份报告 |
|---|---|---|
| 整体骨架 | 五段式架构（入口→鉴权→遍历→交互→反馈） | 功能模式归纳报告 §三 |
| 鉴权模板 | Token 获取（GetTokenAndInvalidTime）+ IsLogin + GetUserInfo | 网络报告 §认证时序 |
| 接口调用 | XMLHTTP + `_namespace=erp.*` + access_token + methodname | 网络报告 §通信模式模板 |
| 上传模板 | uploadZDCGfile / SSFileUploadControl 分块上传 | 网络报告 §上传调用链 |
| 要素处理 | SetSelectCondition→SelectFilter→GetSelGeoCount→GetSelGeoValue/SetSelGeoValue | 本报告 §一.1/§一.2 |
| 工程状态 | ReadEpsDBIni/WriteEpsDBIni（ERPManager 段） | 本报告 §一.17 |

### 3.2 示例：新增"批量修改宗地属性并上传OA"

**需求**：把当前工程中选中宗地的"使用权人"统一改为某值，校验必填后上传成果到 OA 系统。

**步骤 1：确定入口与参数**
```vbs
Sub OnClick()
    ' ① 参数对话框：让用户输入新使用权人
    SSProcess.ClearInputParameter
    SSProcess.AddInputParameter "使用权人", "string", "", "", "请输入新使用权人"
    SSProcess.AddInputParameter "成果图类型", "不动产宗地图", 0, "不动产宗地图,勘界图,违法图,其他宗地", ""
    If SSProcess.ShowInputParameterDlg("批量修改宗地属性并上传") = 0 Then Exit Sub
    newQlr = SSProcess.GetInputParameter("使用权人")
    cgtlx  = SSProcess.GetInputParameter("成果图类型")
    Main
End Sub
```

**步骤 2：鉴权与上下文（复用网络报告认证模板）**
```vbs
Sub Main()
    ' ② 登录/接单校验（照抄 上传宗地图.vbs 写法）
    SSERPTool.GetTokenAndInvalidTime Token, InvalidTime
    SSERPTool.GetCurWorkInfo WorkIID, WorkName, WorkWIID
    SSERPTool.GetUserInfo UserName, UserID, DeptName
    If Token = "" Then MsgBox "没有登录" : Exit Sub
    If WorkIID = "" Then MsgBox "没有接单" : Exit Sub
    ' ③ 检查作业信息（ReadEpsDBIni 逐项校验测量员/绘图员/检查员）
```

**步骤 3：批量修改宗地属性（复用选择集三件套）**
```vbs
    ' ④ 选择使用权宗地（编码 6801053）
    SSProcess.ClearSelection : SSProcess.ClearSelectCondition
    SSProcess.SetSelectCondition "SSObj_Type", "==", "AREA"
    SSProcess.SetSelectCondition "SSObj_Code", "==", "6801053"
    SSProcess.SelectFilter
    cnt = SSProcess.GetSelGeoCount
    If cnt = 0 Then MsgBox "未选中宗地" : Exit Sub
    SSProcess.PushUndoMark   ' 可撤销
    For i = 0 To cnt - 1
        SSProcess.SetSelGeoValue i, "[使用权人]", newQlr
        SSProcess.SetSelGeoValue i, "[修改日期]", Date
    Next
    SSProcess.UpdateCurMap
```

**步骤 4：上传 OA（复用上传调用链：复制 EDB → 上传 → 读取业务号）**
```vbs
    ' ⑤ 复制当前工程到 upload 目录并上传（照抄 上传宗地图.vbs）
    fileName = SSProcess.GetProjectFileName
    uploadpath = Left(fileName, InStrRev(fileName, "\")) & "upload\"
    CreateFolder uploadpath
    FileCopy fileName, uploadpath & Mid(fileName, InStrRev(fileName, "\") + 1)
    uploadZDCGfile WorkIID, uploadpath & Mid(fileName, InStrRev(fileName, "\") + 1), Token, "成果数据", uploadpath
    DelFolder uploadpath
    ' ⑥ 提交业务状态（照抄 新建业务.vbs 的 CommonOperate 调用）
    geterpaddress URL
    Set xmlhttp = CreateObject("Microsoft.XMLHTTP")
    xmlhttp.Open "POST", URL & "/CommonOperate", False
    xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"
    parameter = "_namespace=erp.pro.workflow.workflowsubmit" & "&access_token=" & Token _
              & "&iid=" & WorkIID & "&wiid=" & WorkWIID & "&type=" & cgtlx
    xmlhttp.Send parameter
    If xmlhttp.readyState = 4 And xmlhttp.status = 200 Then
        MsgBox "上传成功"
    End If
End Sub

' ⑦ 公共函数复用（照抄库内公共函数库）
Function geterpaddress(ByRef u)  '#include 或复制 erpnetaddress.vbs
    u = "http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate"
End Function
#include ".\接口调用\Function_JK.vbs"   ' 复用 JK 系列与 JSON 解析
```

**步骤 5：落地要点**
- 进度反馈：`EpsProgressCreate 100,"批量修改"` / `EpsProgressStepIt`（长任务必加）
- 结果持久化：`SSParameter.SetParameterSTR "ERPManager","LastUploadResult",str` 供后续脚本读取
- 挂菜单：放入对应模块的 `Script\业务流程\` 目录，EPS 脚本管理器自动识别 `OnClick` 入口
- 若需自动触发：命名放入 `Script\系统消息\` 并实现 `Before*/After*` 钩子

---

## 四、VBS 脚本背后的意义

### 4.1 为什么 EPS 选择 VBScript

1. **Windows/COM 原生集成**：VBScript 可直接调用 `XMLHTTP/ADODB/FileSystemObject/Excel/Word/MSScriptControl` 等全部 COM 组件，天然适配测绘生产链（数据库+办公+网络）。
2. **免编译、即改即用**：`.vbs` 文本文件改完即可重跑，适合业务人员快速调整业务规则（如检查规则、出图模板），无需重新编译主程序。
3. **低门槛**：VBS 语法简单，测绘业务骨干（非专业程序员）也能写业务脚本——库内 1794 个唯一脚本、`玮哥专用脚本` 等命名即证明"业务人员主导开发"。
4. **进程内沙箱**：脚本在 EPS 进程内运行，可安全访问工程数据模型，同时通过 SSProcess 封装层隔离底层实现，降低误操作风险。
5. **历史生态**：2000-2010 年代 GIS 二次开发主流是 VBS/VBA（ArcGIS、CASS 等皆然），EPS 沿用降低客户迁移成本。

### 4.2 脚本积累代表什么企业资产

1. **业务规则资产（最核心）**：1794 个唯一脚本 = 佛山/顺德不动产测绘**全部业务规则的可执行版本**——取号规则、检查规则（必填/一致性/面积进位）、出图规范（图廓/比例尺/条形码）、入库冲突策略（相交/包含推历史库），是"规则即代码"的典型形态。
2. **系统集成资产**：脚本中沉淀了与 ArcGIS Server、ERP/OA、SDE、权籍库、文件服务器的**全部对接细节**（网关地址、Token 时序、接口参数、双库回源校验逻辑），这些是多年实施调试换来的隐性知识。
3. **生产流程资产**：从采集→处理→质检→输出→集成→工具的六层完整覆盖，说明脚本库本身就是一套可复制、可裁剪的**测绘生产流水线模板**。
4. **数据标准资产**：CASS9/PDB/ZDB/地形标准等转换脚本固化了本单位的数据标准（编码对照、点型线型规则、图层组织），是数据互通与质量统一的基石。
5. **人才与经验资产**：脚本是"老员工经验的外化"——抽查脚本中大量注释掉的备选逻辑与版本演化（报告 1007/1008/1017/1030 多版本），记录了一线生产踩坑史。

### 4.3 对测绘生产单位的战略价值

1. **降低对软件厂商的依赖**：业务规则自己掌控，政策/规范变化（如不动产单元号编码规则调整）可当天改脚本响应，无需等厂商排期。
2. **可复制交付能力**：脚本库=方法论+工具集，承接新区域/新项目时直接"复制模块+改规则"，大幅缩短项目落地周期（库内 15 个一级模块即按项目复制演化的实证）。
3. **数据资产增值**：脚本与 SDE/权籍库深度集成，使本单位不仅是"画图"而是"不动产数据生产与治理"的核心环节，提升在政企链条中的话语权。
4. **质量可控**：17.8% 检查类脚本把人工质检规则固化，交付质量不依赖个人水平；检查记录闭环（AddCheckRecord→定位修改）形成可追溯的质检档案。
5. **战略风险提示**：脚本分散在个人目录、无版本管理、依赖"玮哥"等关键个人（加密脚本+加密狗授权），存在**人员流失风险**与**技术债风险**——建议将脚本库纳入版本管理、建立公共函数标准库、关键脚本去个人化。

---

## 五、结论

- **EPS 的扩展性 = "VBScript + SSProcess 对象模型 + 事件钩子 + SDL/工具箱/WinExec 三道外扩 + COM 生态"**，其中 SSProcess 提供约 345 个 API，覆盖从要素遍历到服务器通信的完整能力面；事件钩子与 SDL 调用使脚本可"长在"系统流程内部而非孤立的菜单功能。
- **EPS 能做什么**：一套完整的测绘生产管理系统（采集→处理→质检→输出→集成→工具六层全覆盖），且通过 ERP 网关、SDE 直连、文件上传与外部系统深度耦合。
- **怎么做**：按"五段式骨架 + 认证模板 + 通信模板 + 上传/入库模板"组合复用，新功能开发本质是"拼装已验证的代码模式"，本报告 §3.2 给出完整示例。
- **脚本的意义**：4783 个 VBS（1794 个唯一）不是"代码垃圾"，而是测绘生产单位十数年积累的**业务规则库、系统集成知识库、生产流程模板与数据标准资产**；在 AI 时代，这些脚本同时是可被大模型解析、重构、迁移的**高价值知识语料**，为后续智能化（自动生成新脚本、规则审计、跨系统迁移）提供了独一无二的数据基础。

---

*报告生成时间：2026-09-01；数据源：《EPS_VBS_API参考手册.md》（345 API/调用统计）、EPS-VBS知识库全库脚本、前两阶段报告；配套中间产物：temp/（无新增中间文件）。*
*（内容由AI生成，仅供参考）*
