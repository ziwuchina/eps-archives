# EPS VBS 开发手册

---

## 第一部分：API 功能参考

## 数据导入导出

> 管理EPS与外部数据格式（DWG/SHP/MIF/EDB等）之间的数据转换

### `SetDataXParameter`

**功能：** 设置数据转换参数（如格式、版本、编码对照表等）

- **调用次数：** 237,145
- **使用文件数：** 681

**示例：**

```vbs
'设置导入文件格式为DWG
		SSProcess.SetDataXParameter "DataType", "1"
		SSProcess.SetDataXParameter "ImportPathName", DWGfileName
      SSProcess.SetDataXParameter "ImportPathName", filenames(i)
```

---

### `ClearDataXParameter`

**功能：** 清空所有数据转换参数

- **调用次数：** 730
- **使用文件数：** 681

**示例：**

```vbs
'清空转换参数
		SSProcess.ClearDataXParameter
		'设置导入文件格式为DWG
		SSProcess.SetDataXParameter "DataType", "1"
```

---

### `CloseDatabase`

**功能：** 关闭当前打开的数据库

- **调用次数：** 482
- **使用文件数：** 271

**示例：**

```vbs
'关闭新打开的数据,并自动还原初始数据库
		  SSProcess.CloseDatabase
       Next
		msgbox "调入完成！"
```

---

### `ExportData`

**功能：** 将当前工程数据导出为指定格式

- **调用次数：** 442
- **使用文件数：** 416

**示例：**

```vbs
SSProcess.SetDataXParameter "TableFieldDef"&CStr(AddOne(startIndex)),"ASSIST,1,ObjectName,ObjectName,NAME:1000,,,dbText,50,0"
		SSProcess.ExportData
		MSGBOX "输出完成"
End Sub
```

---

### `OpenDatabase`

**功能：** 打开指定的EDB数据库文件

- **调用次数：** 414
- **使用文件数：** 245

**示例：**

```vbs
SSProcess.OpenDatabase ctname
    SSProcess.WriteEpsDBIni "ERPManager", "ERP_YIID" , IID
```

---

### `SelectPathName`

**功能：** 弹出目录选择对话框

- **调用次数：** 283
- **使用文件数：** 262

**示例：**

```vbs
Dim arArray2(100),ncount2
	pathname = SSProcess.SelectPathName()
	if pathname = "" then exit sub
	mdbname = pathname&"QQ群维护记录.mdb"
```

---

### `SelectFileName`

**功能：** 弹出文件选择对话框，返回用户选择的文件路径

- **调用次数：** 279
- **使用文件数：** 261

**示例：**

```vbs
'选择用于转换的编码对照表
  'fileName = SSProcess.SelectFileName(1,"",0,"TXT Files(*.txt)|*.txt|All Files (*.*)|*.*||")
	fileName =	SSProcess.GetSysPathName (8) &"CASS9导入编码对照表.txt"
	'msgbox  fileName
```

---

### `CreateDatabase`

**功能：** 创建新的EDB数据库文件

- **调用次数：** 187
- **使用文件数：** 186

**示例：**

```vbs
End If
		  SSProcess.CreateDatabase "佛山市基础地理模板_500.MDT", edbFileName
  		  LoadOneFile filenames(i)
  		  '关闭新打开的数据,并自动还原初始数据库
```

---

### `ImportData`

**功能：** 导入数据文件（DWG/SHP/MIF等）到当前工程

- **调用次数：** 145
- **使用文件数：** 145

**示例：**

```vbs
'开始导入数据
		SSProcess.ImportData
	next
```

---

### `ImportDataFromStream`

**功能：** 从数据流导入数据

- **调用次数：** 133
- **使用文件数：** 133

**示例：**

```vbs
SSProcess.SetDataXParameter "SaveAttrToMemoData","1"
			  SSProcess.ImportDataFromStream zdtgraphicinfo
           '处理图形升级
				SSProcess.PushUndoMark
```

---

### `GetImportFileName`

**功能：** 获取最后一次导入的文件名

- **调用次数：** 38
- **使用文件数：** 38

**示例：**

```vbs
exportFileName = SSProcess.GetImportFileName
      If exportFileName<> "" Then
				exePath = Chr(34) & SSProcess.GetSysPathName (0 ) & "\ConvertDwg\ConvertToR14.exe" & Chr(34)
```

---

### `ExportDataToStream`

**功能：** 将数据导出到数据流

- **调用次数：** 10
- **使用文件数：** 10

**示例：**

```vbs
SSProcess.SetDataXParameter "ExportAttrMode","2"
				SSProcess.ExportDataToStream  byteObjList
				adoRs(3) = byteObjList
```

---

### `ImportDataFromStream4House`

- **调用次数：** 3
- **使用文件数：** 2

**示例：**

```vbs
addtoSelection = 1 '1：数据只加入到选择集       0：下载数据
         SSProcess.ImportDataFromStream4House  dateType,  addtoSelection, lcgraphicinfo
          noteCount=SSProcess.GetSelNoteCount
```

---

### `ExportDataToStream4House`

- **调用次数：** 3
- **使用文件数：** 2

**示例：**

```vbs
fromSelection = 1
				SSProcess.ExportDataToStream4House dateType,  fromSelection ,byteObjList
				adoRs(0) = byteObjList
				adoRs.update
```

---

## 选择集操作

> 管理EPS脚本选择集——用于筛选、遍历和操作地图上的对象

### `SetSelectCondition`

**功能：** 设置选择过滤条件（如按地物类型、编码等）

- **调用次数：** 14,935
- **使用文件数：** 2433

**示例：**

```vbs
SSProcess.ClearSelectCondition
		SSProcess.SetSelectCondition "SSObj_Type", "==", "POINT,LINE,AREA"
		SSProcess.SetSelectCondition "SSObj_DataMark", "<>", "OK"
		SSProcess.SelectFilter
```

---

### `GetSelGeoValue`

**功能：** 获取选择集中指定对象的属性值

- **调用次数：** 14,437
- **使用文件数：** 2344

**示例：**

```vbs
'得到扩展属性中的字段的值
			strID  =  SSProcess.GetSelGeoValue(i, "SSObj_ID")
			strObjType = SSProcess.GetSelGeoValue(i, "SSObj_Type")
			'MemoData = SSProcess.GetSelGeoValue(i, "SSObj_MemoData")      '扩展外部属性
```

---

### `ClearSelection`

**功能：** 清空当前选择集

- **调用次数：** 7,520
- **使用文件数：** 2713

**示例：**

```vbs
SSProcess.PushUndoMark
		SSProcess.ClearSelection
		SSProcess.ClearSelectCondition
		SSProcess.SetSelectCondition "SSObj_Type", "==", "POINT,LINE,AREA"
```

---

### `ClearSelectCondition`

**功能：** 清除选择过滤条件

- **调用次数：** 7,515
- **使用文件数：** 2659

**示例：**

```vbs
SSProcess.ClearSelection
		SSProcess.ClearSelectCondition
		SSProcess.SetSelectCondition "SSObj_Type", "==", "POINT,LINE,AREA"
		SSProcess.SetSelectCondition "SSObj_DataMark", "<>", "OK"
```

---

### `SelectFilter`

**功能：** 执行选择过滤，将符合条件的对象加入选择集

- **调用次数：** 6,658
- **使用文件数：** 2427

**示例：**

```vbs
SSProcess.SetSelectCondition "SSObj_DataMark", "<>", "OK"
		SSProcess.SelectFilter
		geocount = SSProcess.GetSelGeoCount()
   If geocount > 0 Then
```

---

### `GetSelGeoCount`

**功能：** 获取选择集中图形对象的数量

- **调用次数：** 4,514
- **使用文件数：** 2376

**示例：**

```vbs
SSProcess.SelectFilter
		geocount = SSProcess.GetSelGeoCount()
   If geocount > 0 Then
	  '锁定数据库
```

---

### `GetSelGeoPoint`

**功能：** 获取选择集中指定对象的坐标点

- **调用次数：** 2,118
- **使用文件数：** 935

**示例：**

```vbs
geocount=SSProcess.GetSelGeoPointCount(lsjl)
		SSProcess.GetSelGeoPoint lsjl, 0, xf,  yf,  z,  ptype,  name
		SSProcess.GetSelGeoPoint lsjl, geocount-1, xl,  yl,  z,  ptype,  name
		If abs(xf-xl)<0.001 And abs(yf-yl)<0.001 Then
```

---

### `ChangeSelectionObjAttr`

**功能：** 修改选择集中对象的属性

- **调用次数：** 1,395
- **使用文件数：** 399

**示例：**

```vbs
'SSProcess.UpdateSysSelection 1
   SSProcess.ChangeSelectionObjAttr "SSObj_Code", "7101023"
      SSProcess.PushUndoMark
      SSProcess.ClearSelection
```

---

### `UpdateSysSelection`

**功能：** 更新系统选择集

- **调用次数：** 1,375
- **使用文件数：** 1065

**示例：**

```vbs
geoCount = SSProcess.GetSelGeoCount()
		'SSProcess.UpdateSysSelection 1
		For i=0 To geoCount-1
				polygonID = SSProcess.GetSelGeoValue( i, "SSObj_ID" )
```

---

### `DeleteSelectionObj`

**功能：** 删除选择集中的所有对象

- **调用次数：** 1,042
- **使用文件数：** 619

**示例：**

```vbs
SSProcess.SelectFilter
				 SSProcess.DeleteSelectionObj
				 SSProcess.ClearSelection
```

---

### `GetSelGeoPointCount`

**功能：** 获取选择集中指定对象的坐标点数

- **调用次数：** 922
- **使用文件数：** 568

**示例：**

```vbs
yids=SSProcess.GetSelGeoValue (lsjl, "SSObj_ID")
		geocount=SSProcess.GetSelGeoPointCount(lsjl)
		SSProcess.GetSelGeoPoint lsjl, 0, xf,  yf,  z,  ptype,  name
		SSProcess.GetSelGeoPoint lsjl, geocount-1, xl,  yl,  z,  ptype,  name
```

---

### `GetSelNoteValue`

**功能：** 获取选择集中注记的属性值

- **调用次数：** 922
- **使用文件数：** 354

**示例：**

```vbs
'得到扩展属性中的字段的值
			strID  =  SSProcess.GetSelNoteValue (i, "SSObj_ID")
			strUserCode = GetNoteNextValueByPreviousValue(i,"SOUTH")
			  '根据用户编码得到对应的EPS分类号
```

---

### `ClearSelectConditionGroups`

- **调用次数：** 696
- **使用文件数：** 372

**示例：**

```vbs
SSProcess.ClearSelectCondition
      SSProcess.ClearSelectConditionGroups
      'SSProcess.SetSelectCondition "SSObj_Type", "<>", "POINT,NOTE"
SSProcess.SetSelectCondition "SSObj_Type", "=", "LINE"
```

---

### `GetSelNoteCount`

**功能：** 获取选择集中注记的数量

- **调用次数：** 664
- **使用文件数：** 400

**示例：**

```vbs
SSProcess.SelectFilter
	geocount = SSProcess.GetSelNoteCount()
   If geocount > 0 Then
	  '锁定数据库
```

---

### `ClearSysSelection`

**功能：** 清空系统选择集

- **调用次数：** 616
- **使用文件数：** 280

**示例：**

```vbs
SSProcess.ClearSysSelection
	SSProcess.ClearSelection
	SSProcess.ClearSelectCondition
```

---

### `SetSelGeoValue`

**功能：** 设置选择集中指定对象的属性值

- **调用次数：** 509
- **使用文件数：** 143

**示例：**

```vbs
If    objCode(0) <> "" Then
							SSProcess.SetSelGeoValue i, "SSObj_Code", objCode(0)
							SSProcess.SetSelGeoValue i, "SSObj_Reverse", objCode(1)
						 	SSProcess.SetSelGeoValue i, "SSObj_DataMark", "OK"
```

---

### `SetSelectConditionGroup`

- **调用次数：** 364
- **使用文件数：** 83

**示例：**

```vbs
SSProcess.SetSelectCondition "SSObj_Code", "==", "3103013"
SSProcess.SetSelectConditionGroup "房屋面内注记", "SSObj_Type", "==", "NOTE"
SSProcess.SetSelectConditionGroup "房屋面内注记", "SSObj_FontClass", "==", "3990022"
'SSProcess.SetSelectConditionGroup "房屋面内注记", "SSObj_FontWidth", "==", "300"
```

---

### `GetSelNotePoint`

**功能：** 获取注记的坐标点

- **调用次数：** 238
- **使用文件数：** 172

**示例：**

```vbs
zjnr=SSProcess.GetSelNoteValue(i,"SSObj_FontString")   '获得注记的注记内容
            SSProcess.GetSelNotePoint i,0,x,y,z,pt,pn     '获得注记的注记坐标
            drawpoint 3111001,x,y,zjnr,"[地址]"   '绘制点符号
            SSProcess.DeleteObject id    '绘制点后，删除原注记
```

---

### `SetSelNoteValue`

**功能：** 设置选择集中注记的属性值

- **调用次数：** 222
- **使用文件数：** 71

**示例：**

```vbs
If objCode(0) <> ""  Then
					 SSProcess.SetSelNoteValue i, "SSObj_FontClass", objCode(0)
						Erase objCode
              		'set strUserCode = Nothing
```

---

### `DelSelNote`

**功能：** 删除注记

- **调用次数：** 188
- **使用文件数：** 104

**示例：**

```vbs
If dist<2 Then
                                           SSProcess.DelSelNote i
                                           Exit For
                                   End If
```

---

### `AddSelGeoToSaveGeoList`

**功能：** 将选择集中的图形加入保存列表

- **调用次数：** 187
- **使用文件数：** 175

**示例：**

```vbs
SSProcess.AddSelGeoToSaveGeoList i
				End If
```

---

### `SelGeoGotoPoints`

**功能：** 将视图定位到选择集中的对象

- **调用次数：** 143
- **使用文件数：** 143

**示例：**

```vbs
If ZGS<>1 Then Msgbox "选择违法宗地，且只能选择一个违法宗地"  :  Exit Function
    SSProcess.SelGeoGotoPoints GotoPointi,1
	zdcode=SSProcess.GetObjectAttr (ZDID,"SSObj_Code")
	'图廓层解析
```

---

### `SelectionObjTopProcess`

**功能：** 对选择集进行拓扑处理

- **调用次数：** 125
- **使用文件数：** 125

**示例：**

```vbs
SSProcess.SelectFilter
    ' SSProcess.SelectionObjTopProcess "2", "临时拓扑", 0.005, 0
	Topologyarea "6801074","2","临时拓扑","拓扑构面"
```

---

### `ShowSelectMenu1`

- **调用次数：** 106
- **使用文件数：** 53

**示例：**

```vbs
If Len(BZWZ)<1 Then
       BZWZ = SSProcess.ShowSelectMenu1 (ZJBT,zjnr,RGB(127,223,255),RGB(255,255,0) )
        End If
        SSProcess.CreateNewObj 3
```

---

### `SelectionObjClip`

**功能：** 裁剪选择集中的对象

- **调用次数：** 99
- **使用文件数：** 64

**示例：**

```vbs
SSProcess.SelectFilter
	SSProcess.SelectionObjClip cjkid ,1, 0.005'执行裁剪，裁外
    '图形范围全视
    SSProcess.ExecuteSDLFunction "$SDL.SSProject.View.Extend", 0
```

---

### `AddClipBoardObjToMap`

- **调用次数：** 99
- **使用文件数：** 66

**示例：**

```vbs
Sub OnClick()
		SSProcess.AddClipBoardObjToMap -123456789, -123456789
End Sub
```

---

### `SetSelGeoPoint`

**功能：** 设置选择集中指定对象的坐标点

- **调用次数：** 95
- **使用文件数：** 82

**示例：**

```vbs
if (ptype_lastpt or 1)= ptype_lastpt then
				SSProcess.SetSelGeoPoint  lsjl, geocount-1, xl, yl, z1, "0", name1
				changemark = -99 '最后一个点原来是实测修改为非实测（常规面第一个点和最后一个点重合，复合面和镂空面特例）
			end if
```

---

### `SelectionObjToClipBoard`

- **调用次数：** 81
- **使用文件数：** 67

**示例：**

```vbs
'选择集对象放入粘贴板
      SSProcess.SelectionObjToClipBoard
End Sub
```

---

### `SelectionObjMerge`

**功能：** 合并选择集中的对象

- **调用次数：** 76
- **使用文件数：** 70

**示例：**

```vbs
If getcount0>1 Then
		SSProcess.SelectionObjMerge 0,"",0.05,1
		SSProcess.ClearSelection
		SSProcess.ClearSelectCondition
```

---

### `ResetSelGeoByCode`

- **调用次数：** 70
- **使用文件数：** 60

**示例：**

```vbs
end if
						SSProcess.ResetSelGeoByCode i,objCode(0)
						Erase objCode
                  'set strUserCode = Nothing
```

---

### `LockSelGeoPoint`

**功能：** 锁定/解锁选择集中对象的坐标点

- **调用次数：** 69
- **使用文件数：** 35

**示例：**

```vbs
SSProcess.LockSelGeoPoint i, 1
			For j=0 To pointCount-1
					SSProcess.GetSelGeoPoint i, j, x, y, z, ptype, pname
```

---

### `ShowSelectMenu`

**功能：** 显示选择菜单供用户选择

- **调用次数：** 66
- **使用文件数：** 35

**示例：**

```vbs
end if
		selitem = SSProcess.ShowSelectMenu (subpathstr)
		'If selitem="" Then Exit Sub
	end if
```

---

### `GetSelPolygonFocus`

- **调用次数：** 57
- **使用文件数：** 54

**示例：**

```vbs
geoID = SSProcess.GetSelGeoValue(i, "SSObj_ID")
		SSProcess.GetSelPolygonFocus i, x,  y,  z
		name = SSProcess.GetSelGeoValue(i, "[MJKMC]")
		if name <> "住宅单元" And name <> "商铺"And name <>  "车库" And name <>  "车位"And name <>  "摩托车位" And name <>  "办公室" And name <>  "写字楼" And name <>  "阁楼" And name <>  "杂物间" And name <>  "商场" And name <>  "店面" And name <>  "铺位" And name <>  "阳台" And name <> "全阳" And  name <>  "半阳" And  name <> "阳"  Then
```

---

### `AddSelNoteToSaveNoteList`

- **调用次数：** 51
- **使用文件数：** 51

**示例：**

```vbs
End if
							SSProcess.AddSelNoteToSaveNoteList i
							fontclass = ""
					Next
```

---

### `LockSelNotePoint`

- **调用次数：** 50
- **使用文件数：** 25

**示例：**

```vbs
pointCount = SSProcess.GetSelNotePointCount (i)
         SSProcess.LockSelNotePoint i, 1
			For j=0 To pointCount-1
					SSProcess.GetSelNotePoint i, j, x, y, z, ptype, pname
```

---

### `GetSelNotePointCount`

- **调用次数：** 40
- **使用文件数：** 39

**示例：**

```vbs
geoType = SSProcess.GetSelNoteValue(j, "SSObj_Type")
		pointcount = SSProcess.GetSelNotePointCount(j)
		'msgbox pointcount
		SSProcess.GetSelNotePoint id, 0, x,  y,  z,  ptype,  name
```

