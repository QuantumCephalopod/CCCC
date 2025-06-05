#!/usr/bin/env python3
"""Session documentation tool.

Prompts for session state assessment, achievements, and next priorities,
then stores a JSON record in the DATA directory.
"""

import json
import os
from pathlib import Path
import subprocess

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

ASCII_LETTERS = list("abcdefghijklmnopqrstuvwxyz")

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
    letter = ASCII_LETTERS[count % len(ASCII_LETTERS)]
    cycle = count // len(ASCII_LETTERS) + 1
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
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        git_commit(file_path, timestamp)
    except Exception as e:
        print(f"Failed to save record: {e}")
        return False
    return True


def git_commit(file_path: Path, ts: str) -> None:
    """Add the new record to git for persistence."""
    try:
        subprocess.run(["git", "add", str(file_path)], check=True)
        subprocess.run([
            "git",
            "commit",
            "-m",
            f"Record session {ts}",
        ], check=True)
    except Exception as e:
        print(f"Git commit failed: {e}")
        
def main():
    ensure_data_dir()
    ts = next_timestamp()
    assessment, achievements, next_steps = prompt_user()
    if save_record(ts, assessment, achievements, next_steps):
        print(f"Session recorded as {ts}.json")

if __name__ == "__main__":
    main()
