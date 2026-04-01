"""Record building utilities for sl33p."""

from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ASCII_LETTERS = list("abcdefghijklmnopqrstuvwxyz")


def sanitize(text: str | None) -> str:
    """Remove non-printable characters and surrounding whitespace."""
    if text is None:
        return ""
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


def _compute_duration_seconds(start_time: datetime, now: datetime | None = None) -> int:
    """Return non-negative elapsed seconds from start_time to now."""
    if now is None:
        now = (
            datetime.now(start_time.tzinfo)
            if start_time.tzinfo is not None
            else datetime.now(timezone.utc).replace(tzinfo=None)
        )
    delta = now - start_time
    return max(0, int(delta.total_seconds()))


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
        record["duration"] = _compute_duration_seconds(start_time)
    if commands:
        record["commands"] = commands
    if states:
        record["states"] = states
    if stategraph:
        record["stategraph"] = stategraph
    return record
