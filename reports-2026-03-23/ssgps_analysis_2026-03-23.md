# SSGps.dll 分析报告
**日期**: 2026-03-23
**模块**: SSGps.dll (1051函数)
**端口**: 12058

---

## 核心发现：GPS 数据处理模块（含RTK基准站）

### NMEA 协议确认

| NMEA语句 | 含义 | 数量 |
|----------|------|------|
| `GPGGA` | GPS定位数据（时间/坐标/质量） | 1处 |
| `GPRMC` | 推荐最小定位数据（速度/航向） | 1处 |

### GPS 相关字符串

| 关键字 | 引用次数 | 说明 |
|--------|---------|------|
| `GPS` | 7 | GPS相关 |
| `Position` | 1 | 位置 |
| `Coordinate` | 2 | 坐标 |
| `Base` | **56处** | 基准站（RTK测量） |

### 坐标转换

- `CSSTransCoordinate` — 坐标转换类（从字符串命中确认）

---

## EPS GPS 架构

```
SSGps.dll
  ├─ NMEA协议解析：GPGGA（定位）/ GPRMC（航向速度）
  ├─ RTK基准站处理：Base station（56处引用）
  └─ 坐标转换：CSSTransCoordinate

SSEngineeringSurvey.dll
  └─ 调用SSGps进行GPS测量数据处理
```

---

## 实际意义

RTK（实时动态定位）需要基准站差分数据。SSGps的"Base" 56处引用说明EPS支持：
- 基准站模式（Base Station）
- 移动站模式（Rover）
- 实时差分定位
