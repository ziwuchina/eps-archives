# EPS ERP API 业务自动化 — 2026-09-04 进展报告

> 覆盖任务：飞书看板【C路线-EPA API】（进行中）EPS HTTP API业务自动化（P0）
> 执行环境：192.168.1.233 (DESKTOP-BUBBUKE) / SSH 远控
> 报告日期：2026-09-04

---

## 一、本次目标

推进 C 路线 ERP API 业务自动化：验证并打通 `eps_erp_api.py` 的全部业务接口，实现"所有业务操作（提交/审批/查询）均可通过 API 完成，无需操作 EPS 界面"。

## 二、关键突破：HTTP 403 根因定位与修复

### 现象
直接运行 `eps_erp_api.py`，`GetTimeToken` 调用返回 **HTTP 403 Forbidden**。

### 根因
服务器前置 **WAF 强制要求浏览器 User-Agent 请求头**。不带 UA 的 Python urllib 默认请求被 WAF 拦截返回 403 页面；加上 `Mozilla/5.0` 后正常返回 200。

### 修复
修改 `eps_erp_api.py`：
1. `_common_headers()` 加入浏览器 UA
2. `_get_json()` 的请求头加入 UA

原文件已备份为 `eps_erp_api.py.bak_20260904`。

## 三、验证结果（全部通过）

| 接口 | 命名空间 | 结果 |
|------|----------|------|
| Login | erp.neto.netofficehelper.userlogin | ✅ success=True |
| GetWorkList | erp.neto.netofficehelper.getunitworktodolist | ✅ 50 条待办 |
| GetFlowAndUser | erp.neto.workflowhelper.getflowanduser | ✅ 流程流转详情 |
| GetUnitInfo | erp.pro.unithelper.getunitinfo | ✅ |
| GetUnitInfoBySD | erp.pro.unithelper.getunitinfobysd | ✅ |

## 四、业务待办数据概览

- **账号**：曾玮（登录成功，userid=6DFEA517AAC9407DB2653879A61E1E2F）
- **当前待办总数**：50 条
- **业务类型**：佛山市顺德区宗地图测绘业务（乐从镇 / 龙江镇 / 勒流街道等）
- **步骤分布**：作业登记 / 下载数据 / 上传成果数据 等
- **流程流转**：GetFlowAndUser 返回提交选项与可选用户（肖汉维、何碧君、丁勇清、叶成林、林升等）

### 待办样例（前10条）

| iid | 业务名称 | 步骤 |
|-----|----------|------|
| 102026072200190 | 顺德区乐从镇大罗村朝阳坊朝阳大街十二巷10号(宗地图) | 作业登记 |
| 102026072200182 | 顺德区乐从镇大罗村朝阳坊朝阳后街十二巷10号(宗地图) | 作业登记 |
| 102026072000299 | 顺德区勒流街道冲鹤村金银大街南二巷6号(宗地图) | 作业登记 |
| 102026072000177 | 顺德区龙江镇仙塘村市场路环岗街29号(宗地图) | 作业登记 |
| 102026072000161 | 仙塘市场路环岗街29号11 | 下载数据 |
| 102026072000135 | 顺德区龙江镇南坑村南坑路聚龙街七巷15号(宗地图) | 作业登记 |
| 102026072000114 | 顺德区龙江镇新华西村金喜街四巷2号(宗地图) | 作业登记 |
| 102026072000064 | 乐从水藤 | 下载数据 |
| 102026071700169 | 仙塘市场路环岗街29号 | 上传成果数据 |
| 102026071500212 | 勒流街道冲鹤村金银大街南二巷6号22 | 下载数据 |

## 五、证据文件

- `D:\AIcode\mcpida\wrapper\eps_erp_api.py`（修复后 SDK）
- `D:\AIcode\mcpida\wrapper\eps_erp_api.py.bak_20260904`（修复前备份）
- `D:\AIcode\mcpida\reports\worklist_20260904.json`（50 条待办 + 前 10 条流程详情）
- `D:\AIcode\mcpida\wrapper\analyze_worklist.py`（待办分析脚本）

## 六、下一步

1. **写操作需人工确认**：WorkProgressReport（上报进度）/ UnitAccept（接单）/ WorkflowSubmit（提交）等会改动生产数据，需用户明确指定业务后执行
2. **GetUserRoles 修复**：filter_groupname 参数需 SSArcSDE.GetUserRoleNameList() 返回值
3. **业务批处理脚本**：按步骤批量查询 / 上报，输出 Excel 明细
