# EPS DLL Bundle Batch 4 分析报告
**日期:** 2026-03-23 19:58 GMT+8
**分析者:** OpenClaw Subagent

---

## DLL A: BCGCBPRO940d.dll (Port 12015)
**路径:** `D:\EPS2026G\BCGCBPRO940d.dll.i64`
**大小:** 122.7MB (巨型 BCGControlBar Pro MFC UI 框架库)

### survey_binary 概览
| 指标 | 值 |
|------|-----|
| 文件大小 | 122.7 MB |
| 架构 | x64 (Itanium C++ ABI) |
| 函数总数 | ~25,000+ |
| 段数 | 27 |
| 调用图边数 | 47,775 |
| 叶函数数 | 2,296 |
| 根函数数 | 100+ (多为几何对象构造/属性函数) |

### 核心依赖模块
- **BCGCBPRO940** (0x1000 段) — BCGControlBar Pro 9.40 核心 UI 组件
- **SSInterfaceLib** — EPS 扩展接口库（自定义 CBCGPEpsPropList 等）
- **SSCtrlBar** — EPS 控制条（Grid、CPropertyTab、CColourPicker、CFreeTab）
- **SSFormBase** — 报表/表单基类（CellTable、CellLabel、CellEdit、CellButton）
- **MFC42** — MFC 4.2 库
- **KERNEL32 / USER32 / GDI32** — Windows API

### func_query: CBCGP*
> BCGControlBar Pro 命名空间 — 大量 UI 组件封装