---

### `ResetSelNoteByFontClass`

- **调用次数：** 40
- **使用文件数：** 40

**示例：**

```vbs
' SSProcess.SetSelNoteValue i, "SSObj_FontClass", epscode
                         SSProcess.ResetSelNoteByFontClass i, epscode
                  End If
```

---

### `ExplodeSelectionObj`

**功能：** 分解选择集中的复合对象

- **调用次数：** 39
- **使用文件数：** 39

**示例：**

```vbs
SSProcess.SelectFilter
	SSProcess.ExplodeSelectionObj 1,1, ""
End Function
```

---

### `SetSelNotePoint`

**功能：** 设置注记的坐标点

- **调用次数：** 32
- **使用文件数：** 31

**示例：**

```vbs
SSProcess.LongiLatiToxyCGCS2000 114, pB, pL , pX, pY
               SSProcess.SetSelNotePoint i, j,  pX, pY, z, ptype, pname
			Next
         SSProcess.UpdateSelNotePoint i
```

---

### `UpdateSelGeoPoint`

- **调用次数：** 31
- **使用文件数：** 31

**示例：**

```vbs
Next
         SSProcess.UpdateSelGeoPoint i
         SSProcess.AddSelGeoToSaveGeoList i
         SSProcess.LockSelGeoPoint i, 0
```

---

### `UpdateSelNotePoint`

- **调用次数：** 25
- **使用文件数：** 25

**示例：**

```vbs
Next
         SSProcess.UpdateSelNotePoint i
         SSProcess.AddSelNoteToSaveNoteList i
         SSProcess.LockSelNotePoint i,0
```

---

### `DelSelGeo`

- **调用次数：** 22
- **使用文件数：** 14

**示例：**

```vbs
For i=0 To geocount-1
             SSProcess.DelSelGeo i
         Next
```

---

### `DeleteSelGeoPoint`

- **调用次数：** 20
- **使用文件数：** 20

**示例：**

```vbs
SSProcess.XYSA x, y, x0, y0, dist1, angle1, 0
			If abs(angle0 - angle1)<0.01 Then SSProcess.DeleteSelGeoPoint i, j
		Next
		SSProcess.AddSelGeoToSaveGeoList i
```

---

### `RebuildSelectionTopRelation`

- **调用次数：** 13
- **使用文件数：** 3

**示例：**

```vbs
SSProcess.SelectFilter
      SSProcess.RebuildSelectionTopRelation "地类图斑", "地类界线",  0.001
End Function
```

---

### `SelectionObjPartZ`

- **调用次数：** 5
- **使用文件数：** 5

**示例：**

```vbs
next
	SSProcess.SelectionObjPartZ  '范围线节点内插高程
	'图形重新生成
	SSProcess.ExecuteSDLFunction"$SDL.SSProject.Display.RedrawExtend",0
```

---

### `Selection`

- **调用次数：** 4
- **使用文件数：** 4

**示例：**

```vbs
Dim selection
    Set selection = SSProcess.Selection '获取选择集
    If selection.Count > 0 Then
        MsgBox "当前选中了 " & selection.Count & " 个对象。"
```

---

### `SelectionObjOrderby`

- **调用次数：** 3
- **使用文件数：** 3

**示例：**

```vbs
'排序
		'SSProcess.SelectionObjOrderby orderbyMode, refpointx, refpointy
		if ResVal_Dlg = 1 then
```

---

### `SelectionObjInnerInsertPoint`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
'SSProcess.UpdateSysSelection 0
		SSProcess.SelectionObjInnerInsertPoint jianju
		'SSProcess.ClearSelection
```

---

### `FilterSelectionObjVertex`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
SSProcess.SelectFilter
	SSProcess.FilterSelectionObjVertex 0.001,0.001,1,1,1,1
	SSProcess.ClearSelection
	SSProcess.ClearSelectCondition
```

---

### `RemoveSelectionObjPoint`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
SSProcess.SelectFilter
  SSProcess.RemoveSelectionObjPoint 1,1
End Sub
```

---

## 对象属性操作

> 读写地图对象的属性（编码、图层、面积、自定义字段等）

### `GetObjectAttr`

**功能：** 获取指定对象的属性值（如编码、图层、面积等）

- **调用次数：** 7,721
- **使用文件数：** 1284

**示例：**

```vbs
If ids <> "" Then
						zjnr=SSProcess.GetObjectAttr( ids, "SSObj_FontString" )
'3分解注记
						jg=left(zjnr,1)
```

---

### `SetObjectAttr`

**功能：** 设置指定对象的属性值

- **调用次数：** 6,626
- **使用文件数：** 958

**示例：**

```vbs
'4赋属性
						SSProcess.SetObjectAttr polygonID, "[Structure]", jg
						SSProcess.SetObjectAttr polygonID, "[Story]", cs
'5删除注记
```

---

### `SetNewObjValue`

- **调用次数：** 6,516
- **使用文件数：** 531

**示例：**

```vbs
SSProcess.CreateNewObj  GeoType
			SSProcess.SetNewObjValue "SSObj_Code", g_OBJCode(0)
			SSProcess.SetNewObjValue "SSObj_LayerName", strLayername
			SSProcess.SetNewObjValue "SSObj_Color", strColor
```

---

### `GetObjectPoint`

**功能：** 获取对象的坐标点

- **调用次数：** 1,675
- **使用文件数：** 581

**示例：**

```vbs
SSProcess.GetObjectPoint objID, 0, x0,  y0,  z0,  ptype0,  name0
		for i = 1 to pointcount-1
			SSProcess.GetObjectPoint objID, i, x1,  y1,  z1,  ptype1,  name1
```

---

### `GetObjectFocusPoint`

**功能：** 获取对象的焦点坐标

- **调用次数：** 639
- **使用文件数：** 368

**示例：**

```vbs
If zbz=1 Then
            SSProcess.GetObjectFocusPoint id, zx, zy
            lzzdh=SSProcess.GetSelGeoValue(i,"[DJH]")
            If lzzdh<>Zdh Then
```

---

### `Getobjectattr`

- **调用次数：** 166
- **使用文件数：** 12

**示例：**

```vbs
for i=0 to idcount-1
		id=SSProcess.Getobjectattr(idarr(i),"SSObj_ID")
		djh=SSProcess.Getobjectattr(idarr(i),"[DJH]")
		zrzh=SSProcess.Getobjectattr(idarr(i),"[ZRZH]")
```

---

### `ChangeCodeCopySelectionObj`

**功能：** 修改选择集对象的编码并复制属性

- **调用次数：** 88
- **使用文件数：** 53

**示例：**

```vbs
next
	'SSProcess.ChangeCodeCopySelectionObj 3120033
	Dim lcstrs(500),lcids(500)
```

---

### `SetObjectPoint`

**功能：** 设置对象的坐标点

- **调用次数：** 85
- **使用文件数：** 54

**示例：**

```vbs
SSProcess.GetObjectPoint objID, i, x1,  y1,  z1,  ptype1,  name1
			SSProcess.SetObjectPoint objID, i, x1,  y1,  z0,  ptype1,  name1, 1
		next
```

---

### `setobjectattr`

- **调用次数：** 63
- **使用文件数：** 24

**示例：**

```vbs
SSProcess.setobjectattr id,"[SHBW]",shbw
				SSProcess.setobjectattr id ,"[djh]",djh
				SSProcess.setobjectattr id ,"[zrzh]",zrzh
```

---

### `ChangeCodeCopy`

- **调用次数：** 60
- **使用文件数：** 50

**示例：**

```vbs
maxid=SSProcess.GetGeoMaxID
			SSProcess.ChangeCodeCopy id,3120132
			maxid_1=SSProcess.GetGeoMaxID
			for k=maxid+1 to maxid_1
```

---

### `SetObjectBinaryAttr`

**功能：** 设置对象的二进制属性

- **调用次数：** 20
- **使用文件数：** 20

**示例：**

```vbs
If sts0(iii+1) <>"" Then
										SSProcess.SetObjectBinaryAttr id, "[" & sts0(iii) & "]", sts0(iii+1)
                        End If
                  End If
```

---

### `CopyObjectAttr`

**功能：** 复制对象属性到另一个对象

- **调用次数：** 17
- **使用文件数：** 17

**示例：**

```vbs
SSProcess.SaveBufferObjToDatabase
      SSProcess.CopyObjectAttr yid, id, 0, 1
End Function
```

---

### `Setobjectattr`

- **调用次数：** 15
- **使用文件数：** 9

**示例：**

```vbs
str="SYGN_1|" & sygn & "|QSXZ_1|" & qsxz & "|JZMJ_1|" & jzmj
			SSProcess.Setobjectattr id,"SSObj_MemoData",str
		end if
	Next
```

---

### `GetObjectBinaryAttr`

**功能：** 获取对象的二进制属性

- **调用次数：** 11
- **使用文件数：** 7

**示例：**

```vbs
attrField="[文件记录]"
				 dataValue = SSProcess.GetObjectBinaryAttr(geoID, attrField)
				 If  Len(dataValue) > 20 Then
						 pos = CLng(0)
```

---

### `UpdateObjAttrByFeatureCode`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
SSProcess.SelectFilter
      SSProcess.UpdateObjAttrByFeatureCode "FeatureCodeTB_2000", "Feature.Code=SSObj_Code", "SSObj_Color=Feature.LineColor,SSObj_LineWidth=Feature.LineWidth,SSObj_LayerName=Feature.LayerName,SSObj_Type=Feature.Type"
      '注记层,色重置
```

---

## 对象创建与删除

> 创建、添加和删除地图对象（点、线、面、注记等）

### `AddNewObjPoint`

**功能：** 为新对象添加坐标点

- **调用次数：** 3,797
- **使用文件数：** 713

**示例：**

```vbs
if  g_XYChange =  1 then
				SSProcess.AddNewObjPoint  g_strsObjMData(i,5), g_strsObjMData(i,6), g_strsObjMData(i,7), PointType, g_strsObjMData(i,3)&"_"&g_strsObjMData(i,4)         '函数使用的是数学坐标
			else
				SSProcess.AddNewObjPoint  g_strsObjMData(i,6), g_strsObjMData(i,5), g_strsObjMData(i,7), PointType, g_strsObjMData(i,3)&"_"&g_strsObjMData(i,4)        '函数使用的是数学坐标
```

---

### `AddNewObjToSaveObjList`

**功能：** 将新对象加入保存列表

- **调用次数：** 1,884
- **使用文件数：** 701

**示例：**

```vbs
If i > 0 Then
				SSProcess.AddNewObjToSaveObjList  '前一对象加入保存队列
			End if
			SSProcess.CreateNewObj  GeoType
```

---

### `CreateNewObjByCode`

**功能：** 通过编码创建新对象

- **调用次数：** 1,148
- **使用文件数：** 508

**示例：**

```vbs
Function drawpoint(byval pcode,byval x,byval y,byval zjnr,byval fieldname)
		SSProcess.CreateNewObjByCode pcode
		SSProcess.AddNewObjPoint x, y, 0, 0, ""
		SSProcess.SetNewObjValue fieldname, zjnr
```

---

### `DeleteObject`

**功能：** 删除指定对象

- **调用次数：** 1,088
- **使用文件数：** 482

**示例：**

```vbs
if SSObj_Z=121 then
						SSProcess.DeleteObject  polygonID
				end if
		next
```

---

### `CreateNewObjByClass`

**功能：** 通过分类创建新对象

- **调用次数：** 484
- **使用文件数：** 259

**示例：**

```vbs
Function notetable(byval x0,byval y0,byval str)
	SSProcess.CreateNewObjByClass "0"
	SSProcess.SetNewObjValue "SSObj_FontString", str
	SSProcess.SetNewObjValue "SSObj_FontHeight", noteh
```

---

### `CreateNewObj`

**功能：** 创建新对象（指定类型）

- **调用次数：** 372
- **使用文件数：** 168

**示例：**

```vbs
End if
			SSProcess.CreateNewObj  GeoType
			SSProcess.SetNewObjValue "SSObj_Code", g_OBJCode(0)
			SSProcess.SetNewObjValue "SSObj_LayerName", strLayername
```

---

### `AddNewObjToSelObjList`

- **调用次数：** 25
- **使用文件数：** 10

**示例：**

```vbs
SSProcess.SetNewObjValue "SSObj_Color", "RGB(255,0,0)"
			SSProcess.AddNewObjToSelObjList
		end if
		if code ="6801077" then
```

---

### `RepairUpdateObject`

- **调用次数：** 10
- **使用文件数：** 10

**示例：**

```vbs
Sub OnClick()
		SSProcess.RepairUpdateObject()
		SSProcess.ClearDataXParameter
		SSProcess.SetDataXParameter "DataType","21"
```

---

### `AddNewObjToSel`

- **调用次数：** 4
- **使用文件数：** 4

**示例：**

```vbs
SSProcess.SetNewObjValue "SSObj_PointNo", pointNo
                SSProcess.AddNewObjToSel
            End If
        End If
```

---

## 数据库操作

> 访问EPS工程内置的Access MDB数据库，执行SQL查询和数据操作

### `CloseAccessRecordset`

**功能：** 关闭记录集

- **调用次数：** 2,383
- **使用文件数：** 755

**示例：**

```vbs
'关闭记录集
	SSProcess.CloseAccessRecordset mdbName, sql
End Function
```

---

### `OpenAccessRecordset`

**功能：** 打开数据库记录集（执行SQL查询）

- **调用次数：** 2,345
- **使用文件数：** 766

**示例：**

```vbs
'打开记录集
	SSProcess.OpenAccessRecordset mdbName, sql
	'获取记录总数
	RecordCount =SSProcess.GetAccessRecordCount (mdbName, sql)
```

---

### `GetAccessRecord`

**功能：** 获取当前记录的字段名和值

- **调用次数：** 2,181
- **使用文件数：** 731

**示例：**

```vbs
'获取当前记录内容
			SSProcess.GetAccessRecord mdbName, sql, fields, values
			arSQLRecord(iRecordCount) =values										'查询记录
			iRecordCount =iRecordCount +1													'查询记录数
```

---

### `OpenAccessMdb`

**功能：** 打开Access MDB数据库

- **调用次数：** 2,081
- **使用文件数：** 795

**示例：**

```vbs
SSProcess.OpenAccessMdb   mdbname
	if RQQ <> "" and RQZ <> "" then
		if SSMK = "" then
```

---

### `CloseAccessMdb`

**功能：** 关闭Access MDB数据库

- **调用次数：** 1,981
- **使用文件数：** 782

**示例：**

```vbs
next
		SSProcess.CloseAccessMdb   mdbname
		Delpage 1
		ReleaseDOC DocFileName
```

---

### `AccessMoveNext`

**功能：** 将记录指针移到下一条记录

- **调用次数：** 1,904
- **使用文件数：** 647

**示例：**

```vbs
'移动记录游标
			SSProcess.AccessMoveNext mdbName, sql
		Wend
	end if
```

---

### `GetAccessRecordCount`

**功能：** 获取记录集中的记录总数

- **调用次数：** 1,880
- **使用文件数：** 499

**示例：**

```vbs
'获取记录总数
	RecordCount =SSProcess.GetAccessRecordCount (mdbName, sql)
	if RecordCount >0 then
		iRecordCount =0
```

---

### `AccessIsEOF`

**功能：** 判断记录指针是否到达末尾

- **调用次数：** 1,840
- **使用文件数：** 624

**示例：**

```vbs
'浏览记录
		While SSProcess.AccessIsEOF (mdbName, sql) = 0
			fields = ""
			values = ""
```

---

### `AccessMoveFirst`

**功能：** 将记录指针移到第一条记录

- **调用次数：** 1,704
- **使用文件数：** 414

**示例：**

```vbs
'将记录游标移到第一行
		SSProcess.AccessMoveFirst mdbName, sql
		iRecordCount = 0
		'浏览记录
```

---

### `ExecuteAccessSql`

**功能：** 执行Access SQL语句

- **调用次数：** 102
- **使用文件数：** 26

**示例：**

```vbs
msgbox item_id
			SSProcess.ExecuteAccessSql edbname, sql
				'SSProcess.MapCallBackFunction "SDLCommand", "$sscheck,ck",0
				'SSProcess.LoadCheckRecord
```

---

### `ModifyAccessRecord`

**功能：** 修改当前记录的字段值

- **调用次数：** 64
- **使用文件数：** 44

**示例：**

```vbs
SSProcess.GetAccessRecord mdbName, sql, fields, values
              SSProcess.ModifyAccessRecord mdbName, sql, "StringValue", "10130000"
              SSProcess.AccessMoveNext mdbName, sql
       Wend
```

---

### `IsExistentTable`

- **调用次数：** 59
- **使用文件数：** 48

**示例：**

```vbs
SSProcess.OpenAccessMdb mdtFileName
   ismdtversion = SSProcess.IsExistentTable( mdtFileName,"STD_Version" )
   isedbversion = SSProcess.IsExistentTable( edbFileName,"STD_Version" )
       If ismdtversion = 0  And  isedbversion = 0 Then
```

---

### `AddAccessRecord`

**功能：** 添加新记录

- **调用次数：** 48
- **使用文件数：** 48

**示例：**

```vbs
values = strSection & "," & strKeyName & "," & strValue
      SSProcess.AddAccessRecord mdbName, sql, fields, values
      SSProcess.CloseAccessRecordset mdbName, sql
End Function
```

---

### `ExecuteSql`

**功能：** 执行SQL语句

- **调用次数：** 42
- **使用文件数：** 12

**示例：**

```vbs
sql = sql & " Where GeoLineTB.Code In(250200,250201,250202,250203,620200)"
       SSProcess.ExecuteSql sql
       sql = "Update [行政区界线属性表] Inner Join GeoLineTB On 行政区界线属性表.ID=GeoLineTB.ID"
```

---

### `GetAccessFieldInfo`

- **调用次数：** 37
- **使用文件数：** 27

**示例：**

```vbs
'search ="SELECT "&sxb&".ID FROM "&sxb&" INNER JOIN "&dwb&"  ON "&dwb&".ID = "&sxb&".ID  WHERE ((["&dwb&"].[Mark] Mod 2<>0)  and "&dwb&".Code="&code&" and "&sxb&"."&sx&"='*');"
			 SSProcess.GetAccessFieldInfo SSProcess.GetProjectFileName,sxb, fieldInfos '获取字段信息
			 SSFunc.ScanString fieldInfos, ";", zdgs,zdgscount'分解获得总字段信息
			for i=0 to zdgscount -1
```

---

### `DelAccessRecord`

**功能：** 删除当前记录

- **调用次数：** 29
- **使用文件数：** 29

**示例：**

```vbs
If  rsCount >0 Then
	      SSProcess.DelAccessRecord mdbName, sql
      End If
      fields = "Section,KeyName,StringValue"
```

---

### `GetAccessTableNames`

- **调用次数：** 8
- **使用文件数：** 8

**示例：**

```vbs
SSProcess.OpenAccessMdb edbname
			SSProcess.GetAccessTableNames edbname, tableNames
			SSFunc.ScanString tableNames,",",tables,tablecount
```

---

### `AccessMove`

- **调用次数：** 6
- **使用文件数：** 6

