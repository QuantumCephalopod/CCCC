#!/usr/bin/env python3
"""Orchestrator for F33ling session transition graphs."""

from __future__ import annotations

import argparse
from pathlib import Path

import sys
import importlib.util

def _load_module(name: str, alias: str | None = None):
    """Load module from file and register optional alias."""
    path = Path(__file__).resolve().with_name(f"{name}.py")
    target = alias or name
    spec = importlib.util.spec_from_file_location(target, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    pkg = target.split(".")[0]
    if pkg not in sys.modules:
        pkg_mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(pkg, loader=None))
        pkg_mod.__path__ = [str(Path(__file__).resolve().parent)]
        sys.modules[pkg] = pkg_mod
    module.__package__ = pkg
    sys.modules[target] = module
    spec.loader.exec_module(module)
    return module


if __package__:
    from .x.DataLayer import load_state_timeline
    from .y.ProcessLayer import analyze_transitions
    from .z.OutputLayer import save_dot
    from .zx.Formatter import transitions_to_dot
else:  # allow running as standalone script
    _load_module("xx.SessionLoader", "x.xx.SessionLoader")
    _load_module("xy.StateExtractor", "x.xy.StateExtractor")
    _load_module("yx.TransitionBuilder", "y.yx.TransitionBuilder")
    _load_module("yy.Metrics", "y.yy.Metrics")
    _load_module("zx.Formatter", "z.zx.Formatter")
    _load_module("zy.Exporter", "z.zy.Exporter")
    load_state_timeline = _load_module("x.DataLayer").load_state_timeline  # type: ignore
    analyze_transitions = _load_module("y.ProcessLayer").analyze_transitions  # type: ignore
    save_dot = _load_module("z.OutputLayer").save_dot  # type: ignore
    transitions_to_dot = _load_module("zx.Formatter", "z.zx.Formatter").transitions_to_dot  # type: ignore


def repo_root() -> Path:
    """Return repository root using git."""
    import subprocess

    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate F33ling transition graph")
    parser.add_argument("--output", type=Path, default=None, help="Path to save DOT graph")
    args = parser.parse_args()

    data_dir = repo_root() / "y.Utilities" / "yx.DataArchive"
    states = load_state_timeline(data_dir)
    freqs = analyze_transitions(states)

    if args.output:
        out_path = save_dot(freqs, args.output)
        print(f"Saved graph to {out_path}")
    else:
        dot = transitions_to_dot(freqs)
        print(dot)


if __name__ == "__main__":
    main()

