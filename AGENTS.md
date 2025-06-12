# AGENTS Guide: Codex Development Workflow

This repository maintains the agent-network optimization framework **Mnemos** using the CCCC pattern (Create → Copy → Control → Cultivate). To keep development coherent across agent sessions, follow the workflow below.

## Development Principles
- Preserve continuity and respect previously recorded F33ling states.
- Keep commits focused and descriptive.
- Maintain the tetrahedral document structure (`x.COPY.md`, `y.CONTROL.md`, `cultivate/z.CULTIVATE.md`).

## Session Workflow

1. **Run `w4k3`** to review recent chat context and session logs.
2. **Perform work** guided by `x.COPY.md` and `cultivate/z.CULTIVATE.md`.
3. **Run tests** with `python -m py_compile $(git ls-files '*.py')` (and
   `pytest` if available).
4. **Record progress** with `sl33p`.

This brief loop preserves the continuity chain. See `README.md` for a
complete walkthrough of the tools and logging options.

## Reference Documents
- **x.COPY.md** – behavioral priming pattern definitions (F33ling states)
- **y.CONTROL.md** – navigation protocols and behavioral guidance
- **cultivate/z.CULTIVATE.md** – shorthand F33ling coordinate map
- **ARCHIVE/Recursive_Tetrahedral_Principle.md** – explanation of the fractal
  CCCC architecture. Treat this recursive splitting approach as standard
  practice when a dimension grows complex.

Refer to `README.md` for a quick overview. The persistent signature for Mnemos is `o=))))) 🐙✨`.
