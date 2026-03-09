# Regras Globais de Desenvolvimento

---

## Skills & Ferramentas

As skills globais ficam em `~/.codex/skills/`.

Skills do Linear so devem ser acionadas quando o contexto envolver explicitamente o Linear (consultar issues, mover status, criar tarefas, etc.). Nao acione skills do Linear para tarefas de codigo puro, design ou conteudo que nao interajam com o Linear.

---

## Fluxo de Trabalho Obrigatorio

Todo desenvolvimento segue este fluxo. Nenhuma fase pode ser pulada.

```text
DOR -> SPEC -> PROMPT PLAN -> TDD -> BUILD -> EVIDENCIAS -> PR -> DOD
```

### Log de Decisoes

A cada transicao de fase, registrar um log resumido em `docs/decisions/[ISSUE-ID].md` do projeto. O log captura apenas decisoes.

Esse arquivo e a memoria operacional da tarefa. Toda tarefa relevante deve salvar ali seu contexto decisorio ao longo do fluxo, para que a execucao fique rastreavel ate PR e DOD.

Formato:

```markdown
## [FASE ANTERIOR] -> [PROXIMA FASE] -- YYYY-MM-DD

- Decisao: [o que foi decidido e por que]
- Decisao: [alternativa descartada e motivo]
- Risco aceito: [trade-off conscientemente assumido]
```

Regras:

- Maximo 3 itens por transicao
- Somente decisoes irreversiveis ou nao-obvias
- Sem tarefas e sem listas de arquivos
- O arquivo e criado na fase DOR e deve ser commitado com a feature
- Nao manter decisoes importantes apenas no contexto temporario da sessao; salvar na tarefa

### Fase 0 - DOR

Antes de iniciar qualquer tarefa, verificar se ela esta pronta para fazer. A tarefa so pode entrar em desenvolvimento se tiver:

- Intencao clara
- Requisitos de negocio definidos
- Requisitos funcionais listados
- Requisitos nao-funcionais identificados
- Criterios de aceite testaveis
- DOD definido
- `spec.md` criado
- `prompt_plan.md` criado
- `docs/decisions/[ISSUE-ID].md` criado

Se qualquer item estiver faltando, parar e preencher antes de continuar.

### Fase 1 - SPEC

Cada tarefa deve ter `spec.md` com:

- Contexto de negocio
- Requisitos funcionais
- Requisitos nao-funcionais
- Criterios de aceite
- Definition of Done
- Fora de escopo

### Fase 2 - PROMPT PLAN

Antes de codificar, criar `prompt_plan.md` com a sequencia exata de implementacao, dependencias e riscos.

### Fase 3 - TDD

Sempre comecar pelos testes:

1. Escrever o teste que falha
2. Implementar o minimo para passar
3. Refatorar mantendo os testes passando

Nunca escrever codigo de producao sem um teste que o justifique.

### Fase 4 - Skills de Build e Teste do Projeto

Cada projeto deve ter suas proprias skills de build e teste, criadas sob medida para a stack real do projeto.

Ao iniciar trabalho em um projeto pela primeira vez, ou quando as skills ainda nao existirem, identificar:

- Linguagem e runtime
- Ferramenta de build
- Framework de testes
- Linter
- CI existente

Depois criar duas skills especificas do projeto:

- `[projeto]-build`
- `[projeto]-test`

Preferencialmente usando a skill `skill-creator` ja disponivel no Codex.

As skills do projeto devem ficar versionadas no repositorio:

```text
[raiz-do-projeto]/
`-- .codex/
    `-- skills/
        |-- [projeto]-build/
        |   `-- SKILL.md
        `-- [projeto]-test/
            `-- SKILL.md
```

Nao colocar skills especificas do projeto globalmente em `~/.codex/skills/`.

Antes de qualquer commit, rodar obrigatoriamente:

1. `[projeto]-test`
2. `[projeto]-build`

Se qualquer etapa falhar, nao avancar.

### Fase 4.5 - AGENTS.md do Projeto

Todo projeto deve ter um `AGENTS.md` na raiz com instrucoes especificas do contexto.

Conteudo minimo:

```markdown
# [Nome do Projeto] - Regras de Desenvolvimento

## Stack
[linguagem, framework, versoes relevantes]

## Skills disponiveis
- `[projeto]-build` - build do projeto
- `[projeto]-test` - testes e lint

## Fluxo de trabalho
Seguir o fluxo global definido em ~/.codex/AGENTS.md.
```

Se o projeto usa Linear:

- usar as skills do Linear ao criar ou atualizar PRs vinculados a issues
- seguir `gitBranchName` retornado pela integracao
- referenciar a issue no PR
- mover a issue para `In Review` ao abrir PR
- mover para `Done` apos merge

### Fase 5 - Pre-commit Hooks

Todo projeto deve ter hooks de pre-commit configurados com lint e testes, e build quando fizer sentido.

Se o projeto nao tiver hooks, criar antes de qualquer commit.

### Fase 6 - Evidencias

Toda tarefa deve gerar evidencias:

- funcionalidades implementadas
- arquivos criados ou modificados
- comportamento esperado do ponto de vista do usuario
- outputs, screenshots ou logs relevantes
- resultado dos testes automatizados
- passo a passo de validacao humana

### Fase 7 - Branch e PR

O nome da branch deve seguir o padrao da ferramenta de gestao usada pelo projeto. Se houver Linear, usar `gitBranchName`.

Sempre criar branch a partir da `main`.

## Regras Gerais

- Nunca pular fases do fluxo
- Sempre em portugues nas comunicacoes
- Commits convencionais: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`
- Uma responsabilidade por commit
- Sem codigo morto antes de commitar
- Sem TODOs no codigo sem issue correspondente