**示例：**

```vbs
SSProcess.AccessMoveFirst mdbName, sql
      SSProcess.AccessMove mdbName, sql, lRows
      SSProcess.AccessIsEOF mdbName, sql
lcGeoID=0
```

---

### `AccessMovePrev`

- **调用次数：** 4
- **使用文件数：** 4

**示例：**

```vbs
SSProcess.AccessMovePrev mdbName, sql
      SSProcess.AccessMoveNext mdbName, sql
      SSProcess.AccessMoveLast mdbName, sql
```

---

### `AccessMoveLast`

- **调用次数：** 4
- **使用文件数：** 4

**示例：**

```vbs
SSProcess.AccessMoveNext mdbName, sql
      SSProcess.AccessMoveLast mdbName, sql
      SSProcess.AccessMoveFirst mdbName, sql
      SSProcess.AccessMove mdbName, sql, lRows
```

---

## 注记操作

> 管理地图注记（文字标注）的创建、修改和删除

### `GetSelNoteValue`

**功能：** 获取选择集中注记的属性值

- **调用次数：** 922
- **使用文件数：** 354

**示例：**

```vbs
'得到扩展属性中的字段的值
			strID  =  SSProcess.GetSelNoteValue (i, "SSObj_ID")
			strUserCode = GetNoteNextValueByPreviousValue(i,"SOUTH")
			  '根据用户编码得到对应的EPS分类号
```

---

### `GetSelNoteCount`

**功能：** 获取选择集中注记的数量

- **调用次数：** 664
- **使用文件数：** 400

**示例：**

```vbs
SSProcess.SelectFilter
	geocount = SSProcess.GetSelNoteCount()
   If geocount > 0 Then
	  '锁定数据库
```

---

### `GetSelNotePoint`

**功能：** 获取注记的坐标点

- **调用次数：** 238
- **使用文件数：** 172

**示例：**

```vbs
zjnr=SSProcess.GetSelNoteValue(i,"SSObj_FontString")   '获得注记的注记内容
            SSProcess.GetSelNotePoint i,0,x,y,z,pt,pn     '获得注记的注记坐标
            drawpoint 3111001,x,y,zjnr,"[地址]"   '绘制点符号
            SSProcess.DeleteObject id    '绘制点后，删除原注记
```

---

### `SetSelNoteValue`

**功能：** 设置选择集中注记的属性值

- **调用次数：** 222
- **使用文件数：** 71

**示例：**

```vbs
If objCode(0) <> ""  Then
					 SSProcess.SetSelNoteValue i, "SSObj_FontClass", objCode(0)
						Erase objCode
              		'set strUserCode = Nothing
```

---

### `DelSelNote`

**功能：** 删除注记

- **调用次数：** 188
- **使用文件数：** 104

**示例：**

```vbs
If dist<2 Then
                                           SSProcess.DelSelNote i
                                           Exit For
                                   End If
```

---

### `AddSelNoteToSaveNoteList`

- **调用次数：** 51
- **使用文件数：** 51

**示例：**

```vbs
End if
							SSProcess.AddSelNoteToSaveNoteList i
							fontclass = ""
					Next
```

---

### `LockSelNotePoint`

- **调用次数：** 50
- **使用文件数：** 25

**示例：**

```vbs
pointCount = SSProcess.GetSelNotePointCount (i)
         SSProcess.LockSelNotePoint i, 1
			For j=0 To pointCount-1
					SSProcess.GetSelNotePoint i, j, x, y, z, ptype, pname
```

---

### `FindNoteClass`

**功能：** 查找注记分类

- **调用次数：** 43
- **使用文件数：** 42

**示例：**

```vbs
condition = "NoteTemplate.Byname='" & cadcode & "'"
                  epscode =  SSProcess.FindNoteClass ("NoteTemplateTB_500_cassin", condition)
						If( epscode<>"" )Then
                        ' SSProcess.SetSelNoteValue i, "SSObj_FontClass", epscode
```

---

### `GetSelNotePointCount`

- **调用次数：** 40
- **使用文件数：** 39

**示例：**

```vbs
geoType = SSProcess.GetSelNoteValue(j, "SSObj_Type")
		pointcount = SSProcess.GetSelNotePointCount(j)
		'msgbox pointcount
		SSProcess.GetSelNotePoint id, 0, x,  y,  z,  ptype,  name
```

---

### `ResetSelNoteByFontClass`

- **调用次数：** 40
- **使用文件数：** 40

**示例：**

```vbs
' SSProcess.SetSelNoteValue i, "SSObj_FontClass", epscode
                         SSProcess.ResetSelNoteByFontClass i, epscode
                  End If
```

---

### `GetFontClassInfo`

**功能：** 获取字体分类信息

- **调用次数：** 37
- **使用文件数：** 6

**示例：**

```vbs
'+++++++++++++++++++++++++++++++++++++++以下输出报表
														FontClass=SSProcess.GetFontClassInfo (exportFontClass, "FontClass" )
														ObjectName=SSProcess.GetFontClassInfo (exportFontClass, "Memo" )
														LayerName=SSProcess.GetFontClassInfo (exportFontClass, "LayerName" )
```

---

### `SetSelNotePoint`

**功能：** 设置注记的坐标点

- **调用次数：** 32
- **使用文件数：** 31

**示例：**

```vbs
SSProcess.LongiLatiToxyCGCS2000 114, pB, pL , pX, pY
               SSProcess.SetSelNotePoint i, j,  pX, pY, z, ptype, pname
			Next
         SSProcess.UpdateSelNotePoint i
```

---

### `UpdateSelNotePoint`

- **调用次数：** 25
- **使用文件数：** 25

**示例：**

```vbs
Next
         SSProcess.UpdateSelNotePoint i
         SSProcess.AddSelNoteToSaveNoteList i
         SSProcess.LockSelNotePoint i,0
```

---

### `LinkNearNoteObj`

- **调用次数：** 3
- **使用文件数：** 3

**示例：**

```vbs
SSProcess.LinkNearNoteObj "结构注记","层数注记",4.5,"SSObj_FontString","CallBackFunc_LinkText(SSObj_FontString,SSSubObj_FontString)"
     SSProcess.ClearSelectConditionGroups
```

---

## 图形绘制

> 在地图上绘制图形元素（线段、文字、圆弧等）

### `DrawLine`

**功能：** 绘制线段

- **调用次数：** 884
- **使用文件数：** 95

**示例：**

```vbs
For i = 1 To groupcount
        SSProcess.DrawLine pDc, spx+tajj*(i-1), spy,spx+lie1k+lie2k+lie3k+lie4k+tajj*(i-1), spy, RGB(0,0,0), 10, linestyle
        SSProcess.DrawLine pDc, spx+tajj*(i-1), spy-hg,spx+lie1k+lie2k+lie3k+lie4k+tajj*(i-1), spy-hg, RGB(0,0,0), 10, linestyle
        hgk=1
```

---

### `Circle3pToCenter`

**功能：** 通过三点计算圆心

- **调用次数：** 173
- **使用文件数：** 95

**示例：**

```vbs
x000=xxx(j,jj-1)  :   y000=yyy(j,jj-1)  :  x111=xxx(j,jj)  :  y111=yyy(j,jj)  :  x222=xxx(j,jj+1)  :  y222=yyy(j,jj+1)
                        SSProcess.Circle3pToCenter x000, y000, x111, y111, x222, y222, centerx, centery, r
                        SSProcess.XYSA centerx, centery,x000, y000, dist0, angle0, 0
                        SSProcess.XYSA centerx, centery,x111, y111, dist1, angle1, 0
```

---

### `PasteBackgroundImage`

**功能：** 粘贴背景图片

- **调用次数：** 108
- **使用文件数：** 107

**示例：**

```vbs
If buttondownbz = 1 Then
        SSProcess.PasteBackgroundImage
        drawtable spx,spy   '第一个表
    End If
```

---

### `Arc3pToCenter`

**功能：** 通过三点计算弧心

- **调用次数：** 66
- **使用文件数：** 35

**示例：**

```vbs
SSProcess.GetSelGeoPoint i, j+2, x2,  y2,  z,  ptype2,  name
                       SSProcess.Arc3pToCenter x0, y0, x1, y1, x2, y2, centerx, centery, r, ang1, ang2, ang3
							  SSProcess.XYSA centerx,centery,x0, y0, dist00, angle1, 0
							  SSProcess.XYSA centerx,centery,x2, y2, dist00, angle2, 0
```

---

### `DrawText`

**功能：** 绘制文字

- **调用次数：** 3
- **使用文件数：** 3

**示例：**

```vbs
SSProcess.DrawText pDc,spx,spy ,text, 0," 黑体", RGB(255,255, 0),150,150, 0,0,0, 0,500,10, 0,2
End If
```

---

## 地图与视图

> 控制地图显示、比例尺、图层状态和视图刷新

### `SetLayerStatus`

**功能：** 设置图层显示状态

- **调用次数：** 11,393
- **使用文件数：** 228

**示例：**

```vbs
SSProcess.ChangeSelectionObjAttr "SSObj_LayerName", "查图标记层存疑" '换层
      SSProcess.SetLayerStatus "TERL", 1, 0
'层显示开关(可控对像)
```

---

### `UpdateCurMap`

**功能：** 更新当前地图显示

- **调用次数：** 766
- **使用文件数：** 134

**示例：**

```vbs
SSProject.SetActiveMap maphandle
			SSProcess.UpdateCurMap maphandle
			sourcehandle=SSProject.GetActiveDatasource(maphandle)
			sourcepath=SSProject.GetDataSourceInfo(sourcehandle, "PathName")
```

---

### `RefreshView`

**功能：** 刷新视图

- **调用次数：** 522
- **使用文件数：** 389

**示例：**

```vbs
SSProcess.ObjectDeal 0, "FreeSelectionObjectDisplayList", "", result
      SSProcess.RefreshView
End Sub
```

---

### `SetMapScale`

**功能：** 设置地图比例尺

- **调用次数：** 381
- **使用文件数：** 199

**示例：**

```vbs
end if
	SSProcess.SetMapScale blc
	Dim fso, tf, sLine, strs(10000), count
	Dim EPSGeocodes(10000,2), userGeocodes(10000), NoteClasscodes(10000,2),userNoteClasscodes(10000)
```

---

### `SetCursorStatus`

- **调用次数：** 333
- **使用文件数：** 199

**示例：**

```vbs
'0  输入光标 6 选择光标
	'SSProcess.SetCursorStatus  6
End Sub
```

---

### `GetLayerName`

**功能：** 获取图层名称

- **调用次数：** 240
- **使用文件数：** 208

**示例：**

```vbs
For i=0 To count-1
		 layerName = SSProcess.GetLayerName(i)
		MyPos = Instr(1, strLayerTemplate, layerName, 1)
		 If  MyPos = 0 Then
```

---

### `GetLayerCount`

**功能：** 获取图层数量

- **调用次数：** 240
- **使用文件数：** 208

**示例：**

```vbs
Dim layerName
	 count = SSProcess.GetLayerCount
'模板既有标准图层
 strLayerTemplate ="DEFAULT,标注层,图廓层,定位基础线,控制点,定位基础注记,水系点,水系线,水系中心线,水系面,水系注记,房屋面,房屋中心点,门牌号,居民地点,居民地线,居民地面,设施点,设施线,设施面,居民地注记,交通点,交通线,交通中心线,交通面,交通注记,管线点,管线线,管线面,管线注记,境界点,境界线,境界面,境界注记,其它境界线,其它境界面,等高线,高程点,地貌点,地貌线,地貌面,地貌注记,植被点,植被线,植被面,植被注记,更新区域"
```

---

### `GetMapScale`

**功能：** 获取当前地图比例尺

- **调用次数：** 173
- **使用文件数：** 168

**示例：**

```vbs
count = SSProcess.GetSelNoteCount
      bl = SSProcess.GetMapScale
      For i = 0 To count - 1
              id = SSProcess.GetSelNoteValue (i, "SSObj_ID")
```

---

### `GetCursorStatus`

- **调用次数：** 121
- **使用文件数：** 121

**示例：**

```vbs
SSProcess.ShowScriptDlg mode,title
	'oldCursorStatus =   SSProcess.GetCursorStatus
	'0  输入光标 6 选择光标
	'SSProcess.SetCursorStatus  6
```

---

### `SetMapStatus`

- **调用次数：** 40
- **使用文件数：** 17

**示例：**

```vbs
'锁定数据库
		SSProcess.SetMapStatus 1, 2
		For i=0 To geocount-1
		 '得到扩展属性中的字段的值
```

---

### `GetLayerAttrTableName`

- **调用次数：** 9
- **使用文件数：** 9

**示例：**

```vbs
lx=SSProcess.GetFeatureCodeInfo(arID1(i), "GeoType" )'获取编码类型
											sxb=SSProcess.GetLayerAttrTableName(SSProcess.GetFeatureCodeInfo(arID1(i), "LayerName" ), lx )'根据编码获取属性表
											SXisnull sxb,arID1(i),arID2(j),lx,arID3,arID3count'用sql检查是否为空的函数
											if arID3count<>0 then
```

---

### `DeleteLayer`

**功能：** 删除图层

- **调用次数：** 5
- **使用文件数：** 5

**示例：**

```vbs
If geoCount1 = 0  and geoCount2 = 0 Then
				 SSProcess.DeleteLayer layerName
			 End If
		 End If
```

---

### `GetLayerStatus`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
layerName = SSProcess.GetLayerName (i)
layerStatus = SSProcess.GetLayerStatus (layerName, 0 )
allLayers(i) = layerName
allLayerStatus(i) = layerStatus
```

---

## 图框与打印

> 创建和管理图框，设置打印参数

### `PrintMapByCoord`

**功能：** 按坐标范围打印地图

- **调用次数：** 97
- **使用文件数：** 97

**示例：**

```vbs
For i=0 To printpapercount-1
		SSProcess.PrintMapByCoord x,y,width,height,angle
	Next
	SSProcess.MapMethod "SetPrintLineWidthDelta","0"
```

---

### `FreeMapFrame`

**功能：** 释放图框

- **调用次数：** 20
- **使用文件数：** 20

**示例：**

```vbs
Next
     SSProcess.FreeMapFrame
End Sub
```

---

### `GetMapFrameNumber`

**功能：** 获取图框编号

- **调用次数：** 20
- **使用文件数：** 14

**示例：**

```vbs
If abs(x_-x)<125.001 And abs(y_-y)<100.001 Then
						getTFH=SSProcess.GetMapFrameNumber (x, y)
						Exit For
				End If
```

---

### `GetMapFrameCount`

- **调用次数：** 19
- **使用文件数：** 19

**示例：**

```vbs
SSProcess.CreateMapFrameByRegion 1
		gs=SSProcess.GetMapFrameCount
		For  i=0 To gs-1
				 SSProcess.CreateOneMapFrame i, 1201003
```

---

### `GetMapFrameCenterPoint`

- **调用次数：** 17
- **使用文件数：** 17

**示例：**

```vbs
For i=0 To frameCount-1
          SSProcess.GetMapFrameCenterPoint i, x, y
          SSProcess.SetCurMapFrame x, y, 0, ""
          frameID = SSProcess.GetCurMapFrame()
```

---

### `CreateMapFrame`

**功能：** 创建图框

- **调用次数：** 15
- **使用文件数：** 15

**示例：**

```vbs
End If
      SSProcess.CreateMapFrame
      frameCount = SSProcess.GetMapFrameCount()
      For i=0 To frameCount-1
```

---

### `SetCurMapFrame`

- **调用次数：** 14
- **使用文件数：** 14

**示例：**

```vbs
SSProcess.GetMapFrameCenterPoint i, x, y
          SSProcess.SetCurMapFrame x, y, 0, ""
          frameID = SSProcess.GetCurMapFrame()
          mapNumber = SSProcess.GetObjectAttr( CLng(frameID), "[MapNumber]")
```

---

### `CreateOneMapFrame`

- **调用次数：** 10
- **使用文件数：** 10

**示例：**

```vbs
For  i=0 To gs-1
				 SSProcess.CreateOneMapFrame i, 1201003
		Next
     SSProcess.FreeMapFrame
```

---

### `GetCurMapFrame`

- **调用次数：** 7
- **使用文件数：** 7

**示例：**

```vbs
SSProcess.SetCurMapFrame x, y, 0, ""
          frameID = SSProcess.GetCurMapFrame()
          mapNumber = SSProcess.GetObjectAttr( CLng(frameID), "[MapNumber]")
          If mapNumber <> "" Then
```

---

### `SetFrameCode`

- **调用次数：** 6
- **使用文件数：** 6

**示例：**

```vbs
SSProcess.SetFrameCode "1201003"
				changeattr "3111001","[地址]", "[DiZ]"
```

---

### `GetCurMapFrameNumber`

- **调用次数：** 5
- **使用文件数：** 5

**示例：**

```vbs
SSProcess.SetCurMapFrame x, y, 0, ""
		CurMapFrameNumber =SSProcess.GetCurMapFrameNumber
		polygonID =SSProcess.GetCurMapFrame
		'查找与指定多边形相关的对象
```

---

### `CreateMapFrameByRegion`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
Sub OnClick()
		SSProcess.CreateMapFrameByRegion 1
		gs=SSProcess.GetMapFrameCount
		For  i=0 To gs-1
```

---

### `CreateMapFrameByRegionID`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
getTFH=""
		SSProcess.CreateMapFrameByRegionID id
		mapcount=SSProcess.GetMapFrameCount
		For ii=0 To mapcount-1
```

---

## Grid控件与对话框

> 创建和操作Grid表格控件，显示自定义对话框

### `UpdateScriptDlgParameter`

- **调用次数：** 730
- **使用文件数：** 426

**示例：**

```vbs
'更新对话框上参数到内存
		 SSProcess.UpdateScriptDlgParameter 1
	  '取点编码
		MDataType  = SSProcess.GetInputParameter ("测量数据类型")
```

---

### `ShowInputParameterDlg`

**功能：** 显示输入参数对话框

- **调用次数：** 549
- **使用文件数：** 400

**示例：**

```vbs
SSProcess.AddInputParameter "", "",0, "", ""
		res = SSProcess.ShowInputParameterDlg ("设置输出模式" )
		  If res = 0  Then
					Exit Sub
```

---

### `ShowScriptDlg`

**功能：** 显示脚本对话框

- **调用次数：** 543
- **使用文件数：** 517

**示例：**

```vbs
SSProcess.ShowScriptDlg mode,title
End Sub
```

---

### `SetGridCellInfo`

**功能：** 设置Grid控件单元格信息

- **调用次数：** 416
- **使用文件数：** 50

**示例：**

```vbs
dylsh=SSProcess.Getobjectattr(idarr(i),"[DanYLSH]")
		SSProcess.SetGridCellInfo (i+1), 1 , id, ""
		SSProcess.SetGridCellInfo (i+1), 2 , djh, ""
		SSProcess.SetGridCellInfo (i+1), 3 , zrzh, ""
```

---

### `CloseScriptDlg`

**功能：** 关闭脚本对话框

- **调用次数：** 393
- **使用文件数：** 203

**示例：**

```vbs
'EXIT Sub
			'SSProcess.CloseScriptDlg
		'end if
		'dkmj= formatnumber(dkmj,2)
