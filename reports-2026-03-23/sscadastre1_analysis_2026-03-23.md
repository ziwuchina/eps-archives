# SSCadastre1.dll 分析报告
**日期**: 2026-03-23
**模块**: SSCadastre1.dll (3431函数)
**端口**: 12044

---

## 核心发现：SSCadastre 扩展版本

SSCadastre1.dll 是 SSCadastre.dll 的**扩展版本**，增加了登记注册功能。

### 关键功能

**命令注册系统：**
- `CCmOperation::RegisterCommand` — 注册命令
- `CSDLInterface::RegisterCmd` — SDL脚本命令注册
- `IsRegisterSoft` — 软件注册校验

**属性面板UI（与SSHouse共用）：**
- `CBCGPEpsPropList` — EPS属性列表（BCG定制版）
- `OnPropertyChanged` — 属性变更通知
- `FormatProperty` — 属性格式化
- `AddProperty` — 添加属性
- `UpdatePropertyTab` — 更新属性页

**地籍记录：**
- `CCheckRecord` — 地籍审核记录

### 与SSCadastre.dll的区别

SSCadastre.dll（3063函数）= 基础地籍数据模型
SSCadastre1.dll（3431函数）= **增加了登记注册工作流**

两者共同构成完整的 EPS 地籍不动产系统。
