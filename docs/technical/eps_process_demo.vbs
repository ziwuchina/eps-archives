
Dim epsApp,SSProcess,SSView,SSParameter

'执行函数
CreateNewEdb
'OpenExistEdb

'创建新EDB工程
Function CreateNewEdb()
  '创建Eps实例
  Set epsApp = CreateObject( "Eps.EpsApplication" )
  '显示Eps界面
  epsApp.SetVisible 1
  '获取EPS进程内脚本句柄
  Set SSProcess = epsApp.GetScriptDispatch("SScript.dll", "SSProcess")
  Set SSView = epsApp.GetScriptDispatch("SScript.dll", "SSProcessView")
  Set SSParameter=epsApp.GetScriptDispatch("SScript.dll", "SSParameter")	
  '指定新建工程名
  edbfileName = SSProcess.SelectFileName(0, "指定EDB工程名", 1, "Eps Files (*.edb)|*.edb|All Files (*.*)|*.*||")
  If edbfileName="" Then
    '关闭并退出EPS	
    epsApp.CloseAllEdb
    Exit Function
  End If
  Set fso = CreateObject("Scripting.FileSystemObject")
  If (fso.FileExists(edbfileName)) Then
      msgbox "指定工程名已存在！"
      '关闭并退出EPS	
      epsApp.CloseAllEdb
      exit Function
  End If
  '创建工程,此处需修改成相应的模板名称
  templateFileName = "长沙基础地理标准500.mdt"
  epsApp.InitWorkSpace edbfileName, templateFileName
  

  '更新当前Map句柄
  SSProcess.UpdateCurMap 0
  
  '创建点对象
  CreateOneObj 0, 100, 200 ,23.45
  CreateOneObj 0, 200, 300 ,23.45
 
  '关闭并退出EPS	
  epsApp.CloseAllEdb

End Function


'打开EDB工程
Function OpenExistEdb()
  '创建Eps实例
  Set epsApp = CreateObject( "Eps.EpsApplication" )
  '显示Eps界面
  epsApp.SetVisible 1
  '获取EPS进程内脚本句柄
  Set SSProcess = epsApp.GetScriptDispatch("SScript.dll", "SSProcess")
  Set SSView = epsApp.GetScriptDispatch("SScript.dll", "SSProcessView")
  Set SSParameter=epsApp.GetScriptDispatch("SScript.dll", "SSParameter")	
  '指定新建工程名
  edbfileName = SSProcess.SelectFileName(1, "指定EDB工程名", 1, "Eps Files (*.edb)|*.edb|All Files (*.*)|*.*||")
  If edbfileName="" Then
    '关闭并退出EPS	
    epsApp.CloseAllEdb
    Exit Function
  End If
  '打开EDB工程
  epsApp.InitWorkSpace edbfileName, ""
  

  '更新当前Map句柄
  SSProcess.UpdateCurMap 0
  
  '创建点对象
  CreateOneObj 0, 100, 200 ,23.45
  CreateOneObj 0, 200, 300 ,23.45
 
  '关闭并退出EPS	
  epsApp.CloseAllEdb

End Function


'创建一个点对象
Function CreateOneObj(code, x, y ,z)

  SSProcess.CreateNewObjByCode code
  SSProcess.AddNewObjPoint x, y, z, 0,""
  SSProcess.AddNewObjToSaveObjList
  SSProcess.SaveBufferObjToDatabase

End Function