```

---

### `GetGridCellInfo`

**功能：** 获取Grid控件单元格信息

- **调用次数：** 302
- **使用文件数：** 47

**示例：**

```vbs
for i=0 to idcount-1
		id=SSProcess.GetGridCellInfo((i+1), 1)
		djh=SSProcess.GetGridCellInfo((i+1), 2)
		zrzh=SSProcess.GetGridCellInfo((i+1), 3)
```

---

### `ShowScriptUserDefDlg`

**功能：** 显示自定义脚本对话框

- **调用次数：** 202
- **使用文件数：** 202

**示例：**

```vbs
'自定义对话框
'SSProcess.ShowScriptUserDefDlg title, dlgTemplateName, dlgWidth, dlgHeight, colCount, titleWidth, valueWidth
'添加代码
End Sub
```

---

### `SetScriptDlgCellValue`

- **调用次数：** 135
- **使用文件数：** 17

**示例：**

```vbs
End If
 							   SSProcess.SetScriptDlgCellValue ConIDS(i), DefValues(i)
						Else
								SSProcess.SetScriptDlgCellValue ConIDS(i),Valuestr
```

---

### `SetGridHeadInfo`

- **调用次数：** 61
- **使用文件数：** 50

**示例：**

```vbs
SSFunc.ScanString ids,",",idarr,idcount
	SSProcess.SetGridHeadInfo "ID,地籍,自然幢,逻辑幢,层,室号部位,座落,测绘状态,户序号,实测建筑面积,实测套内建筑面积,实测分摊建筑面积,房屋用途,房屋结构,户型,户型结构,房屋类型,房屋性质,分摊功能区名称,单元名称,单元流水号" , "40,40,50,50,30,60,40,60,50,80,100,100,60,60,40,60,60,60,90,60,70" , 0, 1, 0
	for i=0 to idcount-1
		id=SSProcess.Getobjectattr(idarr(i),"SSObj_ID")
```

---

### `GetGridCtrlCellInfo`

- **调用次数：** 41
- **使用文件数：** 4

**示例：**

```vbs
For i=0 To RowCount-1
								value0 = SSProcess.GetGridCtrlCellInfo ("[INIINFOLIST]",  i+1, 1)
								value1 = SSProcess.GetGridCtrlCellInfo ("[INIINFOLIST]",  i+1, 2)
								value2 = SSProcess.GetGridCtrlCellInfo ("[INIINFOLIST]",  i+1, 3)
```

---

### `SetScriptDlgCellOptions`

- **调用次数：** 34
- **使用文件数：** 4

**示例：**

```vbs
ljzhlb = Replace (zrzInfo.ljzhlb, "、", ",")
				SSProcess.SetScriptDlgCellOptions "[逻辑幢号列表]",ljzhlb
				SSProcess.SetScriptDlgCellValue "[逻辑幢号列表]",zrzInfo.GetLJZH(0)
				OnListBoxSelChange "", 0, "[逻辑幢号列表]", zrzInfo.GetLJZH(0)
```

---

### `AdjustGridCtrl`

- **调用次数：** 31
- **使用文件数：** 4

**示例：**

```vbs
Next
                 SSProcess.AdjustGridCtrl "[INIINFOLIST]"
            End If
      End If
```

---

### `SetGridCtrlCellInfo`

- **调用次数：** 29
- **使用文件数：** 4

**示例：**

```vbs
SSProcess.InsertGridCtrlRow "[INIINFOLIST]", i+1, 0
								SSProcess.SetGridCtrlCellInfo "[INIINFOLIST]",  i+1, 1, ConIDS(i),"" , 1, 0
								SSProcess.SetGridCtrlCellInfo "[INIINFOLIST]",  i+1, 2, GFields(i), "" ,1, 0
								SSProcess.SetGridCtrlCellInfo "[INIINFOLIST]",  i+1, 3, DefValues(i), "" , 1, 0
```

---

### `GetScriptDlgCellValue`

- **调用次数：** 29
- **使用文件数：** 16

**示例：**

```vbs
For i=0 To ConCount-1
            		value = SSProcess.GetScriptDlgCellValue (ConIDS(i))
						SSFunc.ScanString GFields(i),",",strs,scount
						SSFunc.ScanString value,"、",strs1,scount1
```

---

### `ShowGridEditDlg`

**功能：** 显示Grid编辑对话框

- **调用次数：** 28
- **使用文件数：** 25

**示例：**

```vbs
next
	res=SSProcess.ShowGridEditDlg("权籍调查户信息")
	if res=0 then
		exit sub
```

---

### `ShowGridEditDlg1`

- **调用次数：** 25
- **使用文件数：** 25

**示例：**

```vbs
next
	   SSProcess.ShowGridEditDlg1 "注记内容列表(" & rowCount & ")", "定位注记位置", 0, 350, 400
End Function
```

---

### `InsertGridCtrlRow`

- **调用次数：** 20
- **使用文件数：** 4

**示例：**

```vbs
For i=0 To ConCount-1
								SSProcess.InsertGridCtrlRow "[INIINFOLIST]", i+1, 0
								SSProcess.SetGridCtrlCellInfo "[INIINFOLIST]",  i+1, 1, ConIDS(i),"" , 1, 0
								SSProcess.SetGridCtrlCellInfo "[INIINFOLIST]",  i+1, 2, GFields(i), "" ,1, 0
```

---

### `ShowScriptUserDefDlgEx`

- **调用次数：** 17
- **使用文件数：** 17

**示例：**

```vbs
Next
      SSProcess.ShowScriptUserDefDlgEx  mode, title, dlgTemplateName, dlgWidth, dlgHeight, colCount, titleWidth, valueWidth
End Sub
```

---

### `DeleteGridCtrlRow`

- **调用次数：** 16
- **使用文件数：** 4

**示例：**

```vbs
for i=0 to selCount-1
								SSProcess.DeleteGridCtrlRow fieldName, delIndex(selCount-i-1), 1
						next
				 ElseIf SelMenu = "插入行" Then
```

---

### `ShowGridEditDlg2`

- **调用次数：** 7
- **使用文件数：** 7

**示例：**

```vbs
result = SSProcess.ShowGridEditDlg2 ("SDE查询", "开始查询", 1, 600, 200)
      if result <>0 Then
             ListSDE
```

---

### `CreateGridCtrl`

**功能：** 创建Grid控件

- **调用次数：** 5
- **使用文件数：** 4

**示例：**

```vbs
SSProcess.ShowScriptUserDefDlgEx  mode, title, dlgTemplateName, dlgWidth, dlgHeight, colCount, titleWidth, valueWidth
		SSProcess.CreateGridCtrl "[INIINFOLIST]",  "控件属性连接名称,对应地物字段名称,默认值,备选项,是否记忆",  "120,150,120,320,50",  1,  1,  0
End Sub
```

---

### `GetGridCtrlSelRowCount`

- **调用次数：** 5
- **使用文件数：** 5

**示例：**

```vbs
If SelMenu = "删除选择行" Then
						selCount = SSProcess.GetGridCtrlSelRowCount(fieldName)
						Dim delIndex(1000)
						for i=0 to selCount-1
```

---

### `GetGridCtrlSelRowIndex`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
for i=0 to selCount-1
								delIndex(i) = SSProcess.GetGridCtrlSelRowIndex(fieldName, i)
						next
						for i=0 to selCount-1
```

---

### `FillGridEditDlg`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
next
						SSProcess.FillGridEditDlg "楼盘列表(" & rowCount & ")", "下载分层数据", 0, 780, 200
            End if
```

---

## 输入参数

> 管理脚本的输入输出参数

### `GetInputParameter`

**功能：** 获取输入参数值

- **调用次数：** 4,618
- **使用文件数：** 662

**示例：**

```vbs
End If
		   DataBoundMode = SSProcess.GetInputParameter ("数据输出范围" )
			If DataBoundMode = "全部输出" Then
					DataBoundMode = "0"
```

---

### `AddInputParameter`

**功能：** 添加输入参数

- **调用次数：** 4,189
- **使用文件数：** 689

**示例：**

```vbs
SSProcess.ClearInputParameter
		SSProcess.AddInputParameter "数据输出范围", DataBoundMode,0, "选择集输出,当前图幅输出,全部输出", "选择'选择集输出'输出选择集内的数据，选择'当前图幅输出'输出指定图幅的数据(需先设定图幅)，选择'全部输出'输出全部数据"
		SSProcess.AddInputParameter "", "",0, "", ""
		res = SSProcess.ShowInputParameterDlg ("设置输出模式" )
```

---

### `AddFunctionParameter`

**功能：** 添加函数参数

- **调用次数：** 1,567
- **使用文件数：** 152

**示例：**

```vbs
'悬挂点处理限距
	SSProcess.AddFunctionParameter "limitdist=0.0005"
	'拓扑弧段编码
	SSProcess.AddFunctionParameter "SrcArcCodes=" & xcodes
```

---

### `ClearInputParameter`

**功能：** 清空输入参数

- **调用次数：** 803
- **使用文件数：** 634

**示例：**

```vbs
DataBoundMode = SSProcess.ReadEpsIni ("设置输出模式", "DataBoundMode" , "全部输出" )
		SSProcess.ClearInputParameter
		SSProcess.AddInputParameter "数据输出范围", DataBoundMode,0, "选择集输出,当前图幅输出,全部输出", "选择'选择集输出'输出选择集内的数据，选择'当前图幅输出'输出指定图幅的数据(需先设定图幅)，选择'全部输出'输出全部数据"
		SSProcess.AddInputParameter "", "",0, "", ""
```

---

### `SetInputParameter`

- **调用次数：** 199
- **使用文件数：** 46

**示例：**

```vbs
if strValue=printerNameList(i) Then
				SSProcess.SetInputParameter "打印机端口", printerPortList(i)
				SSProcess.SetInputParameter "打印机驱动", printerDriverList(i)
			End If
```

---

### `ClearFunctionParameter`

**功能：** 清空函数参数

- **调用次数：** 146
- **使用文件数：** 145

**示例：**

```vbs
'拓扑构面
	SSProcess.ClearFunctionParameter
	'悬挂点处理限距
	SSProcess.AddFunctionParameter "limitdist=0.0005"
```

---

## EPS配置读写

> 读写EPS系统配置文件（INI/XML格式）

### `WriteEpsIni`

**功能：** 写入EPS配置文件

- **调用次数：** 1,806
- **使用文件数：** 335

**示例：**

```vbs
End If
			SSProcess.WriteEpsIni "数据输出范围", "DataBoundMode" , DataBoundMode
       fileName = SSProcess.SelectFileName(0, "指定输出文件名", 0, "AutoCAD Files (*.dwg)|*.dwg|All Files (*.*)|*.*||")
		If fileName = "" Then
```

---

### `ReadEpsIni`

**功能：** 读取EPS配置文件（INI格式）

- **调用次数：** 1,573
- **使用文件数：** 424

**示例：**

```vbs
'数据输出范围
		DataBoundMode = SSProcess.ReadEpsIni ("设置输出模式", "DataBoundMode" , "全部输出" )
		SSProcess.ClearInputParameter
		SSProcess.AddInputParameter "数据输出范围", DataBoundMode,0, "选择集输出,当前图幅输出,全部输出", "选择'选择集输出'输出选择集内的数据，选择'当前图幅输出'输出指定图幅的数据(需先设定图幅)，选择'全部输出'输出全部数据"
```

---

### `ReadEpsDBIni`

**功能：** 读取EPS数据库配置

- **调用次数：** 1,062
- **使用文件数：** 217

**示例：**

```vbs
'SSProcess.WriteEpsDBIni "ERPManager", "Checkers" , PEOPLOINFO
    'IID=SSProcess.ReadEpsDBIni ("ERPManager", "ERP_IID" , "")
    'If IID="" Then Msgbox "本工程没有接单，无法输出XXX"  :  Exit Sub
```

---

### `WriteEpsDBIni`

**功能：** 写入EPS数据库配置

- **调用次数：** 864
- **使用文件数：** 177

**示例：**

```vbs
'If PEOPLOINFO="" Then Exit Sub
	'SSProcess.WriteEpsDBIni "ERPManager", "Checkers" , PEOPLOINFO
    'IID=SSProcess.ReadEpsDBIni ("ERPManager", "ERP_IID" , "")
    'If IID="" Then Msgbox "本工程没有接单，无法输出XXX"  :  Exit Sub
```

---

### `GetPrivateProfile`

- **调用次数：** 272
- **使用文件数：** 68

**示例：**

```vbs
'msgbox "Section="&Section
	Count1 =SSProcess.GetPrivateProfile(Section, "异常项总数" , "", g_strIniFile)
	'msgbox "Count1="&Count1
	if Count1 ="" then
```

---

### `WriteEpsTemplateIni`

**功能：** 写入EPS模板配置

- **调用次数：** 264
- **使用文件数：** 60

**示例：**

```vbs
strKey = "SymbolZoomMode"
		SSProcess.WriteEpsTemplateIni strSection, strKey ,"0"
		strKey = "SymbolZoomExceptionLayer"
		SSProcess.WriteEpsTemplateIni strSection, strKey , ""
```

---

### `ReadEpsTemplateIni`

**功能：** 读取EPS模板配置

- **调用次数：** 52
- **使用文件数：** 26

**示例：**

```vbs
strKey = "LineWidthScale"
	lsstr=SSProcess.ReadEpsTemplateIni (strSection, strKey , "1")
	If lsstr<>"" Then oldLineWidthScale = CDbl(lsstr)  :  Else  :  oldLineWidthScale="1"
	strKey = "LineWidthScaleCount"
```

---

### `ReadEpsXMLIni`

**功能：** 读取EPS XML配置

- **调用次数：** 14
- **使用文件数：** 2

**示例：**

```vbs
Dim  serverName, dbName, dbUsername, dbPassword
      dbType = SSProcess.ReadEpsXMLIni (0, "HouseSetup\DatabaseType" , "0" )
      serverName = SSProcess.ReadEpsXMLIni (0, "HouseSetup\Service" , "" )
      dbName = SSProcess.ReadEpsXMLIni (0, "HouseSetup\Database" , "" )
```

---

### `ReadEpsGlobalIni`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
rjbb = SSProcess.ReadEpsGlobalIni ("LiveUpdate" , "Version" , "未获取到软件版本！" )
	wordHelper.Replace "{软件版本}","软件版本:"&rjbb,0
```

---

## 系统路径与工具

> 获取EPS系统路径、执行外部程序、进度条管理

### `GetProjectFileName`

**功能：** 获取当前工程文件路径

- **调用次数：** 2,327
- **使用文件数：** 1117

**示例：**

```vbs
Set oReg=GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & strComputer & "\root\default:StdRegProv")
       'fileName = SSProcess.GetProjectFileName
		epsTempPath = SSProcess.GetSysPathName (5)
		'设置缺省输出目录
```

---

### `GetSysPathName`

**功能：** 获取EPS系统路径（如模板目录、线型目录等）

- **调用次数：** 1,470
- **使用文件数：** 828

**示例：**

```vbs
'fileName = SSProcess.SelectFileName(1,"",0,"TXT Files(*.txt)|*.txt|All Files (*.*)|*.*||")
	fileName =	SSProcess.GetSysPathName (8) &"CASS9导入编码对照表.txt"
	'msgbox  fileName
  If fileName = "" Then
```

---

### `PushUndoMark`

**功能：** 推送撤销标记

- **调用次数：** 1,137
- **使用文件数：** 746

**示例：**

```vbs
'GEO处理
		SSProcess.PushUndoMark
		SSProcess.ClearSelection
		SSProcess.ClearSelectCondition
```

---

### `MapMethod`

**功能：** 调用EPS内置方法

- **调用次数：** 1,121
- **使用文件数：** 468

**示例：**

```vbs
Sub OnInitScript()
	SSProcess.MapMethod "enumprinters", parameters
	strSection = "System"
	SSParameter.GetParameterSTR strSection, "PrinterNames", "", printerNames
```

---

### `ExecuteSDLFunction`

**功能：** 执行SDL函数（EPS内置功能）

- **调用次数：** 583
- **使用文件数：** 246

**示例：**

```vbs
'图形重新生成
	SSProcess.ExecuteSDLFunction "$SDL.SSProject.Display.RedrawExtend", 0
End Sub
```

---

### `MapCallBackFunction`

- **调用次数：** 357
- **使用文件数：** 154

**示例：**

```vbs
SSProcess.ExecuteSDLFunction "ssproject,display.redrawextend", Reason
    SSProcess.MapCallBackFunction "SDLCommand","SSWorkSpace,SSWorkSpace",0
End Function
```

---

### `TopProcess`

**功能：** 拓扑处理

- **调用次数：** 153
- **使用文件数：** 152

**示例：**

```vbs
SSProcess.AddFunctionParameter "CreateTopArc=0"
	SSProcess.TopProcess topname
End  Function
```

---

### `EpsProgressDelete`

**功能：** 删除进度条

- **调用次数：** 121
- **使用文件数：** 118

**示例：**

```vbs
Function CloseBar()
      SSProcess.EpsProgressDelete
End Function
Function RollBar(barname,dispmsg)
```

---

### `EpsProgressCreate`

**功能：** 创建进度条

- **调用次数：** 120
- **使用文件数：** 119

**示例：**

```vbs
'
		SSProcess.EpsProgressCreate 100,"导入"
		SSProcess.EpsProgressSetStep  1
		'
```

---

### `EpsProgressSetStep`

**功能：** 设置进度条步数

- **调用次数：** 114
- **使用文件数：** 114

**示例：**

```vbs
SSProcess.EpsProgressCreate 100,"导入"
		SSProcess.EpsProgressSetStep  1
		'
		Set fso = CreateObject("Scripting.FileSystemObject")
```

---

### `EpsProgressStepIt`

**功能：** 进度条前进一步

- **调用次数：** 113
- **使用文件数：** 113

**示例：**

```vbs
Function RollBar(barname,dispmsg)
    SSProcess.EpsProgressStepIt
   SSProcess.EpsProgressUpdateMsg  barname  & dispmsg
End Function
```

---

### `EpsProgressUpdateMsg`

**功能：** 更新进度条消息

- **调用次数：** 113
- **使用文件数：** 113

**示例：**

```vbs
SSProcess.EpsProgressStepIt
   SSProcess.EpsProgressUpdateMsg  barname  & dispmsg
End Function
```

---

### `GetTemplateFileName`

**功能：** 获取模板文件路径

- **调用次数：** 62
- **使用文件数：** 44

**示例：**

```vbs
tempath = SSProcess.GetTemplateFileName ()
```

---

### `WinExec`

**功能：** 执行外部程序

- **调用次数：** 38
- **使用文件数：** 38

**示例：**

```vbs
cmdLine  = exePath &  " " & Chr(34) & exportFileName & Chr(34) & " " & Chr(34) & "ACAD14" & Chr(34)  & " " & Chr(34) & "DWG" & Chr(34)
				SSProcess.WinExec cmdLine, 0
     End If
```

---

### `ExecuteToolboxCommand`

**功能：** 执行工具箱命令

- **调用次数：** 24
- **使用文件数：** 8

**示例：**

