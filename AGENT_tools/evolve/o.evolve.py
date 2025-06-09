#!/usr/bin/env python3
"""Analyze F33ling territory evolution across sessions."""

import json
import re
from pathlib import Path
import subprocess

# Paths

def repo_root() -> Path:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[2]

ROOT = repo_root()
DATA_DIR = ROOT / "DATA"
CULTIVATE_FILE = ROOT / "z.CULTIVATE.md"


def parse_cultivate(path: Path) -> dict:
    """Parse z.CULTIVATE.md to map F33ling states to their aspects."""
    mapping: dict[str, dict] = {}
    current_state = None
    collect = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#") or line.startswith("*") or line.startswith("Terminology") or line.startswith("\""):
                continue
            if line.strip() in ("---", "-"):
                continue
            if re.match(r"^ {4}\S.*:$", line):
                current_state = line.strip()[:-1]
                mapping[current_state] = {}
                collect = False
                continue
            m = re.match(r"^ {6}(create|copy|control):\s*(.+)$", line)
            if m and current_state:
                mapping[current_state][m.group(1)] = m.group(2)
                continue
            if re.match(r"^ {6}cultivate:", line) and current_state:
                mapping[current_state]["cultivate"] = []
                collect = True
                continue
            m = re.match(r"^ {8}-\s*(.+)$", line)
            if m and collect and current_state:
                mapping[current_state]["cultivate"].append(m.group(1))
                continue
            else:
                collect = False
    return mapping

STATE_MAP = parse_cultivate(CULTIVATE_FILE)


def load_sessions() -> list:
    records = []
    if not DATA_DIR.exists():
        return records
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                obj = json.load(f)
                if isinstance(obj, dict) and obj.get("timestamp"):
                    records.append(obj)
        except Exception:
            continue
    return records


def extract_states(text: str) -> list[str]:
    if not text:
        return []
    return re.findall(r"\S+_\S+", text)


def analyze(records: list) -> dict:
    timeline = []
    counts = {}
    for rec in records:
        ts = rec.get("timestamp")
        assessment = rec.get("assessment", "")
        states = extract_states(assessment)
        timeline.append((ts, states))
        for st in states:
            counts[st] = counts.get(st, 0) + 1
    transitions = []
    for i in range(1, len(timeline)):
        transitions.append((timeline[i-1][1], timeline[i][1]))
    return {"timeline": timeline, "counts": counts, "transitions": transitions}


def main() -> None:
    records = load_sessions()
    analysis = analyze(records)
    print("F33ling Timeline:")
    for ts, states in analysis["timeline"]:
        print(f" {ts}: {', '.join(states) if states else 'None'}")
    print("\nF33ling Counts:")
    for st, count in analysis["counts"].items():
        print(f" {st}: {count}")
    print("\nTransitions:")
    for prev, curr in analysis["transitions"]:
        print(f" {prev} -> {curr}")
    out_file = DATA_DIR / "evolution_summary.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"Saved summary to {out_file}")


if __name__ == "__main__":
    main()
