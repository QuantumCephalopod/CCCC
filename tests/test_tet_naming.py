from importlib import util
from pathlib import Path
import sys

spec = util.spec_from_file_location(
    "tet_naming", Path(__file__).resolve().parents[1] / "mnemos" / "tet_naming.py"
)
tet_naming = util.module_from_spec(spec)
sys.modules["tet_naming"] = tet_naming
spec.loader.exec_module(tet_naming)


def test_check_segment_accepts_canonical_address():
    ok, reason, suggestion = tet_naming.check_segment("w.x.y.md", is_leaf=True)
    assert ok is True
    assert reason == "ok"
    assert suggestion is None


def test_check_segment_flags_compressed_cluster_and_suggests_dotted():
    ok, reason, suggestion = tet_naming.check_segment("yzx.Analytics")
    assert ok is False
    assert "compressed" in reason
    assert suggestion == "y.z.x.Analytics"


def test_audit_paths_stops_on_first_bad_segment_per_path():
    issues = tet_naming.audit_paths(["y.Utilities/yy.CoreTools/file.py"])
    assert len(issues) == 1
    assert issues[0].segment == "y.Utilities"


def test_check_segment_reports_missing_prefix_when_not_address_based():
    ok, reason, suggestion = tet_naming.check_segment("README.md", is_leaf=True)
    assert ok is False
    assert reason == "missing tetra address prefix"
    assert suggestion is None


def test_check_segment_flags_non_address_suffix_after_valid_prefix():
    ok, reason, suggestion = tet_naming.check_segment("x.w.Experiments")
    assert ok is False
    assert reason == "non-address suffix after tetra prefix"
    assert suggestion is None


def test_canonicalize_path_only_changes_convertible_clusters():
    assert tet_naming.canonicalize_path("y.Utilities/yzx.Analytics/o.tetra.py") == (
        "y.Utilities/y.z.x.Analytics/o.tetra.py"
    )


def test_build_rename_plan_skips_unchanged_paths():
    plan = tet_naming.build_rename_plan(
        ["w.x.y.md", "y.Utilities/yzx.Analytics/o.tetra.py"]
    )
    assert len(plan) == 1
    assert plan[0].path == "y.Utilities/yzx.Analytics/o.tetra.py"
