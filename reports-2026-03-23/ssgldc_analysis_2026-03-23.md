# SSGLDC.dll 分析报告
**日期**: 2026-03-23
**模块**: SSGLDC.dll (1069函数 / 1193字符串)
**端口**: 12034

---

## 核心发现：GLDC = GIS Layer Display Control

CGLDC 是 EPS 的**渲染引擎**，负责地图/图层的屏幕绘制。

### CGLDC 核心方法

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x10002d1d | `SetDoubleBufMode` | 设置双缓冲模式 |
| 0x10002d2a | `IsDoubleBufMode` | 查询双缓冲状态 |
| 0x10002d31 | `SetMapScale` | 设置地图比例尺 |
| 0x10002d3b | `GetMapScale` | 获取地图比例尺 |
| 0x10002d46 | `GetCDC` | 获取设备上下文(MFC CDC) |
| 0x10002d4d | `SetCDC` | 设置设备上下文 |
| 0x10002da5 | `SetCursorPoint` | 设置光标位置 |
| 0x10002db7 | `GetCursorPoint` | 获取光标位置 |
| 0x10002dd5 | `SetLButtonDownPoint` | 设置鼠标左键按下位置 |
| 0x10002e40 | `SetTextColor` | 设置文字颜色 |
| 0x10002e4d | `GetTextColor` | 获取文字颜色 |
| 0x10002d3f | `GetBkColor` | 获取背景色 |
| 0x10002d86 | `SetWindow` | 设置关联窗口 |
| 0x10002d90 | `Invalidate` | 刷新重绘 |

### 对象管理

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x1000853a | `StoreObj` | 存储SSNote对象 |
| 0x10008a0e | `RestoreObj` | 恢复对象 |
| 0x1000945c | `GetDispLists` | 获取显示列表 |

### 标注/符号系统

| 类 | 说明 |
|----|------|
| `CSymBmp` | 符号位图渲染 |
| `CMarkNote` | 标注注记 |
| `CMarkNoteList` | 标注列表 |
| `SSNote` | 通用标注对象 |
| `CColorInfo` | 颜色信息 |
| `CColorInfoList` | 颜色列表 |

---

## EPS 渲染架构

```
Eps.exe (主程序)
    ↓
SSGLDC.dll = CGLDC (渲染引擎)
    ↓
GetCDC() → MFC CDC (设备上下文)
    ↓
GDI/GDI+ 或 OpenGL 绑定
    ↓
屏幕输出 (双缓冲支持)
```

---

## 依赖关系

- 无网络调用（纯渲染）
- 通过 CDC 与 MFC 对接
- 支持位图输出（GdipSetPenDashStyle 引用 GDI+）
