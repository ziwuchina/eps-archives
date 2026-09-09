# ScriptCryptor 脚本加密 + 加密狗授权体系梳理（2026-09-09）

## 1. 加密链（静态分析）

```
ScriptCryptor.exe（前端，472KB PE32 GUI）
  → EncryptByPI\EncryptByPI.dll（COM 封装，DllGetClassObject/DllRegisterServer，含全套 VC 工程产物）
    → PiEncrypt.dll（核心 1MB / 27 导出）/ PiEncrypt1.dll（兼容层 28KB / 13 导出 C++ 修饰）
      → libcrypto-1_1.dll（OpenSSL 1.1 密码学原语）
      → 输出加密脚本 + ScriptCryptor.dat（187KB 密钥/版本库）
```

## 2. 多密钥版本体系（PiEncrypt 导出语义）

| API | 作用 |
|---|---|
| `PiEncryptFile/PiDecryptFile/PiEncFileInMem/PiDecFileInMem/PiEncryptMem/PiDecryptMem` | 文件/内存级加解密 |
| `PiEncFileInMemByKeyID/PiEncryptFileUseKey/PiDecryptFileWithKey` | 按密钥 ID / 显式密钥 |
| `PiGetDefKeyVer/PiSetDefKeyVer/PiGetKeyVer/PiGetKeyVerCount` | 密钥版本管理（默认/枚举） |
| `PiGetFileEncState` | 加密文件状态查询（文件头含版本标识） |
| `PiReadVerInfo/PiWriteVerInfo/PiGetFileBuff/PiSetFileBuff` | 版本信息/文件缓冲 IO |

## 3. License 授权格式（已破解）

`D:\EPS2016Shunde\License\1500-5405-0960-6843.txt`（14981B，17 个授权文件）：

```
SSEdit   编辑平台,1C700C6574031174...CE4EEA1E73A4449F8917F61205BFAD1E
SScript  脚本处理,1C700C6574711174...CE4EEA1E73A4449F8917F61205BFAD1E
SSCheck  数据监理,1C700C6574751174...CE4EEA1E73A4449F8917F61205BFAD1E
```

**行格式**：`模块名,模块中文名,<16 进制权限码>,<32hex MD5 校验>` —— **按功能模块授权**（SSEdit 编辑平台/SScript 脚本处理/SSCheck 数据监理），权限码为密文，行尾 MD5 防篡改。

## 4. 加密狗（UsbKey）

SafeNet **HASP 加密狗**体系：haspdinst.exe（驱动安装）、HASPUserSetup.exe、lmsetup.exe、aksmon32.exe —— EPS 运行时依赖 HASP 狗授权，与 License 文件双保险。

## 5. 结论

- **加密机制**：OpenSSL 原语 + PiEncrypt 多密钥版本加密 + EncryptByPI COM 封装，加密脚本带版本头（`PiGetFileEncState` 可查）。
- **授权机制**：HASP 加密狗 + License 按模块授权（权限码 + MD5 校验）。
- **遗留（blocked）**：加密脚本样例缺失，字节级解包验证未做；License 权限码位含义需解密后确认。

## 6. 证据与复现

- `reports/scriptcryptor_mechanism_evidence.json`；复现：pefile 分析（脚本见会话）。
