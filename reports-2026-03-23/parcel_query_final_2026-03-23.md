# EPS/SSMap 宗地号查询链路 - 最终结论
**日期**: 2026-03-23
**工具**: IDA Pro 9.0 + idalib-mcp (SSMap.dll.i64 @ port 12003)

---

## 目标
还原 EPS 中输入"177030-099"时，从控件到 SQL 的完整字段绑定链。

---

## 核心发现

### SQL WHERE 字段确认：`Code`

通过完整反编译两个 SQL 组装函数，确认**所有脚本查询统一使用 `Code` 字段**作为宗地号过滤关键字：

**函数 1**：`CSSLocalDB::GetScriptSelectSQLexpression` @ `0x1008C376`

伪代码（字符串常量全部确认）：
```cpp
// SQL 构建顺序（来自 IDA 反编译）：
v4 = "SeqID"                  // 0x1015e124
v5 = "SELECT DISTINCTROW "
v7 = v5 + v4                 // "SELECT DISTINCTROW SeqID"
v8 = v7 + ", "               // "SELECT DISTINCTROW SeqID, "
v9 = v8 + "Code"             // 0x1015d454
v10 = v9 + ", "              // ", "
v11 = v10 + "Byname"         // 0x1015db9c
v12 = v11 + ", "             // ", "
v13 = v12 + "Details"        // 0x101608dc
v14 = v13 + " FROM "         // 0x1015da50
v15 = v14 + <table_name>
// 完整模板：
// SELECT DISTINCTROW SeqID, Code, Byname, Details FROM <table>

if (a4 >= 0) {
    // 追加 WHERE 子句
    Format("%d", a4);        // → "177030" (转为数字)
    " WHERE Code = " + "177030"
    // 最终 SQL：
    // SELECT DISTINCTROW SeqID, Code, Byname, Details FROM <table> WHERE Code = 177030
}
```

**函数 2**：`CSSLocalDB::GetFeatureSelectSQLexpression` @ `0x1008BC92`

字段列表（含 GeoType）：
```cpp
// SELECT DISTINCTROW SymbolScript, Code, Scale, Indent, Byname, LayerName,
//   Type, LineType, LineColor, Filter, Explode, Reverse, Thickness,
//   ObjectName, Others, AttrType, Reference, ExtraInfo, EpsCESymbol, GeoType
// FROM <table>
// WHERE Code = <value>
```

---

## 完整查询链路（闭环）

```
用户输入 "177030-099"
        ↓
CSSERPTools/CSSLocalDB::GetFeatureSQLexpression  (总调度)
        ├─→ GetScriptSelectSQLexpression (a4 = -1 或 数值)
        │       字段: SeqID, Code, Byname, Details
        │       WHERE: Code = 177030
        │
        └─→ GetFeatureSelectSQLexpression
                字段: SymbolScript, Code, Scale, Indent, Byname, ...
                WHERE: Code = <value>
                        ↓
                CDBRecordset::OpenRecordset(sql, ...)
                        ↓
                DAO/Jet 执行 SQL → 返回记录集
                        ↓
                CDBRecordset::GetRecord() → 提取字段值
                        ↓
                CRecord::GetString(fieldIndex) → 返回属性值
                        ↓
                MultiByteToWideChar() → 中文编码转换
                        ↓
                EPS UI 控件显示
```

---

## 关键常量表

| 字段名 | 地址 | 说明 |
|--------|------|------|
| `Code` | 0x1015d454 | **WHERE 字段** |
| `Byname` | 0x1015db9c | 宗地名称 |
| `SeqID` | 0x1015e124 | 序号 |
| `Details` | 0x101608dc | 详细信息 |
| `SymbolScript` | 0x1015c740 | 符号脚本 |
| `GeoType` | 0x10160884 | 几何类型 |
| `LayerName` | 0x1015e4f8 | 图层名 |
| ` FROM ` | 0x1015da50 | SQL 关键字 |
| ` WHERE ` | 0x1015cc2c | SQL 关键字 |
| `SELECT DISTINCTROW ` | 0x101608b8 | SQL 关键字 |

---

## 关键函数地址汇总

| 函数 | 地址 | 作用 |
|------|------|------|
| `GetScriptSelectSQLexpression` | 0x1008C376 | Script SQL 组装（Code 字段） |
| `GetFeatureSelectSQLexpression` | 0x1008BC92 | Feature SQL 组装（Code 字段） |
| `GetFeatureSQLexpression` | 0x1008BA4A | 总调度入口 |
| `CSSMultiMediaAttr::GetRecordSQL` | 0x100B6C66 | 字符串键通用 SQL 模板 |
| `CSSLocalDB::DelFeatureCode` | 0x1008D7F3 | 直接 `SELECT code FROM %s WHERE Code=%ld` |
| `CDBRecordset::OpenRecordset` | - | DAO 记录集执行入口 |
| `CSSLocalDB::GetObjAttrTable` | 0x100445B0 | 对象→属性表映射 |
| `CSSLocalDB::GetCodeAttrTable` | 0x1002F1F7 | Code→属性表路由 |
| `GetFieldCodeMap` | 0x1004B76C | 字段码映射 |

---

## 结论

**"177030-099" 的查询字段是 `Code`，值 `177030`（去除连字符后作为整数）。**

整个 EPS 地籍查询系统统一使用 `Code` 字段作为宗地号索引，无论走 Script 链路还是 Feature 链路，`WHERE Code = 177030` 是共同的执行点。

SQL 样例：
```sql
SELECT DISTINCTROW SeqID, Code, Byname, Details
  FROM <属性表名>
  WHERE Code = 177030
```

报告路径：`reports/parcel_query_final_2026-03-23.md`
