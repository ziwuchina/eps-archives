' ascii_test.vbs - English-only path test for InitWorkSpace
' Verifies whether Chinese path encoding blocks workspace loading.
' Uses D:\eps_com_test\test_shunde.edb (ASCII path, copy of 顺德数据.edb)
Option Explicit
On Error Resume Next
Dim epsApp, SSProcess
Dim fso, out
Set fso = CreateObject("Scripting.FileSystemObject")
Set out = fso.CreateTextFile("D:\AIcode\mcpida\wrapper\ascii_test_out.txt", True, True)

Err.Clear
Set epsApp = CreateObject("Eps.EpsApplication")
If Err.Number <> 0 Then
    out.WriteLine "1 CreateObject ERR: " & Err.Number & " " & Err.Description
    out.Close: WScript.Quit 1
End If
out.WriteLine "1 CreateObject OK"

Err.Clear
epsApp.SetVisible 1
out.WriteLine "2 SetVisible err=" & Err.Number

Err.Clear
Set SSProcess = epsApp.GetScriptDispatch("SScript.dll", "SSProcess")
If Err.Number <> 0 Then
    out.WriteLine "3 SSProcess ERR: " & Err.Number & " " & Err.Description
    out.Close: WScript.Quit 1
End If
out.WriteLine "3 SSProcess OK"

' ASCII path, empty template name (avoid dead template popup)
Err.Clear
epsApp.InitWorkSpace "D:\eps_com_test\test_shunde.edb", ""
out.WriteLine "4 InitWorkSpace(ASCII) err=" & Err.Number & " " & Err.Description

WScript.Sleep 5000

Err.Clear
Dim am
am = epsApp.GetActiveMap
out.WriteLine "5 GetActiveMap=" & am & " err=" & Err.Number

Err.Clear
Dim mw
mw = epsApp.GetMainWnd
out.WriteLine "6 GetMainWnd=" & mw & " err=" & Err.Number

Err.Clear
SSProcess.UpdateCurMap 0
out.WriteLine "7 UpdateCurMap err=" & Err.Number

Err.Clear
Dim st
st = SSProcess.GetMapStatus
out.WriteLine "8 GetMapStatus=" & st & " err=" & Err.Number

' PushUndoMark - the key indicator: if workspace truly loaded, this should NOT be RPC_E_SERVERFAULT
Err.Clear
SSProcess.PushUndoMark
out.WriteLine "9 PushUndoMark err=" & Err.Number & " " & Err.Description

out.WriteLine "ASCII TEST COMPLETE - waiting 30s for screenshot"
out.Close

' Keep alive so screenshot can capture the EPS window state
WScript.Sleep 30000

epsApp.CloseAllEdb
WScript.Echo "done"