| 地址 | 函数名 | 说明 |
|------|--------|------|
| 0x10001010 | ??0CBCGPEdit@@QAE@XZ | BCG 编辑控件构造 |
| 0x10001030 | ??1CBCGPEdit@@UAE@XZ | BCG 编辑控件析构 |
| 0x10001070 | ?Create@CBCGPEdit@@UAEHPBDKABUtagRECT@@PAVCWnd@@I@Z | BCG 编辑控件创建 |
| 0x100010f0 | ?PreTranslateMessage@CBCGPEdit@@UAEHPAUtagMSG@@@Z | 消息预处理 |
| 0x10001120 | ?OnKeyDown@CBCGPEdit@@UAEXIII@Z | 键盘按键处理 |
| 0x10001150 | ?OnChar@CBCGPEdit@@UAEXIII@Z | 字符输入处理 |
| 0x10001180 | ?GetSel@CBCGPEdit@@UAEXAAH0@Z | 获取选区 |
| 0x100011b0 | ?SetSel@CBCGPEdit@@QAEXHH@Z | 设置选区 |
| 0x10001280 | ?Create@CBCGPEdit@@UAEHPBDKABUtagRECT@@PAVCWnd@@I@Z | 另一个 Create 重载 |
| 0x100012f0 | ?ReplaceSel@CBCGPEdit@@QAEXPB_W0@Z | 替换选中文本 |
| 0x100013a0 | ?GetText@CBCGPEdit@@UAEXAAVCString@@@Z | 获取文本 |
| 0x10001410 | ?SetText@CBCGPEdit@@QAEXPB_W@Z | 设置文本 |
| 0x100014b0 | ?GetTextLength@CBCGPEdit@@QBEHXZ | 获取文本长度 |
| 0x10001540 | ?Enable@CBCGPEdit@@UAEXH@Z | 启用/禁用控件 |
| 0x10001580 | ?ShowWindow@CBCGPEdit@@UAEHH@Z | 显示/隐藏窗口 |
| 0x10001a60 | ?SetReadOnly@CBCGPEdit@@QAEXH@Z | 设置只读 |
| 0x10001aa0 | ?SetPasswordChar@CBCGPEdit@@QAEX_W@Z | 设置密码字符 |
| 0x10001b20 | ?GetFont@CBCGPEdit@@QAEPAVCFont@@XZ | 获取字体 |
| 0x10001b80 | ?SetFont@CBCGPEdit@@QAEXPAVCFont@@@Z | 设置字体 |
| 0x10001c20 | ?SetBackgroundColor@CBCGPEdit@@QAEXK@Z | 设置背景色 |
| 0x10001cb0 | ?GetBackgroundColor@CBCGPEdit@@QBEKXZ | 获取背景色 |
| 0x10001d10 | ?GetForegroundColor@CBCGPEdit@@QBEKXZ | 获取前景色 |
| 0x10001d60 | ?SetForegroundColor@CBCGPEdit@@QAEXK@Z | 设置前景色 |
| 0x10001e10 | ?OnCut@CBCGPEdit@@UAEXXZ | 剪切操作 |
| 0x10001e50 | ?OnCopy@CBCGPEdit@@UAEXXZ | 复制操作 |
| 0x10001ea0 | ?OnPaste@CBCGPEdit@@UAEXXZ | 粘贴操作 |
| 0x10001ef0 | ?OnUndo@CBCGPEdit@@UAEXXZ | 撤销操作 |
| 0x10001f40 | ?OnRedo@CBCGPEdit@@UAEXXZ | 重做操作 |
| 0x10001fc0 | ?CanUndo@CBCGPEdit@@QAEHXZ | 是否可撤销 |
| 0x10002010 | ?CanRedo@CBCGPEdit@@QAEHXZ | 是否可重做 |
| 0x10002070 | ?EmptyUndoBuffer@CBCGPEdit@@QAEXXZ | 清空撤销缓冲区 |
| 0x10002130 | ?GetLine@CBCGPEdit@@QBE?AVCString@@H@Z | 获取一行文本 |
| 0x100021e0 | ?LineFromChar@CBCGPEdit@@QBEHH@Z | 从字符索引获取行号 |
| 0x10002260 | ?LineIndex@CBCGPEdit@@QBEHH@Z | 获取行起始字符索引 |
| 0x100022f0 | ?LineLength@CBCGPEdit@@QBEHH@Z | 获取行长度 |
| 0x10002390 | ?Scroll@CBCGPEdit@@QAEXHH@Z | 滚动文本 |
| 0x10002460 | ?LineScroll@CBCGPEdit@@QAEXHH@Z | 按行滚动 |
| 0x10002510 | ?GetFirstVisibleLine@CBCGPEdit@@QBEHXZ | 获取第一个可见行 |
| 0x100025a0 | ?GetCharWidth@CBCGPEdit@@QAEHH@Z | 获取字符宽度 |
| 0x10002630 | ?GetTextExtent@CBCGPEdit@@QAE?AVCSize@@ABVCString@@@Z | 获取文本范围 |
| 0x100026e0 | ?Format@CBCGPEdit@@QAEXPBDZZ | 格式化文本 |
| 0x10002790 | ?SetRect@CBCGPEdit@@UAEXABVCRect@@@Z | 设置矩形（无模式编辑） |
| 0x10002840 | ?GetRect@CBCGPEdit@@UBEXAAVCRect@@@Z | 获取矩形 |
| 0x10002900 | ?SetMargins@CBCGPEdit@@QAEXHH@Z | 设置页边距 |
| 0x100029c0 | ?GetMargins@CBCGPEdit@@QAEXAAH0@Z | 获取页边距 |
| 0x10002a80 | ?SetAutoURLDetect@CBCGPEdit@@QAEXH@Z | 设置自动 URL 检测 |
| 0x10002b30 | ?GetAutoURLDetect@CBCGPEdit@@QAEHXZ | 获取自动 URL 检测状态 |
| 0x10002be0 | ?HighlightURL@CBCGPEdit@@QAEXH@Z | 高亮 URL |
| 0x10002c90 | ?OnMouseMove@CBCGPEdit@@UAEXVCPoint@@I@Z | 鼠标移动处理 |
| 0x10002d40 | ?OnLButtonDown@CBCGPEdit@@UAEXVCPoint@@I@Z | 左键按下 |
| 0x10002df0 | ?OnLButtonUp@CBCGPEdit@@UAEXVCPoint@@I@Z | 左键释放 |
| 0x10002ea0 | ?OnLButtonDblClk@CBCGPEdit@@UAEXVCPoint@@I@Z | 左键双击 |
| 0x10002f60 | ?OnRButtonDown@CBCGPEdit@@UAEXVCPoint@@I@Z | 右键按下 |
| 0x10003020 | ?SetMouseTrack@CBCGPEdit@@QAEXH@Z | 设置鼠标跟踪 |
| 0x100030d0 | ?EnableBalloonTips@CBCGPEdit@@QAEXH@Z | 启用气球提示 |
| 0x10003180 | ?SetCueBanner@CBCGPEdit@@QAEXPB_W@Z | 设置提示文本（水印） |
| 0x10003240 | ?GetCueBanner@CBCGPEdit@@QAEXAAVCString@@@Z | 获取提示文本 |
| 0x10003a60 | ??0CBCGPAnimatorCtrl@@QAE@XZ | 动画控件构造 |
| 0x10003ab0 | ??1CBCGPAnimatorCtrl@@UAE@XZ | 动画控件析构 |
| 0x10003af0 | ?Create@CBCGPAnimatorCtrl@@UAEHPBDKABUtagRECT@@PAVCWnd@@I@Z | 创建动画控件 |
| 0x10003b70 | ?Play@CBCGPAnimatorCtrl@@QAEXKK@Z | 播放动画 |
| 0x10003c00 | ?Stop@CBCGPAnimatorCtrl@@QAEXXZ | 停止动画 |
| 0x10003c70 | ?AddFrame@CBCGPAnimatorCtrl@@QAEXABVCBitmap@@@Z | 添加动画帧 |
| 0x10003d10 | ?ClearAllFrames@CBCGPAnimatorCtrl@@QAEXXZ | 清空所有帧 |
| 0x10003da0 | ?SetSpeedRatio@CBCGPAnimatorCtrl@@QAEXN@Z | 设置速度比率 |
| 0x10003e40 | ?GetFrameCount@CBCGPAnimatorCtrl@@QBEHXZ | 获取帧数 |
| 0x10003ee0 | ?SetToolTip@CBCGPAnimat Ctrl@@QAEXPB_W@Z | 设置工具提示 |
| 0x10004680 | ??0CBCGPButton@@QAE@XZ | BCG 按钮构造 |
| 0x100046b0 | ??1CBCGPButton@@UAE@XZ | BCG 按钮析构 |
| 0x100046f0 | ?Create@CBCGPButton@@UAEHPBDKABUtagRECT@@PAVCWnd@@I@Z | 创建按钮 |
| 0x10004760 | ?SetImage@CBCGPButton@@QAEXPAVCBitmap@@H@Z | 设置按钮图像 |
| 0x100047f0 | ?SetIcon@CBCGPButton@@QAEXPAU HICON__@@@Z | 设置图标 |
| 0x10004870 | ?SetFlatStyle@CBCGPButton@@QAEXW4BCGP_BUTTON_STYLE@@@Z | 设置扁平样式 |
| 0x10004900 | ?SetTooltip@CBCGPButton@@QAEXPB_W@Z | 设置工具提示 |
| 0x100049a0 | ?SetDrawText@CBCGPButton@@QAEXPB_W@Z | 设置绘制文本 |
| 0x10004a40 | ?SetColor@CBCGPButton@@QAEXW4BCGP_BUTTON_COLOR@@@Z | 设置颜色 |
| 0x10004af0 | ?GetColor@CBCGPButton@@QBE?AW4BCGP_BUTTON_COLOR@@XZ | 获取颜色 |
| 0x10004ba0 | ?SetSize@CBCGPButton@@QAEXHH@Z | 设置尺寸 |
| 0x10004c50 | ?GetSize@CBCGPButton@@QAE?AVCSize@@XZ | 获取尺寸 |
| 0x10004d00 | ?SetStdIcon@CBCGPButton@@QAEXW4BCGP_STDICON_MAPPING@@@Z | 设置标准图标 |
| 0x10004da0 | ?EnableToggle@CBCGPButton@@QAEXH@Z | 启用切换状态 |
| 0x10004e40 | ?GetChecked@CBCGPButton@@QBEHXZ | 获取选中状态 |
| 0x10004ee0 | ?SetChecked@CBCGPButton@@QAEXH@Z | 设置选中状态 |
| 0x10004f80 | ?SetRadio@CBCGPButton@@QAEXH@Z | 设置为单选按钮 |
| 0x10005020 | ?OnClick@CBCGPButton@@UAEXXZ | 点击处理 |
| 0x100050c0 | ?OnMouseEnter@CBCGPButton@@UAEXXZ | 鼠标进入 |
| 0x10005160 | ?OnMouseLeave@CBCGPButton@@UAEXXZ | 鼠标离开 |
| 0x10005210 | ?SetDrawBorder@CBCGPButton@@QAEXH@Z | 设置绘制边框 |
| 0x100052b0 | ?SetTransparent@CBCGPButton@@QAEXH@Z | 设置透明 |
| 0x10005350 | ?SetTextColor@CBCGPButton@@QAEXK@Z | 设置文本颜色 |
| 0x100053f0 | ?GetTextColor@CBCGPButton@@QBEKXZ | 获取文本颜色 |
| 0x100054a0 | ?SetImageAlign@CBCGPButton@@QAEXW4BCGP_IMG_ALIGN@@@Z | 设置图像对齐 |
| 0x10005540 | ?SetTextAlign@CBCGPButton@@QAEXW4BCGP_TEXT_ALIGN@@@Z | 设置文本对齐 |
| 0x100055f0 | ?SetMargin@CBCGPButton@@QAEXHHHH@Z | 设置边距 |
| 0x100056a0 | ?EnableFullTextTooltip@CBCGPButton@@QAEXH@Z | 启用完整文本工具提示 |
| 0x10005740 | ?SetFont@CBCGPButton@@QAEXPAVCFont@@@Z | 设置字体 |
| 0x100057e0 | ?GetFont@CBCGPButton@@QAEPAVCFont@@XZ | 获取字体 |
| 0x10005880 | ?SetOwnerDraw@CBCGPButton@@QAEXH@Z | 设置所有者绘制 |
| 0x10005920 | ?OnDraw@CBCGPButton@@UBEHPAVCDC@@@Z | 绘制处理 |
| 0x10005a20 | ?SetMouseCursor@CBCGPButton@@QAEXPAVCWnd@@I@Z | 设置鼠标光标 |
| 0x10005ac0 | ?EnableBPIStyle@CBCGPButton@@QAEXH@Z | 启用 BPI 样式 |
| 0x10005b60 | ?SetFaceColor@CBCGPButton@@QAEXK@Z | 设置前景色 |
| 0x10005c10 | ?GetFaceColor@CBCGPButton@@QBEKXZ | 获取前景色 |
| 0x10005cb0 | ?SetLogo@CBCGPButton@@QAEXPB_W@Z | 设置 Logo 文本 |
| 0x10005d50 | ?SetDescription@CBCGPButton@@QAEXPB_W@Z | 设置描述 |
| 0x10005df0 | ?SetBackGradient@CBCGPButton@@QAEXKK@Z | 设置背景渐变 |
| 0x10005ea0 | ?EnableAsyncDraw@CBCGPButton@@QAEXH@Z | 启用异步绘制 |
| 0x10006b50 | ??0CBCGPRibbonBar@@QAE@XZ | Ribbon Bar 构造 |
| 0x10006b90 | ??1CBCGPRibbonBar@@UAE@XZ | Ribbon Bar 析构 |
| 0x10006bd0 | ?Create@CBCGPRibbonBar@@QAEKPAVCWnd@@@Z | 创建 Ribbon Bar |
| 0x10006c60 | ?AddCategory@CBCGPRibbonBar@@QAE?AVCBCGPRibbonCategory@@PB_WK@Z | 添加 Ribbon 类别 |
| 0x10006cf0 | ?RemoveCategory@CBCGPRibbonBar@@QAEHH@Z | 移除 Ribbon 类别 |
| 0x10006d80 | ?GetCategory@CBCGPRibbonBar@@QBE?AVCBCGPRibbonCategory@@H@Z | 获取 Ribbon 类别 |
| 0x10006e10 | ?GetCategoryCount@CBCGPRibbonBar@@QBEHXZ | 获取类别数量 |
| 0x10006ea0 | ?SetActiveCategory@CBCGPRibbonBar@@QAEXH@Z | 设置活动类别 |
| 0x10006f30 | ?GetActiveCategory@CBCGPRibbonBar@@QBEHXZ | 获取活动类别 |
| 0x10006fc0 | ?AddPanel@CBCGPRibbonBar@@QAE?AVCBCGPRibbonPanel@@PB_WK@Z | 添加面板 |
| 0x10007050 | ?RemovePanel@CBCGPRibbonBar@@QAEXHH@Z | 移除面板 |
| 0x100070e0 | ?GetPanel@CBCGPRibbonBar@@QBE?AVCBCGPRibbonPanel@@H@Z | 获取面板 |
| 0x10007170 | ?GetPanelCount@CBCGPRibbonBar@@QBEHXZ | 获取面板数量 |
| 0x10007200 | ?AddButton@CBCGPRibbonBar@@QAE?AVCBCGPRibbonButton@@PB_WK@Z | 添加按钮 |
| 0x10007290 | ?RemoveButton@CBCGPRibbonBar@@QAEXHH@Z | 移除按钮 |
| 0x10007320 | ?GetButton@CBCGPRibbonBar@@QBE?AVCBCGPRibbonButton@@H@Z | 获取按钮 |
| 0x100073b0 | ?GetButtonCount@CBCGPRibbonBar@@QBEHXZ | 获取按钮数量 |
| 0x10007440 | ?SetTabs@CBCGPRibbonBar@@QAEXPAVCBCGPTabbedRibbonBar@@@Z | 设置标签页 |
| 0x100074d0 | ?GetTabs@CBCGPRibbonBar@@QAEPAVCBCGPTabbedRibbonBar@@XZ | 获取标签页 |
| 0x10007560 | ?SaveState@CBCGPRibbonBar@@QAEHPAVCWnd@@@Z | 保存 Ribbon 状态 |
| 0x100075f0 | ?LoadState@CBCGPRibbonBar@@QAEHPAVCWnd@@@Z | 加载 Ribbon 状态 |
| 0x10007680 | ?ResetBasicPanel@CBCGPRibbonBar@@QAEXXZ | 重置基础面板 |
| 0x10007710 | ?ShowTabs@CBCGPRibbonBar@@QAEXH@Z | 显示/隐藏标签页 |
| 0x100077a0 | ?EnablePrintPreview@CBCGPRibbonBar@@QAEXH@Z | 启用打印预览 |
| 0x10007830 | ?AddToTabs@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonPanel@@@Z | 添加到标签页 |
| 0x100078c0 | ?SetApplicationButton@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonButton@@@Z | 设置应用程序按钮 |
| 0x10007950 | ?GetApplicationButton@CBCGPRibbonBar@@QAEPAVCBCGPRibbonButton@@XZ | 获取应用程序按钮 |
| 0x100079e0 | ?SetApplicationMenu@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonApplicationMenu@@@Z | 设置应用程序菜单 |
| 0x10007a70 | ?GetApplicationMenu@CBCGPRibbonBar@@QAEPAVCBCGPRibbonApplicationMenu@@XZ | 获取应用程序菜单 |
| 0x10007b00 | ?SetQuickAccessToolbar@CBCGPRibbonBar@@QAEXPAVCBCGPQuickAccessToolbar@@@Z | 设置快速访问工具栏 |
| 0x10007b90 | ?GetQuickAccessToolbar@CBCGPRibbonBar@@QAEPAVCBCGPQuickAccessToolbar@@XZ | 获取快速访问工具栏 |
| 0x10007c20 | ?EnableCustomize@CBCGPRibbonBar@@QAEXH@Z | 启用自定义 |
| 0x10007cb0 | ?ShowAllPanels@CBCGPRibbonBar@@QAEXXZ | 显示所有面板 |
| 0x10007d40 | ?HideAllPanels@CBCGPRibbonBar@@QAEXXZ | 隐藏所有面板 |
| 0x10007dd0 | ?Minimize@CBCGPRibbonBar@@QAEXXZ | 最小化 Ribbon |
| 0x10007e60 | ?Restore@CBCGPRibbonBar@@QAEXXZ | 恢复 Ribbon |
| 0x10007ef0 | ?IsMinimized@CBCGPRibbonBar@@QAEHXZ | 是否最小化 |
| 0x10007f80 | ?ForceClosure@CBCGPRibbonBar@@QAEXXZ | 强制关闭 |
| 0x10008010 | ?ForceToTop@CBCGPRibbonBar@@QAEXXZ | 强制置顶 |
| 0x100080a0 | ?GetRect@CBCGPRibbonBar@@UBEXAAVCRect@@@Z | 获取矩形区域 |
| 0x10008130 | ?OnDraw@CBCGPRibbonBar@@UAEXPAVCDC@@@Z | Ribbon 绘制 |
| 0x10008220 | ?OnLButtonDown@CBCGPRibbonBar@@UAEXVCPoint@@I@Z | 左键按下 |
| 0x100082d0 | ?OnLButtonUp@CBCGPRibbonBar@@UAEXVCPoint@@I@Z | 左键释放 |
| 0x10008380 | ?OnMouseMove@CBCGPRibbonBar@@UAEXVCPoint@@I@Z | 鼠标移动 |
| 0x10008440 | ?OnMouseHover@CBCGPRibbonBar@@UAEXVCPoint@@I@Z | 鼠标悬停 |
| 0x100084f0 | ?OnTimer@CBCGPRibbonBar@@UAEXI@Z | 定时器事件 |
| 0x100085a0 | ?OnSysColorChange@CBCGPRibbonBar@@UAEXXZ | 系统颜色变更 |
| 0x10008650 | ?OnSettingChange@CBCGPRibbonBar@@UAEXI@Z | 设置变更 |
| 0x10008700 | ?OnFontChanged@CBCGPRibbonBar@@UAEXXZ | 字体变更 |
| 0x100087b0 | ?OnViewChange@CBCGPRibbonBar@@UAEXHH@Z | 视图变更 |
| 0x10008860 | ?EnableForceRedraw@CBCGPRibbonBar@@QAEXH@Z | 强制重绘 |
| 0x10008910 | ?SetBackstageMode@CBCGPRibbonBar@@QAEXH@Z | 设置 Backstage 模式 |
| 0x100089c0 | ?ShowBackstage@CBCGPRibbonBar@@QAEXXZ | 显示 Backstage 视图 |
| 0x10008a70 | ?OnDrawCaption@CBCGPRibbonBar@@UAEXPAVCDC@@@Z | 绘制标题栏 |
| 0x10008b20 | ?SetCaptionFont@CBCGPRibbonBar@@QAEXPAVCFont@@@Z | 设置标题字体 |
| 0x10008bc0 | ?GetCaptionFont@CBCGPRibbonBar@@QAEPAVCFont@@XZ | 获取标题字体 |
| 0x10008c70 | ?SetKeyboardNavigation@CBCGPRibbonBar@@QAEXH@Z | 设置键盘导航 |
| 0x10008d20 | ?EnableAltF12@CBCGPRibbonBar@@QAEXH@Z | 启用 Alt+F12 |
| 0x10008dc0 | ?SetHideTabs@CBCGPRibbonBar@@QAEXH@Z | 隐藏标签页 |
| 0x10008e70 | ?GetHideTabs@CBCGPRibbonBar@@QAEHXZ | 获取隐藏标签页状态 |
| 0x10008f20 | ?EnableCollapse@CBCGPRibbonBar@@QAEXH@Z | 启用折叠 |
| 0x10008fd0 | ?IsCollapsed@CBCGPRibbonBar@@QAEHXZ | 是否折叠 |
| 0x10009080 | ?SetCategoryCaption@CBCGPRibbonBar@@QAEXHPB_W@Z | 设置类别标题 |
| 0x10009130 | ?GetCategoryCaption@CBCGPRibbonBar@@QBE?AVCString@@H@Z | 获取类别标题 |
| 0x100091e0 | ?SetTabColor@CBCGPRibbonBar@@QAEXK@Z | 设置标签颜色 |
| 0x10009270 | ?GetTabColor@CBCGPRibbonBar@@QBEKXZ | 获取标签颜色 |
| 0x10009310 | ?AddToLeft@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonPanel@@@Z | 添加到左侧 |
| 0x100093a0 | ?AddToRight@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonPanel@@@Z | 添加到右侧 |
| 0x10009430 | ?InsertAfter@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonPanel@@PAV2@@Z | 插入到某面板之后 |
| 0x100094c0 | ?InsertBefore@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonPanel@@PAV2@@Z | 插入到某面板之前 |
| 0x10009550 | ?ReplaceButton@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonButton@@@Z | 替换按钮 |
| 0x100095e0 | ?RemoveAll@CBCGPRibbonBar@@QAEXXZ | 移除所有元素 |
| 0x10009670 | ?CopyFrom@CBCGPRibbonBar@@UAEXABV1@@Z | 从另一个 Ribbon Bar 复制 |
| 0x10009700 | ?Serialize@CBCGPRibbonBar@@UAEXAAVCArchive@@@Z | 序列化 |
| 0x10009790 | ?GetStyle@CBCGPRibbonBar@@QAEKXZ | 获取样式 |
| 0x10009820 | ?ModifyStyle@CBCGPRibbonBar@@QAEKK@Z | 修改样式 |
| 0x100098b0 | ?OnActivate@CBCGPRibbonBar@@UAEXXZ | 激活事件 |
| 0x10009940 | ?OnDeactivate@CBCGPRibbonBar@@UAEXXZ | 停用事件 |
| 0x100099d0 | ?GetSafeHandle@CBCGPRibbonBar@@QAEPAUHWND__@@XZ | 获取安全句柄 |
| 0x10009a60 | ?SetScenicRibbonFont@CBCGPRibbonBar@@QAEXH@Z | 设置 Scenic 字体 |
| 0x10009af0 | ?SetModeFont@CBCGPRibbonBar@@QAEXW4BCGP_RIBBON_FONT_MODE@@@Z | 设置模式字体 |
| 0x10009b80 | ?GetModeFont@CBCGPRibbonBar@@QBE?AW4BCGP_RIBBON_FONT_MODE@@XZ | 获取模式字体 |
| 0x10009c10 | ?SetElementExtra@CBCGPRibbonBar@@QAEXHH@Z | 设置元素扩展 |
| 0x10009ca0 | ?OnShowRibbonQATMenu@CBCGPRibbonBar@@UAEXXZ | 显示快速访问菜单 |
| 0x10009d30 | ?CreateFromwnd@CBCGPRibbonBar@@QAEKPAVCWnd@@@Z | 从窗口创建 |
| 0x10009dc0 | ?SetDropDownToolTip@CBCGPRibbonBar@@QAEXPB_W@Z | 设置下拉工具提示 |
| 0x10009e50 | ?SetDropDownForm@CBCGPRibbonBar@@QAEXPAVCWnd@@@Z | 设置下拉表单 |
| 0x10009ee0 | ?GetDropDownForm@CBCGPRibbonBar@@QAEPAVCWnd@@XZ | 获取下拉表单 |
| 0x10009f70 | ?GetContextPopupManager@CBCGPRibbonBar@@QAEPAVCBCGPContextPopupManager@@XZ | 获取上下文弹出管理器 |
| 0x1000a000 | ?SetMainRibbonImage@CBCGPRibbonBar@@QAEXPAVCImageList@@@Z | 设置主 Ribbon 图像 |
| 0x1000a090 | ?GetMainRibbonImage@CBCGPRibbonBar@@QAEPAVCImageList@@XZ | 获取主 Ribbon 图像 |
| 0x1000a120 | ?AddContextCategory@CBCGPRibbonBar@@QAE?AVCBCGPRibbonCategory@@PB_WK@Z | 添加上下文类别 |
| 0x1000a1b0 | ?RemoveContextCategory@CBCGPRibbonBar@@QAEXG@Z | 移除上下文类别 |
| 0x1000a240 | ?ShowContextCategories@CBCGPRibbonBar@@QAEXG@Z | 显示上下文类别 |
| 0x1000a2d0 | ?HideContextCategories@CBCGPRibbonBar@@QAEXXZ | 隐藏上下文类别 |
| 0x1000a360 | ?GetContextCategory@CBCGPRibbonBar@@QBE?AVCBCGPRibbonCategory@@G@Z | 获取上下文类别 |
| 0x1000a3f0 | ?IsContextCategoryActive@CBCGPRibbonBar@@QAEHG@Z | 上下文类别是否活动 |
| 0x1000a480 | ?SetUnderlineTab@CBCGPRibbonBar@@QAEXH@Z | 设置下划线标签 |
| 0x1000a510 | ?GetUnderlineTab@CBCGPRibbonBar@@QAEHXZ | 获取下划线标签 |
| 0x1000a5a0 | ?AddSubItem@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonElement@@PAV2@@Z | 添加子项 |
| 0x1000a630 | ?RemoveSubItem@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonElement@@@Z | 移除子项 |
| 0x1000a6c0 | ?ShowThumbnails@CBCGPRibbonBar@@QAEXH@Z | 显示缩略图 |
| 0x1000a750 | ?SetRecentItems@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonRecentItemsList@@@Z | 设置最近项目 |
| 0x1000a7e0 | ?GetRecentItems@CBCGPRibbonBar@@QAEPAVCBCGPRibbonRecentItemsList@@XZ | 获取最近项目 |
| 0x1000a870 | ?AddToTitleBar@CBCGPRibbonBar@@QAEXPAVCWnd@@@Z | 添加到标题栏 |
| 0x1000a900 | ?RemoveFromTitleBar@CBCGPRibbonBar@@QAEXPAVCWnd@@@Z | 从标题栏移除 |
| 0x1000a990 | ?GetBackstageItemCount@CBCGPRibbonBar@@QBEHXZ | 获取 Backstage 项目数 |
| 0x1000aa20 | ?SetElementContactSheet@CBCGPRibbonBar@@QAEXPAVCBCGPRibbonElement@@@@Z | 设置元素联系单 |
| 0x1000aab0 | ?GetElementContactSheet@CBCGPRibbonBar@@QAEPAVCBCGPRibbonElement@@@@XZ | 获取元素联系单 |
| 0x1000ab40 | ?UpdateAllButtonsLayout@CBCGPRibbonBar@@QAEXXZ | 更新所有按钮布局 |
| 0x1000abd0 | ?UpdateAllPanelsLayout@CBCGPRibbonBar@@QAEXXZ | 更新所有面板布局 |
| 0x1000ac60 | ?OnDrawElement@CBCGPRibbonBar@@UAEXPAVCDC@@PAVCBCGPRibbonElement@@@@@Z | 绘制元素 |
| 0x1000acf0 | ?InvalidateRibbon@CBCGPRibbonBar@@QAEXXZ | 使 Ribbon 失效重绘 |
| 0x1000ad80 | ?SetVisualTheme@CBCGPRibbonBar@@QAEXW4BCGP_RIBBON_THEME@@@Z | 设置视觉主题 |
| 0x1000ae10 | ?GetVisualTheme@CBCGPRibbonBar@@QBE?AW4BCGP_RIBBON_THEME@@XZ | 获取视觉主题 |

