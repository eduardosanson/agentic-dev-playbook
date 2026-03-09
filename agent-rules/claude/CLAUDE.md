# Regras Globais de Desenvolvimento

---

## 🔧 Skills & Ferramentas

**Skills do Linear** só devem ser acionadas quando o contexto envolver explicitamente o Linear (consultar issues, mover status, criar tarefas, etc.). Não acione skills do Linear para tarefas de código puro, design ou conteúdo que não interajam com o Linear.

### 🦸 Plugin Superpowers

O plugin Superpowers fornece skills de **processo** — elas ditam *como* executar cada fase, não *o quê* construir. Invocar via ferramenta `Skill` **antes de qualquer ação** na fase correspondente.

**Regra:** Se houver 1% de chance de uma skill se aplicar, invocá-la antes de agir.

| Fase / Situação | Skill obrigatória |
|---|---|
| Refinamento de feature (DOR → SPEC) | `superpowers:brainstorming` |
| Criar plano de implementação (PROMPT PLAN) | `superpowers:writing-plans` |
| Executar plano na sessão atual (pós-aprovação) | `superpowers:subagent-driven-development` |
| Executar plano em sessão paralela separada | `superpowers:executing-plans` |
| Implementar qualquer feature ou bugfix (TDD) | `superpowers:test-driven-development` |
| Tarefas independentes em paralelo | `superpowers:dispatching-parallel-agents` |
| Isolar trabalho em branch separado | `superpowers:using-git-worktrees` |
| Bug, falha de teste ou comportamento inesperado | `superpowers:systematic-debugging` |
| Verificar antes de declarar concluído / commitar | `superpowers:verification-before-completion` |
| Finalizar branch e preparar PR | `superpowers:finishing-a-development-branch` |
| Solicitar code review após implementação | `superpowers:requesting-code-review` |
| Receber e aplicar feedback de code review | `superpowers:receiving-code-review` |
| Criar ou editar skills do projeto | `superpowers:writing-skills` |

---

## 📋 Fluxo de Trabalho Obrigatório

Todo desenvolvimento segue este fluxo. Nenhuma fase pode ser pulada.

O fluxo é dividido em dois blocos separados por um **checkpoint obrigatório de aprovação**:

```
[ PLANEJAMENTO ]
DOR → SPEC → PROMPT PLAN
        ⬇
  ⏸ ÚNICO CHECKPOINT — aprovação do plano pelo dev
        ⬇
[ EXECUÇÃO — autônomo após aprovação ]
TDD → BUILD → EVIDÊNCIAS → PR (automático) → DOD
```

### ⏸ Checkpoint de Aprovação (único e obrigatório)

Após concluir **DOR + SPEC + PROMPT PLAN**, parar e apresentar o plano:

> "O planejamento está pronto. Posso começar a implementação?"

**Regras do checkpoint:**
- Criar e commitar os artefatos de planejamento (`spec.md`, `prompt_plan.md`, `docs/decisions/[ID].md`) **antes** de fazer a pergunta
- Só avançar para TDD após confirmação explícita ("sim", "pode ir", "executa", etc.)
- Se o usuário pedir ajustes, refinar e perguntar novamente
- **Após aprovação: execução autônoma até PR** — não parar para aprovações intermediárias
- PR é criado automaticamente ao final da execução
- Só interromper a execução se: build falha, testes falham, ou guardrail detecta violação crítica

---

### 🛡️ Guardrails de Execução (verificados automaticamente)

A cada fase da execução, Claude verifica os guardrails abaixo **sem precisar de intervenção do dev**. Falhas são corrigidas autonomamente quando possível; caso contrário, a execução para com diagnóstico claro.

#### G1 — Contexto limpo ao iniciar cada fase

Antes de iniciar qualquer fase, montar internamente:

```
Fase atual: [TDD | BUILD | EVIDÊNCIAS | PR]
Projeto: [nome]
Issue: [ID] — [título]
Branch: [gitBranchName]
Critérios de aceite em escopo: [lista do spec.md]
```

