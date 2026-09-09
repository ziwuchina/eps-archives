# -*- coding: utf-8 -*-
"""wzext_probe.py - WzExtBridge.SDL 调用链静态验证(233)"""
import pefile, capstone, json, datetime

P = r"D:\EPS2016Shunde\WzExtBridge.SDL"
pe = pefile.PE(P)

def get_export_rva(name):
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if e.name and e.name.decode() == name:
            return e.address
    return None

rva = get_export_rva("WzExtProbe")
print("WzExtProbe RVA:", hex(rva) if rva else None)

# 反汇编 WzExtProbe 入口 120 字节
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
if rva:
    data = pe.get_memory_mapped_image()[rva:rva + 160]
    print("--- WzExtProbe 前 24 条指令 ---")
    for ins in md.disasm(data, pe.OPTIONAL_HEADER.ImageBase + rva):
        print(f"  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}")
        if ins.address - (pe.OPTIONAL_HEADER.ImageBase + rva) > 90:
            break

# 字符串扫描：RegisterCmd / SDL 相关
import re
img = pe.get_memory_mapped_image()
strs = set()
for m in re.finditer(rb"[ -~]{6,}", img):
    s = m.group().decode("ascii", "ignore")
    strs.add(s)
kw = [s for s in strs if any(k in s for k in ("Cmd", "SDL", "Probe", "Register", "Execute", "Interface"))]
print("\n--- 关键字符串（去重前 40 个）---")
for s in sorted(kw)[:40]:
    print("  ", s)

print("\nPE 元数据:")
print("  Machine:", hex(pe.FILE_HEADER.Machine))
print("  ImageBase:", hex(pe.OPTIONAL_HEADER.ImageBase))
print("  DllCharacteristics:", hex(pe.OPTIONAL_HEADER.DllCharacteristics),
      "(ASLR:", bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x40), ")")
print("  时间戳:", datetime.datetime.utcfromtimestamp(pe.FILE_HEADER.TimeDateStamp))
print("  Subsystem:", pe.OPTIONAL_HEADER.Subsystem, "(2=GUI)")
