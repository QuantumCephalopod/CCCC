#!/usr/bin/env python3
"""Session documentation tool using tetrahedral submodules."""

from __future__ import annotations

import argparse
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Ensure package imports work when executed directly
ROOT = Path(__file__).resolve().parents[3]
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

from AGENT_tools.sl33p.x_input import (
    prompt_agent,
    extract_states,
    parse_subgoals,
    parse_session_type,
)
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
    append_delta,
)
from AGENT_tools.chat import append_entry, CHAT_FILE
from AGENT_tools.copy_tools import suggest_prompt_adjustment


def main() -> None:
    parser = argparse.ArgumentParser(description="Record session")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--start", type=str, default=None, help="ISO start time for duration")
    parser.add_argument("--command", dest="commands", action="append", help="Command run during session")
    parser.add_argument("--no-deep", action="store_true", help="Disable deep context logging")
    parser.add_argument("--chat-in", type=str, default=None, help="User message to log")
    parser.add_argument("--chat-out", type=str, default=None, help="Assistant reply to log")
    parser.add_argument("--chat-limit", type=int, default=int(os.getenv("CHAT_LIMIT", 10)), help="Max chat messages to keep")
    args = parser.parse_args()

    ensure_data_dir()
    ts = next_timestamp(repo_root() / "DATA")

    assessment = os.getenv("ASSESS")
    achievements = os.getenv("ACHIEVE")
    next_steps = os.getenv("NEXT")

    narrative = os.getenv("NARRATIVE")

    subgoals_env = os.getenv("SUBGOALS")
    subgoals = parse_subgoals(subgoals_env) if subgoals_env else None

    sess_type_env = os.getenv("SESSION_TYPE") or os.getenv("TYPE")
    session_type = parse_session_type(sess_type_env) if sess_type_env else None

    create = os.getenv("CREATE") or os.getenv("ASPECTS")
    copy = os.getenv("COPY") or os.getenv("LEARN")
    control = os.getenv("CONTROL") or os.getenv("METHOD") or os.getenv("OPTIM")
    cultivate = os.getenv("CULTIVATE") or os.getenv("DEPTH")
    optimization = os.getenv("OPTIM")

    chat_in = args.chat_in or os.getenv("CHAT_IN")
    chat_out = args.chat_out or os.getenv("CHAT_OUT")
    chat_limit = args.chat_limit

    if not all([
        assessment,
        achievements,
        next_steps,
        create,
        copy,
        control,
        cultivate,
        narrative,
        subgoals,
        session_type,
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
            subgoals_i,
            session_type_i,
        ) = prompt_agent()
        assessment = assessment or assessment_i
        achievements = achievements or achievements_i
        next_steps = next_steps or next_steps_i
        create = create or create_i
        copy = copy or copy_i
        control = control or control_i
        cultivate = cultivate or cultivate_i
        narrative = narrative or narrative_i
        subgoals = parse_subgoals(subgoals_env) if subgoals_env else subgoals_i
        session_type = session_type or session_type_i

    if chat_in is None:
        chat_in = input("InputMessage to log: ")
    if chat_out is None:
        chat_out = input("OutputMessage to log: ")

    assessment = sanitize(assessment)
    achievements = sanitize(achievements)
    next_steps = sanitize(next_steps)
    create_val = parse_json_field(create)
    copy_val = sanitize(copy) if copy else None
    control_val = sanitize(control) if control else None
    cultivate_val = sanitize(cultivate) if cultivate else None
    narrative_val = sanitize(narrative) if narrative else None
    optimization_val = sanitize(optimization) if optimization else None
    chat_in_val = sanitize(chat_in) if chat_in else ""
    chat_out_val = sanitize(chat_out) if chat_out else ""
    session_type_val = sanitize(session_type) if session_type else None
    if subgoals:
        subgoals_val = [
            {
                "goal": sanitize(sg.get("goal", "")),
                "achieved": bool(sg.get("achieved")),
                "strategy_used": sanitize(sg.get("strategy_used", "")) or None,
            }
            for sg in subgoals
        ]
    else:
        subgoals_val = None

    prompt_update = None
    if "discordant" in assessment.lower():
        prompt_update = suggest_prompt_adjustment(
            assessment, achievements, narrative_val or ""
        )

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
        cultivate_file = repo_root() / "z.CULTIVATE" / "z.CULTIVATE.md"
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
        subgoals=subgoals_val,
        session_type=session_type_val,
        prompt_rewrite=prompt_update,
        optimization=optimization_val,
        start_time=start_dt,
        commands=cmds if cmds else None,
        states=states,
        stategraph=stategraph,
    )
    if save_record(record, dry_run=dry, timestamp=ts):
        if dry:
            print(f"Dry run complete for {ts}.json")
            print(f"Chat: {chat_in_val} -> {chat_out_val}")
        else:
            print(f"Session recorded as {ts}.json")
            append_entry(chat_in_val, chat_out_val, chat_limit)
            if prompt_update:
                append_delta({
                    "timestamp": ts,
                    "state": assessment,
                    "suggestion": prompt_update,
                })
            try:
                subprocess.run(["git", "add", str(CHAT_FILE)], check=True)
                subprocess.run(["git", "commit", "-m", "Update chat context"], check=True)
            except Exception as e:
                print(f"Failed to commit chat log: {e}")
            try:
                from AGENT_tools.sl33p.z_persistence import save_timeline_metrics

                save_timeline_metrics()
            except Exception as e:
                print(f"Failed to update timeline metrics: {e}")


if __name__ == "__main__":
    main()
