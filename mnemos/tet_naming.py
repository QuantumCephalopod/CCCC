"""Audit repository file names against strict recursive `.tet` address naming.

Strict convention used by this audit:
- each path segment stem should begin with a tetra address word over {w,x,y,z}
- canonical address tokens are dot-separated (e.g. `y.z.x`)
- compressed clusters such as `yzx` are treated as non-canonical and receive a suggestion.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
import json

ADDRESS_RE = re.compile(r"^[wxyz](?:\.[wxyz])*$")
CLUSTER_RE = re.compile(r"^[wxyz]+")
ADDRESS_PLUS_SUFFIX_RE = re.compile(r"^([wxyz](?:\.[wxyz])*)(\..+)$")


@dataclass(frozen=True)
class NamingIssue:
    path: str
    segment: str
    reason: str
    suggestion: str | None


@dataclass(frozen=True)
class RenameProposal:
    path: str
    proposed_path: str


@dataclass(frozen=True)
class CanonicalCollision:
    canonical_path: str
    paths: list[str]


def _segment_token(segment: str, *, is_leaf: bool) -> str:
    """Return segment token used for address checks.

    For leaf file names we strip the final extension only.
    For directory segments we keep the full segment so non-address suffixes
    remain visible to the audit (e.g. `x.w.Experiments`).
    """

    if not is_leaf:
        return segment
    if segment.startswith(".") and segment.count(".") == 1:
        return segment[1:]
    if "." not in segment:
        return segment
    token = segment.rsplit(".", 1)[0]
    return token if token else segment.lstrip(".")


def suggest_segment(segment: str, *, is_leaf: bool = False) -> str | None:
    """Suggest a canonicalized segment name when possible."""

    token = _segment_token(segment, is_leaf=is_leaf)
    if not token:
        return None
    if ADDRESS_RE.match(token):
        return None

    m = CLUSTER_RE.match(token)
    if not m:
        return None

    cluster = m.group(0)
    dotted = ".".join(cluster)
    suggestion = segment.replace(cluster, dotted, 1)
    return None if suggestion == segment else suggestion


def check_segment(segment: str, *, is_leaf: bool = False) -> tuple[bool, str, str | None]:
    """Validate a path segment under strict addressing rules."""

    token = _segment_token(segment, is_leaf=is_leaf)
    if ADDRESS_RE.match(token):
        return True, "ok", None

    if ADDRESS_PLUS_SUFFIX_RE.match(token):
        return False, "non-address suffix after tetra prefix", None

    suggestion = suggest_segment(segment, is_leaf=is_leaf)
    if suggestion and CLUSTER_RE.match(token):
        return False, "compressed address cluster (non-canonical)", suggestion
    return False, "missing tetra address prefix (manual naming required)", None


def audit_paths(paths: list[str]) -> list[NamingIssue]:
    issues: list[NamingIssue] = []
    for rel in paths:
        segments = rel.split("/")
        for i, segment in enumerate(segments):
            ok, reason, suggestion = check_segment(
                segment, is_leaf=(i == len(segments) - 1)
            )
            if not ok:
                issues.append(
                    NamingIssue(
                        path=rel,
                        segment=segment,
                        reason=reason,
                        suggestion=suggestion,
                    )
                )
                break
    return issues


def git_tracked_files(root: Path) -> list[str]:
    out = subprocess.check_output(["git", "-C", str(root), "ls-files"], text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def build_summary(root: Path) -> tuple[int, int, list[NamingIssue]]:
    files = git_tracked_files(root)
    issues = audit_paths(files)
    return len(files), len(issues), issues


def canonicalize_segment(segment: str, *, is_leaf: bool = False) -> str:
    """Return a canonicalized segment when conversion is possible."""

    suggestion = suggest_segment(segment, is_leaf=is_leaf)
    return suggestion or segment


def canonicalize_path(path: str) -> str:
    """Return path with canonicalized segments where possible."""

    segments = path.split("/")
    return "/".join(
        canonicalize_segment(segment, is_leaf=(i == len(segments) - 1))
        for i, segment in enumerate(segments)
    )


def build_rename_plan(paths: list[str]) -> list[RenameProposal]:
    """Build rename proposals for paths with deterministic canonicalization."""

    proposals: list[RenameProposal] = []
    for path in paths:
        proposed = canonicalize_path(path)
        if proposed != path:
            proposals.append(RenameProposal(path=path, proposed_path=proposed))
    return proposals


def find_canonical_collisions(paths: list[str]) -> list[CanonicalCollision]:
    """Return canonical path collisions where multiple files map to one target."""

    buckets: dict[str, list[str]] = {}
    for path in paths:
        canonical = canonicalize_path(path)
        buckets.setdefault(canonical, []).append(path)

    collisions = [
        CanonicalCollision(canonical_path=canonical, paths=sorted(originals))
        for canonical, originals in sorted(buckets.items())
        if len(originals) > 1
    ]
    return collisions


def write_rename_plan(root: Path, output_file: Path | None = None) -> Path:
    """Write rename proposal JSON for tracked files and return output path."""

    files = git_tracked_files(root)
    proposals = build_rename_plan(files)
    payload = {
        "tracked_files": len(files),
        "proposals": len(proposals),
        "items": [
            {"path": p.path, "proposed_path": p.proposed_path}
            for p in proposals
        ],
    }
    out = output_file or root / "y.Utilities" / "yx.DataArchive" / "tet_rename_plan.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    return out
