# Agentic Dev Playbook

Portable rules, workflow templates, and reusable skills for agent-assisted software development.

This repository is a generic adaptation of a Claude-centric workflow into an agent-agnostic playbook that can be used with Codex, Claude Code, Cursor agents, Aider-style flows, custom MCP agents, or mixed human+agent teams.

This repository is also the canonical source of truth for workflow rules that can be synchronized into different agent environments.

## What This Repo Contains

- `AGENTS.md`: generic top-level instructions for any agentic development environment
- `spec.md`: bootstrap specification for this repository
- `prompt_plan.md`: implementation plan for the bootstrap work
- `docs/analysis/`: rationale for what was generalized and what changed
- `docs/decisions/`: decision log for repository evolution
- `skills/`: reusable skills, including Git rule synchronization
- `templates/agent/`: starter templates for new projects
- `templates/git/`: Git policy templates managed by the synchronization skill

## Current Skill Set

### Core Repository Skills

- `agentic-dev-playbook-build`: builds the documentation bundle into `dist/`
- `agentic-dev-playbook-test`: validates repository structure and required artifacts
- `git-local-rules-sync`: installs managed local Git templates and config includes
- `agent-workflow-sync`: syncs the active agent's global workflow file with this repository
- `skill-sync-audit`: audits and optionally updates installed skills for the active agent

### Workflow Phase Skills

- `phase-refinement`: clarifies requirements during `DOR` and `SPEC`
- `phase-skill-router`: maps workflow phases and cross-cutting situations to skills
- `approval-checkpoint`: consolidates planning artifacts before implementation approval
- `evidence-capture`: gathers outputs, validation evidence, and human verification steps
- `systematic-debugging`: drives evidence-first debugging when failures occur

### Project Bootstrap and Tracker Skills

- `project-init`: initializes project-level instructions and baseline automation
- `linear`: general Linear operations
- `linear-dependency-analyzer`: analyzes blockers and dependency graphs in Linear
- `linear-pr-workflow`: executes task-to-PR workflow for Linear-managed work
- `linear-test-validator`: executes and documents tests for Linear-related changes

## Core Design Choices

- Tool-specific instructions were rewritten as capability-based guidance
- Linear-specific behavior became optional issue-tracker integration guidance
- Claude/CLAUDE naming became `AGENTS.md` as a neutral convention
- A single planning approval checkpoint is preserved as a required control point
- Skills are treated as portable procedural modules, not platform-bound magic
- The repository acts as the canonical ruleset that other agent environments should sync from

## Recommended Workflow

```text
[ PLANNING ]
DOR -> SPEC -> PLAN
       |
       v
  APPROVAL CHECKPOINT
       |
       v
[ EXECUTION ]
TDD -> BUILD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE
```

This keeps the planning rigor from the source workflow, but makes execution easier to automate across different agents.

The workflow is complemented by phase routing guidance in `AGENTS.md`, including both linear phases and cross-cutting situations such as debugging, branch isolation, review handling, and project initialization.

## Standard Pattern

This repository should be treated as the default standard for:

- workflow phases
- approval checkpoint behavior
- decision logging
- execution guardrails
- project-local build and test skills
- evidence capture
- review or PR preparation
- synchronization of global agent rules

When Codex rules and Claude rules diverge, this repository should be updated first and then synced outward.

## Execution Guardrails

The standard workflow includes these guardrails:

- clean context for each execution phase
- branch verification before the first commit
- commit hygiene before each commit
- test-first discipline before implementation
- review artifact quality before review or PR submission

These guardrails are defined in `AGENTS.md` and should be considered part of the standard, not optional commentary.

## Process Skills

The workflow assumes process skills may exist for:

- refinement
- planning
- execution
- TDD
- debugging
- verification
- review preparation
- review response
- skill authoring

If a process skill is relevant, it should be invoked before acting on that phase or situation.

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

## Agent Sync Utilities

### Workflow Sync

Use `skills/agent-workflow-sync/` to compare the current agent's global instruction file with this repository and optionally update it.

Audit only:

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py --repo-root /path/to/repo --agent codex
```

Apply update from GitHub-backed source:

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py --repo-root /path/to/repo --agent claude --fetch-remote --apply
```

Use this when:

- Codex and Claude rules drift apart
- the repository workflow changes
- a user wants the current agent to follow the latest standard

After synchronization, the agent's global rules should match the repository standard as closely as possible.

### Skill Audit and Update

Use `skills/skill-sync-audit/` to compare installed skills for the active agent with the skills in this repository.

Audit only:

```bash
skills/skill-sync-audit/scripts/sync_skills.py --repo-root /path/to/repo --agent codex
```

Update installed skills and install missing ones:

```bash
skills/skill-sync-audit/scripts/sync_skills.py --repo-root /path/to/repo --agent codex --apply --install-missing
```

The audit reports:

- skills already present
- skills missing
- skills outdated
- skills updated
- skills installed
- similar skills already found in the user's environment

## Canonical Rule Source

`AGENTS.md` in this repository is the canonical standard.

That means:

- changes to workflow rules should happen here first
- documentation should be updated here first
- sync utilities should distribute this standard to agent environments
- local agent files should not become the primary source of truth

## Git Rule Sync Skill

Use `skills/git-local-rules-sync/` to install and refresh local Git conventions from this repository into the developer machine without editing `~/.gitconfig` manually.
