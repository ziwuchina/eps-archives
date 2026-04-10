# SSProject SDL flow deep dive (pass4)

## SDLFunctionExecute 0x1005FFAD
- sig: `int __cdecl ?SDLFunctionExecute@@YAPAXVCString@@I@Z(int, int *)`
- callers: 0, callees: 19
```cpp
int __cdecl SDLFunctionExecute(int a1, int *a2)
{
  int v2; // esi
  int v3; // eax
  int v4; // eax
  int v5; // eax
  int v6; // esi
  const char *v7; // eax
  int v8; // esi
  int v9; // ecx
  int v10; // eax
  int v11; // esi
  int v12; // ecx
  const char *v13; // eax
  int v15; // [esp-Ch] [ebp-48h] BYREF
  _BYTE *v16; // [esp-8h] [ebp-44h]
  _DWORD v17[4]; // [esp-4h] [ebp-40h] BYREF
  _BYTE v18[4]; // [esp+Ch] [ebp-30h] BYREF
  struct CString *v19; // [esp+10h] [ebp-2Ch]
  int v20; // [esp+14h] [ebp-28h]
  _DWORD *v21; // [esp+20h] [ebp-1Ch] BYREF
  _BYTE v22[4]; // [esp+24h] [ebp-18h] BYREF
  _BYTE v23[4]; // [esp+28h] [ebp-14h] BYREF
  _BYTE v24[4]; // [esp+2Ch] [ebp-10h] BYREF
  int v25; // [esp+38h] [ebp-4h]

  v25 = 0;
  CString::CString((CString *)v22);
  LOBYTE(v25) = 1;
  v2 = CString::Find((CString *)&a1, 40);
  v3 = CString::ReverseFind((CString *)&a1, 41);
  if ( v2 > 0 && v2 < v3 && v3 == *(_DWORD *)(a1 - 8) - 1 )
  {
    v4 = CString::Mid(&a1, &v21, v2 + 1, v3 - v2 - 1);
    LOBYTE(v25) = 2;
    CString::operator=(v22, v4);
    LOBYTE(v25) = 1;
    CString::~CString((CString *)&v21);
    v5 = CString::Left(&a1, &v21, v2);
    LOBYTE(v25) = 3;
    CString::operator=(&a1, v5);
    LOBYTE(v25) = 1;
    CString::~CString((CString *)&v21);
  }
  CString::Replace((CString *)&a1, asc_100BDD64, &Default);
  CString::Replace((CString *)&a1, asc_100C37A0, asc_100BD9E4);
  CStringArray::CStringArray((CStringArray *)v18);
  LOBYTE(v25) = 4;
  ScanString((const struct CString *)&a1, asc_100BD9E4, (struct CStringArray *)v18, 0);
  if ( !mbscmp(*(const unsigned __int8 **)v19, (const unsigned __int8 *)aSdl) )
    CStringArray::RemoveAt((CStringArray *)v18, 0, 1);
  v6 = 2;
  if ( v20 >= 2 )
  {
    CString::CString((CString *)v23, v19);
    LOBYTE(v25) = 6;
    CString::CString((CString *)v24, (struct CString *)((char *)v19 + 4));
    LOBYTE(v25) = 7;
    if ( v20 > 2 )
    {
      do
      {
        v10 = operator+(&v21, asc_100C37A0, (char *)v19 + 4 * v6);
        LOBYTE(v25) = 8;
        CString::operator+=(v24, v10);
        LOBYTE(v25) = 7;
        CString::~CString((CString *)&v21);
        ++v6;
      }
      while ( v6 < v20 );
    }
    v17[0] = v9;
    v21 = v17;
    CString::CString((CString *)v17, (const struct CString *)v23);
    v11 = sub_1005FCC4(v17[0]);
    v12 = v17[0];
    if ( v11 )
    {
      v17[0] = a2;
      v16 = v22;
      v15 = v12;
      a2 = &v15;
      CString::CString((CString *)&v15, (const struct CString *)v24);
      v8 = (*(int (__thiscall **)(int, int, _BYTE *, _DWORD))(*(_DWORD *)v11 + 64))(v11, v15, v16, v17[0]);
    }
    else
    {
      v13 = *(const char **)operator+(&a2, &unk_100C59EC, v23);
      LOBYTE(v25) = 9;
      AfxMessageBox(v13, 0, 0);
```
### Direct callees
- `0x1005FCC4` `sub_1005FCC4` calls=1
- `0x10075482` `?ScanString@@YAXABVCString@@PBDAAVCStringArray@@H@Z` calls=1
- `0x1007669A` `??0CString@@QAE@XZ` calls=1
- `0x100766A0` `??0CString@@QAE@ABV0@@Z` calls=4
- `0x100766A6` `??1CString@@QAE@XZ` calls=9
- `0x100766B2` `??4CString@@QAEABV0@ABV0@@Z` calls=2
- `0x100766CA` `??1CStringArray@@UAE@XZ` calls=1
- `0x100766D6` `??0CStringArray@@QAE@XZ` calls=1
- `0x1007682C` `?AfxMessageBox@@YGHPBDII@Z` calls=2
- `0x1007696A` `?RemoveAt@CStringArray@@QAEXHH@Z` calls=1
- `0x100769A0` `??YCString@@QAEABV0@ABV0@@Z` calls=1
- `0x10076A48` `?Left@CString@@QBE?AV1@H@Z` calls=1
- `0x10076A5A` `?Replace@CString@@QAEHPBD0@Z` calls=2
- `0x10076A6C` `??H@YG?AVCString@@PBDABV0@@Z` calls=3
- `0x10076AAE` `?Mid@CString@@QBE?AV1@HH@Z` calls=1
- `0x10076BA4` `?ReverseFind@CString@@QBEHD@Z` calls=1
- `0x10076E6E` `?Find@CString@@QBEHD@Z` calls=1
- `0x100777E8` `_EH_prolog` calls=1
- `0x10084F08` `_mbscmp` calls=1

