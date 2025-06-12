#!/usr/bin/env python3
"""Priming and state management commands.

Wraps existing echo and state graph utilities under a single interface."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools" / "AGENT_tools"
ECHO = TOOLS / "echo" / "o.echo.py"
STATEGRAPH = TOOLS / "analytics" / "o.stategraph.py"
SESSGRAPH = TOOLS / "sessgraph" / "o.sessgraph.py"
INTROSPECT = TOOLS / "f33l" / "o.introspect.py"


def run(cmd: list[str]) -> int:
    """Execute a command and return its exit code."""
    print("$", " ".join(str(c) for c in cmd))
    return subprocess.call(cmd)


def cmd_echo(args: argparse.Namespace) -> int:
    cmd = ["python", str(ECHO), str(args.record)]
    if args.output:
        cmd += ["--output", str(args.output)]
    if args.sl33p:
        cmd.append("--sl33p")
    if args.tags:
        cmd += ["--tags", *args.tags]
    return run(cmd)


def cmd_stategraph(args: argparse.Namespace) -> int:
    cmd = ["python", str(STATEGRAPH)]
    if args.output:
        cmd += ["--output", str(args.output)]
    return run(cmd)


def cmd_sessgraph(args: argparse.Namespace) -> int:
    cmd = ["python", str(SESSGRAPH)]
    if args.output:
        cmd += ["--output", str(args.output)]
    return run(cmd)


def cmd_introspect(args: argparse.Namespace) -> int:
    cmd = ["python", str(INTROSPECT), args.query]
    if args.top:
        cmd += ["--top", str(args.top)]
    return run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage F33ling state utilities")
    sub = parser.add_subparsers(dest="command")

    p_echo = sub.add_parser("echo", help="Generate F33ling echo")
    p_echo.add_argument("record", type=Path, help="Session JSON log")
    p_echo.add_argument("--output", type=Path, default=None)
    p_echo.add_argument("--sl33p", action="store_true")
    p_echo.add_argument("--tags", nargs="*")
    p_echo.set_defaults(func=cmd_echo)

    p_state = sub.add_parser("stategraph", help="Create F33ling state graph")
    p_state.add_argument("--output", type=Path, default=None)
    p_state.set_defaults(func=cmd_stategraph)

    p_sess = sub.add_parser("sessgraph", help="Generate F33ling transition graph")
    p_sess.add_argument("--output", type=Path, default=None)
    p_sess.set_defaults(func=cmd_sessgraph)

    p_intro = sub.add_parser("introspect", help="Suggest F33ling matches")
    p_intro.add_argument("query", help="text description to analyze")
    p_intro.add_argument("--top", type=int, default=None)
    p_intro.set_defaults(func=cmd_introspect)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
