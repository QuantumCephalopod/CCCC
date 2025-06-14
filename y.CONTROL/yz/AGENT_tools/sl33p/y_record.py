"""Record building utilities for sl33p."""

from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ASCII_LETTERS = list("abcdefghijklmnopqrstuvwxyz")


def sanitize(text: str) -> str:
    """Remove non-printable characters and surrounding whitespace."""
    return "".join(ch for ch in text.strip() if ch.isprintable())


def parse_json_field(text: str):
    """Attempt to parse a field as JSON; fall back to sanitized string."""
    if text is None:
        return None
    cleaned = text.strip()
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except Exception:
        return sanitize(cleaned)


def current_time_stamp() -> str:
    """Return an ISO style timestamp for filenames."""
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def next_timestamp(data_dir: Path) -> str:
    files = sorted(data_dir.glob("*.json"))
    count = len(files)
    letter = ASCII_LETTERS[count % len(ASCII_LETTERS)]
    cycle = count // len(ASCII_LETTERS) + 1
    prefix = current_time_stamp()
    return f"{prefix}_{letter}{cycle}"


def build_record(
    timestamp: str,
    assessment: str,
    achievements: str,
    next_steps: str,
    create=None,
    copy=None,
    control=None,
    cultivate=None,
    narrative=None,
    poem=None,
    subgoals: list[dict] | None = None,
    session_type: str | None = None,
    prompt_rewrite: str | None = None,
    optimization=None,
    start_time: datetime | None = None,
    commands: list[str] | None = None,
    states: list[str] | None = None,
    stategraph: dict | None = None,
) -> dict:
    record = {
        "timestamp": timestamp,
        "assessment": assessment,
        "achievements": achievements,
        "next": next_steps,
    }
    tetra = {}
    if create is not None:
        record["aspects"] = create
        tetra["create"] = create
    if copy is not None:
        record["learning"] = copy
        tetra["copy"] = copy
    if control is not None:
        record["methodology"] = control
        tetra["control"] = control
    if cultivate is not None:
        record["framework_depth"] = cultivate
        tetra["cultivate"] = cultivate
    if narrative is not None:
        record["narrative"] = narrative
    if poem is not None:
        record["poem"] = poem
    if tetra:
        record["tetra"] = tetra
    if subgoals:
        record["subgoals"] = subgoals
    if session_type:
        record["session_type"] = session_type
    if prompt_rewrite:
        record["prompt_rewrite"] = prompt_rewrite
    if optimization:
        record["optimization"] = optimization
    if start_time:
        record["start"] = start_time.isoformat(timespec="seconds")
        delta = datetime.utcnow() - start_time
        record["duration"] = max(0, int(delta.total_seconds()))
    if commands:
        record["commands"] = commands
    if states:
        record["states"] = states
    if stategraph:
        record["stategraph"] = stategraph
    return record