Reler `CLAUDE.md` do projeto + `spec.md` + `prompt_plan.md`. Descartar assunções da fase anterior não documentadas.

#### G2 — Verificação de branch (antes do primeiro commit)

```
✓ Branch criado a partir de main — nunca de outro feature branch
✓ Nome do branch segue o padrão feature/TASK-ID
✓ git pull origin main executado antes do checkout
✓ Sem arquivos de outra branch incluídos no stage
```

Ação em falha: recriar branch a partir de `main` e recomeçar os commits.

#### G3 — Git flow (antes de cada commit)

```
✓ Mensagem segue Conventional Commits: feat/fix/test/chore/docs/refactor
✓ Commit é atômico — uma responsabilidade por commit
✓ Sem código morto, sem TODOs sem issue no Linear
✓ Testes passando + build verde antes de commitar
```

Ação em falha: corrigir mensagem ou remover código morto antes de commitar.

#### G4 — TDD (antes de cada implementação)

```
✓ Teste escrito antes do código de produção
✓ Sequência Red → Green → Refactor seguida
✓ Critérios de aceite do spec.md cobertos por testes
```

Ação em falha: escrever o teste antes de avançar com a implementação.

#### G5 — PR (antes de criar o PR)

```
✓ Título referencia o issue ID (ex: "feat: SOF-38 — descrição")
✓ Body inclui evidências + passo a passo de validação humana
✓ Branch de destino == main
✓ Issue movida para In Review no Linear
```

Ação em falha: corrigir dados do PR antes de criar.

#### Tabela de falhas e ações

| Guardrail | Falha | Ação autônoma |
|---|---|---|
| G2 | Branch saiu de feature branch | Recria a partir de main, recomeça commits |
| G3 | Mensagem fora do padrão | Reescreve antes de commitar |
| G4 | Código sem teste | Escreve o teste antes de avançar |
| G5 | Target != main | Corrige target antes de criar PR |

---

### 📝 Log de Decisões (obrigatório em cada transição)

**A cada transição de fase**, registrar um log resumido no arquivo `docs/decisions/[ISSUE-ID].md` do projeto. O log captura **apenas decisões** — não tarefas concluídas, não descrições de código.

Esse arquivo é a **memória operacional da tarefa**. Toda tarefa relevante deve salvar ali seu contexto decisório ao longo do fluxo, para que a execução fique rastreável até PR e DOD.

#### Formato de cada entrada

```markdown
## [FASE ANTERIOR] → [PRÓXIMA FASE] — YYYY-MM-DD

- Decisão: [o que foi decidido e por quê — uma linha]
- Decisão: [alternativa descartada e motivo]
- Risco aceito: [trade-off conscientemente assumido]
```

#### Regras do log

- **Máximo 3 itens** por transição — se precisar de mais, está detalhado demais
- **Somente decisões irreversíveis ou não-óbvias** — o que alguém no futuro precisaria saber para entender o código
- **Sem tarefas, sem listas de arquivos** — isso vai no commit/PR
- O arquivo é criado na Fase 0 (DOR) e recebe entradas a cada fase concluída
- Deve ser **commitado** junto com os arquivos da feature
- Não manter decisões importantes apenas no contexto temporário da sessão; salvar na tarefa

#### Exemplo real

```markdown
## DOR → SPEC — 2026-03-08

- Decisão: usar WorkoutSessionHolder (singleton in-memory) em vez de Room para transferir dados entre telas — evita migração de schema para dado efêmero
- Risco aceito: dados perdidos se o processo morrer entre ExecutionScreen e SummaryScreen (aceitável, treino já foi registrado no backend)

## TDD → BUILD — 2026-03-08

- Decisão: calorias estimadas com MET fixo (7.0) em vez de cálculo por exercício — dados de MET por exercício não estão disponíveis no modelo atual
- Decisão: FlowRow para chips de grupos musculares em vez de LazyRow — quantidade de grupos é pequena (<10) e FlowRow é mais legível

## BUILD → PR — 2026-03-08

- Decisão: extrair state.workoutName para val local antes do null check — Kotlin não faz smart cast em delegated properties (limitação da linguagem)
```

