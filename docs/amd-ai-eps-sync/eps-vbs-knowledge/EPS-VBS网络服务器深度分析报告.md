---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 95ce5665a2763fbde4f792b4da682b54_d520aa0da5fa11f199d2525400287e28
    ReservedCode1: nwYuwKMOc2VF3uIejl7BWwo0UOwvEOtPsP+ibIpDNzZqkGysmjOoZwGscABHlDInEEPdSWA6zTvdCBLVCFxH2YhRS+Yjv+9DIj95klX/z6tkoE4918LcktELJ129vpUsXy5hxddRCfN8luJP+bDxDFx2zdytf2sDAfKITZQe1zh7lEPDj0pgQeLbp6s=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 95ce5665a2763fbde4f792b4da682b54_d520aa0da5fa11f199d2525400287e28
    ReservedCode2: nwYuwKMOc2VF3uIejl7BWwo0UOwvEOtPsP+ibIpDNzZqkGysmjOoZwGscABHlDInEEPdSWA6zTvdCBLVCFxH2YhRS+Yjv+9DIj95klX/z6tkoE4918LcktELJ129vpUsXy5hxddRCfN8luJP+bDxDFx2zdytf2sDAfKITZQe1zh7lEPDj0pgQeLbp6s=
---

# EPS-VBS 网络服务器深度分析报告

> 分析对象：`C:\Users\Administrator\Desktop\EPS-VBS知识库` 全部 VBS 脚本（去重后 1794 个唯一文件）
> 分析重点：网络/服务器通信的真实代码证据、认证体系还原、典型调用链、标准写法模板
> 本报告在《EPS深度分析报告.md》《_深度分析报告.md》的统计基础上深化，不再重复数量统计
> 所有代码片段均来自明文脚本原文（含 `- 副本.vbs` 与"玮哥专用脚本"明文版），加密主文件未纳入代码级引用

---

## 一、执行摘要

EPS（清华山维）VBS 脚本的网络通信呈现**高度统一的"单入口代理"架构**：

1. **几乎所有 ERP 业务调用**（含 ArcGIS 空间操作）都通过**唯一网关** `http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate` 完成，由 `_namespace` 参数路由到具体服务，`access_token` 做认证；
2. **ArcGIS Server** 存在两种调用方式：**直连**（`http://221.4.165.144:6080/arcgis/rest/services/...`，无认证）与**经 ERP 代理**（JK 系列方法，带 Token）；
3. **认证体系三层并存**：ERP Token（`erp.auth.authhelper.gettoken`）、OA 硬编码凭证（`infuser=qinghuashanwei20170726&infpwd=123456`）、完全无认证（ArcGIS 直连、文件服务器、远程 asmx）；
4. **文件上传**统一使用 EPS 私有 COM 控件 `SSFileUploadControl.SSUploadFileCtrl` 分块上传到 `WebFiler`；
5. **远程数据下载**统一走 `SSArcSDE` 组件连接 SDE 空间库（`SDBDC` 等），另有多个远程 WebService（`.asmx`）提供图片/坐标等辅助服务。

---

## 二、网络通信全景统计（代码级扫描）

| 维度 | 数值 | 说明 |
|---|---|---|
| 涉及 token 关键词的脚本 | 1016 | token / access_token / gettoken 等 |
| 使用 SSERPTool 组件 | 571 | 认证与用户信息 |
| 调用 GetTokenAndInvalidTime | 249 | 每次请求前取 Token |
| 调用 GetUserInfo | 163 | 获取用户名/ID/部门 |
| 唯一 URL 数量 | 115 | 去重后 |
| POST 请求 | 489 次 | 主流的调用方式 |
| GET 请求 | 60 次 | 主要用于图片下载/人员查询 |
| `Content-Type: application/x-www-form-urlencoded` | 578 次 | 绝对主流 |
| `Content-Type: application/json` | 2 次 | 少量接口 |
| `Authorization: bearer` | 2 次 | 极少数直连接口 |

> 说明：以上为脚本正文中的字面量/调用统计，不包含被加密脚本内不可见的部分；真实调用量只会更高。

### 2.1 通信目标分类总览

