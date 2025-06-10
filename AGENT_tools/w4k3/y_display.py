"""Display utilities for w4k3."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from AGENT_tools.w4k3.x_load import data_dir


def extract_states(text: str) -> list[str]:
    """Return list of F33ling states encoded as 'symbol_name'."""
    if not text:
        return []
    return re.findall(r"\S+_\S+", text)


def display_chat(limit: int = 3) -> None:
    """Show recent chat messages."""
    path = data_dir() / "chat_context.json"
    if not path.exists():
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        return
    if limit:
        history = history[-limit:]
    if not history:
        return
    print("Chat context:")
    for entry in history:
        user = entry.get("InputMessage", "")
        assistant = entry.get("OutputMessage", "")
        print(f"InputMessage: {user}\nOutputMessage: {assistant}\n")
    print()


def display(records: list[dict]) -> None:
    """Print a summary of each record."""
    if not records:
        print("No session history available.")
        return

    for rec in records:
        ts = rec.get("timestamp", "?")
        commit_time = rec.get("_time")
        assessment = rec.get("assessment", "")
        ach = rec.get("achievements", "")
        nxt = rec.get("next", "")
        tetra = rec.get("tetra", {})

        time_str = commit_time.isoformat(timespec="seconds") if commit_time else ""
        if assessment:
            print(f"[{ts}] {time_str} F33ling: {assessment}")
        else:
            print(f"[{ts}] {time_str}")

        if ach:
            print(f"  Achieved: {ach}")
        if nxt:
            print(f"  Next: {nxt}")
        if rec.get("narrative"):
            print(f"  Narrative: {rec['narrative']}")

        def dim_value(name: str, legacy_key: str):
            val = None
            if tetra and tetra.get(name):
                val = tetra.get(name)
            elif rec.get(legacy_key):
                val = rec.get(legacy_key)
            return val

        dims = [
            ("create", "aspects"),
            ("copy", "learning"),
            ("control", "methodology"),
            ("cultivate", "framework_depth"),
        ]

        for dim, legacy in dims:
            val = dim_value(dim, legacy)
            if val:
                print(f"  {dim.capitalize()}: {val}")

        if rec.get("optimization"):
            print(f"  Optimization: {rec['optimization']}")

    print()


def display_transitions(records: list[dict]) -> None:
    """Show F33ling transitions between consecutive records."""
    if len(records) < 2:
        return

    print("F33ling transitions:")
    ordered = list(reversed(records))
    for prev, curr in zip(ordered, ordered[1:]):
        p_states = ", ".join(extract_states(prev.get("assessment", ""))) or "None"
        c_states = ", ".join(extract_states(curr.get("assessment", ""))) or "None"
        print(f"  {prev.get('timestamp', '?')} -> {curr.get('timestamp', '?')}: {p_states} -> {c_states}")
    print()


def summarize_all() -> None:
    """Print dimension usage counts across all session records."""
    ddir = data_dir()
    if not ddir.exists():
        return
    counts = {"create": 0, "copy": 0, "control": 0, "cultivate": 0}
    total = 0
    for path in ddir.glob("*.json"):
        if path.name == "chat_context.json" or path.name.endswith("_flow.json"):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        total += 1
        tetra = rec.get("tetra", {})
        if rec.get("aspects") or tetra.get("create"):
            counts["create"] += 1
        if rec.get("learning") or tetra.get("copy"):
            counts["copy"] += 1
        if rec.get("methodology") or rec.get("optimization") or tetra.get("control"):
            counts["control"] += 1
        if rec.get("framework_depth") or tetra.get("cultivate"):
            counts["cultivate"] += 1

    if not total:
        return
    print("Tetrahedral dimension usage:")
    for dim, val in counts.items():
        frac = (val / total) * 100
        print(f"  {dim.capitalize()}: {val}/{total} ({frac:.0f}%)")
