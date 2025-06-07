#!/usr/bin/env python3
"""Session documentation tool.

Prompts for session state assessment, achievements, a moment narrative,
and next priorities,
then stores a JSON record in the DATA directory. The data model now
explicitly supports the tetrahedral workflow dimensions (CREATE, COPY,
CONTROL, CULTIVATE). Older fields remain supported so previous tools can
operate without modification.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
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

ASCII_LETTERS = list("abcdefghijklmnopqrstuvwxyz")

def current_time_stamp() -> str:
    """Return an ISO style timestamp for filenames."""
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

def ensure_data_dir():
    if not DATA_DIR.exists():
        try:
            DATA_DIR.mkdir(parents=True)
        except Exception as e:
            print(f"Failed to create DATA directory: {e}")
            raise SystemExit(1)

def next_timestamp() -> str:
    files = sorted(DATA_DIR.glob('*.json'))
    count = len(files)
    letter = ASCII_LETTERS[count % len(ASCII_LETTERS)]
    cycle = count // len(ASCII_LETTERS) + 1
    prefix = current_time_stamp()
    return f"{prefix}_{letter}{cycle}"

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
    create = input(
        "CREATE dimension notes (innovation, problem identification, optional): "
    )
    copy = input(
        "COPY dimension notes (learning, pattern recognition, optional): "
    )
    control = input(
        "CONTROL dimension notes (methodology, optimization, optional): "
    )
    cultivate = input(
        "CULTIVATE dimension notes (growth insights, optional): "
    )
    narrative = input(
        "Moment narrative (short description in sentences, optional): "
    )
    return (
        assessment,
        achievements,
        next_steps,

        create,
        copy,
        control,
        cultivate,
        narrative,
    )

def save_record(
    timestamp,
    assessment,
    achievements,
    next_steps,
    create=None,
    copy=None,
    control=None,
    cultivate=None,
    narrative=None,
    optimization=None,
    dry_run=False,
):
    record = {
        "timestamp": timestamp,
        "assessment": assessment,
        "achievements": achievements,
        "next": next_steps,
    }
    tetra = {}
    if create is not None:
        record["aspects"] = create
        tetra["create"] = create
    if copy is not None:
        record["learning"] = copy
        tetra["copy"] = copy
    if control is not None:
        record["methodology"] = control
        tetra["control"] = control
    if cultivate is not None:
        record["framework_depth"] = cultivate
        tetra["cultivate"] = cultivate
    if narrative is not None:
        record["narrative"] = narrative
    if tetra:
        record["tetra"] = tetra
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

    narrative = os.getenv("NARRATIVE")

    create = os.getenv("CREATE") or os.getenv("ASPECTS")
    copy = os.getenv("COPY") or os.getenv("LEARN")
    control = os.getenv("CONTROL") or os.getenv("METHOD") or os.getenv("OPTIM")
    cultivate = os.getenv("CULTIVATE") or os.getenv("DEPTH")
    optimization = os.getenv("OPTIM")

    if not (assessment and achievements and next_steps):
        (
            assessment_i,
            achievements_i,
            next_steps_i,
            create_i,
            copy_i,
            control_i,
            cultivate_i,
        ) = prompt_user()
        assessment = assessment or assessment_i
        achievements = achievements or achievements_i
        next_steps = next_steps or next_steps_i
        create = create or create_i
        copy = copy or copy_i
        control = control or control_i
        cultivate = cultivate or cultivate_i
        narrative = narrative or narrative_i

    assessment = sanitize(assessment)
    achievements = sanitize(achievements)
    next_steps = sanitize(next_steps)
    create_val = parse_json_field(create)
    copy_val = sanitize(copy) if copy else None
    control_val = sanitize(control) if control else None
    cultivate_val = sanitize(cultivate) if cultivate else None
    narrative_val = sanitize(narrative) if narrative else None
    optimization_val = sanitize(optimization) if optimization else None

    dry = args.dry_run or os.getenv("SL33P_DRY_RUN")

    if save_record(
        ts,
        assessment,
        achievements,
        next_steps,
        create=create_val,
        copy=copy_val,
        control=control_val,
        cultivate=cultivate_val,
        narrative=narrative_val,
        optimization=optimization_val,
        dry_run=dry,
    ):
        if dry:
            print(f"Dry run complete for {ts}.json")
        else:
            print(f"Session recorded as {ts}.json")

if __name__ == "__main__":
    main()
