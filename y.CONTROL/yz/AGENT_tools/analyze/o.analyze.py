#!/usr/bin/env python3
"""Analytics and reporting command wrapping existing utilities."""

from __future__ import annotations

import argparse
import subprocess
import signal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOOLS_BASE = ROOT / "y.CONTROL" / "yz"
TOOLS = TOOLS_BASE / "AGENT_tools"
EVOLVE = TOOLS / "evolve" / "o.evolve.py"
ANALYTICS = TOOLS / "analytics" / "o.analytics.py"
TETRA = TOOLS / "analytics" / "o.tetra.py"
USAGE = TOOLS / "analytics" / "o.usage.py"
SESSGRAPH = TOOLS / "sessgraph" / "o.sessgraph.py"
STRATEGIZE = TOOLS / "analytics" / "o.strategize.py"
EVOLVER = ROOT / "y.CONTROL" / "yz" / "agentflow" / "o.evolver.py"

# Avoid BrokenPipeError when piping output to commands like `head`.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def run(cmd: list[str]) -> int:
    """Run a command, echoing it to stderr so pipelines stay clean."""
    print("$", " ".join(str(c) for c in cmd), file=sys.stderr)
    return subprocess.call(cmd)


def cmd_evolve(_: argparse.Namespace) -> int:
    return run(["python", str(EVOLVE)])


def cmd_summary(_: argparse.Namespace) -> int:
    return run(["python", str(ANALYTICS)])


def cmd_tetra(_: argparse.Namespace) -> int:
    return run(["python", str(TETRA)])


def cmd_usage(_: argparse.Namespace) -> int:
    return run(["python", str(USAGE)])


def cmd_strategize(args: argparse.Namespace) -> int:
    cmd = ["python", str(STRATEGIZE)]
    if args.state:
        cmd += ["--state", args.state]
    return run(cmd)


def cmd_evolver(_: argparse.Namespace) -> int:
    return run(["python", str(EVOLVER)])


def cmd_sessgraph(args: argparse.Namespace) -> int:
    cmd = ["python", str(SESSGRAPH)]
    if args.output:
        cmd += ["--output", str(args.output)]
    return run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analytics and reporting tools")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("evolve", help="Generate evolution summary").set_defaults(func=cmd_evolve)
    sub.add_parser("evolver", help="Propose evolved strategy").set_defaults(func=cmd_evolver)
    sub.add_parser("summary", help="Run analytics summary").set_defaults(func=cmd_summary)
    sub.add_parser("tetra", help="Report tetra dimension usage").set_defaults(func=cmd_tetra)
    sub.add_parser("usage", help="Summarize record field usage").set_defaults(func=cmd_usage)

    p_strat = sub.add_parser("strategize", help="Suggest tactics from past sessions")
    p_strat.add_argument("--state", type=str, default=None, help="F33ling state to analyze")
    p_strat.set_defaults(func=cmd_strategize)

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
