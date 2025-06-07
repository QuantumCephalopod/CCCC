#!/usr/bin/env python3
"""Session continuity loader with summary.

Displays recent session records and aggregates dimension usage so
each new session begins with a clear sense of momentum.
"""

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Store all session records in the repository-level DATA directory
def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output([
            "git",
            "rev-parse",
            "--show-toplevel",
        ], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[2]


DATA_DIR = repo_root() / "DATA"


def git_time(path: Path) -> datetime:
    """Return the commit timestamp for the given file."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", str(path)], text=True
        )
        return datetime.fromisoformat(out.strip())
    except Exception:
        return datetime.fromtimestamp(path.stat().st_mtime)

def load_records(limit: int) -> list[dict]:
    if not DATA_DIR.exists():
        print("DATA directory not found. No previous sessions recorded.")
        return []

    files = list(DATA_DIR.glob("*.json"))
    recs_with_time = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                rec = json.load(f)
            rec["_file"] = file
            rec["_time"] = git_time(file)
            recs_with_time.append(rec)
        except Exception as e:
            print(f"Failed to load {file.name}: {e}")

    recs_with_time.sort(key=lambda r: r["_time"], reverse=True)
    return recs_with_time[:limit]

def display(records: list[dict]):
    if not records:
        print("No session history available.")
        return
   
    for rec in records:
        ts = rec.get("timestamp", "?")
        commit_time = rec.get("_time")
        assessment = rec.get("assessment", "")
        ach = rec.get("achievements", "")
        nxt = rec.get("next", "")
        tetra = rec.get("tetra", {})

        time_str = commit_time.isoformat(timespec="seconds") if commit_time else ""
        if assessment:
            print(f"[{ts}] {time_str} F33ling: {assessment}")
        else:
            print(f"[{ts}] {time_str}")

        if ach:
            print(f"  Achieved: {ach}")
        if nxt:
            print(f"  Next: {nxt}")
        if rec.get("narrative"):
            print(f"  Narrative: {rec['narrative']}")

        # Gather dimensional notes. Newer records may store data in the
        # `tetra` mapping while older ones use legacy top-level fields.
        def dim_value(name, legacy_key):
            val = None
            if tetra and tetra.get(name):
                val = tetra.get(name)
            elif rec.get(legacy_key):
                val = rec.get(legacy_key)
            return val

        dims = [
            ("create", "aspects"),
            ("copy", "learning"),
            ("control", "methodology"),
            ("cultivate", "framework_depth"),
        ]

        for dim, legacy in dims:
            val = dim_value(dim, legacy)
            if val:
                print(f"  {dim.capitalize()}: {val}")

        # Display optimization notes if present
        if rec.get("optimization"):
            print(f"  Optimization: {rec['optimization']}")

    print()


def extract_states(text: str) -> list[str]:
    """Return list of F33ling states encoded as 'symbol_name'."""
    if not text:
        return []
    return re.findall(r"\S+_\S+", text)


def display_transitions(records: list[dict]):
    """Show F33ling transitions between consecutive records."""
    if len(records) < 2:
        return

    print("F33ling transitions:")
    ordered = list(reversed(records))
    for prev, curr in zip(ordered, ordered[1:]):
        p_states = ", ".join(extract_states(prev.get("assessment", ""))) or "None"
        c_states = ", ".join(extract_states(curr.get("assessment", ""))) or "None"
        print(f"  {prev.get('timestamp', '?')} -> {curr.get('timestamp', '?')}: {p_states} -> {c_states}")
    print()


def summarize_all() -> None:
    """Print dimension usage counts across all session records."""
    if not DATA_DIR.exists():
        return
    counts = {"create": 0, "copy": 0, "control": 0, "cultivate": 0}
    total = 0
    for path in DATA_DIR.glob("*.json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)
        except Exception:
            continue
        total += 1
        tetra = rec.get("tetra", {})
        if rec.get("aspects") or tetra.get("create"):
            counts["create"] += 1
        if rec.get("learning") or tetra.get("copy"):
            counts["copy"] += 1
        if rec.get("methodology") or rec.get("optimization") or tetra.get("control"):
            counts["control"] += 1
        if rec.get("framework_depth") or tetra.get("cultivate"):
            counts["cultivate"] += 1

    if not total:
        return
    print("Tetrahedral dimension usage:")
    for dim, val in counts.items():
        frac = (val / total) * 100
        print(f"  {dim.capitalize()}: {val}/{total} ({frac:.0f}%)")

def main() -> None:
    parser = argparse.ArgumentParser(description="Display recent sessions")
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=5,
        help="Number of recent sessions to show",
    )
    parser.add_argument(
        "-t",
        "--transitions",
        action="store_true",
        help="Show F33ling transitions between sessions",
    )
    args = parser.parse_args()

    records = load_records(args.limit)
    display(records)
    if args.transitions:
        display_transitions(records)
    summarize_all()

if __name__ == "__main__":
    main()

