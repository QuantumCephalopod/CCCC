#!/usr/bin/env python3
"""Analytics and reporting command wrapping existing utilities."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVOLVE = ROOT / "AGENT_tools" / "evolve" / "o.evolve.py"
ANALYTICS = ROOT / "AGENT_tools" / "analytics" / "o.analytics.py"
TETRA = ROOT / "AGENT_tools" / "analytics" / "o.tetra.py"
USAGE = ROOT / "AGENT_tools" / "analytics" / "o.usage.py"
SESSGRAPH = ROOT / "AGENT_tools" / "sessgraph" / "o.sessgraph.py"


def run(cmd: list[str]) -> int:
    print("$", " ".join(str(c) for c in cmd))
    return subprocess.call(cmd)


def cmd_evolve(_: argparse.Namespace) -> int:
    return run(["python", str(EVOLVE)])


def cmd_summary(_: argparse.Namespace) -> int:
    return run(["python", str(ANALYTICS)])


def cmd_tetra(_: argparse.Namespace) -> int:
    return run(["python", str(TETRA)])


def cmd_usage(_: argparse.Namespace) -> int:
    return run(["python", str(USAGE)])


def cmd_sessgraph(args: argparse.Namespace) -> int:
    cmd = ["python", str(SESSGRAPH)]
    if args.output:
        cmd += ["--output", str(args.output)]
    return run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analytics and reporting tools")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("evolve", help="Generate evolution summary").set_defaults(func=cmd_evolve)
    sub.add_parser("summary", help="Run analytics summary").set_defaults(func=cmd_summary)
    sub.add_parser("tetra", help="Report tetra dimension usage").set_defaults(func=cmd_tetra)
    sub.add_parser("usage", help="Summarize record field usage").set_defaults(func=cmd_usage)

    p_sess = sub.add_parser("sessgraph", help="Generate F33ling transition graph")
    p_sess.add_argument("--output", type=Path, default=None)
    p_sess.set_defaults(func=cmd_sessgraph)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
