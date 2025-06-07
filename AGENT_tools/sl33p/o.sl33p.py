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
import re
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


def extract_states(text: str) -> list[str]:
    """Return list of F33ling states encoded as 'symbol_name'."""
    if not text:
        return []
    return re.findall(r"\S+_\S+", text)


def parse_cultivate(path: Path) -> tuple[set[str], list[tuple[str, str]]]:
    """Parse cultivate links from z.CULTIVATE.md."""
    nodes: set[str] = set()
    edges: list[tuple[str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_yaml = False
    current: str | None = None
    reading = False

    for line in lines:
        if not in_yaml:
            if line.strip() == "---":
                in_yaml = True
            continue
        if line.startswith("  ") and not line.startswith("    "):
            current = None
            reading = False
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 4 and stripped.endswith(":") and stripped != "cultivate:":
            current = stripped[:-1]
            nodes.add(current)
            reading = False
        elif indent == 6 and stripped.startswith("cultivate:"):
            reading = True
        elif indent >= 8 and reading and stripped.startswith("- "):
            target = stripped[2:]
            if current:
                edges.append((current, target))
                nodes.add(target)
        elif indent <= 4:
            reading = False

    return nodes, edges


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
    start_time: datetime | None = None,
    commands: list[str] | None = None,
    states: list[str] | None = None,
    stategraph: dict | None = None,
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
    if start_time:
        record["start"] = start_time.isoformat(timespec="seconds")
        duration = datetime.utcnow() - start_time
        record["duration"] = int(duration.total_seconds())
    if commands:
        record["commands"] = commands
    if states:
        record["states"] = states
    if stategraph:
        record["stategraph"] = stategraph

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
    parser.add_argument("--start", type=str, default=None, help="ISO start time for duration")
    parser.add_argument("--command", dest="commands", action="append", help="Command run during session")
    parser.add_argument("--deep", action="store_true", help="Record extra context")
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
            narrative_i,
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

    start_env = os.getenv("SL33P_START") or os.getenv("SESSION_START")
    start_dt = None
    if args.start:
        try:
            start_dt = datetime.fromisoformat(args.start)
        except Exception:
            pass
    elif start_env:
        try:
            start_dt = datetime.fromisoformat(start_env)
        except Exception:
            pass

    cmds_env = os.getenv("SL33P_COMMANDS") or os.getenv("COMMANDS")
    cmds = args.commands or []
    if cmds_env:
        cmds += cmds_env.split()

    deep = args.deep or bool(os.getenv("SL33P_DEEP"))
    states = extract_states(assessment + "\n" + (narrative or "")) if deep else None
    stategraph = None
    if deep:
        cultivate_file = repo_root() / "z.CULTIVATE.md"
        try:
            nodes, edges = parse_cultivate(cultivate_file)
            stategraph = {"nodes": len(nodes), "edges": len(edges)}
        except Exception:
            stategraph = None

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
        start_time=start_dt,
        commands=cmds if cmds else None,
        states=states,
        stategraph=stategraph,
        dry_run=dry,
    ):
        if dry:
            print(f"Dry run complete for {ts}.json")
        else:
            print(f"Session recorded as {ts}.json")

if __name__ == "__main__":
    main()
