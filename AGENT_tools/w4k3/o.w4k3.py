#!/usr/bin/env python3
"""Session continuity loader.

Reads the 3 most recent session records from DATA folder and displays
previous achievements and focus areas.
"""

import json
import os
import subprocess
from pathlib import Path

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

def load_records(n=3):
    if not DATA_DIR.exists():
        print("DATA directory not found. No previous sessions recorded.")
        return []
    files = sorted(DATA_DIR.glob('*.json'), key=os.path.getmtime, reverse=True)
    records = []
    for file in files[:n]:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                records.append(json.load(f))
        except Exception as e:
            print(f"Failed to load {file.name}: {e}")
    return records

def display(records):
    if not records:
        print("No session history available.")
        return
   
    for rec in records:
        ts = rec.get("timestamp", "?")
        assessment = rec.get("assessment", "")
        ach = rec.get("achievements", "")
        nxt = rec.get("next", "")
        tetra = rec.get("tetra", {})
        if assessment:
            print(f"[{ts}] F33ling: {assessment}")
        else:
            print(f"[{ts}]")
        if ach:
            print(f"  Achieved: {ach}")
        if nxt:
            print(f"  Next: {nxt}")
        if tetra:
            for dim in ("create", "copy", "control", "cultivate"):
                if dim in tetra and tetra[dim]:
                    print(f"  {dim.capitalize()}: {tetra[dim]}")

def main():
    records = load_records()
    display(records)

if __name__ == "__main__":
    main()
