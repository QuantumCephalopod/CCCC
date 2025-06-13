"""Persistence helpers for sl33p."""

from __future__ import annotations
import json
import subprocess
from pathlib import Path


def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[4]


DATA_DIR = repo_root() / "y.CONTROL" / "DATA"


def ensure_data_dir() -> None:
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)


def parse_cultivate(path: Path) -> tuple[set[str], list[tuple[str, str]]]:
    """Parse cultivate links from z.CULTIVATE.md."""
    nodes: set[str] = set()
    edges: list[tuple[str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_yaml = False
    current: str | None = None
    reading = False
    for line in lines:
        if not in_yaml:
            if line.strip() == "---":
                in_yaml = True
            continue
        if line.startswith("  ") and not line.startswith("    "):
            current = None
            reading = False
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 4 and stripped.endswith(":") and stripped != "cultivate:":
            current = stripped[:-1]
            nodes.add(current)
            reading = False
        elif indent == 6 and stripped.startswith("cultivate:"):
            reading = True
        elif indent >= 8 and reading and stripped.startswith("- "):
            target = stripped[2:]
            if current:
                edges.append((current, target))
                nodes.add(target)
        elif indent <= 4:
            reading = False
    return nodes, edges


def save_record(record: dict, dry_run: bool, timestamp: str) -> bool:
    file_path = DATA_DIR / f"{timestamp}.json"
    if dry_run:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        print("Dry run: record not written")
        return True
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            f.write("\n")
        git_commit(file_path, timestamp)
    except Exception as e:
        print(f"Failed to save record: {e}")
        return False
    return True


def git_commit(file_path: Path, ts: str) -> None:
    """Add the new record to git for persistence."""
    try:
        subprocess.run(["git", "add", str(file_path)], check=True)
        subprocess.run(["git", "commit", "-m", f"Record session {ts}"], check=True)
    except Exception as e:
        print(f"Git commit failed: {e}")


def append_delta(delta: dict) -> None:
    """Append prompt delta to COPY_deltas.json."""
    deltas_path = DATA_DIR / "COPY_deltas.json"
    try:
        if deltas_path.exists():
            with open(deltas_path, "r", encoding="utf-8") as f:
                arr = json.load(f)
        else:
            arr = []
    except Exception:
        arr = []
    arr.append(delta)
    try:
        with open(deltas_path, "w", encoding="utf-8") as f:
            json.dump(arr, f, ensure_ascii=False, indent=2)
            f.write("\n")
        subprocess.run(["git", "add", str(deltas_path)], check=True)
        subprocess.run(["git", "commit", "-m", "Update COPY deltas"], check=True)
    except Exception as e:
        print(f"Failed to store COPY delta: {e}")


def save_timeline_metrics() -> Path | None:
    """Write timeline metrics to DATA and commit the file."""
    import re
    from datetime import datetime

    def git_time(path: Path) -> datetime | None:
        try:
            out = subprocess.check_output(
                ["git", "log", "-1", "--format=%cI", str(path)], text=True
            )
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

    state_re = re.compile(r"\S+_\S+")

    def extract_state(text: str) -> str | None:
        if not text:
            return None
        m = state_re.search(text)
        if m:
            return m.group(0)
        return None

    def parse_time(ts: str) -> datetime | None:
        try:
            base = ts.split("_")[0]
            return datetime.strptime(base, "%Y%m%dT%H%M%SZ")
        except Exception:
            return None

    mapping: dict[str, dict[str, datetime | int]] = {}
    for rec in load_records():
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
    if not mapping:
        return None
    serializable = {
        state: {
            "first": info["first"].isoformat(),
            "last": info["last"].isoformat(),
            "count": info["count"],
        }
        for state, info in mapping.items()
    }
    out_path = DATA_DIR / "timeline_metrics.json"
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
            f.write("\n")
        subprocess.run(["git", "add", str(out_path)], check=True)
        subprocess.run(["git", "commit", "-m", "Update timeline metrics"], check=True)
    except Exception as e:
        print(f"Failed to save timeline metrics: {e}")
        return None
    return out_path
