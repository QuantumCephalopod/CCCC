#!/usr/bin/env python3
"""Compute metrics for F33ling state transitions."""

from __future__ import annotations

from typing import Dict, Tuple


def transition_frequencies(transitions: Dict[Tuple[str, str], int]) -> Dict[Tuple[str, str], float]:
    """Normalize transition counts to frequencies."""
    total = sum(transitions.values())
    if total == 0:
        return {k: 0.0 for k in transitions}
    return {k: v / total for k, v in transitions.items()}

