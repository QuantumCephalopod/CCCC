#!/usr/bin/env python3
"""Session continuity loader using tetrahedral submodules."""

from __future__ import annotations

import sys
import signal
from pathlib import Path

# Ensure package imports work when executed directly
ROOT = Path(__file__).resolve().parents[4]
TOOLS_PATH = ROOT / "y.Utilities" / "yz.AgentOps"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from yz.AgentTools.w4k3.z_summary import main


if __name__ == "__main__":
    # Avoid BrokenPipeError when piping output to commands like `head`.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
