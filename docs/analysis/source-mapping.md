# Source Mapping

## Purpose

This document explains how Claude-specific and environment-specific instructions were translated into portable guidance.

## Mapping Principles

- Replace product names with capability names
- Keep engineering constraints when they are tool-agnostic
- Downgrade platform coupling into optional integrations
- Separate mandatory workflow from recommendations

## Translation Table

| Source Concept | Generic Translation | Reason |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | Neutral file name usable by any agent runtime |
| Claude skills | agent skills / workflow modules | Same concept, less vendor coupling |
| Linear skills | issue-tracker integration skills | Works with Linear, Jira, GitHub Issues, YouTrack |
| MCP-specific branch lookup | tracker-provided branch naming policy | Same need, no protocol lock-in |
| Superpowers plugin | optional process-automation toolkit | The workflow should not depend on one plugin |
| Mandatory PR creation | review artifact creation when the delivery model uses PRs | Some teams do not ship via PRs |
| Portuguese-only communication | team-default communication language | Public repo should not prescribe a single language |

## What Stayed Mandatory

- DOR before implementation
- explicit spec and implementation plan
- test-first implementation expectation
- decision logging across phases
- build/test verification before commit
- evidence for validation

## What Became Optional

- issue-tracker synchronization
- branch naming derived from external task systems
- automatic PR opening
- subagent execution strategies
- vendor-specific plugin invocation rules