```vbs
SSProcess.RemoveCheckRecord "", ""
	SSProcess.ExecuteToolboxCommand "不动产","房产检查"
	nRecordUpper = SSProcess.GetCheckRecordCount
	if  nRecordUpper >0 then
```

---

### `EpsProgressSetStyle`

**功能：** 设置进度条样式

- **调用次数：** 14
- **使用文件数：** 13

**示例：**

```vbs
SSProcess.EpsProgressSetStyle 1
      SSProcess.EpsProgressCreate  SFCXXCount, "规划分层图输出..."
		SSProcess.EpsProgressSetStep  1
```

---

### `Sleep`

**功能：** 暂停执行

- **调用次数：** 9
- **使用文件数：** 9

**示例：**

```vbs
SSProcess.Sleep 6000
RunScript "VBScript", "地籍检查", "输出宗地图与地形图一致性检查"
```

---

### `EpsProgressSetPos`

- **调用次数：** 8
- **使用文件数：** 6

**示例：**

```vbs
for p = 0 to count -1
		SSProcess.EpsProgressSetPos  p*100/count
		mingch0 = replace(fileName,mingch,arymingch(p))
		mingch1 = replace(mingch0,".edb",".etn")
```

---

### `GetScriptPath`

**功能：** 获取当前脚本所在目录

- **调用次数：** 2
- **使用文件数：** 2

---

## 空间查询

> 在空间上搜索对象——按位置关系（内部/外部/附近/包含）查找

### `SearchInnerObjIDs`

**功能：** 搜索指定对象内部的所有对象ID

- **调用次数：** 868
- **使用文件数：** 480

**示例：**

```vbs
polygonID = SSProcess.GetSelGeoValue( i, "SSObj_ID" )
				ids = SSProcess.SearchInnerObjIDs(polygonID, 0, "8103031", 0)
				If ids <> "" Then
						SSFunc.ScanString ids, ",", arID, idCount
```

---

### `SearchNearObjIDs`

**功能：** 搜索指定对象附近的所有对象ID

- **调用次数：** 556
- **使用文件数：** 230

**示例：**

```vbs
dim ids(100),count
		zdids = SSProcess.SearchNearObjIDs (spx, spy, 0.02, 2, "6801053,6801063,6801073", 0)
		if zdids <> "" then
				ScanString zdids,",",ids,count
```

---

### `SearchOuterObjIDs`

**功能：** 搜索指定对象外部的所有对象ID

- **调用次数：** 231
- **使用文件数：** 216

**示例：**

```vbs
noteString = SSProcess.GetObjectAttr (noteID, "SSObj_FontString")
			ids = SSProcess.SearchOuterObjIDs( noteID,2, "3103013,3103014,3103015,3103023,3103053,3104003,3105003,3107003,3108003", 1 )
			'msgbox "ids="&ids
				if ids <> "" then
```

---

### `SearchNearObjIDS`

- **调用次数：** 48
- **使用文件数：** 47

**示例：**

```vbs
SSProcess.GetSelNotePoint i,0,x,y,z,pt,pn
        ids=SSProcess.SearchNearObjIDS (x, y, 2, 3, "6803375", id)
        If ids<>"" Then
            SSFunc.ScanString ids,",",ccstrs,cccount
```

---

### `SearchRelatePolygonIDs`

**功能：** 搜索与指定多边形相关的对象ID

- **调用次数：** 27
- **使用文件数：** 19

**示例：**

```vbs
geoID = SSProcess.GetSelGeoValue (i, "SSObj_ID")
          geoIDs =  SSProcess.SearchRelatePolygonIDs (CLng(geoID), "3103013,3108003,3103015,3103023,3107003,3106003,3106004,3106005,3804034,3804033,3109003,3109004,3109013,3109023,3109033")
          If geoIDs<> "" Then
				ScanString geoIDs, ",", strs, count
```

---

### `SearchInPolyObjIDs`

**功能：** 搜索指定多边形内的所有对象ID

- **调用次数：** 27
- **使用文件数：** 22

**示例：**

```vbs
GID = SSProcess.GetSelGeoValue(i, "SSObj_ID")
				ids1 = SSProcess.SearchInPolyObjIDs( GID, 10, "", 1, 1, 1)
				geoid = geoid&","&ids1
		next
```

---

### `SearchObjIDs`

- **调用次数：** 9
- **使用文件数：** 9

**示例：**

```vbs
For i=0 To count-1
             SSProcess.SearchObjIDs xyCoords, objecType, codes, innerObjGetPointMode
      Next
```

---

### `SearchNearObjIDs2`

- **调用次数：** 3
- **使用文件数：** 2

**示例：**

```vbs
redim gid(10000)  '高程点id数组
			gcids = SSProcess.SearchNearObjIDs2 ( dmxid ,dist, "7201001", 0 )  '搜索断面线附近高程点，返回id数组,返回的id按由小到大排序,因此需要按坐标重新排序
			SSFunc.ScanString gcids, ",", gid, idCount
			if idcount > 1 then 'exit for
```

---

### `SearchNearObjIDs1`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
xyCoords = x0&","&y0&","&x1&","&y1
		ids = SSProcess.SearchNearObjIDs1(xyCoords,  0.00001,AdjacentObjCode, AreaID )	'
		If ids<>""  Then
			ScanString ids, ",",  arID,nCount
```

---

## 几何计算

> 点线面的空间关系判断和几何量算

### `IsPolygonInPolygon`

**功能：** 判断多边形是否在另一个多边形内

- **调用次数：** 149
- **使用文件数：** 32

**示例：**

```vbs
For j=i+1 To hcount-1
					bbzz=SSProcess.IsPolygonInPolygon (drawids(i), drawids(j), 0.001)
					If bbzz=2 Then
						groups(groupcount)=groups(groupcount) & "," & j
```

---

### `IsPtInPoly`

**功能：** 判断点是否在多边形内

- **调用次数：** 124
- **使用文件数：** 54

**示例：**

```vbs
SSProcess.XYSA zx0_, zy0_, xx_, yy_, zdist0_, zangle0_, 1
				isnd0 = SSProcess.IsPtInPoly (xx_, yy_, geoID, 0.001)  ' 或非0，这该点被面包含，=0该点不被面包含
				while angle>2 * 3.1415926
					angle = angle - (3.1415926 * 2)
```

---

### `IsClockwise`

**功能：** 判断多边形是否顺时针

- **调用次数：** 75
- **使用文件数：** 74

**示例：**

```vbs
ZZDID=SSProcess.GetSelGeoValue(i,"SSObj_ID")
			flag=SSProcess.IsClockwise(ZZDID) '顺时针返回1，逆时针返回0.
         pc=SSProcess.GetSelGeoPointCount(i)
         bz=0  :  jlx=-123456.0  :  jly=-123456.0  :  jlj=-1  :  jlpn="xx"
```

---

### `IsPolylineInPolygon`

**功能：** 判断折线是否在多边形内

- **调用次数：** 17
- **使用文件数：** 10

**示例：**

```vbs
For j=0 To idcount-1
                            flag = SSProcess.IsPolylineInPolygon (geoID, strids(j), 0.001 )
                            If flag=2 Then
                                  needDel = 0
```

---

### `IsPtOnLine`

**功能：** 判断点是否在线上

- **调用次数：** 15
- **使用文件数：** 10

**示例：**

```vbs
SSProcess.GetObjectPoint idarr(j), 0, x,  y,  z,  ptype,  name
				aa= SSProcess.IsPtOnLine( x , y, xid , 0.1 )
				if aa=0 then
					SSProcess.AddCheckRecord "哈哈哈", "河里有没有高程点", "自定义脚本类->脚本编程检查", "这里有个高程点", x, y, z, 10, idarr(j), ""
```

---

### `GetNearDist`

**功能：** 获取最近距离

- **调用次数：** 11
- **使用文件数：** 10

**示例：**

```vbs
Else
							   SSProcess.GetNearDist geoID, spx, spy, bindex
								'圆弧暂不支持，以后完善
								SSProcess.GetObjectPoint geoID,bindex,px_1,py_1,pz_1,pt_1,pn_1
```

---

### `LineParallelDist`

**功能：** 计算平行线距离

- **调用次数：** 10
- **使用文件数：** 6

**示例：**

```vbs
id0=SSProcess.GetSelGeoValue(i,"SSObj_ID")
             id1=SSProcess.LineParallelDist (id0,dist,direction,0,1)
             darwarea  id0,id1
             SSProcess.DeleteObject id1
```

---

### `GetNearPointIndex`

- **调用次数：** 6
- **使用文件数：** 5

**示例：**

```vbs
ZDGUID=SSProcess.GetObjectAttr (geoID,"[ZDGUID]")
						pindex=SSProcess.GetNearPointIndex (geoID, spx, spy)
                  SSProcess.GetObjectPoint geoID,pindex,px,py,pz,pt,pn
```

---

### `GetDistDir`

**功能：** 获取距离和方向

- **调用次数：** 6
- **使用文件数：** 6

**示例：**

```vbs
dataMark = SSProcess.GetObjectAttr (idList(0), "SSObj_DataMark")
      SSProcess.GetDistDir idList(0), spx,spy, irec, flag
      SSProcess.GetNearDist idList(0), spx, spy, index
      pindex0 = irec
```

---

### `Cross_P`

**功能：** 计算两线交点

- **调用次数：** 5
- **使用文件数：** 4

**示例：**

```vbs
For j=i+1 To pc-2
						  jdbz=SSProcess.Cross_P (resx, resy, xxx(i), yyy(i), xxx(i+1), yyy(i+1),xxx(j), yyy(j), xxx(j+1),yyy(j+1))
                    If jdbz=0 Then
									  checkpolyon="坐标串自交叉"
```

---

### `Cross_L`

**功能：** 计算线线交叉

- **调用次数：** 5
- **使用文件数：** 3

**示例：**

```vbs
SSFunc.ScanString strids, ",", zxid, zxidCount
		crossxy = SSProcess.Cross_L (x1, y1, x2, y2, zxid(0) )
		SSFunc.ScanString crossxy, ",", xy, xyCount
		cross_x = xy(0)
```

---

### `GetNeardist`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
'查找最近边
       dist = SSProcess.GetNeardist(idlist(0), spx, spy , nearindex)
       '最近边坐标
        SSProcess.GetObjectPoint idlist(0), nearindex-1, x0,  y0,  z0,  ptype,  name
```

---

### `Perpend_P`

**功能：** 计算垂足点

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
'求垂足点
        SSProcess.Perpend_P perpx, perpy,spx, spy, x0, y0, x1, y1
         dist = 0.0
         noteangle = 0.0
```

---

### `DistPerpend`

**功能：** 计算点到线的垂直距离

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
z = SSProcess.GetObjectAttr( gid(j), "SSObj_Z")
					SSProcess.DistPerpend resx,resy,pResRelation,x,y,x1,y1,x2,y2  '高程点与断面线的垂足
					pointlist(j,0) = resx : pointlist(j,1) = resy : pointlist(j,2) = z   '记录下垂足点的坐标和高程，作为重置断面线节点的坐标
				next
```

---

## 坐标转换

> 不同坐标系之间的转换（CGCS2000/北京54/西安80/经纬度）

### `xy2000ToLongiLati`

**功能：** CGCS2000坐标转经纬度

- **调用次数：** 87
- **使用文件数：** 29

**示例：**

```vbs
SSProcess.xy2000ToLongiLati 105, 490767.411, 4158069.119, pB, pL
SSProcess.LongiLatiToxyCGCS2000 105, 37.3316343702, 104.5342691688 , pX, pY
```

---

### `LongiLatiToxyCGCS2000`

**功能：** 经纬度转CGCS2000坐标

- **调用次数：** 74
- **使用文件数：** 25

**示例：**

```vbs
SSProcess.xy2000ToLongiLati 105, 490767.411, 4158069.119, pB, pL
SSProcess.LongiLatiToxyCGCS2000 105, 37.3316343702, 104.5342691688 , pX, pY
msgbox   pB
```

---

### `xy54ToLongiLati`

**功能：** 北京54坐标转经纬度

- **调用次数：** 8
- **使用文件数：** 8

**示例：**

```vbs
SSProcess.xy54ToLongiLati "114", xxx(j,jj), yyy(j,jj), pB, pL
						ObjTable.Cell(jj + 2,4).Range.Text= formatnumber(pB,10,-1,0,0)      '"X坐标"    54
						ObjTable.Cell(jj + 2,5).Range.Text= formatnumber(pL,10,-1,0,0)      '"Y坐标"    54
```

---

### `LongiLatiToxy54`

**功能：** 经纬度转北京54坐标

- **调用次数：** 6
- **使用文件数：** 2

**示例：**

```vbs
SSProcess.xy2000ToLongiLati 113, x1, y, pB, pL
						SSProcess.LongiLatiToxy54 114, pB, pL , pX, pY
                  moveX_BYZD = CDBl(pX) - CDBl(x)   :  moveY_BYZD = CDBl(pY) - CDBl(y)
         End If
```

---

### `TransCoord_7pEx`

**功能：** 七参数坐标转换

- **调用次数：** 6
- **使用文件数：** 3

**示例：**

```vbs
'y=y-101000
					SSProcess.TransCoord_7pEx xoffset, yoffset, srcLon, tagLon, srcCoordType, tagCoordType, srcEllipsoid, tagEllipsoid, dx, dy, dz, dxa, dya, dza, dm, x, y, z, x1, y1, z1
               SSProcess.SetObjectPoint id, j,y1,x1,z1,pointtype,name, 0
					SSProcess.SetObjectAttr id, "SSObj_DataMark", "2000(109)"
```

---

### `LongiLatiToxyz80`

- **调用次数：** 2
- **使用文件数：** 2

**示例：**

```vbs
SSProcess.LongiLatiToxyz80 lon0 , b, l , h, pX , pY, pZ
Msgbox "pX:"& pX&chr(13)& "pY:"&pY&chr( 13)&"pZ:" &pZ
```

---

## 拓扑处理

> 对象的合并、分割、拓扑关系重建等空间分析操作

### `ObjectDeal`

**功能：** 对象拓扑处理

- **调用次数：** 228
- **使用文件数：** 108

**示例：**

```vbs
next
		SSProcess.ObjectDeal objID, "AddToSelection", "", result
		SSProcess.ObjectDeal 0, "FreeSelectionObjectDisplayList", "", result
      SSProcess.RefreshView
```

---

### `MergeObjByCondition`

**功能：** 按条件合并对象

- **调用次数：** 150
- **使用文件数：** 122

**示例：**

```vbs
SSProcess.UpdateSysSelection 1
		SSProcess.MergeObjByCondition "2", "2", 0.05, 0, "", 0, "", 1, 0
		SSProcess.ClearSelection
```

---

### `MergePolygon`

**功能：** 合并多边形

- **调用次数：** 24
- **使用文件数：** 18

**示例：**

```vbs
SSProcess.PushUndoMark
       polygonID = SSProcess.MergePolygon (objIDs, 0.001, inheritAttrID, 1 )
       SSProcess.RefreshView
      SSProcess.ClearSelection
```

---

### `DangleCleanLineToLine`

**功能：** 清除悬挂线

- **调用次数：** 11
- **使用文件数：** 10

**示例：**

```vbs
plj=(zg* 2/3)/100/1000 * mscale
      SSProcess.DangleCleanLineToLine "2101000", 0.001, 1, 0
      deloldbc()
      Toparea()
```

---

### `MergeObjPointList`

- **调用次数：** 7
- **使用文件数：** 7

**示例：**

```vbs
Next
    If code1ids<>"" Then SSProcess.MergeObjPointList code1ids, 0.001, 1
End Function
```

---

### `LineCrack`

- **调用次数：** 3
- **使用文件数：** 3

**示例：**

```vbs
SSProcess.SetObjectAttr GeoMaxID, "SSObj_Color", "RGB(255,0,0)"
			SSProcess.LineCrack objID, 0
			'删除中心点
			ids = SSProcess.SearchNearObjIDs(x, y, 0.01, 0, "680316301", 0 )
```

---

### `MergeIslandAreaObj`

- **调用次数：** 2
- **使用文件数：** 1

**示例：**

```vbs
SSProcess.SelectFilter
									SSProcess.MergeIslandAreaObj "Land_Classification"
							SSProcess.ClearSelection
```

---

### `SplitPolygon`

**功能：** 分割多边形

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
'分割多边形,并保留原面
       sids = SSProcess.SplitPolygon (areaID, lineID, 0 )
       '与面相关的弧段做悬挂处理
       TopArcDeal areaID
```

---

### `RebuildTopRelation`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
'先单元处理polygonID
      SSProcess.RebuildTopRelation "面", "界线",  0.001
End Function
```

---

## 检查记录

> 数据质量检查结果的记录和输出

### `AddCheckRecord`

- **调用次数：** 2,896
- **使用文件数：** 683

**示例：**

```vbs
SSProcess.GetSelGeoPoint i, 0, x, y, z, pointtype, name
						SSProcess.AddCheckRecord "房产检查", "一层非建基面积块检查", "自定义脚本检查类->一层非建基面积块检查", "一层面积块为非建基面积,建基面积类型: "& jjmjType, x, y, z, geoType, geoID, ""
             End If
		Next
```

---

### `RemoveCheckRecord`

- **调用次数：** 679
- **使用文件数：** 651

**示例：**

```vbs
SSProcess.RemoveCheckRecord  "房产检查", "一层非建基面积块检查"
		geoCount = SSProcess.GetSelGeoCount()
		For i=0 To geoCount-1
```

---

### `ShowCheckOutput`

- **调用次数：** 239
- **使用文件数：** 232

**示例：**

```vbs
Next
		SSProcess.ShowCheckOutput
End Sub
```

---

### `GetCheckRecordValue`

- **调用次数：** 31
- **使用文件数：** 16

**示例：**

```vbs
For i=0 To gs-1
               SSProcess.GetCheckRecordValue i, "CHECKNAME,GEOIDLIST,NOTEIDLIST", strValues
               SSFunc.ScanString strValues,",",strs,count
               If strs(0)="FeatureGUID重复检查" Then
```

---

### `GetCheckRecordCount`

- **调用次数：** 31
- **使用文件数：** 24

**示例：**

```vbs
Dim strs(100),count  :  jlid=""
        gs=SSProcess.GetCheckRecordCount
        For i=0 To gs-1
               SSProcess.GetCheckRecordValue i, "CHECKNAME,GEOIDLIST,NOTEIDLIST", strValues
```

---

### `ClearCheckRecord`

- **调用次数：** 18
- **使用文件数：** 18

**示例：**

```vbs
SSProcess.AccessMoveFirst Projectname,sql
      SSProcess.ClearCheckRecord
		SSProcess.GetAccessRecord Projectname, sql ,pkfields, values
		'msgbox values
```

---

### `SaveCheckRecord`

- **调用次数：** 7
- **使用文件数：** 6

**示例：**

```vbs
SSProcess.ShowCheckOutput
		SSProcess.SaveCheckRecord
End Sub
```

---

### `LoadCheckRecord`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
'SSProcess.MapCallBackFunction "SDLCommand", "$sscheck,ck",0
				'SSProcess.LoadCheckRecord
				'SSProcess.ShowCheckOutput
				SSProcess.SaveCheckRecord
