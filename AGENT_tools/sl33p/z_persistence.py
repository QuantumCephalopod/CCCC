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
        return Path(__file__).resolve().parents[2]


DATA_DIR = repo_root() / "DATA"


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