---

### Fase 0 — DOR (Definition of Ready)

> 🦸 **Skill:** Se a feature ainda não está clara ou há ambiguidade nos requisitos, invocar `superpowers:brainstorming` antes de preencher o DOR. A skill conduz o refinamento através de perguntas e proposta de abordagens.

Antes de iniciar qualquer tarefa, verificar se ela está "pronta para fazer". A tarefa só pode entrar em desenvolvimento se tiver:

- [ ] Intenção clara do projeto/feature descrita
- [ ] Requisitos de negócio definidos (o "por quê")
- [ ] Requisitos funcionais listados (o "o quê")
- [ ] Requisitos não-funcionais identificados (performance, segurança, acessibilidade)
- [ ] Critérios de aceite escritos de forma testável
- [ ] DOD definido para esta tarefa
- [ ] `spec.md` criado (ver abaixo)
- [ ] `prompt_plan.md` criado (ver abaixo)
- [ ] `docs/decisions/[ISSUE-ID].md` criado (arquivo de log de decisões — inicialmente vazio)

Se qualquer item estiver faltando, **parar e preencher antes de continuar**.

---

### Fase 1 — SPEC (`spec.md`)

Cada tarefa deve ter um arquivo `spec.md` com:

```markdown
# Spec: [Nome da Feature]

## Contexto de Negócio
Por que estamos fazendo isso? Qual problema resolve?

## Requisitos Funcionais
- RF01: ...
- RF02: ...

## Requisitos Não-Funcionais
- RNF01: Performance — resposta < 500ms
- RNF02: ...

## Critérios de Aceite
- CA01: Dado X, quando Y, então Z
- CA02: ...

## Definition of Done (DOD)
- [ ] Código implementado e compilando
- [ ] Testes unitários escritos e passando
- [ ] Testes de integração passando
- [ ] Lint sem erros
- [ ] Pre-commit hooks passando
- [ ] Evidências capturadas
- [ ] Passo a passo de validação humana escrito
- [ ] PR aberta com link no Linear
- [ ] Issue movida para In Review no Linear

## Fora de Escopo
O que explicitamente NÃO será feito nesta tarefa.
```

---

### Fase 2 — PROMPT PLAN (`prompt_plan.md`)

> 🦸 **Skill:** Usar `superpowers:writing-plans` para gerar o `prompt_plan.md`. A skill estrutura o plano em tasks atômicas com passos exatos, comandos e expected output — prontos para execução por subagents.

Antes de codificar, criar um plano de prompts/passos com a sequência exata de implementação:

```markdown
# Prompt Plan: [Nome da Feature]

## Ordem de Implementação

1. [ ] Criar testes para [componente A] — descrever o que testar
2. [ ] Implementar [componente A] para fazer os testes passarem
3. [ ] Criar testes para [componente B]
4. [ ] Implementar [componente B]
5. [ ] Teste de integração entre A e B
6. [ ] Refactor se necessário
7. [ ] Capturar evidências

## Dependências
- Depende de: [issues/PRs bloqueantes]
- Impacta: [outras áreas do sistema]

## Riscos Identificados
- Risco 1: como mitigar
```

> Ao finalizar o `prompt_plan.md`, commitar os artefatos e **acionar o Checkpoint de Aprovação** — aguardar confirmação antes de seguir para TDD.

---

### Fase 3 — TDD (Test-Driven Development)

> 🦸 **Skill:** Invocar `superpowers:test-driven-development` antes de escrever qualquer código de produção. A skill garante a sequência Red → Green → Refactor e previne implementação sem cobertura de testes.
>
> **Execução do plano:** Após aprovação do checkpoint, usar `superpowers:subagent-driven-development` (sessão atual) ou `superpowers:executing-plans` (sessão paralela) para executar as tasks do `prompt_plan.md` de forma autônoma com revisão por subagents.

