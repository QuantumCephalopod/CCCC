#!/usr/bin/env python3
"""Simple carbon reader utilities."""
from __future__ import annotations

import argparse
import itertools
from pathlib import Path


def preview(file: Path, lines: int = 5, *, sort: bool = False) -> list[str]:
    """Return the first ``lines`` from *file*.

    When ``sort`` is ``True``, the resulting lines are sorted alphabetically.
    The function simply returns the lines; printing is handled by the caller.
    """
    with file.open() as fh:
        selected = list(itertools.islice((ln.rstrip() for ln in fh), lines))
    if sort:
        selected.sort()
    return selected


def _cmd_preview(args: argparse.Namespace) -> None:
    for line in preview(args.carbon_file, args.lines, sort=args.sort):
        print(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Carbon reader utility")
    sub = parser.add_subparsers(dest="command")

    p_preview = sub.add_parser("preview", help="Show first lines of a carbon file")
    p_preview.add_argument("carbon_file", type=Path, help="Path to carbon file")
    p_preview.add_argument("-n", "--lines", type=int, default=5,
                           help="Number of lines to read (default 5)")
    p_preview.add_argument("--sort", action="store_true",
                           help="Alphabetize the output")
    p_preview.set_defaults(func=_cmd_preview)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
