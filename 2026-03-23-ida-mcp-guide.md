# IDA-MCP 完整使用指南
**日期：2026-03-23**
**版本：v1.0**

---

## 一、核心问题与解决

### 问题：Gateway 注册机制失效

IDA 实例启动后不向 gateway 注册（`ida list` 返回 0 实例），所有通过 `command.py tool call --port X` 的调用都失败。

### 解决方案：直连实例端口 + mcp-session-id

绕过 gateway 注册，直接访问每个 IDA 实例的 HTTP MCP 端点：
```
http://127.0.0.1:{port}/mcp  (注意不是 /mcp/)
```

请求先发 `initialize`，从响应 Header 中取出 `mcp-session-id`，后续所有请求都带这个 header。

---

## 二、IDA 实例端口分配

| 端口 | DLL/文件 | 说明 |
|------|----------|------|
| 10000 | `Eps.exe.i64` | 主程序，x86 32位 |
| 10001 | `SSCore32.dll.i64` | 核心库（HASP加密/EDB） |
| 10002 | `SSMap.dll.i64` | 地图模块，5119函数 |
| 10003 | `SScript.dll.i64` | 脚本引擎，1641 SDL命令 |

查看当前监听的 IDA 端口：
```powershell
Get-NetTCPConnection -LocalPort 10000,10001,10002,10003 -ErrorAction SilentlyContinue | Where-Object {$_.State -eq 'Listen'} | Format-Table LocalPort, OwningProcess
```

Gateway 状态（此方法下 gateway 注册数不重要）：
```cmd
python "D:\AIcode\mcpida\IDA-MCP\command.py" gateway status
```

---

## 三、MCP 调用协议（可直接使用的 Python 模板）

### 关键文件
- `C:\Users\Administrator\.openclaw\workspace\ida_mcp_call.py` — 单次工具调用
- `C:\Users\Administrator\.openclaw\workspace\exercise_ida_mcp.py` — 全工具覆盖测试脚本

### 标准调用流程

```python
import urllib.request, json

def post(url, payload, session_id=None, timeout=60):
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    if session_id:
        headers["mcp-session-id"] = session_id
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        sid = resp.headers.get("mcp-session-id") or session_id
        text = resp.read().decode("utf-8", errors="replace")
    return sid, text

def parse_sse_json(text):
    for line in text.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:])
    raise RuntimeError("No JSON in SSE")

# ===== 使用 =====
PORT = 10000  # 或 10001/10002/10003
url = f"http://127.0.0.1:{PORT}/mcp"

# 1. Initialize 获取 session_id
sid, init_text = post(url, {
    "jsonrpc": "2.0", "id": "init", "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "clientInfo": {"name": "client", "version": "1.0"},
        "capabilities": {},
    }
})
init_result = parse_sse_json(init_text)
print("Session ID:", sid)
print("Server:", init_result["result"]["serverInfo"])

# 2. 调用工具
sid, tool_text = post(url, {
    "jsonrpc": "2.0", "id": "call", "method": "tools/call",
    "params": {"name": "get_metadata", "arguments": {}}
}, sid)
tool_result = parse_sse_json(tool_text)
print(json.dumps(tool_result, indent=2, ensure_ascii=False))
```

### 常用工具调用示例

```python
# 列出所有工具
sid, t = post(url, {"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}, sid)
tools = parse_sse_json(t)["result"]["tools"]

# 获取二进制信息
sid, r = post(url, {"jsonrpc":"2.0","id":"2","method":"tools/call",
    "params":{"name":"get_metadata","arguments":{}}}, sid)

# 列出函数（分页）
sid, r = post(url, {"jsonrpc":"2.0","id":"3","method":"tools/call",
    "params":{"name":"list_functions","arguments":{"offset":0,"limit":10}}}, sid)

# 反汇编
sid, r = post(url, {"jsonrpc":"2.0","id":"4","method":"tools/call",
    "params":{"name":"disasm","arguments":{"addresses":["0x401000"]}}}, sid)

# 反编译
sid, r = post(url, {"jsonrpc":"2.0","id":"5","method":"tools/call",
    "params":{"name":"decompile","arguments":{"addresses":["0x401000"]}}}, sid)

# 交叉引用
sid, r = post(url, {"jsonrpc":"2.0","id":"6","method":"tools/call",
    "params":{"name":"xrefs_to","arguments":{"addresses":["0x401000"]}}}, sid)

# 搜索字节
sid, r = post(url, {"jsonrpc":"2.0","id":"7","method":"tools/call",
    "params":{"name":"find_bytes","arguments":{"pattern":"4C 6F 67 69 6E 45 52 50","limit":5}}}, sid)

# 读内存
sid, r = post(url, {"jsonrpc":"2.0","id":"8","method":"tools/call",
    "params":{"name":"get_bytes","arguments":{"address":"0x401000","size":32}}}, sid)

# 资源（ida:// URI）
sid, rl = post(url, {"jsonrpc":"2.0","id":"9","method":"resources/list","params":{}}, sid)
sid, rr = post(url, {"jsonrpc":"2.0","id":"10","method":"resources/read",
    "params":{"uri":"ida://idb/metadata"}}, sid)
```

---

## 四、工具分类与调用示例

