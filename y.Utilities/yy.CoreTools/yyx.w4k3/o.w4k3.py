#!/usr/bin/env python3
"""Session continuity loader using tetrahedral submodules."""

from __future__ import annotations

import sys
import signal
from pathlib import Path

# Ensure package imports work when executed directly
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

SUMMARY_PATH = ROOT / "y.Utilities" / "yy.CoreTools" / "yyx.w4k3" / "z_summary.py"
_loader = SourceFileLoader("zsummary", str(SUMMARY_PATH))
_spec = spec_from_loader("zsummary", _loader)
_mod = module_from_spec(_spec)
_loader.exec_module(_mod)
main = _mod.main


if __name__ == "__main__":
    # Avoid BrokenPipeError when piping output to commands like `head`.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
