# -*- coding: utf-8 -*-
"""233: 验证用户实际用的 EPS2016 目录完好 + 对比两个目录"""
import os, glob

# 用户实际用的目录（Eps快捷.lnk 指向）
actual = None
for d in os.listdir('D:\\'):
    if d.startswith('EPS2016') and 'FS2K' in d:
        actual = os.path.join('D:\\', d)
        break

print("actual dir:", repr(actual))
if actual:
    print("exists:", os.path.isdir(actual))
    print("Eps.exe:", os.path.exists(os.path.join(actual, 'Eps.exe')))
    print("EpsGlobal.ini:", os.path.exists(os.path.join(actual, 'EpsGlobal.ini')))
    print("Hello.SDL:", os.path.exists(os.path.join(actual, 'Hello.SDL')))
    print("WzExtBridge.SDL:", os.path.exists(os.path.join(actual, 'WzExtBridge.SDL')))
    print("nethasp.ini:", os.path.exists(os.path.join(actual, 'nethasp.ini')))
    n = len(os.listdir(actual))
    print("file count:", n)
    # 列出根目录所有 SDL
    sdls = [f for f in os.listdir(actual) if f.lower().endswith('.sdl')]
    print("SDL count:", len(sdls))
    print("  ", sdls[:15])

print("\n=== mis-moved dir (EPS2016Shunde) ===")
dst = r'D:\EPS2016Shunde'
print("nethasp.ini:", os.path.exists(os.path.join(dst, 'nethasp.ini')))
print("Hello.SDL:", os.path.exists(os.path.join(dst, 'Hello.SDL')))
print("WzExtBridge.SDL:", os.path.exists(os.path.join(dst, 'WzExtBridge.SDL')))
print("Eps.exe:", os.path.exists(os.path.join(dst, 'Eps.exe')))

# 对比两个目录的 Eps.exe 大小（判断是否同版本）
print("\n=== compare Eps.exe ===")
for label, d in [('actual', actual), ('mismoved', dst)]:
    if d:
        p = os.path.join(d, 'Eps.exe')
        if os.path.exists(p):
            print(label, os.path.getsize(p), "bytes")
