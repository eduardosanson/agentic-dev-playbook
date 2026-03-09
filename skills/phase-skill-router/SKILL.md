---
name: phase-skill-router
description: Analyze AGENTS.md and map project phases to specific skills. Use when a user wants to identify which skill should support each workflow phase, where that skill should be declared in AGENTS.md, whether it already exists in the repository, and whether a new skill should be proposed or created.
---

# Phase Skill Router

Use this skill when the user wants phase-specific or cross-cutting operational guidance in `AGENTS.md`.

## Goal

Read the workflow defined in `AGENTS.md`, identify the phases and transversal situations that would benefit from dedicated skills, and decide one of three outcomes for each item:

1. A matching skill already exists and should be referenced
2. No matching skill exists, but one should be described and suggested
3. The user explicitly authorizes creation, so a new skill should be added

## Required Inputs

- Repository root
- Current `AGENTS.md`
- Current `skills/` directory

## Procedure

1. Read `AGENTS.md` and extract:
   - workflow phases
   - cross-cutting situations such as debugging, review handling, branch isolation, or skill authoring
2. Inspect `skills/` and identify existing skills that support a phase or situation directly or indirectly.
3. For each phase or situation, evaluate whether a dedicated skill would improve consistency or execution quality.
4. Recommend a skill only when it changes how the work is executed, not merely what the phase means.
5. For each recommendation, state:
   - phase or situation name
   - recommended skill name
   - whether it already exists
   - exact place to declare it in `AGENTS.md`
6. If the skill exists:
   - suggest adding a line directly below the relevant phase heading or in a dedicated `Phase Skills` subsection
   - add it only if the user explicitly permits editing
7. If the skill does not exist:
   - say clearly that no suitable skill was found
   - describe the missing skill in 3-5 bullets
   - suggest creating it in `skills/[skill-name]/SKILL.md`
   - only create it if the user explicitly asks

## Placement Rule

Default placement in `AGENTS.md`:

- Prefer adding phase-specific skill guidance immediately below the phase heading it supports
- Prefer adding cross-cutting skills in a `Phase Skill Routing` section directly after the workflow block
- If the workflow is described as a single sequence only, add a dedicated section named `Phase Skill Routing` directly after the workflow block

## Good Recommendations

- `DOR/SPEC`: a refinement skill that removes ambiguity before planning
- `PLAN`: a skill that expands tasks, dependencies, risks, and implementation order
- `APPROVAL`: a checkpoint skill that summarizes artifacts and requests approval
- `TDD`: a skill that enforces red-green-refactor and test-first behavior
- `BUILD`: a skill that standardizes build commands and artifact checks
- `VERIFY`: a skill that standardizes validation commands and evidence capture
- `REVIEW/PR`: a skill that structures review evidence and submission steps
- `DEBUGGING`: a skill that requires evidence-first root cause analysis
- `SKILL AUTHORING`: a skill that helps describe and create a missing reusable capability

## Do Not Do

- Do not invent that a skill exists if it does not
- Do not edit `AGENTS.md` without user permission
- Do not recommend a skill when plain text guidance is enough
