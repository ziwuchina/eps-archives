# SSMap.dll EDB属性读取快速深挖
- Module: SSMap.dll
- Path: D:\EPS2026G\SSMap.dll.i64
- Functions: 5119, Strings: 5352

## 字符串命中（Top）
- EDB: 5 hits
  - 0x1013dc02
  - 0x1013dc2a
  - 0x10150a9a
  - 0x1015ca0e
  - 0x1015cb22
- .edb: 3 hits
  - 0x1015cbdc
  - 0x1015cc21
  - 0x101629e1
- FeatureGUID: 14 hits
  - 0x1012e188
  - 0x1012faed
  - 0x1012fb10
  - 0x1015aa56
  - 0x1015aa8d
- GetField: 14 hits
  - 0x10126b03
  - 0x10126b3d
  - 0x10126b71
  - 0x101272d7
  - 0x1012739f
- GetRecord: 9 hits
  - 0x10126811
  - 0x101276e9
  - 0x101277b1
  - 0x10127f31
  - 0x1014a609
- DBF: 10 hits
  - 0x10127148
  - 0x1012716c
  - 0x101275b0
  - 0x10138f88
  - 0x10139efc
- MDB: 1 hits
  - 0x10152924

## 关键地址Xref与伪代码片段

### 0x1013dc02
- xrefs: none

### 0x1013dc2a
- xrefs: none

### 0x10150a9a
- xrefs: none

### 0x1015ca0e
- xrefs: none

### 0x1015cb22
- xrefs: none

### 0x1015cbdc
- xrefs: none

### 0x1015cc21
- xrefs: none

### 0x101629e1
- xrefs: none

### 0x1012e188
- xrefs: none

### 0x1012faed
- xrefs: none

### 0x1012fb10
- xrefs: none

### 0x1015aa56
- xrefs: none

## 函数名查询（func_query）

### EDB (10)
- 0x100166a4 ?GetTemplateDB@CScaleMap@@QBEPAVCSSLocalDB@@XZ
- 0x1001a07b ?MapClipToNewEDB@CScaleMap@@QAEHVCString@@ABV?$CArray@VCPoint3D@@AAV1@@@ABVCStringArray@@AAV4@@Z
- 0x10027afe ?SetAutoCreateEdbFileName@@YAXVCString@@@Z
- 0x10027b32 ?GetAutoCreateEdbFileName@@YA?AVCString@@XZ
- 0x1002bda3 ?CheckTemplateDBBaseTable@CDataSource@@AAEHPAVCSSLocalDB@@@Z
- 0x1003284e ?GetTemplateDB@CDataSource@@QBEPAVCSSLocalDB@@XZ
- 0x100b5bc8 ?LoadAttrTableInfoInTemplateDB@@YAHPAVCDataSource@@AAV?$CSSPtrArray@VCFieldInfos@@@@@Z
- 0x100cd820 ?CreateGCSCOREDB@@YAHPAVCSSDatabase@@@Z

### Attribute (1)
- 0x1001299b ?PurgeAttributeDatabase@CScaleMap@@QAEHXZ

### Record (50)
- 0x10002e3c ??0CRecord@@QAE@XZ
- 0x10002e53 ??1CRecord@@UAE@XZ
- 0x10003115 ?SetStrSQL@CDBRecordset@@QAEXVCString@@@Z
- 0x1000314c ?GetStrSQL@CDBRecordset@@QAE?AVCString@@XZ
- 0x100036fa ?GetRecordsetHandle@CSSLocalDB@@QAEPAVCDBRecordset@@W4DBRecordsetEnum@@@Z
- 0x10005fc5 ??0CCheckRecord@@QAE@ABV0@@Z
- 0x10006078 ??4CCheckRecord@@QAEAAV0@ABV0@@Z
- 0x100060f7 ??1CCheckRecord@@QAE@XZ

### Field (50)
- 0x10002ea9 ??1CDBFieldInfo@@QAE@XZ
- 0x10002f29 ??0CDBFieldInfo@@QAE@ABV0@@Z
- 0x10003cec ??0CFieldBandItem@@QAE@XZ
- 0x10003d33 ??1CFieldBandItem@@QAE@XZ
- 0x1002623c ?GetAllFieldInfos@CScaleMap@@QAEHPAVCGeoBase@@AAVCFieldInfos@@@Z
- 0x10026b01 ?GetFieldInfos@CScaleMap@@QAEPBVCFieldInfos@@VCString@@@Z
- 0x10026b59 ?GetFieldNames@CScaleMap@@QAEHIAAVCStringArray@@@Z
- 0x10026f32 ?GetSourceFieldInfoList@CScaleMap@@QAEHAAVCFieldInfos@@@Z

### Coord (38)
- 0x100024c8 ??4CSSTransCoordinate@@QAEAAV0@ABV0@@Z
- 0x10002661 ?SetCoordGridShowStatus@CGLDC@@QAEXH@Z
- 0x1000266e ?GetCoordCridShowStatus@CGLDC@@QBEHXZ
- 0x1000316a ?IsEncryptCoord@CSSDatabase@@QAEHXZ
- 0x10011049 ?GetCoordSystem@CScaleMap@@QBEFXZ
- 0x1001104e ?SetCoordSystem@CScaleMap@@QAEXF@Z
- 0x100bde4b ??0CSSCoordSystem@@QAE@ABV0@@Z
- 0x100bdec8 ??4CSSCoordSystem@@QAEAAV0@ABV0@@Z

