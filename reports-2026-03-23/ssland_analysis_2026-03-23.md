# SSLand.dll 分析报告
**日期**: 2026-03-23
**模块**: SSLand.dll (1919函数)
**端口**: 12048

---

## 核心发现：土地利用规划模块

### 核心类

| 类 | 说明 |
|----|------|
| `CGeoBase` | 地理基础类（SetUserID/GetUserID） |
| `CUserLayer` | 用户图层管理 |
| `CCheckDesign` | 土地检查设计 |

### 关键功能

- **用户ID管理**：`SetUserID/GetUserID`
- **图层操作**：`SetlayerName/GetUserLayerList/GetUserLayer/GetMapboxLayer`
- **检查设计**：`CCheckDesign` — 用于土地规划的合规检查

### 与其他模块的关系

SSLand 与 SSCadastre（地籍）的区别：
- **SSCadastre**：不动产登记（权利、证书）
- **SSLand**：土地利用规划（用途分区、用地红线）
- 两者共享同一地图视图（SSMap.dll）