### 分析类
| 工具 | 示例参数 | 说明 |
|------|----------|------|
| `decompile` | `{"addresses": ["0x401000"]}` | Hex-Rays 反编译 |
| `disasm` | `{"addresses": ["0x401000"]}` | 反汇编 |
| `linear_disasm` | `{"start_address": "0x401000", "count": 20}` | 线性反汇编 |
| `xrefs_to` | `{"addresses": ["0x401000"]}` | 谁调用了这个地址 |
| `xrefs_from` | `{"addresses": ["0x401000"]}` | 这个地址调用了什么 |
| `get_callers` | `{"addresses": ["0x401000"]}` | 调用者汇总 |
| `get_callees` | `{"addresses": ["0x401000"]}` | 被调者汇总 |
| `get_function_signature` | `{"addresses": ["0x401000"]}` | 函数签名 |
| `get_basic_blocks` | `{"address": "0x401000"}` | 基本块 CFG |
| `find_bytes` | `{"pattern": "55 8B EC", "limit": 5}` | 字节模式搜索 |

### 列表类
| 工具 | 示例参数 | 说明 |
|------|----------|------|
| `list_functions` | `{"offset": 0, "limit": 100}` | 函数列表（Eps.exe共2374个） |
| `list_strings` | `{"offset": 0, "limit": 100}` | 字符串列表 |
| `list_imports` | `{"offset": 0, "limit": 50}` | 导入函数 |
| `list_exports` | `{"offset": 0, "limit": 50}` | 导出函数 |
| `list_segments` | `{}` | 内存段（.text/.idata/.rdata/.rsrc） |
| `list_globals` | `{"offset": 0, "limit": 10}` | 全局符号 |

### 内存读取类
| 工具 | 示例参数 | 说明 |
|------|----------|------|
| `get_bytes` | `{"address": "0x401000", "size": 16}` | 读原始字节 |
| `read_scalar` | `{"address": "0x401000", "width": 4}` | 读整数 |
| `get_string` | `{"address": "0x401000", "max_length": 64}` | 读字符串 |

### 修改类（写操作）
| 工具 | 示例参数 | 说明 |
|------|----------|------|
| `set_comment` | `{"address": "0x401000", "comment": "test", "repeatable": false}` | 设置注释 |
| `rename_function` | `{"address": "0x401000", "new_name": "my_func"}` | 重命名函数 |
| `patch_bytes` | `{"address": "0x401000", "bytes": "90"}` | 补丁字节 |

### 资源（ida:// URI）
所有资源通过 `resources/read` 访问：
- `ida://idb/metadata` — IDB元数据
- `ida://functions` — 函数列表
- `ida://strings` — 字符串列表
- `ida://segments` — 内存段
- `ida://imports` — 导入表
- `ida://exports` — 导出表

---

## 五、已知问题与限制

1. **decompiler vs decompile**：工具列表显示 `decompiler`，但正确工具名是 `decompile`
2. **Debugger 工具需要活跃调试会话**：否则返回 "debugger not active"
3. **参数验证严格**：部分工具缺少参数时返回 validation error（正常行为）
4. **`dbg_start` 会导致服务器中断**：在某些实例上启动调试器会使 MCP 服务器无响应
5. **Gateway 注册机制不稳定**：直接连接实例端口是唯一可靠方式

---

## 六、启动新的 IDA 实例

```cmd
:: 启动 IDA 加载 Eps.exe（ autonomous 模式会分析完自动退出）
python "D:\AIcode\mcpida\IDA-MCP\command.py" ida open "D:\EPS2026G\Eps.exe" --interactive

:: 启动 IDA 加载 DLL（推荐保留交互模式）
python "D:\AIcode\mcpida\IDA-MCP\command.py" ida open "D:\EPS2026G\SSMap.dll.i64" --interactive

:: 列出可用实例（不稳定，参考价值有限）
python "D:\AIcode\mcpida\IDA-MCP\command.py" ida list

:: 关闭实例（不保存数据库）
python "D:\AIcode\mcpida\IDA-MCP\command.py" ida close --port 10000 --save no
```

---

## 七、相关文件路径

| 文件 | 说明 |
|------|------|
| `C:\Users\Administrator\.openclaw\workspace\ida_mcp_call.py` | MCP 单次调用工具 |
| `C:\Users\Administrator\.openclaw\workspace\exercise_ida_mcp.py` | 全工具覆盖测试脚本 |
| `C:\Users\Administrator\.openclaw\workspace\reports\ida_mcp_eps_alltools.md` | Eps.exe 工具报告 |
| `C:\Users\Administrator\.openclaw\workspace\reports\ida_mcp_sscore_alltools.md` | SSCore32.dll 报告 |
| `C:\Users\Administrator\.openclaw\workspace\reports\ida_mcp_ssmap_alltools.md` | SSMap.dll 报告 |
| `C:\Users\Administrator\.openclaw\workspace\reports\ida_mcp_sscript_alltools.md` | SScript.dll 报告 |
| `D:\AIcode\mcpida\IDA-MCP\` | IDA-MCP 安装目录 |
| `D:\AIcode\mcpida\IDA-MCP\command.py` | IDA-MCP 命令行工具 |
| `D:\AIcode\mcpida\IDA-MCP\ida_mcp\` | MCP 核心库 |
| `D:\EPS2026G\*.i64` | IDA 数据库文件 |