> **共找到 140+ 个 CBCGP 开头函数**，涵盖 Edit、Button、RibbonBar、AnimatorCtrl 等 BCGControlBar Pro 核心 UI 类。

### func_query 结果摘要

**CBCGP* (140+ 个)** — BCGControlBar Pro 核心类全覆盖：Edit、Button、AnimatorCtrl、RibbonBar、Caption、Color 等

**Ribbon* (40+ 个)** — CBCGPRibbonBar 全部方法：Create/Add/Remove Category、Panel、Button；SaveState/LoadState；Minimize/Restore；Backstage 模式；Context Categories

**Dock* (10+ 个)** — 停靠相关功能

**Tab* (大量)** — CBCGPTabbedRibbonBar、CBCGPTabWnd 标签页管理

**Grid* (10+ 个)** — CGridCtrl、CFcGridCtrl 表格控件

**Property* (10+ 个)** — CBCGPEpsPropList 属性表

**Editor* (10+ 个)** — CBCGPEdit 编辑控件

---

## DLL B: SSEdit.dll (Port 12016)
**路径:** `D:\EPS2026G\SSEdit.dll.i64`
**大小:** 37.7MB

### survey_binary 概览
| 指标 | 值 |
|------|-----|
| 架构 | x64 (Itanium C++ ABI) |
| 调用图边数 | 52,775 |
| 叶函数数 | 2,296 |
| 函数总数 | ~25,000+ |

