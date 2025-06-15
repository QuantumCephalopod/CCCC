#!/usr/bin/env python3
"""Utility to suggest prompt adjustments based on feedback."""

from __future__ import annotations


def suggest_prompt_adjustment(state: str, result: str, notes: str | None = None) -> str:
    """Return a simple prompt adjustment suggestion."""
    base = f"State `{state}` with result `{result}`"
    if notes:
        base += f" and notes `{notes}`"
    if "discordant" in state.lower():
        return base + " -> Consider shifting COPY focus toward reflective alignment."
    if "flux" in state.lower():
        return base + " -> Emphasize CONTROL for stability."
    return base + " -> Maintain current strategy, minor tweaks only."

