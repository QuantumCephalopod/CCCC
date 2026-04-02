#!/usr/bin/env python3
"""Unified command-line interface for Mnemos tools."""

from __future__ import annotations

import argparse
import subprocess
import signal
from pathlib import Path
import sys
from mnemos.tet_naming import build_summary, write_rename_plan

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
CORE = ROOT / "y.Utilities" / "yy.CoreTools"
TOOLS_BASE = ROOT / "y.Utilities" / "yz.AgentOps"
if str(TOOLS_BASE) not in sys.path:
    sys.path.insert(0, str(TOOLS_BASE))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TOOLS = TOOLS_BASE / "yzz.Development"
W4K3 = CORE / "yyx.w4k3" / "o.w4k3.py"
SL33P = CORE / "yyz.sl33p" / "o.sl33p.py"
F33L = CORE / "yyy.f33l" / "o.f33l.py"
ANALYZE = TOOLS / "yzzx.Analytics" / "analyze" / "o.analyze.py"
BOOTSTRAP_PROMPT = (
    ROOT
    / "y.Utilities"
    / "yz.AgentOps"
    / "yzx.OperationalData"
    / "octavia_bootstrap_prompt_v1.md"
)


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


def cmd_bootstrap(args: argparse.Namespace) -> int:
    """Print the Octavia bootstrap reminder, then run w4k3."""
    if BOOTSTRAP_PROMPT.exists():
        print(BOOTSTRAP_PROMPT.read_text(encoding="utf-8").strip())
        print()
    else:
        print(
            "Bootstrap prompt not found at "
            f"{BOOTSTRAP_PROMPT}. Continuing with w4k3.",
            file=sys.stderr,
        )
    return cmd_w4k3(argparse.Namespace(extra=args.extra))


def cmd_tet_audit(args: argparse.Namespace) -> int:
    """Report strict `.tet` naming compliance for tracked files."""
    total, bad, issues = build_summary(ROOT)
    print(f"Tracked files: {total}")
    print(f"Divergent files: {bad}")
    rate = (total - bad) / total if total else 0.0
    print(f"Strict compliance: {rate:.1%}")
    if args.limit <= 0:
        return 0
    print()
    print("Top divergent paths:")
    for issue in issues[: args.limit]:
        suggestion = issue.suggestion or "—"
        print(
            f"- {issue.path} :: segment={issue.segment} :: {issue.reason}"
            f" :: suggest={suggestion}"
        )
    return 0


def cmd_tet_plan(args: argparse.Namespace) -> int:
    """Write deterministic rename proposals for canonical dotted addressing."""
    out = write_rename_plan(ROOT, Path(args.out) if args.out else None)
    print(f"Wrote rename plan: {out}")
    return 0



def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "w4k3":
        return cmd_w4k3(argparse.Namespace(extra=sys.argv[2:]))

    parser = argparse.ArgumentParser(description="Mnemos unified CLI")
    sub = parser.add_subparsers(dest="command")

    p_w4k3 = sub.add_parser("w4k3", help="Display recent sessions")
    p_w4k3.set_defaults(func=cmd_w4k3)

    p_sl33p = sub.add_parser("sl33p", help="Record a session")
    p_sl33p.add_argument("--start", type=str, default=None)
    p_sl33p.add_argument("--command", dest="commands", action="append")
    p_sl33p.add_argument("--no-deep", action="store_true")
    p_sl33p.add_argument("extra", nargs=argparse.REMAINDER)
    p_sl33p.set_defaults(func=cmd_sl33p)

    p_f33l = sub.add_parser("f33l", help="F33ling utilities")
    p_f33l.add_argument(
        "subcommand", help="log/suggest/patterns/similar"
    )
    p_f33l.add_argument("extra", nargs=argparse.REMAINDER)
    p_f33l.set_defaults(func=cmd_f33l)

    p_analyze = sub.add_parser("analyze", help="Run analytics suite")
    p_analyze.add_argument("subcommand", help="evolve/summary/tetra/usage/sessgraph")
    p_analyze.add_argument("extra", nargs=argparse.REMAINDER)
    p_analyze.set_defaults(func=cmd_analyze)

    p_bootstrap = sub.add_parser(
        "bootstrap",
        help="Read Octavia bootstrap prompt and run w4k3",
    )
    p_bootstrap.add_argument("extra", nargs=argparse.REMAINDER)
    p_bootstrap.set_defaults(func=cmd_bootstrap)

    p_tet_audit = sub.add_parser(
        "tet-audit",
        help="Audit file naming against strict recursive `.tet` addressing",
    )
    p_tet_audit.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of divergent paths to print (default: 20)",
    )
    p_tet_audit.set_defaults(func=cmd_tet_audit)

    p_tet_plan = sub.add_parser(
        "tet-plan",
        help="Generate a JSON rename plan toward canonical dotted `.tet` segments",
    )
    p_tet_plan.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional output path (default: y.Utilities/yx.DataArchive/tet_rename_plan.json)",
    )
    p_tet_plan.set_defaults(func=cmd_tet_plan)


    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
