# SSMap EDB关键函数反编译

## 0x100166a4
{
  "addr": "0x100166a4",
  "code": "struct CSSLocalDB *__thiscall CScaleMap::GetTemplateDB(CScaleMap *this)\n{\n  CDataSource *v1; // ecx\n\n  v1 = (CDataSource *)*((_DWORD *)this + 51); /*0x100166a4*/\n  if ( v1 ) /*0x100166ac*/\n    return CDataSource::GetTemplateDB(v1); /*0x100166ae*/\n  else\n    return 0; /*0x100166b4*/\n}"
}

## 0x1001a07b
{
  "addr": "0x1001a07b",
  "code": "int __thiscall CScaleMap::MapClipToNewEDB(CString *this, char a2, int a3, unsigned __int8 **a4, CStringArray *a5)\n{\n  int v6; // esi\n  struct AFX_MODULE_STATE *ModuleState; // eax\n  unsigned __int8 *v8; // ecx\n  int v9; // edi\n  struct AFX_MODULE_STATE *v10; // eax\n  unsigned __int8 *v12; // [esp-8h] [ebp-1Ch] BYREF\n  int v13; // [esp-4h] [ebp-18h]\n  int v14; // [esp+10h] [ebp-4h]\n\n  v14 = 0; /*0x1001a089*/\n  v6 = 0; /*0x1001a08d*/\n  if ( !dword_10164314 ) /*0x1001a095*/\n  {\n    CreateMapClipHandle(); /*0x1001a097*/\n    v6 = 1; /*0x1001a09e*/\n  }\n  sub_10018B9E(this, (int)a4); /*0x1001a0a9*/\n  CString::operator=((char *)dword_10164314 + 160, &a2); /*0x1001a0bd*/\n  ModuleState = AfxGetModuleState(); /*0x1001a0c2*/\n  CCmdTarget::BeginWaitCursor(*((CCmdTarget **)ModuleState + 1)); /*0x1001a0ca*/\n  v13 = a3; /*0x1001a0cf*/\n  LOBYTE(v14) = 1; /*0x1001a0d5*/\n  v12 = v8; /*0x1001a0d9*/\n  a4 = &v12; /*0x1001a0dc*/\n  CString::CString((CString *)&v12, (const struct CString *)&a2); /*0x1001a0e0*/\n  v9 = sub_1001D526(v12, v13); /*0x1001a0f3*/\n  CStringArray::Copy(a5, (const struct CStringArray *)((char *)dword_10164314 + 184)); /*0x1001a100*/\n  if ( v6 ) /*0x1001a107*/\n    FreeMapClipHandle(); /*0x1001a109*/\n  LOBYTE(v14) = 0; /*0x1001a10e*/\n  v10 = AfxGetModuleState(); /*0x1001a112*/\n  CCmdTarget::EndWaitCursor(*((CCmdTarget **)v10 + 1)); /*0x1001a11a*/\n  v14 = -1; /*0x1001a11f*/\n  CString::~CString((CString *)&a2); /*0x1001a126*/\n  return v9; /*0x1001a12b*/\n}"
}

## 0x10027afe
{
  "addr": "0x10027afe",
  "code": "void __cdecl SetAutoCreateEdbFileName(char a1)\n{\n  CString::operator=(&dword_10164340, &a1); /*0x10027b15*/\n  CString::~CString((CString *)&a1); /*0x10027b21*/\n}"
}

## 0x10027b32
{
  "addr": "0x10027b32",
  "code": "CString *__cdecl GetAutoCreateEdbFileName(CString *a1)\n{\n  CString::CString(a1, (const struct CString *)&dword_10164340); /*0x10027b42*/\n  return a1; /*0x10027b4a*/\n}"
}

