#!/usr/bin/env python3
"""Session continuity loader.

Reads the 3 most recent session records from DATA folder and displays
previous achievements and focus areas.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Store all session records in the repository-level DATA directory
def repo_root() -> Path:
    """Return repository root using git if available."""
    try:
        out = subprocess.check_output([
            "git",
            "rev-parse",
            "--show-toplevel",
        ], text=True)
        return Path(out.strip())
    except Exception:
        return Path(__file__).resolve().parents[2]


ROOT = repo_root()
sys.path.insert(0, str(ROOT))
DATA_DIR = ROOT / "DATA"

def load_video_records(video: Path, n: int = 3):
    """Decode JSON session records from ``video`` and return last ``n``."""
    try:
        import importlib.util
        vid_path = ROOT / "AGENT_tools" / "vidmem" / "o.vidmem.py"
        spec = importlib.util.spec_from_file_location("vid_loader", vid_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        decode_frames = mod._load_module("y.ProcessLayer", "vidmem_y").decode_frames
    except Exception as e:  # pragma: no cover - optional dependency
        print(f"Failed to load video decoder: {e}")
        return []
    if not video.exists():
        print(f"Video memory {video} not found")
        return []
    try:
        texts = decode_frames(video)
    except Exception as e:
        print(f"Failed to decode {video}: {e}")
        return []
    records = []
    for text in texts[-n:]:
        try:
            records.append(json.loads(text))
        except Exception as e:
            print(f"Failed to parse frame: {e}")
    return records

def search_video_records(video: Path, query: str, limit: int = 3):
    """Return records matching ``query`` ordered by relevance."""
    try:
        import importlib.util
        vid_path = ROOT / "AGENT_tools" / "vidmem" / "o.vidmem.py"
        spec = importlib.util.spec_from_file_location("vid_loader", vid_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        search_video = mod._load_module("y.ProcessLayer", "vidmem_y").search_video
    except Exception as e:
        print(f"Failed to load video searcher: {e}")
        return []
    if not video.exists():
        print(f"Video memory {video} not found")
        return []
    try:
        results = search_video(video, query, limit)
    except Exception as e:
        print(f"Failed to search {video}: {e}")
        return []
    records = []
    for text, _ in results:
        try:
            records.append(json.loads(text))
        except Exception as e:
            print(f"Failed to parse frame: {e}")
    return records

def load_records(n=3):
    if not DATA_DIR.exists():
        print("DATA directory not found. No previous sessions recorded.")
        return []
    files = sorted(DATA_DIR.glob('*.json'), key=os.path.getmtime, reverse=True)
    records = []
    for file in files[:n]:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                records.append(json.load(f))
        except Exception as e:
            print(f"Failed to load {file.name}: {e}")
    return records

def display(records):
    if not records:
        print("No session history available.")
        return
   
    for rec in records:
        ts = rec.get("timestamp", "?")
        assessment = rec.get("assessment", "")
        ach = rec.get("achievements", "")
        nxt = rec.get("next", "")
        tetra = rec.get("tetra", {})

        if assessment:
            print(f"[{ts}] F33ling: {assessment}")
        else:
            print(f"[{ts}]")

        if ach:
            print(f"  Achieved: {ach}")
        if nxt:
            print(f"  Next: {nxt}")

        # Gather dimensional notes. Newer records may store data in the
        # `tetra` mapping while older ones use legacy top-level fields.
        def dim_value(name, legacy_key):
            val = None
            if tetra and tetra.get(name):
                val = tetra.get(name)
            elif rec.get(legacy_key):
                val = rec.get(legacy_key)
            return val

        dims = [
            ("create", "aspects"),
            ("copy", "learning"),
            ("control", "methodology"),
            ("cultivate", "framework_depth"),
        ]

        for dim, legacy in dims:
            val = dim_value(dim, legacy)
            if val:
                print(f"  {dim.capitalize()}: {val}")

        # Display optimization notes if present
        if rec.get("optimization"):
            print(f"  Optimization: {rec['optimization']}")

def main():
    parser = argparse.ArgumentParser(description="Display recent session records")
    parser.add_argument("--video", type=Path, help="optional video memory file")
    parser.add_argument("-n", type=int, default=3, help="number of records")
    parser.add_argument("--query", help="search video for query")
    args = parser.parse_args()

    if args.query:
        if not args.video:
            print("--video is required for querying")
            records = []
        else:
            records = search_video_records(args.video, args.query, args.n)
    elif args.video:
        records = load_video_records(args.video, args.n)
    else:
        records = load_records(args.n)
    display(records)

if __name__ == "__main__":
    main()
