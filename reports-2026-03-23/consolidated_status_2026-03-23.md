# EPS 工作进展总报告

**生成时间**: 2026-03-23 03:13:42

---

## 一、177030-099 追踪结果  ✅

**重大发现**：在 `佛山数据.edb` 的 `FC_楼层分割信息表` 中找到了 177030-099！

| 字段 | 值 |
|------|-----|
| 完整编号 | `177030-099F0001L001` |
| 行政区号 | 177030 |
| 户序号 | 099 |
| 楼栋号 | F0001 |
| 楼层 | L001 |
| FeatureGUID | D56BD259-08AB-49B3-9A91-CDA8FD73126F |
| ZDGUID (宗地) | BA637CC1-4666-4551-B72C-E40A6A6CACE8 |
| ZRZGUID (权利) | 26E8C9DB-BBC8-43E4-BB34-48B67797F469 |
| 原产权面积 | 0.0 |
| 门牌号 | NULL |

**含义**：这是佛山市禅城区的一个房产单元（户），对应的权利对象和项目信息需要进一步查询。

---

## 二、EPS 登录系统故障  ❌

**错误**：`Load loginerploginerp.SDL/(.DLL) failed`

**根本原因**：`D:\EPS2026G\loginerploginerp.SDL` 文件不存在

**证据**：
- D:\EPS2026G 下共 47 个 .SDL 文件，但没有一个以 'login' 开头
- 全盘搜索：无此文件
- 文件名非常可疑：'loginerploginerp' 看起来像 'loginERP' + 'loginERP.SDL' 拼接错误

**影响**：点击「扩展登录...」后立即报错，无法完成 EPS 系统登录

**分析**：
- loginERP 命令字符串在 DLL 中不存在（动态构造）
- SDL 脚本系统在 EPS 内部，不在文件系统
- 可能是路径构建 bug：module name + command name 拼接错误

**尝试的解决方向**：
- SDSLogin → ArcSDE 数据库登录，非 EPS 系统登录
- SDBLogin → 数据库登录，非 EPS 系统登录
- COM 自动化 → 需要先登录才能使用
- 注册表 → 无 SDL 路径配置

---

## 三、IDA-MCP 全工具覆盖测试  ✅

| 实例 | 端口 | 工具成功 | 总测试 |
|------|------|----------|--------|
| Eps.exe | 10000 | 24 | 29 (4参数错误) |
| SSCore32.dll | 10001 | 31 | 31全成功 |
| SSMap.dll | 10002 | 33 | 33全成功+10资源 |
| SScript.dll | 10003 | 46 | 53 (7Debugger) |

---

## 四、loginERP 命令链追溯  ✅

**完整调用链**：
```
ExecuteCommand (0x10044B5B, SScript.dll)
  → GetSDLRuntimeCmdID (0x1001D851)
    → SDLFunctionExecute [thunk → SScriptCore.dll]
      → script_ExecuteFunction (0x1002D140)
        → CSScriptHandle::RunScript (0x1002B440)
          → ScriptEngineFactory::GetIDOfFunction('loginERP')
            → COleDispatchDriver::InvokeHelper [COM IDispatch]
              → loginERP 实现 (在 SScriptCore.dll)
```

**关键发现**：
- SScriptCore.dll 是真正的 SDL 运行时
- loginERP 字符串在 DLL 中不存在（动态注册）
- HASP licensing 代码在 SSCore32.dll，不在 SScriptCore.dll
- HASP 狗狗问题（已忽略）：佛山狗 = 硬件狗，需正常使用时插入

---

## 五、EPS 网络架构  ✅

- HTTP 库：MFC WinInet (CInternetSession, CHttpConnection, CHttpFile)
- 服务端点：`langem14x/EpsService`
- 更新服务：`sunwaysurvey.com.cn/update`
- IP 219.130.221.6：未找到硬编码，可能通过 DNS 解析
- ArcGIS 集成：SSArcSDEUpdate, SSArcGISRender (SuperMap SDE)

---

## 六、ODBC 直读 EDB 数据  ✅

- 连接字符串：`Driver={Microsoft Access Driver (*.mdb)};DBQ={path}`
- 佛山数据.edb：194 个表，可读
- 顺德数据.edb：可读
- 当前 EDB (2500.00-408.00)：测试数据，2013年，X~408000
- 佛山数据中无 177xxx 系列代码（177030 在 FC_楼层分割信息表中）

---

## 七、SScriptCore.dll 分析结论  ✅

- 纯 MFC/COM 脚本引擎包装器（ScriptEngineFactory）
- 7 个导入：ScriptEngineFactory 类方法（Instance, GetIDOfFunction, LoadScript 等）
- 不含 HASP/licensing 代码
- 不含 loginERP 字符串
- HRVerify (ORDINAL 7) = HResult verification，非 HASP

---

## 八、下一步工作

**登录故障解决后**：
1. 查询 177030-099 对应的 ZD_权利信息（zdguid: BA637CC1...）
2. 查询 ZD_实情信息、楼栋信息
3. 在 EPS 中打开佛山数据，验证 177030-099 是否存在

**登录故障解决方法**：
1. 检查 EPS 安装是否完整，尝试修复/重装
2. 从备份恢复 loginerploginerp.SDL 文件
3. 检查是否有 EPS 修复工具
4. 询问曾工此文件的正常位置

---

*报告生成时间：2026-03-23 03:13:42*