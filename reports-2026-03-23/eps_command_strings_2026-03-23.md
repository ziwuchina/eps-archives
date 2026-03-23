# EPS 命令字符串完整列表
**日期**: 2026-03-23
**模块**: SSERPTools.exe (端口12002)

---

## 已确认的命令字符串

| 命令字符串 | IDA地址 | 文件偏移 | 说明 |
|-----------|---------|---------|------|
| `WorkProgressReport` | 0x10049654 | 0x49654 | 工作进度上报 |
| `ProgressReportList` | 0x1004929c | 0x4929c | 进度上报列表 |
| `CancelAcceptWork` | 0x10049678 | 0x49678 | 取消接件 |
| `WorkSubmit` | 0x10049698 | 0x49698 | 提交工作 |
| `CheckRecordUpload` | 0x100496b0 | 0x496b0 | 检查记录上传 |
| `NewWork` | 0x1004909d | 0x4909d | 新建工作对话框 |

---

## EPS 脚本系统架构

```
用户界面 (SSERPTools.exe)
    ↓ 对话框操作
GetWorkInfo() / SetWorkInfo()
    ↓
CERPManager::GetToken() — 获取 ACCESS_TOKEN
    ↓
ssExcuteFunction("SScript", "ExecuteScript", "ERPManager", "ProgressReportList")
    ↓
AfxLoadLibrary("D:\EPS2026G\SScript.SDL")  ← SDL脚本（DLL格式）
    ↓
ExecuteScript(模块, 命令名, 参数...)
    ↓
脚本中组装 HTTP 请求
    ↓
MFC CInternetSession → POST erp.gis.arcgisserverhelper
```

---

## 53个SDL脚本文件

| 脚本 | 大小 | 用途推测 |
|------|------|---------|
| SSSuperMapUpdate.sdl | 2.7MB | 超图数据库更新 |
| SSCommTools.SDL | 1.1MB | 通用工具 |
| ToolsGz.SDL | 1.0MB | 广州工具 |
| SSynthesizer.SDL | 1.4MB | 综合工具 |
| SSGeoProcess.sdl | 467KB | GIS处理 |
| SSGISQuery.SDL | 483KB | GIS查询 |
| SSTBManager.SDL | 254KB | 表管理 |
| SS3DView.sdl | 348KB | 3D视图 |
| LandDispatch.SDL | 422KB | 土地Dispatch |
| SSCommTools.SDL | 1.1MB | 通用工具 |

---

## 关键结论

1. **HTTP请求在SDL脚本里构建** — SSERPTools只是命令路由
2. **所有ERP命令都是SDL脚本调用** — ProgressReportList/WorkSubmit等都是脚本名
3. **SScript.SDL是主入口** — ssExcuteFunction加载此文件执行脚本
4. **ACCESS_TOKEN在运行时获取** — 不持久化，每次调用GetToken()
