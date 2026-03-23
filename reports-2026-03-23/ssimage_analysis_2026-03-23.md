# SSImage.dll 分析报告
**日期**: 2026-03-23
**模块**: SSImage.dll (1909函数)
**端口**: 12055

---

## 核心发现：EPS 影像数据处理模块

### 核心类

| 类 | 说明 |
|----|------|
| `CEpsImage` | EPS影像数据类 |
| `CDib` | Windows设备无关位图（Device Independent Bitmap） |

### 关键函数

**影像定位与几何：**
| 函数 | 说明 |
|------|------|
| `GetImageLeftBottomPos` | 获取影像左下角坐标 |
| `SetImageLeftBottomPos` | 设置影像左下角坐标 |
| `GetPixelPerMeter` | 获取像素/米比例（分辨率） |

**影像滤波：**
| 函数 | 说明 |
|------|------|
| `GetFilterScale` | 获取滤波比例 |
| `SetFilterScale` | 设置滤波比例 |

**BMP处理：**
| 函数 | 说明 |
|------|------|
| `FlashBmpRowBuffer` | 刷新BMP行缓冲区 |
| `SetBmpRowBufferCount` | 设置BMP行缓冲数量 |

---

## EPS 影像架构

```
SSImage.dll
  └─ CEpsImage — 加载GeoTIFF/影像
       ├─ 像素分辨率：GetPixelPerMeter
       ├─ 地理定位：SetImageLeftBottomPos
       └─ 滤波处理：SetFilterScale/GetFilterScale

SSMap.dll (CDataXCore)
  └─ 调用SSImage进行影像底图显示
```

---

## 与SS3DView的关系

SS3DView 的 SSGDALDataset 处理DEM和栅格数据，而 SSImage 处理普通影像（航空影像、卫星影像等）。两者共同构成EPS的完整栅格影像支持。
