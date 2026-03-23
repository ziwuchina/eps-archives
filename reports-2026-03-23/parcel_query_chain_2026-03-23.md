# Parcel Query Chain Trace (SSMap.dll)
## Candidate functions
- [2] 0x1000314c ?GetStrSQL@CDBRecordset@@QAE?AVCString@@XZ (from SQL)
- [2] 0x10003115 ?SetStrSQL@CDBRecordset@@QAEXVCString@@@Z (from SQL)
- [2] 0x100063e6 ?GetRecordSet@CAdoRecordset@@QAE?AV?$_com_ptr_t@V?$_com_IIID@U_Recordset@ADOCG@@$1?_GUID_00000556_0000_0010_8000_00aa006d2ea4@@3U__s_GUID@@A@@@@XZ (from Recordset)
- [2] 0x100036fa ?GetRecordsetHandle@CSSLocalDB@@QAEPAVCDBRecordset@@W4DBRecordsetEnum@@@Z (from Recordset)
- [1] 0x100b6c66 ?GetRecordSQL@CSSMultiMediaAttr@@IAEXAAVCString@@@Z (from SQL)
- [1] 0x10082350 ?GetSelectSQLexpression@CSSLocalDB@@QAEXW4ObjecTypeEnum@@W4DBRecordsetEnum@@AAVCString@@H@Z (from SQL)
- [1] 0x100ddff8 ??1CAdoRecordset@@UAE@XZ (from Recordset)
- [1] 0x100ddff2 ?GetEOF@CAdoRecordset@@QAEHXZ (from Recordset)
- [1] 0x100ddfec ?GetBOF@CAdoRecordset@@QAEHXZ (from Recordset)
- [1] 0x100994a9 ?InitFieldsInfo@CMapboxTable@@AAEHPAVCDBRecordset@@@Z (from Recordset)
- [1] 0x100908a2 ?ExchangeItemValue@CSSLocalDB@@QAEHPAVCDBRecordset@@ABVCString@@ABV?$CArray@UFieldAndValue@@AAU1@@@AAV4@@Z (from Recordset)
- [1] 0x100856dd ?SavePointList@CSSLocalDB@@AAEHW4DBRecordsetEnum@@IABV?$CArray@VCPoint3D@@AAV1@@@@Z (from Recordset)
- [1] 0x1007e429 ?GetCPointRecordsetEnum@@YA?AW4DBRecordsetEnum@@W4ObjecTypeEnum@@@Z (from Recordset)
- [1] 0x1007e404 ?GetGeoRecordsetEnum@@YA?AW4DBRecordsetEnum@@W4ObjecTypeEnum@@@Z (from Recordset)
- [1] 0x1003ecae ?GetAttrTableRS@CUserLayer@@QBEPAVCDBRecordset@@W4ObjecTypeEnum@@@Z (from Recordset)
- [1] 0x1002f00f ?GetAttrTableRS@CDataSource@@QAEPAVCDBRecordset@@VCString@@@Z (from Recordset)
- [1] 0x10026b77 ?GetAttrTableRS@CScaleMap@@QAEPAVCDBRecordset@@VCString@@@Z (from Recordset)
- [1] 0x10006469 ??4CAdoRecordset@@QAEAAV0@ABV0@@Z (from Recordset)
- [1] 0x10006412 ??0CAdoRecordset@@QAE@ABV0@@Z (from Recordset)
- [1] 0x1000640d ?IsEOF@CAdoRecordset@@QAEHXZ (from Recordset)
- [1] 0x10006408 ?IsBOF@CAdoRecordset@@QAEHXZ (from Recordset)
- [1] 0x100dfde6 ?Requery@CDaoRecordset@@UAEXXZ (from Query)
- [1] 0x1002f1f7 ?GetCodeAttrTable@CDataSource@@QAE?AVCString@@HH@Z (from GetCode)
- [1] 0x1002f070 ?GetCodeAttrTables@CDataSource@@QAEXHAAVCStringArray@@H@Z (from GetCode)
- [1] 0x100deeec ?GetAtByname@CFeatureList@@QBEPAVFeatureCode@@ABVCString@@@Z (from FeatureCode)
- [1] 0x100dee92 ?GetAtBycode@CFeatureList@@QBEPAVFeatureCode@@I@Z (from FeatureCode)
- [1] 0x1008d8e4 ?SaveFeatureCode@CSSLocalDB@@QAEHABVCString@@0AAVCFeatureList@@H@Z (from FeatureCode)
- [1] 0x1008d7f3 ?DelFeatureCode@CSSLocalDB@@QAEHABVCString@@0PAVFeatureCode@@@Z (from FeatureCode)
- [1] 0x1008d524 ?UpdateFeatureCode@CSSLocalDB@@QAEHABVCString@@0PAVFeatureCode@@PAVCColorInfoList@@@Z (from FeatureCode)
- [1] 0x1008cb8d ?LoadFeatureCode@CSSLocalDB@@QAEHAAVCFeatureList@@ABVCString@@1HH@Z (from FeatureCode)
- [1] 0x1008c59c ?ResetFeatureFlags@@YAXPAVFeatureCode@@@Z (from FeatureCode)
- [1] 0x1005e43d ?GetFeatureCodes@CUserLayer@@QBEHAAVCUIntArray@@W4ObjecTypeEnum@@@Z (from FeatureCode)
- [1] 0x100557b1 ?SymbolProcess@CDataSource@@QAEHPAVCGeoBase@@AAVCGeObjList@@AAVCMarkNoteList@@2PAVFeatureCode@@@Z (from FeatureCode)
- [1] 0x100552c1 ?SymbolProcess@CScaleMap@@QAEHPAVCGeoBase@@AAVCGeObjList@@AAVCMarkNoteList@@2PAVFeatureCode@@@Z (from FeatureCode)
- [1] 0x100326a4 ?SaveFeatureCode@CDataSource@@QAEHABVCString@@0PAVCFeatureList@@PAVCColorInfoList@@H@Z (from FeatureCode)
- [1] 0x1002ed26 ?GetFeature@CDataSource@@QAEPAVFeatureCode@@I@Z (from FeatureCode)
- [1] 0x10026ee2 ?SetCodeAttrTable@CScaleMap@@QAEHIVCString@@H@Z (from Code)
- [1] 0x10026e4f ?GetCodeAttrTable@CScaleMap@@QAE?AVCString@@IH@Z (from Code)
- [1] 0x10026bcf ?GetCodeAttrTables@CScaleMap@@QAEXIAAVCStringArray@@H@Z (from Code)
- [1] 0x10016b3b ?GetFeatureCodeTableName@CScaleMap@@QBE?AVCString@@XZ (from Code)

