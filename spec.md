# Spec: Agentic Dev Playbook Bootstrap

## Business Context

The current workflow and skill set are useful, but strongly tied to Claude-specific conventions and vendor naming. This repository should publish a reusable, public version that preserves the engineering discipline while making it portable across agentic development environments.

## Functional Requirements

- FR01: Provide a generic `AGENTS.md` that captures the core workflow and rules without Claude-specific naming.
- FR02: Document how source instructions were translated from tool-specific to capability-based guidance.
- FR03: Include concrete suggestions for improving the original workflow for broader adoption.
- FR04: Provide templates for `AGENTS.md`, `spec.md`, and `prompt_plan.md`.
- FR05: Provide a skill under `skills/` that updates local Git rules from repository-managed templates.
- FR06: Provide repository-local build and test skills to validate the playbook itself.

## Non-Functional Requirements

- NFR01: All content should be plain text or shell-based and portable across common Unix-like environments.
- NFR02: The repository must be understandable without access to Claude, Linear, or proprietary plugins.
- NFR03: Validation scripts must fail fast with actionable output.

## Acceptance Criteria

- AC01: A new reader can understand the generic workflow from `README.md` and `AGENTS.md`.
- AC02: The repository explains what was generalized and why in dedicated analysis docs.
- AC03: The Git sync skill includes executable automation and usage instructions.
- AC04: Local validation scripts complete successfully.
- AC05: The repository is initialized as a Git repository and ready to publish.

## Definition of Done

- [ ] Core docs created and internally consistent
- [ ] Git sync skill created with runnable script
- [ ] Project build/test skills created
- [ ] Validation scripts passing
- [ ] Decision log updated for completed phases
- [ ] Repository initialized with Git
- [ ] Publish attempt made to GitHub or blocker documented

## Out of Scope

- Full migration of every existing global skill into this repository
- Automating GitHub authentication
- Integrating with any specific issue tracker by default
