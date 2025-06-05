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

GREEK_LETTERS = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ",
    "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ",
    "φ", "χ", "ψ", "ω"
]

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