```

---

### `WriteCheckRecord`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
SSProcess.SaveCheckRecord
				'SSProcess.WriteCheckRecord
				SSProcess.CloseAccessMdb edbname
End Sub
```

---

## 加解密

> EPS脚本的加密和解密功能

### `DecryptData`

- **调用次数：** 3
- **使用文件数：** 3

**示例：**

```vbs
reportHouseGUID = SSProcess.ReadEpsXMLIni (0, "HouseSetup\ReportHouseGUID" , "" )
      dbPassword = SSProcess.DecryptData ("~!@#", dbPassword )
  '连接到房产数据库连接
    set adoConn = CreateObject("ADODB.Connection")
```

---

### `EncryptData`

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
password = "adgagaer"                '密码
  strInfo_Encrypt = SSProcess.EncryptData( password , strInfo)         '加密字符串
  strInfo_Decrypt = SSProcess.DecryptData(password ,strInfo_Encrypt)   ' 解密字符串
  strmsg =  " 字符串内容： "&strInfo&chr(13) &" 加密后内容： "&strInfo_Encrypt&chr(13)&" 解密后内容： "&strInfo_Decrypt
```

---

## 其他方法

- `SaveBufferObjToDatabase` (1,905次调用) — 
- `XYSA` (1,328次调用) — 
- `GetGeoMaxID` (792次调用) — 
- `ByteStackStore` (247次调用) — 
- `ClearselectConditionGroups` (125次调用) — 
- `GetFeatureCodeInfo` (95次调用) — 
- `ByteStackRestore` (55次调用) — 
- `FindFeatureCode` (45次调用) — 
- `LockGeoPointsInMemory` (41次调用) — 
- `RadianToDeg` (36次调用) — 
- `Getselgeovalue` (36次调用) — 
- `SetFeatureCodeTB` (31次调用) — 
- `SetNewObjAttr` (28次调用) — 
- `SendFrameMessage` (16次调用) — 
- `IsExistentFeatureCode` (10次调用) — 
- `GetColorIndex` (10次调用) — 
- `LabelAttrToAreaAttr` (9次调用) — 
- `AreaAttrToLabelAttr` (9次调用) — 
- `ClearsysSelection` (9次调用) — 
- `GetFieldCodeMap` (8次调用) — 
- `GetGridSelRowIndex` (8次调用) — 
- `GetGridSelRowCount` (8次调用) — 
- `ClearSelectionObjNodeSymbol` (7次调用) — 
- `CloseSelectionObj` (7次调用) — 
- `clearSelectionobjnodesymbol` (6次调用) — 
- `RadianToDms` (6次调用) — 
- `getgridcellinfo` (6次调用) — 
- `ZoomInoutPolygon` (5次调用) — 
- `MapCallBackFunction1` (5次调用) — 
- `DeleteObjectPoint` (5次调用) — 

---

## SSFunc 工具函数

> 提供字符串处理、数学计算等工具函数

### `SSFunc.ScanString`

**功能：** 按分隔符拆分字符串到数组

- **调用次数：** 4,769
- **使用文件数：** 1249

**示例：**

```vbs
if arArray(6) <> "" then
				SSFunc.ScanString arArray(6),";",arArray2,ncount2
				line = 5
				for j = 0 to  ncount2 -1
```

---

### `SSFunc.Scanstring`

**功能：** 按分隔符拆分字符串到数组（小写版本）

- **调用次数：** 1,784
- **使用文件数：** 81

**示例：**

```vbs
GetALLDHXKZ DHXKZ
		SSFunc.Scanstring DHXKZ,",",FDHXKZ,FDHXKZCount
		For i = 0 to FDHXKZCount - 1
			Erase SDHXKZ:Erase FFCXX
```

---

### `SSFunc.atof`

**功能：** 字符串转浮点数

- **调用次数：** 187
- **使用文件数：** 3

**示例：**

```vbs
JCLX=SSProcess.GetSelGeoValue(i, "[楼层信息]")
         JCQSC=formatnumber(SSFunc.atof(JCLX),0)
         JCCS=JCQSC+SSFunc.atof (JCCS1)-1
         JCGD=formatnumber(JCCS*SSFunc.atof (JCCG),2)
```

---

### `SSFunc.GetChineseDigit`

**功能：** 获取中文数字

- **调用次数：** 182
- **使用文件数：** 20

**示例：**

```vbs
If replace( cengci, "-", "") <> cengci Then
						cchh = "地下"&SSFunc.GetChineseDigit(replace(cengci,"-",""))&"层"
				Else
						cchh = SSFunc.GetChineseDigit(cengci)&"层"
```

---

### `SSFunc.DrawToImage`

**功能：** 绘制到图片

- **调用次数：** 64
- **使用文件数：** 38

**示例：**

```vbs
dpi = 300
			SSFunc.DrawToImage minX, minY, maxX, maxY, strPaperSize, dpi, PictureFileName '输出指定范围内的图形到bmp图片
			Set iShape = wApp.Selection.InlineShapes.AddPicture (PictureFileName,False,True) '插入图片
```

---

### `SSFunc.SortArrayByValue`

**功能：** 按值排序数组

- **调用次数：** 59
- **使用文件数：** 10

**示例：**

```vbs
SSProcess.CloseAccessMdb ProjectName
	SSFunc.SortArrayByValue CM, CH, AllLcInfoCount, 1, 3
	SSFunc.SortArrayByValue GC, arids0, AllLcInfoCount, 1, 3
	SSFunc.SortArrayByValue JG, arids1, AllLcInfoCount, 1, 3
```

---

### `SSFunc.OutputGraphToBmp`

**功能：** 输出图形为BMP图片

- **调用次数：** 42
- **使用文件数：** 6

**示例：**

```vbs
Sub OnClick()
		SSFunc.OutputGraphToBmp 27500, 27400, 27750, 27600, 450, "C:\1.bmp"
		'SSFunc.OutputGraphToBmp 27619.042819617607, 27519.606229527188, 27630.406154915068, 27524.226486736046, 20, "C:\1.bmp"
```

---

### `SSFunc.GetObjectRect`

**功能：** 获取对象矩形范围

- **调用次数：** 34
- **使用文件数：** 34

**示例：**

```vbs
idds(0)=id
            SSFunc.GetObjectRect idds, 1, 0, rects
            for k=0 To 3
                  rects(k)=CDbl(rects(k))
```

---

### `SSFunc.SelectListAttr`

**功能：** 选择列表属性

- **调用次数：** 14
- **使用文件数：** 11

**示例：**

```vbs
ResVal_Dlg =SSFunc.SelectListAttr("选择列表", "待选数据列表", "选中数据列表", arRecordShortList1, RecordShortListCount1)
      If ResVal_Dlg<>1 Then Exit Sub
      If RecordShortListCount1=0 Then Exit Sub
```

---

### `SSFunc.GetBinaryBitValue`

**功能：** 获取二进制位值

- **调用次数：** 10
- **使用文件数：** 7

**示例：**

```vbs
SSProcess.GetSelGeoPoint i, k, x1,  y1,  z1,  ptype,  name
								if SSFunc.GetBinaryBitValue(ptype, 1) then
										AddLine x1,y1
								end if
```

---

### `SSFunc.ExcelSelectFile`

**功能：** Excel文件选择

- **调用次数：** 2
- **使用文件数：** 1

**示例：**

```vbs
Dim arFile(20),nRecordCount
		aa = SSFunc.ExcelSelectFile(arFile, nFileCount)
		if aa = 0 then exit Sub
		strFile = arFile(0)
```

---

### `SSFunc.AutoTrimExtend`

**功能：** 自动裁剪扩展

- **调用次数：** 1
- **使用文件数：** 1

**示例：**

```vbs
'返回值：处理的地物个数
		nDealCount= SSFunc.AutoTrimExtend("9112031", geocode,"1,0,100,1")
		'清空选择
		SSProcess.ExecuteSDLFunction"$SDL.SSEdit.SelectionEmpty",0
```

---

## SSERPTool ERP集成

> 提供与EPS ERP系统的集成功能

### `SSERPTool.GetTokenAndInvalidTime`

**功能：** 获取ERP访问令牌和过期时间

- **调用次数：** 961
- **使用文件数：** 302

---

### `SSERPTool.GetUserInfo`

**功能：** 获取当前登录用户信息（姓名、ID、部门）

- **调用次数：** 533
- **使用文件数：** 333

---

### `SSERPTool.IsLogin`

**功能：** 检查是否已登录ERP系统

- **调用次数：** 289
- **使用文件数：** 283

---

### `SSERPTool.GetCurWorkInfo`

**功能：** 获取当前工作信息

- **调用次数：** 124
- **使用文件数：** 67

---

### `SSERPTool.ClearWorkInfo`

**功能：** 清除工作信息

- **调用次数：** 9
- **使用文件数：** 9

---

### `SSERPTool.FormLogin`

**功能：** 表单登录

- **调用次数：** 6
- **使用文件数：** 6

---

### `SSERPTool.GetNewWorkInfo`

**功能：** 获取新工作信息

- **调用次数：** 4
- **使用文件数：** 4

---

### `SSERPTool.Logout`

**功能：** 退出登录

- **调用次数：** 1
- **使用文件数：** 1

---

### `SSERPTool.GetUserNameAndUserID`

**功能：** 获取用户名和用户ID

- **调用次数：** 1
- **使用文件数：** 1

---

### `SSERPTool.Login`

**功能：** 登录

- **调用次数：** 1
- **使用文件数：** 1

---

## SSParameter 参数管理

> 用于读写EPS脚本参数

### `SSParameter.GetParameterSTR`

**功能：** 获取字符串类型的脚本参数

- **调用次数：** 459
- **使用文件数：** 113

---

### `SSParameter.SetParameterSTR`

**功能：** 设置字符串类型的脚本参数

- **调用次数：** 310
- **使用文件数：** 192

---

### `SSParameter.GetParameterINT`

**功能：** 获取整数类型的脚本参数

- **调用次数：** 155
- **使用文件数：** 141

---

### `SSParameter.SetParameterINT`

**功能：** 设置整数类型的脚本参数

- **调用次数：** 104
- **使用文件数：** 28

---

### `SSParameter.GetParameterDBL`

**功能：** 获取双精度浮点类型的脚本参数

- **调用次数：** 3
- **使用文件数：** 3

---

## 第二部分：使用场景实战指南

---

### 如何创建一个EPS脚本

新建一个 .vbs 文件，写入以下基本结构：

```vbs
Sub OnClick()
    ' 你的业务逻辑写在这里
    MsgBox "Hello EPS!"
End Sub
```

**关键点：**
- 入口必须是 `Sub OnClick()` —— 这是EPS脚本管理器识别的标准入口
- 也可以使用 `Sub OnInitScript()` 作为初始化入口
- 用 `End Sub` 结束
- 变量无需声明即可使用（VBScript特性）

---

### 如何获取当前工程信息

```vbs
Sub GetProjectInfo()
    ' 获取工程文件路径
    edbname = SSProcess.GetProjectFileName
    
    ' 获取EPS系统路径
    sysPath = SSProcess.GetSysPathName(0)  ' 0=系统目录
    tplPath = SSProcess.GetTemplateFileName
    scriptPath = SSProcess.GetScriptPath
    
    MsgBox "工程文件: " & edbname
    MsgBox "系统路径: " & sysPath
End Sub
```

---

### 如何登录和获取用户信息

```vbs
Sub CheckLogin()
    ' 检查是否已登录
    isl = SSERPTool.IsLogin
    If isl = 0 Then
        MsgBox "请先登录EPS系统！"
        Exit Sub
    End If
    
    ' 获取当前用户信息
    SSERPTool.GetUserInfo UserName, UserID, DeptName
    
    MsgBox "用户: " & UserName
    MsgBox "部门: " & DeptName
    MsgBox "用户ID: " & UserID
    
    ' 获取ERP Token（用于接口调用）
    SSERPTool.GetTokenAndInvalidTime Token, InvalidTime
    MsgBox "Token: " & Token
End Sub
```

---

### 如何操作选择集

选择集是EPS脚本中最常用的功能——先筛选对象，再遍历处理。

```vbs
Sub ProcessSelection()
    ' 1. 设置筛选条件
    SSProcess.SetSelectCondition "SSObj_Code", "==", "3103013"  ' 按编码筛选
    ' SSProcess.SetSelectCondition "GeType", "==", "Polygon"     ' 按类型筛选
    SSProcess.SelectFilter  ' 执行筛选
    
    ' 2. 遍历选择集
    count = SSProcess.GetSelGeoCount
    For i = 0 To count - 1
        ' 获取对象属性
        objID = SSProcess.GetSelGeoValue(i, "SSObj_ID")
        area = SSProcess.GetSelGeoValue(i, "SSObj_Area")
        
        ' 获取对象坐标
        px = SSProcess.GetSelGeoPoint(i, 0, 0)  ' 第i个对象,第0个点,X坐标
        py = SSProcess.GetSelGeoPoint(i, 0, 1)  ' 第i个对象,第0个点,Y坐标
        
        ' 修改属性
        SSProcess.SetSelGeoValue(i, "自定义字段", "新值")
    Next
    
    ' 3. 清理
    SSProcess.ClearSelection
    SSProcess.ClearSelectCondition
End Sub
```

**常用筛选条件：**
- `SSObj_Code == "3103013"` — 按地物编码
- `GeType == "Polygon"` — 按几何类型（Polygon/Polyline/Point/Note）
- `SSObj_Layer == "JZJ"` — 按图层名
- `SSObj_DataMark <> "OK"` — 按数据标记

---

### 如何读写Access数据库

EPS工程内置Access MDB数据库，用于存储业务数据。

```vbs
Sub DatabaseDemo()
    ' 打开数据库
    edbname = SSProcess.GetProjectFileName
    SSProcess.OpenAccessMdb edbname
    
    ' 查询数据
    sql = "SELECT [DJH], [ZRZH] FROM [ZD_宗地基本信息表] WHERE [面积] > 100"
    SSProcess.OpenAccessRecordset edbname, sql
    rscount = SSProcess.GetAccessRecordCount(edbname, sql)
    
    MsgBox "查询到 " & rscount & " 条记录"
    
    ' 遍历记录
    If rscount > 0 Then
        SSProcess.AccessMoveFirst edbname, sql
        While SSProcess.AccessIsEOF(edbname, sql) = False
            SSProcess.GetAccessRecord edbname, sql, fields, values
            ' fields = "DJH,ZRZH"
            ' values = "440606001,001"
            
            ' 解析字段值
            Dim farr(100), varr(100), fcount, vcount
            SSFunc.ScanString fields, ",", farr, fcount
            SSFunc.ScanString values, ",", varr, vcount
            
            MsgBox "地籍号: " & varr(0)
            
            SSProcess.AccessMoveNext edbname, sql
        Wend
    End If
    
    ' 关闭
    SSProcess.CloseAccessRecordset edbname, sql
    SSProcess.CloseAccessMdb edbname
End Sub
```

**修改记录：**
```vbs
SSProcess.OpenAccessMdb edbname
sql = "SELECT * FROM [表名] WHERE [条件]"
SSProcess.OpenAccessRecordset edbname, sql
SSProcess.AccessMoveFirst edbname, sql
SSProcess.ModifyAccessRecord edbname, sql, "[字段名]", "新值"
SSProcess.CloseAccessRecordset edbname, sql
SSProcess.CloseAccessMdb edbname
```

---

### 如何导入导出数据

```vbs
' === 导出为DWG ===
Sub ExportToDWG()
    SSProcess.ClearDataXParameter
    SSProcess.SetDataXParameter "DataType", "1"
    SSProcess.SetDataXParameter "Version", "14"
    SSProcess.SetDataXParameter "FeatureCodeTBName", "FeatureCodeTB_OutDwg"
    SSProcess.SetDataXParameter "SymbolScriptTBName", "SymbolScriptTB_OutDwg"
    SSProcess.SetDataXParameter "ExportPathName", "C:\output.dwg"
    SSProcess.SetDataXParameter "FontWidthScale", "0.7"
    SSProcess.SetDataXParameter "FontHeightScale", "0.7"
    SSProcess.ExportData
    MsgBox "DWG导出完成！"
End Sub

' === 导入DWG ===
Sub ImportFromDWG()
    fctnames = SSProcess.SelectFileName(1, "", 1, "Files(*.dwg)|*.dwg||")
    If fctnames = "" Then Exit Sub
    
    SSProcess.ClearDataXParameter
    SSProcess.SetDataXParameter "DataType", "1"
    SSProcess.SetDataXParameter "ImportFileName", fctnames
    SSProcess.ImportData
    MsgBox "DWG导入完成！"
End Sub

' === 读取配置 ===
Sub ReadConfig()
    val = SSProcess.ReadEpsIni("section", "key", "default")
    SSProcess.WriteEpsIni "section", "key", "newvalue"
End Sub
```

---

### 如何调用ERP接口

```vbs
Function CallERPInterface(methodName, params)
    ' 获取Token
    SSERPTool.GetTokenAndInvalidTime Token, InvalidTime
    
    Set xmlhttp = CreateObject("Microsoft.XMLHTTP")
    xmlhttp.Open "POST", "http://erp-server/api", False
    xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"
    
    parameter = "_namespace=erp.gis.arcgisserverhelper.interfaceentry"
    parameter = parameter & "&access_token=" & Token
    parameter = parameter & "&methodname=" & methodName
    parameter = parameter & "&parameter=" & params
    
    xmlhttp.Send parameter
    
    If xmlhttp.readyState = 4 Then
        If xmlhttp.status = 200 Then
            CallERPInterface = xmlhttp.responseText
        End If
    End If
    
    Set xmlhttp = Nothing
End Function
```

---

### 如何显示进度条和对话框

```vbs
Sub ShowProgress()
    ' 创建进度条
    SSProcess.EpsProgressCreate "正在处理..."
    SSProcess.EpsProgressSetStep 100  ' 设置总步数
    
    For i = 0 To 99
        ' 处理逻辑...
        
        SSProcess.EpsProgressStepIt  ' 进度+1
        SSProcess.EpsProgressUpdateMsg "正在处理第 " & (i+1) & " 项..."
    Next
    
    SSProcess.EpsProgressDelete  ' 关闭进度条
End Sub

Sub ShowDialog()
    ' 显示输入参数对话框
    SSProcess.ClearInputParameter
    SSProcess.AddInputParameter "地籍号", "string", "请输入地籍号"
    SSProcess.AddInputParameter "面积", "double", "请输入面积"
    SSProcess.ShowInputParameterDlg "数据录入", "确定", "取消"
    
    ' 获取用户输入
    djh = SSProcess.GetInputParameter("地籍号")
    area = SSProcess.GetInputParameter("面积")
    
    MsgBox "地籍号: " & djh & ", 面积: " & area
End Sub
```

---

### 如何创建新地图对象

```vbs
Sub CreateObject()
    ' 创建新的面状对象
    SSProcess.CreateNewObj "Polygon"  ' 或 "Polyline"/"Point"/"Note"
    
    ' 设置编码
    SSProcess.CreateNewObjByCode "3103013"
    
    ' 添加坐标点
    SSProcess.AddNewObjPoint x1, y1, z1
    SSProcess.AddNewObjPoint x2, y2, z2
    SSProcess.AddNewObjPoint x3, y3, z3
    SSProcess.AddNewObjPoint x1, y1, z1  ' 闭合
    
    ' 加入保存列表
    SSProcess.AddNewObjToSaveObjList
    
    ' 保存到数据库
    SSProcess.SaveBufferObjToDatabase
    
    ' 刷新显示
    SSProcess.UpdateCurMap
