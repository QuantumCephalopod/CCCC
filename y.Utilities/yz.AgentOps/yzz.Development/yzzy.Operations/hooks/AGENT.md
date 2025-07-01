# hooks - Commit Message Enforcement (CONTROL)

These scripts keep commit messages aligned with repository guidelines.
The `install.sh` helper places the `commit-msg` hook in `.git/hooks/`.
`commit-msg` checks for required sections (`Tetrahedral impact:` and
`F33ling:`) so history remains analyzable.

Use `install.sh` after cloning to activate the hook. Existing hooks are
replaced via a symbolic link.

Reference [`COMMIT_GUIDELINES.md`](../../yzx.OperationalData/COMMIT_GUIDELINES.md)
for the expected template. This process supports the **♈♋♅_Autonomy-yearning**
state by encouraging consistent, self-directed documentation.