| 通信目标 | 主机 | 认证方式 | 主要协议 | 典型用途 |
|---|---|---|---|---|
| ERP 系统（CommonOperate 网关） | getnumber.shunde.gov.cn | Token（access_token） | HTTP POST + form | 业务取号/提交/查询/待办/审批 |
| ArcGIS Server（直连） | 221.4.165.144:6080 | 无 | HTTP POST + form | 空间要素 CRUD、地图查询 |
| ArcGIS Server（经 ERP 代理 JK） | 经 getnumber 网关 | Token | HTTP POST + form | 同上，走代理 |
| OA 系统 | chqy.shunde.gov.cn | 硬编码凭证（URL 参数） | HTTP GET | 企业/人员信息查询 |
| 文件服务器（WebFiler） | getnumber.shunde.gov.cn/sg_erp_sdqtqh/WebFiler | Token（会话） | SOAP/HTTP 分块上传 | 测绘成果文件上传 |
| 远程 WebService | 47.94.1.65:8065 | 无（ASMX） | SOAP | 业务通用 asmx |
| 远程 WebService（第三方入口） | getnumber.../sg_zyservices/Service1.asmx | 硬编码 user/password | HTTP POST | 代理运行 ArcGIS 查询 |
| 远程 WebService（宗地图片） | 19.200.42.71 | 无 | HTTP GET（SOAP 风格 asmx） | 宗地 JPG 图片下载 |
| 南方权籍库 ArcGIS | 19.200.44.251:3280 | 无 | HTTP POST | 宗地存在性验证/坐标下载 |
| 远程 SDE 空间库 | 内网（SSArcSDE 配置） | 数据库账号 | SDE 协议 | 宗地/幢/户数据批量下载 |
| 远程数据库 | 内网（Oracle/SQL Server） | 硬编码账号（sdgis/sdgis78 等） | ADODB | 属性数据直连读取 |
| 联合测绘/其他 | 172.20.10.240、dtgx.fszrzy.foshan.gov.cn 等 | 待确认 | HTTP | 联合测绘业务接口 |

---

## 三、认证体系深度还原

### 3.1 三层认证并存结构

```
┌────────────────────────────────────────────────────────────────────┐
│                         认证体系全景                               │
├────────────────────────────────────────────────────────────────────┤
│ ① ERP Token 认证（主流）                                          │
│    SSERPTool.GetTokenAndInvalidTime → access_token                │
│    → 所有 CommonOperate 请求携带 &access_token=Token             │
│    → 另有 _timestamp 参数（时间戳）                                │
│                                                                    │
│ ② OA 硬编码凭证（人员查询）                                       │
│    interface_ryxx.jsp?infuser=qinghuashanwei20170726&infpwd=123456│
│                                                                    │
│ ③ 无认证（直连服务）                                              │
│    ArcGIS Server REST、WebFiler 上传、19.200.42.x asmx、           │
│    19.200.44.251:3280、SDE 空间库                                  │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 Token 获取（令牌获得.vbs，全文核心）

```vbs
Sub OnClick()
      SSParameter.GetParameterSTR "ERPManager", "UserIDAndCode", "", keyValue1
      'keyValue1="test,1"
      If keyValue1="" Then Exit Sub
      Dim strs(100),count,strs1(100),count1
      SSFunc.ScanString keyValue1,",",strs,count
      If count<>2 Then Exit Sub
      Set   xmlhttp   =   CreateObject( "Microsoft.XMLHTTP") 
      geterpaddress URL
      getEpsMark Mark
      xmlhttp.Open  "POST", URL, false 
      xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"
      parameter = "_namespace=erp.auth.authhelper.gettoken" & "&userid=" & strs(0) & "&code=" & strs(1) & "&clientid=" & Mark
      xmlhttp.Send  Parameter

      str=""
      If   xmlhttp.readyState=4     Then
            If xmlhttp.status=200     Then
                  str=xmlhttp.responseText
                  SSParameter.SetParameterSTR "ERPManager", "访问令牌", str
            End IF
      End iF
End Sub
```

要点：
- Token 的"钥匙"是 `UserIDAndCode`（用户 ID + 授权码，逗号分隔），存于 EPS 会话参数 `SSParameter`；
- `clientid=eps` 标识客户端类型；
- Token 响应被**原样写入** `SSParameter "访问令牌"`，后续由 `SSERPTool` 组件统一管理。

### 3.3 Token 传递

每次业务请求前，脚本都调用 `SSERPTool.GetTokenAndInvalidTime Token, InvalidTime`，然后拼入请求参数。典型片段（通用接口方法调用.vbs）：

```vbs
FUnction bb()
      geterpaddress URL
      SSERPTool.GetTokenAndInvalidTime Token,InvalidTime

      Set   xmlhttp   =   CreateObject( "Microsoft.XMLHTTP") 
      xmlhttp.Open  "POST", URL, false 
      xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"

      pstr="where=objectid=1&...&f=pjson"   'ArcGIS REST 查询串
      pstr=replace(pstr,"=","%3D")
      pstr=replace(pstr,"&","%26")
      parameter = "_namespace=erp.arc.arcgisserverhelper.interfaceentry&access_token=" & Token& "&methodname=JK1&parameter=" & pstr

      xmlhttp.Send  Parameter
      ...
