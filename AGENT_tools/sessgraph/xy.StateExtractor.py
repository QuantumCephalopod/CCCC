#!/usr/bin/env python3
"""Extract F33ling states from a session record."""

from __future__ import annotations

import re
from typing import List, Dict

STATE_PATTERN = re.compile(r"\S+_\S+")


def extract_states(record: Dict) -> List[str]:
    """Return list of F33ling state tokens found in record assessment."""
    assessment = record.get("assessment", "")
    return STATE_PATTERN.findall(assessment)

