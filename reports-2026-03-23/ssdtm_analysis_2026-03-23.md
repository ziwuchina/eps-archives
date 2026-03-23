# SSDtm.dll 分析报告
**日期**: 2026-03-23
**模块**: SSDtm.dll (2469函数)
**端口**: 12042

---

## 核心发现：DTM/TERRAIN 数字地形模型

### 类体系

| 类 | 说明 |
|----|------|
| `CDtmBase` | DTM基类 |
| `CGridNet` | **Grid格式DEM**（规则网格） |
| `CDemBlock` | DEM数据块 |
| `CDemCell` | 单个DEM单元格 |
| `CTriNet` | **TIN格式DEM**（不规则三角网） |
| `CTriangleMateItem` | 三角网辅助项 |

### 关键函数（DEM操作）

| 函数 | 说明 |
|------|------|
| `GetDemCellList` | 获取DEM单元格列表 |
| `GetDemHeight` | 获取指定坐标高程 |
| `GetDemSlope` | 获取坡度 |
| `GetDemSurfaceArea` | 获取表面积 |
| `GetDem3DLine` | 获取3D线 |
| `CreateOneDemInRect` | 在矩形范围内创建DEM |

### 关键函数（等高线生成）

| 函数 | 说明 |
|------|------|
| `CreateContour` | **生成等高线**（Grid/TIN双实现） |
| `CreateOneHeightContour` | 生成单高等高线 |

### 关键函数（Grid属性）

| 函数 | 说明 |
|------|------|
| `GetCellSize` | 获取格网单元大小 |
| `GetCellRows` | 获取行数 |
| `GetCellCols` | 获取列数 |
| `GetBlockList` | 获取块列表 |

---

## EPS 地形模型架构

```
SSDtm.dll
    │
    ├─ Grid格式 (CGridNet) — 规则高程格网
    │     ├─ GetDemHeight — 高程插值
    │     ├─ CreateContour — Grid等高线生成
    │     └─ CreateOneDemInRect — 区域DEM创建
    │
    └─ TIN格式 (CTriNet) — 不规则三角网
          ├─ CreateContour — TIN等高线生成
          ├─ CreateOneHeightContour — 单高等高线
          └─ CTriangleMateItem — 三角网构建

SS3DView.dll (SSGDALDataset)
    └─ generateContour ← 来自SSDtm的等高线生成结果
```

---

## 与SS3DView的关系

`SS3DView` 的 `SSGDALDataset::generateContour` 只是渲染层面的调用，实际等高线计算在 `SSDtm.dll` 的 `CreateContour` 函数中。

SS3DView 通过 GDAL 读取 DEM 栅格数据，然后调用 SSDtm 进行等高线计算，最后渲染输出。
