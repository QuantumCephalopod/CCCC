#!/usr/bin/env python3
"""Process layer orchestrating transition analysis."""

from __future__ import annotations

from typing import Dict, Tuple
from .yx.TransitionBuilder import build_transitions
from .yy.Metrics import transition_frequencies


def analyze_transitions(states: list[list[str]]) -> Dict[Tuple[str, str], float]:
    """Return frequency table for state transitions."""
    counts = build_transitions(states)
    return transition_frequencies(counts)