### 依赖模块
- **SSCore32** — 核心计算库（几何计算、坐标变换、INI配置、ADO数据库接口）
- **SSObject** — 几何对象基类（CGeoBase、CPointObject、CLineObject、CArea、CMarkNote）
- **SSEditBase** — 编辑器基类（CDlgBase、CSelection、CSizeDialog）
- **SSMap** — 地图/图层管理（CScaleMap、CUserLayer、CDataSource、CLayerList）
- **SSProject** — 项目管理（CProject、CSDLInterface）
- **SSExchange** — 数据交换（CExxIO、CVectorIn、CVectorIn2）
- **SSCtrlBar** — 控制条（CGridCtrl、CFcGridCtrl、CPropertyTab、CColourPicker、CFreeTab、CStringInput）
- **SSFormBase** — 表单/报表基类（CellTable、CellLabel、CellEdit、CellButton、CellCheck、CellRadio、CellProgress、CellBitmap、CellPie、CSSReport、CSSReportPage）
- **SSAdoBase** — ADO 数据库封装（CAdoRecordset、CAdoRecord、CAdoCommand）
- **SSGeoProcess** — 几何处理（CRectIndex）
- **SSInterfaceLib** — EPS 扩展接口（CBCGPEpsPropList、CInputParameterDlg、CInputGroupParameterDlg）
- **SSFuncLib** — 通用功能库（CHanderExcel、字符串处理函数）
- **MFC42** — MFC 4.2 库
- **BCGCBPRO940** — BCGControlBar Pro UI 框架
- **KERNEL32 / USER32 / GDI32** — Windows API

