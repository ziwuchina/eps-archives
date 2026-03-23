# EPS 逆向工程分析存档

私有存档，曾玮私人使用。

## 目录结构

```
eps-archives/
├── README.md                          # 本文件
├── 2026-03-18.md                     # 每日记忆日志
├── 2026-03-19.md
├── 2026-03-20.md
├── 2026-03-21.md
├── 2026-03-22.md
├── 2026-03-23.md                     # 主日志（最详细）
├── 2026-03-23_addendum.md            # 补充记录
├── 2026-03-23-ida-mcp-guide.md      # IDA MCP使用指南
└── reports-2026-03-23/               # 分析报告
    ├── eps_architecture_master_2026-03-23.md   # 总架构图
    ├── eps_dispatch_chain_2026-03-23.md       # 命令分发链
    ├── eps_workflow_commands_2026-03-23.md     # 工作流命令
    ├── batch6_db_stack_2026-03-23.md          # 数据库栈
    ├── batch7_main_geometry_2026-03-23.md   # 主程序/几何
    ├── hasp_sspipe_analysis_2026-03-23.md    # HASP狗+管线
    ├── sscript_analysis_2026-03-23.md         # SDL脚本引擎
    ├── sscriptcore_com_pipeline_2026-03-23.md # COM脚本管道
    └── [其他报告...]                           # 39份分析报告
```

## 内容概要

| 日期 | 内容 |
|------|------|
| 2026-03-18 | EPS IDA MCP首次搭建，开始DLL分析 |
| 2026-03-19 | 继续DLL批量分析 |
| 2026-03-20 | EPS2026G深入逆向，HASP/登录链 |
| 2026-03-21 | ArcGIS服务器发现，Fiddler抓包 |
| 2026-03-22 | SSWEBGIS Web应用分析 |
| 2026-03-23 | ** IDA MCP全开，21个DLL并行分析， SDL脚本/VBScript引擎破译，数据库栈全链路 |

## 关键发现摘要

- **HASP狗**: regcode=54390，USB本地验证，无网络狗功能
- **SDL脚本**: VBScript COM引擎，HTTP请求在.sdl脚本中构建
- **数据库**: DAO/ADO双路径，platform.mdb本地MDB，无网络代理
- **ArcGIS**: 218.104.177.240，JK101/JK102空间查询
- **SSERPTools**: 命令路由，ssExcuteFunction动态加载脚本
- **SScriptCore**: ScriptEngineFactory COM组件
- **SuperMapX**: 4205函数SuperMap GIS引擎

---
*由 OpenClawZeng 自动存档*
