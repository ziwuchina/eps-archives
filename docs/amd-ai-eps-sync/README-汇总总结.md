# \\Amd\ai相关 — EPS 相关内容盘点、筛选与归档汇总（2026-09-09）

> 本目录为共享盘 `\\Amd\ai相关` 中与 **EPS 自动化/逆向/测绘** 项目相关内容的**盘点与精选归档**。
> 归档原则：只收录与 EPS 主线相关、当前仍具参考价值的非敏感内容；凭据、隐私、大体积低增量、过期探测脚本一律排除。

## 一、共享盘全景盘点（根目录 42 条目）

| 类别 | 条目 | 处置 |
|---|---|---|
| **EPS 核心** | `EPS-VBS知识库/`（13 文件+14 业务子目录）、`VBS解密工具/`、`EPS项目汇报/`（6 报告+Eps2016_exe 全量脚本+看板快照）、`AIbc/`（EPSre 空目录、EPS劫持 空目录）、`狗狗问题/`（双狗互通+EDB 转换） | ✅ 精选归档（见下） |
| EPS 根报告 | `EPS_VBS解密项目总结报告.md`、`EPS测绘工具箱_项目总结报告.txt`、`EPS逆向与自动化进展汇总.docx`、`顺德宗地号定位脚本_项目总结与复盘.md`、`篡改猴脚本关于EPS登录.txt` | ✅ 归档 |
| **敏感凭据** | `API KEY.txt`、`Cloudflare API.txt`、`AIcode_凭据清单.md`、`API密钥清单_测试报告.xlsx` | ⛔ **排除（凭据，绝不归档）** |
| **其他项目（与 EPS 无关）** | `DeepSeek助手/`、`wechattool/`、`oneplus5/`、`组合拳/`、`注册测绘师备考平台/`、`悬浮框/`、`aliddns/`、`olingai/`、`ox-alpha/`、`quarkclouddrive*`、`中国龙主题海报.pdf`、`OA*`、`SJLC*_detail.html`、`build_excel.py` | ⛔ 非 EPS，不归档 |
| **隐私/密钥目录** | `元衡中转站/`（tokens/cookies/localStorage/keys）、`局域网访问/`（id_ed25519_remote 私钥）、`freeapi/`（freellmapi-keys.json）、`ssh-nas-login/`（askpass） | ⛔ **排除（密钥/私钥/隐私）** |
| 无关数据 | `AIbc/`（OpenClaw/arcgis/money/shadu 等）、`oneplus5/`（手机 SSH） | ⛔ 排除 |

## 二、归档内容（39 文件 → `docs/amd-ai-eps-sync/`）

### 1. `eps-vbs-knowledge/`（10 文件）— EPS VBS 知识库核心
- `EPS_VBS_API参考手册.md`（128KB）：API 功能参考 + **调用次数统计**（如 SetDataXParameter 237,145 次/681 文件），与 `eps_api_catalog.csv` 互补
- `EPS_VBS加密解密分析报告.md`、`EPS-VBS功能模式归纳报告.md`、`EPS-VBS网络服务器深度分析报告.md`、`EPS扩展性深度分析报告.md`、`EPS深度分析报告.md`、`_深度分析报告.md`、`_INDEX.md`（482KB 索引）
- `EpsScript_content.txt`（295KB）+ `EpsScript.doc`（4MB 官方脚本文档）

### 2. `vbs-decrypt/`（2 文件）— VBS 解密工具
- `README.md` + `action_build_include.bat`（构建封装）；`output/` 解密产物因含业务内容不归档

### 3. `dog-bridge/`（8 文件）— 顺德/佛山双狗互通 + EDB 转换档案（2026-08~09，时效高）
- `顺德佛山双狗数据互通_当前状态总结_20260919.md`（✅ 一切正常，用户确认）
- `顺德佛山双狗数据互通_全项目详细总结.md`、`EPS双狗互通与时间锁_完整技术档案_20260828.md`、`加密狗研究总结报告.md`
- EDB 转换 3 报告（研究进展/部署说明/最终报告）+ `EDBConvert.spec`

