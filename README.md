# EPS 自动化项目 — 知识库总入口

> 存档仓库 / 知识库 / 交接文档。本仓库记录 EPS 自动化全量过程文档，不含敏感凭证。

---

## 📂 目录结构

```
eps-archives/
├── docs/
│   ├── daily-logs/          ← 裴谦每日工作日志（04-01 ~ 09-09）
│   ├── technical/           ← 核心技术文档（逆向/API 目录/字段字典）
│   └── amd-ai-eps-sync/     ← \\Amd\ai相关 共享盘 EPS 相关内容精选归档（2026-09-09）
├── reports/                 ← 进展报告 + 阶段报告 + 证据 JSON
│   └── dm-status/           ← DM 状态结构化记录
├── tools/                   ← 可复用工具/复现脚本
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
| [2026-09-04](docs/daily-logs/2026-09-04.md) | C路线ERP API业务自动化：HTTP 403根因修复（User-Agent）/ 只读接口全验证通过 / 50条待办盘点 |
| [2026-09-05](docs/daily-logs/2026-09-05.md) | 任务重启分析 / 官方 COM 通道确认（Eps.EpsApplication→GetScriptDispatch） |
| [2026-09-08](docs/daily-logs/2026-09-08.md) | **COM 生产化落地**：ASCII 工作副本方案 / 12 宗地多坐标绘制录入 / 属性导出 / 性能优化（1.8~2.6x）/ 进程治理 |
| [2026-09-09](docs/daily-logs/2026-09-09.md) | 步骤2.4 调用链闭环 / 阶段3.1 函数批量分析 254 函数 / WzExtBridge 静态验证 / ScriptCryptor 机制破解 / 看板治理 / 共享盘归档 / git 同步 |

---

## 🔬 核心技术文档

### 逆向工程（2026-03~04）

| 文件 | 说明 |
|---|---|
| `re_sserptools_v2.md` | SSERPTools.dll 逆向报告（v2） |
| `re_ssmap_v2_summary_clean.md` | SSMap.dll 逆向摘要 |
| `eps_sscore32_signatures.md` | SSCore32.dll 符号表 |
| `eps_sserptools_signatures.md` | SSERPTools.dll 符号表 |
| `eps_source_pass.md` | 源码重建 Pass 总述（17 轮） |
| `eps_sdl_flow_pass4.md` | SDL 加载全链路分析（Pass 4） |
| `eps_v23_command_mapping.json` | v23 BAR 命令 ID → 功能映射 |
| `eps_v23_whitelist_report.json` | v23 白名单验证报告 |

### COM 生产化与宗地自动化（2026-09-08，已落地）

| 文件 | 说明 |
|---|---|
| `宗地绘制清单_20260908.csv` | 12 宗地 4×3 网格坐标清单（ZDMJ=10000.0） |
| `宗地属性导出_全字段/有效字段_20260908.csv` | 41 行×122 字段 / 34 有效字段（含 ID0 基线） |
| `ZD_宗地基本信息属性表_字段字典.csv` | 328 行字段字典（97 专属+231 公共，53 字典规则） |
| `reports/宗地绘制录入_坐标核验总报告_20260908.md` | 绘制证据链（12/12 逐点匹配、0 重叠） |
| `reports/优化对比报告_单会话轮询_20260908.md` | 单会话轮询 22.7s vs 旧版 40.5~58s（1.8~2.6x） |
| `reports/EPS会话自动清理_交付说明_20260908.md` | eps_com_runner.run_and_clean 进程治理 |

### 逆向审计（2026-09-09）

| 文件 | 说明 |
|---|---|
| `reports/步骤2.4_调用链闭环_静态反汇编报告_20260909.md` | SSProject.dll ExecuteSDLCommand → IsRegisterCmd → vtable[0x40]（无 ASLR 对齐） |
| `reports/阶段3.1_函数批量分析_批1~10_20260909.md` + `stage31_batch*.json` | 官方函数 254 个全量分析（SSProcess 174 覆盖 + 小类 80） |
| `reports/WzExtBridge_调用链验证_静态报告_20260909.md` | WzExtBridge.SDL=PE 模块，WzExtProbe 3 参签名匹配 |
| `reports/ScriptCryptor_加密授权体系_梳理报告_20260909.md` | PiEncrypt+OpenSSL 加密链 + License 格式 + HASP 狗 |

### VBS 脚本 / API 目录

| 文件 | 说明 |
|---|---|
| `eps_api_catalog.csv` + `EPS2016_脚本API目录.xlsx` | CHM 611 页解析，460+ 签名方法 |
| `eps_vbs_classification.json` | VBS 脚本全量分类（2.1MB） |
| `eps_dynamic_verification.md` | 动态验证报告 |

### 共享盘归档（2026-09-09，`\\Amd\ai相关` 精选）

| 文件 | 说明 |
|---|---|
| `docs/amd-ai-eps-sync/README-汇总总结.md` | 盘点 42 条目 / 筛选标准 / 敏感排除清单 |
| `docs/amd-ai-eps-sync/eps-vbs-knowledge/` | EPS VBS API 参考手册（含调用统计）/ 加密解密分析 / 官方脚本文档 |
| `docs/amd-ai-eps-sync/dog-bridge/` | 顺德佛山双狗互通档案（2026-09-19 状态✅）+ EDB 转换器 |
| `docs/amd-ai-eps-sync/tools/` | WzExtBridge.cpp 源码 / eps_erp_api.py / 验证脚本 |

---

## ⚠️ 避坑总则（必读）

> 04-01~04-10 教训 + 2026-09 生产化/逆向实测补充

1. **`ret=0` ≠ 成功** — 必须同时验证：① COM 返回 ② EPS 主进程存在 ③ EDB 时间戳 / SQL 回读
2. **无 `.edb` 窗口时禁止发自动化命令** — 会命中后台残留进程，虚假成功
3. **禁止用坐标点击作为主路径** — 换机器/分辨率必失效（官方 COM 通道替代）
4. **IDA调试模式下执行VBS会崩溃** — 验证环节必须用独立（非调试）实例
5. **Hook断点过多会导致EPS卡死** — 单次安全回放 > 批量候选试探
6. **SDL加载失败弹窗** — 根因是命令加了 `$epsscript,` 前缀，去掉即可
7. **多EPS孤儿进程** — 每次自动化后必须 `tasklist | findstr Eps` 核验
8. **EPS 会话必须走 `eps_com_runner.run_and_clean()`** — EPS 为 out-of-proc COM，客户端断开不自动释放，裸跑 VBS 必留孤儿进程
9. **读属性走 SQL** — `GetObjectAttr`/`GetSelGeoValue` 实测 err=450 不可用；`SELECT *` 可用
10. **`GetObjectPoint` 首参是 geoID**（传 handle 静默返回全 0）；`GetSelGeoPointCount` 首参是**选择集 index**
11. **VBS 挂住时先查落盘输出再清进程** — EPS 调用可能已成功（cscript 收尾超时 ≠ 失败）
12. **SDL 插件文件可能是 PE 伪装** — WzExtBridge.SDL 实为 PE 模块（MZ 头），按导出表解析而非文本

详见 [REPORTS-AND-KNOWLEDGE.md](REPORTS-AND-KNOWLEDGE.md) 避坑章节。

---

## 🏗️ 关键系统路径（参考）

```
EPS主程序:     D:\EPS2026G\Eps.exe
SSERPTools:    D:\EPS2026G\SSERPTools.exe
EPS2016Shunde: D:\EPS2016Shunde\（模板/加密狗/SCRIPT/脚本工具）
IDA MCP端口:   127.0.0.1:11339 (默认) / 10000 (调试实例)
裴谦工作区:    C:\Users\Administrator\.openclaw\workspace-peiqian
EPS技能:       C:\Users\Administrator\.openclaw\skills\eps-workspace-control\scripts\eps_session_command.ps1
共享盘:        \\Amd\ai相关（EPS 相关内容已精选归档至 docs/amd-ai-eps-sync/）
```

---

*本文件由 openclawzeng 更新于 2026-09-09*
