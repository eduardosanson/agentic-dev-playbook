# Global Development Rules

---

## Skills and Tools

Global skills should be installed in the active agent's global skills directory.

Issue-tracker skills should only be used when the task explicitly involves issue lookup, status updates, task creation, dependency analysis, or review workflow tied to a tracker.

### Process Skills

Process skills define how to execute a phase, not what to build.

Rule:

- if there is a meaningful chance that a process skill applies, invoke it before acting

Recommended mappings:

| Phase or Situation | Recommended Skill Type |
|---|---|
| Feature refinement (`DOR -> SPEC`) | refinement or brainstorming skill |
| Implementation planning (`PLAN`) | planning or task-expansion skill |
| Plan execution after approval | execution or subagent orchestration skill |
| Test-first implementation (`TDD`) | TDD enforcement skill |
| Parallelizable tasks | orchestration or parallel-work skill |
| Isolated branch or worktree work | branch-isolation skill |
| Bugs, failed tests, unexpected behavior | systematic debugging skill |
| Pre-completion verification | verification or evidence-capture skill |
| Final review or PR preparation | review workflow skill |
| Handling code review feedback | review-response skill |
| Creating or updating project skills | skill-authoring skill |

---

## Required Workflow

Every meaningful change follows this flow. No phase should be skipped.

The workflow is divided into two blocks separated by a single mandatory approval checkpoint:

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

### Approval Checkpoint

After `DOR`, `SPEC`, and `PLAN`, stop and present the plan before implementation starts.

Suggested prompt:

> "Planning is ready. Can I start implementation?"

Rules:

- create and update planning artifacts before asking for approval
- only move to implementation after explicit confirmation
- if the user asks for adjustments, refine and ask again
- after approval, execute autonomously until review or PR unless a blocking failure occurs

---

### Execution Guardrails

Before and during execution, apply these guardrails.

#### G1 - Clean Context Per Phase

Before each execution phase, restate internally:

```text
Current phase: [TDD | BUILD | VERIFY | EVIDENCE | REVIEW/PR]
Project: [name]
Work item: [ID or title]
Branch: [name]
Acceptance criteria in scope: [from spec]
```

Re-read the project instruction file plus `spec.md`, `prompt_plan.md`, and the decision log before continuing.

#### G2 - Branch Verification

Before the first commit:

- branch must come from `main`
- branch naming must follow the project naming policy
- `main` should be updated before branch creation when the workflow requires it
- staged files must belong to the intended change only

Action on failure:

- recreate the branch from `main`
- restage only the intended work

#### G3 - Commit Hygiene

Before each commit:

- commit message follows conventional commit style
- commit is atomic
- no dead code
- no orphan TODOs
- required tests and build checks are green

Action on failure:

- correct the message, remove dead code, or rerun validation before committing

#### G4 - Test-First Discipline

Before each implementation step:

- a failing test should justify the production change
- follow `red -> green -> refactor`
- acceptance criteria must be covered by tests or explicit validation evidence

Action on failure:

- add the missing test or validation step before proceeding

#### G5 - Review Artifact Quality

Before opening a review or PR:

- title references the relevant work item when one exists
- body includes evidence and human validation steps
- target branch matches project policy
- linked tracker items are updated when the project requires it

Action on failure:

- fix the review artifact before submission

---

### Decision Log

At each phase transition, append a concise log entry to `docs/decisions/[WORK-ID].md`.

This file is the operational memory of the task.

Format:

```markdown
## [PREVIOUS PHASE] -> [NEXT PHASE] -- YYYY-MM-DD

- Decision: irreversible or non-obvious choice and reason
- Decision: rejected alternative and reason
- Accepted risk: explicit trade-off
```

Rules:

- maximum 3 bullets per transition
- decisions only, never task lists
- create the file during `DOR`
- commit it with the feature
- do not keep important decisions only in session context

---

### Phase 0 - DOR

