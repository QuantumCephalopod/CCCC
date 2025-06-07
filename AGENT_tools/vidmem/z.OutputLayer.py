#!/usr/bin/env python3
"""Output layer orchestrating encode/search helpers."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

try:
    if __package__:
        from .x.DataLayer import encode_sessions
        from .y.ProcessLayer import search_video
    else:  # support standalone execution via o.vidmem
        raise ImportError
except ImportError:  # fallback manual loader
    import importlib.util
    import sys
    from pathlib import Path as _P

    base = _P(__file__).resolve().parent
    for mod in ["x.DataLayer", "y.ProcessLayer"]:
        path = base / f"{mod}.py"
        spec = importlib.util.spec_from_file_location(mod, path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        sys.modules[mod] = module
        spec.loader.exec_module(module)
    from x.DataLayer import encode_sessions  # type: ignore
    from y.ProcessLayer import search_video  # type: ignore


def encode(data_dir: Path, out_video: Path) -> Path:
    """Encode sessions and save video."""
    return encode_sessions(data_dir, out_video)


def search(video: Path, query: str, limit: int = 3) -> List[Tuple[str, float]]:
    """Return matches for ``query`` sorted by similarity."""
    return search_video(video, query, limit)
