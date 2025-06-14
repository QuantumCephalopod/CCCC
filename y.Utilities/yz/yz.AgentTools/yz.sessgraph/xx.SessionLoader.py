#!/usr/bin/env python3
"""Load session JSON records from the DATA directory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict


def load_sessions(data_dir: Path) -> List[Dict]:
    """Return list of session records sorted by filename."""
    records: List[Dict] = []
    if not data_dir.exists():
        return records
    for path in sorted(data_dir.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            rec["_file"] = path
            records.append(rec)
        except Exception:
            continue
    return records

