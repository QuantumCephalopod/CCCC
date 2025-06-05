#!/usr/bin/env python3
"""Session documentation tool.

Prompts for session state assessment, achievements, and next priorities,
then stores a JSON record in the DATA directory.
"""

import json
import os
from pathlib import Path

# Use the parent AGENT_tools/DATA directory so this tool shares history
# with other utilities regardless of its own folder.
DATA_DIR = Path(__file__).resolve().parents[1] / "DATA"

GREEK_LETTERS = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ",
    "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ",
    "φ", "χ", "ψ", "ω"
]

def ensure_data_dir():
    if not DATA_DIR.exists():
        try:
            DATA_DIR.mkdir(parents=True)
        except Exception as e:
            print(f"Failed to create DATA directory: {e}")
            raise SystemExit(1)

def next_timestamp():
    files = sorted(DATA_DIR.glob('*.json'))
    count = len(files)
    letter = GREEK_LETTERS[count % len(GREEK_LETTERS)]
    cycle = count // len(GREEK_LETTERS) + 1
    return f"{letter}{cycle}"

def prompt_user():
    print("Provide F33ling state assessment as described in x.COPY.md")
    assessment = input("State assessment: ")
    achievements = input("Main achievements: ")
    next_steps = input("Next session priorities: ")
    return assessment, achievements, next_steps

def save_record(timestamp, assessment, achievements, next_steps):
    record = {
        "timestamp": timestamp,
        "assessment": assessment,
        "achievements": achievements,
        "next": next_steps,
    }
    file_path = DATA_DIR / f"{timestamp}.json"
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save record: {e}")
        return False
    return True

def main():
    ensure_data_dir()
    ts = next_timestamp()
    assessment, achievements, next_steps = prompt_user()
    if save_record(ts, assessment, achievements, next_steps):
        print(f"Session recorded as {ts}.json")

if __name__ == "__main__":
    main()
