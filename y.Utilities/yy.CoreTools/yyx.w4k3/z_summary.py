"""Main CLI for w4k3 using tetra modules."""

from __future__ import annotations

import argparse

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

HERE = Path(__file__).resolve().parent

def _load(name: str, file: str):
    loader = SourceFileLoader(name, str(HERE / file))
    spec = spec_from_loader(name, loader)
    mod = module_from_spec(spec)
    loader.exec_module(mod)
    return mod

x_load = _load("x_load", "x_load.py")
y_display = _load("y_display", "y_display.py")
load_records = x_load.load_records
display = y_display.display
display_transitions = y_display.display_transitions
summarize_all = y_display.summarize_all
summarize_states = y_display.summarize_states
display_timeline_metrics = y_display.display_timeline_metrics


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

    records = load_records(args.limit)
    display(records)
    if args.transitions:
        display_transitions(records, args.transitions_limit)
    summarize_all()
    summarize_states(args.top_states)
    display_timeline_metrics(args.timeline_limit or None)


if __name__ == "__main__":
    main()
