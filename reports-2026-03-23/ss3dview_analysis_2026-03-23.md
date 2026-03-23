# SS3DView.dll 分析报告
**日期**: 2026-03-23
**模块**: SS3DView.dll (2241函数 / 1876字符串)
**端口**: 12036

---

## 核心发现

### 1. SSGDALDataset — GDAL栅格封装类

EPS通过 GDAL 封装类处理卫星/航空影像和 DEM 数据：

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x100405d9 | `SSGDALDataset` vtable | GDAL数据集接口 |
| 0x10040603 | `generateContour` | **生成等高线** |
| 0x1004064a | `getRasterXSize` | 获取栅格X方向像素数 |
| 0x10040672 | `getRasterYSize` | 获取栅格Y方向像素数 |

### 2. 立体测量（Stereo）系统

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x10026a3a | `gbGetStereoViewMode` | 获取立体视图模式 |
| 多处 `Stereo` 引用 | | 立体像对处理 |

### 3. DEM 地形管理

| 类 | 说明 |
|----|------|
| `CDemBlock` | DEM数据块管理 |
| `CDemCell` | 单个DEM单元 |
| `CGridNet` | 网格网络 |
| `GetDemCellList` | 获取DEM单元格列表 |
| `GetBlockList` | 获取块列表 |

### 4. 完整3D引擎命令

SS3DView 实现了完整的 3D 渲染管线：

| 类别 | 命令 |
|------|------|
| **编辑** | `ss3dEditBegin`, `ss3dEditEnd` |
| **坐标变换** | `ss3dCoordTransform`, `ss3dSetWorkDirectory` |
| **几何** | `ss3dGeoBegin`, `ss3dGeoEnd`, `ss3dGeometryBegin/End` |
| **LOD** | `ss3dLodBegin`, `ss3dLodEnd` - 多层次细节管理 |
| **几何体** | `ss3dGeometrySphere`, `ss3dGeometryBox`, `ss3dGeometryCone`, `ss3dGeometryCylinder`, `ss3dGeometryCapsule` |
| **光源** | `ss3dAddLight` |
| **多边形** | `ss3dRetessellatePolygons`, `ss3dCreateSmoothNormals` |
| **图元** | `ss3dAddPrimitiveSet1`, `ss3dAddPrimitiveSet2` |

---

## EPS 3D/立体系统架构

```
SS3DView.dll
    │
    ├─ SSGDALDataset → GDAL → 卫星影像 / DEM
    │                     ├─ generateContour (等高线)
    │                     └─ getRasterX/YSize (影像尺寸)
    │
    ├─ CDemBlock / CDemCell → 数字高程模型
    │
    ├─ Stereo Module → gbGetStereoViewMode → 立体像对
    │
    └─ 3D Renderer
           ├─ ss3dGeometry* (球/立方体/锥/柱/胶囊)
           ├─ ss3dAddLight (光照)
           └─ ss3dLod* (LOD多细节层次)
```

---

## GDAL 在 EPS 中的作用

**GDAL 用途**：栅格影像处理（卫星、航空、DEM）

| 格式 | 说明 |
|------|------|
| GeoTIFF | 航测影像 |
| DEM | 数字高程模型 |
|.img | ERDAS 影像 |
| 各种栅格 | 通过 GDAL 统一接口读取 |

**GDAL 不用于**：矢量格式（SHP/DXF/GeoJSON）— 这些走 SSExchange
