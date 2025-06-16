#!/usr/bin/env python3
"""Automation helper to run w4k3, compile tests, and sl33p."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


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
        return Path(__file__).resolve().parents[3]


ROOT = repo_root()

# Path to consolidated mnemos operator
MNEMOS = ROOT / "y.Utilities" / "yy.CoreTools" / "yyo.mnemos.py"


def run(cmd: list[str], **kwargs) -> None:
    """Run command and exit on failure."""
    print("$", " ".join(str(c) for c in cmd))
    res = subprocess.run(cmd, **kwargs)
    if res.returncode != 0:
        raise SystemExit(res.returncode)


def load_env(path: Path) -> None:
    """Load environment variables from a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load config {path}: {e}")
        raise SystemExit(1)
    for k, v in data.items():
        if isinstance(v, (dict, list)):
            os.environ[k] = json.dumps(v)
        else:
            os.environ[k] = str(v)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run typical session workflow")
    parser.add_argument("--skip-w4k3", action="store_true", help="Skip w4k3 step")
    parser.add_argument("--skip-tests", action="store_true", help="Skip py_compile")
    parser.add_argument("--config", type=Path, help="JSON file with env vars for sl33p")

    args, sl33p_args = parser.parse_known_args()

    if args.config:
        load_env(args.config)

    if not args.skip_w4k3:
        run(["python", str(MNEMOS), "w4k3"])

    if not args.skip_tests:
        files = subprocess.check_output(["git", "ls-files", "*.py"], text=True)
        py_files = files.split()
        run(["python", "-m", "py_compile", *py_files])

    sl33p_cmd = ["python", str(MNEMOS), "sl33p"]
    sl33p_cmd += sl33p_args
    run(sl33p_cmd)


if __name__ == "__main__":
    main()
