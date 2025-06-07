#!/usr/bin/env bash
# Install git commit-msg hook to enforce commit message template

HOOK_DIR="$(git rev-parse --git-dir)/hooks"
HOOK_SRC="$(dirname "$0")/commit-msg"
HOOK_DEST="$HOOK_DIR/commit-msg"

mkdir -p "$HOOK_DIR"
ln -sf "$HOOK_SRC" "$HOOK_DEST"
echo "commit-msg hook installed to $HOOK_DEST"
