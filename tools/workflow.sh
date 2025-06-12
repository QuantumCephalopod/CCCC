#!/usr/bin/env bash
# Automates the Mnemos session cycle following the ideal recursive input
# described in PHENO/ideal_recursive_input.PHENO.md.

# 1. Load previous session summaries and active F33ling states
python tools/AGENT_tools/o.mnemos.py w4k3 || exit 1

# 2. Glance at the repository index to recall key docs
head -n 12 cultivate/INDEX.md || exit 1

# 3. Compile all python files to check syntax
python -m py_compile $(git ls-files '*.py') || exit 1

# 4. Record the new session (deep mode is default)
python tools/AGENT_tools/o.mnemos.py sl33p "$@"

# o=))))) 🐙✨