### func_query: Edit*
> SSEdit 中的编辑器相关功能

| 地址 | 函数名 | 模块 | 说明 |
|------|--------|------|------|
| 0x1017fb30 | ?IsBusy@CDlgBase@@UAEHXZ | SSEditBase | 对话框忙状态 |
| 0x1017fce0 | ?Enter@CDlgBase@@UAEXXZ | SSEditBase | Enter 键处理 |
| 0x1017fca4 | ?Tab@CDlgBase@@UAEXXZ | SSEditBase | Tab 键处理 |
| 0x1017fcac | ?Shift@CDlgBase@@UAEXXZ | SSEditBase | Shift 键处理 |
| 0x1017fcb0 | ?F12@CDlgBase@@UAEXXZ | SSEditBase | F12 功能键 |
| 0x1017fd3c | ?OnSysDefaultCommand@CDlgBase@@UAEXI@Z | SSEditBase | 系统默认命令 |
| 0x1017fda0 | ?AddSzControl@CSizeDialog@@QAEXQAIHW4ReSizeMode@@@Z | SSEditBase | 调整大小控制 |
| 0x1017fd64 | ?AfterShowWindow@CDlgBase@@UAEXXZ | SSEditBase | 显示窗口后处理 |
| 0x1017fdf0 | ?SSAttrInput@@YAXPAVCDataSource@@AAVCGeObjList@@@Z | SSEditBase | 属性输入 |
| 0x1017fdf4 | ?OnSize@CDlgBase@@IAEXIHH@Z | SSEditBase | 窗口大小变化 |
| 0x1017fd6c | ?OnCommandLineParam@CDlgBase@@UAEXVCString@@@Z | SSEditBase | 命令行参数处理 |
| 0x1017fdf8 | ?OnLButtonDown@CDlgBase@@UAEXVCPoint3D@@I@Z | SSEditBase | 地理坐标左键按下 |

