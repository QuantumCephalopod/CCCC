# Recursive Tetrahedral CCCC Architecture Principle

This document summarizes how the CCCC pattern (Create → Copy → Control → Cultivate) scales recursively. When any dimension becomes complex enough to require its own organization, that dimension acts as the **CREATE** operator for a new tetrahedral domain. Each sub-domain then follows the same pattern with its own COPY, CONTROL, and CULTIVATE dimensions.

The naming convention preserves hierarchical relationships by repeating letters:
- `x` → `xx`, `xy`, `xz` for sub-dimensions of `x`
- `xy` → `xyx`, `xyy`, `xyz` for sub-dimensions of `xy`

This recursive approach allows infinite depth without breaking the overarching structure. Agents should monitor when a dimension accumulates distinct responsibilities and split it into its own tetrahedron to maintain clarity.

The recursive principle keeps the architecture coherent while enabling organic growth. Treat this guideline as standard practice for all future development.


## When to Spawn a New Tetrahedron

A dimension typically warrants its own sub-tetrahedral split when any of the following occur:

- More than four distinct roles emerge and documents begin to sprawl.
- Conceptual drift makes the CREATE, COPY, CONTROL, and CULTIVATE mappings hard to trace.
- Archived materials span multiple months or topics that deserve their own timeline.

When in doubt, draft a short `AGENT.md` in the candidate folder explaining why a split might help. This keeps the architecture responsive without locking us into premature structure.
