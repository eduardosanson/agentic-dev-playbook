# Agentic Dev Playbook

Apply this workflow in Cascade:

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

Rules:

- do not skip phases
- ask for approval after planning
- use test-first implementation
- validate before completion
- capture evidence before review
- keep commits atomic and use conventional commits
- preserve tool-specific behavior when agent ecosystems differ

If `AGENTS.md` exists in the workspace root, treat it as the main project instruction file.
