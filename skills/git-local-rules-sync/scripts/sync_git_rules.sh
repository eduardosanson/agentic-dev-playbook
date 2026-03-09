#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <repo-root> [target-config-dir]" >&2
  exit 1
fi

REPO_ROOT="$1"
TARGET_DIR="${2:-$HOME/.config/agentic-dev-playbook/git}"
SOURCE_DIR="$REPO_ROOT/templates/git"
MANAGED_INCLUDE="$TARGET_DIR/rules.gitconfig"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Missing templates directory: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR/hooks"

install -m 0644 "$SOURCE_DIR/commit-template.txt" "$TARGET_DIR/commit-template.txt"
install -m 0644 "$SOURCE_DIR/global.gitignore" "$TARGET_DIR/global.gitignore"
install -m 0755 "$SOURCE_DIR/pre-commit" "$TARGET_DIR/hooks/pre-commit"
install -m 0644 "$SOURCE_DIR/gitconfig.include" "$MANAGED_INCLUDE"

current_include="$(git config --global --get-all include.path || true)"
if printf '%s\n' "$current_include" | grep -Fxq "$MANAGED_INCLUDE"; then
  echo "Git include already configured: $MANAGED_INCLUDE"
else
  git config --global --add include.path "$MANAGED_INCLUDE"
  echo "Added git include.path: $MANAGED_INCLUDE"
fi

echo "Installed managed Git rules into: $TARGET_DIR"
