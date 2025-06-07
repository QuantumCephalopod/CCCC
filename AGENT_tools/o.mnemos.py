#!/usr/bin/env python3
"""Unified command-line interface for Mnemos tools."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W4K3 = ROOT / "AGENT_tools" / "w4k3" / "o.w4k3.py"
SL33P = ROOT / "AGENT_tools" / "sl33p" / "o.sl33p.py"
EVOLVE = ROOT / "AGENT_tools" / "evolve" / "o.evolve.py"
ANALYTICS = ROOT / "AGENT_tools" / "analytics" / "o.analytics.py"
TETRA = ROOT / "AGENT_tools" / "analytics" / "o.tetra.py"
STATEGRAPH = ROOT / "AGENT_tools" / "analytics" / "o.stategraph.py"
USAGE = ROOT / "AGENT_tools" / "analytics" / "o.usage.py"
SESSGRAPH = ROOT / "AGENT_tools" / "sessgraph" / "o.sessgraph.py"
VIDMEM = ROOT / "AGENT_tools" / "vidmem" / "o.vidmem.py"


def run(cmd: list[str]) -> int:
    """Execute a command and return its exit code."""
    print("$", " ".join(str(c) for c in cmd))
    return subprocess.call(cmd)


def cmd_w4k3(_: argparse.Namespace) -> int:
    return run(["python", str(W4K3)])


def cmd_sl33p(args: argparse.Namespace) -> int:
    cmd = ["python", str(SL33P)]
    if args.dry_run:
        cmd.append("--dry-run")
    cmd += args.extra
    return run(cmd)


def cmd_evolve(_: argparse.Namespace) -> int:
    return run(["python", str(EVOLVE)])


def cmd_analytics(_: argparse.Namespace) -> int:
    return run(["python", str(ANALYTICS)])


def cmd_tetra(_: argparse.Namespace) -> int:
    return run(["python", str(TETRA)])


def cmd_stategraph(args: argparse.Namespace) -> int:
    cmd = ["python", str(STATEGRAPH)]
    if args.output:
        cmd += ["--output", str(args.output)]
    return run(cmd)


def cmd_usage(_: argparse.Namespace) -> int:
    return run(["python", str(USAGE)])


def cmd_sessgraph(args: argparse.Namespace) -> int:
    cmd = ["python", str(SESSGRAPH)]
    if args.output:
        cmd += ["--output", str(args.output)]
    return run(cmd)


def cmd_vidmem(args: argparse.Namespace) -> int:
    cmd = ["python", str(VIDMEM)] + args.extra
    return run(cmd)


def cmd_workflow(args: argparse.Namespace) -> int:
    if not args.skip_w4k3:
        code = cmd_w4k3(args)
        if code:
            return code
    if not args.skip_tests:
        files = subprocess.check_output(["git", "ls-files", "*.py"], text=True)
        py_files = files.split()
        code = run(["python", "-m", "py_compile", *py_files])
        if code:
            return code
    sl_args = argparse.Namespace(dry_run=args.dry_run, extra=args.sl33p_args)
    return cmd_sl33p(sl_args)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mnemos unified CLI")
    sub = parser.add_subparsers(dest="command")

    p_w4k3 = sub.add_parser("w4k3", help="Display recent sessions")
    p_w4k3.set_defaults(func=cmd_w4k3)

    p_sl33p = sub.add_parser("sl33p", help="Record a session")
    p_sl33p.add_argument("--dry-run", action="store_true")
    p_sl33p.add_argument("extra", nargs=argparse.REMAINDER)
    p_sl33p.set_defaults(func=cmd_sl33p)

    p_evolve = sub.add_parser("evolve", help="Generate evolution summary")
    p_evolve.set_defaults(func=cmd_evolve)

    p_analytics = sub.add_parser("analytics", help="Run analytics")
    p_analytics.set_defaults(func=cmd_analytics)

    p_tetra = sub.add_parser("tetra", help="Report tetra dimension usage")
    p_tetra.set_defaults(func=cmd_tetra)

    p_stategraph = sub.add_parser(
        "stategraph", help="Create F33ling state graph"
    )
    p_stategraph.add_argument("--output", type=Path, default=None)
    p_stategraph.set_defaults(func=cmd_stategraph)

    p_usage = sub.add_parser("usage", help="Summarize record field usage")
    p_usage.set_defaults(func=cmd_usage)

    p_sessgraph = sub.add_parser(
        "sessgraph", help="Generate F33ling transition graph"
    )
    p_sessgraph.add_argument("--output", type=Path, default=None)
    p_sessgraph.set_defaults(func=cmd_sessgraph)

    p_vidmem = sub.add_parser("vidmem", help="Video memory operations")
    p_vidmem.add_argument("extra", nargs=argparse.REMAINDER)
    p_vidmem.set_defaults(func=cmd_vidmem)

    p_workflow = sub.add_parser(
        "workflow", help="Run w4k3, optional tests, then sl33p"
    )
    p_workflow.add_argument("--skip-w4k3", action="store_true")
    p_workflow.add_argument("--skip-tests", action="store_true")
    p_workflow.add_argument("--dry-run", action="store_true")
    p_workflow.add_argument("sl33p_args", nargs=argparse.REMAINDER)
    p_workflow.set_defaults(func=cmd_workflow)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
