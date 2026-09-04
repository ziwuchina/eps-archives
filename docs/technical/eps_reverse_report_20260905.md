# EPS2016 逆向研究报告 — 2026-09-05 决定性突破

> 主线：把 `Eps.exe`（EPS2016 顺德专用版）完完全全逆向研究
> 本报告记录 2026-09-05 的关键突破：官方 CHM 文档全解析 + COM 外部自动化通道验证成功

---

## 一、今日突破总览

| # | 突破 | 证据 | 价值 |
|---|------|------|------|
| 1 | **官方 CHM 脚本开发文档全解析**（611 页） | `chm_extract\` 600+ htm + `eps_api_catalog.csv`（479 方法） | 拿到完整官方 API 手册，无需逆向即可开发 EPS 自动化 |
| 2 | **COM 外部自动化通道验证成功** | `CreateObject("Eps.EpsApplication")` + `GetScriptDispatch` 实测 OK | EPS 可被外部程序/VBS/Python 自动化 |
| 3 | **第二套 COM 接口发现**（EpsCom.*，80 ProgID） | 注册表 dump `com_progids_full.txt` | ECFeature/ECMap/ECLayer 等底层对象模型 |
| 4 | **ScriptCryptor + vbsedit + 加密狗体系梳理** | `D:\EPS2016Shunde` 目录发现 | 脚本加密、HASP 授权机制线索 |
| 5 | **官方"进程外调用 EPS"demo 脚本获取** | `demo_EPS_Demo.vbs`（2392B） | 官方外部自动化配方完整还原 |
| 6 | **SDL 标准格式确认** | CHM 296 页：`$SDL.SSProject.View.Extend`（点号） | 与逗号格式并存，命令分发改明白 |

---

## 二、EPS 官方脚本系统机制（CHM 文档确认）

### 2.1 核心规则（CHM 8 页《EPS脚本语言规则》）

1. **入口函数**：`Sub OnClick()` — 每个脚本必须有
2. **系统消息函数**（事件钩子）：
   - `BeforeSaveImportData()` — 导入外部数据存库前
   - `BeforeSaveExportData()` — 写出外部数据前
   - `TransCoordXYZ(...)` — 坐标投影换算
   - 另有键盘/鼠标/快捷键/上下文菜单/定时器/选择集改变等 20+ 事件钩子（CHM 457-487 页）
3. **`SSProcess` 是系统缺省对象**：与 EPS 平台交互主入口，无需定义直接 `SSProcess.方法名` 调用
4. **脚本调用**：
   - `RunScript "VBScript", "分组", "名称"` — 运行外部脚本（相对 `工作台面\Script` 目录）
   - `#include "脚本文件名.vbs"` — 引用外部脚本（合并代码）
5. **存储**：脚本存 `EPS 执行目录\SCRIPT\`，组织文件 `SScript.TXT`
6. **激活**：命令行输入 `Script` 命令打开脚本编辑器

### 2.2 六大对象（CHM 文档结构）

| 对象 | 方法数 | 功能 |
|------|--------|------|
| **SSProcess** | 455 | 图形编辑/工程管理/选择集/数据整理/数据转换/坐标转换/系统设置（CHM 12-455 页） |
| **SSView** | 25 | 屏幕绘制（画线/圆/多边形/文本/图片）（CHM 488-512 页） |
| **SSArray** | 12 | 数组操作（CHM 513-524 页） |
| **SSParameter** | 11 | 跨脚本共享参数（CHM 525-537 页） |
| **SSFunc** | 38 | 扩展函数库（EXCEL/LOG/汉字转拼音等）（CHM 538-575 页） |
| **SSProject** | 32 | 工程/数据源/地图/图层管理（CHM 576-609 页） |

### 2.3 经典脚本样例（CHM 8 页）

```vbs
Sub OnClick()
  SSProcess.ClearSelection
  SSProcess.ClearSelectCondition
  SSProcess.SetSelectCondition "SSObj_Code", "==", "4420"
  SSProcess.SelectFilter
  SSProcess.PushUndoMark
  SSProcess.ChangeSelectionObjAttr "SSObj_Code", "4430"
