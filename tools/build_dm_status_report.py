import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

START = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
END = datetime.now(timezone.utc)

ROOT = Path(r"C:\Users\Administrator\.openclaw")
OUT_DIR = Path(r"C:\Users\Administrator\.openclaw\workspace-main\eps-archives\reports\dm-status")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_SENDERS = {
    "main": {
        "ou_a5e1f2895be8502f4f09642711b78100",
        "ou_a29189ce048c287392cd9815c2b308ab",
    },
    "peiqian": {
        "ou_a29189ce048c287392cd9815c2b308ab",
        "ou_a5e1f2895be8502f4f09642711b78100",
    },
}

SUCCESS_RE = re.compile(
    r"(成功|完成|已完成|通过|已修复|恢复|正常|PASS|DONE|resolved|fixed|ok|OK|✅)",
    re.IGNORECASE,
)
FAIL_RE = re.compile(
    r"(失败|报错|error|Error|ERROR|BLOCKED|停摆|超时|timeout|未通过|无法|卡住|429|400|冲突|Exception|❌|未命中)",
    re.IGNORECASE,
)
PITFALL_RE = re.compile(r"(避坑|教训|风险|注意|坑点|提醒)")
ABS_PATH_RE = re.compile(r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]+")
MSG_ID_RE = re.compile(r"\[message_id:\s*([^\]]+)\]")


def parse_ts(ts: str):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def extract_text(content: Any) -> str:
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(p for p in parts if p)
    return ""


def classify(text: str, error_message: str = "") -> str:
    merged = (text or "") + "\n" + (error_message or "")
    has_success = bool(SUCCESS_RE.search(merged))
    has_fail = bool(FAIL_RE.search(merged))
    has_pitfall = bool(PITFALL_RE.search(merged))
    if has_success and has_fail:
        return "mixed"
    if has_fail:
        return "failure"
    if has_success:
        return "success"
    if has_pitfall:
        return "pitfall"
    return "other"


def scan_agent(agent: str) -> Dict[str, Any]:
    session_dir = ROOT / "agents" / agent / "sessions"
    records: List[Dict[str, Any]] = []
    scanned_files = []

    for file in sorted(session_dir.glob("*.jsonl*")):
        if file.name == "sessions.json":
            continue
        if file.suffix.lower() == ".json":
            continue

        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue

        if not lines:
            continue

        parsed = []
        dm_user_hits = 0
        for idx, line in enumerate(lines, start=1):
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("type") != "message":
                continue
            msg = obj.get("message", {})
            role = msg.get("role")
            text = extract_text(msg.get("content", []))
            if role == "user":
                if (
                    "Conversation info (untrusted metadata):" in text
                    and any(sender in text for sender in TARGET_SENDERS[agent])
                ):
                    dm_user_hits += 1
            parsed.append((idx, obj, text))

        # Only keep true DM threads with explicit inbound conversation envelope.
        if dm_user_hits == 0:
            continue

        scanned_files.append(str(file))
        last_user_message_id = ""

        for idx, obj, cached_text in parsed:
            ts = parse_ts(obj.get("timestamp", ""))
            if not ts or ts < START or ts > END:
                continue

            msg = obj.get("message", {})
            role = msg.get("role")

            if role == "user":
                text = cached_text
                m = MSG_ID_RE.search(text)
                if m:
                    last_user_message_id = m.group(1)
                continue

            if role != "assistant":
                continue

            text = extract_text(msg.get("content", []))
            err = msg.get("errorMessage", "")
            status = classify(text, err)

            abs_paths = sorted(set(ABS_PATH_RE.findall((text or "") + "\n" + (err or ""))))

            records.append(
                {
                    "agent": agent,
                    "timestamp": ts.isoformat(),
                    "status": status,
                    "message_id": last_user_message_id,
                    "source_file": str(file),
                    "source_line": idx,
                    "error": err,
                    "text": text,
                    "absolute_paths": abs_paths,
                }
            )

    # Keep only status-bearing records for final summary export; all records go full export.
    status_records = [
        r for r in records if r["status"] in {"success", "failure", "mixed", "pitfall"}
    ]

    return {
        "agent": agent,
        "scanned_files": scanned_files,
        "all_records": records,
        "status_records": status_records,
    }


def write_json(path: Path, data: Any):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_markdown(main_data: Dict[str, Any], peiqian_data: Dict[str, Any]) -> str:
    now_local = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    lines = []
    lines.append("# EPS DM状态汇总（2026-04-01 至当前）")
    lines.append("")
    lines.append(f"- 生成时间: {now_local}")
    lines.append("- 时间窗口: 2026-04-01 00:00:00 UTC 至当前")
    lines.append("- 口径: 仅统计 assistant 在私聊会话中的状态类回报（success/failure/mixed/pitfall）")
    lines.append("")

    for data in (main_data, peiqian_data):
        status_records = data["status_records"]
        lines.append(f"## Agent: {data['agent']}")
        lines.append("")
        lines.append(f"- 扫描文件数: {len(data['scanned_files'])}")
        lines.append(f"- 状态记录数: {len(status_records)}")
        if data["scanned_files"]:
            lines.append("- 扫描文件(绝对路径):")
            for fp in data["scanned_files"]:
                lines.append(f"  - `{fp}`")
        else:
            lines.append("- 扫描文件(绝对路径): 无")
        lines.append("")

        if not status_records:
            lines.append("- 未发现状态类回报记录")
            lines.append("")
            continue

        lines.append("| 时间(UTC) | 状态 | message_id | 来源文件 | 行号 | 摘要 |")
        lines.append("|---|---|---|---|---:|---|")
        for r in status_records:
            summary = (r["text"] or r["error"] or "").replace("\n", " ").strip()
            summary = summary[:120].replace("|", "\\|")
            lines.append(
                f"| {r['timestamp']} | {r['status']} | {r['message_id'] or '-'} | `{r['source_file']}` | {r['source_line']} | {summary} |"
            )
        lines.append("")

        all_paths = sorted({p for r in status_records for p in r.get("absolute_paths", [])})
        lines.append("### 记录中提及的绝对路径")
        if all_paths:
            for p in all_paths:
                lines.append(f"- `{p}`")
        else:
            lines.append("- 无")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    main_data = scan_agent("main")
    peiqian_data = scan_agent("peiqian")

    write_json(OUT_DIR / "main-all-records.json", main_data["all_records"])
    write_json(OUT_DIR / "main-status-records.json", main_data["status_records"])
    write_json(OUT_DIR / "peiqian-all-records.json", peiqian_data["all_records"])
    write_json(OUT_DIR / "peiqian-status-records.json", peiqian_data["status_records"])

    manifest = {
        "window_utc": {
            "start": START.isoformat(),
            "end": END.isoformat(),
        },
        "sources": {
            "main": main_data["scanned_files"],
            "peiqian": peiqian_data["scanned_files"],
        },
        "counts": {
            "main_all": len(main_data["all_records"]),
            "main_status": len(main_data["status_records"]),
            "peiqian_all": len(peiqian_data["all_records"]),
            "peiqian_status": len(peiqian_data["status_records"]),
        },
    }
    write_json(OUT_DIR / "manifest.json", manifest)

    md = build_markdown(main_data, peiqian_data)
    (OUT_DIR / "dm-status-summary.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
