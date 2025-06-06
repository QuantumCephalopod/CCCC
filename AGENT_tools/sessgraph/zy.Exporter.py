#!/usr/bin/env python3
"""Export formatted graph data to a file."""

from __future__ import annotations

from pathlib import Path


def export_text(text: str, path: Path) -> Path:
    """Write text to path and return it."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

