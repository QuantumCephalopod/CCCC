#!/usr/bin/env python3
"""Format transition metrics as Graphviz DOT string."""

from __future__ import annotations

from typing import Dict, Tuple


def transitions_to_dot(freqs: Dict[Tuple[str, str], float]) -> str:
    """Return DOT graph representing transitions."""
    lines = ["digraph F33lingGraph {"]
    for (src, dst), val in freqs.items():
        lines.append(f"    \"{src}\" -> \"{dst}\" [label={val:.2f}];")
    lines.append("}")
    return "\n".join(lines)