End Function
```

要点：
- **Token 是表单参数而非 HTTP Header**（极少数直连接口才用 `Authorization: bearer`）；
- 每次调用都重新取 Token，即**无显式刷新机制**——依赖 `SSERPTool` 内部缓存与失效时间（`GetTokenAndInvalidTime` 同时返回 Token 与 InvalidTime）。

### 3.4 Token 相关辅助接口

| 接口 | 命名空间 | 用途 |
|---|---|---|
| gettoken | erp.auth.authhelper.gettoken | 获取 Token（userid+code+clientid） |
| userlogin | erp.neto.netofficehelper.userlogin | 用户登录（loginname+password+grant_type=password） |
| validepsregcode | erp.neto.netofficehelper.validepsregcode | 验证 EPS 加密狗（regcode） |
| getunitworktodolist | erp.neto.netofficehelper.getunitworktodolist | 获取待办/校验接单 |

用户登录（用户登录.vbs，与取 Token 同构）：

```vbs
parameter = "_namespace=erp.neto.netofficehelper.userlogin" & "&loginname=" & strs(0) & "&password=" & strs(1) & "&grant_type=password" & "&clientid=" & Mark
```

加密狗校验（违法宗地取号.vbs 的 getdogrw）：

```vbs
Function getdogrw(dogcode)
      getdogrw=0
      geterpaddress URL
      SSERPTool.GetTokenAndInvalidTime Token,InvalidTime
      SSERPTool.GetUserInfo UserName, UserID, DeptName
      dogcode=SSProcess.MapMethod ("getusbkeyid", parameters)
      Set xmlhttp = CreateObject( "Microsoft.XMLHTTP")
      xmlhttp.Open "POST", URL, false
      xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"
      parameter = "_namespace=erp.neto.netofficehelper.validepsregcode" & "&_timestamp=&access_token=" & Token & "&userid=" & UserID & "&regcode=" & dogcode
      xmlhttp.Send Parameter
      str=""
      If xmlhttp.readyState=4 Then
            If xmlhttp.status=200 Then
                  str=xmlhttp.responseText
                  If instr(str,chr(34) & "success" & chr(34) & ":false")>0 Then
                        getdogrw=0
                  Else
                        getdogrw=1
                  End If
            End IF
      End iF
      Set xmlhttp = nothing
End Function
```

要点：
- 业务合法性依赖**物理加密狗**：`SSProcess.MapMethod("getusbkeyid")` 读取 USB Key 序列号，服务器端验证单位授权；
- 响应格式为 JSON，按 `"success":false` 判断失败。

### 3.5 认证时序图（完整业务请求）

```
用户/脚本                       ERP 网关 (CommonOperate)         业务服务
   │                                   │                          │
   │ 1. gettoken                       │                          │
   │ (userid,code,clientid=eps) ─────► │ ──► authhelper.gettoken  │
   │ ◄────────────── Token ─────────── │ ◄── token                │
   │ 2. 保存到 SSParameter"访问令牌"    │                          │
   │                                   │                          │
   │ 3. GetTokenAndInvalidTime         │                          │
   │    (每次业务请求前)                │                          │
   │ 4. POST _namespace=业务服务        │                          │
   │    &access_token=Token            │                          │
   │    &methodname=JKxxx / 业务参数 ─► │ ──► 目标服务             │
   │ ◄────────── JSON 结果 ─────────── │ ◄── 结果                 │
   │ 5. 解析 responseText → MsgBox/绘图 │                          │
```

---

## 四、通信目标详细分析

### 4.1 ERP 系统（统一网关 CommonOperate）

**网关地址**（erpnetaddress.vbs 原文）：

```vbs
Function geterpaddress(byref URL)
      URL = "http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate"
End Function

Function getEpsMark(byref Mark)
      Mark = "eps"
