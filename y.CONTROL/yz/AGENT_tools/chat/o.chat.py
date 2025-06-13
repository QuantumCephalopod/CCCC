#!/usr/bin/env python3
"""Maintain a simple chat context log between sessions.

Each entry stores the user's input and the agent's reply. The log
preserves only the most recent messages to keep the context small.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure package imports work when executed directly
ROOT = Path(__file__).resolve().parents[4]
TOOLS_PATH = ROOT / "y.CONTROL" / "yz"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

from AGENT_tools.sl33p.z_persistence import ensure_data_dir
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

INTROSPECT_PATH = Path(__file__).resolve().parents[1] / 'f33l' / 'o.introspect.py'
_loader = SourceFileLoader('f33lintrospect', str(INTROSPECT_PATH))
_spec = spec_from_loader('f33lintrospect', _loader)
_mod = module_from_spec(_spec)
_loader.exec_module(_mod)
parse_states = _mod.parse_states
search_states = _mod.search_states

CHAT_FILE = ROOT / "DATA" / "chat_context.json"

_STATES: dict[str, str] | None = None


def load_states() -> dict[str, str]:
    """Return F33ling states parsed from z.CULTIVATE.md."""
    global _STATES
    if _STATES is None:
        try:
            path = ROOT / "z.CULTIVATE" / "z.CULTIVATE.md"
            _STATES = parse_states(path)
        except Exception:
            _STATES = {}
    return _STATES


def load_history(path: Path) -> list[dict]:
    ensure_data_dir()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history: list[dict], path: Path) -> None:
    ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_entry(user: str, assistant: str, limit: int) -> None:
    ensure_data_dir()
    history = load_history(CHAT_FILE)
    history.append(
        {
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "InputMessage": user,
            "OutputMessage": assistant,
        }
    )
    if limit and len(history) > limit:
        history = history[-limit:]
    save_history(history, CHAT_FILE)


def show_history(limit: int) -> None:
    ensure_data_dir()
    history = load_history(CHAT_FILE)
    if limit:
        history = history[-limit:]
    for entry in history:
        user = entry.get("InputMessage", "")
        assistant = entry.get("OutputMessage", "")
        print(f"InputMessage: {user}\nOutputMessage: {assistant}\n")


def introspect_history(limit: int, top: int) -> None:
    """Suggest F33ling states for each chat entry."""
    ensure_data_dir()
    history = load_history(CHAT_FILE)
    if limit:
        history = history[-limit:]
    states = load_states()
    if not states:
        print("No F33ling states available.")
        return
    for entry in history:
        user = entry.get("InputMessage", "")
        assistant = entry.get("OutputMessage", "")
        text = f"{user} {assistant}".strip()
        matches = search_states(text, states, top=top)
        print(f"InputMessage: {user}\nOutputMessage: {assistant}")
        if matches:
            print("F33l suggestions:")
            for name, score in matches:
                print(f"  {name} ({score:.2f})")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage session chat context")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Append a conversation pair")
    add.add_argument("user", help="User input text")
    add.add_argument("assistant", help="Agent reply text")
    add.add_argument("--limit", type=int, default=10, help="Max messages to keep")

    show = sub.add_parser("show", help="Display recent conversation")
    show.add_argument("--limit", type=int, default=10, help="Number of messages")

    intros = sub.add_parser("f33l", help="Analyze F33ling states in chat")
    intros.add_argument("--limit", type=int, default=10, help="Messages to analyze")
    intros.add_argument("--top", type=int, default=3, help="Matches per message")

    args = parser.parse_args()
    if args.command == "add":
        append_entry(args.user, args.assistant, args.limit)
    elif args.command == "show":
        show_history(args.limit)
    elif args.command == "f33l":
        introspect_history(args.limit, args.top)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
