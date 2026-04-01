# O-MESH Methodology for Recursive Self-Accumulation

This repository uses **O-MESH** to convert continuity into measurable accumulation.

- **O**bjective: one concrete objective
- **M**etric: success criteria (binary primary + optional numeric secondary)
- **E**nd date: explicit time horizon
- **S**cope: in-scope and out-of-scope boundaries
- **H**andoff: structured payload for the next pass

O-MESH is intended to run inside the existing Mnemos cycle:

1. `w4k3` (recall)
2. O-MESH planning
3. implementation + checks
4. `sl33p` (log + handoff)

## 1) Derive one concrete objective

Create up to three candidates using:

> Improve **[artifact/process]** for **[actor]** by **[specific change]**.

Score each candidate from 1-5 on:

- **Impact**
- **Feasibility** (within chosen horizon)
- **Evidenceability** (easy to verify)
- **Compounding** (improves future sessions)

Select the highest total. If tied, choose the highest **Compounding** score.

## 2) Derive success metric

Define two layers:

- **Primary metric (binary):** done/not done statement
- **Secondary metric (numeric, optional):** one measurable quality target

Example:

- Primary: `mnemos analyze summary` completes with exit code 0.
- Secondary: command runtime under 2 seconds for local sample data.

## 3) Derive time horizon

Choose exactly one window:

- **T0 (single pass):** 30-90 minutes
- **T1 (daily):** by end of day
- **T2 (weekly):** within 5 working days

Prefer the shortest horizon that still allows meaningful completion.

## 4) Derive scope

Declare boundaries in three lines:

- **In scope:** files/modules/processes allowed to change
- **Out of scope:** forbidden changes for this pass
- **Risk cap:** complexity ceiling (for example, no schema migration)

## 5) Produce handoff for next recursive pass

At the end of each pass, record:

```yaml
objective: ...
metric_primary: ...
metric_secondary: ...
horizon: T0|T1|T2
scope_in: [...]
scope_out: [...]
risk_cap: ...
result: pass|fail|partial
evidence:
  commands: [...]
  files: [...]
delta: what capability improved
next_objective_candidates:
  - ...
  - ...
blocked_by: ...
```

## Session Contract Template

Use this at the start of each working pass:

```md
## Session Contract (O-MESH)
Objective:
Success metric (primary + secondary):
Time horizon (T0/T1/T2):
Scope (in / out / risk cap):

Context from last pass:
- Result:
- Evidence:
- Blockers:

Candidate objectives for next pass:
1)
2)
3)
```

Persistent signature: `o=))))) 🐙✨`