End Function
```

所有 ERP 调用共用此地址，通过 `_namespace` 路由。已确认的真实命名空间：

| 命名空间 | 用途 | 代表脚本 |
|---|---|---|
| erp.auth.authhelper.gettoken | 获取 Token | 令牌获得.vbs |
| erp.neto.netofficehelper.userlogin | 用户登录 | 用户登录.vbs |
| erp.neto.netofficehelper.validepsregcode | 加密狗校验 | 违法宗地取号.vbs |
| erp.neto.netofficehelper.getunitworktodolist | 待办列表/接单校验 | 上传宗地图.vbs |
| erp.neto.workflowhelper.workflowsubmit | 工作流提交 | 上传宗地图.vbs |
| erp.pro.unithelper.updateunitinfo | 更新业务单元信息 | 上传宗地图.vbs |
| erp.pro.unithelper.unitaccept | 接单 | 上传下载数据.vbs |
| erp.gis.arcgisserverhelper.interfaceentry | ArcGIS 代理（JK 系列） | 违法宗地取号.vbs / 通用接口方法调用.vbs |
| erp.arc.arcgisserverhelper.interfaceentry | ArcGIS 代理（JK 系列） | 通用接口方法调用.vbs |

**业务单元信息更新**（上传宗地图.vbs）：

```vbs
unitinfostr="{" & chr(34) & "是否数据已下载" & chr(34) & ":" & chr(34) & "1" & chr(34) 
      unitinfostr=unitinfostr & "," & chr(34) & "测量员" & chr(34) & ":" & chr(34) & gcinfo(0) & chr(34)
      ...
      parameter = "_namespace=erp.pro.unithelper.updateunitinfo" & "&_timestamp=&access_token=" & Token & "&iid=" & WorkIID & "&unitinfo=" & unitinfostr
```

**工作流提交**：

```vbs
parameter = "_namespace=erp.neto.workflowhelper.workflowsubmit" & "&_timestamp=&access_token=" & Token & "&iid=" & WorkIID & "&wiid=" & WorkWIID & "&userid=" & userid & "&users=" & userjson
```

**待办/接单校验**（reGetWork）：

```vbs
parameter = "_namespace=erp.neto.netofficehelper.getunitworktodolist" & "&_timestamp=&access_token=" & Token & "&userid=" & UserID& "&iid=" & WorkIID
```

**业务含义**：ERP 网关是"业务流程中枢"，承载取号、接单、提交、待办、人员、加密狗验证等全部业务语义；VBS 是 BPM 客户端。

### 4.2 ArcGIS Server

#### 4.2.1 直连模式（无认证）

通用接口方法调用.vbs 的 `aa()`：

```vbs
Function aa()
      URL="http://221.4.165.144:6080/arcgis/rest/services/QH/MapServer/1/query"
      Poststr="where=objectid=1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPolygon&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=objectid&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=pjson"
      set xmlhttp   =   CreateObject( "Microsoft.XMLHTTP") 
      xmlhttp.Open   "POST ",URL, false 
      xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"
      xmlhttp.Send Poststr
      STR=xmlhttp.responseText  
      Set xmlhttp=nothing
End Function
```

#### 4.2.2 经 ERP 代理模式（JK 系列，带 Token）

违法宗地取号.vbs 的 `getHTTPattr`（查询核心）：

```vbs
Function getHTTPattr(byval zbstr,byval BreturnCountOnly,byval outFields,byval jkname)
      geterpaddress URLnew
      SSERPTool.GetTokenAndInvalidTime Token,InvalidTime
      getHTTPattr=""
      URLnew= encodeURI(URLnew)
      Set xmlhttp = CreateObject( "Microsoft.XMLHTTP")
      xmlhttp.Open "POST", URLnew, false
      xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"

      Poststr="where=&objectIds=&time=&geometry=" & zbstr & "&geometryType=esriGeometryPolygon&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=" & outFields & "&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=" & BreturnCountOnly & "&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=pjson"
      Poststr=encodestr(Poststr)
      parameter1 = "_namespace=erp.gis.arcgisserverhelper.interfaceentry&access_token=" & Token& "&methodname=" & jkname & "&parameter=" & Poststr
      xmlhttp.Send parameter1
      If xmlhttp.readyState=4 Then
            If xmlhttp.status=200 Then
                  getHTTPattr=xmlhttp.responsetext
            End IF
      End iF
      Set xmlhttp=nothing
End Function
```

**参数编码函数**（encodestr + encodeURI，全库通用）：

```vbs
Function encodestr(str)
      encodestr=""
      Dim strs(9000),scount
      SSFunc.ScanString str,chr(34),strs,scount
      For i=0 To scount-1
            If i=0 Then encodestr=encodeURI(strs(i))
            If i>0 Then encodestr=encodestr & "\" & chr(34) & encodeURI(strs(i))
      Next
      encodestr=replace(encodestr,"=","%3D")
      encodestr=replace(encodestr,"&","%26")
End Function

Function encodeURI(str)
      Set sc = CreateObject("MSScriptControl.ScriptControl")
      sc.Language = "JScript"
      line = "var a = encodeURI("& CHR(34) & str & CHR(34) & ");" 
      sc.AddCode line
      encodeURI=sc.Eval("a")
      Set sc=nothing
