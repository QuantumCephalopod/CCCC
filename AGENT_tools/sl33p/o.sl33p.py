#!/usr/bin/env python3
"""Session documentation tool using tetrahedral submodules."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure package imports work when executed directly
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from AGENT_tools.sl33p.x_input import prompt_user, extract_states
from AGENT_tools.sl33p.y_record import (
    sanitize,
    parse_json_field,
    build_record,
    next_timestamp,
)
from AGENT_tools.sl33p.z_persistence import (
    ensure_data_dir,
    save_record,
    parse_cultivate,
    repo_root,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Record session")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--start", type=str, default=None, help="ISO start time for duration")
    parser.add_argument("--command", dest="commands", action="append", help="Command run during session")
    parser.add_argument("--no-deep", action="store_true", help="Disable deep context logging")
    args = parser.parse_args()

    ensure_data_dir()
    ts = next_timestamp(repo_root() / "DATA")

    assessment = os.getenv("ASSESS")
    achievements = os.getenv("ACHIEVE")
    next_steps = os.getenv("NEXT")

    narrative = os.getenv("NARRATIVE")

    create = os.getenv("CREATE") or os.getenv("ASPECTS")
    copy = os.getenv("COPY") or os.getenv("LEARN")
    control = os.getenv("CONTROL") or os.getenv("METHOD") or os.getenv("OPTIM")
    cultivate = os.getenv("CULTIVATE") or os.getenv("DEPTH")
    optimization = os.getenv("OPTIM")

    if not all([
        assessment,
        achievements,
        next_steps,
        create,
        copy,
        control,
        cultivate,
        narrative,
    ]):
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

    deep = not args.no_deep and not os.getenv("SL33P_NO_DEEP")
    states = extract_states(assessment + "\n" + (narrative or "")) if deep else None
    stategraph = None
    if deep:
        cultivate_file = repo_root() / "z.CULTIVATE.md"
        try:
            nodes, edges = parse_cultivate(cultivate_file)
            stategraph = {"nodes": len(nodes), "edges": len(edges)}
        except Exception:
            stategraph = None

    record = build_record(
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
    )
    if save_record(record, dry_run=dry, timestamp=ts):
        if dry:
            print(f"Dry run complete for {ts}.json")
        else:
            print(f"Session recorded as {ts}.json")


if __name__ == "__main__":
    main()