## Decompiled snippets

### 0x1000314c ?GetStrSQL@CDBRecordset@@QAE?AVCString@@XZ
{
  "addr": "0x1000314c",
  "code": "CString *__thiscall CDBRecordset::GetStrSQL(int this, CString *a2)\n{\n  CString::CString(a2, (const struct CString *)(this + 160)); /*0x1000315e*/\n  return a2; /*0x10003166*/\n}"
}

### 0x10003115 ?SetStrSQL@CDBRecordset@@QAEXVCString@@@Z
{
  "addr": "0x10003115",
  "code": "void __thiscall CDBRecordset::SetStrSQL(char *this, char a2)\n{\n  CString::operator=(this + 160, &a2); /*0x1000312d*/\n  CString::~CString((CString *)&a2); /*0x10003139*/\n}"
}

### 0x100063e6 ?GetRecordSet@CAdoRecordset@@QAE?AV?$_com_ptr_t@V?$_com_IIID@U_Recordset@ADOCG@@$1?_GUID_00000556_0000_0010_8000_00aa006d2ea4@@3U__s_GUID@@A@@@@XZ
{
  "addr": "0x100063e6",
  "code": "_DWORD *__thiscall CAdoRecordset::GetRecordSet(_DWORD *this, _DWORD *a2)\n{\n  int v2; // eax\n\n  v2 = this[2]; /*0x100063ea*/\n  *a2 = v2; /*0x100063f7*/\n  if ( v2 ) /*0x100063f9*/\n    (*(void (__stdcall **)(int))(*(_DWORD *)v2 + 4))(v2); /*0x100063fe*/\n  return a2; /*0x10006403*/\n}"
}

