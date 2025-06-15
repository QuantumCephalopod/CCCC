#!/usr/bin/env python3
"""Advanced session analytics for workflow optimization.

This script analyzes session records in the DATA directory and
produces statistics about session frequency, F33ling state trends,
and common achievement themes. The goal is to provide actionable
insights for improving development patterns.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]


ROOT = repo_root()
DATA_DIR = ROOT / "y.Utilities" / "yx.DataArchive"


def load_sessions() -> list[dict]:
    records = []
    if not DATA_DIR.exists():
        return records
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            rec["_file"] = path
            records.append(rec)
        except Exception:
            continue
    return records


def git_time(path: Path) -> datetime:
    """Return the commit timestamp for the given file."""
    out = subprocess.check_output([
        "git",
        "log",
        "-1",
        "--format=%cI",
        str(path),
    ], text=True)
    return datetime.fromisoformat(out.strip())


def extract_states(text: str) -> list[str]:
    if not text:
        return []
    return re.findall(r"\S+_\S+", text)


STOPWORDS = {
    "the",
    "and",
    "to",
    "a",
    "of",
    "in",
    "for",
    "with",
    "on",
    "run",
    "ran",
}


def analyze() -> dict:
    sessions = load_sessions()
    if not sessions:
        return {}

    timeline = []
    for rec in sessions:
        rec["commit_time"] = git_time(rec["_file"])
        rec["states"] = extract_states(rec.get("assessment", ""))
        timeline.append(rec)
    timeline.sort(key=lambda r: r["commit_time"])

    # session intervals
    gaps = []
    for i in range(1, len(timeline)):
        delta = timeline[i]["commit_time"] - timeline[i - 1]["commit_time"]
        gaps.append(delta.total_seconds() / 3600.0)

    avg_gap = sum(gaps) / len(gaps) if gaps else 0.0
    max_gap = max(gaps) if gaps else 0.0

    # F33ling effectiveness: average gap after each state
    state_gap_store: dict[str, list[float]] = defaultdict(list)
    for i in range(len(timeline) - 1):
        gap_hours = (
            timeline[i + 1]["commit_time"] - timeline[i]["commit_time"]
        ).total_seconds() / 3600.0
        for st in timeline[i]["states"]:
            state_gap_store[st].append(gap_hours)

    state_avg_gap = {
        st: sum(vals) / len(vals) for st, vals in state_gap_store.items()
    }

    # word frequency in achievements
    word_counts: Counter[str] = Counter()
    for rec in timeline:
        words = re.findall(r"[A-Za-z]+", rec.get("achievements", "").lower())
        for w in words:
            if w not in STOPWORDS:
                word_counts[w] += 1

    # competency heatmap per state and session type
    heat: dict[str, Counter] = {}
    for rec in timeline:
        stype = rec.get("session_type") or "unspecified"
        for st in rec.get("states", []):
            counter = heat.setdefault(st, Counter())
            counter[stype] += 1

    top_words = word_counts.most_common(10)

    result = {
        "session_count": len(timeline),
        "average_gap_hours": round(avg_gap, 2),
        "max_gap_hours": round(max_gap, 2),
        "state_average_gaps": {st: round(v, 2) for st, v in state_avg_gap.items()},
        "top_achievement_words": top_words,
        "heatmap": {k: dict(v) for k, v in heat.items()},
    }
    return result


def save_summary(summary: dict) -> Path:
    out = DATA_DIR / "analytics_summary.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return out


def main() -> None:
    summary = analyze()
    if not summary:
        print("No session data found.")
        return
    save_path = save_summary(summary)
    print("Session Analytics Summary:")
    for key, val in summary.items():
        if key == "heatmap":
            print("heatmap:")
            for st, mapping in val.items():
                print(f"  {st}:")
                for t, cnt in mapping.items():
                    print(f"    {t}: {cnt}")
        else:
            print(f"{key}: {val}")
    print(f"Saved summary to {save_path}")


if __name__ == "__main__":
    main()
