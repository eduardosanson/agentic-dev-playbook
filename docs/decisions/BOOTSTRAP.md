## DOR -> SPEC -- 2026-03-09

- Decision: publish the playbook as a standalone repository instead of embedding it into an existing project so it can be reused independently.
- Decision: use `AGENTS.md` as the neutral instruction filename because it can represent multiple agent runtimes without vendor branding.
- Accepted risk: some Claude-specific automation semantics will be documented as optional capabilities rather than enforced behavior.

## SPEC -> PLAN -- 2026-03-09

- Decision: keep a single mandatory approval checkpoint between planning and implementation to preserve control without over-fragmenting autonomous execution.
- Decision: include repository-local build/test skills even for a docs-heavy repository so the workflow demonstrates its own rules.
- Accepted risk: validation is shell-based and intentionally lightweight rather than introducing a heavier documentation toolchain.

## PLAN -> TDD -- 2026-03-09

- Decision: implement the repository artifacts first and validate them with shell scripts instead of introducing a language runtime solely for linting markdown.
- Decision: create the Git sync capability as a repository skill with a bundled script so the behavior is deterministic and reusable.
- Accepted risk: the playbook includes templates and reference automation, but does not attempt to auto-generate every project-specific skill.

## TDD -> VERIFY -- 2026-03-09

- Decision: validate the Git sync script against a temporary `HOME` directory to avoid mutating the real user Git configuration during bootstrap.
- Decision: add a repository-local `.githooks/pre-commit` hook so the playbook follows its own pre-commit rule.
- Accepted risk: hook installation is configured at repository level only after `git init`, not automatically for external consumers.

## VERIFY -> EVIDENCE -- 2026-03-09

- Decision: treat validation script output and the temporary-home Git sync run as the bootstrap evidence set.
- Decision: generate a `dist/` bundle as the repository build artifact so the build skill has a concrete deliverable.
- Accepted risk: the build artifact is documentation packaging only, not a compiled binary or published site.

## EVIDENCE -> REVIEW/PR -- 2026-03-09

- Decision: publish the repository publicly on GitHub immediately after local validation so the playbook is consumable without an additional staging step.
- Decision: keep the initial history as a single bootstrap commit because the repository starts from documentation and reusable automation assets, not an evolving codebase.
- Accepted risk: the first public revision is intentionally broad and may later be split into more focused modules as adoption patterns emerge.
