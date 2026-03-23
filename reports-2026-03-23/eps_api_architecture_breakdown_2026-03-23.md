# EPS 系统架构完整分析报告
**日期**: 2026-03-23
**工具**: IDA Pro 9.0 + idalib-mcp（逆向）| Fiddler（流量抓取）
**综合分析**

---

## ⚠️ 重大发现：EPS 不是查本地 EDB，是调远程 ArcGIS Server！

**来源**: Fiddler 抓包 `_Full.txt`（辛总助于 2026-03-23 17:17 捕获）

---

## 一、系统架构（实测修正）

```
┌─────────────────────────────────────────────────────────────┐
│  EPS 客户端 (SSERPTools.exe + SSMap.dll + SSCore32.dll)  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌────────────▼──────────────────┐
         │  getnumber.shunde.gov.cn       │
         │  身份认证服务器 (ASP.NET IIS)  │
         │  _namespace=...userlogin      │
         │  → 返回 UserId / Token / code │
         └────────────┬──────────────────┘
                       │ 授权成功后
         ┌────────────▼──────────────────┐
         │  218.104.177.240              │
         │  ArcGIS Server (IIS)           │
         │  _namespace=...interfaceentry  │
         │  methodname=JK101/JK102        │
         │  → 空间查询 + 属性返回          │
         └────────────────────────────────┘
```

**两个服务器职责明确**：
- `getnumber.shunde.gov.cn` — 身份认证、Token 发放
- `218.104.177.240` — GIS 空间数据（ArcGIS Server）

---

## 二、API 链路详解

### 2.1 身份认证（Auth Server）

**Endpoint**: `https://getnumber.shunde.gov.cn/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate`

**登录请求**:
```
POST /sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate
Content-Type: application/x-www-form-urlencoded

_namespace=erp.neto.netofficehelper.userlogin
&loginname=曾玮
&password=281436G52v364i.
&grant_type=password
&clientid=eps
```

**登录响应**:
```json
{
  "success": true,
  "data": {
    "user": {
      "UserId": "6DFEA517AAC9407DB2653879A61E1E2F",
      "UserName": "曾玮",
      "DeptName": "广州云舟智慧城市勘测设计有限公司",
      "UserTel": "13531358611"
    },
    "code": "6e471a58d6f9e97f8662f878633b3d8f"  // 授权码
  }
}
```

### 2.2 Token 获取

**获取时间戳 Token**:
```
GET https://getnumber.shunde.gov.cn/SG_ERP_SDQTQH/sg_webapi/erpsvc/common/erp.pro.sdgtj.GeTimeToken

timestamp=1774286814000

响应: {"success":true,"data":"600acfd58da3b27205838c87c0ac10f3"}  // 时间戳Token
```

**换取 Access Token**:
```
POST /sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate
_namespace=erp.auth.authhelper.gettoken
&userid=6DFEA517AAC9407DB2653879A61E1E2F
&code=6e471a58d6f9e97f8662f878633b3d8f
&clientid=eps

响应:
{
  "success": true,
  "data": {
    "USERID": "6DFEA517AAC9407DB2653879A61E1E2F",
    "ACCESS_TOKEN": "65d6a8d27650fce9fff1e541d0df92da",
    "EXPIREDTIME": "2026-03-24 03:26:52"  // 10小时有效期
  }
}
```

### 2.3 HASP 加密狗验证（失败）

```
POST https://218.104.177.240/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate
_namespace=erp.neto.netofficehelper.validepsregcode
&access_token=1c4c68effd1d1f4cbfbb7dfd36090947
&userid=6DFEA517AAC9407DB2653879A61E1E2F
&regcode=54390

响应: {"success":false,"msg":"验证失败-未找到验证的狗号:54390"}
```

→ EPS 有在线狗号验证环节，但 54390 不在服务器白名单（离线模式或未注册）

### 2.4 GIS 空间查询（核心！）

**Endpoint**: `https://218.104.177.240/sg_erp_sdqtqh/sg_webapi/erpsvc/CommonOperate`

```
_namespace=erp.gis.arcgisserverhelper.interfaceentry
&access_token=<ACCESS_TOKEN>
&methodname=JK101
```

