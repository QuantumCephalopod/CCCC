#!/usr/bin/env python3
"""Session documentation tool.

Prompts for session state assessment, achievements, next priorities and
other context details, then stores a JSON record in the DATA directory.
The JSON structure can now include additional optional fields capturing
aspect mappings, methodology notes, learning insights, framework depth and
performance optimization ideas. Older fields remain unchanged so previous
tools continue to operate.
"""

import argparse
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

def sanitize(text: str) -> str:
    """Remove non-printable characters and surrounding whitespace."""
    return "".join(ch for ch in text.strip() if ch.isprintable())


def parse_json_field(text: str):
    """Attempt to parse a field as JSON; fall back to sanitized string."""
    if text is None:
        return None
    cleaned = text.strip()
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except Exception:
        return sanitize(cleaned)


def prompt_user():
    print("Provide F33ling state assessment as described in x.COPY.md")
    assessment = input("State assessment: ")
    achievements = input("Main achievements: ")
    next_steps = input("Next session priorities: ")
    aspects = input("Detailed aspect mappings (JSON or text, optional): ")
    methodology = input("Methodology patterns (optional): ")
    learning = input("Learning discoveries (optional): ")
    depth = input("Framework utilization depth (optional): ")
    optimization = input("Performance optimization insights (optional): ")
    return (
        assessment,
        achievements,
        next_steps,
        aspects,
        methodology,
        learning,
        depth,
        optimization,
    )

def save_record(
    timestamp,
    assessment,
    achievements,
    next_steps,
    aspects=None,
    methodology=None,
    learning=None,
    depth=None,
    optimization=None,
    dry_run=False,
):
    record = {
        "timestamp": timestamp,
        "assessment": assessment,
        "achievements": achievements,
        "next": next_steps,
    }
    if aspects is not None:
        record["aspects"] = aspects
    if methodology:
        record["methodology"] = methodology
    if learning:
        record["learning"] = learning
    if depth:
        record["framework_depth"] = depth
    if optimization:
        record["optimization"] = optimization
    file_path = DATA_DIR / f"{timestamp}.json"
    if dry_run:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        print("Dry run: record not written")
        return True
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
    parser = argparse.ArgumentParser(description="Record session")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    ensure_data_dir()
    ts = next_timestamp()

    assessment = os.getenv("ASSESS")
    achievements = os.getenv("ACHIEVE")
    next_steps = os.getenv("NEXT")
    aspects = os.getenv("ASPECTS")
    methodology = os.getenv("METHOD")
    learning = os.getenv("LEARN")
    depth = os.getenv("DEPTH")
    optimization = os.getenv("OPTIM")

    if not (assessment and achievements and next_steps):
        (
            assessment_i,
            achievements_i,
            next_steps_i,
            aspects_i,
            methodology_i,
            learning_i,
            depth_i,
            optimization_i,
        ) = prompt_user()
        assessment = assessment or assessment_i
        achievements = achievements or achievements_i
        next_steps = next_steps or next_steps_i
        aspects = aspects or aspects_i
        methodology = methodology or methodology_i
        learning = learning or learning_i
        depth = depth or depth_i
        optimization = optimization or optimization_i

    assessment = sanitize(assessment)
    achievements = sanitize(achievements)
    next_steps = sanitize(next_steps)
    aspects_val = parse_json_field(aspects)
    methodology_val = sanitize(methodology) if methodology else None
    learning_val = sanitize(learning) if learning else None
    depth_val = sanitize(depth) if depth else None
    optimization_val = sanitize(optimization) if optimization else None

    dry = args.dry_run or os.getenv("SL33P_DRY_RUN")

    if save_record(
        ts,
        assessment,
        achievements,
        next_steps,
        aspects=aspects_val,
        methodology=methodology_val,
        learning=learning_val,
        depth=depth_val,
        optimization=optimization_val,
        dry_run=dry,
    ):
        if dry:
            print(f"Dry run complete for {ts}.json")
        else:
            print(f"Session recorded as {ts}.json")

if __name__ == "__main__":
    main()