End Function
```

> 注：VBScript 无原生 `encodeURI`，脚本通过 **MSScriptControl 内嵌 JScript** 实现 URL 编码——这是全库最精巧的兼容技巧之一。

#### 4.2.3 已确认的 JK 方法（违法宗地取号.vbs 实证）

| JK 方法 | 操作 | 请求体语义 | 对应 ArcGIS 直连语义 |
|---|---|---|---|
| JK1 | 通用查询（示例） | where/geometry/outFields → f=pjson | MapServer query |
| JK112 | 图廓查询（按几何相交） | geometry={rings:[[...]]} + returnCountOnly | FeatureServer query |
| JK113 | 宗地查询（按几何相交） | geometry + outFields=DJH,BBH,ZL,QHZT | FeatureServer query |
| JK133 | 宗地/图幅状态查询 | geometry 相交或 where=TFH='xxx'，返回 QHSJ 取号时间 | FeatureServer query |
| JK114 | 写新宗地到取号库 | features=[{geometry:{rings},attributes:{YSDM,FEATUREGUID,DJH,BBH,QHZT,QHDW,QHRQ,QHR}}]&gdbVersion=SDE.DEFAULT | FeatureServer addFeatures |
| JK115 | 写操作日志 | features=[{attributes:{取号时间,单位名,用户名,建议操作,实际操作,取号狗号,宗地号,版本号}}] | FeatureServer addFeatures |
| JK134 | 写取号队列 | features=[{attributes:{TFH,YJH,QHSJ,CZR}}] | FeatureServer addFeatures |
| JK135 | 删除取号队列 | objectIds=&where=TFH='xxx'&gdbVersion=&rollbackOnFailure=true | FeatureServer deleteFeatures |

**JK134 写入取号队列**（writeQHQueuelog）：

```vbs
attrstr="[{" & chr(34) & "attributes" & chr(34) & ": {"
      attrstr=attrstr & chr(34) & "TFH" & chr(34) & ":" & chr(34) & TFH & chr(34) & ","
      attrstr=attrstr & chr(34) & "YJH" & chr(34) & ":" & chr(34) & YJH & chr(34) & ","
      attrstr=attrstr & chr(34) & "QHSJ" & chr(34) & ":" & chr(34) & QHSJ & chr(34) & ","
      attrstr=attrstr & chr(34) & "CZR" & chr(34) & ":" & chr(34) & CZR & chr(34) & "}}]"
zstr="features=" &  attrstr & "&gdbVersion=&rollbackOnFailure=true&f=pjson"
zstr=encodestr(zstr)
parameter4 = "_namespace=erp.gis.arcgisserverhelper.interfaceentry&access_token=" & Token & "&methodname=JK134&parameter=" & zstr
```

**JK114 写新宗地**（NewZDToQHK，含几何）：

```vbs
inzbstr="[{" & chr(34) & "geometry" & chr(34) & ":{" & chr(34) & "rings" & chr(34) & ": [[" & replace(zdzbstr , "{rings:[[","")
fea_=SSProcess.GetObjectAttr(ZDID,"[FeatureGUID]")
attrstr=chr(34) & "attributes" & chr(34) & ": {"
      attrstr=attrstr & chr(34) & "YSDM" & chr(34) & ":" & chr(34) & "6801074" & chr(34) & ","
      ...
      attrstr=attrstr & chr(34) & "QHR" & chr(34) & ":" & chr(34) & QHR & chr(34) & "}}]"
