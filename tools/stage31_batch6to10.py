# -*- coding: utf-8 -*-
"""stage31_batch6to10.py - 阶段3.1 批6-10：SSProcess 剩余 5 批全量分析（官方帮助目录直读）(233)
批6 数据库操作 / 批7 数据整理 / 批8 系统设置+图幅打印 / 批9 选择集+地模+外部函数 / 批10 工程管理+数据转换+数据检查+坐标转换+角度
"""
import os, re, json, html as ihtml

BASE = r"D:\AIcode\mcpida\eps_script_help\语言参考\SSProcess对象参考"
OUT_DIR = r"D:\AIcode\mcpida\reports"

BATCHES = {
    "batch6_db": ["数据库操作"],
    "batch7_arrange": ["数据整理"],
    "batch8_sys_print": ["系统设置", "图幅与打印"],
    "batch9_sel_dem_ext": ["选择集操作", "地模处理", "外部函数"],
    "batch10_misc": ["工程管理", "数据转换", "数据检查", "坐标转换", "角度函数"],
}

def parse_page(path):
    name = os.path.basename(path)
    if not name.endswith("函数.htm"):
        return None  # 目录页/索引页
    fname = name[: -len("函数.htm")]
    raw = open(path, "rb").read()
    t = None
    for enc in ("gb18030", "gbk", "utf-8"):
        try:
            t = raw.decode(enc)
            break
        except Exception:
            continue
    if t is None:
        return None
    t = re.sub(r"<[^>]+>", " ", t)
    t = ihtml.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    # 签名：标题区第一个 "Name( args )" 模式
    m = re.search(re.escape(fname) + r"\s*\(\s*([^)]{0,250})\)", t)
    sig = f"{fname}({m.group(1)})" if m else fname + "(...)"
    # 说明：'说明' 到 '示例' 之间
    desc = ""
    dm = re.search(r"说明\s*(.{0,500}?)\s*示例", t)
    if dm:
        desc = dm.group(1).strip()
    elif "说明" in t:
        desc = t.split("说明", 1)[1][:300].strip()
    return {"name": fname, "signature": sig[:160], "desc": desc[:300],
            "snippet": t[:600]}

def main():
    summary = {}
    for batch, dirs in BATCHES.items():
        items = []
        for d in dirs:
            p = os.path.join(BASE, d)
            for fn in sorted(os.listdir(p)):
                if not fn.endswith(".htm"):
                    continue
                it = parse_page(os.path.join(p, fn))
                if it:
                    it["class"] = "SSProcess"
                    it["section"] = d
                    items.append(it)
        json_path = os.path.join(OUT_DIR, f"stage31_{batch}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"task": f"阶段3.1 {batch}：{'+'.join(dirs)}",
                       "date": "2026-09-09", "count": len(items),
                       "functions": items}, f, ensure_ascii=False, indent=2)
        summary[batch] = len(items)
        print(f"{batch}: {len(items)} 函数 -> {json_path}")
    print("TOTAL:", sum(summary.values()))

if __name__ == "__main__":
    main()
