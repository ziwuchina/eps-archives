# -*- coding: utf-8 -*-
"""验证已完成任务的证据文件 + 检查233当前环境状态"""
import os
import subprocess

files = [
    # 任务1: 步骤3 SDL/ERP闭环
    r"D:\AIcode\mcpida\reports\bar_v23_command_catalog.json",
    # 任务2: 分水岭
    r"D:\AIcode\mcpida\reports\frida_trace_vbs_args_20260414_205515.json",
    # 任务3: B阶段1
    r"D:\AIcode\mcpida\wrapper\probe_erp_login_v37_report.json",
    r"D:\AIcode\mcpida\wrapper\probe_worklist_net_v38_report.json",
    r"D:\AIcode\mcpida\wrapper\memory_notes_20260418.md",
    # 任务5: 步骤2.1
    r"D:\AIcode\mcpida\wrapper\stage2_p0_21_stability_evidence_20260418_1102.md",
    r"D:\AIcode\mcpida\wrapper\stage2_p0_21_run1_20260418_110231.json",
    r"D:\AIcode\mcpida\wrapper\stage2_p0_21_run2_20260418_110231.json",
    r"D:\AIcode\mcpida\wrapper\stage2_p0_21_run3_20260418_110231.json",
    # 任务6: 步骤2.2
    r"D:\AIcode\mcpida\wrapper\frida_wmcmd_context_probe.py",
    r"D:\AIcode\mcpida\wrapper\wmcmd_context_20260418_1224.json",
    r"D:\AIcode\mcpida\wrapper\stage2_22_wmcmd_context_evidence_20260418_1224.md",
    # 任务7: Frida稳定性
    r"D:\AIcode\mcpida\wrapper\frida_stable_full_probe.py",
    r"D:\AIcode\mcpida\wrapper\stable_full_20260418_1200_fix.json",
    # ERP SDK 现状
    r"D:\AIcode\mcpida\wrapper\eps_erp_api.py",
    r"D:\AIcode\mcpida\wrapper\eps_erp_api.py.bak_20260904",
    r"D:\AIcode\mcpida\reports\worklist_20260904.json",
    # 新进展相关
    r"C:\Users\Administrator\ghidra_scripts\hook_foshan.py",
    r"D:\EPS2026G\wzbridgeprobe.dll",
    r"D:\EPS2026G\WzExtBridge.dll",
    r"D:\佛顺数据数据\佛山数据.edb",
]

print("=== 证据文件检查 ===")
for f in files:
    print("EXIST" if os.path.exists(f) else "MISS ", f)

print()
print("=== EPS 进程检查 ===")
r = subprocess.run("tasklist /FI \"IMAGENAME eq EPS.exe\" /FO CSV", shell=True, capture_output=True, text=True, encoding="gbk", errors="replace")
print(r.stdout[:500])
# 更宽松的查找
r2 = subprocess.run("tasklist /FO CSV", shell=True, capture_output=True, text=True, encoding="gbk", errors="replace")
eps_lines = [l for l in r2.stdout.splitlines() if "EPS" in l.upper() or "eps" in l]
print("含EPS的进程行:", eps_lines if eps_lines else "无")

print()
print("=== 关键文件状态 ===")
for f in [r"D:\AIcode\mcpida\wrapper\eps_erp_api.py", r"D:\AIcode\mcpida\reports\worklist_20260904.json"]:
    if os.path.exists(f):
        print(f, os.path.getsize(f), "bytes, mtime:", __import__('datetime').datetime.fromtimestamp(os.path.getmtime(f)))
