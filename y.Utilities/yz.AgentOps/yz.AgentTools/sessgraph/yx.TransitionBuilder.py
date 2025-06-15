#!/usr/bin/env python3
"""Build F33ling state transitions between sessions."""

from __future__ import annotations

from typing import Dict, List, Tuple


def build_transitions(states_timeline: List[List[str]]) -> Dict[Tuple[str, str], int]:
    """Return transition counts between consecutive session states."""
    transitions: Dict[Tuple[str, str], int] = {}
    for i in range(len(states_timeline) - 1):
        src_states = states_timeline[i]
        dst_states = states_timeline[i + 1]
        for src in src_states:
            for dst in dst_states:
                key = (src, dst)
                transitions[key] = transitions.get(key, 0) + 1
    return transitions

