# Parcel Query Chain - Phase 3 (SSMap.dll)

## 目标
还原“宗地号查询（如 177030-099）”在 SSMap 中的 SQL 组装链，确认字段、WHERE 条件模板、执行函数。

## 已确认的 SQL 组装函数

1) `CSSLocalDB::GetFeatureSQLexpression` @ `0x1008BA4A`
- 作用：总调度，按参数走 feature/script 两条 SQL 生成路径。
- 调用：
  - `GetFeatureSelectSQLexpression` @ `0x1008BC92`
  - `GetScriptSelectSQLexpression` @ `0x1008C376`

2) `CSSLocalDB::GetFeatureSelectSQLexpression` @ `0x1008BC92`
- 作用：拼 Feature 选择 SQL。
- 关键 WHERE 模板（a4>=0 时）：`WHERE Code=<value>`
- 关键排序：`ORDER BY Code` / `ORDER BY Byname`（取决于上层参数）

3) `CSSLocalDB::GetScriptSelectSQLexpression` @ `0x1008C376`
- 作用：拼 Script 侧 SQL。
- 关键 SQL（核心字段）：`SELECT DISTINCT SeqID, Code, Byname, Details FROM <table>`
- 关键 WHERE 模板（a4>=0 时）：`WHERE Code=<value>`

4) `CSSLocalDB::DelFeatureCode` @ `0x1008D7F3`
- 直接命中模板：`SELECT code From %s WHERE Code=%ld`
- 说明：Code 列作为关键过滤字段被直接用于 SQL 条件。

5) `CSSMultiMediaAttr::GetRecordSQL` @ `0x100B6C66`
- 通用记录查询模板：
  - 字符串键：`Select [%s] From [%s] Where [%s] = '%s';`
  - 数值键：`Select [%s] From [%s] Where [%s] = %s;`
- 说明：这是“字段名 + 表名 + 键字段 + 键值”四元组拼接器，宗地号类字符串键（如 177030-099）更可能走这一分支。

## 已确认的 WHERE 片段字符串（get_string）
- `0x101609D6` -> `Code=%ld`
- `0x1015CD22` -> ` where ID in([IDList])`
- `0x1015CD29` -> `ID in([IDList])`
- `0x1015CE3E` -> ` where ID>0 and (FeatureGUID={00000000-0000-0000-0000-000000000000} or FeatureGUID Is Null)`

## 执行层函数（已确认）
- `CSSDatabase::CreateRecordset`（多处调用）
- `CDBRecordset::OpenRecordset` / `CloseRecordset`
- `CSSDatabase::GetAllRecords`

即：上层先拼 SQL，再由 `CreateRecordset/OpenRecordset` 执行。

## 关于“177030-099”的结论（当前阶段）
- 数值型 feature code 链路：明确是 `WHERE Code=<int>`（见 0x1008BC92 / 0x1008C376 / 0x1008D7F3）。
- 字符串型宗地号链路：使用 `CSSMultiMediaAttr::GetRecordSQL` 的字符串 WHERE 模板（见 0x100B6C66）。
- 还差最后一跳：从“宗地号输入控件/命令”到 `GetRecordSQL` 参数 `this[4]/this[5]/this[3]` 的实参绑定点（即可得最终键字段名是否为 ParcelNo/Byname/其它字典映射字段）。

## 推荐下一刀
从 `GetObjAttrTable` (`0x100445B0`) + `GetFieldCodeMap` (`0x1004B76C`) 继续追实参绑定，锁定 `this[4]` 实际字段名。
