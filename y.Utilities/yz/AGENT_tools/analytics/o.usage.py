#!/usr/bin/env python3
"""Analyze usage of session record fields."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import subprocess


def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]


DATA_DIR = repo_root() / "y.Utilities" / "DATA"


FIELDS = [
    "aspects",
    "learning",
    "methodology",
    "framework_depth",
    "narrative",
    "optimization",
    "tetra",
]


def load_records() -> list[dict]:
    records = []
    if not DATA_DIR.exists():
        return records
    for path in DATA_DIR.glob("*.json"):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                records.append(data)
        except Exception:
            continue
    return records


def count_fields(records: list[dict]) -> dict:
    counts: Counter[str] = Counter()
    for rec in records:
        for field in FIELDS:
            if rec.get(field) is not None:
                counts[field] += 1
    return counts


def analyze() -> dict:
    records = load_records()
    total = len(records)
    usage = count_fields(records)
    return {"total_sessions": total, "usage": usage}


def save_summary(summary: dict) -> Path:
    out = DATA_DIR / "usage_summary.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return out


def main() -> None:
    summary = analyze()
    if not summary:
        print("No session data found.")
        return
    out_path = save_summary(summary)
    print("Field usage summary:")
    for key, val in summary["usage"].items():
        print(f"  {key}: {val}/{summary['total_sessions']}")
    print(f"Saved summary to {out_path}")


if __name__ == "__main__":
    main()
