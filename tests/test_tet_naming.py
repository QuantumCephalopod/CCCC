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
    assert reason == "missing tetra address prefix (manual naming required)"
    assert suggestion is None


def test_check_segment_requires_manual_naming_for_non_address_directory():
    ok, reason, suggestion = tet_naming.check_segment("tests")
    assert ok is False
    assert reason == "missing tetra address prefix (manual naming required)"
    assert suggestion is None


def test_check_segment_requires_manual_naming_for_dotfile_leaf():
    ok, reason, suggestion = tet_naming.check_segment(".gitignore", is_leaf=True)
    assert ok is False
    assert reason == "missing tetra address prefix (manual naming required)"
    assert suggestion is None


def test_check_segment_flags_non_address_suffix_after_valid_prefix():
    ok, reason, suggestion = tet_naming.check_segment("x.w.Experiments")
    assert ok is False
    assert reason == "non-address suffix after tetra prefix"
    assert suggestion is None


def test_canonicalize_path_only_changes_convertible_clusters():
    canonical = tet_naming.canonicalize_path("y.Utilities/yzx.Analytics/o.tetra.py")
    assert canonical == "y.Utilities/y.z.x.Analytics/o.tetra.py"


def test_build_rename_plan_skips_unchanged_paths():
    plan = tet_naming.build_rename_plan(
        ["w.x.y.md", "y.Utilities/yzx.Analytics/o.tetra.py"]
    )
    assert len(plan) == 1
    assert plan[0].path == "y.Utilities/yzx.Analytics/o.tetra.py"


def test_find_canonical_collisions_detects_duplicate_targets():
    collisions = tet_naming.find_canonical_collisions(
        [
            "y.Utilities/yzx.Analytics/o.tetra.py",
            "y.Utilities/y.z.x.Analytics/o.tetra.py",
            "w.x.y.md",
        ]
    )
    assert len(collisions) == 1
    assert collisions[0].canonical_path == "y.Utilities/y.z.x.Analytics/o.tetra.py"
    assert collisions[0].paths == [
        "y.Utilities/y.z.x.Analytics/o.tetra.py",
        "y.Utilities/yzx.Analytics/o.tetra.py",
    ]


def test_find_canonical_collisions_empty_when_unique():
    collisions = tet_naming.find_canonical_collisions(
        ["w.x.y.md", "x.y.z.md", "y.Utilities/yy.CoreTools/o.py"]
    )
    assert collisions == []