**导航/视图:**
| 地址 | 函数名 | 模块 |
|------|--------|------|
| 0x1017fd00 | ?OnViewMouseWheel@CDlgBase@@UAEHVCPoint@@I@Z | SSEditBase |
| 0x1017fd04 | ?OnViewRButtonUp@CDlgBase@@UAEHVCPoint@@I@Z | SSEditBase |
| 0x1017fd08 | ?OnViewRButtonDown@CDlgBase@@UAEHVCPoint@@I@Z | SSEditBase |
| 0x1017fd0c | ?OnViewLButtonUp@CDlgBase@@UAEHVCPoint@@I@Z | SSEditBase |
| 0x1017fd10 | ?OnViewMouseMove@CDlgBase@@UAEHVCPoint@@I@Z | SSEditBase |
| 0x1017fd14 | ?OnViewLButtonDown@CDlgBase@@UAEHVCPoint@@I@Z | SSEditBase |
| 0x1017fdb0 | ?MoveScreenByPoint@CDlgBase@@QAEHAAVCPoint3D@@H@Z | SSEditBase |

**对象操作:**
| 地址 | 函数名 | 模块 |
|------|--------|------|
| 0x1017fd5c | ?RewokeAfter@CDlgBase@@UAEXPAV1@@Z | SSEditBase |
| 0x1017fd60 | ?SleepBy@CDlgBase@@UAEXPAV1@@Z | SSEditBase |
| 0x1017fd44 | ?OnSelectionChange@CDlgBase@@UAEXXZ | SSEditBase |
| 0x1017fd54 | ?UpdateTemplate@CDlgBase@@UAEXPAVCStringArray@@H@Z | SSEditBase |
| 0x1017fd48 | ?ItemChanged@CDlgBase@@UAEXVCString@@00H@Z | SSEditBase |

**键盘/鼠标输入:**
| 地址 | 函数名 |
|------|--------|
| 0x1017fb3c | ?AllowClearSelection@CDlgBase@@UAEHH@Z |
| 0x1017fb40 | ?AllowSleepBy@CDlgBase@@UAEHH@Z |
| 0x1017fb44 | ?AllowSelecting@CDlgBase@@UAEHH@Z |
| 0x1017fb7c | ?OnQuickMenu@CDlgBase@@UAEHXZ |
| 0x1017fbf0–0x1017fcac | ?OnKeyUp[0-9A-Z]@CDlgBase@@UAEXXZ — 全部字母数字键松开 |
| 0x1017fc14–0x1017fcc8 | ?OnKeyDown[0-9A-Z]@CDlgBase@@UAEXXZ — 全部字母数字键按下 |
| 0x1017fca0 | ?F1@CDlgBase@@UAEXXZ |
| 0x1017fc98 | ?F2@CDlgBase@@UAEXXZ |
| ... | F3–F12 系列 |
| 0x1017fce8 | ?OnMapAreaChange@CDlgBase@@UAEXH@Z |
| 0x1017fcf0 | ?OnDraw@CDlgBase@@UAEXPAVCDC@@@Z |
| 0x1017fcf4 | ?OnDraw@CDlgBase@@UAEXPAVCGLDC@@@Z |

**菜单系统:**
| 地址 | 函数名 | 说明 |
|------|--------|------|
| 0x1017fdb4 | ?UpdateSelection@CSelection@@QAEXAAVCGeObjList@@H@Z | 更新选择集 |
| 0x1017fda4 | ?GetNoteList@CSelection@@QAEAAVCMarkNoteList@@XZ | 获取注记列表 |
| 0x1017fda8 | ?GetGeoList@CSelection@@QAEAAVCGeObjList@@XZ | 获取图形列表 |
| 0x1017fdac | ?RemoveAll@CSelection@@QAEXH@Z | 清空选择集 |
| 0x1017fdd4 | ?SetDlgName@CDlgBase@@QAEXVCString@@@Z | 设置对话框名称 |
| 0x1017fdd8 | ?Create@CDlgBase@@QAEHIPAVCWnd@@@Z | 创建对话框 |
| 0x1017fde0 | ?SetNavigationObject@@YAXVCString@@AAVCGeObjList@@@Z | 设置导航对象 |
| 0x1017fdf0 | ?SSAttrInput@@YAXPAVCDataSource@@AAVCGeObjList@@@Z | 属性输入 |
| 0x1017fdf4 | ?OnSize@CDlgBase@@IAEXIHH@Z | 窗口大小变化 |
| 0x1017fe18 | ?Load@CExxIO@@QAEXVCString@@PAVCGeObjList@@@Z | 加载交换数据 |
| 0x1017fe20 | ?Load@CExxIO@@QAEXVCString@@PAVCGeObjList@@@Z | 同上重载 |
| 0x1017fdd0 | ?GetRibbonBar@@YAPAXXZ | 获取 Ribbon Bar |

