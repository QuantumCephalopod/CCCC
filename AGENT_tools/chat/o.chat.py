#!/usr/bin/env python3
"""Maintain a simple chat context log between sessions.

Each entry stores the user's input and the agent's reply. The log
preserves only the most recent messages to keep the context small.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHAT_FILE = ROOT / "DATA" / "chat_context.json"


def load_history(path: Path) -> list[dict]:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history: list[dict], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def append_entry(user: str, assistant: str, limit: int) -> None:
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
    history = load_history(CHAT_FILE)
    if limit:
        history = history[-limit:]
    for entry in history:
        user = entry.get("InputMessage", "")
        assistant = entry.get("OutputMessage", "")
        print(f"InputMessage: {user}\nOutputMessage: {assistant}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage session chat context")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Append a conversation pair")
    add.add_argument("user", help="User input text")
    add.add_argument("assistant", help="Agent reply text")
    add.add_argument("--limit", type=int, default=10, help="Max messages to keep")

    show = sub.add_parser("show", help="Display recent conversation")
    show.add_argument("--limit", type=int, default=10, help="Number of messages")

    args = parser.parse_args()
    if args.command == "add":
        append_entry(args.user, args.assistant, args.limit)
    elif args.command == "show":
        show_history(args.limit)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