End Sub
```

---

### 如何进行空间查询

```vbs
Sub SpatialQuery()
    ' 获取当前选中的对象ID
    SSProcess.SetSelectCondition "SSObj_Code", "==", "3103013"
    SSProcess.SelectFilter
    
    count = SSProcess.GetSelGeoCount
    If count = 0 Then
        MsgBox "请先选择一个对象"
        Exit Sub
    End If
    
    objID = SSProcess.GetSelGeoValue(0, "SSObj_ID")
    SSProcess.ClearSelection
    SSProcess.ClearSelectCondition
    
    ' 搜索该对象内部的所有对象
    Dim innerIDs(1000)
    innerCount = SSProcess.SearchInnerObjIDs(objID, innerIDs)
    
    ' 搜索附近的对象
    Dim nearIDs(1000)
    nearCount = SSProcess.SearchNearObjIDs(objID, 10.0, nearIDs)  ' 10米范围内
    
    ' 判断点是否在多边形内
    result = SSProcess.IsPtInPoly(px, py, objID)
    If result = 1 Then
        MsgBox "点在多边形内"
    End If
End Sub
```

---

## 第三部分：速查索引

---

### 字母排序索引（共 345 个方法）

| 方法 | 调用次数 | 文件数 | 说明 |
|------|----------|--------|------|
| **C** | | | |
| `SSERPTool.ClearWorkInfo` | 9 | 9 | 清除工作信息 |
| **F** | | | |
| `SSERPTool.FormLogin` | 6 | 6 | 表单登录 |
| **G** | | | |
| `SSERPTool.GetCurWorkInfo` | 124 | 67 | 获取当前工作信息 |
| `SSERPTool.GetNewWorkInfo` | 4 | 4 | 获取新工作信息 |
| `SSERPTool.GetTokenAndInvalidTime` | 961 | 302 | 获取ERP访问令牌和过期时间 |
| `SSERPTool.GetUserInfo` | 533 | 333 | 获取当前登录用户信息（姓名、ID、部门） |
| `SSERPTool.GetUserNameAndUserID` | 1 | 1 | 获取用户名和用户ID |
| **I** | | | |
| `SSERPTool.IsLogin` | 289 | 283 | 检查是否已登录ERP系统 |
| **L** | | | |
| `SSERPTool.Login` | 1 | 1 | 登录 |
| `SSERPTool.Logout` | 1 | 1 | 退出登录 |
| **A** | | | |
| `SSFunc.AutoTrimExtend` | 1 | 1 | 自动裁剪扩展 |
| **D** | | | |
| `SSFunc.DrawToImage` | 64 | 38 | 绘制到图片 |
| **E** | | | |
| `SSFunc.ExcelSelectFile` | 2 | 1 | Excel文件选择 |
| **G** | | | |
| `SSFunc.GetBinaryBitValue` | 10 | 7 | 获取二进制位值 |
| `SSFunc.GetChineseDigit` | 182 | 20 | 获取中文数字 |
| `SSFunc.GetObjectRect` | 34 | 34 | 获取对象矩形范围 |
| **O** | | | |
| `SSFunc.OutputGraphToBmp` | 42 | 6 | 输出图形为BMP图片 |
| **S** | | | |
| `SSFunc.ScanString` | 4,769 | 1249 | 按分隔符拆分字符串到数组 |
| `SSFunc.Scanstring` | 1,784 | 81 | 按分隔符拆分字符串到数组（小写版本） |
| `SSFunc.SelectListAttr` | 14 | 11 | 选择列表属性 |
| `SSFunc.SortArrayByValue` | 59 | 10 | 按值排序数组 |
| **A** | | | |
| `SSFunc.atof` | 187 | 3 | 字符串转浮点数 |
| **G** | | | |
| `SSParameter.GetParameterDBL` | 3 | 3 | 获取双精度浮点类型的脚本参数 |
| `SSParameter.GetParameterINT` | 155 | 141 | 获取整数类型的脚本参数 |
| `SSParameter.GetParameterSTR` | 459 | 113 | 获取字符串类型的脚本参数 |
| **S** | | | |
| `SSParameter.SetParameterINT` | 104 | 28 | 设置整数类型的脚本参数 |
| `SSParameter.SetParameterSTR` | 310 | 192 | 设置字符串类型的脚本参数 |
| **A** | | | |
| `SSProcess.AccessIsEOF` | 1,840 | 624 | 判断记录指针是否到达末尾 |
| `SSProcess.AccessMove` | 6 | 6 |  |
| `SSProcess.AccessMoveFirst` | 1,704 | 414 | 将记录指针移到第一条记录 |
| `SSProcess.AccessMoveLast` | 4 | 4 |  |
| `SSProcess.AccessMoveNext` | 1,904 | 647 | 将记录指针移到下一条记录 |
| `SSProcess.AccessMovePrev` | 4 | 4 |  |
| `SSProcess.AddAccessRecord` | 48 | 48 | 添加新记录 |
| `SSProcess.AddCheckRecord` | 2,896 | 683 |  |
| `SSProcess.AddClipBoardObjToMap` | 99 | 66 |  |
| `SSProcess.AddDispFilterInfo` | 3 | 3 |  |
| `SSProcess.AddFunctionParameter` | 1,567 | 152 | 添加函数参数 |
| `SSProcess.AddInputParameter` | 4,189 | 689 | 添加输入参数 |
| `SSProcess.AddNewObjPoint` | 3,797 | 713 | 为新对象添加坐标点 |
| `SSProcess.AddNewObjToSaveObjList` | 1,884 | 701 | 将新对象加入保存列表 |
| `SSProcess.AddNewObjToSel` | 4 | 4 |  |
| `SSProcess.AddNewObjToSelObjList` | 25 | 10 |  |
| `SSProcess.AddNewObjToSelObjList加入到脚本选择集列表` | 1 | 1 |  |
| `SSProcess.AddSelGeoToSaveGeoList` | 187 | 175 | 将选择集中的图形加入保存列表 |
| `SSProcess.AddSelNoteToSaveNoteList` | 51 | 51 |  |
| `SSProcess.AdjustAngle` | 1 | 1 |  |
| `SSProcess.AdjustGridCtrl` | 31 | 4 |  |
| `SSProcess.Arc3pToCenter` | 66 | 35 | 通过三点计算弧心 |
| `SSProcess.AreaAttrToLabelAttr` | 9 | 7 |  |
| **B** | | | |
| `SSProcess.ByteStackRestore` | 55 | 7 |  |
| `SSProcess.ByteStackStore` | 247 | 19 |  |
| **C** | | | |
| `SSProcess.ChangeCodeByDataTransMap` | 1 | 1 |  |
| `SSProcess.ChangeCodeCopy` | 60 | 50 |  |
| `SSProcess.ChangeCodeCopySelectionObj` | 88 | 53 | 修改选择集对象的编码并复制属性 |
| `SSProcess.ChangeSelectionObjAttr` | 1,395 | 399 | 修改选择集中对象的属性 |
| `SSProcess.Circle3pToCenter` | 173 | 95 | 通过三点计算圆心 |
| `SSProcess.ClearCheckRecord` | 18 | 18 |  |
| `SSProcess.ClearDataXParameter` | 730 | 681 | 清空所有数据转换参数 |
| `SSProcess.ClearDispFilterInfo` | 3 | 3 |  |
| `SSProcess.ClearFunctionParameter` | 146 | 145 | 清空函数参数 |
| `SSProcess.ClearInputParameter` | 803 | 634 | 清空输入参数 |
| `SSProcess.ClearOutput` | 2 | 2 |  |
| `SSProcess.ClearSelectCondition` | 7,515 | 2659 | 清除选择过滤条件 |
| `SSProcess.ClearSelectConditionGroups` | 696 | 372 |  |
| `SSProcess.ClearSelection` | 7,520 | 2713 | 清空当前选择集 |
| `SSProcess.ClearSelectionObjNodeSymbol` | 7 | 7 |  |
| `SSProcess.ClearSysSelection` | 616 | 280 | 清空系统选择集 |
| `SSProcess.ClearselectConditionGroups` | 125 | 24 |  |
| `SSProcess.ClearsysSelection` | 9 | 9 |  |
| `SSProcess.CloseAccessMdb` | 1,981 | 782 | 关闭Access MDB数据库 |
| `SSProcess.CloseAccessRecordset` | 2,383 | 755 | 关闭记录集 |
| `SSProcess.CloseDatabase` | 482 | 271 | 关闭当前打开的数据库 |
| `SSProcess.CloseScriptDlg` | 393 | 203 | 关闭脚本对话框 |
| `SSProcess.CloseSelectionObj` | 7 | 7 |  |
| `SSProcess.CopyObjectAttr` | 17 | 17 | 复制对象属性到另一个对象 |
| `SSProcess.CreateDatabase` | 187 | 186 | 创建新的EDB数据库文件 |
| `SSProcess.CreateGridCtrl` | 5 | 4 | 创建Grid控件 |
| `SSProcess.CreateMapFrame` | 15 | 15 | 创建图框 |
| `SSProcess.CreateMapFrameByRegion` | 2 | 2 |  |
| `SSProcess.CreateMapFrameByRegionID` | 2 | 2 |  |
| `SSProcess.CreateNewObj` | 372 | 168 | 创建新对象（指定类型） |
| `SSProcess.CreateNewObjByClass` | 484 | 259 | 通过分类创建新对象 |
| `SSProcess.CreateNewObjByCode` | 1,148 | 508 | 通过编码创建新对象 |
| `SSProcess.CreateOneMapFrame` | 10 | 10 |  |
| `SSProcess.CreateSelectionAreaLabel` | 2 | 2 |  |
| `SSProcess.Cross_L` | 5 | 3 | 计算线线交叉 |
| `SSProcess.Cross_P` | 5 | 4 | 计算两线交点 |
| `SSProcess.CutRegionToEdb` | 2 | 2 |  |
| **D** | | | |
| `SSProcess.DangleCleanLineToLine` | 11 | 10 | 清除悬挂线 |
| `SSProcess.DecryptData` | 3 | 3 |  |
| `SSProcess.DegToRadian` | 1 | 1 |  |
| `SSProcess.DelAccessRecord` | 29 | 29 | 删除当前记录 |
| `SSProcess.DelSelGeo` | 22 | 14 |  |
| `SSProcess.DelSelNote` | 188 | 104 | 删除注记 |
| `SSProcess.DeleteGridCtrlRow` | 16 | 4 |  |
| `SSProcess.DeleteLayer` | 5 | 5 | 删除图层 |
| `SSProcess.DeleteObject` | 1,088 | 482 | 删除指定对象 |
| `SSProcess.DeleteObjectPoint` | 5 | 4 |  |
| `SSProcess.DeleteSelGeoPoint` | 20 | 20 |  |
| `SSProcess.DeleteSelectionObj` | 1,042 | 619 | 删除选择集中的所有对象 |
| `SSProcess.DistPerpend` | 1 | 1 | 计算点到线的垂直距离 |
| `SSProcess.DmsToDeg` | 3 | 3 |  |
| `SSProcess.DrawLine` | 884 | 95 | 绘制线段 |
| `SSProcess.DrawText` | 3 | 3 | 绘制文字 |
| **E** | | | |
| `SSProcess.EncryptData` | 1 | 1 |  |
| `SSProcess.EpsProgressCreate` | 120 | 119 | 创建进度条 |
| `SSProcess.EpsProgressDelete` | 121 | 118 | 删除进度条 |
| `SSProcess.EpsProgressSetPos` | 8 | 6 |  |
| `SSProcess.EpsProgressSetRange32` | 1 | 1 |  |
| `SSProcess.EpsProgressSetStep` | 114 | 114 | 设置进度条步数 |
| `SSProcess.EpsProgressSetStyle` | 14 | 13 | 设置进度条样式 |
| `SSProcess.EpsProgressStepIt` | 113 | 113 | 进度条前进一步 |
| `SSProcess.EpsProgressUpdateMsg` | 113 | 113 | 更新进度条消息 |
| `SSProcess.ExecuteAccessSql` | 102 | 26 | 执行Access SQL语句 |
| `SSProcess.ExecuteSDLFunction` | 583 | 246 | 执行SDL函数（EPS内置功能） |
| `SSProcess.ExecuteSql` | 42 | 12 | 执行SQL语句 |
| `SSProcess.ExecuteToolboxCommand` | 24 | 8 | 执行工具箱命令 |
| `SSProcess.ExplodeObj` | 1 | 1 |  |
| `SSProcess.ExplodeSelectionObj` | 39 | 39 | 分解选择集中的复合对象 |
| `SSProcess.ExportData` | 442 | 416 | 将当前工程数据导出为指定格式 |
| `SSProcess.ExportDataToStream` | 10 | 10 | 将数据导出到数据流 |
| `SSProcess.ExportDataToStream4House` | 3 | 2 |  |
| **F** | | | |
| `SSProcess.FillGridEditDlg` | 1 | 1 |  |
| `SSProcess.FilterSelectionObjVertex` | 1 | 1 |  |
| `SSProcess.FindFeatureCode` | 45 | 44 |  |
| `SSProcess.FindNoteClass` | 43 | 42 | 查找注记分类 |
| `SSProcess.FreeMapFrame` | 20 | 20 | 释放图框 |
| **G** | | | |
| `SSProcess.Get` | 2 | 2 |  |
| `SSProcess.GetAccessFieldInfo` | 37 | 27 |  |
| `SSProcess.GetAccessRecord` | 2,181 | 731 | 获取当前记录的字段名和值 |
| `SSProcess.GetAccessRecordCount` | 1,880 | 499 | 获取记录集中的记录总数 |
| `SSProcess.GetAccessTableNames` | 8 | 8 |  |
| `SSProcess.GetCheckRecordCount` | 31 | 24 |  |
| `SSProcess.GetCheckRecordValue` | 31 | 16 |  |
| `SSProcess.GetCodeAttrTableName` | 5 | 5 |  |
| `SSProcess.GetColorIndex` | 10 | 5 |  |
| `SSProcess.GetCurMapFrame` | 7 | 7 |  |
| `SSProcess.GetCurMapFrameNumber` | 5 | 5 |  |
| `SSProcess.GetCursorPoint` | 4 | 4 |  |
| `SSProcess.GetCursorStatus` | 121 | 121 |  |
| `SSProcess.GetDistDir` | 6 | 6 | 获取距离和方向 |
| `SSProcess.GetFeatureCodeInfo` | 95 | 28 |  |
| `SSProcess.GetFeatureCodeTB` | 5 | 5 |  |
| `SSProcess.GetFieldCodeMap` | 8 | 7 |  |
| `SSProcess.GetFontClassInfo` | 37 | 6 | 获取字体分类信息 |
| `SSProcess.GetGeoID` | 1 | 1 |  |
| `SSProcess.GetGeoMaxID` | 792 | 379 |  |
| `SSProcess.GetGeoValue` | 2 | 2 |  |
| `SSProcess.GetGridCellInfo` | 302 | 47 | 获取Grid控件单元格信息 |
| `SSProcess.GetGridCtrlCellInfo` | 41 | 4 |  |
| `SSProcess.GetGridCtrlCurRow` | 1 | 1 |  |
| `SSProcess.GetGridCtrlRowCount` | 1 | 1 |  |
| `SSProcess.GetGridCtrlSelRowCount` | 5 | 5 |  |
| `SSProcess.GetGridCtrlSelRowIndex` | 1 | 1 |  |
| `SSProcess.GetGridSelRowCount` | 8 | 8 |  |
| `SSProcess.GetGridSelRowIndex` | 8 | 8 |  |
| `SSProcess.GetImportFileName` | 38 | 38 | 获取最后一次导入的文件名 |
| `SSProcess.GetInputParameter` | 4,618 | 662 | 获取输入参数值 |
| `SSProcess.GetLayerAttrTableName` | 9 | 9 |  |
| `SSProcess.GetLayerCount` | 240 | 208 | 获取图层数量 |
| `SSProcess.GetLayerName` | 240 | 208 | 获取图层名称 |
| `SSProcess.GetLayerStatus` | 1 | 1 |  |
| `SSProcess.GetMapFrameCenterPoint` | 17 | 17 |  |
| `SSProcess.GetMapFrameCount` | 19 | 19 |  |
| `SSProcess.GetMapFrameNumber` | 20 | 14 | 获取图框编号 |
| `SSProcess.GetMapScale` | 173 | 168 | 获取当前地图比例尺 |
| `SSProcess.GetNearDist` | 11 | 10 | 获取最近距离 |
| `SSProcess.GetNearPointIndex` | 6 | 5 |  |
| `SSProcess.GetNeardist` | 2 | 2 |  |
| `SSProcess.GetNoteTemplateTB` | 5 | 5 |  |
| `SSProcess.GetObjectAttr` | 7,721 | 1284 | 获取指定对象的属性值（如编码、图层、面积等） |
| `SSProcess.GetObjectBinaryAttr` | 11 | 7 | 获取对象的二进制属性 |
| `SSProcess.GetObjectFocusPoint` | 639 | 368 | 获取对象的焦点坐标 |
| `SSProcess.GetObjectFocusPointInFrame` | 1 | 1 |  |
| `SSProcess.GetObjectPoint` | 1,675 | 581 | 获取对象的坐标点 |
| `SSProcess.GetPointHeight` | 2 | 2 |  |
| `SSProcess.GetPrivateProfile` | 272 | 68 |  |
| `SSProcess.GetProjectFileName` | 2,327 | 1117 | 获取当前工程文件路径 |
| `SSProcess.GetScriptDlgCellValue` | 29 | 16 |  |
| `SSProcess.GetScriptPath` | 2 | 2 | 获取当前脚本所在目录 |
| `SSProcess.GetSelGeoCount` | 4,514 | 2376 | 获取选择集中图形对象的数量 |
| `SSProcess.GetSelGeoPoint` | 2,118 | 935 | 获取选择集中指定对象的坐标点 |
| `SSProcess.GetSelGeoPointCount` | 922 | 568 | 获取选择集中指定对象的坐标点数 |
| `SSProcess.GetSelGeoValue` | 14,437 | 2344 | 获取选择集中指定对象的属性值 |
| `SSProcess.GetSelNoteCount` | 664 | 400 | 获取选择集中注记的数量 |
| `SSProcess.GetSelNotePoint` | 238 | 172 | 获取注记的坐标点 |
| `SSProcess.GetSelNotePointCount` | 40 | 39 |  |
| `SSProcess.GetSelNoteValue` | 922 | 354 | 获取选择集中注记的属性值 |
| `SSProcess.GetSelPolygonFocus` | 57 | 54 |  |
| `SSProcess.GetSelnoteCount` | 4 | 2 |  |
| `SSProcess.GetSysPathName` | 1,470 | 828 | 获取EPS系统路径（如模板目录、线型目录等） |
| `SSProcess.GetTemplateFileName` | 62 | 44 | 获取模板文件路径 |
| `SSProcess.Getobjectattr` | 166 | 12 |  |
| `SSProcess.GetselGeovalue` | 1 | 1 |  |
| `SSProcess.GetselNoteCount` | 3 | 3 |  |
| `SSProcess.Getselgeovalue` | 36 | 9 |  |
| **I** | | | |
| `SSProcess.ImportData` | 145 | 145 | 导入数据文件（DWG/SHP/MIF等）到当前工程 |
| `SSProcess.ImportDataFromStream` | 133 | 133 | 从数据流导入数据 |
| `SSProcess.ImportDataFromStream4House` | 3 | 2 |  |
| `SSProcess.InsertGridCtrlRow` | 20 | 4 |  |
| `SSProcess.IsClockwise` | 75 | 74 | 判断多边形是否顺时针 |
| `SSProcess.IsExistentFeatureCode` | 10 | 9 |  |
| `SSProcess.IsExistentTable` | 59 | 48 |  |
| `SSProcess.IsPolygonInPolygon` | 149 | 32 | 判断多边形是否在另一个多边形内 |
| `SSProcess.IsPolylineInPolygon` | 17 | 10 | 判断折线是否在多边形内 |
| `SSProcess.IsPtInPoly` | 124 | 54 | 判断点是否在多边形内 |
| `SSProcess.IsPtOnLine` | 15 | 10 | 判断点是否在线上 |
| **L** | | | |
| `SSProcess.LabelAttrToAreaAttr` | 9 | 7 |  |
| `SSProcess.LineCrack` | 3 | 3 |  |
| `SSProcess.LineParallelDist` | 10 | 6 | 计算平行线距离 |
| `SSProcess.LinkNearNoteObj` | 3 | 3 |  |
| `SSProcess.LoadCheckRecord` | 1 | 1 |  |
| `SSProcess.LockGeoPointsInMemory` | 41 | 21 |  |
| `SSProcess.LockObjectPoint` | 2 | 1 |  |
| `SSProcess.LockSelGeoPoint` | 69 | 35 | 锁定/解锁选择集中对象的坐标点 |
| `SSProcess.LockSelNotePoint` | 50 | 25 |  |
| `SSProcess.LongiLatiToxy54` | 6 | 2 | 经纬度转北京54坐标 |
| `SSProcess.LongiLatiToxyCGCS2000` | 74 | 25 | 经纬度转CGCS2000坐标 |
| `SSProcess.LongiLatiToxyz80` | 2 | 2 |  |
| **M** | | | |
| `SSProcess.MapCallBackFunction` | 357 | 154 |  |
| `SSProcess.MapCallBackFunction1` | 5 | 5 |  |
| `SSProcess.MapMethod` | 1,121 | 468 | 调用EPS内置方法 |
| `SSProcess.MergeIslandAreaObj` | 2 | 1 |  |
| `SSProcess.MergeObjByCondition` | 150 | 122 | 按条件合并对象 |
| `SSProcess.MergeObjPointList` | 7 | 7 |  |
| `SSProcess.MergePolygon` | 24 | 18 | 合并多边形 |
| `SSProcess.ModifyAccessRecord` | 64 | 44 | 修改当前记录的字段值 |
| **O** | | | |
| `SSProcess.ObjectDeal` | 228 | 108 | 对象拓扑处理 |
| `SSProcess.OpenAccessMdb` | 2,081 | 795 | 打开Access MDB数据库 |
| `SSProcess.OpenAccessRecordset` | 2,345 | 766 | 打开数据库记录集（执行SQL查询） |
| `SSProcess.OpenDatabase` | 414 | 245 | 打开指定的EDB数据库文件 |
| `SSProcess.OutputText` | 4 | 4 |  |
| **P** | | | |
| `SSProcess.PasteBackgroundImage` | 108 | 107 | 粘贴背景图片 |
| `SSProcess.Perpend_P` | 1 | 1 | 计算垂足点 |
| `SSProcess.PrintMapByCoord` | 97 | 97 | 按坐标范围打印地图 |
| `SSProcess.PushUndoMark` | 1,137 | 746 | 推送撤销标记 |
| **R** | | | |
| `SSProcess.RadianToDeg` | 36 | 27 |  |
| `SSProcess.RadianToDms` | 6 | 6 |  |
| `SSProcess.ReadEpsDBIni` | 1,062 | 217 | 读取EPS数据库配置 |
| `SSProcess.ReadEpsGlobalIni` | 2 | 2 |  |
| `SSProcess.ReadEpsIni` | 1,573 | 424 | 读取EPS配置文件（INI格式） |
| `SSProcess.ReadEpsTemplateIni` | 52 | 26 | 读取EPS模板配置 |
| `SSProcess.ReadEpsXMLIni` | 14 | 2 | 读取EPS XML配置 |
| `SSProcess.RebuildSelectionTopRelation` | 13 | 3 |  |
| `SSProcess.RebuildTopRelation` | 1 | 1 |  |
| `SSProcess.RefreshView` | 522 | 389 | 刷新视图 |
| `SSProcess.RemoveCheckRecord` | 679 | 651 |  |
| `SSProcess.RemoveSelGeo` | 3 | 2 |  |
| `SSProcess.RemoveSelNote` | 1 | 1 |  |
| `SSProcess.RemoveSelectionObjPoint` | 1 | 1 |  |
| `SSProcess.RepairDGXHeight` | 1 | 1 |  |
| `SSProcess.RepairGeoHeight` | 1 | 1 |  |
| `SSProcess.RepairUpdateObject` | 10 | 10 |  |
| `SSProcess.ResetSelGeoByCode` | 70 | 60 |  |
| `SSProcess.ResetSelNoteByFontClass` | 40 | 40 |  |
| **S** | | | |
| `SSProcess.SaveBufferObjToDatabase` | 1,905 | 819 |  |
| `SSProcess.SaveCheckRecord` | 7 | 6 |  |
| `SSProcess.SearchInPolyObjIDs` | 27 | 22 | 搜索指定多边形内的所有对象ID |
| `SSProcess.SearchInnerObjIDs` | 868 | 480 | 搜索指定对象内部的所有对象ID |
| `SSProcess.SearchNearObjIDS` | 48 | 47 |  |
| `SSProcess.SearchNearObjIDs` | 556 | 230 | 搜索指定对象附近的所有对象ID |
| `SSProcess.SearchNearObjIDs1` | 2 | 2 |  |
| `SSProcess.SearchNearObjIDs2` | 3 | 2 |  |
| `SSProcess.SearchObjIDs` | 9 | 9 |  |
| `SSProcess.SearchOuterObjIDs` | 231 | 216 | 搜索指定对象外部的所有对象ID |
| `SSProcess.SearchRelatePolygonIDs` | 27 | 19 | 搜索与指定多边形相关的对象ID |
| `SSProcess.SelGeoGotoPoints` | 143 | 143 | 将视图定位到选择集中的对象 |
| `SSProcess.SelectFileName` | 279 | 261 | 弹出文件选择对话框，返回用户选择的文件路径 |
| `SSProcess.SelectFilter` | 6,658 | 2427 | 执行选择过滤，将符合条件的对象加入选择集 |
| `SSProcess.SelectPathName` | 283 | 262 | 弹出目录选择对话框 |
| `SSProcess.Selection` | 4 | 4 |  |
| `SSProcess.SelectionObjClip` | 99 | 64 | 裁剪选择集中的对象 |
| `SSProcess.SelectionObjInnerInsertPoint` | 2 | 2 |  |
| `SSProcess.SelectionObjMerge` | 76 | 70 | 合并选择集中的对象 |
| `SSProcess.SelectionObjOrderby` | 3 | 3 |  |
| `SSProcess.SelectionObjPartZ` | 5 | 5 |  |
| `SSProcess.SelectionObjToClipBoard` | 81 | 67 |  |
| `SSProcess.SelectionObjTopProcess` | 125 | 125 | 对选择集进行拓扑处理 |
| `SSProcess.SendFrameMessage` | 16 | 8 |  |
| `SSProcess.SendViewMessage` | 5 | 5 |  |
| `SSProcess.SetCurMapFrame` | 14 | 14 |  |
| `SSProcess.SetCursorStatus` | 333 | 199 |  |
| `SSProcess.SetDataXParameter` | 237,145 | 681 | 设置数据转换参数（如格式、版本、编码对照表等） |
| `SSProcess.SetFeatureCodeTB` | 31 | 26 |  |
| `SSProcess.SetFrameCode` | 6 | 6 |  |
| `SSProcess.SetGridCellInfo` | 416 | 50 | 设置Grid控件单元格信息 |
| `SSProcess.SetGridCtrlCellInfo` | 29 | 4 |  |
| `SSProcess.SetGridHeadInfo` | 61 | 50 |  |
| `SSProcess.SetInputParameter` | 199 | 46 |  |
| `SSProcess.SetLayerStatus` | 11,393 | 228 | 设置图层显示状态 |
| `SSProcess.SetMapScale` | 381 | 199 | 设置地图比例尺 |
| `SSProcess.SetMapStatus` | 40 | 17 |  |
| `SSProcess.SetNewObjAttr` | 28 | 2 |  |
| `SSProcess.SetNewObjValue` | 6,516 | 531 |  |
| `SSProcess.SetObjectAttr` | 6,626 | 958 | 设置指定对象的属性值 |
| `SSProcess.SetObjectBinaryAttr` | 20 | 20 | 设置对象的二进制属性 |
| `SSProcess.SetObjectPoint` | 85 | 54 | 设置对象的坐标点 |
| `SSProcess.SetScriptDlgCellOptions` | 34 | 4 |  |
| `SSProcess.SetScriptDlgCellValue` | 135 | 17 |  |
| `SSProcess.SetSelGeoPoint` | 95 | 82 | 设置选择集中指定对象的坐标点 |
| `SSProcess.SetSelGeoValue` | 509 | 143 | 设置选择集中指定对象的属性值 |
| `SSProcess.SetSelNotePoint` | 32 | 31 | 设置注记的坐标点 |
| `SSProcess.SetSelNoteValue` | 222 | 71 | 设置选择集中注记的属性值 |
| `SSProcess.SetSelectCondition` | 14,935 | 2433 | 设置选择过滤条件（如按地物类型、编码等） |
| `SSProcess.SetSelectConditionGROUP` | 5 | 2 |  |
| `SSProcess.SetSelectConditionGroup` | 364 | 83 |  |
| `SSProcess.SetTimer` | 4 | 4 |  |
| `SSProcess.Setobjectattr` | 15 | 9 |  |
| `SSProcess.ShowCheckOutput` | 239 | 232 |  |
| `SSProcess.ShowGridEditDlg` | 28 | 25 | 显示Grid编辑对话框 |
| `SSProcess.ShowGridEditDlg1` | 25 | 25 |  |
| `SSProcess.ShowGridEditDlg2` | 7 | 7 |  |
| `SSProcess.ShowInputParameterDlg` | 549 | 400 | 显示输入参数对话框 |
| `SSProcess.ShowOutput` | 4 | 4 |  |
| `SSProcess.ShowScriptDlg` | 543 | 517 | 显示脚本对话框 |
| `SSProcess.ShowScriptUserDefDlg` | 202 | 202 | 显示自定义脚本对话框 |
| `SSProcess.ShowScriptUserDefDlgEx` | 17 | 17 |  |
| `SSProcess.ShowSelectMenu` | 66 | 35 | 显示选择菜单供用户选择 |
| `SSProcess.ShowSelectMenu1` | 106 | 53 |  |
| `SSProcess.Sleep` | 9 | 9 | 暂停执行 |
| `SSProcess.SplitPolygon` | 1 | 1 | 分割多边形 |
| **T** | | | |
| `SSProcess.TopProcess` | 153 | 152 | 拓扑处理 |
| `SSProcess.TransCoord_7pEx` | 6 | 3 | 七参数坐标转换 |
| `SSProcess.TransSelectionObjToAttr` | 1 | 1 |  |
| **U** | | | |
| `SSProcess.UpdateCurMap` | 766 | 134 | 更新当前地图显示 |
| `SSProcess.UpdateNoteAttrByNoteTemplate` | 2 | 1 |  |
| `SSProcess.UpdateObjAttrByFeatureCode` | 1 | 1 |  |
| `SSProcess.UpdateObjectPoint` | 2 | 1 |  |
| `SSProcess.UpdateScriptDlgParameter` | 730 | 426 |  |
| `SSProcess.UpdateSelGeoPoint` | 31 | 31 |  |
| `SSProcess.UpdateSelNotePoint` | 25 | 25 |  |
| `SSProcess.UpdateSysSelection` | 1,375 | 1065 | 更新系统选择集 |
| **W** | | | |
| `SSProcess.WinExec` | 38 | 38 | 执行外部程序 |
| `SSProcess.WriteCheckRecord` | 1 | 1 |  |
| `SSProcess.WriteEpsDBIni` | 864 | 177 | 写入EPS数据库配置 |
| `SSProcess.WriteEpsIni` | 1,806 | 335 | 写入EPS配置文件 |
| `SSProcess.WriteEpsTemplateIni` | 264 | 60 | 写入EPS模板配置 |
| **X** | | | |
| `SSProcess.XYSA` | 1,328 | 203 |  |
| **Z** | | | |
| `SSProcess.ZoomInoutPolygon` | 5 | 5 |  |
| **C** | | | |
| `SSProcess.clearSelectionobjnodesymbol` | 6 | 6 |  |
| **G** | | | |
| `SSProcess.getgridcellinfo` | 6 | 6 |  |
| **S** | | | |
| `SSProcess.setobjectattr` | 63 | 24 |  |
| **X** | | | |
| `SSProcess.xy2000ToLongiLati` | 87 | 29 | CGCS2000坐标转经纬度 |
| `SSProcess.xy54ToLongiLati` | 8 | 8 | 北京54坐标转经纬度 |

### 最常用方法 Top 20

| 排名 | 方法 | 调用次数 | 文件数 | 说明 |
|------|------|----------|--------|------|
| 1 | `SSProcess.SetDataXParameter` | 237,145 | 681 | 设置数据转换参数（如格式、版本、编码对照表等） |
| 2 | `SSProcess.SetSelectCondition` | 14,935 | 2433 | 设置选择过滤条件（如按地物类型、编码等） |
| 3 | `SSProcess.GetSelGeoValue` | 14,437 | 2344 | 获取选择集中指定对象的属性值 |
| 4 | `SSProcess.SetLayerStatus` | 11,393 | 228 | 设置图层显示状态 |
| 5 | `SSProcess.GetObjectAttr` | 7,721 | 1284 | 获取指定对象的属性值（如编码、图层、面积等） |
| 6 | `SSProcess.ClearSelection` | 7,520 | 2713 | 清空当前选择集 |
| 7 | `SSProcess.ClearSelectCondition` | 7,515 | 2659 | 清除选择过滤条件 |
| 8 | `SSProcess.SelectFilter` | 6,658 | 2427 | 执行选择过滤，将符合条件的对象加入选择集 |
| 9 | `SSProcess.SetObjectAttr` | 6,626 | 958 | 设置指定对象的属性值 |
| 10 | `SSProcess.SetNewObjValue` | 6,516 | 531 |  |
| 11 | `SSFunc.ScanString` | 4,769 | 1249 | 按分隔符拆分字符串到数组 |
| 12 | `SSProcess.GetInputParameter` | 4,618 | 662 | 获取输入参数值 |
| 13 | `SSProcess.GetSelGeoCount` | 4,514 | 2376 | 获取选择集中图形对象的数量 |
| 14 | `SSProcess.AddInputParameter` | 4,189 | 689 | 添加输入参数 |
| 15 | `SSProcess.AddNewObjPoint` | 3,797 | 713 | 为新对象添加坐标点 |
| 16 | `SSProcess.AddCheckRecord` | 2,896 | 683 |  |
| 17 | `SSProcess.CloseAccessRecordset` | 2,383 | 755 | 关闭记录集 |
| 18 | `SSProcess.OpenAccessRecordset` | 2,345 | 766 | 打开数据库记录集（执行SQL查询） |
| 19 | `SSProcess.GetProjectFileName` | 2,327 | 1117 | 获取当前工程文件路径 |
| 20 | `SSProcess.GetAccessRecord` | 2,181 | 731 | 获取当前记录的字段名和值 |

### COM 对象速查

| 对象 | 使用次数 | 文件数 | 用途 |
|------|----------|--------|------|
| `Scripting.FileSystemObject` | 3,100 | 1176 | 文件系统操作（读写文件/目录） |
| `VBScript.RegExp` | 571 | 147 | 正则表达式匹配 |
| `ADODB.Connection` | 353 | 175 | 数据库连接 |
| `MSScriptControl.ScriptControl` | 300 | 300 | 执行JavaScript代码 |
| `ADODB.recordset` | 273 | 149 | 数据库记录集 |
| `Excel.Application` | 194 | 179 | Excel自动化 |
| `Word.Application` | 154 | 89 | Word自动化 |
| `wscript.shell` | 132 | 126 | 执行系统命令 |
| `ADODB.Recordset` | 123 | 18 |  |
| `ADODB.Stream` | 118 | 118 | 二进制流操作 |
| `wscript.network` | 97 | 97 | 网络操作 |
| `SSFileUploadControl.SSUploadFileCtrl` | 85 | 81 | EPS文件上传控件 |
| `Scriptlet.TypeLib` | 57 | 57 |  |
| `scripting.filesystemobject` | 49 | 49 |  |
| `WinHttp.WinHttpRequest.5.1` | 36 | 8 | HTTP请求 |
| `WPS.Application` | 34 | 34 | WPS Office自动化 |
| `KWPS.Application` | 34 | 34 |  |
| `adodb.stream` | 27 | 26 |  |
| `WScript.Shell` | 27 | 26 |  |
| `Word.application` | 24 | 23 |  |
| `AsposeWordsCom.AsposeWordsHelper` | 24 | 14 |  |
| `ADODB.RECORDSET` | 24 | 12 |  |
| `ADODB.COMMAND` | 24 | 12 |  |
| `MSXML.DOMDocument` | 22 | 22 | XML文档解析 |
| `Shell.Application` | 22 | 15 | Shell操作（文件浏览等） |
| `Scripting.Dictionary` | 20 | 17 | 字典/哈希表 |
| `SSFileUploadControl.SSDownloadFileCtrl` | 18 | 10 |  |
| `Wscript.Shell` | 13 | 12 |  |
| `adodb.recordset` | 8 | 8 |  |
| `SSCoordXControl.SSTransCoord` | 7 | 7 |  |
| `MSSOAP.SoapClient` | 6 | 6 |  |
| `InternetExplorer.Application` | 5 | 5 |  |
| `Microsoft.XMLDOM` | 2 | 2 |  |
| `ADOX.Catalog` | 2 | 2 |  |
| `Excel.Sheet` | 2 | 2 |  |
| `AsposeCellsCom.AsposeCellsHelper` | 2 | 2 |  |
| `htmlfile` | 1 | 1 |  |
| `UserAccounts.CommonDialog` | 1 | 1 |  |
| `ADOX.Table` | 1 | 1 |  |
| `MSXML2.ServerXMLHTTP` | 1 | 1 |  |
| `MSXML2.DOMDocument` | 1 | 1 |  |
| `Scripting.Filesystemobject` | 1 | 1 |  |

