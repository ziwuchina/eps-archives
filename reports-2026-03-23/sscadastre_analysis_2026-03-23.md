# SSCadastre.dll 地籍/不动产分析报告
**日期**: 2026-03-23
**模块**: SSCadastre.dll (3063函数 / 2830字符串)
**端口**: 12009

---

## 1. 模块定位

SSCadastre = **Cadastral Real Estate Module**（地籍不动产模块）
- 27处 "SSCadastre" 字符串
- 27处 "Cadastre" 字符串
- 管理 房屋/权利人/不动产单元

---

## 2. 核心数据结构（从字符串推断）

| 字符串 | 地址 | 含义 |
|--------|------|------|
| `House` | 0x1009be00 (2处) | 房屋 |
| `QLR` | 0x1009aaaf (1处) | 权利人 |
| `FJ` | 0x10098921, 0x100992c9 (2处) | 附件/房屋 |
| `FW` | 10处 | 房屋（FW=房屋） |

---

## 3. 与其他模块的关系

- **SSJointSurvey.dll** 有 `BDCDYH`（不动产单元号）字段
- **SSCadastre** 通过 BDCDYH 关联 权利人(QLR) 和 房屋(FW)
- **SSMap.dll** 也引用了 `FW`, `QLR`, `FJ`（共享数据模型）

```
SSJointSurvey (ImportJZD)
    ↓ BDCDYH (不动产单元号)
SSCadastre (SSCadastre.dll)
    ↓ QLR (权利人) + FW (房屋)
SSMap (属性表)
```

---

## 4. 数据流推测

```
1. SSJointSurvey::ImportJZD → 导入界址点（含BDCDYH）
2. SSMap::GetObjAttrTable(BDCDYH) → 读取属性
3. SSCadastre → 查询权利人(QLR)和房屋(FW)信息
4. EPS EDB数据库 ← DAO存储
```

---

## 5. 待继续

- 具体 class 名称尚未解析（func_query 超时）
- BDCDYH 的格式和校验规则
- 与 ArcGIS 不动产库的关联方式