zstr="features=" & inzbstr & "," & attrstr & "&gdbVersion=SDE.DEFAULT&rollbackOnFailure=true&f=pjson"
zstr=encodestr(zstr)
parameter2 = "_namespace=erp.gis.arcgisserverhelper.interfaceentry&access_token=" & Token & "&methodname=JK114&parameter=" & zstr
```

要点：
- JK 系列本质是**把 ArcGIS REST 请求体整体包进 `parameter` 字段**，由 ERP 网关转发到 ArcGIS Server，从而获得 Token 保护并隐藏内网 GIS 服务；
- 脚本注释中保留了直连 URL 原型（`QH/FeatureServer/3/addFeatures`、`QH/FeatureServer/0/addFeatures`），证明代理模式是直连模式的"加认证封装"。

#### 4.2.4 已确认的 ArcGIS 服务与图层

| 服务 | 图层/用途 | 调用语义 |
|---|---|---|
| QH/FeatureServer/0 | 宗地要素（写取号库） | addFeatures |
| QH/FeatureServer/2 | 更新区域面 | query（占用验证）/ addFeatures（写入） |
| QH/FeatureServer/3 | 取号队列 | addFeatures / deleteFeatures |
| QH/MapServer/0、/1 | 图廓/宗地查询 | query |
| ZDHQH/FeatureServer/0 | 宗地号查询 | query |
| ZDWQH/FeatureServer/0 | 宗地文号查询 | query |

### 4.3 OA 系统（硬编码凭证）

**人员/企业信息查询**（输出勘界图.vbs 的 getallpeopleinfo 核心）：

```vbs
URL="http://chqy.shunde.gov.cn/sdch/public/interface/interface_ryxx.jsp?infuser=qinghuashanwei20170726&infpwd=123456&enterpriseName=" & enterpriseName
```

要点：
- 账号口令 `qinghuashanwei20170726 / 123456` **明文硬编码**在脚本 URL 中，全库多处复用；
- 另有 `yqxx.jsp`（企业信息）等同模式接口；
- 返回人员信息用于在成果图（勘界图/宗地图/违法图）上标注测量员/检查员等签字栏。

### 4.4 文件服务器 / 成果上传（WebFiler）

上传宗地图.vbs / 上传下载数据.vbs 的上传核心：

```vbs
Set fileUpload = CreateObject("SSFileUploadControl.SSUploadFileCtrl")
fileUpload.ProjectNO = WorkIID
fileUpload.SubPathName = createpath_     ' "成果出图数据"
fileUpload.serviceURL = "http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/WebFiler/EpsFileUploadService.asmx"
fileUpload.serviceSaveFileURL = "http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/WebFiler/SaveUploadFileForm.aspx"
fileUpload.blockSize = 1024*1024
' 分块上传本地 EDB 成果文件
```

要点：
- 上传对象为 EDB（EPS 工程文件）及各类成果附件；
- `blockSize = 1024*1024` 分块上传，支持断点续传；
- 上传完成后立即调用 `updateunitinfo` 写单元信息、`workflowsubmit` 提交工作流——**上传即业务推进**；
- 上传前必须 `reGetWork`（getunitworktodolist）确认已接单。

### 4.5 远程数据库 / SDE 空间库

下载数据函数.vbs 实证：

```vbs
WorkspaceHandle=SSArcSDE.ConnectToTablespace ("SDBDC")
DownLoadBDCDate WorkspaceHandle,ZDH,ZRZH,CH,FWID
```

按宗地号逐层下载（宗地→界址点→界址线→自然幢→房屋面/权界线/分层界线/楼层/户/基准点）：

```vbs
ZDlayerName="SDBDC.SHIYQZDJBXX"
ZDstrCondition="DJH='" & ZDH & "'"
SSArcSDE.SearchFeatureAttr WorkspaceHandle, ZDlayerName, ZDstrCondition, ZDorderByField, ZDselFields, ZDresultValues
...
SSArcSDE.DownloadSDEDBToLocalDB WorkspaceHandle, regionCoords, ZDlayerName, ZDwhereClause, 0
```

已确认的 SDE 图层命名规范（`库名.图层`）：

| 库 | 图层 | 含义 |
|---|---|---|
| SDBDC | SHIYQZDJBXX | 使用权宗地基本信息 |
| SDBDC | JZD / JZX | 界址点 / 界址线 |
| SDBDC | ZRZ / FWLC / FWH | 自然幢 / 房屋楼层 / 房屋户 |
| SDBDC | FWMJK / FWWQX / FWFHZQX / FangCZJ / FWFCFZD / FWFCFZX / FWFCFZM | 房屋面积库 / 房屋权界线 / 分层界线 / 房产测量基准点等 |
| SDBDC | QiTZD_500 | 其他宗地（500 比例尺） |
| NNDXDJ | （输出勘界图.vbs 中） | 农村地籍/地形数据 |

另有 ADODB 直连远程 Oracle（`sdgis/sdgis78` 等硬编码账号）与 SQL Server 的脚本，用于属性数据直查。

### 4.6 其他远程 WebService

| 服务 | 地址 | 认证 | 用途 |
|---|---|---|---|
| 业务通用 asmx | http://47.94.1.65:8065/SG_ERP_sdqtqh/sg_services/ws/business.asmx | 无 | 业务服务（注释保留） |
| 第三方代理 asmx | http://getnumber.shunde.gov.cn/SG_ERP_SDQTQH/sg_zyservices/Service1.asmx/RunWebservice | 硬编码 user=bjswkjgfyxgs&password=cnmdaohaob1&jk=runwebserviceaddress1 | 代理执行 ArcGIS 查询串 |
| 宗地图片服务 | http://19.200.42.71/chcgglywjk/getzd/LandInfoService.asmx/getZDAFile?ZDH=..&version=..&fileExt=JPG | 无 | 下载宗地 JPG（base64Binary 解码） |
| 南方权籍库 | http://19.200.44.251:3280/ArcGIS/rest/services/BDC_ZD_SHYQ/MapServer/0/query | 无 | 宗地存在性验证、坐标下载 |
| 联合测绘接口 | 172.20.10.240/FSCHQY/interface/dkxx、dtgx.fszrzy.foshan.gov.cn | 待确认 | 地块信息等联合测绘业务 |

**宗地 JPG 下载**（下载宗地jpg.vbs / 测试宗地接口.vbs 实证）：

```vbs
' GET http://19.200.42.71/chcgglywjk/getzd/LandInfoService.asmx/getZDAFile?ZDH=..&version=..&fileExt=JPG
' 响应为 base64Binary，解码后写为本地 JPG
```

---

## 五、典型调用链还原

### 5.1 违法宗地取号（最完整的端到端业务链）

```
┌─ 客户端（违法宗地取号.vbs） ─────────────────────────────────────┐
│ 1. OnInitScript：GetUserInfo 取用户名/部门；getdogrw 校验加密狗    │
│ 2. OnRButtonDown：选择违法宗地（SSObj_Code=6801074/6801053）      │
│ 3. 读取宗地坐标 → 拼 {rings:[[x,y],...]}                          │
│ 4. getHTTPattr(JK112) → 查询相交图廓，outFields=TFH               │
│ 5. 本地拓扑构面(Topologyarea) → 拼宗地范围 rings                  │
│ 6. getHTTPattr(JK113) → 查询相交宗地 DJH,BBH,ZL,QHZT              │
│ 7. OnDraw：绘制图廓/宗地/版本号/状态                              │
│ 8. OnOK：                                                            │
│    ├─ 读 Win32_PhysicalMedia 硬盘序列号作"机器标识"                │
│    ├─ getHTTPattr_1(JK133) → 按图幅查 QHSJ，时间差<0.01min 则拒   │
│    ├─ writeQHQueuelog(JK134) / deleteQHQueuelog(JK135) 抢锁       │
│    ├─ getHTTPattr(JK133) → 相交宗地交叉面积比 → 建议取新号/版本    │
│    ├─ SSPro.VbsQHDialog 弹窗人工决策                               │
│    ├─ NewZDToQHK(JK114) → 写新宗地到取号库（addFeatures）         │
│    ├─ writelog(JK115) → 写操作日志                                 │
│    └─ SSProcess.SetObjectAttr 回写本地宗地属性                     │
└───────────────────────────────────────────────────────────────────┘
        │ 每个请求都：geterpaddress → GetTokenAndInvalidTime
        ▼                      → POST CommonOperate（access_token）