### 0x100036fa ?GetRecordsetHandle@CSSLocalDB@@QAEPAVCDBRecordset@@W4DBRecordsetEnum@@@Z
{
  "addr": "0x100036fa",
  "code": "int __thiscall CSSLocalDB::GetRecordsetHandle(_DWORD *this, int a2)\n{\n  return *(_DWORD *)(this[40] + 4 * a2); /*0x10003707*/\n}"
}

### 0x100b6c66 ?GetRecordSQL@CSSMultiMediaAttr@@IAEXAAVCString@@@Z
{
  "addr": "0x100b6c66",
  "code": "void __thiscall CSSMultiMediaAttr::GetRecordSQL(const unsigned __int8 **this, struct CString *a2)\n{\n  int v3; // eax\n  const unsigned __int8 *v4; // [esp-10h] [ebp-14h]\n  const unsigned __int8 *v5; // [esp-Ch] [ebp-10h]\n  const unsigned __int8 *v6; // [esp-8h] [ebp-Ch]\n  const unsigned __int8 *v7; // [esp-4h] [ebp-8h]\n\n  v3 = mbscmp(this[4], (const unsigned __int8 *)byte_1015C8B0); /*0x100b6c72*/\n  v7 = this[5]; /*0x100b6c7a*/\n  v6 = this[4]; /*0x100b6c7f*/\n  v5 = this[3]; /*0x100b6c82*/\n  v4 = this[6]; /*0x100b6c85*/\n  if ( v3 ) /*0x100b6c88*/\n    CString::Format(a2, \"Select [%s] From [%s] Where [%s] = '%s';\", v4, v5, v6, v7); /*0x100b6c8f*/\n  else\n    CString::Format(a2, \"Select [%s] From [%s] Where [%s] = %s;\", v4, v5, v6, v7); /*0x100b6c9a*/\n}"
}

