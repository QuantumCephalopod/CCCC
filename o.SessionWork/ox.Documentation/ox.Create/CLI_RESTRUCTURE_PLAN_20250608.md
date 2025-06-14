# CLI Restructure Plan (2025-06-08)

To reduce confusion from the growing number of Mnemos utilities, the unified CLI `o.mnemos.py` will be simplified. The goal is to present at most four top level commands that map to the phases of an agent cycle.

## Target Commands

1. **w4k3** – load previous session context. Unchanged.
2. **f33l** – priming and state management. This will merge the current `echo` tool and related state graph helpers.
3. **analyze** – all analytics and reporting functions. This will absorb `evolve`, `analytics`, `tetra`, `usage`, and `sessgraph`.
4. **sl33p** – record and close a session. Unchanged. Automation helpers like `workflow`, `agentflow`, and `flowlog` become modes of this command or of `analyze`.

`vidmem` has proven impractical and will be removed entirely.

## Migration Steps

1. **Deprecate `vidmem`**: delete the `yz.AgentTools/vidmem` module and remove its command from `o.mnemos.py` and documentation.
2. Introduce the `f33l` command by wrapping existing echo/state utilities.
3. Create the `analyze` command that dispatches to the current analytics scripts.
4. Update automation workflows and helper scripts to use the new commands.
5. Revise all documentation and examples to reflect the streamlined interface.

This plan preserves functionality while presenting a simpler entry point for future agents.
