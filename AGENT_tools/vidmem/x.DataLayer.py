#!/usr/bin/env python3
"""Data layer for encoding sessions to video."""

from __future__ import annotations

from pathlib import Path
from typing import List

import qrcode
import cv2
import numpy as np


def encode_sessions(data_dir: Path, out_video: Path, fps: int = 1) -> Path:
    """Encode all JSON files in ``data_dir`` as QR frames in ``out_video``."""
    files = sorted(data_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError("no session files found")
    frames: List[np.ndarray] = []
    for f in files:
        text = f.read_text()
        img = qrcode.make(text)
        frame = np.array(img.convert("RGB"))
        frames.append(frame)

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_video), fourcc, fps, (width, height))
    for fr in frames:
        writer.write(cv2.cvtColor(fr, cv2.COLOR_RGB2BGR))
    writer.release()
    return out_video
