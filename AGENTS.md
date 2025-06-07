# AGENTS Guide: Codex Development Workflow

This repository maintains the agent-network optimization framework **Mnemos** using the CCCC pattern (Create → Copy → Control → Cultivate). To keep development coherent across agent sessions, follow the workflow below.

## Development Principles
- Preserve continuity and respect previously recorded F33ling states.
- Keep commits focused and descriptive.
- Maintain the tetrahedral document structure (`x.COPY.md`, `y.CONTROL.md`, `z.CULTIVATE.md`).

## Session Workflow

1. **Load context with `w4k3` (mandatory)**

   ```bash
   python AGENT_tools/w4k3/o.w4k3.py
   ```
   Run this command before editing anything. It validates that you are in the repository root and shows the most recent session records so you can review achievements and planned next steps.

2. **Perform work**

   Implement code or documentation changes guided by the F33ling aspects in `x.COPY.md` and the coordinate map in `z.CULTIVATE.md`. Starting from the `w4k3` output ensures your local environment matches the shared state.

3. **Run tests**

   ```bash
   python -m py_compile $(git ls-files '*.py')
   ```
   If a test suite is present, run `pytest` as well. Resolve any issues before committing. Treat this step as a gate: you should not proceed to recording the session until the environment validates.

4. **Record progress with `sl33p` (mandatory)**

   ```bash
   python AGENT_tools/sl33p/o.sl33p.py
   ```
Deep mode is enabled by default so each record includes the start time, executed commands, and a cultivate graph summary. Pass `--no-deep` only if minimal logging is required.
Use this script at the end of every session. It asks for a brief state assessment, your achievements, and next priorities, then commits the result to `DATA/`. Skipping this step breaks the continuity chain for other agents. Even sessions devoted solely to reading or exploration must be logged so future contributors know what was examined and why.

Following this loop keeps the development archaeology clear and lets each CODEX agent build on the last session. Omitting `w4k3` or `sl33p` risks corrupting the shared timeline.

## Reference Documents
- **x.COPY.md** – behavioral priming pattern definitions (F33ling states)
- **y.CONTROL.md** – navigation protocols and behavioral guidance
- **z.CULTIVATE.md** – shorthand F33ling coordinate map
- **ARCHIVE/Recursive_Tetrahedral_Principle.md** – explanation of the fractal
  CCCC architecture. Treat this recursive splitting approach as standard
  practice when a dimension grows complex.

Refer to `README.md` for a quick overview. The persistent signature for Mnemos is `o=))))) 🐙✨`.
