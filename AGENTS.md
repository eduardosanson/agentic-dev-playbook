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

### Phase Skill Routing

If a project uses dedicated skills to support specific workflow phases, declare them in one of these two places:

- directly below the phase heading they support
- in a dedicated subsection immediately after the workflow block when the workflow is defined as a single sequence

Recommended phase mappings:

- `DOR/SPEC`: use a refinement or brainstorming skill that clarifies intent, requirements, constraints, and acceptance criteria
- `PLAN`: use a planning or brainstorming skill that expands scope, tasks, dependencies, and risks
- `APPROVAL`: use a checkpoint skill or explicit review pattern that summarizes planning artifacts and requests implementation approval
- `TDD`: use a test-first implementation skill that enforces red -> green -> refactor
- `BUILD`: use a build validation skill that standardizes compilation, packaging, or artifact generation
- `VERIFY`: use a validation skill that standardizes commands, outputs, and acceptance checks
- `EVIDENCE`: use an evidence capture skill that records outputs, screenshots, logs, and human validation steps
- `REVIEW/PR`: use a review workflow skill when the team uses pull requests or formal review gates

Recommended cross-cutting mappings:

- `DEBUGGING`: use a debugging skill when tests fail, runtime behavior diverges, or the root cause is unclear
- `PARALLEL WORK`: use an orchestration skill when tasks can be safely split across agents or sessions
- `BRANCH ISOLATION`: use a branch or worktree skill when isolated changes are safer than working in the current tree
- `CODE REVIEW REQUEST`: use a review-request skill when implementation is ready for formal feedback
- `CODE REVIEW RESPONSE`: use a review-response skill when feedback must be applied systematically
- `SKILL AUTHORING`: use a skill-authoring skill when the workflow reveals a reusable capability gap
- `PROJECT INIT`: use a project-init skill when the repository still lacks project-specific build/test automation

If the needed skill is not found in `skills/`, document the gap, describe the expected behavior of the missing skill, and suggest creating a new skill instead of silently improvising.

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
