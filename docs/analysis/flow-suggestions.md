# Flow Suggestions

## Recommended Changes

### 1. Rename `PROMPT PLAN` to `PLAN`

Reason: the artifact should outlive any specific prompting style or agent interface.

### 2. Insert an explicit `VERIFY` phase before evidence collection

Reason: test/build execution and manual checks are operational validation, while evidence is the persistent record of those results.

### 3. Make PR creation conditional

Reason: teams using trunk-based development, patch queues, or direct deployment pipelines still need review evidence, but not necessarily pull requests.

### 4. Split rules into three classes

- Mandatory: must hold for all teams
- Default: recommended unless the project overrides them
- Optional integration: only applies when the tool exists

Reason: this reduces false non-compliance when the environment differs.

### 5. Treat agent skills as repository assets

Reason: colocating operational knowledge with code improves traceability and onboarding.

## Suggested Generic Flow

```text
DOR -> SPEC -> PLAN -> APPROVAL -> TDD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE
```

## Rationale

This preserves the original rigor while making the flow easier to adopt in heterogeneous environments where not every team has the same issue tracker, skill runtime, or release mechanics.
