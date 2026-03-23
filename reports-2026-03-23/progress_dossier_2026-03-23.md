# 3/18-3/23 进度总台账（持续推进版）

生成时间：2026-03-23 02:55:41

## 文件汇总

- .json: 169 个
- .md: 272 个
- .py: 494 个
- .txt: 48 个

- 详细索引：`reports/file_index_2026-03-23.json`

## 已验证成功过程

- IDA-MCP 直连模式稳定：initialize + mcp-session-id + /mcp SSE
- 四实例并行完成（Eps.exe, SSCore32.dll, SSMap.dll, SScript.dll）
- EPS 登录自动化打通：loginERP + 状态栏可见成功标志
- ODBC 直读 EDB 打通：佛山/顺德/当前库可读，能查 GeoPoint/GeoLine/GeoArea/FeatureCode 表
- 网络架构确认：WinInet + langem14x/EpsService + LiveUpdate 机制

## 尚未完成/进行中

- SScriptCore.dll 中 loginERP 实际实现函数定位（进行中）
- 177030-099 在具体 EDB 表中的定位（当前样本库未命中）
- Eps.exe 新开 IDB 自动分析完成后补全 loginERP 在主程序侧调用链

## 关键成果文件

- `reports\ida_mcp_eps_alltools.md`
- `reports\ida_mcp_sscore_alltools.md`
- `reports\ida_mcp_ssmap_alltools.md`
- `reports\ida_mcp_sscript_alltools.md`
- `reports\sscript_sdl_deep_analysis.md`
- `reports\sscore_login_chain.md`
- `reports\eps_network_analysis.md`
- `reports\foshan_data_search.md`
- `memory\2026-03-23-ida-mcp-guide.md`

## 最近更新文件（Top 50）

- `temp_check_structure.py` | 2026-03-23 02:55:40 | 2110 bytes
- `sscore_login_search_results.json` | 2026-03-23 02:55:32 | 166 bytes
- `build_master_dossier.py` | 2026-03-23 02:55:30 | 4085 bytes
- `temp_search_sscore.py` | 2026-03-23 02:55:29 | 4231 bytes
- `login_search_results.json` | 2026-03-23 02:55:16 | 71 bytes
- `temp_search_login.py` | 2026-03-23 02:55:08 | 3494 bytes
- `temp_check_ports.py` | 2026-03-23 02:54:46 | 1802 bytes
- `memory\2026-03-23.md` | 2026-03-23 02:53:57 | 5395 bytes
- `search_177.py` | 2026-03-23 02:50:17 | 1876 bytes
- `search_shunde_edb.py` | 2026-03-23 02:49:18 | 1872 bytes
- `search_foshan_edb.py` | 2026-03-23 02:49:02 | 1656 bytes
- `read_foshan_edb.py` | 2026-03-23 02:48:28 | 2228 bytes
- `reports\sscript_sdl_deep_analysis.json` | 2026-03-23 02:47:21 | 10817 bytes
- `reports\sscore_login_chain.md` | 2026-03-23 02:46:41 | 9672 bytes
- `reports\eps_login_verify.md` | 2026-03-23 02:46:40 | 3714 bytes
- `reports\sscript_sdl_deep_analysis.md` | 2026-03-23 02:46:19 | 16588 bytes
- `check_foshan_edb.py` | 2026-03-23 02:45:01 | 932 bytes
- `sscore_login_search.py` | 2026-03-23 02:44:35 | 3692 bytes
- `check_ida_status.py` | 2026-03-23 02:42:54 | 2012 bytes
- `find_loginERP_chain.py` | 2026-03-23 02:42:36 | 3577 bytes
- `sscript_step4.py` | 2026-03-23 02:42:11 | 3949 bytes
- `reports\eps_network_analysis.md` | 2026-03-23 02:41:46 | 6806 bytes
- `search_ip.py` | 2026-03-23 02:40:54 | 3292 bytes
- `read_edb_current.py` | 2026-03-23 02:40:38 | 779 bytes
- `reports\sscript_key_functions.json` | 2026-03-23 02:40:31 | 983235 bytes
- `search_network7.py` | 2026-03-23 02:40:28 | 4751 bytes
- `sscript_step3.py` | 2026-03-23 02:40:14 | 4245 bytes
- `search_network6.py` | 2026-03-23 02:39:57 | 3427 bytes
- `reports\sscript_sdl_strings.json` | 2026-03-23 02:39:42 | 43242 bytes
- `eps_find_login.py` | 2026-03-23 02:39:41 | 13885 bytes
- `sscript_step2.py` | 2026-03-23 02:39:31 | 3206 bytes
- `search_network5.py` | 2026-03-23 02:39:30 | 3631 bytes
- `reports\foshan_data_search.md` | 2026-03-23 02:39:10 | 4600 bytes
- `search_network4.py` | 2026-03-23 02:39:09 | 4566 bytes
- `reports\sscript_sdl_funcs.json` | 2026-03-23 02:39:05 | 21085 bytes
- `sscript_step1.py` | 2026-03-23 02:38:53 | 3582 bytes
- `eps_login_verify.py` | 2026-03-23 02:38:43 | 11743 bytes
- `search_network3.py` | 2026-03-23 02:38:43 | 2902 bytes
- `search_network2.py` | 2026-03-23 02:38:25 | 2006 bytes
- `search_network.py` | 2026-03-23 02:38:11 | 1052 bytes
- `analyze_commands.py` | 2026-03-23 02:38:06 | 1485 bytes
- `debug_ida.py` | 2026-03-23 02:38:01 | 374 bytes
- `reports\sscript_all_functions.json` | 2026-03-23 02:37:24 | 2 bytes
- `reports\sscript_decompilation.json` | 2026-03-23 02:37:24 | 2 bytes
- `reports\sscript_strings.json` | 2026-03-23 02:37:24 | 41 bytes
- `reports\sscript_xrefs.json` | 2026-03-23 02:37:24 | 2 bytes
- `sscript_sdl_deep_analysis.py` | 2026-03-23 02:37:16 | 8989 bytes
- `TOOLS.md` | 2026-03-23 02:26:52 | 3203 bytes
- `MEMORY.md` | 2026-03-23 02:25:56 | 10001 bytes
- `memory\2026-03-23-ida-mcp-guide.md` | 2026-03-23 02:25:37 | 9067 bytes

## 下一步执行队列（到08:00前持续）

1. 完成 SScriptCore.dll 三路并行结果汇总
2. 将 loginERP 命令链写入 `reports/loginERP_full_chain.md`
3. 对佛山数据 EDB 做按 code 范围扫描，定位 177xxx 及图幅映射
4. 汇总错误重试策略到 `reports/retry_playbook.md`