Before starting implementation, confirm the task is ready to work on.

Minimum requirements:

- clear intent
- business requirements defined
- functional requirements listed
- non-functional requirements identified
- testable acceptance criteria
- explicit definition of done
- `spec.md` created
- `prompt_plan.md` created
- `docs/decisions/[WORK-ID].md` created

If any item is missing, stop and fill the gap first.

---

### Phase 1 - SPEC

Each task should have a `spec.md` containing:

- business context
- functional requirements
- non-functional requirements
- acceptance criteria
- definition of done
- out-of-scope items

Suggested structure:

```markdown
# Spec: [Feature Name]

## Business Context

## Functional Requirements

## Non-Functional Requirements

## Acceptance Criteria

## Definition of Done

## Out of Scope
```

---

### Phase 2 - PLAN

Before writing production code, create `prompt_plan.md` with the exact implementation sequence, dependencies, and risks.

Suggested structure:

```markdown
# Plan: [Feature Name]

## Implementation Order

1. [ ] Write failing tests for ...
2. [ ] Implement the minimum change ...
3. [ ] Refactor ...
4. [ ] Run validation ...
5. [ ] Capture evidence ...

## Dependencies

## Risks
```

When planning is complete, trigger the approval checkpoint.

---

### Phase 3 - TDD

Always start from tests.

Required order:

1. write the failing test
2. implement the minimum needed to pass
3. refactor while keeping tests green

Never add production code without a test or explicit validation need justifying it.

---

### Phase 4 - Build and Test Skills

Each project should have project-specific build and test skills based on the real stack.

When starting work in a project for the first time, or when those skills do not exist yet:

- identify language and runtime
- identify build tool
- identify test framework
- identify linter
- inspect existing CI

Then create at least:

- `[project]-build`
- `[project]-test`

Preferred location inside the repository:

```text
[repo-root]/
`-- skills/
    |-- [project]-build/
    |   `-- SKILL.md
    `-- [project]-test/
        `-- SKILL.md
```

Do not rely on global installation for project-specific skills.

Before any commit, run:

1. `[project]-test`
2. `[project]-build`

If either step fails, do not advance.

---

### Phase 4.5 - Project Instruction File

Every project should have a project-local instruction file at the repository root.

Common names include:

- `AGENTS.md`
- `CLAUDE.md`

The file should include at least:

- stack summary
- available project skills
- workflow reference
- optional tracker or review integration rules

If the project uses an issue tracker:

- use tracker-related skills only when relevant
- follow tracker-provided branch naming when required
- reference the work item in review artifacts
- move the work item through the required review states

---

### Phase 5 - Pre-commit Hooks

Every project should have pre-commit hooks configured with lint and tests, and optionally build when it is fast enough.

If the project has no pre-commit hook, create it before committing.

---

### Phase 6 - Evidence

Every task should generate evidence:

- implemented functionality
- created or modified files when relevant
- expected behavior from the user's perspective
- relevant outputs, screenshots, or logs
- automated test results
- human validation steps

Suggested validation format:

```markdown
## How To Validate

### Preconditions

- environment
- required data

### Steps

1. Go to ...
2. Perform ...
3. Verify ...

### Edge Cases

- invalid input -> expected error
- offline mode -> expected behavior
```

---

### Phase 7 - Branch and Review/PR

Branch naming should follow the policy defined by the project or its tracker.

Always branch from `main`.

Typical flow:

```bash
git checkout main
git pull origin main
git checkout -b <branch-name>
```

Never create a feature branch from another feature branch.

---

## Debugging

When a bug, failed test, or unexpected behavior appears in any phase, switch to evidence-first debugging before proposing a fix.

Do not guess the cause.

---

## General Rules

- never skip workflow phases
- use the team's communication language
- use conventional commits
- keep commits small and atomic
- remove dead code before commit
- do not leave orphan TODOs without a tracked follow-up