## CSSView::ExecuteSDLCommand 0x1004E51A
- sig: `int __thiscall ?ExecuteSDLCommand@CSSView@@QAEHVCString@@@Z(int this, char *String)`
- callers: 3, callees: 37
```cpp
int __thiscall CSSView::ExecuteSDLCommand(int this, char *String)
{
  char *v3; // ecx
  WPARAM v4; // ebx
  int v5; // eax
  int v6; // eax
  int v8; // ecx
  char *v9; // ecx
  int v10; // ecx
  int v11; // ecx
  int v12; // ecx
  int v13; // esi
  int v14; // eax
  WPARAM v15; // eax
  void *v16; // ecx
  char *v17; // ecx
  void *v18; // ecx
  int v19; // eax
  int v20; // eax
  void *v21; // ecx
  int v22; // eax
  struct CFeatureList *FeatureList; // eax
  struct CFeatureList *v24; // edi
  int v25; // eax
  int v26; // eax
  _DWORD *v27; // eax
  int v28; // eax
  void *v29; // ecx
  struct MarkNoteTempls *NoteTemplate; // edi
  int v31; // ebx
  int v32; // eax
  int v33; // eax
  const char **v34; // ebx
  int v35; // eax
  char *v36; // ecx
  void *v37; // ecx
  int v38; // eax
  char *v39; // ecx
  void *v40; // ecx
  int v41; // ebx
  int v42; // eax
  char *v43; // ecx
  int v44; // eax
  int v45; // eax
  int v46; // eax
  int v47; // eax
  int v48; // eax
  int v49; // ecx
  int v50; // ecx
  char *v51; // ecx
  int v52; // ecx
  int v53; // ecx
  int v54; // ecx
  char *v55; // ecx
  void *v56; // ecx
  int v57; // [esp+30h] [ebp-5Ch] BYREF
  int v58; // [esp+34h] [ebp-58h] BYREF
  int v59; // [esp+38h] [ebp-54h] BYREF
  void *p_String; // [esp+3Ch] [ebp-50h] BYREF
  char *v61[4]; // [esp+40h] [ebp-4Ch] BYREF
  LPARAM lParam[3]; // [esp+50h] [ebp-3Ch] BYREF
  _BYTE v63[4]; // [esp+5Ch] [ebp-30h] BYREF
  CString *v64; // [esp+60h] [ebp-2Ch] BYREF
  CString *p_p_String; // [esp+64h] [ebp-28h] BYREF
  CString *v66; // [esp+68h] [ebp-24h] BYREF
  unsigned __int8 *Str1; // [esp+6Ch] [ebp-20h] BYREF
  CString *v68; // [esp+70h] [ebp-1Ch] BYREF
  int v69; // [esp+74h] [ebp-18h] BYREF
  char *v70; // [esp+78h] [ebp-14h] BYREF
  unsigned __int8 *v71; // [esp+7Ch] [ebp-10h] BYREF
  int v72; // [esp+88h] [ebp-4h]

  v72 = 0;
  lParam[1] = 0;
  lParam[0] = 20013;
  CString::CString((CString *)&v69);
  LOBYTE(v72) = 1;
  CString::CString((CString *)&v70);
  LOBYTE(v72) = 2;
  CString::CString((CString *)&Str1);
  LOBYTE(v72) = 3;
  CString::CString((CString *)&v66, `string');
  LOBYTE(v72) = 4;
  CString::operator=(&v69, aSysmessage);
  CString::operator=(&v70, aExecutesdlcomm_0);
  v61[0] = v3;
  v64 = (CString *)v61;
  CString::CString((CString *)v61, (const struct CString *)&String);
  CScaleMap::SetShareParameter(*(_DWORD *)(this + 392), &v69, &v70, v61[0]);
  CString::operator=(&v69, aSysmessage);
