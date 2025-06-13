#!/usr/bin/env python3
"""Data layer orchestrating session loading and state extraction."""

from __future__ import annotations

from pathlib import Path
from typing import List

from .xx.SessionLoader import load_sessions
from .xy.StateExtractor import extract_states


def load_state_timeline(data_dir: Path) -> List[List[str]]:
    """Return list of state lists in chronological order."""
    sessions = load_sessions(data_dir)
    states = [extract_states(rec) for rec in sessions]
    return states

