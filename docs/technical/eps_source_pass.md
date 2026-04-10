# EPS source pass (port=10000)

## Function hits by pattern
### *Script*
```json
{"total":5,"offset":0,"count":5,"items":[{"name":"?SetDescription@CBCGPBaseRibbonElement@@UAEXPBD@Z","start_ea":"0x42C296","end_ea":"0x42C29C"},{"name":"?SetDescription@CBCGPRibbonButton@@UAEXPBD@Z","start_ea":"0x42C452","end_ea":"0x42C458"},{"name":"?GetDescription@CBCGPBaseRibbonElement@@UBE?AVCString@@XZ","start_ea":"0x42C45E","end_ea":"0x42C464"},{"name":"?OnDrawDescription@CBCGPToolTipCtrl@@UAE?AVCSize@@PAVCDC@@VCRect@@H@Z","start_ea":"0x42C4A0","end_ea":"0x42C4A6"},{"name":"?SetDescription@CBCGPToolTipCtrl@@UAEXVCString@@@Z","start_ea":"0x42C4B8","end_ea":"0x42C4BE"}]}
```
### *Command*
```json
{"total":20,"offset":0,"count":20,"items":[{"name":"?OnCommand@CSSView@@MAEHIJ@Z","start_ea":"0x42A81A","end_ea":"0x42A820"},{"name":"?OnCommand@CWnd@@MAEHIJ@Z","start_ea":"0x42A92E","end_ea":"0x42A934"},{"name":"?GetCommandMap@CCmdTarget@@MBEPBUAFX_OLECMDMAP@@XZ","start_ea":"0x42A9FA","end_ea":"0x42AA00"},{"name":"?OnCommand@CFrameWnd@@MAEHIJ@Z","start_ea":"0x42AD24","end_ea":"0x42AD2A"},{"name":"?OnDDECommand@CWinApp@@UAEHPAD@Z","start_ea":"0x42AE98","end_ea":"0x42AE9E"},{"name":"??1CCommandLineInfo@@UAE@XZ","start_ea":"0x42AF70","end_ea":"0x42AF76"},{"name":"?ParseCommandLine@CWinApp@@QAEXAAVCCommandLineInfo@@@Z","start_ea":"0x42AFC4","end_ea":"0x42AFCA"},{"name":"??0CCommandLineInfo@@QAE@XZ","start_ea":"0x42AFCA","end_ea":"0x42AFD0"},{"name":"?OnCommand@CBCGPDialog@@MAEHIJ@Z","start_ea":"0x42B828","end_ea":"0x42B82E"},{"name":"?SetMenuButtonSDLCommandMap@@YAXAAVCStringArray@@AAVCUIntArray@@@Z","start_ea":"0x42BA14","end_ea":"0x42BA1A"},{"name":"?OnCommand@CBCGPRibbonBar@@MAEHIJ@Z","start_ea":"0x42BCDE","end_ea":"0x42BCE4"},{"name":"?OnCommand@CBCGPOleIPFrameWnd@@MAEHIJ@Z","start_ea":"0x42BD56","end_ea":"0x42BD5C"},{"name":"?FillAllCommandsList@CBCGPToolbarCustomize@@UBEXAAVCListBox@@@Z","start_ea":"0x42BFE4","end_ea":"0x42BFEA"},{"name":"?OnCommand@CBCGPToolbarCustomize@@MAEHIJ@Z","start_ea":"0x42BFF6","end_ea":"0x42BFFC"},{"name":"?InCommand@CBCGPPopupMenu@@UAEHXZ","start_ea":"0x42C19A","end_ea":"0x42C1A0"},{"name":"?AddToListBox@CBCGPRibbonSeparator@@UAEHPAVCBCGPRibbonCommandsListBox@@H@Z","start_ea":"0x42C23C","end_ea":"0x42C242"},{"name":"?IsCommandAreaHighlighted@CBCGPRibbonButton@@UBEHXZ","start_ea":"0x42C2D8","end_ea":"0x42C2DE"},{"name":"?NotifyControlCommand@CBCGPBaseRibbonElement@@MAEHHHIJ@Z","start_ea":"0x42C308","end_ea":"0x42C30E"},{"name":"?AddToListBox@CBCGPRibbonButton@@MAEHPAVCBCGPRibbonCommandsListBox@@H@Z","start_ea":"0x42C38C","end_ea":"0x42C392"},{"name":"?GetSDLCommandParameter@@YA?AVCString@@I@Z","start_ea":"0x42C494","end_ea":"0x42C49A"}]}
```
### *Register*
```json
{"total":8,"offset":0,"count":8,"items":[{"name":"?GetRegisterSoftStatus@@YA?AVCString@@V1@@Z","start_ea":"0x42A64C","end_ea":"0x42A652"},{"name":"?IsRegisterCheckModel@CCheckManager@@UAEHVCString@@0@Z","start_ea":"0x42A748","end_ea":"0x42A74E"},{"name":"?RegisterCheckModel@CCheckManager@@UAEXPAVCCheckModel@@@Z","start_ea":"0x42A74E","end_ea":"0x42A754"},{"name":"?Register@COleTemplateServer@@UAEHXZ","start_ea":"0x42AE7A","end_ea":"0x42AE80"},{"name":"?RegisterAll@COleObjectFactory@@SGHXZ","start_ea":"0x42AF76","end_ea":"0x42AF7C"},{"name":"?RegisterShellFileTypes@CWinApp@@IAEXH@Z","start_ea":"0x42AF82","end_ea":"0x42AF88"},{"name":"?AfxOleRegisterServerClass@@YGHABU_GUID@@PBD11W4OLE_APPTYPE@@PAPBD3H11@Z","start_ea":"0x42AFD0","end_ea":"0x42AFD6"},{"name":"?Register@COleDropTarget@@QAEHPAVCWnd@@@Z","start_ea":"0x42B26A","end_ea":"0x42B270"}]}
```
### *Execute*
```json
{"total":1,"offset":0,"count":1,"items":[{"name":"?SDLFunctionExecute@@YAPAXVCString@@I@Z","start_ea":"0x42A784","end_ea":"0x42A78A"}]}
```
### *ToolBox*
```json
{"total":0,"offset":0,"count":0,"items":[]}
```
### *Vbs*
```json
{"total":0,"offset":0,"count":0,"items":[]}
```
## Decompiled candidates (first 15)
### 0x42C296
```cpp
[{"query":"0x42C296","name":"?SetDescription@CBCGPBaseRibbonElement@@UAEXPBD@Z","start_ea":"0x42C296","end_ea":"0x42C29C","decompiled":"// attributes: thunk\nvoid __thiscall CBCGPBaseRibbonElement::SetDescription(CBCGPBaseRibbonElement *this, const char *a2)\n{\n  __imp_?SetDescription@CBCGPBaseRibbonElement@@UAEXPBD@Z(this, a2);\n}\n"}]
```
### 0x42C452
```cpp
[{"query":"0x42C452","name":"?SetDescription@CBCGPRibbonButton@@UAEXPBD@Z","start_ea":"0x42C452","end_ea":"0x42C458","decompiled":"// attributes: thunk\nvoid __thiscall CBCGPRibbonButton::SetDescription(CBCGPRibbonButton *this, const char *a2)\n{\n  __imp_?SetDescription@CBCGPRibbonButton@@UAEXPBD@Z(this, a2);\n}\n"}]
```
### 0x42C45E
```cpp
[{"query":"0x42C45E","name":"?GetDescription@CBCGPBaseRibbonElement@@UBE?AVCString@@XZ","start_ea":"0x42C45E","end_ea":"0x42C464","decompiled":"// attributes: thunk\nint CBCGPBaseRibbonElement::GetDescription()\n{\n  return __imp_?GetDescription@CBCGPBaseRibbonElement@@UBE?AVCString@@XZ();\n}\n"}]
```
### 0x42C4A0
```cpp
[{"query":"0x42C4A0","name":"?OnDrawDescription@CBCGPToolTipCtrl@@UAE?AVCSize@@PAVCDC@@VCRect@@H@Z","start_ea":"0x42C4A0","end_ea":"0x42C4A6","decompiled":"// attributes: thunk\nint CBCGPToolTipCtrl::OnDrawDescription()\n{\n  return __imp_?OnDrawDescription@CBCGPToolTipCtrl@@UAE?AVCSize@@PAVCDC@@VCRect@@H@Z();\n}\n"}]
```
### 0x42C4B8
```cpp
[{"query":"0x42C4B8","name":"?SetDescription@CBCGPToolTipCtrl@@UAEXVCString@@@Z","start_ea":"0x42C4B8","end_ea":"0x42C4BE","decompiled":"// attributes: thunk\nint CBCGPToolTipCtrl::SetDescription()\n{\n  return __imp_?SetDescription@CBCGPToolTipCtrl@@UAEXVCString@@@Z();\n}\n"}]
```
### 0x42A81A
```cpp
[{"query":"0x42A81A","name":"?OnCommand@CSSView@@MAEHIJ@Z","start_ea":"0x42A81A","end_ea":"0x42A820","decompiled":"// attributes: thunk\nint __thiscall CSSView::OnCommand(CSSView *this, unsigned int a2, int a3)\n{\n  return __imp_?OnCommand@CSSView@@MAEHIJ@Z(this, a2, a3);\n}\n"}]
```
### 0x42A92E
```cpp
[{"query":"0x42A92E","name":"?OnCommand@CWnd@@MAEHIJ@Z","start_ea":"0x42A92E","end_ea":"0x42A934","decompiled":"// attributes: thunk\nint __thiscall CWnd::OnCommand(CWnd *this, unsigned int a2, int a3)\n{\n  return __imp_?OnCommand@CWnd@@MAEHIJ@Z(this, a2, a3);\n}\n"}]
```
### 0x42A9FA
```cpp
[{"query":"0x42A9FA","name":"?GetCommandMap@CCmdTarget@@MBEPBUAFX_OLECMDMAP@@XZ","start_ea":"0x42A9FA","end_ea":"0x42AA00","decompiled":"// attributes: thunk\nconst struct AFX_OLECMDMAP *__thiscall CCmdTarget::GetCommandMap(CCmdTarget *this)\n{\n  return __imp_?GetCommandMap@CCmdTarget@@MBEPBUAFX_OLECMDMAP@@XZ(this);\n}\n"}]
```
### 0x42AD24
```cpp
[{"query":"0x42AD24","name":"?OnCommand@CFrameWnd@@MAEHIJ@Z","start_ea":"0x42AD24","end_ea":"0x42AD2A","decompiled":"// attributes: thunk\nint __thiscall CFrameWnd::OnCommand(CFrameWnd *this, unsigned int a2, int a3)\n{\n  return __imp_?OnCommand@CFrameWnd@@MAEHIJ@Z(this, a2, a3);\n}\n"}]
```
### 0x42AE98
```cpp
[{"query":"0x42AE98","name":"?OnDDECommand@CWinApp@@UAEHPAD@Z","start_ea":"0x42AE98","end_ea":"0x42AE9E","decompiled":"// attributes: thunk\nint __thiscall CWinApp::OnDDECommand(CWinApp *this, char *a2)\n{\n  return __imp_?OnDDECommand@CWinApp@@UAEHPAD@Z(this, a2);\n}\n"}]
```
### 0x42AF70
```cpp
[{"query":"0x42AF70","name":"??1CCommandLineInfo@@UAE@XZ","start_ea":"0x42AF70","end_ea":"0x42AF76","decompiled":"// attributes: thunk\nvoid __thiscall CCommandLineInfo::~CCommandLineInfo(CCommandLineInfo *this)\n{\n  __imp_??1CCommandLineInfo@@UAE@XZ(this);\n}\n"}]
```
### 0x42AFC4
```cpp
[{"query":"0x42AFC4","name":"?ParseCommandLine@CWinApp@@QAEXAAVCCommandLineInfo@@@Z","start_ea":"0x42AFC4","end_ea":"0x42AFCA","decompiled":"// attributes: thunk\nvoid __thiscall CWinApp::ParseCommandLine(CWinApp *this, struct CCommandLineInfo *a2)\n{\n  __imp_?ParseCommandLine@CWinApp@@QAEXAAVCCommandLineInfo@@@Z(this, a2);\n}\n"}]
```
### 0x42AFCA
```cpp
[{"query":"0x42AFCA","name":"??0CCommandLineInfo@@QAE@XZ","start_ea":"0x42AFCA","end_ea":"0x42AFD0","decompiled":"// attributes: thunk\nCCommandLineInfo *__thiscall CCommandLineInfo::CCommandLineInfo(CCommandLineInfo *this)\n{\n  return __imp_??0CCommandLineInfo@@QAE@XZ(this);\n}\n"}]
```
### 0x42B828
```cpp
[{"query":"0x42B828","name":"?OnCommand@CBCGPDialog@@MAEHIJ@Z","start_ea":"0x42B828","end_ea":"0x42B82E","decompiled":"// attributes: thunk\nint __thiscall CBCGPDialog::OnCommand(CBCGPDialog *this, unsigned int a2, int a3)\n{\n  return __imp_?OnCommand@CBCGPDialog@@MAEHIJ@Z(this, a2, a3);\n}\n"}]
```
### 0x42BA14
```cpp
[{"query":"0x42BA14","name":"?SetMenuButtonSDLCommandMap@@YAXAAVCStringArray@@AAVCUIntArray@@@Z","start_ea":"0x42BA14","end_ea":"0x42BA1A","decompiled":"// attributes: thunk\nvoid __cdecl SetMenuButtonSDLCommandMap(struct CStringArray *a1, struct CUIntArray *a2)\n{\n  __imp_?SetMenuButtonSDLCommandMap@@YAXAAVCStringArray@@AAVCUIntArray@@@Z(a1, a2);\n}\n"}]
```