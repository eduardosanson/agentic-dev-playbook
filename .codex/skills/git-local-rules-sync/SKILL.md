---
name: git-local-rules-sync
description: Synchronize Git rules from this repository into the local developer environment. Use when a user wants to install or refresh commit templates, hooks, ignore rules, or managed Git config includes from repo-owned templates.
---

# Git Local Rules Sync

Use this skill when a repository manages local Git conventions and the user wants to apply them to the current machine safely.

## What This Skill Does

- installs managed Git templates under `~/.config/agentic-dev-playbook/git/`
- ensures `~/.gitconfig` includes the managed config file through `include.path`
- refreshes commit template, ignore file, and hook scripts from repository templates
- avoids destructive rewrites of unrelated user Git configuration

## Inputs

- Repository root path
- Optional target config directory override

## Procedure

1. Confirm the repository contains `templates/git/`.
2. Run `scripts/sync_git_rules.sh` from this skill with the repository root.
3. Review the output for:
   - installed files
   - whether `include.path` was added or already existed
   - whether hooks were made executable
4. If the repository has project-specific hooks, tell the user to review `core.hooksPath` trade-offs before applying globally.

## Command

```bash
.codex/skills/git-local-rules-sync/scripts/sync_git_rules.sh /path/to/repo
```

## Safety Rules

- Do not delete existing user Git config
- Do not overwrite unrelated hooks directories
- Keep all managed files under a dedicated config directory
