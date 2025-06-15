"""Main CLI for w4k3 using tetra modules."""

from __future__ import annotations

import argparse

from .x_load import load_records
from .y_display import (
    display,
    display_transitions,
    summarize_all,
    display_chat,
    summarize_states,
    display_timeline_metrics,
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
        "--transitions-limit",
        type=int,
        default=None,
        help="Limit how many transitions to show when --transitions is set",
    )
    parser.add_argument(
        "--chat-limit",
        type=int,
        default=3,
        help="Number of chat messages to display first",
    )
    parser.add_argument(
        "--top-states",
        type=int,
        default=5,
        help="Show most common F33ling states",
    )
    parser.add_argument(
        "--timeline-limit",
        type=int,
        default=0,
        help="Show timeline metrics for this many states (0=all)",
    )
    args = parser.parse_args()

    display_chat(args.chat_limit)
    records = load_records(args.limit)
    display(records)
    if args.transitions:
        display_transitions(records, args.transitions_limit)
    summarize_all()
    summarize_states(args.top_states)
    display_timeline_metrics(args.timeline_limit or None)


if __name__ == "__main__":
    main()
