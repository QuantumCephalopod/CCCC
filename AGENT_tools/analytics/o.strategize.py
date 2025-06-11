#!/usr/bin/env python3
"""Suggest tactics based on past F33ling-state success."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


def repo_root() -> Path:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[2]


DATA_DIR = repo_root() / "DATA"


def load_records() -> list[dict]:
    records = []
    if not DATA_DIR.exists():
        return records
    for path in DATA_DIR.glob("*.json"):
        name = path.name
        if (
            name == "chat_context.json"
            or name.endswith("_flow.json")
            or name.endswith("summary.json")
            or name == "COPY_deltas.json"
        ):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            if isinstance(rec, dict):
                records.append(rec)
        except Exception:
            continue
    return records


def extract_states(text: str) -> list[str]:
    if not text:
        return []
    import re
    return re.findall(r"\S+_\S+", text)


def gather(records: list[dict]):
    mapping: dict[str, Counter] = {}
    for rec in records:
        states = extract_states(rec.get("assessment", ""))
        for sg in rec.get("subgoals", []):
            if not sg.get("achieved"):
                continue
            strat = sg.get("strategy_used") or "unspecified"
            for st in states:
                counter = mapping.setdefault(st, Counter())
                counter[strat] += 1
    return mapping


def suggest(state: str | None) -> None:
    records = load_records()
    mapping = gather(records)
    if state:
        counters = mapping.get(state)
        if not counters:
            print(f"No data for {state}")
            return
        print(f"Strategies succeeding with {state}:")
        for strat, count in counters.most_common(5):
            print(f"  {strat}: {count}")
    else:
        for st, counter in mapping.items():
            total = sum(counter.values())
            top, cnt = counter.most_common(1)[0]
            print(f"{st}: best strategy '{top}' ({cnt}/{total})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Suggest tactics from history")
    parser.add_argument("--state", type=str, default=None, help="F33ling state to analyze")
    args = parser.parse_args()
    suggest(args.state)


if __name__ == "__main__":
    main()
