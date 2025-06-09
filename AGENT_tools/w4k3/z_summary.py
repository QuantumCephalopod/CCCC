"""Main CLI for w4k3 using tetra modules."""

from __future__ import annotations

import argparse

from AGENT_tools.w4k3.x_load import load_records
from AGENT_tools.w4k3.y_display import (
    display,
    display_transitions,
    summarize_all,
    display_chat,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Display recent sessions")
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=5,
        help="Number of recent sessions to show",
    )
    parser.add_argument(
        "-t",
        "--transitions",
        action="store_true",
        help="Show F33ling transitions between sessions",
    )
    parser.add_argument(
        "--chat-limit",
        type=int,
        default=3,
        help="Number of chat messages to display first",
    )
    args = parser.parse_args()

    display_chat(args.chat_limit)
    records = load_records(args.limit)
    display(records)
    if args.transitions:
        display_transitions(records)
    summarize_all()


if __name__ == "__main__":
    main()
