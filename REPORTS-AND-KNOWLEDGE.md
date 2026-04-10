# EPS 自动化项目 — 状态记录（2026-04-01 ~ 2026-04-10）

> 接管模板数据来源。记录 main agent 与 peiqian agent 在此时间窗口内的所有私聊汇报。

## 数据文件索引

| 文件 | 说明 |
|---|---|
| `reports/dm-status/manifest.json` | 统计清单（扫描文件列表、记录数） |
| `reports/dm-status/main-status-records.json` | main agent 状态回报（87条） |
| `reports/dm-status/peiqian-status-records.json` | peiqian agent 状态回报（595条） |
| `reports/dm-status/main-all-records.json` | main agent 完整记录（含非状态类） |
| `reports/dm-status/peiqian-all-records.json` | peiqian agent 完整记录 |
| `reports/dm-status/dm-status-summary.md` | 人工可读摘要 |
| `tools/build_dm_status_report.py` | 汇报提取工具 |

## 关键成功状态（已验证可用）

### 1. EPS 工作空间启动
- 工具：`eps_session_command.ps1`
- 路径：`C:\Users\Administrator\.openclaw\skills\eps-workspace-control\scripts\eps_session_command.ps1`
- 动作：`login`、`logout`、登录后命令发送

### 2. IDA MCP 联动
- 路径：`C:\Users\Administrator\.openclaw\skills\desktop-tool-launcher-mvp\scripts\mcp_ida.ps1`
- 动作：`check`、`decompile`、`functions`、`instances`、`xrefs-from/to`、`metadata`
- IDA MCP 端口：默认 `11339`，当前被调实例使用 `10000`

### 3. EPS 命令输入定位
- 路径：`C:\Users\Administrator\.openclaw\skills\eps-workspace-control\scripts\find_eps_cmd_input.ps1`
- 功能：定位 EPS 命令输入框（不是工具栏编辑框，是底部"命令行窗口"）

### 4. 弹窗监控
- 工具：`eps_onecmd.py`（`D:\AIcode\mcpida\tools\eps_onecmd.py`）
- 功能：自动探测 EPS 弹窗并处理

### 5. VBS 脚本执行链路（COM）
- 稳定路径：`GetObject("Eps.EpsApplication") → RunScript`
- 工具：`run_vbs_mapmethod.py`（`D:\AIcode\mcpida\tools\run_vbs_mapmethod.py`）
- 成功前提：EPS 主.edb 窗口必须存在；纯后台 COM 调用会失败

## 关键失败状态（避坑记录）

### A. EPS 多实例残留
- **现象**：自动化操作后留下多个 EPS 孤儿进程（`Eps.exe` / `SSERPTools.exe`）
- **后果**：后续 COM 调用命中错误实例，命令"成功"但功能无效果
- **避坑**：每次自动化前先确认主 `.edb` 窗口；操作后用 `tasklist | findstr Eps` 核验

### B. IDA 调试下 EPS 崩溃
- **现象**：在 IDA 调试器里运行的 EPS 执行 VBS 时崩溃
- **根因**：调试模式下 EPS 内部状态不稳定
- **避坑**：调试环节用 IDA MCP `dbg_*`，但 VBS 执行链验证必须在独立（非调试）EPS 实例中

### C. 命令返回值假阳性
- **现象**：`MapMethod("RunScript")` 返回 `ret=0`，但功能未真正生效
- **根因**：无可见 `.edb` 窗口时 COM 调用命中后台残留进程
- **避坑**：必须同时检查三类证据——① COM 返回 ② EPS 主窗口存在 ③ EDB 文件修改时间戳

### D. 高频 Hook 导致 EPS 卡死
- **现象**：Frida hook 断点过多或候选列表过长时 EPS UI 无响应
- **根因**：UI 线程被阻塞或图面对象短时间堆叠
- **避坑**：单次安全回放 > 批量候选试探；监听以只读为主

### E. `ret=0` 不等于成功
- **现象**：脚本执行后返回 `ok:true`，但 EPS 闪退或功能无变化
- **根因**：延迟崩溃；或者命令被发到错误窗口
- **避坑**：必须等待 N 秒后检查 EPS 是否仍在运行（`hung=False`），才算完整成功

