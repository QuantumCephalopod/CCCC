"""Analyze first and last appearances of F33ling states."""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
import subprocess


def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]


DATA_DIR = repo_root() / "y.Utilities" / "yx.DataArchive"


def git_time(path: Path) -> datetime | None:
    """Return the commit timestamp for the given file."""
    try:
        out = subprocess.check_output([
            "git",
            "log",
            "-1",
            "--format=%cI",
            str(path),
        ], text=True)
        return datetime.fromisoformat(out.strip())
    except Exception:
        return None


def load_records() -> list[dict]:
    records = []
    if not DATA_DIR.exists():
        return records
    for path in DATA_DIR.glob("*.json"):
        if path.name == "chat_context.json" or path.name.endswith("_flow.json"):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            rec["_file"] = path
            rec["_time"] = git_time(path)
            records.append(rec)
        except Exception:
            continue
    return records


STATE_RE = re.compile(r"\S+_\S+")


def extract_state(text: str) -> str | None:
    if not text:
        return None
    match = STATE_RE.search(text)
    if match:
        return match.group(0)
    return None


def parse_time(ts: str) -> datetime | None:
    try:
        base = ts.split("_")[0]
        return datetime.strptime(base, "%Y%m%dT%H%M%SZ")
    except Exception:
        return None


def analyze() -> dict[str, dict[str, datetime | int]]:
    records = load_records()
    mapping: dict[str, dict[str, datetime | int]] = {}
    for rec in records:
        state = extract_state(rec.get("assessment", ""))
        if not state:
            continue
        dt = rec.get("_time") or parse_time(rec.get("timestamp", ""))
        if not dt:
            continue
        info = mapping.setdefault(state, {"first": dt, "last": dt, "count": 0})
        if dt < info["first"]:
            info["first"] = dt
        if dt > info["last"]:
            info["last"] = dt
        info["count"] = int(info.get("count", 0)) + 1
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="F33ling state timeline")
    parser.add_argument(
        "--sort",
        choices=["first", "last"],
        default="first",
        help="Sort by first or last occurrence",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of states displayed",
    )
    args = parser.parse_args()

    mapping = analyze()
    if not mapping:
        print("No session data found.")
        return

    ordered = sorted(mapping.items(), key=lambda x: x[1][args.sort])
    if args.limit:
        ordered = ordered[: args.limit]

    for state, info in ordered:
        first = info["first"].isoformat()
        last = info["last"].isoformat()
        count = info["count"]
        print(f"{state}: {first} -> {last} ({count})")


if __name__ == "__main__":
    main()
