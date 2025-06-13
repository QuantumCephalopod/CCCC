#!/usr/bin/env python3
"""Meta-agent to propose evolved tetra priorities."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


# repository root
ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "DATA"


def load_records() -> list[dict]:
    recs = []
    for path in sorted(DATA_DIR.glob("*.json")):
        name = path.name
        if (
            name == "chat_context.json"
            or name.endswith("_flow.json")
            or name.endswith("summary.json")
            or name.endswith("metrics.json")
        ):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                recs.append(data)
        except Exception:
            continue
    return recs


def propose(records: list[dict]) -> dict:
    """Return simple strategy proposal."""
    counts = {"create": 0, "copy": 0, "control": 0, "cultivate": 0}
    fail_counts = counts.copy()
    for rec in records:
        states = rec.get("states") or []
        for dim in counts:
            if rec.get(dim if dim != "copy" else "learning"):
                counts[dim] += 1
        for sg in rec.get("subgoals", []):
            if not sg.get("achieved"):
                for st in states:
                    fail_counts[st.split("_")[-1].lower()] = fail_counts.get(
                        st.split("_")[-1].lower(), 0
                    ) + 1
    dominant = max(counts, key=counts.get) if records else "create"
    tweak = max(fail_counts, key=fail_counts.get) if fail_counts else "control"
    return {
        "focus": dominant,
        "increase": tweak,
    }


def save(proposal: dict) -> Path:
    out = DATA_DIR / "evolved_strategy.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(proposal, f, indent=2)
        f.write("\n")
    return out


def main() -> None:
    recs = load_records()
    prop = propose(recs)
    out = save(prop)
    print("Evolved strategy proposal:")
    print(json.dumps(prop, indent=2))
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
