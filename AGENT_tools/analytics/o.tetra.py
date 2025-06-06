#!/usr/bin/env python3
"""Analyze tetrahedral dimension usage in session records."""

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


def load_sessions() -> list[dict]:
    records = []
    if not DATA_DIR.exists():
        return records
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            records.append(rec)
        except Exception:
            continue
    return records


DIMS = {
    "create": "aspects",
    "copy": "learning",
    "control": ["methodology", "optimization"],
    "cultivate": "framework_depth",
}


def analyze_dimensions() -> dict:
    sessions = load_sessions()
    if not sessions:
        return {}
    counts = {dim: 0 for dim in DIMS}
    for rec in sessions:
        if rec.get("aspects") is not None:
            counts["create"] += 1
        if rec.get("learning"):
            counts["copy"] += 1
        if rec.get("methodology") or rec.get("optimization"):
            counts["control"] += 1
        if rec.get("framework_depth"):
            counts["cultivate"] += 1
    total = len(sessions)
    fractions = {dim: round(counts[dim] / total, 2) for dim in counts}
    return {"total_sessions": total, "dimension_fractions": fractions}


def main() -> None:
    summary = analyze_dimensions()
    if not summary:
        print("No session data found.")
        return
    print("Tetrahedral Dimension Utilization:")
    print(f"Total sessions: {summary['total_sessions']}")
    for dim, val in summary["dimension_fractions"].items():
        print(f"  {dim}: {val * 100:.1f}%")


if __name__ == "__main__":
    main()
