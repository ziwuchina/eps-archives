# SSFuncLib.dll 分析报告
**日期**: 2026-03-23
**模块**: SSFuncLib.dll (2685函数)
**端口**: 12047

---

## 核心发现：Microsoft Excel 集成库！

SSFuncLib.dll 不是"函数库"，而是 **EPS 与 Microsoft Excel 的集成桥梁**！

### Excel 函数封装

| 函数 | 说明 |
|------|------|
| `GetWorksheetFunction@_Application@msexcel` | 获取Excel工作表函数 |
| `GetRegisteredFunctions@_Application@msexcel` | 获取已注册函数列表 |
| `GetConsolidationFunction@_Worksheet@msexcel` | 获取合并函数 |
| `FunctionWizard@Range@msexcel` | 函数向导 |
| `Calculate@_Worksheet@msexcel` | 重新计算工作表 |
| `CalculateFull@_Application@msexcel` | 全量计算 |
| `Calculate@Range@msexcel` | 范围计算 |

### 关键结论

EPS 通过 SSFuncLib 调用 Excel 的计算引擎，实现：
- **公式计算**：土地面积、容积率等指标的Excel公式计算
- **数据汇总**：多地块数据的Excel式汇总
- **函数向导**：用户可在EPS中使用Excel函数

### EPS Excel 集成架构

```
用户输入 → SSFuncLib → Microsoft Excel COM
                    ↓
            计算结果返回EPS
                    ↓
            属性表更新
```
