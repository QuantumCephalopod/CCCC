from datetime import datetime, timedelta, timezone
from importlib import util
from pathlib import Path

spec = util.spec_from_file_location(
    "sl33p_record",
    Path(__file__).resolve().parents[1]
    / "y.Utilities"
    / "yy.CoreTools"
    / "yyz.sl33p"
    / "y_record.py",
)
sl33p_record = util.module_from_spec(spec)
spec.loader.exec_module(sl33p_record)


def test_build_record_duration_with_timezone_aware_start_time():
    start = datetime.now(timezone.utc) - timedelta(seconds=5)

    record = sl33p_record.build_record(
        "20260401T000000Z_a1",
        "state",
        "achieved",
        "next",
        start_time=start,
    )

    assert record["start"].endswith("+00:00")
    assert record["duration"] >= 0


def test_compute_duration_seconds_works_for_naive_datetimes():
    start = datetime(2026, 4, 1, 0, 0, 0)
    now = datetime(2026, 4, 1, 0, 0, 7)

    assert sl33p_record._compute_duration_seconds(start, now=now) == 7


def test_compute_duration_seconds_clamps_future_start_to_zero():
    now = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
    start = now + timedelta(seconds=3)

    assert sl33p_record._compute_duration_seconds(start, now=now) == 0
