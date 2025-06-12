"""Utilities for loading session records."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path


def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]


def data_dir() -> Path:
    return repo_root() / "DATA"


def git_time(path: Path) -> datetime:
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
        return datetime.fromtimestamp(path.stat().st_mtime)


def load_records(limit: int) -> list[dict]:
    """Load up to `limit` recent session records."""
    ddir = data_dir()
    if not ddir.exists():
        print("DATA directory not found. No previous sessions recorded.")
        return []

    files = [
        f
        for f in ddir.glob("*.json")
        if f.name != "chat_context.json" and not f.name.endswith("_flow.json")
    ]
    recs_with_time = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                rec = json.load(f)
            if isinstance(rec, dict):
                rec["_file"] = file
                rec["_time"] = git_time(file)
                recs_with_time.append(rec)
        except Exception as e:
            print(f"Failed to load {file.name}: {e}")

    recs_with_time.sort(key=lambda r: r["_time"], reverse=True)
    return recs_with_time[:limit]
