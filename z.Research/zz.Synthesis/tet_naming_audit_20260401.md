# Tet Naming Audit — 2026-04-01

## Why this audit

The repository currently mixes tetra-inspired naming and legacy labels. This audit checks strict recursive address naming (`w/x/y/z` dot words) and highlights where names diverge.

## Snapshot

- Tracked files scanned: **380**
- Files with first-segment/path naming divergence: **380**
- Strict compliance rate: **0.0%**

## Top divergent examples (first 20)

| Path | First divergent segment | Reason | Suggested normalization |
|---|---|---|---|
| `.gitignore` | `.gitignore` | missing tetra address prefix | `—` |
| `.gitmessage` | `.gitmessage` | missing tetra address prefix | `—` |
| `AGENTS.md` | `AGENTS.md` | missing tetra address prefix | `—` |
| `AGENT_PERSONA.md` | `AGENT_PERSONA.md` | missing tetra address prefix | `—` |
| `O-MESH.md` | `O-MESH.md` | missing tetra address prefix | `—` |
| `README.md` | `README.md` | missing tetra address prefix | `—` |
| `carbon_reader.md` | `carbon_reader.md` | missing tetra address prefix | `—` |
| `carbon_reader.py` | `carbon_reader.py` | missing tetra address prefix | `—` |
| `mnemos.py` | `mnemos.py` | missing tetra address prefix | `—` |
| `mnemos/__init__.py` | `mnemos` | missing tetra address prefix | `—` |
| `mnemos/__main__.py` | `mnemos` | missing tetra address prefix | `—` |
| `mnemos/tet_kernel.py` | `mnemos` | missing tetra address prefix | `—` |
| `mnemos/tet_naming.py` | `mnemos` | missing tetra address prefix | `—` |
| `tests/test_carbon_reader.py` | `tests` | missing tetra address prefix | `—` |
| `tests/test_sl33p_record.py` | `tests` | missing tetra address prefix | `—` |
| `tests/test_tet_kernel.py` | `tests` | missing tetra address prefix | `—` |
| `tests/test_tet_naming.py` | `tests` | missing tetra address prefix | `—` |
| `x.MemoryVault/AGENT.md` | `x.MemoryVault` | non-address suffix after tetra prefix | `—` |
| `x.MemoryVault/INDEX.md` | `x.MemoryVault` | non-address suffix after tetra prefix | `—` |
| `x.MemoryVault/control.PHENO.md` | `x.MemoryVault` | non-address suffix after tetra prefix | `—` |

## Immediate alignment strategy

1. Introduce canonical dotted address prefixes for new files only (no mass rename yet).
2. Add a pre-commit naming audit mode to prevent drift.
3. Migrate highest-churn directories first (`y.Utilities/*`, then `z.Research/*`).
4. Keep compatibility aliases/symlinks or index maps while migrating legacy names.
5. Enforce `w/x/y/z` as the only legal vertex alphabet for renamed segments.
