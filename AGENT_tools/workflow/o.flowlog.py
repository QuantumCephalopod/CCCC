#!/usr/bin/env python3
"""Run workflow with intermediate F33ling state logging."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
MNEMOS = ROOT / "AGENT_tools" / "o.mnemos.py"
LOG_DIR = ROOT / "DATA"


def run(cmd: list[str]) -> None:
    """Execute command and stop on failure."""
    print("$", " ".join(str(c) for c in cmd))
    res = subprocess.run(cmd)
    if res.returncode != 0:
        raise SystemExit(res.returncode)


def log_state(logfile: Path, stage: str, state: str) -> None:
    entry = {
        "time": datetime.utcnow().isoformat(timespec="seconds"),
        "stage": stage,
        "state": state,
    }
    data = []
    if logfile.exists():
        try:
            with open(logfile, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(entry)
    with open(logfile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run workflow with F33ling state logging"
    )
    parser.add_argument(
        "state", help="Initial F33ling state assessment"
    )
    parser.add_argument("--dry-run", action="store_true")
    args, sl33p_args = parser.parse_known_args()

    log_file = LOG_DIR / f"{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_flow.json"

    log_state(log_file, "start", args.state)
    run(["python", str(MNEMOS), "w4k3"])
    log_state(log_file, "after_w4k3", args.state)

    files = (
        subprocess.check_output(["git", "ls-files", "*.py"], text=True).split()
    )
    run(["python", "-m", "py_compile", *files])
    log_state(log_file, "after_tests", args.state)

    sl33p_cmd = ["python", str(MNEMOS), "sl33p"]
    if args.dry_run:
        sl33p_cmd.append("--dry-run")
    sl33p_cmd += sl33p_args
    run(sl33p_cmd)
    log_state(log_file, "after_sl33p", args.state)


if __name__ == "__main__":
    main()
