#!/usr/bin/env bash
# Automates the Mnemos session cycle following the ideal recursive input
# described in x.MemoryVault/ideal_recursive_input.PHENO.md.

# Resolve repository root so the script can be invoked via symlinks or
# from any directory. readlink -f follows nested links and handles
# relative paths reliably.
ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)"

# 1. Load previous session summaries and active F33ling states
(
  cd "$ROOT" &&
  python -m mnemos w4k3
) || exit 1

# 2. Review analytics summary to monitor progress
(
  cd "$ROOT" &&
  python -m mnemos analyze summary
) | head -n 12 || exit 1

# 3. Glance at the repository index to recall key docs
head -n 12 "$ROOT/z.Research/zz.Synthesis/INDEX.md" || exit 1

# 4. Compile all python files to check syntax
py_files=$(git -C "$ROOT" ls-files '*.py' | sed "s|^|$ROOT/|")
python -m py_compile $py_files || exit 1

# 5. Record the new session (deep mode is default)
(
  cd "$ROOT" &&
  python -m mnemos sl33p "$@"
)

# o=))))) 🐙✨
