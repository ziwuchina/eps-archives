# WzExtBridge 调用链验证（静态）报告（2026-09-09）

## 1. 关键发现：WzExtBridge.SDL 实为 PE 可执行文件

- `D:\EPS2016Shunde\WzExtBridge.SDL`（299,520 字节）**不是脚本/文本，而是 32 位 PE GUI 模块**（MZ 头，i386，Subsystem=2）。
- 印证 EPS SDL 插件机制：**SDL 文件 = PE 模块伪装**，由 `ExecuteCommand` 按文件名加载执行。
- PE 元数据：ImageBase=0x10000000，DllCharacteristics=0x140（**启用 ASLR**，与 SSProject.dll 无 ASLR 不同），编译时间戳 2026-04-12。

## 2. 12 个导出函数 = 完整外部模块接口

| 导出 | 作用（对照步骤2.4 调用链） |
|---|---|
| `RegisterCmd` | 命令注册（SSProject.IsRegisterCmd 匹配目标） |
| `ExecuteCommand` | 外部模块入口（官方 `ExecuteCommand(libFileName, procName, desc, transSelection)`） |
| `ExecuteSDLFunction` | SDL 函数执行（SSProcess.ExecuteSDLFunction 对应） |
| `ExecFunction` / `SDLFunctionExecute` | 函数执行体 |
| `SetModulName` / `SSInterfaceHandle` / `CreateInterface` | 模块挂接（步骤2.4：SetModulName/GetModulName 挂接） |
| `GetSDLCommandInfo` | 命令信息查询 |
| `WzExtProbe` / `WzExtProbeWithSelection` | **业务 proc（候选）**，字符串含 `WzExtBridge Probe Report` / `(dispatch)` |

## 3. WzExtProbe 入口反汇编（RVA 0x4CC0）

```
push ebp; mov ebp,esp; sub esp,0x20          ; 标准 prologue
mov eax,[ebp+0x10]; push eax                  ; arg3 -> CProgressCtrl*
mov ecx,[ebp+0x0c]; push ecx                  ; arg2 -> CGeObjList*
mov edx,[ebp+8];    push edx                  ; arg1 -> CStringArray*
lea eax,[ebp-0x1c]; push eax
call 0x10004380                               ; 内部调度（3 参 + 返回缓冲）
```

**签名匹配**：`WzExtProbe` 3 个栈参数与官方 `extern "C" BOOL proc(CStringArray*, CGeObjList*, CProgressCtrl*)` **完全一致**。

## 4. 调用链闭环（静态证明）

```
SSProcess.ExecuteCommand("WzExtBridge.SDL", "WzExtProbe", desc, transSelection)
  → LoadLibrary(WzExtBridge.SDL)      （SDL=PE 伪装模块）
  → GetProcAddress("WzExtProbe")       （导出表 RVA 0x4CC0）
  → proc(CStringArray*, CGeObjList*, CProgressCtrl*)   （3 参栈调用）
  → 返回 "WzExtBridge Probe Report"（内部 0x10004380 调度）
```

与步骤2.4 的 SSProject.dll 链路（ExecuteSDLCommand → IsRegisterCmd → vtable[0x40] → LoadModule/SetModulName）**衔接闭合**：WzExtBridge.SDL 正是该机制的可加载外部模块样例。

## 5. 限制（如实）

- 动态加载验证需 EPS 运行环境实机调用，未执行（不在用户生产环境注入外部模块）。
- WzExtBridge.SDL 启用 ASLR，运行时基址随机；导出表按名解析不受影响。

## 6. 证据

- `reports/wzext_bridge_evidence.json`（PE/导出/反汇编/链路/限制）
- 复现：`wzext_probe.py`（pefile + capstone）
