#!/usr/bin/env python3
"""Output layer orchestrating formatting and export."""

from __future__ import annotations

from pathlib import Path

from .zx.Formatter import transitions_to_dot
from .zy.Exporter import export_text


def save_dot(freqs: dict, path: Path) -> Path:
    """Format frequencies to DOT and save to path."""
    dot = transitions_to_dot(freqs)
    return export_text(dot, path)