ERP 网关 CommonOperate ──► ArcGIS 代理(JK) / 业务服务 / 加密狗服务
```

业务含义：该链路是**测绘生产取号的并发控制核心**——通过"图幅锁（QHSJ 时间戳）+ 宗地相交面积比"防止多地多队重复取号，保证宗地号/版本号唯一。

### 5.2 成果上传并提交审批（上传宗地图.vbs）

```
1. GetTokenAndInvalidTime + GetCurWorkInfo + GetUserInfo
2. reGetWork：getunitworktodolist 校验当前作业已接单
3. SSFileUploadControl.SSUploadFileCtrl 分块上传 EDB → WebFiler
4. updateunitinfo：写测量员/作业员/检查员及证件号等单元信息
5. workflowsubmit：带 userid+users(JSON) 提交工作流
```

业务含义：测绘成果（宗地图/勘界图/违法图/房产文件）完成本地绘制后，通过该链路**上传至政务 OA 并推动审批流程**，实现"图件入库+业务流转"一体化。

### 5.3 数据下载（下载数据函数.vbs）

```
1. SSArcSDE.ConnectToTablespace("SDBDC") 连远程 SDE
2. 按 DJH 查 SHIYQZDJBXX 拿 ZDGUID
3. 有 → DownloadSDEDBToLocalDB 下载宗地/界址点/界址线/幢/户全量
4. 无 → ISCBDCWEBSERVER 查南方权籍库(19.200.44.251) 验证宗地
5. 南方有 → 取坐标/属性绘制到本地（darwZDFW）
6. 都无 → DownloadSDEDBToLocalDB5 按范围批量下载其他宗地
```

业务含义：**双库校验**——本地 SDE 库查不到时自动回源到南方权籍库，保证宗地数据不遗漏。

---

## 六、EPS 网络通信标准写法模板

### 6.1 取 Token（每次请求前）

```vbs
geterpaddress URL                    ' 取网关地址
SSERPTool.GetTokenAndInvalidTime Token, InvalidTime   ' 取 Token
```

### 6.2 通用 POST 请求（form 编码）

```vbs
Set xmlhttp = CreateObject("Microsoft.XMLHTTP")
xmlhttp.Open "POST", URL, false
xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"
xmlhttp.Send parameter   ' 已拼好的参数字符串
str = xmlhttp.responseText
Set xmlhttp = nothing
```

### 6.3 调用 ERP 业务接口（统一模板）

```vbs
parameter = "_namespace=" & Namespace & "&_timestamp=&access_token=" & Token & "&业务参数..."
' 例：_namespace=erp.pro.unithelper.updateunitinfo&access_token=..&iid=..&unitinfo=..
```

### 6.4 调用 ArcGIS 代理（JK 模板）

```vbs
pstr="where=..&geometry=..&outFields=..&f=pjson"     ' ArcGIS REST 串
pstr=encodestr(pstr)                                  ' URL 编码
parameter = "_namespace=erp.gis.arcgisserverhelper.interfaceentry&access_token=" & Token & "&methodname=JKxxx&parameter=" & pstr
```

### 6.5 上传文件

```vbs
Set fileUpload = CreateObject("SSFileUploadControl.SSUploadFileCtrl")
fileUpload.ProjectNO = WorkIID
fileUpload.SubPathName = "成果出图数据"
fileUpload.serviceURL = "http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/WebFiler/EpsFileUploadService.asmx"
fileUpload.serviceSaveFileURL = "http://getnumber.shunde.gov.cn/sg_erp_sdqtqh/WebFiler/SaveUploadFileForm.aspx"
fileUpload.blockSize = 1024*1024
' fileUpload.UploadFile fileName
```

### 6.6 下载远程数据

```vbs
' SDE 空间库（SSArcSDE 组件）
WorkspaceHandle = SSArcSDE.ConnectToTablespace("SDBDC")
SSArcSDE.SearchFeatureAttr WorkspaceHandle, layerName, strCondition, orderBy, selFields, resultValues
SSArcSDE.DownloadSDEDBToLocalDB WorkspaceHandle, regionCoords, layerName, whereClause, 0