## 0x1002bda3
{
  "addr": "0x1002bda3",
  "code": "int __thiscall CDataSource::CheckTemplateDBBaseTable(CDataSource *this, struct CSSLocalDB *a2)\n{\n  BOOL v3; // esi\n  BOOL v4; // edi\n  BOOL v5; // ebx\n  CString *v6; // esi\n  int v7; // eax\n  _BYTE v9[4]; // [esp+8h] [ebp-3Ch] BYREF\n  int v10; // [esp+Ch] [ebp-38h]\n  int v11; // [esp+10h] [ebp-34h]\n  CString *v12; // [esp+1Ch] [ebp-28h]\n  CString *v13; // [esp+20h] [ebp-24h]\n  CString *v14; // [esp+24h] [ebp-20h]\n  _BYTE v15[4]; // [esp+28h] [ebp-1Ch] BYREF\n  _BYTE v16[4]; // [esp+2Ch] [ebp-18h] BYREF\n  int v17; // [esp+30h] [ebp-14h]\n  char *v18; // [esp+34h] [ebp-10h] BYREF\n  int v19; // [esp+40h] [ebp-4h]\n\n  if ( a2 ) /*0x1002bdb9*/\n  {\n    CStringArray::CStringArray((CStringArray *)v9); /*0x1002bdc2*/\n    v19 = 0; /*0x1002bdce*/\n    CSSDatabase::GetTablesInDB(a2, (struct CStringArray *)v9); /*0x1002bdd1*/\n    CString::CString((CString *)&v18, aSymbolscripttb_0); /*0x1002bdde*/\n    LOBYTE(v19) = 1; /*0x1002bdeb*/\n    CString::CString((CString *)v15, aNotetemplatetb); /*0x1002bdef*/\n    LOBYTE(v19) = 2; /*0x1002bdfc*/\n    CString::CString((CString *)v16, aFeaturecodetbI); /*0x1002be00*/\n    LOBYTE(v19) = 3; /*0x1002be08*/\n    v17 = 0; /*0x1002be0c*/\n    if ( v11 > 0 ) /*0x1002be0f*/\n    {\n      v14 = (CDataSource *)((char *)this + 48); /*0x1002be19*/\n      v13 = (CDataSource *)((char *)this + 52); /*0x1002be22*/\n      v12 = (CDataSource *)((char *)this + 44); /*0x1002be25*/\n      do /*0x1002bf25*/\n      {\n        CString::CString((CString *)&a2, (const struct CString *)(v10 + 4 * v17)); /*0x1002be35*/\n        LOBYTE(v19) = 4; /*0x1002be42*/\n        v3 = CString::Find((CString *)&a2, aSymbolscripttb_1) == 0; /*0x1002be59*/\n        v4 = CString::Find((CString *)&a2, aNotetemplatetb_0) == 0; /*0x1002be6d*/\n        v5 = CString::Find((CString *)&a2, aFeaturecodetb) == 0; /*0x1002be7e*/\n        if ( !*(_DWORD *)(*(_DWORD *)v14 - 8) && v3 ) /*0x1002be87*/\n          CString::operator=(v14, &

## 0x1003284e
{
  "addr": "0x1003284e",
  "code": "struct CSSLocalDB *__thiscall CDataSource::GetTemplateDB(CDataSource *this)\n{\n  unsigned __int8 *v2[2]; // [esp+0h] [ebp-8h] BYREF\n\n  v2[1] = (unsigned __int8 *)v2; /*0x10032855*/\n  CString::CString((CString *)v2, (CDataSource *)((char *)this + 16)); /*0x1003285a*/\n  return (struct CSSLocalDB *)sub_10027BA4(v2[0]); /*0x10032865*/\n}"
}

## 0x100b5bc8
{
  "addr": "0x100b5bc8",
  "code": "int __cdecl LoadAttrTableInfoInTemplateDB(CDataSource *a1, CPtrArray *a2)\n{\n  int i; // esi\n  CRecord *v3; // eax\n  CFieldInfos *v4; // edi\n  const struct CString *v5; // eax\n  int v6; // ecx\n  int v7; // esi\n  _BYTE v9[12]; // [esp-14h] [ebp-120h] BYREF\n  int v10; // [esp-8h] [ebp-114h]\n  _DWORD v11[4]; // [esp-4h] [ebp-110h] BYREF\n  _BYTE v12[172]; // [esp+Ch] [ebp-100h] BYREF\n  _BYTE v13[36]; // [esp+B8h] [ebp-54h] BYREF\n  _DWORD *v14; // [esp+DCh] [ebp-30h]\n  _BYTE v15[4]; // [esp+E0h] [ebp-2Ch] BYREF\n  int v16; // [esp+E4h] [ebp-28h]\n  int v17; // [esp+E8h] [ebp-24h]\n  CRecord *v18; // [esp+F4h] [ebp-18h]\n  struct CDaoDatabase *TemplateDB; // [esp+F8h] [ebp-14h]\n  _BYTE v20[4]; // [esp+FCh] [ebp-10h] BYREF\n  int v21; // [esp+108h] [ebp-4h]\n\n  TemplateDB = CDataSource::GetTemplateDB(a1); /*0x100b5be6*/\n  CStringArray::CStringArray((CStringArray *)v15); /*0x100b5be9*/\n  v21 = 0; /*0x100b5bfa*/\n  CDataSource::GetCodeAttrTables(a1, 0xFFFFFFFF, (struct CStringArray *)v15, 0); /*0x100b5bfd*/\n  OrderArray((struct CStringArray *)v15, 1); /*0x100b5c08*/\n  for ( i = 0; i < v17; ++i ) /*0x100b5c14*/\n  {\n    CString::CString((CString *)&a1, (const struct CString *)(v16 + 4 * i)); /*0x100b5c24*/\n    LOBYTE(v21) = 1; /*0x100b5c2f*/\n    if ( CSSDatabase::IsExistentTable(TemplateDB, (const struct CString *)(v16 + 4 * i)) ) /*0x100b5c37*/\n    {\n      operator+(v20, aSelectFrom_0, &a1); /*0x100b5c60*/\n      LOBYTE(v21) = 2; /*0x100b5c6e*/\n      CDBRecordset::CDBRecordset((CDBRecordset *)v12, TemplateDB); /*0x100b5c72*/\n      LOBYTE(v21) = 3; /*0x100b5c85*/\n      if ( CDBRecordset::OpenRecordset(v12, v20, 0, 2, 0) ) /*0x100b5c89*/\n      {\n        v3 = (CRecord *)operator new(0x24u); /*0x100b5c94*/\n        v18 = v3; /*0x100b5c9a*/\n        LOBYTE(v21) = 4; /*0x100b5c9f*/\n        if ( v3 ) /*0x100b5ca3*/\n          v4 = CFieldInfos::CFieldInfos(v3); /*0x100b5cac*/\n        else\n          v4 = 0; /*0x100b

## 0x100cd820
{
  "addr": "0x100cd820",
  "code": "int __cdecl CreateGCSCOREDB(struct CSSDatabase *a1)\n{\n  int IsExistentTable; // eax\n  int v3; // esi\n  int v4; // esi\n  int Table; // eax\n  bool v6; // bl\n  _BYTE v7[208]; // [esp+Ch] [ebp-168h] BYREF\n  _BYTE v8[36]; // [esp+DCh] [ebp-98h] BYREF\n  _BYTE v9[4]; // [esp+100h] [ebp-74h] BYREF\n  __int16 v10; // [esp+104h] [ebp-70h]\n  int v11; // [esp+108h] [ebp-6Ch]\n  int v12; // [esp+10Ch] [ebp-68h]\n  __int16 v13; // [esp+110h] [ebp-64h]\n  int v14; // [esp+114h] [ebp-60h]\n  int v15; // [esp+118h] [ebp-5Ch]\n  _BYTE v16[4]; // [esp+15Ch] [ebp-18h] BYREF\n  BOOL v17; // [esp+160h] [ebp-14h] BYREF\n  _BYTE v18[4]; // [esp+164h] [ebp-10h] BYREF\n  int v19; // [esp+170h] [ebp-4h]\n\n  if ( !a1 ) /*0x100cd837*/\n    return 1; /*0x100cd83c*/\n  CString::CString((CString *)v18, &byte_10163748); /*0x100cd84a*/\n  v19 = 0; /*0x100cd852*/\n  IsExistentTable = CSSDatabase::IsExistentTable(a1, (const struct CString *)v18); /*0x100cd85a*/\n  v19 = -1; /*0x100cd85f*/\n  v3 = IsExistentTable; /*0x100cd866*/\n  CString::~CString((CString *)v18); /*0x100cd868*/\n  if ( v3 ) /*0x100cd872*/\n  {\n    CString::CString((CString *)v18); /*0x100cd87b*/\n    v4 = 1; /*0x100cd885*/\n    v19 = 1; /*0x100cd88d*/\n    CString::Format((CString *)v18, \"select * From %s\", &byte_10163748); /*0x100cd890*/\n    CDBRecordset::CDBRecordset((CDBRecordset *)v7, a1); /*0x100cd8a1*/\n    LOBYTE(v19) = 2; /*0x100cd8b5*/\n    CDBRecordset::OpenRecordset(v7, v18, 0, 2, 0); /*0x100cd8b8*/\n    v17 = CDaoRecordset::GetFieldCount((CDaoRecordset *)v7) != 5; /*0x100cd8d2*/\n    CDBRecordset::CloseRecordset((CDBRecordset *)v7); /*0x100cd8db*/\n    if ( !v17 ) /*0x100cd8e4*/\n    {\n      LOBYTE(v19) = 1; /*0x100cd8ec*/\n      CDBRecordset::~CDBRecordset((CDBRecordset *)v7); /*0x100cd8f0*/\n      v19 = -1; /*0x100cd8f5*/\n      CString::~CString((CString *)v18); /*0x100cd8fc*/\n      return 0; /*0x100cd903*/\n    }\n    CString::CString((CString *)&v17, &byte_101637

## func_query: FeatureGUID (5)
- 0x10027561 ?UpdateFeatureGUID@CScaleMap@@QAEXW4ObjecTypeEnum@@H@Z
- 0x10064d56 ?UpdateFeatureGUID@CUserLayer@@QAEXW4ObjecTypeEnum@@H@Z
- 0x100df0b4 ?SetFeatureGUID@CGeoBase@@QAEXABVCString@@@Z
- 0x100df42c ?CreateFeatureGUID@CGeoBase@@QAEXXZ
- 0x100df432 ?GetFeatureGUID@CGeoBase@@QBE?AVCString@@XZ

## func_query: GetField (19)
- 0x10026b01 ?GetFieldInfos@CScaleMap@@QAEPBVCFieldInfos@@VCString@@@Z
- 0x10026b59 ?GetFieldNames@CScaleMap@@QAEHIAAVCStringArray@@@Z
- 0x10026f66 ?GetFieldInfoEx@CScaleMap@@QAEHABVCString@@0AAVCDBFieldInfo@@H@Z
- 0x1002ef61 ?GetFieldNames@CDataSource@@QAEHHAAVCStringArray@@@Z
- 0x1002f6d6 ?GetFieldInfos@CDataSource@@QAEPBVCFieldInfos@@VCString@@@Z
- 0x1002f787 ?GetFieldInfoEx@CDataSource@@QAEHABVCString@@0AAVCDBFieldInfo@@H@Z
- 0x10044c01 ?GetFieldValueRange@CDataSource@@QAEXVCString@@0AAN1@Z
- 0x10047c31 ?GetFieldBandInfo@@YAHAAV?$CSSPtrArray@VCFieldBandItem@@@@@Z
- 0x1004b76c ?GetFieldCodeMap@CSSAttrDicItem@@QAEHAAVCStringArray@@0VCString@@1PAVCDataSource@@PAVCGeoBase@@@Z
- 0x100de064 ?GetFieldValue@CAdoRecordset@@QAEHABJAAVCOleVariant@@@Z
- 0x100de06a ?GetFieldName@CAdoRecordset@@QAE?AVCString@@ABJ@Z
- 0x100de070 ?GetFieldCount@CAdoRecordset@@QAEJXZ
- 0x100de160 ?GetFieldName@CFieldInfos@@QBE?AVCString@@H@Z
- 0x100de178 ?GetFieldInfo@CSSDatabase@@QAEHPAVCDaoTableDef@@PAUCDaoFieldInfo@@HH@Z
- 0x100dfa26 ?GetFieldCount@CDaoTableDef@@QAEFXZ
- 0x100dfa44 ?GetFieldInfo@CDaoTableDef@@QAEXPBDAAUCDaoFieldInfo@@K@Z
- 0x100dfa8c ?GetFieldValue@CDaoRecordset@@UAEXHAAVCOleVariant@@@Z
- 0x100dfdaa ?GetFieldCount@CDaoRecordset@@QAEFXZ
- 0x100dffa8 ?GetFieldValue@CDaoRecordset@@UAEXPBDAAVCOleVariant@@@Z

## func_query: GetRecord (9)
- 0x100036fa ?GetRecordsetHandle@CSSLocalDB@@QAEPAVCDBRecordset@@W4DBRecordsetEnum@@@Z
- 0x100063e6 ?GetRecordSet@CAdoRecordset@@QAE?AV?$_com_ptr_t@V?$_com_IIID@U_Recordset@ADOCG@@$1?_GUID_00000556_0000_0010_8000_00aa006d2ea4@@3U__s_GUID@@A@@@@XZ
- 0x100b6c66 ?GetRecordSQL@CSSMultiMediaAttr@@IAEXAAVCString@@@Z
- 0x100c6e10 ?GetRecord@CCheckRecordList@@QAEPAVCCheckRecord@@H@Z
- 0x100ddebd ?GetRecord@CCheckRecord_NList@@QAEPAVCCheckRecord_N@@H@Z
- 0x100de016 ?GetRecord@CAdoRecordset@@QAEHAAVCAdoRecord@@H@Z
- 0x100de1d8 ?GetRecord@CDBRecordset@@QAEHAAVCRecord@@H@Z
- 0x100de1f0 ?GetRecordFromBuffer@CFieldInfos@@QAEHIAAVCStringArray@@0@Z
- 0x100de304 ?GetRecordType@CRecord@@QBEFH@Z

## func_query: AttrTable (34)
- 0x100147ff ?GetAttrTableCharacter@CScaleMap@@QAE?AVCString@@XZ
- 0x10026b77 ?GetAttrTableRS@CScaleMap@@QAEPAVCDBRecordset@@VCString@@@Z
- 0x10026bcf ?GetCodeAttrTables@CScaleMap@@QAEXIAAVCStringArray@@H@Z
- 0x10026bed ?GetSeqAttrTables@CScaleMap@@QAEHVCString@@AAVCStringArray@@11@Z
- 0x10026c4d ?GetLayerAttrTables@CScaleMap@@QAEXVCString@@AAVCStringArray@@W4ObjecTypeEnum@@H@Z
- 0x10026e4f ?GetCodeAttrTable@CScaleMap@@QAE?AVCString@@IH@Z
- 0x10026ee2 ?SetCodeAttrTable@CScaleMap@@QAEHIVCString@@H@Z
- 0x1002f00f ?GetAttrTableRS@CDataSource@@QAEPAVCDBRecordset@@VCString@@@Z
- 0x1002f070 ?GetCodeAttrTables@CDataSource@@QAEXHAAVCStringArray@@H@Z
- 0x1002f0a4 ?GetSeqAttrTables@CDataSource@@QAEHVCString@@AAVCStringArray@@11@Z
- 0x1002f1f7 ?GetCodeAttrTable@CDataSource@@QAE?AVCString@@HH@Z
- 0x1002f3b1 ?GetLayerAttrTables@CDataSource@@QAEXVCString@@AAVCStringArray@@W4ObjecTypeEnum@@H@Z
- 0x1002f60d ?SetCodeAttrTable@CDataSource@@QAEHHVCString@@H@Z
- 0x1003d43e ?GetAttrTableFormFile@CDataSource@@QAE?AVCString@@V2@@Z
- 0x1003eb50 ?GetAttrTableName@CUserLayer@@QBE?AVCString@@W4ObjecTypeEnum@@@Z
- 0x1003ec9c ?SetAttrTableName@CUserLayer@@QAEXABVCString@@W4ObjecTypeEnum@@@Z
- 0x1003ecae ?GetAttrTableRS@CUserLayer@@QBEPAVCDBRecordset@@W4ObjecTypeEnum@@@Z
- 0x100445b0 ?GetObjAttrTable@CDataSource@@QAE?AVCString@@PAVCGeoBase@@H@Z
- 0x1004c98e ?GetAttrTableFormFile@@YA?AVCString@@PAVCDataSource@@V1@@Z
- 0x1004d09a ?GetAttrTableForm@@YAPAVCSSReport@@PAVCDataSource@@VCString@@@Z

## func_query: TemplateDB (5)
- 0x100166a4 ?GetTemplateDB@CScaleMap@@QBEPAVCSSLocalDB@@XZ
- 0x1002bda3 ?CheckTemplateDBBaseTable@CDataSource@@AAEHPAVCSSLocalDB@@@Z
- 0x1003284e ?GetTemplateDB@CDataSource@@QBEPAVCSSLocalDB@@XZ
- 0x100b5bc8 ?LoadAttrTableInfoInTemplateDB@@YAHPAVCDataSource@@AAV?$CSSPtrArray@VCFieldInfos@@@@@Z
- 0x100df5ac ?LoadTemplateDB@CSSGisDB@@QAEHVCString@@AAVCByteArray@@@Z

## func_query: EdbFileName (2)
- 0x10027afe ?SetAutoCreateEdbFileName@@YAXVCString@@@Z
- 0x10027b32 ?GetAutoCreateEdbFileName@@YA?AVCString@@XZ