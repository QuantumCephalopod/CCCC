"""Python entry point for the Mnemos CLI."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "y.Utilities" / "yy.CoreTools" / "yyo.mnemos.py"

# Ensure repo paths are on sys.path for imports used by the CLI
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "y.Utilities" / "yz.AgentOps"))

spec = importlib.util.spec_from_file_location("mnemos_cli", CLI)
module = importlib.util.module_from_spec(spec)
loader = spec.loader
assert loader is not None
loader.exec_module(module)


def main() -> int:
    """Entry point used by `python -m mnemos` or `python mnemos.py`."""
    return module.main()

if __name__ == "__main__":
    raise SystemExit(main())
