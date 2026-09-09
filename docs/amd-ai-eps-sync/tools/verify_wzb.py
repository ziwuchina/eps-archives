# -*- coding: utf-8 -*-
"""验证：WzExtBridge 被 EPS 加载 + 多次 $SDL 命令 + 模块状态"""
import frida, sys, time, os, io, ctypes
from ctypes import wintypes

PID = 16592
LOG = r'D:\EPS2026G\Temp\wz_ext_bridge.log'
user32 = ctypes.windll.user32

# 1. Frida 检查 WzExtBridge 模块
def check_module():
    try:
        session = frida.attach(PID)
        script = session.create_script("""
            'use strict';
            var found = [];
            Process.enumerateModules().forEach(function(m) {
                if (m.name.toLowerCase().indexOf('wzext') >= 0 || m.name.toLowerCase().indexOf('hello') >= 0) {
                    found.push({name: m.name, base: m.base.toString(), size: m.size, path: m.path});
                }
            });
            send({mods: found});
        """)
        res = []
        script.on('message', lambda m, d: res.append(m.get('payload') if m.get('type') == 'send' else m))
        script.load()
        time.sleep(2)
        session.detach()
        return res
    except Exception as e:
        return [{'err': str(e)}]

# 2. 发 $SDL 命令
def send_cmd(cmd):
    user32.SetForegroundWindow(723820)
    user32.SetFocus(1181706)
    time.sleep(0.05)
    user32.SendMessageW(1181706, 0x00B1, 0, -1)
    user32.SendMessageW(1181706, 0x00C2, 1, ctypes.c_wchar_p(""))
    user32.SendMessageW(1181706, 0x000C, 0, ctypes.c_wchar_p(cmd))
    time.sleep(0.05)
    user32.PostMessageW(1181706, 0x0100, 0x0D, 0)
    user32.PostMessageW(1181706, 0x0101, 0x0D, 0)
    time.sleep(0.1)
    user32.PostMessageW(1181706, 0x0102, 0x0D, 0)

def log_tail(n=6):
    if not os.path.exists(LOG): return []
    with io.open(LOG, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.read().splitlines()
    return lines[-n:]

print("=== module check ===")
for r in check_module():
    print(r)

# 先关可能的弹窗
import ctypes as ct

# 3. 发 3 次 $SDL 命令
print("\n=== send $SDL x3 ===")
for i in range(3):
    send_cmd('$SDL,WzExtBridge,WzExtProbe')
    time.sleep(3)
    print("iter %d done" % i)

print("\n=== log tail ===")
for l in log_tail(10):
    print(" ", l)

print("\n=== module check after ===")
for r in check_module():
    print(r)

print("\nprobe file:", os.path.exists(r'D:\EPS2026G\Temp\wz_ext_probe.txt'))