### F. 工具栏按钮点击坐标依赖
- **现象**：用坐标点击 BAR 按钮，换机器/换分辨率后失效
- **根因**：BCGPToolBar 按钮区域不标准，依赖坐标
- **避坑**：优先用命令注入（`WM_COMMAND`）或 COM 脚本直调

### G. 模型超时（`embedded run timeout`）
- **现象**：peiqian agent 队列堆积，连续超时，汇报延迟
- **根因**：会话过长 / 任务过载 / 模型限额耗尽
- **避坑**：单次任务控制在合理 Token 范围；及时开启新会话

### H. `SDL loading failed` 弹窗
- **现象**：命令路径错误导致 EPS 尝试把脚本名当 SDL 库加载
- **根因**：命令加了 `$epsscript,` 前缀导致走错通道
- **避坑**：去掉前缀，用裸命令直发

## PEIQIAN 主线进度（EPS 自动化）

| 日期 | 主线 | 状态 |
|---|---|---|
| 04-01 | 接棒 DLL 封装 | ✅ 完成 |
| 04-02 | 监督体制建立（cron 30min） | ✅ 完成 |
| 04-03 | Skill 落地（eps-workspace-control 等2个） | ✅ 完成 |
| 04-04 | Frida Hook 链路打通（`AddClipBoardObjToMap`） | ✅ 完成 |
| 04-04 | "零点击触发"原型验证 | ✅ 完成 |
| 04-04 | 自动化导致 EPS 多次崩溃（高风险路径） | ❌ 教训 |
| 04-05 | 工具拉起验证（qclaw/workbuddy/trae） | ✅ 完成 |
| 04-06 | 会话超时恢复机制 | ✅ 完成 |
| 04-08 | EPS 监控仪表盘上线 | ✅ 完成 |
| 04-08 | VBS 脚本 29/29 批跑通过 | ✅ 完成 |
| 04-08 | EPS 导出链路（VBS + COM）| ✅ 部分可用 |
| 04-09 | IDA MCP F9 联动（`dbg_continue`）| ✅ 完成 |
| 04-09 | WM_COMMAND 抓包（`button_id=1` = 宗地默认信息填写）| ✅ 完成 |
| 04-09 | 自动化把 EPS 打崩（多次 Application Error）| ❌ 教训 |
| 04-09 | 切到"只监听不执行"安全模式 | ✅ 收敛 |
| 04-10 | Frida `SendMessageW/PostMessageW` 进程内 hook | ✅ 进行中 |

## 文件绝对路径参考（生产环境）

```
EPS主程序:     D:\EPS2026G\Eps.exe
SSERPTools:    D:\EPS2026G\SSERPTools.exe
IDA MCP端口:   127.0.0.1:11339 (默认) / 10000 (当前实例)
IDA MCP工具:   C:\Users\Administrator\.openclaw\skills\desktop-tool-launcher-mvp\scripts\mcp_ida.ps1
EPS技能:       C:\Users\Administrator\.openclaw\skills\eps-workspace-control\scripts\eps_session_command.ps1
IDA MCP状态:   C:\Users\Administrator\.openclaw\skills\desktop-tool-launcher-mvp\scripts\mcp_status.ps1
裴谦工作区:    C:\Users\Administrator\.openclaw\workspace-peiqian
裴谦日报:      C:\Users\Administrator\.openclaw\workspace-peiqian\memory\2026-04-*.md
IDA会话日志:   C:\Users\Administrator\.openclaw\workspace-peiqian\reports\ida_dbg_events_live_*.json
IDA WM_COMMAND: D:\AIcode\mcpida\reports\ida_wm_command_*.json
VBS执行报告:   D:\AIcode\mcpida\reports\bar_unified_exec_*.json
批量测试结果:  D:\AIcode\mcpida\reports\script_runs\batch_*.json
EPS监控报告:   D:\AIcode\mcpida\reports\monitoring\monitor_eps_*.json
IDA事件日志:   D:\AIcode\mcpida\reports\ida_*.json
IDA MCP配置:   C:\Users\Administrator\.mcporter\mcporter.json
IDA别名:       ida-mcp -> http://127.0.0.1:11339/mcp
```

---
*本文件由 openclawzeng 自动生成，时间戳：2026-04-10T04:15:00+08:00*