' HTTP 图片（base64 解码）
' GET http://19.200.42.71/.../getZDAFile?ZDH=..&fileExt=JPG
```

### 6.7 提交工作流

```vbs
parameter = "_namespace=erp.neto.workflowhelper.workflowsubmit&_timestamp=&access_token=" & Token & "&iid=" & WorkIID & "&wiid=" & WorkWIID & "&userid=" & userid & "&users=" & userjson
```

---

## 七、安全风险评估

| 风险点 | 位置 | 等级 | 说明 |
|---|---|---|---|
| OA 凭证硬编码 | interface_ryxx.jsp / yqxx.jsp URL | 🔴 高 | `qinghuashanwei20170726/123456` 明文分布于多个明文脚本 |
| 第三方代理凭证硬编码 | sg_zyservices/Service1.asmx | 🔴 高 | `bjswkjgfyxgs/cnmdaohaob1` 明文 |
| ArcGIS Server 直连无认证 | 221.4.165.144:6080 | 🔴 高 | 任何能访问内网的主机可直接 CRUD 空间数据 |
| 文件服务器上传无独立鉴权 | WebFiler 两个 asmx | 🟡 中 | 上传仅依赖会话，URL 无签名 |
| 远程数据库账号硬编码 | Oracle sdgis/sdgis78 等 | 🔴 高 | ADODB 直连脚本含明文口令 |
| 南方权籍库/图片服务无认证 | 19.200.44.251 / 19.200.42.71 | 🟡 中 | 可被遍历批量拉取宗地图片 |
| Token 每次取用、无刷新管理 | 全部脚本 | 🟢 低 | 失效后脚本无重试逻辑 |
| 无超时/重试机制 | 全部脚本 | 🟢 低 | xmlhttp 同步阻塞，网络异常直接失败 |

---

## 八、对 EPS 扩展性的网络层结论

1. **架构可迁移性高**：所有网络调用收敛于"CommonOperate 网关 + JK 代理 + SSArcSDE/SSFileUploadControl 组件"三套接口，只要按同样语义重写，即可将 VBS 迁移到 Python/Java/.NET，无需改动服务端；
2. **认证可强化路径明确**：Token 已是统一方案，只需将 OA/数据库/直连 ArcGIS 的硬编码与无认证统一纳入网关鉴权即可收敛风险；
3. **业务语义可复用**：取号锁、接单校验、成果上传、双库校验等调用链可直接映射为现代 API 编排（如工作流引擎 + 消息队列）；
4. **扩展新业务的标准姿势**：新功能 = 本地 EPS API（SSProcess 取数/写数）+ 一个 `_namespace` 命名空间 + 若干 JK/业务参数，服务端无需改动客户端部署。

---

*报告生成基于全库明文脚本代码级扫描与精读，所有 URL、参数、命名空间均有原文出处；加密脚本（`@1234567890-` 头）对应的明文副本已优先采用。*
*（内容由AI生成，仅供参考）*
