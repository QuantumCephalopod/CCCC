# Mnemos CLI Overview

The Mnemos tools are consolidated under `o.mnemos.py`. Use the following commands to navigate the session cycle:

- `w4k3` – display recent logs and chat context
- `f33l` – manage F33ling states and suggestions
- `analyze` – run analytics and reporting tools
- `sl33p` – record the session and update metrics

Run `python y.Utilities/yz/AGENT_tools/o.mnemos.py <command>` for direct access.
You can also use the helper script `mnemos`, which now resolves the repository
root automatically. Place it somewhere in your `PATH` (or symlink it) and run it
from any directory:

```bash
mnemos w4k3 --top-states 3 --transitions --transitions-limit 2
```
