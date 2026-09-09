# 🎯 EPS 自动化项目贡献指南

## 项目定位

`eps-archives` 是 EPS（地籍测量软件）自动化项目的知识库与存档仓库。
核心目标是实现 **EPS 操作的无人值守自动化**，包括：

1. **官方 COM 通道生产化（主攻方向，已落地）** — `Eps.EpsApplication → GetScriptDispatch → SSProcess`，绘制/录入/导出全链路
2. **逆向文档体系化** — CHM 官方文档解析（611 页）+ DLL 静态反汇编 + API 目录
3. **VBS 脚本执行** — 通过 COM 接口触发 EPS 内部 VBS 脚本（官方通道，非命令框注入）
4. **弹窗治理** — 自动识别和处理 EPS 运行时弹窗
5. **数据导出** — EDB 数据批量导出与结构化处理（读属性走 SQL）

历史路线（IDA 调试联动 / BAR WM_COMMAND / 命令框注入）已被官方 COM 通道取代，相关结论保留在 reports 中归档。

## 工作流程原则

### 硬约束（绝对不允许绕过）

1. **官方 COM 通道优先**  
   所有自动化走 `Eps.EpsApplication` COM 通道；命令框注入 / HIDDEN Edit / SendInput 路径已废弃

2. **`.edb` 主窗口存在才执行**  
   任何 EPS 操作前必须确认主 `.edb` 窗口在线

3. **三证合一才算成功**  
   - COM 返回 `ret=0`
   - EPS 主进程存在（`hung=False`）
   - EDB 文件修改时间戳更新 / SQL 回读数据一致

4. **不盲发命令**  
   每条自动化命令后必须等待 + 观察 + 判窗，再发下一条

5. **EPS 会话必须走 `eps_com_runner.run_and_clean()`**  
   EPS 是 out-of-proc COM 服务器，客户端断开不自动释放；裸跑 VBS 必留孤儿进程。快照→执行→只清本次新增实例

6. **读属性走 SQL，不走 GetObjectAttr 族**  
   `GetObjectAttr`/`GetSelGeoValue` 实测报 err=450 不可用；`SELECT *` 可用

7. **坐标读取参数语义**  
   `GetObjectPoint` 首参是 **geoID**（传 handle 静默返回全 0）；`GetSelGeoPointCount` 首参是**选择集 index**——两者不同，勿混用

8. **VBS 挂住 ≠ 失败**  
   VBS 收尾超时但数据可能已落盘：先查输出/落盘结果，再清残留进程

9. **自动化操作后必须核验残留进程**  
   用 `tasklist | findstr Eps` 确认无孤儿进程

10. **不提交敏感内容**  
    凭据类文件（API KEY / 密钥 / tokens / cookies / SSH 私钥 / 对话记录）绝不进仓库，`git add` 前用 `git status` 核验

## 分支策略

```
master   ← 稳定归档，只接受 PR 合并
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
eps: 新增 EPS COM 生产化闭环（宗地绘制+属性录入）
docs: 更新 README / 归档共享盘 EPS 内容
```

## 代码风格

- PowerShell 脚本：遵循 [PoshCode](https://github.com/PoshCode/PowerShell-practice-and-style)
- Python：遵循 [PEP 8](https://pep8.org/)
- 文件编码：**UTF-8**（无 BOM）

## 报告与证据规范

所有自动化执行必须附带证据（脚本 + JSON 报告 + 实测输出），证据存放路径：

```
D:\AIcode\mcpida\reports\          ← 裴谦工作区（报告 + 证据 JSON）
D:\AIcode\mcpida\deliverables\     ← 交付物（CSV/XLSX）
C:\Users\Administrator\Desktop\AI_Documents\EPS\  ← 2026-09 逆向/看板工作目录
```

证据文件命名：`{类型}_{时间戳}.{格式}`；写入看板必须回读验证（written ≠ verified）。

## 崩溃处理流程

```
检测崩溃 → 立即停所有自动化 → 保留现场截图/日志 → 
确认主.edb窗口 → 判断能否自动恢复 → 
如不能则重启 EPS → 归档本次报告
```

## 联系方式

- 主维护者：openclawzeng（曾玮）
- 技术开发：peiqian agent