### Encrypt (7)
- 0x1000316a ?IsEncryptCoord@CSSDatabase@@QAEHXZ
- 0x100de646 ?GetEncryptCoordSeedID@@YAHXZ
- 0x100de652 ?IsEncryptCoord@@YAHXZ
- 0x100de6ac ?FindEncryptCoordSeedID@@YAHH@Z
- 0x100de9e2 ?SetEncryptCoordSeedID@@YAHH@Z
- 0x100dea48 ?EncryptCoord1@@YAXAAN00JJ@Z
- 0x100df456 ?EnableEncryptCoord@@YAHH@Z

### Decrypt (1)
- 0x100dea4e ?DecryptCoord1@@YAXAAV?$CArray@VCPoint3D@@AAV1@@@J@Z

### Geo (50)
- 0x10002129 ?SetUserID@CGeoBase@@QAEXABVCString@@@Z
- 0x10002135 ?GetUserID@CGeoBase@@QBE?AVCString@@XZ
- 0x1000214c ??1CGeObjList@@UAE@XZ
- 0x10002a32 ?SetPointInfo@CGeoBase@@QAEXHW4PointInfoEnum@@@Z
- 0x10005564 ?SetGeoStartID@CSSVirtualDB@@QAEXI@Z
- 0x1000556e ?GetGeoStartID@CSSVirtualDB@@QAEIXZ
- 0x100059a4 ??0SSGeo@@QAE@XZ
- 0x10005a0b ??1SSGeo@@UAE@XZ

## 已知关键函数二次确认

### 0x1003801d
{   "addr": "0x1003801d",   "code": "void __stdcall CellPie::SetAt(int a1, char a2, int a3, char a4)\n{\n  char v4; // [esp-Ch] [ebp-20h] BYREF\n  int v5; // [esp-8h] [ebp-1Ch]\n  char v6; // [esp-4h] [ebp-18h]\n  char *v7; // [esp+4h] [ebp-10h]\n  int v8; // [esp+10h] [ebp-4h]\n\n  v8 = 0; /*0x1003802a*/\n  v7 = &v4; /*0x10038036*/\n  sub_10038093(&a2); /*0x1003803a*/\n  sub_10043DED(a1, v4, v5, v6); /*0x10038045*/\n  v8 = -1; /*0x1003804a*/\n  CString::~CString((CString *)&a4); /*0x10038051*/\n}" }

### 0x10038044
{   "addr": "0x10038044",   "code": "void __stdcall CellPie::SetAt(int a1, char a2, int a3, char a4)\n{\n  char v4; // [esp-Ch] [ebp-20h] BYREF\n  int v5; // [esp-8h] [ebp-1Ch]\n  char v6; // [esp-4h] [ebp-18h]\n  char *v7; // [esp+4h] [ebp-10h]\n  int v8; // [esp+10h] [ebp-4h]\n\n  v8 = 0; /*0x1003802a*/\n  v7 = &v4; /*0x10038036*/\n  sub_10038093(&a2); /*0x1003803a*/\n  sub_10043DED(a1, v4, v5, v6); /*0x10038045*/\n  v8 = -1; /*0x1003804a*/\n  CString::~CString((CString *)&a4); /*0x10038051*/\n}" }

### 0x10038243
{   "addr": "0x10038243",   "code": "CString *__cdecl sub_100381DE(CString *a1, double X, double a3, int a4)\n{\n  double v4; // st7\n  int v5; // esi\n  int v6; // eax\n  int v7; // eax\n  double v8; // st7\n  int Y; // [esp+10h] [ebp-34h]\n  double v11; // [esp+20h] [ebp-24h]\n  double v12; // [esp+28h] [ebp-1Ch]\n  double v13; // [esp+28h] [ebp-1Ch]\n  _BYTE v14[4]; // [esp+34h] [ebp-10h] BYREF\n  int v15; // [esp+40h] [ebp-4h]\n\n  CString::CString((CString *)v14); /*0x100381f4*/\n  v15 = 1; /*0x10038204*/\n  v12 = fmod(X, 1000.0); /*0x10038217*/\n  v4 = fmod(a3, 1000.0); /*0x1003822e*/\n  v11 = v4; /*0x10038233*/\n  if ( a4 == 500 || a4 == 1000 ) /*0x1003824a*/\n  {\n    if ( v4 >= 500.

### 0x1003824f
{   "addr": "0x1003824f",   "code": "CString *__cdecl sub_100381DE(CString *a1, double X, double a3, int a4)\n{\n  double v4; // st7\n  int v5; // esi\n  int v6; // eax\n  int v7; // eax\n  double v8; // st7\n  int Y; // [esp+10h] [ebp-34h]\n  double v11; // [esp+20h] [ebp-24h]\n  double v12; // [esp+28h] [ebp-1Ch]\n  double v13; // [esp+28h] [ebp-1Ch]\n  _BYTE v14[4]; // [esp+34h] [ebp-10h] BYREF\n  int v15; // [esp+40h] [ebp-4h]\n\n  CString::CString((CString *)v14); /*0x100381f4*/\n  v15 = 1; /*0x10038204*/\n  v12 = fmod(X, 1000.0); /*0x10038217*/\n  v4 = fmod(a3, 1000.0); /*0x1003822e*/\n  v11 = v4; /*0x10038233*/\n  if ( a4 == 500 || a4 == 1000 ) /*0x1003824a*/\n  {\n    if ( v4 >= 500.