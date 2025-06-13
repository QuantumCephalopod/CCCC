# Repository Consolidation Plan (2025-06-12)

The Mnemos repository has expanded rapidly. Documentation, tools and logs now span many folders. This plan summarizes steps to coalesce related files and lighten the root directory while preserving the tetrahedral layout.

## 1. Group by Tetrahedral Domain

- **Create** – policy and architecture notes
  - Keep `AGENTS.md`, `COMMIT_GUIDELINES.md`, and `ARCHIVE/Recursive_Tetrahedral_Principle.md` here.
  - Move scattered design references into a `o.CREATE/docs/create/` folder.
- **Copy** – experiential patterns and phenomenology
  - Retain `x.COPY.md` and gather all `*.PHENO.md` under `x.COPY/xx/PHENO/`.
  - Cross‑link PHENO notes from the relevant COPY aspects to simplify navigation.
- **Control** – workflow utilities and safety guides
  - Store `AGENT_tools/`, `workflow.sh`, and `SAFETY_SESSION_LOGGING.md` under `y.CONTROL/yz/`.
  - Consolidate CLI usage examples in a single `o.CREATE/docs/control/README.md`.
- **Cultivate** – indices and state maps
  - Keep `z.CULTIVATE.md`, `INDEX.md`, and analytics outputs (`DATA/state_graph.dot`, summaries) in a `z.CULTIVATE/` folder.
  - Reference these from the root README so new contributors know where to look.

## 2. Archive Legacy Notes

Move older reports in `ARCHIVE/` to dated subfolders (e.g., `ARCHIVE/2025-06`), keeping the root archive tidy. Compress session logs older than one month into zip files or transfer them to long‑term storage.

## 3. Streamline the CLI

Follow the earlier [CLI Restructure Plan](CLI_RESTRUCTURE_PLAN_20250608.md) so that `o.mnemos.py` exposes only four top-level commands: `w4k3`, `f33l`, `analyze`, and `sl33p`. Remove deprecated helpers (`echo`, `vidmem`) once documentation is updated.

## 4. Consolidate Documentation

- Merge repeated workflow descriptions from README and AGENTS.md, leaving AGENTS.md focused on policy while README covers quick start usage.
- Provide a short `o.CREATE/docs/overview.md` linking to the tetrahedral domains and major tools.

## 5. Maintain Clean History

Continue using `w4k3` and `sl33p` for each session. Summarize consolidation progress in commit messages using the recommended template.

Adopting these steps will keep the repository coherent as it grows and make it easier for new agents to find information.