```
### Direct callees
- `0x10023683` `?GetModulName@CSDLInterface@@QAE?AVCString@@XZ` calls=1
- `0x100247C1` `sub_100247C1` calls=2
- `0x1002C9F8` `?CallBackFunction@CSSView@@QAEHJPAXH@Z` calls=2
- `0x1004C48D` `?LoadModule@CSSView@@QAEHVCString@@0I0@Z` calls=1
- `0x1004DD6F` `?ExecuteFunction@CSSView@@QAEPAXVCString@@I@Z` calls=1
- `0x1004DEB5` `?ExecuteFunction@CSSView@@QAEPAXVCString@@0@Z` calls=7
- `0x1004E304` `sub_1004E304` calls=1
- `0x1004E371` `sub_1004E371` calls=1
- `0x10075470` `?ssExcuteFunction@@YAHVCString@@00PAX1@Z` calls=2
- `0x100757C4` `?IsDigit@@YAHABVCString@@@Z` calls=1
- `0x10075CF2` `?GetNoteTemplate@CScaleMap@@QBEPAVMarkNoteTempls@@XZ` calls=1
- `0x10075CF8` `?GetFeatureList@CScaleMap@@QBEPAVCFeatureList@@XZ` calls=1
- `0x10075D22` `?SetShareParameter@CScaleMap@@QAEXABVCString@@0V2@@Z` calls=3
- `0x100760DC` `?GetShareParameter@CScaleMap@@QAEHABVCString@@0AAV2@1@Z` calls=1
- `0x100760E2` `?SetShareParameter@CScaleMap@@QAEXABVCString@@0PBX@Z` calls=1
- `0x1007669A` `??0CString@@QAE@XZ` calls=8
- `0x100766A0` `??0CString@@QAE@ABV0@@Z` calls=15
- `0x100766A6` `??1CString@@QAE@XZ` calls=30
- `0x100766AC` `??4CString@@QAEABV0@PBD@Z` calls=10
- `0x100766B2` `??4CString@@QAEABV0@ABV0@@Z` calls=3
- `0x100766E2` `??0CString@@QAE@PBD@Z` calls=20
- `0x1007671E` `?Format@CString@@QAAXPBDZZ` calls=2
- `0x100769CA` `?TrimLeft@CString@@QAEXXZ` calls=1
- `0x100769E2` `??H@YG?AVCString@@ABV0@PBD@Z` calls=4
- `0x10076A36` `?Delete@CString@@QAEHHH@Z` calls=3
- `0x10076A48` `?Left@CString@@QBE?AV1@H@Z` calls=2
- `0x10076A4E` `?Find@CString@@QBEHPBD@Z` calls=4
- `0x10076A5A` `?Replace@CString@@QAEHPBD0@Z` calls=2
- `0x10076A6C` `??H@YG?AVCString@@PBDABV0@@Z` calls=3
- `0x10076BD4` `?MakeUpper@CString@@QAEXXZ` calls=3

## Expanded first-level callees (head)
### 0x1005FCC4 sub_1005FCC4
```cpp
int __cdecl sub_1005FCC4(char a1)
{
  int v1; // ecx
  int SDLInterface; // esi
  int ScaleMap; // eax
  int v4; // ecx
  int v5; // eax
  _DWORD v7[3]; // [esp-4h] [ebp-1Ch] BYREF
  _DWORD *v8; // [esp+8h] [ebp-10h] BYREF
  int v9; // [esp+14h] [ebp-4h]

  v9 = 0;
  v7[0] = v1;
  v8 = v7;
  CString::CString((CString *)v7, (const struct CString *)&a1);
  SDLInterface = GetSDLInterface();
  if ( !SDLInterface )
  {
    CString::CString((CString *)&v8, (const struct CString *)&a1);
    LOBYTE(v9) = 1;
    ScaleMap = GetScaleMap(1);
    (*(void (__thiscall **)(int, int, _DWORD **, _DWORD))(*(_DWORD *)ScaleMap + 8))(ScaleMap, 31, &v8, 0);
    v7[0] = v4;
    v7[2] = v7;
```
### 0x10075482 ?ScanString@@YAXABVCString@@PBDAAVCStringArray@@H@Z
```cpp
// attributes: thunk
void __cdecl ScanString(const struct CString *a1, const char *a2, struct CStringArray *a3, int a4)
{
  __imp_?ScanString@@YAXABVCString@@PBDAAVCStringArray@@H@Z(a1, a2, a3, a4);
}
```
### 0x1007669A ??0CString@@QAE@XZ
```cpp
// attributes: thunk
CString *__thiscall CString::CString(CString *this)
{
  return __imp_??0CString@@QAE@XZ(this);
}
```
### 0x100766A0 ??0CString@@QAE@ABV0@@Z
```cpp
// attributes: thunk
CString *__thiscall CString::CString(CString *this, const struct CString *a2)
{
  return __imp_??0CString@@QAE@ABV0@@Z(this, a2);
}
```
### 0x100766A6 ??1CString@@QAE@XZ
```cpp
// attributes: thunk
void __thiscall CString::~CString(CString *this)
{
  __imp_??1CString@@QAE@XZ(this);
}
```
### 0x100766B2 ??4CString@@QAEABV0@ABV0@@Z
```cpp
// attributes: thunk
int __thiscall CString::operator=(void *this, int a2)
{
  return __imp_??4CString@@QAEABV0@ABV0@@Z(this, a2);
}
```
### 0x100766CA ??1CStringArray@@UAE@XZ
```cpp
// attributes: thunk
void __thiscall CStringArray::~CStringArray(CStringArray *this)
{
  __imp_??1CStringArray@@UAE@XZ(this);
}
```
### 0x100766D6 ??0CStringArray@@QAE@XZ
```cpp
// attributes: thunk
CStringArray *__thiscall CStringArray::CStringArray(CStringArray *this)
{
  return __imp_??0CStringArray@@QAE@XZ(this);
}
```
### 0x1007682C ?AfxMessageBox@@YGHPBDII@Z
```cpp
// attributes: thunk
int __stdcall AfxMessageBox(const char *a1, unsigned int a2, unsigned int a3)
{
  return __imp_?AfxMessageBox@@YGHPBDII@Z(a1, a2, a3);
}
```
### 0x1007696A ?RemoveAt@CStringArray@@QAEXHH@Z
```cpp
// attributes: thunk
void __thiscall CStringArray::RemoveAt(CStringArray *this, int a2, int a3)
{
  __imp_?RemoveAt@CStringArray@@QAEXHH@Z(this, a2, a3);
}
```
### 0x100769A0 ??YCString@@QAEABV0@ABV0@@Z
```cpp
// attributes: thunk
int __thiscall CString::operator+=(void *this, int a2)
{
  return __imp_??YCString@@QAEABV0@ABV0@@Z(this, a2);
}
```
### 0x10076A48 ?Left@CString@@QBE?AV1@H@Z
```cpp
// attributes: thunk
int __thiscall CString::Left(void *this, int a2, int a3)
{
  return __imp_?Left@CString@@QBE?AV1@H@Z(this, a2, a3);
}
```
### 0x10076A5A ?Replace@CString@@QAEHPBD0@Z
```cpp
// attributes: thunk
int __thiscall CString::Replace(CString *this, const char *a2, const char *a3)
{
  return __imp_?Replace@CString@@QAEHPBD0@Z(this, a2, a3);
}
```
### 0x10076A6C ??H@YG?AVCString@@PBDABV0@@Z
```cpp
// attributes: thunk
int __stdcall operator+(int a1, int a2, int a3)
{
  return __imp_??H@YG?AVCString@@PBDABV0@@Z(a1, a2, a3);
}
```
### 0x10076AAE ?Mid@CString@@QBE?AV1@HH@Z
```cpp
// attributes: thunk
int __thiscall CString::Mid(void *this, int a2, int a3, int a4)
{
  return __imp_?Mid@CString@@QBE?AV1@HH@Z(this, a2, a3, a4);
}
```
### 0x10076BA4 ?ReverseFind@CString@@QBEHD@Z
```cpp
// attributes: thunk
int __thiscall CString::ReverseFind(CString *this, char a2)
{
  return __imp_?ReverseFind@CString@@QBEHD@Z(this, a2);
}
```
### 0x10076E6E ?Find@CString@@QBEHD@Z
```cpp
// attributes: thunk
int __thiscall CString::Find(CString *this, char a2)
{
  return __imp_?Find@CString@@QBEHD@Z(this, a2);
}
```
### 0x100777E8 _EH_prolog
```cpp
// attributes: thunk
int EH_prolog()
{
  return _EH_prolog();
}
```
### 0x10084F08 _mbscmp
```cpp
```
### 0x10023683 ?GetModulName@CSDLInterface@@QAE?AVCString@@XZ
```cpp
CString *__thiscall CSDLInterface::GetModulName(int this, CString *a2)
{
  CString::CString(a2, (const struct CString *)(this + 4));
  return a2;
}
```
### 0x100247C1 sub_100247C1
```cpp
int sub_100247C1()
{
  struct CWinThread *Thread; // eax

  Thread = AfxGetThread();
  if ( Thread )
    return (*(int (__thiscall **)(struct CWinThread *))(*(_DWORD *)Thread + 124))(Thread);
  else
    return 0;
}
```
### 0x1002C9F8 ?CallBackFunction@CSSView@@QAEHJPAXH@Z
```cpp
int __thiscall CSSView::CallBackFunction(CSSView *this, CString *p_X, __int64 a3)
{
  CString *v3; // edi
  int v5; // esi
  int v6; // ecx
  CString *v7; // eax
  int v8; // edi
  int v9; // ecx
  int ClientArea; // eax
  int v11; // esi
  int v12; // ecx
  int v13; // eax
  int i; // esi
  int v15; // ecx
  char *v16; // edi
  char *v17; // edi
  char *v18; // edi
  bool v19; // zf
  int v20; // eax
  int v21; // eax
  int v22; // eax
  int v23; // eax
  int v24; // eax
  struct MarkNoteTempl *NoteTemplBynumber; // eax
```
### 0x1004C48D ?LoadModule@CSSView@@QAEHVCString@@0I0@Z
```cpp
int __thiscall CSSView::LoadModule(CSSView *this, char *a2, LPCSTR lpProcName, CString *a4, int a5)
{
  struct CSDLInterface *v6; // ecx
  int PathName; // eax
  int v9; // ebx
  int v10; // ecx
  struct CSDLInterface *v11; // ecx
  HMODULE Library; // ebx
  int v13; // eax
  int v14; // eax
  int v15; // esi
  struct CSDLInterface *v16; // ecx
  int v17; // eax
  int (*ProcAddress)(void); // eax
  struct CSDLInterface *v19; // eax
  CSSView *v20; // ecx
  struct CSDLInterface *v21; // ecx
  struct CSDLInterface *v22; // ecx
  struct CSDLInterface *v23; // [esp-8h] [ebp-238h] BYREF
  struct CSDLInterface *v24[4]; // [esp-4h] [ebp-234h] BYREF
  _BYTE v25[176]; // [esp+Ch] [ebp-224h] BYREF
  _BYTE v26[332]; // [esp+BCh] [ebp-174h] BYREF
  char *v27; // [esp+208h] [ebp-28h] BYREF
  int v28; // [esp+20Ch] [ebp-24h] BYREF
```
### 0x1004DD6F ?ExecuteFunction@CSSView@@QAEPAXVCString@@I@Z
```cpp
CString *__thiscall CSSView::ExecuteFunction(int *this, char a2, unsigned int a3)
{
  int v4; // ebx
  int v5; // ecx
  int v6; // eax
  int *v8; // eax
  int v9; // edx
  CString *v10; // eax
  int v11; // ecx
  CString *v12; // esi
  int v13; // [esp-Ch] [ebp-34h] BYREF
  _BYTE *v14; // [esp-8h] [ebp-30h]
  _DWORD v15[4]; // [esp-4h] [ebp-2Ch] BYREF
  CString *v16; // [esp+Ch] [ebp-1Ch]
  CString *v17; // [esp+10h] [ebp-18h] BYREF
  _BYTE v18[4]; // [esp+14h] [ebp-14h] BYREF
  _BYTE v19[4]; // [esp+18h] [ebp-10h] BYREF
  int v20; // [esp+24h] [ebp-4h]

  v4 = 0;
  v20 = 0;
  if ( CSSView::OnCommProcess((CSSView *)this, a3) )
    goto LABEL_6;
  CString::CString((CString *)v19);
```
### 0x1004DEB5 ?ExecuteFunction@CSSView@@QAEPAXVCString@@0@Z
```cpp
CString *__thiscall CSSView::ExecuteFunction(int this, unsigned __int8 *a2, unsigned __int8 *Str1)
{
  const CHAR *v4; // ecx
  CString *v5; // esi
  char *v6; // ecx
  int v7; // ecx
  int v8; // eax
  int v9; // eax
  int OperateBar; // ebx
  unsigned __int8 *v11; // ecx
  int v12; // ecx
  int v13; // edi
  int v14; // eax
  int v15; // eax
  int v16; // eax
  int v17; // ecx
  const CHAR *v18; // ecx
  char *v19; // ecx
  int v20; // eax
  bool v21; // cc
  int v22; // edi
  int v23; // eax
  int v24; // eax
  const CHAR *v25; // ecx
```
### 0x1004E304 sub_1004E304
```cpp
void __cdecl sub_1004E304(CString *a1)
{
  int v1; // edi
  int v2; // eax

  if ( !CString::Find(a1, aSdl) || !CString::Find(a1, aSdl_2) )
  {
    CString::SetAt(a1, 4, 44);
    v1 = CString::Find(a1, asc_100BD9E4, 5);
    v2 = CString::Find(a1, asc_100C37A0, 5);
    if ( v1 < 0 )
      v1 = 10000;
    if ( v2 > 0 && v2 < v1 )
      CString::SetAt(a1, v2, 44);
  }
}
```
### 0x1004E371 sub_1004E371
```cpp
void __cdecl sub_1004E371(int a1, char *String)
{
  int v2; // esi
  int v3; // eax
  int v4; // eax
  int v5; // ecx
  int i; // esi
  int v7; // eax
  _DWORD v8[3]; // [esp-10h] [ebp-5Ch] BYREF
  _DWORD v9[4]; // [esp-4h] [ebp-50h] BYREF
  _BYTE v10[4]; // [esp+Ch] [ebp-40h] BYREF
  int v11; // [esp+10h] [ebp-3Ch]
  int v12; // [esp+14h] [ebp-38h]
  _BYTE v13[16]; // [esp+24h] [ebp-28h] BYREF
  _BYTE v14[4]; // [esp+34h] [ebp-18h] BYREF
  _DWORD *v15; // [esp+38h] [ebp-14h]
  unsigned __int16 v16; // [esp+3Eh] [ebp-Eh]
  int v17; // [esp+48h] [ebp-4h]

  v17 = 0;
  CGeObjList::CGeObjList((CGeObjList *)v10);
  v2 = a1;
  LOBYTE(v17) = 1;
  CPtrArray::Copy((CPtrArray *)v10, (const struct CPtrArray *)(a1 + 384));
```
### 0x10075470 ?ssExcuteFunction@@YAHVCString@@00PAX1@Z
```cpp
// attributes: thunk
int ssExcuteFunction(void)
{
  return __imp_?ssExcuteFunction@@YAHVCString@@00PAX1@Z();
}
```
### 0x100757C4 ?IsDigit@@YAHABVCString@@@Z
```cpp
// attributes: thunk
int __cdecl IsDigit(const struct CString *a1)
{
  return __imp_?IsDigit@@YAHABVCString@@@Z(a1);
}
```
### 0x10075CF2 ?GetNoteTemplate@CScaleMap@@QBEPAVMarkNoteTempls@@XZ
```cpp
// attributes: thunk
struct MarkNoteTempls *__thiscall CScaleMap::GetNoteTemplate(CScaleMap *this)
{
  return __imp_?GetNoteTemplate@CScaleMap@@QBEPAVMarkNoteTempls@@XZ(this);
}
```
### 0x10075CF8 ?GetFeatureList@CScaleMap@@QBEPAVCFeatureList@@XZ
```cpp
// attributes: thunk
struct CFeatureList *__thiscall CScaleMap::GetFeatureList(CScaleMap *this)
{
  return __imp_?GetFeatureList@CScaleMap@@QBEPAVCFeatureList@@XZ(this);
}
```
### 0x10075D22 ?SetShareParameter@CScaleMap@@QAEXABVCString@@0V2@@Z
```cpp
// attributes: thunk
int __thiscall CScaleMap::SetShareParameter(void *this, int a2, int a3, int a4)
{
  return __imp_?SetShareParameter@CScaleMap@@QAEXABVCString@@0V2@@Z(this, a2, a3, a4);
}
```
### 0x100760DC ?GetShareParameter@CScaleMap@@QAEHABVCString@@0AAV2@1@Z
```cpp
// attributes: thunk
int __thiscall CScaleMap::GetShareParameter(
        CScaleMap *this,
        const struct CString *a2,
        const struct CString *a3,
        struct CString *a4,
        struct CString *a5)
{
  return __imp_?GetShareParameter@CScaleMap@@QAEHABVCString@@0AAV2@1@Z(this, a2, a3, a4, a5);
}
```
### 0x100760E2 ?SetShareParameter@CScaleMap@@QAEXABVCString@@0PBX@Z
```cpp
// attributes: thunk
void __thiscall CScaleMap::SetShareParameter(
        CScaleMap *this,
        const struct CString *a2,
        const struct CString *a3,
        const void *a4)
{
  __imp_?SetShareParameter@CScaleMap@@QAEXABVCString@@0PBX@Z(this, a2, a3, a4);
}
```
### 0x100766AC ??4CString@@QAEABV0@PBD@Z
```cpp
// attributes: thunk
int __thiscall CString::operator=(void *this, int a2)
{
  return __imp_??4CString@@QAEABV0@PBD@Z(this, a2);
}
```