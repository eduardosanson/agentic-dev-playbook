# Workflow Flowchart

Este documento descreve o workflow padrão do projeto, as regras operacionais e as skills recomendadas em cada fase.

## Regra Padrão

```text
DOR -> SPEC -> PLAN -> APPROVAL -> TDD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE
```

Regras base:

- não pular fases
- registrar decisões em `docs/decisions/[WORK-ID].md`
- confirmar aprovação antes de implementar
- validar build/test antes de concluir
- capturar evidências antes de declarar a entrega pronta

## Fluxograma Geral

```mermaid
flowchart TD
    A[DOR] --> B[SPEC]
    B --> C[PLAN]
    C --> D{Aprovado?}
    D -- nao --> C
    D -- sim --> E[TDD]
    E --> F[VERIFY]
    F --> G[EVIDENCE]
    G --> H[REVIEW/PR]
    H --> I[DONE]
```

## Fases e Skills

```mermaid
flowchart TD
    A[DOR / SPEC] --> A1[phase-refinement]
    B[PLAN] --> B1[phase-skill-router]
    C[APPROVAL] --> C1[approval-checkpoint]
    D[TDD] --> D1[skill de TDD do projeto ou fluxo test-first]
    E[BUILD / VERIFY] --> E1[agentic-dev-playbook-build]
    E --> E2[agentic-dev-playbook-test]
    F[EVIDENCE] --> F1[evidence-capture]
    G[REVIEW / PR] --> G1[linear-pr-workflow ou fluxo de review do time]
```

## Fluxos Transversais

```mermaid
flowchart LR
    A[Bug ou falha] --> B[systematic-debugging]
    C[Falta skill por fase] --> D[phase-skill-router]
    D --> E{Skill existe?}
    E -- sim --> F[referenciar no AGENTS.md]
    E -- nao --> G[descrever skill faltante]
    G --> H{usuario permitiu criar?}
    H -- sim --> I[criar em skills/nome-da-skill]
    H -- nao --> J[sugerir criacao]
    K[Setup inicial do projeto] --> L[project-init]
    M[Sincronizar workflow global do agente] --> N[agent-workflow-sync]
    O[Auditar ou atualizar skills instaladas] --> P[skill-sync-audit]
    Q[Sincronizar regras locais de Git] --> R[git-local-rules-sync]
```

## Leitura Operacional

1. Refinar a demanda em `DOR` e `SPEC`.
2. Planejar a implementação em `PLAN`.
3. Parar no checkpoint de aprovação.
4. Implementar com disciplina test-first.
5. Validar com build, testes e verificações necessárias.
6. Capturar evidências.
7. Encaminhar para review ou PR.
8. Concluir somente depois da validação e do registro de evidências.

## Observações

- `phase-skill-router` decide se já existe skill adequada para uma fase ou situação transversal.
- Se a skill não existir, ela deve ser descrita e só criada com permissão do usuário.
- `agent-workflow-sync` e `skill-sync-audit` são agent-aware: atuam sobre o agente em uso ou sobre o agente explicitamente informado.