### 4. `reports/`（11 文件）— 项目总结与汇报
- 根目录 5 份：解密总结/测绘工具箱/逆向进展汇总.docx/宗地号定位/登录脚本
- EPS项目汇报 6 份：ERP API 进展（20260904）/逆向自动化汇总（20260828）/任务交接（20260908）/重启分析（20260904）/详细总结（20260811）/核实复盘（20260811）

### 5. `tools/`（8 文件）— 精选可复用工具
- `WzExtBridge.cpp`（21KB **外部模块源码**，与已验证的 WzExtBridge.SDL 对应）
- `eps_erp_api.py`（ERP HTTP SDK）、`eps_command_bridge.py`、`export_kanban.py`、`verify_actual.py`/`verify_done_tasks.py`/`verify_wzb.py`、`裴谦-任务看板.xlsx`

## 三、时效性与可行性评估

| 内容 | 时效 | 可行性/价值 |
|---|---|---|
| 双狗互通档案（2026-09-19 状态✅） | ✅ 最新 | 加密因子+EDBConvert 全链路，可直接复用于数据互通 |
| EPS_VBS_API参考手册 | ✅ 长期有效 | 调用统计揭示高频 API，指导自动化选型 |
| WzExtBridge.cpp 源码 | ✅ 与 2026-04-12 编译产物对应 | 外部模块开发蓝本（签名已验证） |
| 项目总结/复盘报告（20260811~0908） | ✅ 已归档主线一致 | 知识沉淀 |
| 宗地号定位脚本复盘 | ✅ 与宗地主线相关 | 坐标定位逻辑参考 |
| 看板快照（kanban_*/tblX*.ndjson 多副本） | ❌ 过期 | 仓库已有最新版，不归档 |
| 一次性探测脚本（check_*/test_*/frida_* 数十个） | ❌ 一次性 | 多为实验残件，不归档 |
| bmp 截图（menu_dump/screen_full 等 8MB×4） | ❌ 过期 | 体积大无增量，不归档 |
| `AIbc/EPSre`、`AIbc/EPS劫持` | ❌ 空目录 | 无内容 |

## 四、明确排除清单（不归档原因）

| 文件/目录 | 原因 |
|---|---|
| `API KEY.txt` / `Cloudflare API.txt` / `AIcode_凭据清单.md` / `API密钥清单_测试报告.xlsx` | API 凭据 |
| `元衡中转站/`（tokens.json/cookies.json/localStorage.json/extracted_keys.txt/test_token_key.txt 等） | 第三方平台密钥/会话 |
| `局域网访问/id_ed25519_remote` | SSH 私钥 |
| `freeapi/freellmapi-keys.json`、`ssh-nas-login/`（askpass/凭据） | 密钥/认证 |
| `wechattool/`（wechat-decrypt 等）、`peiqian_chat/`（对话记录 txt） | 隐私数据 |
| `worklist_20260904.json/.xlsx` | 业务待办数据（非知识） |
| `EpsGlobal.ini/EpsUser.xml/EpsLocal.xml` | 本机路径/用户配置 |
| `狗狗问题/禁止改时间/`、`时间守护/` | 授权时间锁规避工具（不归档） |
| 各业务子目录（三维测图/佛山基础地形测绘/南海农房/房地一体 等） | 业务数据/模板，非逆向知识 |

## 五、归档结构与复现

- 归档位置：`docs/amd-ai-eps-sync/`（与仓库既有 `docs/technical`、`reports` 并列）
- 来源：`\\Amd\ai相关`（网络共享，只读引用）；全部文件为复制件，原文件未改动
- 本次提交：39 文件（含 EpsScript.doc 4MB / API参考手册 128KB 等高价值文档）
