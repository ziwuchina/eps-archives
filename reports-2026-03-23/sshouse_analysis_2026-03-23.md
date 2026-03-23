# SSHouse.dll 分析报告
**日期**: 2026-03-23
**模块**: SSHouse.dll (3000函数)
**端口**: 12041

---

## 重要发现：SSHouse 不是房产管理！

"House" 不是房地产，而是 **Survey House 测量房屋** — EPS 的房产分摊/分层数据模块。

### 真实功能

**1. TIN网格构建（与SSDtm重叠）**
- `CTriNetBuild` — TIN三角网构建器
- `SetMaxSideLength` — 设置最大边长
- `SetBorderTriFlag` — 设置边界三角标志
- `GetAllTriItems` / `GetOutAllTriItems` — 获取三角形列表
- `GetExtentRect` / `GetExtentHeight` — 范围/高程

**2. EPS属性面板UI**
- `CBCGPEpsPropList` — EPS属性列表控件
- `OnPropertyChanged` — 属性变更回调
- `FormatProperty` — 格式化属性值
- `UpdatePropertyTab` — 更新属性页

**3. Floor/分层数据**
- Floor字符串74处引用 — 分层分摊数据
- 房产分层管理（不是房产权利，是房屋分层）

---

## EPS "房屋" 分层模型

```
测量分层 (Survey House)
  ↓
CTriNetBuild — 生成三角网格
  ↓
CBCGPEpsPropList — 属性面板展示
  ↓
Floor数据管理 — 分层分摊计算
```

与SSRETools的"房产管理"的区别：
- SSRETools → 不动产登记（BDCDYH、权利人）
- SSHouse → 测量分层（分摊面积、楼层几何）
