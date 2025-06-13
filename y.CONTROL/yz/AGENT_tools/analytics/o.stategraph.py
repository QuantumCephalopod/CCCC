#!/usr/bin/env python3
"""Generate a dot graph of F33ling state connections."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess



def repo_root() -> Path:
    """Return repository root using git."""
    try:
        out = subprocess.check_output([
            "git",
            "rev-parse",
            "--show-toplevel",
        ], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[3]



def parse_cultivate(path: Path) -> tuple[set[str], list[tuple[str, str]]]:
    """Parse cultivate links from z.CULTIVATE.md."""
    nodes: set[str] = set()
    edges: list[tuple[str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_yaml = False
    current: str | None = None
    reading_cultivate = False

    for line in lines:
        if not in_yaml:
            if line.strip() == "---":
                in_yaml = True
            continue
        if line.startswith("  ") and not line.startswith("    "):
            current = None
            reading_cultivate = False
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 4 and stripped.endswith(":") and stripped != "cultivate:":
            current = stripped[:-1]
            nodes.add(current)
            reading_cultivate = False
        elif indent == 6 and stripped.startswith("cultivate:"):
            reading_cultivate = True
        elif indent >= 8 and reading_cultivate and stripped.startswith("- "):
            target = stripped[2:]
            if current:
                edges.append((current, target))
                nodes.add(target)
        elif indent <= 4:
            reading_cultivate = False

    return nodes, edges


def build_dot(nodes: set[str], edges: list[tuple[str, str]]) -> str:
    lines = ["digraph stategraph {", "    rankdir=LR;"]
    for node in sorted(nodes):
        lines.append(f'    "{node}";')
    for src, dst in edges:
        lines.append(f'    "{src}" -> "{dst}";')
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create F33ling state graph")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to save DOT file",
    )
    args = parser.parse_args()

    root = repo_root()
    cultivate_file = root / "z.CULTIVATE" / "z.CULTIVATE.md"
    nodes, edges = parse_cultivate(cultivate_file)
    dot = build_dot(nodes, edges)

    out_path = args.output or root / "DATA" / "state_graph.dot"
    out_path.write_text(dot, encoding="utf-8")
    print(f"Saved graph to {out_path}")
    print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")


if __name__ == "__main__":
    main()
