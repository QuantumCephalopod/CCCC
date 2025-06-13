#!/usr/bin/env python3
"""Generate a brief echo of F33ling states from a session log."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]


ROOT = repo_root()
DATA_DIR = ROOT / "DATA"
CULTIVATE_MAP = ROOT / "z.CULTIVATE" / "z.CULTIVATE.md"


def extract_states(text: str) -> list[str]:
    """Return list of F33ling states encoded as 'symbol_name'."""
    if not text:
        return []
    return re.findall(r"\S+_\S+", text)


def load_record(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compose_echo(states: list[str]) -> list[str]:
    lines: list[str] = []
    if not states:
        return ["No notable F33ling states detected."]
    for st in states:
        name = st.split("_")[-1]
        lines.append(f"The session resonates with {name} vibes.")
        if len(lines) == 3:
            break
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Echo dominant F33ling states")
    parser.add_argument("record", type=Path, help="Path to session JSON log")
    parser.add_argument("--output", "-o", type=Path, default=Path("ECHO.md"))
    parser.add_argument("--sl33p", action="store_true", help="Commit echo via sl33p")
    parser.add_argument("--tags", nargs="*", help="Only process if these tags appear")
    args = parser.parse_args()

    rec = load_record(args.record)
    text = (rec.get("assessment", "") or "") + "\n" + (rec.get("narrative", "") or "")
    states = extract_states(text)

    if args.tags:
        if not any(tag in states for tag in args.tags):
            print("No matching tags found in record")
            return
        states = [st for st in states if any(tag in st for tag in args.tags)]

    lines = compose_echo(states)
    with open(args.output, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"Saved echo to {args.output}")

    if args.sl33p:
        env = {"ASSESS": "Echo", "ACHIEVE": f"generated echo {args.output.name}", "NEXT": "review"}
        subprocess.run(["python", str(ROOT / "y.CONTROL" / "yz" / "AGENT_tools" / "sl33p" / "o.sl33p.py")], env=env)


if __name__ == "__main__":
    main()