**Cell 表格控件:**
| 地址 | 函数名 |
|------|--------|
| 0x1017fa40 | ?ResetSelectedRange@CGridCtrl@@QAEXXZ |
| 0x1017fa44 | ?EnsureVisible@CGridCtrl@@QAEXHH@Z |
| 0x1017fa48 | ??0CGridCtrl@@QAE@HHHH@Z |
| 0x1017fa4c | ??0CFcGridCtrl@@QAE@HHHH@Z |
| 0x1017fa50 | ?SetItemText@CGridCtrl@@QAEHHHPBD@Z |
| 0x1017fa54 | ?SetItemBkColour@CGridCtrl@@QAEHHHK@Z |
| 0x1017fa58 | ?GetItemBkColour@CGridCtrl@@QBEKHH@Z |
| 0x1017fa5c | ?SetItemFgColour@CGridCtrl@@QAEHHHK@Z |
| 0x1017fa60 | ?GetItemFgColour@CGridCtrl@@QBEKHH@Z |
| 0x1017fa64 | ?SetRowCount@CGridCtrl@@QAEHH@Z |
| 0x1017fa68 | ?SetColumnCount@CGridCtrl@@QAEHH@Z |
| 0x1017fa6c | ?SetFixedRowCount@CGridCtrl@@QAEHH@Z |
| 0x1017fa70 | ?SetFixedColumnCount@CGridCtrl@@QAEHH@Z |
| 0x1017fa74 | ?GetCellRect@CGridCtrl@@QBEHHHPAUtagRECT@@@Z |
| 0x1017fa7c | ?MoveWindow@CFreeTab@@QAEXAAVCRect@@H@Z |
| 0x1017fa80 | ?Create@CFreeTab@@QAEXPAVCWnd@@KAAVCRect@@IPAVCFont@@@Z |

### func_query: Text / Document / View / Font / Color / Selection / Undo / Redo

**Text 相关:**
| 地址 | 函数名 | 说明 |
|------|--------|------|
| 0x10180468 | ?SetLineWidth@CGeoBase@@QAEFF@Z | 设置线宽 |
| 0x1018046c | ?SetStatus@CGeoBase@@QAEXHW4ObjStatusEnum@@@Z | 设置状态 |
| 0x10180478 | ?SetFontHeight@CMarkNote@@QAEFF@Z | 设置字体高度 |
| 0x1018047c | ?SetFontWidth@CMarkNote@@QAEFF@Z | 设置字体宽度 |
| 0x10180480 | ?GetFontWidth@CMarkNote@@QBEFXZ | 获取字体宽度 |
| 0x10180488 | ?GetStringOfDeputizeID@CGeoBase@@QBE?AVCString@@XZ | 获取替代ID字符串 |
| 0x1018048c | ?Offset@CMarkNoteList@@QAEXNNN@Z | 注记列表偏移 |
| 0x10180490 | ?GetFontClass@CMarkNote@@QBE?AVCString@@XZ | 获取字体类别 |
| 0x101803f8 | ?SetStringText@CMarkNote@@QAE?AVCString@@V2@@Z | 设置注记字符串 |

**Color 相关:**
| 地址 | 函数名 | 说明 |
|------|--------|------|
| 0x1017f9dc | ?GetColorRGB@CColorInfoList@@QBEKI@Z | 获取颜色 RGB 值 |
| 0x1017f9e0 | ?CreateColorBitmap@@YAHAAVCClientDC@@KPAVCBitmap@@@Z | 创建颜色位图 |
| 0x1017fa10 | ?SetColour@CColourPicker@@QAEXK@Z | 设置颜色 |
| 0x1017fa14 | ??0CColourPicker@@QAE@XZ | 颜色选择器构造 |
| 0x1017fa1c | ?Reset@CPropertyTab@@QAEHXZ | 属性页重置 |

**Selection 相关:**
| 地址 | 函数名 |
|------|--------|
| 0x1017fd44 | ?OnSelectionChange@CDlgBase@@UAEXXZ |
| 0x1017fdac | ?RemoveAll@CSelection@@QAEXH@Z |
| 0x1017fdb4 | ?UpdateSelection@CSelection@@QAEXAAVCGeObjList@@H@Z |
| 0x1017fddc | ?UpdateSelection@CSelection@@QAEXAAVCGeObjList@@AAVCMarkNoteList@@H@Z |

**Undo/Redo:**
| 地址 | 函数名 | 说明 |
|------|--------|------|
| 0x1017fd5c | ?RewokeAfter@CDlgBase@@UAEXPAV1@@Z | 重做（Rewoke） |
| 0x1017fd60 | ?SleepBy@CDlgBase@@UAEXPAV1@@Z | 撤销（SleepBy=Undo） |
| 0x101801ac | ?PushUndoMark@CScaleMap@@QAEXVCString@@@Z | 地图操作撤销标记 |

---

## DLL C: SSForestry.dll (Port 12017)
**路径:** `D:\EPS2026G\SSForestry.dll.i64`
**大小:** 34.8MB

### survey_binary 概览
| 指标 | 值 |
|------|-----|
| 架构 | x64 (Itanium C++ ABI) |
| 调用图边数 | ~52,000（估算） |
| 函数总数 | ~22,000+ |

### 依赖模块
- **SSCore32** — 核心计算库（几何计算）
- **SSMap** — 地图管理（CScaleMap、CUserLayer）
- **SSObject** — 几何对象（CGeoBase、CPointObject、CArea、CLineObject）
- **SSEditBase** — 编辑器基类（CDlgBase）
- **SSExchange** — 数据交换
- **SSProject** — 项目管理
- **SSCtrlBar** — 控制条
- **SSAdoBase** — 数据库接口
- **SSFormBase** — 表单基类
- **MFC42** — MFC 库
- **KERNEL32 / USER32 / GDI32** — Windows API
- **BCGCBPRO940** — BCGControlBar Pro UI（通过 SSEditBase 间接引入）

### func_query: CForestryInterface 发现

