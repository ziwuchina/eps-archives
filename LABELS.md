# 🏷️ 标签体系

## 状态标签

| 标签 | 颜色 | 说明 |
|---|---|---|
| `status:blocked` | 🔴 红色 | 完全阻塞，无法推进 |
| `status:in-progress` | 🟡 黄色 | 正在进行中 |
| `status:review` | 🔵 蓝色 | 待 review / 待验收 |
| `status:done` | 🟢 绿色 | 已完成 |
| `status:stale` | ⚫ 灰色 | 长期无更新 |

## 类型标签

| 标签 | 颜色 | 说明 |
|---|---|---|
| `bug` | 红色 | Bug 报告 |
| `enhancement` | 绿色 | 功能改进 |
| `eps-specific` | 紫色 | EPS 自动化专项 |
| `ida-mcp` | 蓝色 | IDA MCP 相关 |
| `vbs-script` | 橙色 | VBS 脚本相关 |
| `frida-hook` | 粉色 | Frida Hook 相关 |
| `wm-command` | 青色 | WM_COMMAND 抓包相关 |
| `popup-dialog` | 黄色 | 弹窗处理相关 |
| `documentation` | 灰色 | 文档相关 |
| `security` | 红色 | 安全相关 |

## 优先级标签

| 标签 | 颜色 | 说明 |
|---|---|---|
| `priority:critical` | ⚫ 黑色 | 必须立即处理（P0） |
| `priority:high` | 🔴 红色 | 高优先级（P1） |
| `priority:medium` | 🟡 黄色 | 中优先级（P2） |
| `priority:low` | 🟢 绿色 | 低优先级（P3） |

## 避坑标签

| 标签 | 颜色 | 说明 |
|---|---|---|
| `pitfall` | ⚠️ 橙色 | 历史教训，已知风险点 |
| `no-coord-click` | 🔒 紫色 | 禁止使用坐标点击 |
| `three-evidence` | 📋 蓝色 | 需要三证合一验收 |
