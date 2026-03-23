# Parcel Query Chain - Phase 4 (实参绑定点)

## 目标
确定 `CSSMultiMediaAttr::GetRecordSQL` 中 `this[3..6]` 的真实来源，打通“字段名 + where 值 + SQL 执行”最后一跳。

## 关键函数

### 1) SQL模板函数
- `CSSMultiMediaAttr::GetRecordSQL` @ `0x100B6C66`

伪代码核心：
```cpp
if (mbscmp(this[4], byte_1015C8B0))
    Format("Select [%s] From [%s] Where [%s] = '%s';", this[6], this[3], this[4], this[5]);
else
    Format("Select [%s] From [%s] Where [%s] = %s;", this[6], this[3], this[4], this[5]);
```

字段含义：
- `this[3]` (offset +12): 表名
- `this[4]` (offset +16): WHERE 字段名
- `this[5]` (offset +20): WHERE 值
- `this[6]` (offset +24): SELECT 返回字段名

---

### 2) 实参绑定函数（命中）
- `CRuntimeDlgTemplate::SetAttrData` @ `0x100A3C4D`

在为二进制/文件引用控件创建 `CSSLongBinaryEdit/CSSFileReferenceEdit` 后，直接赋值：
```cpp
UserData = CRuntimeDlgCell::GetUserData(cell);
CString::operator=(UserData + 12, &a3);                    // this[3]
CString::operator=(UserData + 16, &a4);                    // this[4]
CString::operator=(UserData + 20, &a5);                    // this[5]
CString::operator=(UserData + 24, Str2_values[v16]);       // this[6]
(*UserData->vftable[5])(UserData); // Open/LoadData
```

含义：
- `a3` = 表名（函数内 `CDaoTableDef::Open(a3)` 可证）
- `a4` = 键字段名（WHERE 左侧）
- `a5` = 键值（WHERE 右侧）
- `Str2[v16]` = 当前属性字段名（SELECT 字段）

---

### 3) 调用/执行层
`GetRecordSQL` 的代码 xrefs（调用点）：
- `0x100B6F74` (CSSLongBinaryEdit::Upload)
- `0x100B7D91` (CSSLongBinaryEdit::Delete)
- `0x100B7F0C` (CSSLongBinaryEdit::LoadData)
- `0x100B8A1C` (CSSFileReferenceEdit::Upload)
- `0x100B8EF6` (CSSFileReferenceEdit::Delete)
- `0x100B9047` (CSSFileReferenceEdit::LoadData)

这些调用点统一走：
```cpp
GetRecordSQL(...) -> CDBRecordset::OpenRecordset(sql,...)
```

并在多个分支可见：
- `atoi(this+20)` → 说明此链路中 `this[5]` 常为数值 ID 字符串（可转 int）

---

## 与“177030-099”的关系（结论）
- 对 **多媒体属性链路**（CSSMultiMediaAttr）而言：
  - WHERE 字段和 WHERE 值不是硬编码，均由 `SetAttrData(0x100A3C4D)` 的 `a4/a5` 运行时注入。
- 因此：
  - 若输入 `177030-099`，它将出现在 `a5 -> this[5]`，最终进入 `Where [%s] = '%s'` 模板。
  - 最终字段名取决于同一调用点给的 `a4`（不是在 `GetRecordSQL` 内决定）。

---

## 最后一刀建议
下一步只需再追一层：谁调用了 `CRuntimeDlgTemplate::SetAttrData(0x100A3C4D)` 并传入了 `a4/a5`。
拿到那个调用点，就能把 `177030-099` 对应字段名（ParcelNo/Byname/Code/其他）精确落地。