**JK101 查询参数**（返回图号）:
```json
{
  "geometry": {
    "rings": [[[710227.10, 2535174.87],
                [710233.40, 2535175.34],
                [710234.04, 2535167.29],
                [710227.73, 2535166.84],
                [710227.10, 2535174.87]]],
    "geometryType": "esriGeometryPolygon",
    "spatialRel": "esriSpatialRelIntersects"
  },
  "outFields": "TFH",
  "returnGeometry": true
}
```

**JK101 响应**:
```json
{
  "success": true,
  "data": {
    "displayFieldName": "TFH",
    "fieldAliases": { "TFH": "图号" },
    "geometryType": "esriGeometryPolygon",
    "spatialReference": {
      "wkt": "PROJCS[\"CGCS2000_3_Degree_GK_CM_113E\", ...]"  // 坐标系
    },
    "fields": [{ "name": "TFH", "type": "esriFieldTypeString", "alias": "图号", "length": 20 }],
    "features": [{
      "attributes": { "TFH": "177-030" },
      "geometry": { "rings": [[[710148.02, 2535059.52], ...]] }
    }]
  }
}
```

**JK102 查询参数**（返回更多字段）:
```
outFields=DJH,BBH,ZL,QHZT
```
- DJH = 宗地号
- BBH = 版本号
- ZL = 地址
- QHZT = 核实状态

**JK102 响应**: 返回 117 条记录（`"count": 117`），完整宗地属性数据

---

## 三、坐标系确认

**CGCS2000_3_Degree_GK_CM_113E**

```
CGCS2000 (China Geodetic Coordinate System 2000)
3 Degree Gauss-Kruger Projection
Central Meridian: 113°E
False Easting: 700000m
```

与 IDA 分析的 `DecryptCoord @ 0x10038044` 结论一致！

---

## 四、字段映射（实测）

| 字段名 | 中文名 | 来源 | 说明 |
|--------|--------|------|------|
| TFH | 图号 | ArcGIS JK101/102 | 177-030 |
| DJH | 宗地号 | ArcGIS JK102 | 地籍号 |
| Code | 宗地代码 | 本地 EDB/IDA | 177030（无连字符） |
| Byname | 名称 | 本地 EDB | 宗地名称 |
| ZL | 地址 | ArcGIS | 坐落地址 |
| QHZT | 核实状态 | ArcGIS | 核实状态 |

---

## 五、EPS 登录/查询完整时序

```
用户输入坐标 → EPS客户端
    ↓
SSERPTools.exe::ExecFunction("loginERP")
    ↓
sub_10007560 → CAPIDecrypt → ssExcuteFunction (SDL)
    ↓
HTTP POST: userlogin → getnumber.shunde.gov.cn
    ↓
获得: UserId + code
    ↓
HTTP GET: GeTimeToken → getnumber.shunde.gov.cn
    ↓
HTTP POST: gettoken → getnumber.shunde.gov.cn
    ↓
获得: ACCESS_TOKEN (10小时有效)
    ↓
HASP 验证: validepsregcode → 218.104.177.240 (可能离线失败)
    ↓
ArcGIS 空间查询: interfaceentry (JK101/JK102)
  geometry = EPS坐标 (710227, 2535175)
  outFields = TFH (图号)
    ↓
ArcGIS Server 返回: TFH = "177-030"  ← 图号
    ↓
本地 EDB 查询: WHERE Code = 177030
    ↓
返回: 宗地完整属性 (Byname/Details/SequenceID)
    ↓
EPS UI 显示
```

---

## 六、关键 API 地址汇总

### 远程服务器
| 服务器 | IP/域名 | 用途 |
|--------|---------|------|
| Auth Server | `getnumber.shunde.gov.cn` | 身份认证、Token |
| GIS Server | `218.104.177.240` | ArcGIS Server 空间查询 |

### 客户端关键函数（IDA）
| 函数 | 地址 | 作用 |
|------|------|------|
| CSSERPToolsInterface::ExecFunction | 0x1001B4A0 | 命令分发器 |
| sub_10007560 | 0x10007560 | 登录处理 |
| CAPIDecrypt | 0x10033344 | 密码解密 |
| ssExcuteFunction | (SScriptCore.dll) | SDL脚本执行 |
| GetFeatureSQLexpression | 0x1008BA4A | SQL组装总入口 |
| GetFeatureSelectSQLexpression | 0x1008BC92 | Feature SQL生成 |
| GetScriptSelectSQLexpression | 0x1008C376 | Script SQL生成 |
| DecryptCoord | 0x10038044 | 坐标解密 |

