#!/usr/bin/env bash
# Automates the standard Mnemos session cycle: w4k3, tests, sl33p.

# Load previous session summaries
python AGENT_tools/o.mnemos.py w4k3 || exit 1

# Compile all python files to check syntax
python -m py_compile $(git ls-files '*.py') || exit 1

# Record the new session (deep mode is default)
python AGENT_tools/o.mnemos.py sl33p "$@"
