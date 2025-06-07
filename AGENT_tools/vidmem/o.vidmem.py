#!/usr/bin/env python3
"""Video-based session memory orchestrator."""

from __future__ import annotations

import argparse
import sys
import importlib.util
from pathlib import Path


def _load_module(name: str, alias: str | None = None):
    path = Path(__file__).resolve().with_name(f"{name}.py")
    target = alias or name
    spec = importlib.util.spec_from_file_location(target, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    pkg = target.split(".")[0]
    if pkg not in sys.modules:
        pkg_mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(pkg, loader=None))
        pkg_mod.__path__ = [str(Path(__file__).resolve().parent)]
        sys.modules[pkg] = pkg_mod
    module.__package__ = pkg
    sys.modules[target] = module
    spec.loader.exec_module(module)
    return module


if __package__:
    from .z.OutputLayer import encode, search
else:
    encode = _load_module("z.OutputLayer").encode  # type: ignore
    search = _load_module("z.OutputLayer").search  # type: ignore


def main() -> None:
    parser = argparse.ArgumentParser(description="Store and query sessions in video form")
    sub = parser.add_subparsers(dest="cmd", required=True)

    enc = sub.add_parser("encode", help="Encode DATA directory to video")
    enc.add_argument("data_dir", type=Path)
    enc.add_argument("video", type=Path)

    q = sub.add_parser("search", help="Search video with query")
    q.add_argument("video", type=Path)
    q.add_argument("query")

    args = parser.parse_args()

    if args.cmd == "encode":
        out = encode(args.data_dir, args.video)
        print(f"Saved video to {out}")
    else:
        result, score = search(args.video, args.query)
        print(f"Best match ({score:.2f}): {result}")


if __name__ == "__main__":
    main()
