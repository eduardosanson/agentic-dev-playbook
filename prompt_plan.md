# Prompt Plan: Agentic Dev Playbook Bootstrap

## Implementation Order

1. [x] Read source rule documents and identify vendor-specific instructions.
2. [x] Define the generic repository structure and core document set.
3. [x] Create the generic `AGENTS.md`, `README.md`, and analysis docs.
4. [x] Create starter templates for future projects.
5. [x] Create the `git-local-rules-sync` skill and supporting script.
6. [x] Create repository-local build and test skills.
7. [x] Run validation scripts and fix any issues.
8. [ ] Initialize Git and attempt GitHub publication.

## Dependencies

- Depends on: access to the local source rule files and installed `git`
- Impacts: future repositories that adopt this playbook

## Risks

- Risk 1: over-generalizing may remove useful operational constraints
- Risk 2: GitHub publication may be blocked by invalid local authentication
- Risk 3: a portable Git sync script may need to stay conservative to avoid destructive config changes
