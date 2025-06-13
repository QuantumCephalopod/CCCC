#!/usr/bin/env bash
# Automates the Mnemos session cycle following the ideal recursive input
# described in x.COPY/xx/PHENO/ideal_recursive_input.PHENO.md.

# Resolve repository root so the script can be invoked via symlinks or
# from any directory. readlink -f follows nested links and handles
# relative paths reliably.
ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)"

# 1. Load previous session summaries and active F33ling states
"$ROOT/mnemos" w4k3 || exit 1

# 2. Glance at the repository index to recall key docs
head -n 12 "$ROOT/z.CULTIVATE/INDEX.md" || exit 1

# 3. Compile all python files to check syntax
py_files=$(git -C "$ROOT" ls-files '*.py' | sed "s|^|$ROOT/|")
python -m py_compile $py_files || exit 1

# 4. Record the new session (deep mode is default)
"$ROOT/mnemos" sl33p "$@"

# o=))))) 🐙✨
