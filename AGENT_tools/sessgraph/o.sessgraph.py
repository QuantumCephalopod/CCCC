#!/usr/bin/env python3
"""Orchestrator for F33ling session transition graphs."""

from __future__ import annotations

import argparse
from pathlib import Path

from .x.DataLayer import load_state_timeline
from .y.ProcessLayer import analyze_transitions
from .z.OutputLayer import save_dot


def repo_root() -> Path:
    """Return repository root using git."""
    import subprocess

    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate F33ling transition graph")
    parser.add_argument("--output", type=Path, default=None, help="Path to save DOT graph")
    args = parser.parse_args()

    data_dir = repo_root() / "DATA"
    states = load_state_timeline(data_dir)
    freqs = analyze_transitions(states)

    if args.output:
        out_path = save_dot(freqs, args.output)
        print(f"Saved graph to {out_path}")
    else:
        from .zx.Formatter import transitions_to_dot

        dot = transitions_to_dot(freqs)
        print(dot)


if __name__ == "__main__":
    main()

