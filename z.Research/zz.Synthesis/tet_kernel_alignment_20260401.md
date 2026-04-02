# Tet Kernel Alignment Pass — 2026-04-01

## Purpose

Align repository language and conventions with the geometry-first `.tet` kernel:

- tensors as the only substrate,
- recursive tetrahedral addressing,
- operator-based reading,
- positional parsing as first-class behavior.

This pass does not introduce a full runtime. It establishes canonical naming and interpretation rules so future implementation work can remain coherent.

## Canonical Address Semantics

### 1) Address is recursive descent

Addresses such as `w`, `x.w`, `y.y.z`, and `z.w.w.w` are locality paths through recursive tetrahedral subdivision.

- each symbol is a directional branch decision,
- each `.` appends one further descent step,
- address length corresponds to recursive depth.

### 2) Global alphabet + local basis closure

Use global direction alphabet `{w, x, y, z}`.

Context selectors (`P/E/F/T`) define local basis arity:

- `P` opens 1 direction,
- `E` opens 2,
- `F` opens 3,
- `T` opens 4.

Within a context, recursive address expansion is closed over only the selected basis.

### 3) `.` is propagation, not namespace

`a.b.c` must be interpreted as chained propagation/concatenation through tensor structure, not symbolic namespacing.

### 4) Name tensors (0D)

A name (for example `.günther`) is a 0D tensor concatenated into expression structure.

- `value.günther` inserts into named shadow,
- `T.günther` projects from named shadow.

Same-name contributions coalesce globally.

## Operator Model (Repository Contract)

The repository should treat the following as kernel-level semantics:

- `.` propagation / concatenation,
- `:` rank-up recursive growth,
- `@` temporal reading,
- `>` morphism (preferred over two-symbol `->`),
- `⊥` positional rendering,
- `L` outward rendering operator.

Operator stacks are valid. Reading order should be defined after positional-grid parse.

## Parsing Priority

Interpretation order:

1. positional grid (columns/rows),
2. context basis selection (`P/E/F/T`),
3. address validation under local basis closure,
4. operator evaluation (left-to-right, top-to-bottom inside parsed grid).

This preserves the claim that position is itself an operator.

## Cascade Direction Contract

Cascade is not scheduled as a separate object. It emerges from reading direction:

- small -> big = emergence,
- big -> small = constraint.

Any future implementation should encode direction in traversal/read relations, not in external scheduler entities.

## Repository Conventions to Adopt

### A. Documentation vocabulary

When discussing `.tet` behavior, prefer these exact terms:

- **address** = recursive descent path,
- **basis** = local open directions selected by context,
- **concatenation** = tensor propagation,
- **shadow** = same-name global coalesced tensor,
- **rendering** = outward projection,
- **projection** (`⊥`) = positional readout at column.

### B. Symbol normalization

Prefer `>` in new kernel prose and implementation notes. Keep `->` only where compatibility is explicitly documented.

### C. Minimal implementation checklist for upcoming code passes

1. Add explicit address parser with basis-closure validation.
2. Add explicit operator-stack parser that keeps left-of-`@` referent rule.
3. Add positional grid phase before operator execution.
4. Add named-shadow coalescence behavior with highest-dimensional contribution resolution.

## Non-goals of this pass

- No claim that existing Mnemos utilities are a `.tet` runtime.
- No forced migration of historical docs to new symbols.
- No scheduler rewrite.

This document is a continuity bridge: it aligns language now so runtime behavior can be implemented later without semantic drift.
