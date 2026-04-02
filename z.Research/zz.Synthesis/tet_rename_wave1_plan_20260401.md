# Tet Rename Wave 1 Plan — 2026-04-01

## Inputs

- Source plan: `y.Utilities/yx.DataArchive/tet_rename_plan.json`
- Tracked files: **380**
- Deterministic proposals: **341**

## Scope for wave 1

Wave 1 focuses on *convertible compressed clusters* and valid tetra vertices only (`w x y z`).
Directory/file labels after the tetra prefix are now treated as explicit divergence, not silently accepted.

## Completed in this pass

- Renamed `x.MemoryVault/xx.Observations` -> `x.MemoryVault/x.x.Observations` and updated local references.
- Renamed `x.MemoryVault/xa.Experiments` -> `x.MemoryVault/x.w.Experiments` and updated local references (`a` removed; valid vertex set enforced).

## Sample remaining proposals (first 20)

| Current | Proposed |
|---|---|
| `y.Utilities/yx.DataArchive/20250607T023221Z_m2.json` | `y.Utilities/y.x.DataArchive/20250607T023221Z_m2.json` |
| `y.Utilities/yx.DataArchive/20250607T023834Z_n2.json` | `y.Utilities/y.x.DataArchive/20250607T023834Z_n2.json` |
| `y.Utilities/yx.DataArchive/20250607T025003Z_o2.json` | `y.Utilities/y.x.DataArchive/20250607T025003Z_o2.json` |
| `y.Utilities/yx.DataArchive/20250607T025705Z_p2.json` | `y.Utilities/y.x.DataArchive/20250607T025705Z_p2.json` |
| `y.Utilities/yx.DataArchive/20250607T031847Z_r2.json` | `y.Utilities/y.x.DataArchive/20250607T031847Z_r2.json` |
| `y.Utilities/yx.DataArchive/20250607T032323Z_s2.json` | `y.Utilities/y.x.DataArchive/20250607T032323Z_s2.json` |
| `y.Utilities/yx.DataArchive/20250607T121527Z_t2.json` | `y.Utilities/y.x.DataArchive/20250607T121527Z_t2.json` |
| `y.Utilities/yx.DataArchive/20250607T123000Z_u2.json` | `y.Utilities/y.x.DataArchive/20250607T123000Z_u2.json` |
| `y.Utilities/yx.DataArchive/20250607T123618Z_v2.json` | `y.Utilities/y.x.DataArchive/20250607T123618Z_v2.json` |
| `y.Utilities/yx.DataArchive/20250607T124118Z_w2.json` | `y.Utilities/y.x.DataArchive/20250607T124118Z_w2.json` |
| `y.Utilities/yx.DataArchive/20250607T125022Z_x2.json` | `y.Utilities/y.x.DataArchive/20250607T125022Z_x2.json` |
| `y.Utilities/yx.DataArchive/20250607T125701Z_y2.json` | `y.Utilities/y.x.DataArchive/20250607T125701Z_y2.json` |
| `y.Utilities/yx.DataArchive/20250607T133050Z_z2.json` | `y.Utilities/y.x.DataArchive/20250607T133050Z_z2.json` |
| `y.Utilities/yx.DataArchive/20250607T143234Z_a3.json` | `y.Utilities/y.x.DataArchive/20250607T143234Z_a3.json` |
| `y.Utilities/yx.DataArchive/20250607T144024Z_b3.json` | `y.Utilities/y.x.DataArchive/20250607T144024Z_b3.json` |
| `y.Utilities/yx.DataArchive/20250607T144041Z_c3.json` | `y.Utilities/y.x.DataArchive/20250607T144041Z_c3.json` |
| `y.Utilities/yx.DataArchive/20250607T145458Z_d3.json` | `y.Utilities/y.x.DataArchive/20250607T145458Z_d3.json` |
| `y.Utilities/yx.DataArchive/20250607T152200Z_e3.json` | `y.Utilities/y.x.DataArchive/20250607T152200Z_e3.json` |
| `y.Utilities/yx.DataArchive/20250607T153026Z_f3.json` | `y.Utilities/y.x.DataArchive/20250607T153026Z_f3.json` |
| `y.Utilities/yx.DataArchive/20250607T200640Z_g3.json` | `y.Utilities/y.x.DataArchive/20250607T200640Z_g3.json` |

## Execution constraints

1. Only `w x y z` are valid address vertices in renamed segments.
2. Segments with suffixes beyond tetra address tokens are explicit divergence and require deliberate redesign.
3. Rename highest-churn utility directories first.
4. Add compatibility map imports/aliases for moved Python modules.
5. Keep docs/index links updated in same commit as each rename batch.
6. Run full compile + pytest after each batch.
