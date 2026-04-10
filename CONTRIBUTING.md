# 🎯 EPS 自动化项目贡献指南

## 项目定位

`eps-archives` 是 EPS（地籍测量软件）自动化项目的知识库与存档仓库。
核心目标是实现 **EPS 操作的无人值守自动化**，包括：

1. **IDA 调试联动** — 通过 IDA MCP 接口操控 EPS 调试状态
2. **VBS 脚本执行** — 通过 COM 接口触发 EPS 内部 VBS 脚本
3. **BAR 命令触发** — 通过 `WM_COMMAND` 模拟工具栏按钮点击
4. **弹窗治理** — 自动识别和处理 EPS 运行时弹窗
5. **数据导出** — EDB 数据批量导出与结构化处理

## 工作流程原则

### 硬约束（绝对不允许绕过）

1. **不接受坐标点击作为主执行路径**  
   工具栏按钮点击必须走 `WM_COMMAND` 或 COM 脚本，坐标路径只做兜底

2. **`.edb` 主窗口存在才执行**  
   任何 EPS 操作前必须确认主 `.edb` 窗口在线

3. **三证合一才算成功**  
   - COM 返回 `ret=0`
   - EPS 主进程存在（`hung=False`）
   - EDB 文件修改时间戳更新

4. **不盲发命令**  
   每条自动化命令后必须等待 + 观察 + 判窗，再发下一条

5. **自动化操作后必须核验残留进程**  
   用 `tasklist | findstr Eps` 确认无孤儿进程

## 分支策略

```
master   ← 稳定代码，只接受 PR 合并
  ↑
main    ← 开发主线
  ↑
feature/xxx  ← 功能分支，PR 到 main
```

## Commit 规范

```
feat:     新功能
fix:      修复
docs:     文档
refactor: 重构
test:     测试
chore:    杂项
eps:      EPS 自动化相关
```

示例：
```
eps: 新增 WM_COMMAND 抓包脚本
fix: 修复 IDA MCP 端口配置
docs: 更新 CONTRIBUTING.md
```

## 代码风格

- PowerShell 脚本：遵循 [PoshCode](https://github.com/PoshCode/PowerShell-practice-and-style)
- Python：遵循 [PEP 8](https://pep8.org/)
- 文件编码：**UTF-8**（无 BOM）

## 报告与证据规范

所有自动化执行必须附带证据，证据存放路径：

```
D:\AIcode\mcpida\reports\          ← 裴谦工作区
C:\Users\Administrator\.openclaw\workspace-peiqian\reports\  ← 主报告区
```

证据文件命名：`{类型}_{时间戳}.{格式}`

## 崩溃处理流程

```
检测崩溃 → 立即停所有自动化 → 保留现场截图/日志 → 
确认主.edb窗口 → 判断能否自动恢复 → 
如不能则重启 EPS → 归档本次报告
```

## 联系方式

- 主维护者：openclawzeng（曾玮）
- 技术开发：peiqian agent
