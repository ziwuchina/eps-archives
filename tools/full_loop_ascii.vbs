' full_loop_ascii.vbs - Complete closed-loop test on ASCII path
' CreateObject -> InitWorkSpace(ASCII) -> PushUndoMark -> CreateNewObjByCode ->
' AddNewObjPoint -> AddNewObjToSaveObjList -> SaveBufferObjToDatabase -> CloseAllEdb
Option Explicit
On Error Resume Next
Dim epsApp, SSProcess
Dim fso, out
Set fso = CreateObject("Scripting.FileSystemObject")
Set out = fso.CreateTextFile("D:\AIcode\mcpida\wrapper\full_loop_ascii_out.txt", True, True)

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

' Open workspace with ASCII path
Err.Clear
epsApp.InitWorkSpace "D:\eps_com_test\test_shunde_loop.edb", ""
out.WriteLine "4 InitWorkSpace(ASCII) err=" & Err.Number & " " & Err.Description

WScript.Sleep 5000

Err.Clear
SSProcess.UpdateCurMap 0
out.WriteLine "5 UpdateCurMap err=" & Err.Number

' --- Closed loop: create object and save to database ---
Err.Clear
SSProcess.PushUndoMark
out.WriteLine "6 PushUndoMark err=" & Err.Number & " " & Err.Description

' Create object by code 831000 (elevation point) - CHM official recipe
Err.Clear
SSProcess.CreateNewObjByCode 831000
out.WriteLine "7 CreateNewObjByCode(831000) err=" & Err.Number & " " & Err.Description

' Add vertex points
Err.Clear
SSProcess.AddNewObjPoint 1000.01, 1000.34, 22.45, 0, ""
out.WriteLine "8 AddNewObjPoint(1) err=" & Err.Number

Err.Clear
SSProcess.AddNewObjPoint 1001.01, 1000.34, 22.45, 0, ""
out.WriteLine "9 AddNewObjPoint(2) err=" & Err.Number

Err.Clear
SSProcess.AddNewObjPoint 1000.51, 1001.34, 22.45, 0, ""
out.WriteLine "10 AddNewObjPoint(3) err=" & Err.Number

' Add to save list
Err.Clear
SSProcess.AddNewObjToSaveObjList
out.WriteLine "11 AddNewObjToSaveObjList err=" & Err.Number & " " & Err.Description

' Save to database
Err.Clear
SSProcess.SaveBufferObjToDatabase
out.WriteLine "12 SaveBufferObjToDatabase err=" & Err.Number & " " & Err.Description

out.WriteLine "CLOSED LOOP COMPLETE - waiting 30s for screenshot"
out.Close

' Keep alive for screenshot
WScript.Sleep 30000

Err.Clear
epsApp.CloseAllEdb
WScript.Echo "done"
