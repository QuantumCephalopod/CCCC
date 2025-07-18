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
def _repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        )
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]

ROOT = _repo_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

X_INPUT_PATH = ROOT / "y.Utilities" / "yy.CoreTools" / "yyz.sl33p" / "x_input.py"
_x_loader = SourceFileLoader("x_input", str(X_INPUT_PATH))
_x_spec = spec_from_loader("x_input", _x_loader)
x_mod = module_from_spec(_x_spec)
_x_loader.exec_module(x_mod)
prompt_agent = x_mod.prompt_agent
extract_states = x_mod.extract_states
parse_subgoals = x_mod.parse_subgoals
parse_session_type = x_mod.parse_session_type

Y_RECORD_PATH = ROOT / "y.Utilities" / "yy.CoreTools" / "yyz.sl33p" / "y_record.py"
_r_loader = SourceFileLoader("y_record", str(Y_RECORD_PATH))
_r_spec = spec_from_loader("y_record", _r_loader)
r_mod = module_from_spec(_r_spec)
_r_loader.exec_module(r_mod)
sanitize = r_mod.sanitize
parse_json_field = r_mod.parse_json_field
build_record = r_mod.build_record
next_timestamp = r_mod.next_timestamp

Z_PERSIST_PATH = ROOT / "y.Utilities" / "yy.CoreTools" / "yyz.sl33p" / "z_persistence.py"
_p_loader = SourceFileLoader("z_persistence", str(Z_PERSIST_PATH))
_p_spec = spec_from_loader("z_persistence", _p_loader)
p_mod = module_from_spec(_p_spec)
_p_loader.exec_module(p_mod)
ensure_data_dir = p_mod.ensure_data_dir
save_record = p_mod.save_record
parse_cultivate = p_mod.parse_cultivate
repo_root = p_mod.repo_root
append_delta = p_mod.append_delta



def suggest_prompt_adjustment(state: str, result: str, notes: str | None = None) -> str:
    """Return a simple prompt adjustment suggestion."""
    base = f"State `{state}` with result `{result}`"
    if notes:
        base += f" and notes `{notes}`"
    if "discordant" in state.lower():
        return base + " -> Consider shifting COPY focus toward reflective alignment."
    if "flux" in state.lower():
        return base + " -> Emphasize CONTROL for stability."
    return base + " -> Maintain current strategy, minor tweaks only."


def main() -> None:
    parser = argparse.ArgumentParser(description="Record session")
    parser.add_argument("--start", type=str, default=None, help="ISO start time for duration")
    parser.add_argument("--command", dest="commands", action="append", help="Command run during session")
    parser.add_argument("--no-deep", action="store_true", help="Disable deep context logging")
    args = parser.parse_args()

    ensure_data_dir()
    ts = next_timestamp(repo_root() / "y.Utilities" / "yx.DataArchive")

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


    assessment = sanitize(assessment)
    achievements = sanitize(achievements)
    next_steps = sanitize(next_steps)
    create_val = parse_json_field(create)
    copy_val = sanitize(copy) if copy else None
    control_val = sanitize(control) if control else None
    cultivate_val = sanitize(cultivate) if cultivate else None
    narrative_val = sanitize(narrative) if narrative else None
    optimization_val = sanitize(optimization) if optimization else None
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
        cultivate_file = repo_root() / "z.Research" / "AGENT.md"
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
    if save_record(record, timestamp=ts):
        print(f"Session recorded as {ts}.json")
        if prompt_update:
            append_delta({
                "timestamp": ts,
                "state": assessment,
                "suggestion": prompt_update,
            })
        try:
            p_mod.save_timeline_metrics()
        except Exception as e:
            print(f"Failed to update timeline metrics: {e}")


if __name__ == "__main__":
    main()
