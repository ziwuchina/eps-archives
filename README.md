# EPS 自动化项目 — 知识库总入口

> 存档仓库 / 知识库 / 交接文档。本仓库记录 EPS 自动化全量过程文档，不含敏感凭证。

---

## 📂 目录结构

```
eps-archives/
├── docs/
│   ├── daily-logs/          ← 裴谦每日工作日志（04-01 ~ 04-10）
│   └── technical/           ← 核心技术文档
├── reports/
│   └── dm-status/           ← DM 状态结构化记录
├── .github/
│   ├── workflows/           ← CI 配置
│   ├── ISSUE_TEMPLATE/      ← Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md
├── LABELS.md
├── SECURITY.md
└── REPORTS-AND-KNOWLEDGE.md
```

---

## 📅 每日工作日志（裴谦）

| 日期 | 主要工作 |
|---|---|
| [2026-04-01](docs/daily-logs/2026-04-01.md) | 接棒启动 / Feishu线程绑定问题收口 / EPS DLL封装完成 |
| [2026-04-02](docs/daily-logs/2026-04-02.md) | 监督体制建立 / cron 30min督办 / Tavily搜索接入 |
| [2026-04-03](docs/daily-logs/2026-04-03.md) | EPS Workspace Control Skill落地 / IDA MCP固化 / 飞书文档写入 |
| [2026-04-04](docs/daily-logs/2026-04-04.md) | Frida Hook AddClipBoardObjToMap打通 / 零点击触发原型 / 自动化导致EPS崩溃（教训） |
| [2026-04-05](docs/daily-logs/2026-04-05.md) | 工具拉起验证（qclaw/workbuddy/trae）/ 模型重复回复问题定位 |
| [2026-04-06](docs/daily-logs/2026-04-06.md) | 会话超时恢复 / IDA MCP重启方案 |
| [2026-04-07](docs/daily-logs/2026-04-07.md) | EPS弹窗监控 / 自动化仪表盘上线 |
| [2026-04-08](docs/daily-logs/2026-04-08.md) | EPS监控Phase2 / VBS脚本29/29批跑通过 / EPS导出链路 |
| [2026-04-09](docs/daily-logs/2026-04-09.md) | IDA MCP F9联动 / WM_COMMAND抓包 / button_id=1确认 / 多次崩溃教训 |
| [2026-04-10](docs/daily-logs/2026-04-10.md) | Frida SendMessageW hook / IDA实例端口确认 / WM_COMMAND批量捕获 |

---

## 🔬 核心技术文档

### 逆向工程

| 文件 | 说明 |
|---|---|
| `re_sserptools_v2.md` | SSERPTools.dll 逆向报告（v2） |
| `re_ssmap_v2_summary_clean.md` | SSMap.dll 逆向摘要 |
| `eps_sscore32_signatures.md` | SSCore32.dll 符号表 |
| `eps_sserptools_signatures.md` | SSERPTools.dll 符号表 |

### SDL 加载流程

| 文件 | 说明 |
|---|---|
| `eps_sdl_flow_pass4.md` | SDL 加载全链路分析（Pass 4） |

### VBS 脚本

| 文件 | 说明 |
|---|---|
| `eps_vbs_classification.json` | VBS 脚本全量分类（2.1MB） |
| `eps_safe_addclip_replay_runbook.md` | 安全回放执行手册（AddClipBoardObjToMap 专用） |
| `eps_dynamic_verification.md` | 动态验证报告 |

### BAR / 命令映射

| 文件 | 说明 |
|---|---|
| `eps_v23_command_mapping.json` | v23 BAR 命令 ID → 功能映射 |
| `eps_v23_whitelist_report.json` | v23 白名单验证报告 |

### 源码重建

| 文件 | 说明 |
|---|---|
| `eps_source_pass.md` | 源码重建 Pass 总述 |
| `eps_source_reconstruction_pass*.md` | 各轮重建细节（共17轮） |

### IDA 调试

| 文件 | 说明 |
|---|---|
| `ida_dbg_events_summary.json` | IDA 调试事件汇总 |
| `ida_capture_after_exec_*.json` | F9执行后捕获记录 |
| `f9_capture_F9CAP_*.json` | F9连续捕获 |

### WM_COMMAND 抓包

| 文件 | 说明 |
|---|---|
| `ida_wm_command_capture_*.json` | WM_COMMAND 抓包原始数据 |
| `eps_f9_hook_F9MCP_*.json` | F9 + MCP 联动事件 |

---

## ⚠️ 避坑总则（必读）

> 来自 04-01~04-10 全部教训的精华提炼

1. **`ret=0` ≠ 成功** — 必须同时验证：① COM返回 ② EPS主进程存在 ③ EDB时间戳
2. **无 `.edb` 窗口时禁止发自动化命令** — 会命中后台残留进程，虚假成功
3. **禁止用坐标点击作为主路径** — 换机器/分辨率必失效
4. **IDA调试模式下执行VBS会崩溃** — 验证环节必须用独立（非调试）实例
5. **Hook断点过多会导致EPS卡死** — 单次安全回放 > 批量候选试探
6. **SDL加载失败弹窗** — 根因是命令加了 `$epsscript,` 前缀，去掉即可
7. **多EPS孤儿进程** — 每次自动化后必须 `tasklist | findstr Eps` 核验

详见 [REPORTS-AND-KNOWLEDGE.md](REPORTS-AND-KNOWLEDGE.md) 避坑章节。

---

## 🏗️ 关键系统路径（参考）

```
EPS主程序:     D:\EPS2026G\Eps.exe
SSERPTools:    D:\EPS2026G\SSERPTools.exe
IDA MCP端口:   127.0.0.1:11339 (默认) / 10000 (调试实例)
裴谦工作区:    C:\Users\Administrator\.openclaw\workspace-peiqian
IDA MCP工具:   C:\Users\Administrator\.openclaw\skills\desktop-tool-launcher-mvp\scripts\mcp_ida.ps1
EPS技能:       C:\Users\Administrator\.openclaw\skills\eps-workspace-control\scripts\eps_session_command.ps1
IDA别名:       ida-mcp -> http://127.0.0.1:11339/mcp
IDA MCP配置:   C:\Users\Administrator\.mcporter\mcporter.json
```

---

*本文件由 openclawzeng 自动生成于 2026-04-10*
