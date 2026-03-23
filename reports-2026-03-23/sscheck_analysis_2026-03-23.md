# SSCheck.dll 质检系统分析报告
**日期**: 2026-03-23
**模块**: SSCheck.dll (3501函数 / 3089字符串)
**端口**: 12007

---

## 1. 模块定位

SSCheck.dll 是 EPS 的**质检引擎**，负责对测绘数据进行质量检查，生成检查记录和错误报告。

---

## 2. 核心类结构

### 质检管理层
| 类 | 地址 | 说明 |
|---|------|------|
| `CCheckManager` | - | 质检管理器（GetCheckModelList等） |
| `CCheckModelList` | 0x10004165 | 质检模型列表 |
| `CCheckModel` | 0x100a73d6 | **质检模型（核心）**，执行ExecuteCheck/ExecuteRepair |
| `CCheckDesignList` | 0x100a74ea | 质检设计列表 |
| `CCheckDesign` | 0x100041c2 | 质检设计（配置） |

### 检查记录层
| 类 | 地址 | 说明 |
|---|------|------|
| `CCheckRecord` | 0x10003fb2 | **单条检查记录**（错误/警告） |
| `CCheckRecordList` | - | 检查记录列表 |
| `CSSProcess` | - | 过程管理，含GetCheckRecordList/SetCheckRecordList |

---

## 3. 核心方法

### CCheckModel（质检模型执行器）
| 地址 | 函数 | 说明 |
|------|------|------|
| 0x100a740c | `ExecuteCheck` | **执行质检**（传入ScaleMap+模型+记录列表） |
| 0x100a73f4 | `ExecuteRepair` | 执行修复 |
| 0x100a73d6 | `DealCheckRecord` | 处理检查记录 |
| 0x100a73e8 | `AddParameter` | 添加质检参数（参数名/类型/值） |
| 0x100a7418 | `CreateCheckRecord` | 创建检查记录 |
| 0x100a73fa | `GetCheckModelList` | 获取质检模型列表 |

### CCheckDesignList（质检设计管理）
| 地址 | 函数 | 说明 |
|------|------|------|
| 0x100a752c | `ReadDesign` | **读取质检设计文件** |
| 0x100a74de | `GetCheck` | 获取指定检查 |
| 0x100a7556 | `RemoveCheck` | 删除检查 |
| 0x100a755c | `IsExistCheck` | 检查是否存在 |
| 0x100a7568 | `GetGroupCheckDesignList` | 获取分组检查设计列表 |
| 0x100a7574 | `RenameCheck` | 重命名检查 |

---

## 4. 错误报告系统

### 错误记录管理
| 地址 | 函数 | 说明 |
|------|------|------|
| 0x100a74c0 | `ResetErrorReportRecordStatus` | 重置错误报告记录状态 |
| 0x100a75b0 | `RegisterErrorReportRecord` | **注册错误报告记录** |
| 0x100a75b6 | `RemoveErrorReportRecord` | 删除错误报告记录 |
| 0x100a769a | `SaveErrorReportRecord` | 保存错误报告记录 |
| 0x100a81d4 | `ReportError` | 报告错误 |

---

## 5. 质检流程推测

```
1. CCheckDesignList::ReadDesign(xml/配置文件)
   → 加载质检设计（检查项/分组/规则）

2. CCheckModel::ExecuteCheck(ScaleMap, 模型名, 参数, 记录列表)
   → 遍历所有质检项

3. 每项检查 → CCheckModel::CreateCheckRecord
   → CCheckModel::DealCheckRecord
   → 注册错误报告 → RegisterErrorReportRecord

4. 检查完成 → SaveErrorReportRecord

5. CSSProcess::SetCheckRecordList(CCheckRecordList)
   → 纳入工作流管理
```

---

## 6. 与其他模块的集成

- `CSSProcess::GetCheckRecordList/SetCheckRecordList` — 与SSProcess工作流系统集成
- 质检记录可通过 DAO 存储到 EPS EDB 数据库
- 与 SSMap.dll 坐标检查功能集成（DecryptCoord/EncryptCoord）

---

## 7. 关键字符串

| 字符串 | 地址 | 说明 |
|--------|------|------|
| `SSCheck` | 0x100e9a17等4处 | 模块名 |
| `Check` | 0x100e6c56等245处 | 检查相关 |
| `QC` | 0x10083093 | 质检控制 |
| `Rule` | 0x100e2cb4等2处 | 质检规则 |
| `Error` | 0x100e7658等7处 | 错误相关 |
| `Validate` | 0x100e3797等2处 | 验证 |

---

## 8. 结论

SSCheck.dll 是一个**基于配置文件驱动**的质检引擎：
- **设计层**：XML/配置文件定义检查项和规则（`ReadDesign`）
- **执行层**：`CCheckModel::ExecuteCheck` 遍历执行
- **记录层**：`CCheckRecord/CCheckRecordList` 保存错误记录
- **集成点**：`CSSProcess::SetCheckRecordList` 与工作流系统连接

质检结果可以触发工作流状态变更（进入"质检中"→"已办结"）。
