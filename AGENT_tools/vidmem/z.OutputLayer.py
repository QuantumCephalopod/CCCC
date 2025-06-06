#!/usr/bin/env python3
"""Output layer orchestrating encode/search helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .x.DataLayer import encode_sessions
from .y.ProcessLayer import search_video


def encode(data_dir: Path, out_video: Path) -> Path:
    """Encode sessions and save video."""
    return encode_sessions(data_dir, out_video)


def search(video: Path, query: str) -> Tuple[str, float]:
    """Search query in video and return best match and score."""
    return search_video(video, query)