End Sub
```

### 2.4 SDL 命令（CHM 296 页）

```vbs
SSProcess.ExecuteSDLFunction "$SDL.SSProject.View.Extend", 0    ' 全视
SSProcess.ExecuteSDLFunction "$SDL.SSProject.Display.RedrawExtend", 0  ' 重生成
```

**注意**：官方 SDL 标准格式为**点号分隔**（`$SDL.模块.命令`）；此前 Frida 验证的逗号格式（`$SDL,WzExtBridge,WzExtProbe`）为另一种调用形式。

### 2.5 外部 DLL 模块（CHM 294 页 — WzExtBridge 机制）

```
SSProcess.ExecuteCommand(libFileName, procName, commandDescription, transSelection)
```

- `libFileName`：外部模块名（无路径则放 EPS 执行目录），如 `"MyFunction.DLL"`
- `procName`：函数名
- `transSelection`：1 = 传递选择集，函数签名：
  ```c
  extern "C" __declspec(dllexport) BOOL procName(CStringArray*, CGeObjList*, CProgressCtrl*);
  ```
- 参数传递：`SSProcess.AddFunctionParameter "code==2110,layer=123"` + `ClearFunctionParameter`

**这正是 WzExtBridge.dll 的官方调用机制！**

---

## 三、COM 外部自动化通道（决定性验证）

### 3.1 官方"进程外调用 EPS"demo（`进程外调用EPS_Demo.vbs`）

```vbs
' 创建 Eps 实例
Set epsApp = CreateObject("Eps.EpsApplication")
' 显示 Eps 界面
epsApp.SetVisible 1
' 获取 EPS 进程内脚本句柄
Set SSProcess = epsApp.GetScriptDispatch("SScript.dll", "SSProcess")
Set SSView    = epsApp.GetScriptDispatch("SScript.dll", "SSProcessView")
Set SSParameter = epsApp.GetScriptDispatch("SScript.dll", "SSParameter")
' 新建/打开工程
epsApp.InitWorkSpace edbfileName, templateFileName
' 更新当前 Map 句柄
SSProcess.UpdateCurMap 0
' 创建点对象（地物编码/坐标/高程）
SSProcess.CreateNewObjByCode code
SSProcess.AddNewObjPoint x, y, z, 0, ""
SSProcess.AddNewObjToSaveObjList
SSProcess.SaveBufferObjToDatabase
' 关闭并退出 EPS
epsApp.CloseAllEdb
```

### 3.2 实测验证结果

| 步骤 | SSH 会话（session 0） | GUI 会话（session 1） |
|------|----------------------|----------------------|
| `CreateObject("Eps.EpsApplication")` | ✅ OK | ✅ OK |
| `GetScriptDispatch("SScript.dll","SSProcess")` | ✅ OK | ✅ OK |
| `SetVisible(1)` | —（无桌面） | ✅ OK |
| `CloseAllEdb()` | ✅ OK | ✅ OK |
| 业务方法（GetSysPathName/InitWorkSpace 等） | ⚠️ 需完整初始化 | ⚠️ InitWorkSpace 弹模态对话框需人工交互 |

**结论**：
- **COM 通道完全打通**——EPS2016 可被外部 VBS/Python 实例化并获取脚本句柄
- **完整流程（InitWorkSpace 建工程）需要在 233 解锁的桌面会话**运行（EPS 启动弹模态对话框）
- 之前"VBS 自动化不可行"的结论**仅针对命令框注入路径**，官方 COM 通道可行

### 3.3 EpsCom.* 第二套 COM 接口（80 个 ProgID）

注册表 HKCR 发现，来自 `EpsCOM.dll`：

| 分类 | ProgID 示例 |
|------|------------|
| 应用 | `EpsCOM.ECAppliction`、`Eps.EpsApplication`、`Eps.Database` |
| 要素/对象 | `EpsCom.ECFeature`、`ECFeatureManager`、`ECGeoAttrib` |
| 地图/图层 | `EpsCom.ECMap`、`ECLayer`、`ECDataSource`、`ECDrawMap` |
| 几何 | `EpsCom.ECGeometrys`、`ECPointGeometry`、`ECLineGeometry`、`ECNoteGeometry`、`ECAreaGeometry` |
| 命令/UI | `EpsCOM.ECCmdBase`、`ECCmdManager`、`ECCommandBar`、`ECDlgBase` |
| 数学/工具 | `EpsCom.ECMath`、`ECCtrlPoint`、`ECByteArray`、`ECTriangleNet` |

完整列表见 `com_progids_full.txt`（80 个）。

---

## 四、加密狗与脚本加密体系

`D:\EPS2016Shunde` 完整目录发现：

| 组件 | 路径 | 说明 |
|------|------|------|
| HASP 驱动 | `UsbKey\haspdinst.exe`、`HASPUserSetup.exe` | SafeNet HASP 加密狗驱动 |
| 授权文件 | `License\*.txt`（16 个） | HASP 授权码（1500-5405-0960-6843 等） |
| 网络授权 | `nethasp.ini` | 网络 HASP 配置 |
| 授权 DLL | `hasp_windows_82156.dll`、`siusbxp.dll` | HASP 运行时 / USB Key |
| 注册工具 | `EpsRegister.xml`、`EpsRegTools.exe`、`regeps.bat` | EPS 注册 |
| 授权测试 | `testSunwayLic.exe` | 授权测试 |
| **脚本加密** | `ScriptCryptor.exe` + `.chm` + `.dat` | 把 .vbs 加密为不可读脚本 |
| VBS 编辑器 | `vbsedit.exe` | 第三方 VBS 编辑器 |
| 官方文档 | `Help\EpsScipt-20161030.chm` | **611 页脚本开发文档** |

授权检查函数：`SSCore32.dll` 的 `GetUsbKeyID` / `InitNetLicenseStatus`（字符串分析定位）。

---

## 五、CHM 文档 API 目录统计

| 类别 | 页数 |
|------|------|
| 总页数 | 611 |
| SSProcess 方法 | 479（含签名） |
| 系统消息函数（事件钩子） | ~30（457-487 页） |
| 对象参考（SSView/SSArray/SSParameter/SSFunc/SSProject） | 120（488-609 页） |
| VBScript/JScript 语言参考 | 大量（4-5 页等） |

产物：
- `Eps2016_exe\chm_extract\` — CHM 解压全文（600+ htm）
- `Eps2016_exe\eps_api_catalog.csv` — 479 方法目录 CSV
- `Eps2016_exe\EPS2016_脚本API目录.xlsx` — 格式化 Excel

---

## 六、看板重启（2026-09-05）

- **24 条原记录**：8 条已完成重新验证 ✅、16 条进行中加【2026-09-05 重启】标记
- **3 条新增**：
  1. 【今日突破】EPS 官方 CHM 文档全解析（611 页 API 手册）
  2. 【今日突破】EPS COM 外部自动化通道验证成功
  3. 【今日发现】ScriptCryptor 脚本加密 + 加密狗体系梳理
- **分水岭结论修正**：A 路线"VBS 自动化不可行"仅针对命令框注入；**EPS 自动化可行，走官方 COM + SCRIPT 目录 + SDL 机制**

---

## 七、下一步计划

| 优先级 | 任务 | 说明 |
|--------|------|------|
| P0 | 233 解锁桌面后验证 InitWorkSpace 建工程 + 建对象 | 完整闭环自动化 |
| P0 | 构建自动化运行脚本（官方配方） | 可交付用户使用 |
| P1 | 静态反汇编 SSProject.dll 的 ExecuteSDLCommand | 对照官方文档验证 |
| P1 | 分析 License 授权格式 + ScriptCryptor 加密脚本 | 加密狗/脚本加密逆向 |
| P2 | EpsCom.* 第二套接口对象模型 dump | 底层对象模型 |

---

## 附：关键文件路径

- 本机汇报目录：`C:\Users\Administrator\Desktop\AI相关\EPS项目汇报\`
  - `Eps2016_exe\` — 逆向分析工作区
    - `Eps.exe`（2543616B 主程序副本）
    - `dlls\`（SScript/SSCore32/SSProject/SSMap 等 6 DLL）
    - `COM_interfaces_dump.txt`（590 行 COM 接口 dump）
    - `chm_extract\`（CHM 解压 600+ htm）
    - `eps_api_catalog.csv` / `EPS2016_脚本API目录.xlsx`
    - `com_progids_full.txt`（80 ProgID）
    - `demo_EPS_Demo.vbs`（官方进程外调用 demo）
- 233 远程：`D:\EPS2016Shunde\`（EPS2016 安装根）
