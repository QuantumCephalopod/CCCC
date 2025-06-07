#!/usr/bin/env python3
"""Process layer for decoding and searching video sessions."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import base64
import zlib

import cv2
from pyzbar.pyzbar import decode
import difflib


def decode_frames(video_path: Path) -> List[str]:
    """Return decoded text from each frame in the video."""
    cap = cv2.VideoCapture(str(video_path))
    texts: List[str] = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = decode(frame)
        if results:
            raw = results[0].data
            try:
                data = zlib.decompress(base64.b64decode(raw))
                texts.append(data.decode("utf-8"))
            except Exception:
                texts.append(raw.decode("utf-8", errors="ignore"))
    cap.release()
    return texts


def search_video(video_path: Path, query: str, limit: int = 3) -> List[Tuple[str, float]]:
    """Return ``limit`` matches sorted by similarity for ``query``."""
    texts = decode_frames(video_path)
    results: List[Tuple[str, float]] = []
    for text in texts:
        score = difflib.SequenceMatcher(None, query, text).ratio()
        results.append((text, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit]
