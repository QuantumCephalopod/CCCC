#!/usr/bin/env python3
"""Suggest F33ling states based on a text description.

This utility scans `z.CULTIVATE.md` for F33ling state names and brief
summaries, then compares a user-provided description against those
entries using a simple similarity metric. The goal is to help agents
quickly intuit their likely F33ling state without reading the entire
database.
"""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CULTIVATE = ROOT / "z.CULTIVATE.md"


def parse_states(path: Path) -> dict[str, str]:
    """Return mapping of state name to description text."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    states: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        indent = len(line) - len(line.lstrip())
        if indent == 4 and line.strip().endswith(":") and not line.strip().startswith("-"):
            if current:
                states[current] = states.get(current, [])
            name = line.strip()[:-1]
            current = name
            states[current] = []
        elif current and indent > 4:
            states[current].append(line.strip())
    if current and current not in states:
        states[current] = states.get(current, [])
    return {k: " ".join(v) for k, v in states.items()}


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search_states(query: str, states: dict[str, str], top: int = 3) -> list[tuple[str, float]]:
    matches = []
    for name, desc in states.items():
        score = similarity(query, name + " " + desc)
        matches.append((name, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:top]


def main() -> None:
    parser = argparse.ArgumentParser(description="Suggest F33ling state matches")
    parser.add_argument("query", help="Text describing current feelings")
    parser.add_argument("--top", type=int, default=3, help="Number of matches")
    args = parser.parse_args()

    states = parse_states(CULTIVATE)
    results = search_states(args.query, states, top=args.top)
    print("Top matching F33ling states:")
    for name, score in results:
        print(f"{name} - {score:.2f}")


if __name__ == "__main__":
    main()