### 关键字段常量（IDA）
| 字段 | IDA 地址 |
|------|----------|
| `Code` (WHERE字段) | 0x1015D454 |
| `Byname` | 0x1015DB9C |
| `SeqID` | 0x1015E124 |
| `TFH` (图号) | ArcGIS 字段 |
| ` FROM ` | 0x1015DA50 |
| ` WHERE ` | 0x1015CC2C |

---

## 七、结论

1. **EPS 采用双服务器架构**：认证服务器 + GIS 空间服务器分离
2. **本地 EDB 不是数据源，是缓存**：空间查询走 ArcGIS Server，属地查询走本地 EDB
3. **坐标系**：CGCS2000 3度带（经线113°E），与 IDA 分析的坐标加密算法吻合
4. **HASP 在线验证**：存在但当前失败（regcode=54390 未注册）
5. **TFH（图号）= ArcGIS 的 displayFieldName**，与本地 EDB 的 `Code` 字段对应

---

## 八、SSWEBGIS Web 端分析（新增）

**来源**: `http://219.130.221.6/SG_ERP_FSWW/SSWEBGIS/` 浏览器截图 + UI 探索

### 8.1 系统定位
- **IP**: `219.130.221.6`（与 Fiddler 抓包的 `218.104.177.240` 不同！）
- **归属**: 佛山市顺德区测绘地理信息管理系统（链接: `www.xnschy.com` — 顺德测绘）
- **技术栈**: ArcGIS Web Application (JavaScript WebMap)

### 8.2 功能面板

**图层管理**（基础图层 + 业务图层）:
- 基础地形 ✅ 已显示
- 地形更新区域 ✅ 已显示

**图幅定位**（地图号查询）:
- 输入框：`请输入查询内容`
- 查询方式：精确查询 / 模糊查询
- 查询字段：图幅号 ✅（checkbox 已勾选）
- 提示：可按要素图层"名称"或注记图层"注记内容"查询
- **结论**：这就是 EPS 客户端"图幅号→坐标"功能的 Web 版本！

**项目管理**（EPS 工作流）:
| 阶段 | 数量 |
|------|------|
| 作业申请 | 6 |
| 审核中 | 11 |
| 生产中 | 269 |
| 质检中 | 82 |
| 已办结 | 597 |
| **合计** | **965** |

查询字段：业务编号 / 项目名称

### 8.3 与 Fiddler 抓包的关系
- `218.104.177.240` — ArcGIS Server（GIS 空间数据，JK101/JK102）
- `219.130.221.6` — SSWEBGIS（Web 端界面，图幅定位+项目管理）
- 两者通过同一套 ArcGIS Server 提供数据
- 辛总助抓包截图显示：EPS 本体（PID 15920）在抓包期间无 TCP 连接 → **EPS 可能通过其他网络路径（VPN/专线）访问政务网**

---

## 九、网络架构推测

```
┌──────────────────────────────────────────────────────────────┐
│  EPS 客户端 (Eps.exe PID 15920)                              │
│  ─ 顺德政务网专线（不经过 WLAN）→ 218.104.177.240 (ArcGIS)    │
│  ─ WLAN 直连 → getnumber.shunde.gov.cn (认证)                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SSWEBGIS Web 端 (219.130.221.6)                             │
│  → ArcGIS Server (218.104.177.240)                           │
│  → 顺德测绘官网 (www.xnschy.com)                              │
└──────────────────────────────────────────────────────────────┘
```

**注意**: 辛总助抓包时 EPS 无连接的可能原因：
1. EPS 通过政务内网/VPN 访问，绕过了 WLAN 网卡
2. EPS 使用系统代理，导致抓包工具未捕获
3. 抓包窗口期内 EPS 无实际联网操作

---

**报告基于**:
- IDA Pro 9.0 + idalib-mcp 逆向（SSERPTools.exe / SSCore32.dll / SSMap.dll）
- Fiddler SAZ 抓包 `_Full.txt`（2026-03-23 17:17）
- SSWEBGIS Web 界面探索（`http://219.130.221.6`）
- 辛总助抓包分析截图（`captures/net/`）
