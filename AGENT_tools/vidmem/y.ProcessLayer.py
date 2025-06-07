#!/usr/bin/env python3
"""Process layer for decoding and searching video sessions."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

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
            texts.append(results[0].data.decode("utf-8"))
    cap.release()
    return texts


def search_video(video_path: Path, query: str) -> Tuple[str, float]:
    """Return best matching text and similarity score for ``query``."""
    texts = decode_frames(video_path)
    if not texts:
        return "", 0.0
    best = difflib.get_close_matches(query, texts, n=1)
    if best:
        match = best[0]
        score = difflib.SequenceMatcher(None, query, match).ratio()
    else:
        match = ""
        score = 0.0
    return match, score
