# SSDataXCore.dll 分析报告
**日期**: 2026-03-23
**模块**: SSDataXCore.dll (1376函数)
**端口**: 12057

---

## 核心发现：数据交换核心引擎

SSDataXCore 是 EPS 的**统一数据交换中间层**，负责所有格式的数据导入导出。

### 核心接口

| 函数 | 说明 |
|------|------|
| `ImportData` | **导入数据**（`_DataXParameters`驱动） |
| `GetCustomExportFieldList` | 获取自定义导出字段列表 |
| `GetParameter@_DataXParameters` | 获取交换参数 |
| `GetParameterIndex` | 获取参数索引 |

### 数据操作

| 类 | 说明 |
|----|------|
| `CDaoRecordset` | DAO记录集操作 |
| `CDBRecordset` | 数据库记录集 |
| `CRecord` | 通用记录 |
| `CAttrItem / CAttrItemList` | 属性项/属性列表 |
| `CFieldBandItem` | 字段带项目 |
| `CSSTableCtrl` | 表格控件 |

### SQL操作
- `SetStrSQL` / `GetStrSQL` — SQL语句管理
- `OpenRecordset` — 打开记录集
- `MoveNext` — 记录导航
- `GetFieldValue` — 获取字段值

### 与其他模块的关系

```
SSERPTools.exe → SSDataXCore → 多种数据格式
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         SSImage.dll      SSDtm.dll      SSMap.dll
        （影像交换）      （DEM交换）    （矢量交换）
```

**关键结论：** SSDataXCore 是 EPS 数据互操作的核心枢纽，通过 `_DataXParameters` 参数驱动，支持多种数据格式的导入导出。