**Sempre começar pelos testes. Sem exceção.**

Ordem obrigatória:
1. Escrever o teste que falha (red)
2. Implementar o mínimo para o teste passar (green)
3. Refatorar mantendo os testes passando (refactor)

Nunca escrever código de produção sem um teste que o justifique.

---

### Fase 4 — Skills de Build e Teste do Projeto

Cada projeto deve ter suas próprias skills de build e teste criadas sob medida. Essas skills **não são genéricas** — são construídas com base na stack real do projeto.

#### Quando criar as skills

Ao iniciar qualquer trabalho em um projeto **pela primeira vez**, ou sempre que as skills não existirem ainda em `.claude/skills/` do repositório, invocar:

```
skill: "project-init"
```

Esta skill detecta a stack automaticamente, gera o `CLAUDE.md` do projeto e cria as skills `[projeto]-build` e `[projeto]-test` sem intervenção manual.

> Verificar primeiro se as skills já existem em `[raiz-do-projeto]/.claude/skills/`. Se existirem, apenas validar se ainda estão corretas para a stack atual.

#### Localização das Skills

As skills de build e teste ficam **dentro do repositório do projeto**, não globalmente:

```
# ✅ Local correto
[projeto]/.claude/skills/[projeto]-build/SKILL.md
[projeto]/.claude/skills/[projeto]-test/SKILL.md

# ❌ Não colocar globalmente
~/.claude/skills/[projeto]-build/
```

Isso garante que as skills viajam junto com o projeto, ficam versionadas no Git e qualquer dev que clonar o repositório já tem as skills disponíveis.

> Adicionar `.claude/skills/` ao `.gitignore` apenas se as skills contiverem informações sensíveis. Em geral, devem ser commitadas.

#### Uso das skills no fluxo

Uma vez criadas, essas skills substituem os comandos genéricos de build/test em todo o fluxo:

```bash
# ❌ Não usar comandos genéricos avulsos
./gradlew build
npm test

# ✅ Usar as skills do projeto (lidas de .claude/skills/ do repositório)
skill: "[projeto]-build"
skill: "[projeto]-test"
```

Antes de qualquer commit, rodar obrigatoriamente:
1. `[projeto]-test` — todos os testes devem passar
2. `[projeto]-build` — build deve ser bem-sucedido

Se qualquer etapa falhar, **não avançar**.

---

### Fase 4.5 — CLAUDE.md do Projeto

Todo projeto deve ter um arquivo `CLAUDE.md` na raiz do repositório com instruções específicas para aquele contexto. Este arquivo viaja junto com o código e garante que qualquer sessão de desenvolvimento siga as convenções certas.

#### Conteúdo mínimo do `CLAUDE.md` do projeto

```markdown
# [Nome do Projeto] — Regras de Desenvolvimento

## Stack
[linguagem, framework, versões relevantes]

## Skills disponíveis
- `[projeto]-build` — build do projeto
- `[projeto]-test` — testes e lint

## Fluxo de trabalho
Seguir o fluxo global definido em ~/.claude/CLAUDE.md.
```

#### Para projetos integrados ao Linear

Se o projeto usa o Linear como ferramenta de gestão de tarefas, adicionar obrigatoriamente ao `CLAUDE.md` do projeto:

```markdown
## Integração com o Linear

Este projeto usa o **Linear** para gestão de tarefas. Ao trabalhar em qualquer issue do Linear:

### Skills obrigatórias
- **`personal-trainer-athlete` / skill de PR do Linear** — usar ao criar ou atualizar um Pull Request
  vinculado a uma issue do Linear. Garante que o PR siga o formato correto e seja linkado automaticamente.
- **Skill de criação do Linear** — usar quando for necessário criar novas issues, sub-tasks ou
  documentar descobertas encontradas durante o desenvolvimento.

### Regras
- Toda branch deve seguir o padrão `feature/TASK-ID` (ex: `feature/SOF-38`)
- Todo PR deve referenciar a issue com o identificador (ex: `SOF-38`) no título ou no corpo
- Mover a issue para **In Review** após abrir o PR
- Mover a issue para **Done** após o PR ser mergeado
```