**核心类:** `CForestryInterface` — 林业模块的主接口类（继承自 CBCGPDialog）

| 地址 | 函数名 | 大小 | 说明 |
|------|--------|------|------|
| 0x1002a550 | ??0CForestryInterface@@QAE@XZ | 0x63 | 构造 |
| 0x1002a640 | ??1CForestryInterface@@UAE@XZ | 0xb | 析构 |
| 0x1002a650 | ?AddRibbonCategory@CForestryInterface@@UAEXXZ | 0xb60 | **添加 Ribbon 类别** — 主入口函数！ |
| 0x1002b1d0 | ?RemoveRibbonCategory@CForestryInterface@@UAEXXZ | 0x59 | 移除 Ribbon 类别 |
| 0x1002b230 | ?ExecFunction@CForestryInterface@@UAEPAXVCString@@AAV2@I@Z | 0x2157 | **执行林业命令** — 最大的函数（8535字节） |
| 0x1002da40 | ?RegisterCommand@CForestryInterface@@AAEXXZ | 0xcda | 注册命令 |
| 0x1002e720 | ?OnUpdateCmdUI@CForestryInterface@@UAEHPAVCCmdUI@@@Z | 0x8 | UI 命令更新 |
| 0x1002e730 | ?OnDraw@CForestryInterface@@UAEXPAVCDC@@@Z | 0x8 | 绘制 |
| 0x1002e740 | ?OnViewSize@CForestryInterface@@UAEXVCRect@@@Z | 0x3 | 视图大小变化 |

> **关键发现:** `CForestryInterface::ExecFunction` 是林业模块的中央调度函数，大小 0x2157 (8535字节)，负责分发所有林业相关命令。

### func_query: Tree / CTreeItemSite 发现

**TreeItem 站点管理（EPS 通用树控件）：**

| 地址 | 函数名 | 说明 |
|------|--------|------|
| 0x10004b70 | ?SetData@CTreeItemSite@@UAEXAAVCUIntArray@@AAVCStringArray@@@Z | 设置数据 |
| 0x10004b80 | ?GetObjIDList@CTreeItemSite@@UAEXAAVCUIntArray@@@Z | 获取对象ID列表 |
| 0x10004b90 | ?GetSelectedItem@CTreeItemSite@@UAEHAAV?$CSSPtrArray@VTSS_LC_ITEM@@@@@Z | 获取选中项 |
| 0x10004ba0 | ?GetFindString@CTreeItemSite@@UAEXAAVCStringArray@@@Z | 获取查找字符串 |
| 0x10004bb0 | ?Find@CTreeItemSite@@UAEXVCString@@@Z | 查找 |
| 0x10004bc0 | ?SetParentTreeItem@CTreeItemSite@@QAEXPAVCTreeItem@@@Z | 设置父树项 |
| 0x10004bd0 | ?SetParentWnd@CTreeItemSite@@QAEXPAVCWnd@@@Z | 设置父窗口 |
| 0x10004be0 | ?GetParentTreeItem@CTreeItemSite@@QAEPAVCTreeItem@@XZ | 获取父树项 |
| 0x10004bf0 | ?GetParentWnd@CTreeItemSite@@QAEPAVCWnd@@XZ | 获取父窗口 |
| 0x10004c00 | ?GetSiteInfo@CTreeItemSite@@UAE?AVCString@@XZ | 获取站点信息 |
| 0x10004c30 | ?SetSiteInfo@CTreeItemSite@@UAEXVCString@@@Z | 设置站点信息 |
| 0x10004c80 | ??0CTreeItemSite@@QAE@ABV0@@Z | 构造 |
| 0x10004de0 | ?GetParentTreeItem@CSSListCtrl@@QAEPAVCTreeItem@@XZ | CSS 列表控件 |
| 0x10004e40 | ?GetParentTreeItem@CSSTableCtrl@@QAEPAVCTreeItem@@XZ | CSS 表格控件 |
| 0x10004e80 | ?GetItemRect@CTreeItem@@QAE?AVCRect@@XZ | 获取项矩形 |
| 0x10004eb0 | ?GetObjIDList@CTreeItem@@QAEPAVCUIntArray@@XZ | 获取对象ID列表 |
| 0x10004f30 | ?GetParameterList@CTreeItem@@QAEPAVCStringArray@@XZ | 获取参数列表 |
| 0x10004f40 | ?IsChartGraphType@CTreeItem@@QAEHXZ | 是否图表类型 |
| 0x10004f60 | ?HasChildItems@CTreeItem@@QAEHXZ | 是否有子项 |
| 0x10005080 | ?IsSaveToFile@CTreePage@@QAEHXZ | 是否保存到文件 |
| 0x10005090 | ?GetFilePathName@CTreePage@@QAE?AVCString@@XZ | 获取文件路径 |

### func_query: 林业/中文关键词搜索
> 搜索 '林业'、'森林'、'Wood'、'Vegetation' 等关键词

**结果:** 0 个精确匹配函数

> 说明：SSForestry.dll 中的林业功能命名采用英文或缩写（如 CForestryInterface::AddRibbonCategory/ExecFunction），中文关键词未在函数名中出现。该模块更多是调用 SSEdit/SSCore 中的几何和地图功能来实现林业业务逻辑。

---

## 汇总对比

| 指标 | BCGCBPRO940d.dll | SSEdit.dll | SSForestry.dll |
|------|-------------------|------------|-----------------|
| 大小 | 122.7 MB | 37.7 MB | 34.8 MB |
| 调用图边数 | 47,775 | 52,775 | ~52,000 |
| 核心角色 | UI 框架层 | 核心业务层 | 业务模块层 |
| 主要类 | CBCGP* (140+) | CDlgBase, CSelection, CScaleMap | CForestryInterface, CTreeItem |
| 架构特点 | BCGControlBar Pro + EPS 扩展 | 地理对象管理 + 表单控件 | 林业业务 + EPS 接口集成 |

### 关键发现

1. **BCGCBPRO940d.dll** — 纯粹的 UI 框架，提供 Edit/Ribbon/Grid/Property/Button/Dock 等控件
2. **SSEdit.dll** — EPS 编辑器的核心，地理对象管理、选择集、地图操作、表单报表
3. **SSForestry.dll** — 林业模块，通过 `CForestryInterface::AddRibbonCategory` 将自己集成到 EPS Ribbon UI，通过 `CForestryInterface::ExecFunction` 分发林业命令（0x2157 字节的大型函数）
4. **三 DLL 均依赖 BCGControlBar Pro** — EPS 的 UI 框架统一使用 BCGControlBar Pro 9.40
5. **跨 DLL 调用链:** SSForestry → SSEdit → SSCore32/SSMap（业务→核心→计算）

---
*报告生成时间: 2026-03-23 19:58 GMT+8*
