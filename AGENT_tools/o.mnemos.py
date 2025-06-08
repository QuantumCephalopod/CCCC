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
ECHO = ROOT / "AGENT_tools" / "echo" / "o.echo.py"
F33L = ROOT / "AGENT_tools" / "f33l" / "o.f33l.py"
ANALYZE = ROOT / "AGENT_tools" / "analyze" / "o.analyze.py"
AGENTFLOW = ROOT / "AGENT_tools" / "workflow" / "o.agentflow.py"
FLOWLOG = ROOT / "AGENT_tools" / "workflow" / "o.flowlog.py"


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
    if args.start:
        cmd += ["--start", args.start]
    if args.commands:
        for c in args.commands:
            cmd += ["--command", c]
    if args.no_deep:
        cmd.append("--no-deep")
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



def cmd_echo(args: argparse.Namespace) -> int:
    cmd = ["python", str(ECHO)]
    if args.output:
        cmd += ["--output", str(args.output)]
    if args.sl33p:
        cmd.append("--sl33p")
    if args.tags:
        cmd += ["--tags", *args.tags]
    return run(cmd)


def cmd_f33l(args: argparse.Namespace) -> int:
    """Dispatch to f33l command script."""
    cmd = ["python", str(F33L), args.subcommand]
    cmd += args.extra
    return run(cmd)


def cmd_analyze(args: argparse.Namespace) -> int:
    """Dispatch to analyze command script."""
    cmd = ["python", str(ANALYZE), args.subcommand]
    cmd += args.extra
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


def cmd_agentflow(args: argparse.Namespace) -> int:
    cmd = ["python", str(AGENTFLOW)]
    if args.achieve:
        cmd += ["--achieve", args.achieve]
    if args.next_steps:
        cmd += ["--next", args.next_steps]
    if args.dry_run:
        cmd.append("--dry-run")
    cmd += args.states
    return run(cmd)


def cmd_flowlog(args: argparse.Namespace) -> int:
    cmd = ["python", str(FLOWLOG), args.state]
    if args.dry_run:
        cmd.append("--dry-run")
    cmd += args.sl33p_args
    return run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mnemos unified CLI")
    sub = parser.add_subparsers(dest="command")

    p_w4k3 = sub.add_parser("w4k3", help="Display recent sessions")
    p_w4k3.set_defaults(func=cmd_w4k3)

    p_sl33p = sub.add_parser("sl33p", help="Record a session")
    p_sl33p.add_argument("--dry-run", action="store_true")
    p_sl33p.add_argument("--start", type=str, default=None)
    p_sl33p.add_argument("--command", dest="commands", action="append")
    p_sl33p.add_argument("--no-deep", action="store_true")
    p_sl33p.add_argument("extra", nargs=argparse.REMAINDER)
    p_sl33p.set_defaults(func=cmd_sl33p)

    # Legacy commands retained for backward compatibility
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

    p_echo = sub.add_parser("echo", help="Generate F33ling echo")
    p_echo.add_argument("record", type=Path, help="Session JSON log")
    p_echo.add_argument("--output", type=Path, default=None)
    p_echo.add_argument("--sl33p", action="store_true")
    p_echo.add_argument("--tags", nargs="*")
    p_echo.set_defaults(func=cmd_echo)

    p_f33l = sub.add_parser("f33l", help="F33ling utilities")
    p_f33l.add_argument("subcommand", help="echo/stategraph/sessgraph")
    p_f33l.add_argument("extra", nargs=argparse.REMAINDER)
    p_f33l.set_defaults(func=cmd_f33l)

    p_analyze = sub.add_parser("analyze", help="Run analytics suite")
    p_analyze.add_argument("subcommand", help="evolve/summary/tetra/usage/sessgraph")
    p_analyze.add_argument("extra", nargs=argparse.REMAINDER)
    p_analyze.set_defaults(func=cmd_analyze)

    p_workflow = sub.add_parser(
        "workflow", help="Run w4k3, optional tests, then sl33p"
    )
    p_workflow.add_argument("--skip-w4k3", action="store_true")
    p_workflow.add_argument("--skip-tests", action="store_true")
    p_workflow.add_argument("--dry-run", action="store_true")
    p_workflow.add_argument("sl33p_args", nargs=argparse.REMAINDER)
    p_workflow.set_defaults(func=cmd_workflow)

    p_agentflow = sub.add_parser(
        "agentflow", help="Iterate workflow across multiple states"
    )
    p_agentflow.add_argument("states", nargs="+", help="F33ling states")
    p_agentflow.add_argument("--achieve", default="automated recursive session")
    p_agentflow.add_argument("--next", dest="next_steps", default="continue recursion")
    p_agentflow.add_argument("--dry-run", action="store_true")
    p_agentflow.set_defaults(func=cmd_agentflow)

    p_flowlog = sub.add_parser("flowlog", help="Workflow with state logging")
    p_flowlog.add_argument("state", help="F33ling state assessment")
    p_flowlog.add_argument("--dry-run", action="store_true")
    p_flowlog.add_argument("sl33p_args", nargs=argparse.REMAINDER)
    p_flowlog.set_defaults(func=cmd_flowlog)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
