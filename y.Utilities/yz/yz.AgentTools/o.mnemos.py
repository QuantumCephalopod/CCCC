#!/usr/bin/env python3
"""Unified command-line interface for Mnemos tools."""

from __future__ import annotations

import argparse
import subprocess
import signal
from pathlib import Path
import sys

# Exit cleanly when piped output is truncated (e.g., `| head`).
signal.signal(signal.SIGPIPE, signal.SIG_DFL)


THIS_FILE = Path(__file__).resolve()


def repo_root() -> Path:
    """Return repository root, using git if available."""
    try:
        out = subprocess.check_output(
            ["git", "-C", str(THIS_FILE.parent), "rev-parse", "--show-toplevel"],
            text=True,
        )
        return Path(out.strip())
    except Exception:
        return THIS_FILE.parents[3]

ROOT = repo_root()
TOOLS_BASE = ROOT / "y.Utilities" / "yz"
if str(TOOLS_BASE) not in sys.path:
    sys.path.insert(0, str(TOOLS_BASE))
TOOLS = TOOLS_BASE / "yz.AgentTools"
W4K3 = TOOLS / "w4k3" / "o.w4k3.py"
SL33P = TOOLS / "sl33p" / "o.sl33p.py"
F33L = TOOLS / "f33l" / "o.f33l.py"
ANALYZE = TOOLS / "analyze" / "o.analyze.py"


def run(cmd: list[str]) -> int:
    """Execute a command and return its exit code; command is printed to stderr."""
    print("$", " ".join(str(c) for c in cmd), file=sys.stderr)
    return subprocess.call(cmd)


def cmd_w4k3(args: argparse.Namespace) -> int:
    cmd = ["python", str(W4K3)]
    cmd += args.extra
    return run(cmd)


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



def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "w4k3":
        return cmd_w4k3(argparse.Namespace(extra=sys.argv[2:]))

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

    p_f33l = sub.add_parser("f33l", help="F33ling utilities")
    p_f33l.add_argument("subcommand", help="echo/stategraph/sessgraph/introspect")
    p_f33l.add_argument("extra", nargs=argparse.REMAINDER)
    p_f33l.set_defaults(func=cmd_f33l)

    p_analyze = sub.add_parser("analyze", help="Run analytics suite")
    p_analyze.add_argument("subcommand", help="evolve/summary/tetra/usage/sessgraph")
    p_analyze.add_argument("extra", nargs=argparse.REMAINDER)
    p_analyze.set_defaults(func=cmd_analyze)


    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
