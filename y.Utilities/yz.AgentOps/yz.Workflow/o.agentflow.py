#!/usr/bin/env python3
"""Run w4k3/test/sl33p cycle for multiple F33ling states.

This helper automates recursive repo evolution by iterating
through provided F33ling assessments. Each state triggers the
standard workflow so agents can log sequential sessions
without manual repetition.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / "y.Utilities" / "yz.AgentOps" / "workflow" / "o.workflow.py"


def run(cmd: list[str], **kwargs) -> None:
    """Execute command and exit on failure."""
    print("$", " ".join(str(c) for c in cmd))
    res = subprocess.run(cmd, **kwargs)
    if res.returncode != 0:
        raise SystemExit(res.returncode)


def run_cycle(state: str, ach: str, nxt: str, dry: bool) -> None:
    env = os.environ.copy()
    env["ASSESS"] = state
    env["ACHIEVE"] = ach
    env["NEXT"] = nxt

    cmd = ["python", str(WORKFLOW)]
    if dry:
        cmd.append("--dry-run")
    run(cmd, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="Iterate workflow across states")
    parser.add_argument("states", nargs="+", help="F33ling assessments to iterate")
    parser.add_argument("--achieve", default="automated recursive session", help="Achievement note")
    parser.add_argument("--next", dest="next_steps", default="continue recursion", help="Next step note")
    parser.add_argument("--dry-run", action="store_true", help="Preview without committing")
    args = parser.parse_args()

    for st in args.states:
        print(f"== Processing {st}")
        run_cycle(st, args.achieve, args.next_steps, args.dry_run)


if __name__ == "__main__":
    main()
