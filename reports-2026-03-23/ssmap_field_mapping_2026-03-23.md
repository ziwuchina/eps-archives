# SSMap 字段映射/属性读取关键函数

## 0x1004b76c
{
  "addr": "0x1004b76c",
  "code": "int __thiscall CSSAttrDicItem::GetFieldCodeMap(\n        _DWORD *this,\n        CStringArray *a2,\n        CStringArray *a3,\n        char a4,\n        char a5,\n        int a6,\n        CString *a7)\n{\n  _DWORD *v8; // ecx\n  int v9; // eax\n  bool v10; // cc\n  int v11; // esi\n  int v12; // eax\n  bool v13; // zf\n  const char *v14; // eax\n  int v15; // ecx\n  const struct CString *v16; // eax\n  CStringArray *v17; // ecx\n  int v18; // ecx\n  int v19; // edi\n  int v20; // eax\n  unsigned __int8 *v21; // ecx\n  int v22; // eax\n  const char *UserLayer; // eax\n  double v24; // st7\n  BOOL v25; // ecx\n  _DWORD *v26; // ecx\n  int v27; // ecx\n  unsigned __int8 *v28; // ecx\n  _DWORD *v29; // ecx\n  int v30; // ecx\n  unsigned __int8 *v31; // ecx\n  int v32; // esi\n  unsigned __int8 *v34; // [esp-Ch] [ebp-90h] BYREF\n  int v35; // [esp-8h] [ebp-8Ch] BYREF\n  struct CStringArray *v36; // [esp-4h] [ebp-88h]\n  CStringArray *v37; // [esp+0h] [ebp-84h] BYREF\n  unsigned __int8 *p_Str2; // [esp+4h] [ebp-80h] BYREF\n  _DWORD *v39; // [esp+8h] [ebp-7Ch] BYREF\n  _DWORD v40[4]; // [esp+Ch] [ebp-78h] BYREF\n  _BYTE v41[4]; // [esp+1Ch] [ebp-68h] BYREF\n  int v42; // [esp+20h] [ebp-64h]\n  _BYTE v43[4]; // [esp+30h] [ebp-54h] BYREF\n  int v44; // [esp+34h] [ebp-50h]\n  int v45; // [esp+38h] [ebp-4Ch]\n  _BYTE v46[8]; // [esp+44h] [ebp-40h] BYREF\n  int v47; // [esp+4Ch] [ebp-38h]\n  CString *p_p_Str2; // [esp+58h] [ebp-2Ch]\n  CString *v49; // [esp+5Ch] [ebp-28h]\n  _DWORD *v50; // [esp+60h] [ebp-24h]\n  _DWORD *v51; // [esp+64h] [ebp-20h] BYREF\n  int v52; // [esp+68h] [ebp-1Ch]\n  int i; // [esp+6Ch] [ebp-18h]\n  unsigned __int8 *Str2; // [esp+70h] [ebp-14h] BYREF\n  _BYTE v55[4]; // [esp+74h] [ebp-10h] BYREF\n  int v56; // [esp+80h] [ebp-4h]\n\n  v56 = 1; /*0x1004b785*/\n  CStringArray::Copy(a2, (const struct CStringArray *)(this + 3)); /*0x1004b78c*/\n  CStringArray::Copy(a3, (const struct CStringArray *)(this + 8)); /*0x1004b798*/\n  if ( !a7 || !this[15] ) /*0x1004b7a8*/\n    goto LABEL_38; /*0x1004b7ab*/\n  CStringArray::CStringArray((CStringArray *)v43); /*0x1004b7b4*/\n  LOBYTE(v56) = 2; /*0x1004b7bc*/\n  CStringArray::CStringArray((CStringArray *)v41); /*0x1004b7c0*/\n  v40[0] = 0; /*0x1004b7c5*/\n  v39 = v8; /*0x1004b7c6*/\n  v50 = &v39; /*0x1004b7c9*/\n  LOBYTE(v56) = 3; /*0x1004b7d1*/\n  CString::CString((CString *)&v39, &`string'); /*0x1004b7d5*/\n  CDataSource::GetExtentAttr(a6, a7, v43, v41, v39, v40[0]); /*0x1004b7e8*/\n  v9 = 0; /*0x1004b7ed*/\n  v10 = this[15] <= 0; /*0x1004b7ef*/\n  v52 = 0; /*0x1004b7f2*/\n  if ( v10 ) /*0x1004b7f5*/\n    goto LABEL_37; /*0x1004b7f5*/\n  while ( 1 ) /*0x1004b7fb*/\n  {\n    if ( v9 < 0 || v9 >= this[15] ) /*0x1004b802*/\n      v11 = 0; /*0x1004b80c*/\n    else\n      v11 = *(_DWORD *)(this[14] + 4 * v9); /*0x1004b807*/\n    CStringArray::CStringArray((CStringArray *)v46); /*0x1004b811*/\n    LOBYTE(v56) = 4; /*0x1004b820*/\n    v12 = CString::Find((CString *)(

## 0x10026f66
{
  "addr": "0x10026f66",
  "code": "int __thiscall CScaleMap::GetFieldInfoEx(\n        CScaleMap *this,\n        const struct CString *a2,\n        const struct CString *a3,\n        struct CDBFieldInfo *a4,\n        int a5)\n{\n  CDataSource *v5; // ecx\n\n  v5 = (CDataSource *)*((_DWORD *)this + 51); /*0x10026f66*/\n  if ( v5 ) /*0x10026f6e*/\n    return CDataSource::GetFieldInfoEx(v5, a2, a3, a4, a5); /*0x10026f80*/\n  else\n    return 0; /*0x10026f87*/\n}"
}

## 0x100de1d8
{
  "addr": "0x100de1d8",
  "code": "// attributes: thunk\nint __thiscall CDBRecordset::GetRecord(CDBRecordset *this, struct CRecord *a2, int a3)\n{\n  return __imp_?GetRecord@CDBRecordset@@QAEHAAVCRecord@@H@Z(this, a2, a3);\n}"
}

## 0x1002f00f
{
  "addr": "0x1002f00f",
  "code": "int __fastcall CDataSource::GetAttrTableRS(unsigned __int8 *a1, int a2, char a3)\n{\n  unsigned __int8 *v3; // esi\n  int v4; // eax\n  int v5; // eax\n  int v6; // esi\n  unsigned __int8 *v8[3]; // [esp-4h] [ebp-18h] BYREF\n  int v9; // [esp+10h] [ebp-4h]\n\n  v3 = a1; /*0x1002f01b*/\n  v9 = 0; /*0x1002f01d*/\n  if ( !*((_DWORD *)a1 + 134) ) /*0x1002f021*/\n  {\n    v4 = sub_1002DD1C((CDataSource *)a1); /*0x1002f02b*/\n    a1 = v8[0]; /*0x1002f030*/\n    *((_DWORD *)v3 + 134) = v4; /*0x1002f031*/\n  }\n  v8[0] = a1; /*0x1002f037*/\n  v8[2] = (unsigned __int8 *)v8; /*0x1002f03d*/\n  CString::CString((CString *)v8, (const struct CString *)&a3); /*0x1002f041*/\n  v5 = sub_100BA600(v8[0]); /*0x1002f04c*/\n  v9 = -1; /*0x1002f051*/\n  v6 = v5; /*0x1002f058*/\n  CString::~CString((CString *)&a3); /*0x1002f05a*/\n  return v6; /*0x1002f05f*/\n}"
}

## 0x10026bcf
{
  "addr": "0x10026bcf",
  "code": "void __thiscall CScaleMap::GetCodeAttrTables(CScaleMap *this, unsigned int a2, struct CStringArray *a3, int a4)\n{\n  CDataSource *v4; // ecx\n\n  v4 = (CDataSource *)*((_DWORD *)this + 51); /*0x10026bcf*/\n  if ( v4 ) /*0x10026bd7*/\n    CDataSource::GetCodeAttrTables(v4, a2, a3, a4); /*0x10026be5*/\n}"
}

## 0x100445b0
{
  "addr": "0x100445b0",
  "code": "CString *__thiscall CDataSource::GetObjAttrTable(void *this, CString *a2, CGeoBase *a3, int a4)\n{\n  CGeoBase *v5; // esi\n  int v6; // ecx\n  int Code; // eax\n  int CodeAttrTable; // eax\n  int v9; // edi\n  int v10; // eax\n  int v11; // eax\n  int UserLayer; // eax\n  int AttrTableName; // eax\n  _DWORD v15[4]; // [esp-4h] [ebp-24h] BYREF\n  int v16; // [esp+Ch] [ebp-14h]\n  unsigned __int8 *Str1; // [esp+10h] [ebp-10h] BYREF\n  int v18; // [esp+1Ch] [ebp-4h]\n\n  v16 = 0; /*0x100445bc*/\n  CString::CString((CString *)&Str1, &`string'); /*0x100445ce*/\n  v5 = a3; /*0x100445d3*/\n  v18 = 1; /*0x100445d6*/\n  if ( (*(int (__thiscall **)(CGeoBase *))(*(_DWORD *)a3 + 4))(a3) == 3 ) /*0x100445e7*/\n  {\n    v15[0] = v6; /*0x10044673*/\n    a3 = (CGeoBase *)v15; /*0x10044678*/\n    CGeoBase::GetLayerName(v5, v15); /*0x1004467c*/\n    UserLayer = CDataSource::GetUserLayer(this, v15[0]); /*0x10044683*/\n    if ( UserLayer ) /*0x1004468a*/\n    {\n      AttrTableName = CUserLayer::GetAttrTableName(UserLayer, &a3, 3); /*0x10044694*/\n      LOBYTE(v18) = 4; /*0x1004469d*/\n      CString::operator=(&Str1, AttrTableName); /*0x100446a1*/\n      LOBYTE(v18) = 1; /*0x100446a6*/\n      goto LABEL_7; /*0x100446a6*/\n    }\n  }\n  else\n  {\n    Code = CGeoBase::GetCode(v5); /*0x100445ef*/\n    CodeAttrTable = CDataSource::GetCodeAttrTable(this, &a3, Code, 0); /*0x100445fd*/\n    LOBYTE(v18) = 2; /*0x10044606*/\n    CString::operator=(&Str1, CodeAttrTable); /*0x1004460a*/\n    LOBYTE(v18) = 1; /*0x10044612*/\n    CString::~CString((CString *)&a3); /*0x10044616*/\n    if ( !mbscmp(Str1, (const unsigned __int8 *)&`string') ) /*0x1004461f*/\n    {\n      a3 = (CGeoBase *)v15; /*0x10044634*/\n      CGeoBase::GetLayerName(v5, v15); /*0x10044638*/\n      v9 = CDataSource::GetUserLayer(this, v15[0]); /*0x10044644*/\n      if ( v9 ) /*0x10044648*/\n      {\n        v10 = (*(int (__thiscall **)(CGeoBase *))(*(_DWORD *)v5 + 4))(v5); /*0x1004464e*/\n        v11 = CUserLayer::GetAttrTableName(v9, &a3, v10); /*0x10044658*/\n        LOBYTE(v18) = 3; /*0x10044661*/\n        CString::operator=(&Str1, v11); /*0x10044665*/\n        LOBYTE(v18) = 1; /*0x1004466a*/\nLABEL_7:\n        CString::~CString((CString *)&a3); /*0x100446ad*/\n      }\n    }\n  }\n  CString::CString(a2, (const struct CString *)&Str1); /*0x100446b2*/\n  v16 = 1; /*0x100446be*/\n  LOBYTE(v18) = 0; /*0x100446c5*/\n  CString::~CString((CString *)&Str1); /*0x100446cc*/\n  return a2; /*0x100446d1*/\n}"
}

## 0x100de064
{
  "addr": "0x100de064",
  "code": "// attributes: thunk\nint __thiscall CAdoRecordset::GetFieldValue(CAdoRecordset *this, const int *a2, struct COleVariant *a3)\n{\n  return __imp_?GetFieldValue@CAdoRecordset@@QAEHABJAAVCOleVariant@@@Z(this, a2, a3);\n}"
}

## 0x100dffa8
{
  "addr": "0x100dffa8",
  "code": "// attributes: thunk\nvoid __thiscall CDaoRecordset::GetFieldValue(CDaoRecordset *this, const char *a2, struct COleVariant *a3)\n{\n  __imp_?GetFieldValue@CDaoRecordset@@UAEXPBDAAVCOleVariant@@@Z(this, a2, a3); /*0x100dffa8*/\n}"
}