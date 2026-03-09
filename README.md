# Agentic Dev Playbook

Portable rules, workflow templates, and reusable skills for agent-assisted software development.

This repository is a generic adaptation of a Claude-centric workflow into an agent-agnostic playbook that can be used with Codex, Claude Code, Cursor agents, Aider-style flows, custom MCP agents, or mixed human+agent teams.

## What This Repo Contains

- `AGENTS.md`: generic top-level instructions for any agentic development environment
- `spec.md`: bootstrap specification for this repository
- `prompt_plan.md`: implementation plan for the bootstrap work
- `docs/analysis/`: rationale for what was generalized and what changed
- `docs/decisions/`: decision log for repository evolution
- `skills/`: reusable skills, including Git rule synchronization
- `templates/agent/`: starter templates for new projects
- `templates/git/`: Git policy templates managed by the synchronization skill

## Core Design Choices

- Tool-specific instructions were rewritten as capability-based guidance
- Linear-specific behavior became optional issue-tracker integration guidance
- Claude/CLAUDE naming became `AGENTS.md` as a neutral convention
- Mandatory pauses were reduced to a single planning approval checkpoint
- Skills are treated as portable procedural modules, not platform-bound magic

## Recommended Workflow

```text
DOR -> SPEC -> PLAN -> APPROVAL -> TDD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE
```

This keeps the planning rigor from the source workflow, but makes execution easier to automate across different agents.

## Suggested Improvements Over The Original

- Prefer capability tags over vendor names: `issue-tracker`, `code-review`, `test-runner`
- Allow repository-local `AGENTS.md` to override global defaults explicitly
- Treat build/test skills as project assets versioned in the repo
- Split mandatory rules from recommended practices to reduce false rigidity
- Make PR creation optional when teams use trunk-based or patch-based delivery

See `docs/analysis/source-mapping.md` and `docs/analysis/flow-suggestions.md`.

## Local Validation

```bash
./scripts/validate_repo.sh
./scripts/build_docs.sh
```

## Git Rule Sync Skill

Use `skills/git-local-rules-sync/` to install and refresh local Git conventions from this repository into the developer machine without editing `~/.gitconfig` manually.
