# -*- coding: utf-8 -*-
"""
eps_com_runner.py - EPS2016 COM closed-loop production runner (233)

打通后的生产工具骨架：
  打开 ASCII 路径工程 -> 自动处理弹窗 -> 建对象 -> 存库 -> 关闭

用法:
  python eps_com_runner.py --edb D:\\eps_com_test\\work.edb --code 831000 \
      --points "1000.01,1000.34,22.45;1001.01,1000.34,22.45;1000.51,1001.34,22.45" \
      --name run001 --wait 5

关键约束:
  - edb 路径必须为 ASCII（COM 通道中文路径编码问题，见 EPS进展_233_20260908.md）
  - VBS 脚本以 GBK/ASCII 编码写入（已知坑：VBS 必须 GBK 编码）
  - 输出文件为 UTF-16（VBS 内 CreateTextFile(..., True, True)）
"""
import argparse
import os
import subprocess
import sys
import time
import ctypes
import threading

WRAPPER = r"D:\AIcode\mcpida\wrapper"
RESULTS = r"D:\AIcode\mcpida\reports"

USER32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)


def _get_text(hwnd):
    length = USER32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    USER32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def _get_class(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    USER32.GetClassNameW(hwnd, buf, 256)
    return buf.value


def _top_dialogs():
    """返回顶层 #32770 对话框列表 [(hwnd, title)]"""
    dialogs = []

    def cb(hwnd, lparam):
        if USER32.IsWindowVisible(hwnd):
            cls = _get_class(hwnd)
            if cls == '#32770':
                dialogs.append((hwnd, _get_text(hwnd)))
        return True

    USER32.EnumWindows(WNDENUMPROC(cb), 0)
    return dialogs


def _find_ok_button(dlg_hwnd):
    """在对话框内找标题为 '确定' 的 Button"""
    buttons = []

    def cb(hwnd, lparam):
        cls = _get_class(hwnd)
        if cls == 'Button':
            buttons.append((hwnd, _get_text(hwnd)))
        return True

    USER32.EnumChildWindows(dlg_hwnd, WNDENUMPROC(cb), 0)
    for h, t in buttons:
        if t == '确定':
            return h
    return None


def dismiss_dialogs_loop(stop_event, name):
    """自动关闭标题含 Eps/EPS 的模态弹窗（如 Load SSLBPTools.dll failed）"""
    while not stop_event.is_set():
        try:
            for dlg, title in _top_dialogs():
                if 'Eps' in title or 'EPS' in title:
                    btn = _find_ok_button(dlg)
                    if btn:
                        USER32.SendMessageW(btn, 0x00F5, 0, 0)  # BM_CLICK
                        print(f"[{name}] dialog dismissed: {title!r}", flush=True)
        except Exception as e:
            print(f"[{name}] dialog loop error: {e}", flush=True)
        time.sleep(0.5)


def build_vbs(edb_path, code, points, out_file, run_id):
    """生成闭环 VBS 脚本（ASCII 内容），返回脚本路径"""
    vbs_lines = [
        "' eps_com_runner generated - closed loop",
        "Option Explicit",
        "On Error Resume Next",
        "Dim epsApp, SSProcess",
        "Dim fso, out",
        "Set fso = CreateObject(\"Scripting.FileSystemObject\")",
        f"Set out = fso.CreateTextFile(\"{out_file}\", True, True)",
        "Err.Clear",
        "Set epsApp = CreateObject(\"Eps.EpsApplication\")",
        "If Err.Number <> 0 Then",
        "    out.WriteLine \"1 CreateObject ERR: \" & Err.Number & \" \" & Err.Description",
        "    out.Close: WScript.Quit 1",
        "End If",
        "out.WriteLine \"1 CreateObject OK\"",
        "Err.Clear",
        "epsApp.SetVisible 1",
        "out.WriteLine \"2 SetVisible err=\" & Err.Number",
        "Err.Clear",
        "Set SSProcess = epsApp.GetScriptDispatch(\"SScript.dll\", \"SSProcess\")",
        "If Err.Number <> 0 Then",
        "    out.WriteLine \"3 SSProcess ERR: \" & Err.Number & \" \" & Err.Description",
        "    out.Close: WScript.Quit 1",
        "End If",
        "out.WriteLine \"3 SSProcess OK\"",
        f"epsApp.InitWorkSpace \"{edb_path}\", \"\"",
        "out.WriteLine \"4 InitWorkSpace err=\" & Err.Number & \" \" & Err.Description",
        "WScript.Sleep 5000",
        "Err.Clear",
        "SSProcess.UpdateCurMap 0",
        "out.WriteLine \"5 UpdateCurMap err=\" & Err.Number",
        "Err.Clear",
        "SSProcess.PushUndoMark",
        "out.WriteLine \"6 PushUndoMark err=\" & Err.Number & \" \" & Err.Description",
        f"SSProcess.CreateNewObjByCode {code}",
        "out.WriteLine \"7 CreateNewObjByCode err=\" & Err.Number & \" \" & Err.Description",
    ]
    for i, (x, y, z) in enumerate(points, 1):
        vbs_lines.append(f"SSProcess.AddNewObjPoint {x}, {y}, {z}, 0, \"\"")
        vbs_lines.append(f"out.WriteLine \"8.{i} AddNewObjPoint err=\" & Err.Number")
    vbs_lines += [
        "SSProcess.AddNewObjToSaveObjList",
        "out.WriteLine \"9 AddNewObjToSaveObjList err=\" & Err.Number & \" \" & Err.Description",
        "SSProcess.SaveBufferObjToDatabase",
        "out.WriteLine \"10 SaveBufferObjToDatabase err=\" & Err.Number & \" \" & Err.Description",
        f"out.WriteLine \"RUN {run_id} COMPLETE\"",
        "out.Close",
        "WScript.Sleep 3000",
        "epsApp.CloseAllEdb",
        "WScript.Echo \"done\"",
    ]
    vbs_path = os.path.join(WRAPPER, f"eps_com_run_{run_id}.vbs")
    with open(vbs_path, 'w', encoding='ascii') as f:
        f.write('\r\n'.join(vbs_lines))
    return vbs_path


def main():
    parser = argparse.ArgumentParser(description="EPS2016 COM closed-loop runner")
    parser.add_argument("--edb", required=True, help="ASCII-path EDB workspace")
    parser.add_argument("--code", type=int, default=831000, help="object code (831000=elevation point)")
    parser.add_argument("--points", required=True, help="semicolon-separated x,y,z points")
    parser.add_argument("--name", default="run", help="run id")
    parser.add_argument("--wait", type=int, default=5, help="post-save wait seconds")
    args = parser.parse_args()

    if not os.path.exists(args.edb):
        print(f"ERROR: edb not found: {args.edb}")
        return 1
    if any(ord(c) > 127 for c in args.edb):
        print("ERROR: edb path must be ASCII-only (COM channel Chinese-path issue)")
        return 1

    points = []
    for p in args.points.split(';'):
        parts = p.strip().split(',')
        if len(parts) != 3:
            print(f"ERROR: bad point {p!r}, need x,y,z")
            return 1
        points.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))

    run_id = args.name
    out_file = os.path.join(WRAPPER, f"eps_com_run_{run_id}_out.txt")
    vbs_path = build_vbs(args.edb, args.code, points, out_file, run_id)
    print(f"VBS generated: {vbs_path}")
    print(f"Running closed loop on {args.edb} ...")

    stop_event = threading.Event()
    t = threading.Thread(target=dismiss_dialogs_loop, args=(stop_event, run_id), daemon=True)
    t.start()

    proc = subprocess.Popen(
        ["cscript", "//nologo", vbs_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    proc.wait(timeout=args.wait + 120)
    stop_event.set()
    t.join(timeout=2)

    stdout, stderr = proc.communicate()
    print("cscript stdout:", stdout.decode('utf-8', errors='replace').strip())
    if stderr:
        print("cscript stderr:", stderr.decode('utf-8', errors='replace').strip())

    if not os.path.exists(out_file):
        print("ERROR: output file not created")
        return 1
    with open(out_file, 'r', encoding='utf-16') as f:
        content = f.read()
    print("=== run output ===")
    print(content)
    print("==================")

    ok = 'COMPLETE' in content and 'err=0' in content
    print(f"RESULT: {'SUCCESS' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
