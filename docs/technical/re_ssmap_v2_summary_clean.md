## check {"ok":true,"count":4}

## setshare decompile
[{"query":"0x10016E67","name":"?SetShareParameter@CScaleMap@@QAEXABVCString@@0V2@@Z","start_ea":"0x10016E67","end_ea":"0x10016EB4","decompiled":"void __thiscall CScaleMap::SetShareParameter(void *this, int a2, int a3, char a4)\n{\n  _DWORD v4[3]; // [esp-4h] [ebp-18h] BYREF\n  int v5; // [esp+10h] [ebp-4h]\n\n  v5 = 0;\n  v4[0] = this;\n  v4[2] = v4;\n  CString::CString((CString *)v4, (const struct CString *)&a4);\n  sub_1001750B(a2, a3, v4[0]);\n  v5 = -1;\n  CString::~CString((CString *)&a4);\n}\n"}]

## setshare callers
{"query":"0x10016E67","function":"?SetShareParameter@CScaleMap@@QAEXABVCString@@0V2@@Z","start_ea":"0x10016E67","end_ea":"0x10016EB4","total":2,"items":[{"address":"0x1004A7DE","name":"sub_1004A7DE","call_count":4,"call_sites":["0x1004A9A5","0x1004A9F9","0x1004AA4D","0x1004AAA2"]},{"address":"0x1004C607","name":"?SelectOptionFromScript@@YA?AVCString@@PAVCScaleMap@@IV1@11@Z","call_count":4,"call_sites":["0x1004C6E3","0x1004C737","0x1004C78B","0x1004C7E0"]}]}

## setshare callees
{"query":"0x10016E67","function":"?SetShareParameter@CScaleMap@@QAEXABVCString@@0V2@@Z","start_ea":"0x10016E67","end_ea":"0x10016EB4","total":4,"items":[{"address":"0x1001750B","name":"sub_1001750B","call_count":1,"call_sites":["0x10016E94"]},{"address":"0x100DF6EA","name":"??0CString@@QAE@ABV0@@Z","call_count":1,"call_sites":["0x10016E83"]},{"address":"0x100DF6F0","name":"??1CString@@QAE@XZ","call_count":1,"call_sites":["0x10016EA0"]},{"address":"0x100E0058","name":"_EH_prolog","call_count":1,"call_sites":["0x10016E6C"]}]}

## setshare xrefs
[{"query":"0x10016E67","address":"0x10016E67","total":9,"xrefs":[{"frm":"0x1004A9A5","type":17,"iscode":true},{"frm":"0x1004A9F9","type":17,"iscode":true},{"frm":"0x1004AA4D","type":17,"iscode":true},{"frm":"0x1004AAA2","type":17,"iscode":true},{"frm":"0x1004C6E3","type":17,"iscode":true},{"frm":"0x1004C737","type":17,"iscode":true},{"frm":"0x1004C78B","type":17,"iscode":true},{"frm":"0x1004C7E0","type":17,"iscode":true},{"frm":"0x10131AB8","type":1,"iscode":false}]}]