### 0x10082350 ?GetSelectSQLexpression@CSSLocalDB@@QAEXW4ObjecTypeEnum@@W4DBRecordsetEnum@@AAVCString@@H@Z
{
  "addr": "0x10082350",
  "code": "void __stdcall CSSLocalDB::GetSelectSQLexpression(int a1, int a2, int a3, int a4)\n{\n  int v4; // edi\n  int v5; // eax\n  int v6; // eax\n  int v7; // eax\n  int v8; // eax\n  int v9; // eax\n  int v10; // eax\n  int v11; // eax\n  int v12; // eax\n  int v13; // eax\n  int v14; // eax\n  int v15; // eax\n  int v16; // eax\n  int v17; // eax\n  int v18; // eax\n  int v19; // eax\n  int v20; // eax\n  int v21; // eax\n  int v22; // eax\n  int v23; // eax\n  int v24; // eax\n  int v25; // eax\n  int v26; // eax\n  int v27; // eax\n  int v28; // eax\n  int v29; // eax\n  int v30; // eax\n  int v31; // eax\n  int v32; // eax\n  int v33; // eax\n  int v34; // eax\n  int v35; // eax\n  int v36; // eax\n  int v37; // eax\n  int v38; // esi\n  CString *v39; // eax\n  int v40; // eax\n  CString *v41; // ecx\n  int v42; // eax\n  int v43; // eax\n  int v44; // eax\n  int v45; // eax\n  int v46; // eax\n  int v47; // eax\n  int CPointTableName; // esi\n  CString *v49; // eax\n  int v50; // eax\n  int v51; // eax\n  int v52; // eax\n  int v53; // eax\n  int v54; // eax\n  int v55; // eax\n  int v56; // eax\n  int v57; // eax\n  int v58; // eax\n  int v59; // eax\n  int v60; // eax\n  int v61; // eax\n  int v62; // eax\n  int v63; // eax\n  int v64; // eax\n  int v65; // eax\n  int v66; // eax\n  int v67; // eax\n  int v68; // eax\n  int v69; // eax\n  int v70; // eax\n  int v71; // eax\n  int v72; // eax\n  int OperationTableName; // esi\n  CString *v74; // eax\n  int v75; // eax\n  _BYTE v76[4]; // [esp+Ch] [ebp-120h] BYREF\n  _BYTE v77[4]; // [esp+10h] [ebp-11Ch] BYREF\n  _BYTE v78[4]; // [esp+14h] [ebp-118h] BYREF\n  _BYTE v79[4]; // [esp+18h] [ebp-114h] BYREF\n  _BYTE v80[4]; // [esp+1Ch] [ebp-110h] BYREF\n  _BYTE v81[4]; // [esp+20h] [ebp-10Ch] BYREF\n  _BYTE v82[4]; // [esp+24h] [ebp-108h] BYREF\n  _BYTE v83[4]; // [esp+28h] [ebp-104h] BYREF\n  _BYTE v84[4]; // [esp+2Ch] [ebp-100h] BYREF\n  _BYTE v85[4]; // [esp+30h] [ebp-FCh] BYREF\n  _BYTE v86[4]; // [esp+34h] [ebp-F8h] BYREF\n  _BYTE v87[4]; // [esp+38h] [ebp-F4h] BYREF\n  _BYTE v88[4]; // [esp+3Ch] [ebp-F0h] BYREF\n  _BYTE v89[4]; // [esp+40h] [ebp-ECh] BYREF\n  _BYTE v90[4]; 

### 0x100ddff8 ??1CAdoRecordset@@UAE@XZ
{
  "addr": "0x100ddff8",
  "code": "// attributes: thunk\nvoid __thiscall CAdoRecordset::~CAdoRecordset(CAdoRecordset *this)\n{\n  __imp_??1CAdoRecordset@@UAE@XZ(this); /*0x100ddff8*/\n}"
}

### 0x100ddff2 ?GetEOF@CAdoRecordset@@QAEHXZ
{
  "addr": "0x100ddff2",
  "code": "// attributes: thunk\nint __thiscall CAdoRecordset::GetEOF(CAdoRecordset *this)\n{\n  return __imp_?GetEOF@CAdoRecordset@@QAEHXZ(this);\n}"
}

### 0x100ddfec ?GetBOF@CAdoRecordset@@QAEHXZ
{
  "addr": "0x100ddfec",
  "code": "// attributes: thunk\nint __thiscall CAdoRecordset::GetBOF(CAdoRecordset *this)\n{\n  return __imp_?GetBOF@CAdoRecordset@@QAEHXZ(this);\n}"
}

### 0x100994a9 ?InitFieldsInfo@CMapboxTable@@AAEHPAVCDBRecordset@@@Z
{
  "addr": "0x100994a9",
  "code": "int __thiscall CMapboxTable::InitFieldsInfo(CMapboxTable *this, struct CDBRecordset *a2)\n{\n  int v3; // edi\n  int Index; // ebx\n  int v5; // eax\n  int i; // ebx\n  int FieldName; // eax\n  int v9; // eax\n  int v10; // eax\n  _BYTE v11[92]; // [esp+Ch] [ebp-ACh] BYREF\n  _BYTE v12[36]; // [esp+68h] [ebp-50h] BYREF\n  _BYTE v13[4]; // [esp+8Ch] [ebp-2Ch] BYREF\n  _BYTE v14[4]; // [esp+90h] [ebp-28h] BYREF\n  _BYTE v15[4]; // [esp+94h] [ebp-24h] BYREF\n  _BYTE v16[4]; // [esp+98h] [ebp-20h] BYREF\n  int v17; // [esp+9Ch] [ebp-1Ch]\n  int v18; // [esp+A0h] [ebp-18h]\n  int v19; // [esp+B4h] [ebp-4h]\n\n  CFieldInfos::CFieldInfos((CFieldInfos *)v12); /*0x100994c1*/\n  v3 = 0; /*0x100994c9*/\n  v19 = 0; /*0x100994d4*/\n  sub_1002783A((char *)a2 + 172); /*0x100994d7*/\n  CStringArray::CStringArray((CStringArray *)v16); /*0x100994df*/\n  LOBYTE(v19) = 1; /*0x100994ef*/\n  CStringArray::SetAtGrow((CStringArray *)v16, v18, &byte_10161364); /*0x100994f3*/\n  CStringArray::SetAtGrow((CStringArray *)v16, v18, &byte_1015C98C); /*0x10099503*/\n  CStringArray::SetAtGrow((CStringArray *)v16, v18, &byte_1015C5BC); /*0x10099513*/\n  if ( v18 <= 0 ) /*0x1009951b*/\n  {\nLABEL_5:\n    sub_1009E03D(v12); /*0x10099588*/\n    CString::operator=((char *)this + 96, &`string'); /*0x1009959e*/\n    for ( i = 0; i < *((_DWORD *)this + 28); ++i ) /*0x100995a8*/\n    {\n      if ( i ) /*0x100995ac*/\n        CString::operator+=((char *)this + 96, asc_1015C310); /*0x100995b5*/\n      FieldName = CFieldInfos::GetFieldName((char *)this + 104, v15, i); /*0x100995c2*/\n      LOBYTE(v19) = 8; /*0x100995ca*/\n      CString::operator+=((char *)this + 96, FieldName); /*0x100995ce*/\n      LOBYTE(v19) = 1; /*0x100995d6*/\n      CString::~CString((CString *)v15); /*0x100995da*/\n    }\n    LOBYTE(v19) = 0; /*0x100995e5*/\n    CStringArray::~CStringArray((CStringArray *)v16); /*0x100995ec*/\n    v19 = -1; /*0x100995f1*/\n    CFieldInfos::~CFieldInfos((CFieldInfos *)v12); /*0x100995f8*/\n    return 1; /*0x100995ff*/\n  }\n  else\n  {\n    while ( 1 ) /*0x1009952c*/\n    {\n      Index = CFieldInfos::FindIndex((CFieldInfos *)v12, (const struct CString *)(v17 + 4 *

### 0x100908a2 ?ExchangeItemValue@CSSLocalDB@@QAEHPAVCDBRecordset@@ABVCString@@ABV?$CArray@UFieldAndValue@@AAU1@@@AAV4@@Z
{
  "addr": "0x100908a2",
  "code": "int __thiscall CSSLocalDB::ExchangeItemValue(\n        struct CDaoDatabase *this,\n        int a2,\n        const char **a3,\n        int a4,\n        unsigned __int8 *a5)\n{\n  int v5; // edi\n  unsigned __int8 *v6; // ebx\n  int v8; // eax\n  int v9; // eax\n  int v10; // eax\n  int v11; // eax\n  __int16 Type; // ax\n  __int16 v13; // di\n  CString *v14; // eax\n  int v15; // eax\n  int v16; // eax\n  int v17; // edi\n  CString *v18; // eax\n  int v19; // eax\n  int v20; // eax\n  LONG *p_lVal; // ecx\n  int v22; // edi\n  CString *v23; // eax\n  int v24; // eax\n  int v25; // edi\n  int v26; // esi\n  __int16 RecordType; // ax\n  _BYTE v28[208]; // [esp+8h] [ebp-14Ch] BYREF\n  _BYTE v29[4]; // [esp+D8h] [ebp-7Ch] BYREF\n  _BYTE v30[4]; // [esp+DCh] [ebp-78h] BYREF\n  _BYTE v31[4]; // [esp+E0h] [ebp-74h] BYREF\n  _BYTE v32[4]; // [esp+E4h] [ebp-70h] BYREF\n  VARIANTARG pvarg; // [esp+E8h] [ebp-6Ch] BYREF\n  _BYTE v34[4]; // [esp+F8h] [ebp-5Ch] BYREF\n  _BYTE v35[4]; // [esp+FCh] [ebp-58h] BYREF\n  _BYTE v36[4]; // [esp+100h] [ebp-54h] BYREF\n  _BYTE v37[4]; // [esp+104h] [ebp-50h] BYREF\n  _BYTE v38[4]; // [esp+108h] [ebp-4Ch] BYREF\n  _BYTE v39[4]; // [esp+10Ch] [ebp-48h] BYREF\n  struct CDaoDatabase *v40; // [esp+110h] [ebp-44h]\n  _BYTE v41[4]; // [esp+114h] [ebp-40h] BYREF\n  _BYTE v42[4]; // [esp+118h] [ebp-3Ch] BYREF\n  _BYTE v43[4]; // [esp+11Ch] [ebp-38h] BYREF\n  void **v44; // [esp+120h] [ebp-34h] BYREF\n  int v45; // [esp+124h] [ebp-30h]\n  int v46; // [esp+128h] [ebp-2Ch]\n  int v47; // [esp+12Ch] [ebp-28h]\n  int v48; // [esp+130h] [ebp-24h]\n  CFieldInfos *v49; // [esp+134h] [ebp-20h]\n  CString *v50; // [esp+138h] [ebp-1Ch] BYREF\n  _BYTE v51[4]; // [esp+13Ch] [ebp-18h] BYREF\n  unsigned __int8 *Str1; // [esp+140h] [ebp-14h] BYREF\n  int i; // [esp+144h] [ebp-10h] BYREF\n  int v54; // [esp+150h] [ebp-4h]\n\n  v5 = 0; /*0x100908b7*/\n  v40 = this; /*0x100908bb*/\n  if ( !a2 ) /*0x100908be*/\n    return 0; /*0x100908be*/\n  v6 = a5; /*0x100908c0*/\n  if ( *((int *)a5 + 2) <= 0 ) /*0x100908c6*/\n    return 0; /*0x100908c8*/\n  v49 = (CFieldInfos *)(a2 + 172); /*0x100908de*/\n  CString::CString((CString *)&Str1,

### 0x100856dd ?SavePointList@CSSLocalDB@@AAEHW4DBRecordsetEnum@@IABV?$CArray@VCPoint3D@@AAV1@@@@Z
{
  "addr": "0x100856dd",
  "code": "int __thiscall CSSLocalDB::SavePointList(_DWORD *this, int a2, unsigned int a3, int a4)\n{\n  int v4; // eax\n  int v5; // edi\n  int v6; // eax\n  double v8[3]; // [esp+3Ch] [ebp-48h] BYREF\n  __int16 v9[2]; // [esp+54h] [ebp-30h]\n  char v10[4]; // [esp+58h] [ebp-2Ch] BYREF\n  _DWORD v11[5]; // [esp+5Ch] [ebp-28h] BYREF\n  int v12; // [esp+70h] [ebp-14h]\n  _DWORD *v13; // [esp+74h] [ebp-10h]\n  int v14; // [esp+80h] [ebp-4h]\n  int v15; // [esp+8Ch] [ebp+8h]\n\n  v4 = *(_DWORD *)(a4 + 8); /*0x100856f1*/\n  v13 = this; /*0x100856fa*/\n  v12 = v4; /*0x100856fd*/\n  memset(&v11[1], 0, 16); /*0x10085700*/\n  v11[0] = &CRecord::`vftable'; /*0x1008570c*/\n  v5 = 0; /*0x1008570f*/\n  v14 = 0; /*0x10085713*/\n  if ( v4 <= 0 ) /*0x10085716*/\n  {\nLABEL_5:\n    v14 = -1; /*0x100857cf*/\n    v11[0] = &CRecord::`vftable'; /*0x100857d6*/\n    sub_10004A76(v11); /*0x100857d9*/\n    return 1; /*0x100857e0*/\n  }\n  else\n  {\n    v15 = 4 * a2; /*0x10085722*/\n    while ( 1 ) /*0x1008572d*/\n    {\n      sub_1001E17B((CPoint3D *)v8, v5); /*0x1008572d*/\n      LOBYTE(v14) = 1; /*0x10085738*/\n      CRecord::SetData((CRecord *)v11, 0, a3); /*0x1008573d*/\n      CRecord::SetData((CRecord *)v11, 1, v5); /*0x10085748*/\n      CRecord::SetData((CRecord *)v11, 2, v8[0]); /*0x1008575a*/\n      CRecord::SetData((CRecord *)v11, 3, v8[1]); /*0x1008576c*/\n      CRecord::SetData((CRecord *)v11, 4, v8[2]); /*0x1008577e*/\n      CRecord::SetData((CRecord *)v11, 5, (const struct CString *)v10); /*0x1008578c*/\n      CRecord::SetData((CRecord *)v11, 6, v9[0]); /*0x10085799*/\n      v6 = CDBRecordset::AddRecord(*(CDBRecordset **)(v13[40] + v15), (const struct CRecord *)v11); /*0x100857b1*/\n      LOBYTE(v14) = 0; /*0x100857b8*/\n      if ( !v6 ) /*0x100857be*/\n        break; /*0x100857be*/\n      CString::~CString((CString *)v10); /*0x100857c0*/\n      if ( ++v5 >= v12 ) /*0x100857c9*/\n        goto LABEL_5; /*0x100857c9*/\n    }\n    CString::~CString((CString *)v10); /*0x100857f2*/\n    v14 = -1; /*0x100857f7*/\n    v11[0] = &CRecord::`vftable'; /*0x100857fe*/\n    sub_10004A76(v11); /*0x10085801*/\n    return 0; /*0x10085806*/\n  }\n}"
}

### 0x1007e429 ?GetCPointRecordsetEnum@@YA?AW4DBRecordsetEnum@@W4ObjecTypeEnum@@@Z
{
  "addr": "0x1007e429",
  "code": "int __cdecl GetCPointRecordsetEnum(int a1)\n{\n  int result; // eax\n\n  result = -1; /*0x1007e42d*/\n  switch ( a1 ) /*0x1007e433*/\n  {\n    case 0: /*0x1007e433*/\n      return 0; /*0x1007e44a*/\n    case 1: /*0x1007e433*/\n      return 1; /*0x1007e448*/\n    case 2: /*0x1007e433*/\n      return 2; /*0x1007e444*/\n    case 3: /*0x1007e433*/\n      return 3; /*0x1007e440*/\n  }\n  return result; /*0x1007e441*/\n}"
}

### 0x1007e404 ?GetGeoRecordsetEnum@@YA?AW4DBRecordsetEnum@@W4ObjecTypeEnum@@@Z
{
  "addr": "0x1007e404",
  "code": "int __cdecl GetGeoRecordsetEnum(int a1)\n{\n  int result; // eax\n\n  result = -1; /*0x1007e408*/\n  switch ( a1 ) /*0x1007e40e*/\n  {\n    case 0: /*0x1007e40e*/\n      return 4; /*0x1007e427*/\n    case 1: /*0x1007e40e*/\n      return 5; /*0x1007e423*/\n    case 2: /*0x1007e40e*/\n      return 6; /*0x1007e41f*/\n    case 3: /*0x1007e40e*/\n      return 7; /*0x1007e41b*/\n  }\n  return result; /*0x1007e41c*/\n}"
}

## String hits
-  where : 13
  - 0x1015cd22
  - 0x1015ce3e
  - 0x1015d053
  - 0x1015e00d
  - 0x1015e04f
  - 0x1015e071
- FeatureCode: 40
  - 0x1012d27d
  - 0x1012d4bb
  - 0x1012d593
  - 0x1012d5d0
  - 0x1012d5e5
  - 0x1012d8e7
- FeatureGUID: 14
  - 0x1012e188
  - 0x1012faed
  - 0x1012fb10
  - 0x1015aa56
  - 0x1015aa8d
  - 0x1015cb78
- Code=: 1
  - 0x101609d6