# EPS 项目任务重启分析报告 — 2026-09-04

> 数据来源：与裴谦的飞书聊天记录导出（192.168.1.233 上的 `C:\Users\Administrator\Desktop\AI_Documents\Feishu_chat_export\peiqian`，27 个 CSV，覆盖 2026-02-27 ~ 2026-06-12）
> 看板：飞书多维表格「裴谦-EPS任务看板」（23 条任务）
> 本报告：基于聊天内容详细分析 + 全部任务重启（已完成验证，其他重启）

---

## 一、聊天记录分析结论

### 1.1 项目时间线
| 阶段 | 时间 | 关键事件 |
|---|---|---|
| 环境搭建 | 2026-02~03 | OpenClaw 多 agent 环境、飞书通道、安卓/Ubuntu 设备 |
| A路线探索 | 2026-04-12~16 | VBS 自动化尝试，最终判定**不可行**（EPS 内部路由层丢弃 VBSExecute） |
| B路线逆向 | 2026-04-17~22 | Frida/Ghidra 工具链，命令分发链 `Edit→OnEpsCommand→OCB→EXECFN` 定位 |
| 看板建立 | 2026-05-07 | 裴谦要求更新飞书看板，API 服务恢复确认 |
| 停滞 | 2026-05-24 | 尝试"AI 自主点击检测"方向（截图+KIMI 解析），程序崩溃后项目停滞 |

### 1.2 关键结论（来自聊天与看板交叉验证）
- **A 路线（VBS 自动化）**：正式判定不可行（4 种命令格式全部被丢弃），证据完整
- **B 路线（逆向工程）**：阶段1~2 前半完成，命令分发链已稳定复现；阶段2 后半（RunScript 直调）受阻
- **C 路线（ERP HTTP API）**：2026-05-07 API 恢复后已验证，2026-09-04 修复 403 后全链路打通（50 条待办）
- **Frida 稳定性**：进程内 SendMessageW 方案已验证有效（P0 阻断解除）

---

## 二、任务重启方案与执行结果

### 2.1 已完成任务验证（7 条，全部通过）
逐一核对 233 上证据文件存在性，7 条已完成任务结论全部确认有效：
1. A路线步骤3（SDL/ERP链路可用）— `bar_v23_command_catalog.json` ✅
2. A/B分水岭（VBS不可行判定）— `frida_trace_vbs_args_20260414_205515.json` ✅
3. B阶段1（ExecuteFuction分析）— `probe_erp_login_v37_report.json` 等 ✅
4. 留档（ERP/网络结论）— 归档文件 ✅
5. B阶段2.1（链路稳定化）— `stage2_p0_21_*` 三份run ✅
6. B阶段2.2（真实UI入口）— `frida_wmcmd_context_probe.py` 等 ✅
7. Frida稳定性 — `frida_stable_full_probe.py` 等 ✅

### 2.2 重启任务（16 条，已全部更新为"进行中"）
- **A 路线 5 条**（步骤1/2/2a/2b/2c）：重启评审——维持不可行基线，需 EPS GUI 复核，投入转向 B/C 路线
- **B 路线阶段2**（SScriptCore/2.3/2.4）：重启推进，需启动 EPS + Frida 验证
- **B 路线阶段3/4**：重启领取，先并行做模块分析文档框架
- **C 路线 2 条**：重启继续，ERP API 已打通
- **WzExtBridge.dll 开发**：重启，**已部署 DLL 到 D:\EPS2026G\**
- **SDL 封装路线**：重启领取，优先改造 wzbridgeprobe.dll
- **command ID 捕获**：重启，需 EPS 启动后触发

### 2.3 本轮实际执行成果（2026-09-04）
1. **WzExtBridge.dll 部署**：源码确认在 `...\eps_dll\WzExtBridge\WzExtBridge.cpp`，编译产物（299KB）已复制到 `D:\EPS2026G\WzExtBridge.dll`
2. **C 路线 GetUserRoles 排查**：确认服务端 `NullReferenceException`（"方法出错:未将对象引用设置到对象的实例"），非参数问题，需 EPS 端 SSArcSDE 上下文，纯 HTTP API 无法独立调用 → 标记已知限制
3. **C 路线批处理脚本**：`batch_worklist.py` 拉取 50 条待办 + 业务详情/流程流转，生成 `worklist_detail_20260904.xlsx`（Excel 明细）
4. **看板全量更新**：7 条已验证 + 16 条已重启，状态与进展已回填

---

## 三、当前阻塞与下一步

### 3.1 需要 EPS GUI 环境（当前 233 上 EPS 未运行）
以下任务需启动 `D:\EPS2026G\Eps.exe` 后继续：
- B 路线阶段2（SScriptCore/2.3/2.4）逆向推进
- WzExtBridge.dll 加载验证（确认 auto-load）
- VBS 菜单 command ID 实时捕获（需触发「宗地默认信息填写」）
- SDL 封装路线验证

### 3.2 需要用户授权
- **C 路线写操作**（WorkProgressReport 上报 / UnitAccept 接单 / WorkflowSubmit 提交）会改动生产数据，需用户指定业务 iid 后执行
- **GetUserRoles**：确认是否需要 EPS 端配合或放弃该接口

### 3.3 建议优先级
1. **P0**：启动 EPS → 验证 WzExtBridge.dll 加载 + command ID 捕获（打通 SDL 封装路线前置）
2. **P0**：C 路线写操作小范围试点（用户指定 1 条待办做 WorkProgressReport）
3. **P1**：B 路线阶段2 重启（HIDDEN Edit 稳定路径 + CStringData 直调）
4. **P2**：阶段3/4 并行文档框架

---

## 四、证据文件
- `D:\AIcode\mcpida\wrapper\batch_worklist.py`（批处理脚本）
- `D:\AIcode\mcpida\reports\worklist_detail_20260904.xlsx`（50 条待办明细）
- `D:\AIcode\mcpida\wrapper\eps_erp_api.py`（修复后 SDK）
- `D:\EPS2026G\WzExtBridge.dll`（已部署）
- `C:\Users\Administrator\.openclaw\workspace\eps_dll\WzExtBridge\`（源码）
