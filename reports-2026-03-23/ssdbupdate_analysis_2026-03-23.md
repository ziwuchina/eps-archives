# SSDBUpdate.dll 分析报告
**日期**: 2026-03-23
**模块**: SSDBUpdate.dll (3078函数)
**端口**: 12043

---

## 核心发现：数据库更新引擎

### CSSGisDB — GIS数据库操作核心类

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x1007fd24 | `GetAttrFieldInfos` | 获取属性字段信息 |
| 0x1007fe26 | `CreateAttrTable` | 创建属性表 |
| 0x1007fe20 | `UpdateTemplate` | 更新模板 |
| 0x1007fe6e | `UpdateAttrData` | **更新属性数据** |
| 0x1007fde0 | `GetAttrRecord` | 获取属性记录 |
| 0x1007fe0e | `DeleteData` | 删除数据 |
| 0x1007fe8c | `DeleteDEM` | 删除DEM数据 |
| 0x10080234 | `DeleteTable` | 删除表 |
| 0x1007fd54 | `DeleteData` | 删除数据 |
| 0x1008071a | `DeleteKey` | 删除键值 |

### 空间查询

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x100061a0 | `IsCanQuery` | 是否可查询 |
| 0x10003c80 | `SearchPoint` | 点查询 |
| 0x10080b10 | `SearchObject` | 对象查询 |
| 0x10080b52 | `SearchPolygon` | 多边形查询 |
| 0x10080af8 | `SearchFilter` | 过滤器查询 |

### 图层/缓冲管理

| 地址 | 函数 | 说明 |
|------|------|------|
| 0x1008067e | `InsertBufferLayer` | 插入缓冲层 |
| 0x10080000 | `Insert` | 插入对象 |
| 0x10080144 | `UpdateSelection` | 更新选择集 |
| 0x10080ba0 | `ExChangeObj` | 交换对象 |

---

## EPS 数据库更新架构

```
用户编辑地物
    ↓
SSERPTools（命令路由）
    ↓
SSDBUpdate.dll::CSSGisDB
    ├─ UpdateAttrData — 更新属性字段
    ├─ CreateAttrTable — 创建属性表
    └─ DeleteData — 删除记录
    ↓
SSDataXCore → SSDaoBase/SSAdoBase
    ↓
EPS EDB 数据库（platform.mdb）
```
