# Agentic Dev Playbook - Development Rules

## Scope

This repository defines a portable workflow for agent-assisted software development. It is intentionally vendor-neutral.

## Capability Routing

Only use specialized integrations when the task explicitly requires them.

- Issue tracker skills: only when reading or updating tasks, statuses, or linked delivery artifacts
- PR/review skills: only when creating or updating review records
- Documentation skills: when producing structured docs, specs, RFCs, or decision logs
- Build/test skills: before claiming a change is complete

## Required Workflow

Every meaningful change follows this sequence:

```text
DOR -> SPEC -> PLAN -> APPROVAL -> TDD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE
```

### Approval Checkpoint

After `DOR`, `SPEC`, and `PLAN`, pause and confirm the implementation plan before code changes begin.

### Decision Log

At every phase transition, append a concise entry to `docs/decisions/[WORK-ID].md`:

```markdown
## [PREVIOUS] -> [NEXT] -- YYYY-MM-DD

- Decision: irreversible or non-obvious choice and reason
- Decision: rejected alternative and reason
- Accepted risk: explicit trade-off
```

Rules:

- Maximum 3 bullets per transition
- Record decisions only, never task lists
- Create the file at DOR

## Repository Deliverables

Each change should leave behind:

- `spec.md` or task-specific spec
- `prompt_plan.md` or equivalent execution plan
- decision log entry updates
- automated validation evidence
- human validation steps when user-facing behavior changes

## Project-Level Automation

Each project should version its own automation assets in-repo:

- `skills/[project]-build/`
- `skills/[project]-test/`
- `.githooks/pre-commit` or equivalent
- project-local `AGENTS.md`

## Git Rules

- Branch from `main`
- Use conventional commits
- Keep commits atomic
- Do not commit dead code or orphan TODOs
- Run project test and build validation before commit

## Language

- Team-facing communication may follow the team's default language
- Code comments should stay concise and only explain non-obvious logic
