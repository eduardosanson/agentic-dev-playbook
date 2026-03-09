#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

required_files=(
  "$ROOT_DIR/README.md"
  "$ROOT_DIR/AGENTS.md"
  "$ROOT_DIR/spec.md"
  "$ROOT_DIR/prompt_plan.md"
  "$ROOT_DIR/.githooks/pre-commit"
  "$ROOT_DIR/agent-rules/codex/AGENTS.md"
  "$ROOT_DIR/agent-rules/claude/CLAUDE.md"
  "$ROOT_DIR/agent-rules/cursor/agentic-dev-playbook.mdc"
  "$ROOT_DIR/agent-rules/windsurf/agentic-dev-playbook.md"
  "$ROOT_DIR/docs/analysis/source-mapping.md"
  "$ROOT_DIR/docs/analysis/flow-suggestions.md"
  "$ROOT_DIR/skills/superpowers-sync/SKILL.md"
  "$ROOT_DIR/skills/workspace-editor-sync/SKILL.md"
  "$ROOT_DIR/docs/decisions/BOOTSTRAP.md"
  "$ROOT_DIR/skills/git-local-rules-sync/SKILL.md"
  "$ROOT_DIR/skills/agentic-dev-playbook-build/SKILL.md"
  "$ROOT_DIR/skills/agentic-dev-playbook-test/SKILL.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file" >&2
    exit 1
  fi
done

if ! grep -q "DOR -> SPEC -> PLAN" "$ROOT_DIR/README.md"; then
  echo "Planning workflow string missing from README.md" >&2
  exit 1
fi

if ! grep -q "TDD -> BUILD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE" "$ROOT_DIR/README.md"; then
  echo "Execution workflow string missing from README.md" >&2
  exit 1
fi

if ! grep -q "git-local-rules-sync" "$ROOT_DIR/skills/git-local-rules-sync/SKILL.md"; then
  echo "Skill metadata missing expected name" >&2
  exit 1
fi

echo "Repository structure validation passed."
