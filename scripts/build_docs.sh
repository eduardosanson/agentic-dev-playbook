#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp "$ROOT_DIR/README.md" "$DIST_DIR/README.md"
cp "$ROOT_DIR/AGENTS.md" "$DIST_DIR/AGENTS.md"
cp "$ROOT_DIR/docs/analysis/source-mapping.md" "$DIST_DIR/source-mapping.md"
cp "$ROOT_DIR/docs/analysis/flow-suggestions.md" "$DIST_DIR/flow-suggestions.md"

echo "Built documentation bundle at $DIST_DIR"
