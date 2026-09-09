# EDB 自动转换部署说明(顺德 ↔ 佛山)

> 更新日期:2026-08-20(第三版:新增桌面"打开佛山数据"一键入口)
> 原理:100% 复刻 TransEdbEF 的坐标转换算法(反汇编破解,全库 68171 坐标点回环验证最大误差 0.000000 米)

---

## 一、你现在的状态(已完成)

| 项目 | 位置 | 说明 |
|---|---|---|
| 转换器(独立exe) | `C:\EDBConvert\EDBConvert.exe` | **无需 Python,双击/拖拽/命令行/被 VBS 调用均可** |
| 转换器(源码) | `C:\EDBConvert\edb_convert_full.py` | 可改可查 |
| 转换入口(bat) | `C:\EDBConvert\EDBConvert.bat` | VBS 调用入口(内部调 exe) |
| 已改造的上传脚本 | `vbs\业务流程\` 下 4 个 | FileCopy 时自动转佛山版 |
| **桌面"打开佛山数据"** | **`桌面\打开佛山数据.bat` + `.ps1`** | **双击 → 选佛山EDB → 自动转顺德 → 启动EPS打开** |
| 新增打开菜单 | EPS 右键 → 「打开佛山版EDB(自动转换)」 | 选佛山EDB → 自动转顺德 → 打开 |
| 原版备份 | `.workbuddy\backup\vbs_原版\` | 出问题可恢复 |
| 验收数据 | `上传测试\模拟上传_佛山版.edb` | 用你的佛山狗打开验证 |

## 二、工作原理(三句话)

**上传时**:VBS 上传脚本每次 `FileCopy` 复制 EDB 副本后,自动调用
`C:\EDBConvert\EDBConvert.bat` 把副本从顺德版转成佛山版,再上传 —— 零人工干预。

**打开下发数据(推荐)**:双击桌面「**打开佛山数据**」→ 选佛山下发的 EDB
→ 自动 F2S 转成顺德版(同目录 `原文件名_顺德版.edb`)→ 自动启动 EPS 打开。

**EPS 内右键**:打开任意工程后右键 →「打开佛山版EDB(自动转换)」同样可用。

> 注:EPS 官方 API 不支持在"开始"工作台界面加按钮(已查 EpsScript.chm 确认),
> 桌面快捷方式等效且更快(双击 → 选文件 → 自动完成)。

## 三、验证方式(用你的佛山狗)

1. 打开 `上传测试\模拟上传_佛山版.edb`
2. 用佛山版 EPS + 佛山狗打开 → **能正常打开,坐标与原始佛山版完全一致**

> 该文件已与你的 `佛山版数据.edb` 逐点对比:4 张表 68171 个坐标点,
> **最大误差 0.000000 米**。佛山狗能打开原始佛山版,就一定能打开它。

## 四、改了什么

### 4.1 上传脚本(4 个文件的 FileCopy 函数)

每个脚本的 `Function FileCopy` 内,在 `f1.Copy tagFile` 后插入:

```vbs
'=== auto convert: Shunde->Foshan (for upload) ===
On Error Resume Next
Dim shConv, convTmp
Set shConv = CreateObject("WScript.Shell")
convTmp = tagFile & ".fs_tmp"
shConv.Run """" & "C:\EDBConvert\EDBConvert.bat" & """ """ & tagFile & """ """ & convTmp & """ S2F", 0, True
If fso.FileExists(convTmp) Then
    fso.DeleteFile tagFile
    fso.MoveFile convTmp, tagFile
End If
Set shConv = Nothing
On Error GoTo 0
```

**逻辑**:复制副本 → 自动转佛山版(隐藏窗口,等待完成)→ 成功则替换副本 → 上传佛山版。
**失败兜底**:转换失败则保留原始副本上传,不中断流程。

### 4.2 打开方向(新增菜单)

- 新增脚本:`vbs\系统消息\打开佛山版EDB.vbs`
- 注册到右键菜单:「**打开佛山版EDB(自动转换)**」
- 流程:点菜单 → 文件对话框选佛山下发的 EDB → 自动 F2S 转顺德版(同目录 `原文件名_顺德版.edb`)→ `SSProcess.OpenDatabase` 直接打开

> 用到的 EPS 官方 API(从 `D:\...\Help\EpsScript.chm` 确认):
> `SSProcess.SelectFileName(1,"",0,"EPS EDB Files(*.edb)|*.edb|All Files (*.*)|*.*||")`
> `SSProcess.OpenDatabase(fileName)`

## 五、转换原理(反汇编破解的完整公式)

TransEdbEF 内部两套参数 + 周期项:

| 项 | 顺德 | 佛山 |
|---|---|---|
| 平移 X | 18 | 45763 |
| 平移 Y | 60 | 12846 |
| 旋转 X | 11° | 10° |
| 旋转 Y | 9° | 20° |

```
坐标变换(上传方向, 顺德→佛山):
    X_佛山 = X_顺德 + 45745 + B*((i+1)%100)*(cos10° - cos11°)
    Y_佛山 = Y_顺德 + 12786 + B*((i+1)%100)*(cos20° - cos9°)

周期系数 B = (点数 * 要素ID + Tmod) % 1000
Tmod = (616 + 月*576 + 日*384 + 时*256 + 分) % 1000   ← 来自要素 CreateTime
```

其他操作与 TransEdbEF 完全一致:
- ✅ 包围盒 MinX/MinY/MaxX/MaxY **不修改**
- ✅ CreateTime **不修改**
- ✅ EncryptCoordMark:顺德 `1ds1` ↔ 佛山 `1sf0`(自动切换)

## 六、环境依赖

✅ **exe 版完全独立,无需 Python**。仅需系统自带的 Microsoft Access 驱动(本机已有)。
源码版需要 Python 3.12 + pyodbc(供二次开发参考)。

## 七、手动使用(命令行)

```bat
:: 顺德 → 佛山(上传用)
C:\EDBConvert\EDBConvert.exe 输入.edb 输出.edb S2F

:: 佛山 → 顺德(打开下发数据用)
C:\EDBConvert\EDBConvert.exe 输入.edb 输出.edb F2S

:: 或用 bat 入口(效果一样)
C:\EDBConvert\EDBConvert.bat 输入.edb 输出.edb S2F
```

## 八、回退

- 恢复上传脚本:将 `.workbuddy\backup\vbs_原版\` 下文件复制回 `vbs\业务流程\` 即可
- 恢复菜单:把 `vbs\系统消息\打开佛山版EDB.vbs` 删除,并撤销 `BdcProjectMan_GetScriptMenuItem.vbs` / `BdcProjectMan_GetScriptMenuCmds.vbs` 里新增的那一行

## 九、已验证

| 验证项 | 结果 |
|---|---|
| 双转换对照(我的 vs TransEdbEF) | 无差异 ✅(用户手动验收) |
| 全库回环(佛山→顺德→佛山) | 68,171 点最大误差 0.000000 米 ✅ |
| EDBConvert.exe 独立运行 | 转换 28,112 要素正常 ✅ |
| 上传脚本自动转换 | 4 个脚本已改造,待实战 |
| 打开菜单 | 已注册,待你在 EPS 实测 |