> O `CLAUDE.md` do projeto deve ser commitado no repositório, assim todos os desenvolvedores (humanos e IAs) seguem as mesmas regras automaticamente.

---

### Fase 5 — Pre-commit Hooks

Todo projeto deve ter hooks de pre-commit configurados. Ao iniciar um projeto ou feature, criar/verificar `.husky/pre-commit` ou equivalente:

```bash
#!/bin/sh
# Lint
npm run lint        # ou equivalente do projeto

# Testes
npm run test        # ou equivalente do projeto

# Build (opcional, se rápido)
# npm run build
```

Se o projeto não tiver hooks, **criar antes de qualquer commit**.

---

### Fase 6 — Evidências

> 🦸 **Skill:** Antes de declarar qualquer coisa como "concluído", invocar `superpowers:verification-before-completion`. A skill exige rodar e capturar output dos comandos de verificação — evidências antes de assertions.

Toda tarefa executada deve gerar evidências documentadas:

#### Para o Linear (foco: produto)
- Funcionalidades implementadas
- Arquivos criados/modificados (com contagem de linhas)
- Comportamento esperado do ponto de vista do usuário
- Screenshots/outputs se houver UI

#### Para o PR (foco: validação)
- Passo a passo de como o ser humano deve validar a feature
- Cenários de teste manuais
- Pré-requisitos para testar
- Logs ou outputs que comprovam funcionamento
- Resultado dos testes automatizados

Formato do passo a passo de validação humana:

```markdown
## Como Validar Esta Feature

### Pré-requisitos
- [ ] Ambiente: [dev/staging]
- [ ] Dados: [o que precisa existir]

### Passo a Passo
1. Acesse [tela/endpoint]
2. Execute [ação]
3. Verifique [resultado esperado] ✅

### Casos de Borda
- Teste com [dado inválido] → deve exibir [erro esperado]
- Teste offline → deve [comportamento offline]
```

---

### Fase 7 — Branch & PR

> 🦸 **Skills:**
> - `superpowers:using-git-worktrees` — antes de iniciar trabalho que exige isolamento de branch
> - `superpowers:finishing-a-development-branch` — ao final da implementação para fechar a branch com PR estruturado
> - `superpowers:requesting-code-review` — após criar o PR para verificar se o trabalho atende aos requisitos
> - `superpowers:receiving-code-review` — ao receber feedback de revisores para aplicar com rigor técnico

O nome do branch segue o padrão:

```
feature/TASK-ID
```

Exemplo: `feature/SOF-38`

**Nunca usar** `feat/TASK-ID` — o prefixo correto é `feature/`, não `feat/`.

#### Regra de origem do branch

**Sempre criar o branch a partir da `main`**. Antes de criar qualquer branch de feature:

```bash
git checkout main
git pull origin main
git checkout -b feature/TASK-ID
```

Nunca criar branches a partir de outros branches de feature. A base é sempre `main`.

---

## 🐛 Debugging (transversal — qualquer fase)

> 🦸 **Skill:** Ao encontrar qualquer bug, falha de teste ou comportamento inesperado em **qualquer fase do fluxo**, invocar `superpowers:systematic-debugging` **antes de propor correções**. A skill exige diagnóstico baseado em evidências, não em suposições.

---

## 🔄 Regras Gerais

- **Nunca pular fases** do fluxo, mesmo sob pressão de prazo
- **Sempre em português** nas comunicações, comentários de código podem ser em inglês
- **Commits convencionais**: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`
- **Uma responsabilidade por commit** — commits pequenos e atômicos
- **Sem código morto** — remover antes de commitar
- **Sem TODOs no código** sem issue correspondente no Linear
