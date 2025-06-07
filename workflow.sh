#!/usr/bin/env bash
# Automates the standard Mnemos session cycle: w4k3, tests, sl33p.

# Load previous session summaries
python AGENT_tools/w4k3/o.w4k3.py || exit 1

# Compile all python files to check syntax
python -m py_compile $(git ls-files '*.py') || exit 1

# Record the new session
python AGENT_tools/sl33p/o.sl33p.py "$@"
