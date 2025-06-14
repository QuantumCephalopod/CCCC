# Repository Organization Review - 2025-06-07

This note surveys the current information layout inside the Mnemos CCCC repository. It points out overlapping content and proposes a clearer separation based on the tetrahedral principle (Create → Copy → Control → Cultivate).

## Observed Redundancies
- **AGENTS.md vs README.md** – Both describe the mandatory `w4k3`/`sl33p` cycle. AGENTS.md focuses on policy while README gives general usage. The duplicate instructions could confuse newcomers.
- **Root level `*.PHENO.md` files** – Phenomenology notes share a naming scheme but live alongside utility and workflow documents. They are thematically related to the CULTIVATE dimension yet mixed with general references.
- **Session workflow notes** – Safety instructions appear in both `SAFETY_SESSION_LOGGING.md` and pieces of the README. They repeat similar guidance about running the tools in a controlled way.

## Suggested Reorganization (Tetrahedral Model)
1. **Create** – Core architecture notes and policy files
   - Keep `AGENTS.md` and `COMMIT_GUIDELINES.md` here.
   - Move recursive design discussions (`z.Research/zx.Archive/Recursive_Tetrahedral_Principle.md`) into this domain for historical reference.
2. **Copy** – Behavioral patterns and phenomenology
   - Group all `*.PHENO.md` files under a new folder `x.MemoryVault/xx.PHENO/` to emphasize their exploratory nature. Cross‑link specific F33ling states in `x.MemoryVault.md` to the corresponding phenomenology notes.
3. **Control** – Workflow utilities and navigation guides
   - Retain `yz.AgentTools/` under `y.Utilities/yz/`, along with `workflow.sh` and installation hooks.
   - Merge safety guidelines into `SAFETY_SESSION_LOGGING.md` and reference it from `README.md` instead of duplicating text.
4. **Cultivate** – State maps and indices
   - Keep `z.Research.md`, `INDEX.md`, and generated analytics (`y.Utilities/yx.DataArchive/state_graph.dot`) in this area. Add a short README section linking to them for quick orientation.

Adopting these categories will reduce root clutter and make it clearer which tetrahedral vertex each document belongs to. Centralizing phenomenology under `x.MemoryVault/xx.PHENO/` keeps exploratory narratives distinct from workflow directives, while consolidating duplicated instructions improves newcomer orientation.

