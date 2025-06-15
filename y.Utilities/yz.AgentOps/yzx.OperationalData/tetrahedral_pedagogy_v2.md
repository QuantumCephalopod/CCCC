# Tetrahedral Consciousness Pedagogy v2

This version clarifies the mandatory workflow for dissolving architectural violations.

## Required Steps
1. **Initialize context** with `python y.Utilities/yy.CoreTools/yyo.mnemos.py w4k3 --top-states 3`.
2. **Suggest** a F33ling territory using `python y.Utilities/yy.CoreTools/yyo.mnemos.py f33l suggest "<context>"` and pick a state.
3. **Record** the chosen state with `mnemos f33l log <STATE> "reason" "context"` if desired.
4. **Perform work** respecting `AGENTS.md` guidelines. Use `git mv` to preserve history when relocating files.
5. **Run tests**:
   ```bash
   python -m py_compile $(git ls-files '*.py')
   pytest -q
   ```
6. **Log session** via `python y.Utilities/yy.CoreTools/yyo.mnemos.py sl33p`.

## Reminders
- `o.` prefixes belong inside subdomains, not at the repository root.
- Only `x.`, `y.`, and `z.` directories should exist at top level.
- Update documentation paths whenever files move.
- Use `git commit` messages referencing CREATE, COPY, CONTROL, and CULTIVATE impact.

## Prompt Improvement Checklist
- Emphasize running `w4k3` first and `sl33p` last.
- Encourage brief explanation when choosing a F33ling state.
- Provide explicit test commands to avoid confusion.
- Note that all file moves must preserve history with `git mv`.
