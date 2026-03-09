---
name: linear-pr-workflow
description: |
  Automatiza o ciclo completo de desenvolvimento: desde buscar tarefas do Linear até ter PRs prontos com evidências documentadas e validação de codex.

  Use esta skill quando você quer:
  - Processar tarefas do Linear automaticamente
  - Implementar features e bugfixes com workflow completo
  - Gerar PRs com código seguindo padrões de projeto (codex)
  - Capturar evidências de cada tarefa (funcionalidade, testes, outputs)
  - Documentar como testar e validar o que foi implementado
  - Solicitar validação automática do codex e aguardar review
  - Atualizar status de tarefas no Linear com contexto completo

  Exemplos de triggers: "processa as tarefas do linear", "implemente SOF-20", "fluxo completo com evidências", "codex workflow completo", "abra PR com validações"
---

# Linear PR Workflow Skill

## Resumo

Executa um fluxo ponta a ponta a partir de uma task do Linear: seleção da tarefa, implementação, abertura de PR, coleta de evidências e atualização de status.

Automatiza o ciclo completo de desenvolvimento em projetos que usam Linear e GitHub com padrões de código (codex).

## 📋 O que esta skill faz

1. **Identifica o Projeto** → Detecta o projeto Linear baseado no repositório Git atual
2. **Busca Tarefas** → Pega tarefas em TODO ordenadas por prioridade
3. **Implementa** → Agent implementa a funcionalidade na branch feature/TASK-ID
4. **Abre PR & Move Status** → Cria PR com descrição automática e **move tarefa para In Review**
5. **Aplica Codex** → Agent revisa e corrige padrões de código
6. **Solicita Review** → Adiciona comentário @codex solicitando validação
7. **Captura Evidências** → Documenta funcionalidade, testes e outputs (Linear + PR)
8. **Finaliza Status** → Atualiza Linear com contexto completo (produto, funcionalidade, PR link)

## 🎯 Fluxo Passo-a-Passo

### Fase 1: Descoberta & Setup

```
Usuario chama skill
    ↓
Detectar projeto Linear (git remote origin → Linear workspace)
    ↓
Buscar tarefas TODO (ordenadas por prioridade)
    ↓
Se múltiplas tarefas:
    → Apresentar lista e usuário escolhe (ou usar primeira com maior prioridade)
Else:
    → Usar única tarefa encontrada
```

**Resultado:** Tarefa selecionada em formato:
```json
{
  "id": "SOF-20",
  "title": "[Android][Bug] Nome do treino vazio + edição de reps/kg",
  "priority": 3,
  "identifier": "SOF-20",
  "description": "...",
  "status": "Todo"
}
```

### Fase 2: Implementação Automática

**Antes de criar a branch**, buscar o nome exato via MCP:
```
get_issue(id: "TASK-ID") → usar o campo gitBranchName retornado
```

O campo `gitBranchName` já retorna o nome no padrão do Linear:
```
{username}/{issue-identifier}-{issue-title-slugified}
```

Exemplo: `eduardobosanson/sof-20-androidbug-nome-do-treino-vazio-edicao-de-repskg-ausente-na`

> ⚠️ **NUNCA usar** `feat/TASK-ID` como nome de branch — o Linear não consegue detectar o PR automaticamente com esse padrão.

**Agent chamado:**
- Lê a descrição da tarefa no Linear
- Busca `gitBranchName` da issue via MCP
- Explora estrutura do projeto
- Cria worktree (se necessário)
- Cria branch usando exatamente o valor de `gitBranchName`
- Implementa a solução
- Faz commit com mensagem padrão: `feat(TASK-ID): [Título da tarefa resumido]`
- Retorna status de sucesso/erro

**Inputs do agent:**
```
- Task ID, descrição completa e gitBranchName do Linear
- Estrutura do projeto (arquivos, convenções)
- Padrões detectados em commits recentes
```

**Output esperado:**
- ✅ Branch criada com nome exato do Linear (`gitBranchName`)
- ✅ Compilação bem-sucedida
- ✅ Commit realizado

### Fase 3: Abertura de PR e Atualização de Status Inicial

Após implementação:

```bash
# Usar o gitBranchName retornado pelo Linear (ex: "eduardobosanson/sof-20-...")
BRANCH=$(linear issue get TASK-ID --json | jq -r '.branchName')
# ou via MCP: get_issue(id) → gitBranchName

git push -u origin $BRANCH
gh pr create \
  --base main \
  --head $BRANCH \
  --title "feat(TASK-ID): [Título]" \
  --body "[Descrição automática do Linear]"
```

**Resultado:** PR aberta (ex: #9)

**⚡ Status Update Imediato:**
Assim que a PR é criada com sucesso, a skill **imediatamente** atualiza a tarefa no Linear:
- Status: `In Progress` → `In Review`
- Adiciona link da PR na tarefa
- Marca como "Aguardando Validação de Código"

⚠️ **CRÍTICO:** Este step é obrigatório - a tarefa DEVE estar em "In Review" antes de prosseguir

### Fase 4: Revisão de Codex

**Agent chamado com:**
- Arquivos modificados da branch
- Padrões de codex do projeto (ler `.codex/*.md`)
- Convenções de nomenclatura, documentação, estrutura

**Agent deve:**
1. Revisar cada arquivo contra padrões codex
2. Identificar desvios:
   - Imports duplicados
   - Comentários inconsistentes
   - Estrutura de pastas
   - Documentação de classes/funções
   - Separadores de seção
3. Fazer correções necessárias
4. Criar commit: `refactor: Apply codex guidelines to TASK-ID`
5. Fazer push da branch atualizada

**Output:**
- ✅ Código corrigido conforme padrões
- ✅ Commit de refactor realizado
- ✅ Branch atualizada no GitHub

### Fase 5: Solicitação de Review

Adiciona comentário no PR:

```markdown
@codex por favor revisar as correções de padrões codex aplicadas no commit [HASH].
Validar se todos os comentários, documentação e estrutura estão conforme guidelines do projeto.
Aprovar para merge se estiver conforme.
```

**Resultado:** Comentário adicionado, aguardando validação do codex

### Fase 6: Captura de Evidências

Agent executa procedimentos para capturar e documentar evidências em **dois contextos diferentes**:

#### 6.1 Evidências para Linear (Foco: Produto & Funcionalidade)

Documenta **o que** foi feito e **por que** funciona:

```markdown
## ✅ Evidências de Implementação

### Funcionalidades Implementadas
- ✅ [Feature 1] - Breve descrição do que foi feito
- ✅ [Feature 2] - Breve descrição do que foi feito

### Estrutura de Arquivos Criados/Modificados
\`\`\`
src/features/
├── new_feature/
│   ├── screens/
│   │   └── DetailScreen.kt (50 linhas)
│   ├── models/
│   │   └── FeatureModel.kt (30 linhas)
│   └── repository/
│       └── FeatureRepository.kt (45 linhas)
\`\`\`

### Dependências Adicionadas (se houver)
- library-name (version 1.2.3) - para [propósito]

### Impacto em Outras Áreas
- Nenhuma breaking change
- Compatível com versões anteriores

### Screenshots/Evidências Visuais
- [Link para screenshot 1]
- [Link para screenshot 2]

### Comportamento Esperado
1. Passo 1 do fluxo do usuário
2. Passo 2 do fluxo do usuário
3. Resultado esperado alcançado
```

**Instruções para Agent:**
- Usar linguagem amigável e focada em **produto**
- Listar arquivos criados/modificados com contagem de linhas
- Explicar **impacto** da mudança no projeto
- Se houver UI, capturar screenshots (usar `adb logcat` em Android, console browser, etc)
- Detalhar comportamento esperado do ponto de vista do usuário

#### 6.2 Evidências para PR (Foco: Testes & Validação)

Documenta **como testar** e **o que validar**:

```markdown
## 🧪 Como Testar Esta Implementação

### Pré-requisitos
- [ ] Environment: [DEV/STAGING/etc]
- [ ] Dados de teste: [especificar dados necessários]
- [ ] Branch: feature/TASK-ID

### Cenários de Teste

#### Cenário 1: [Descrição do teste]
**Passos:**
1. Ação 1
2. Ação 2
3. Ação 3

**Resultado Esperado:**
- Comportamento 1
- Comportamento 2

**Status:** ✅ Passou / ❌ Falhou

---

#### Cenário 2: [Caso extremo/edge case]
**Passos:**
1. ...

**Resultado Esperado:**
- ...

**Status:** ✅ Passou

---

### Testes Automatizados
\`\`\`bash
# Executar testes unitários
gradle test

# Executar testes de integração
gradle testIntegration

# Resultado:
# ✅ 5/5 testes passaram
\`\`\`

### Performance
- Tempo de load: [tempo]ms (esperado: < 500ms)
- Memória usada: [mem]MB
- Status: ✅ Dentro do esperado

### Logs Relevantes
\`\`\`
[Copiar logs relevantes que mostram execução bem-sucedida]
\`\`\`
```

**Instruções para Agent:**
- Detalhar **como reproduzir** cada cenário
- Incluir edge cases e validações
- Executar testes automatizados se existirem
- Capturar logs/outputs que comprovam funcionamento
- Especificar ambiente de teste

**Resultado:** Comentários adicionados no PR com guias práticos de teste

### Fase 7: Finalização de Status e Contexto

Atualiza tarefa no Linear com informações completas (após evidências capturadas):
- Status já está em `In Review` (desde Fase 3)
- **Agora:** Adiciona evidências de implementação (de 6.1) na descrição da tarefa
- Adiciona link do PR (já adicionado em Fase 3, agora com contexto)
- Marca como "Pronto para Codex Review & Testing"
- Notifica equipe que está pronta

**Resultado:** Tarefa com contexto completo, pronta para revisão e testes

**⚠️ Garantias de Status:**
```
Fase 3: TODO → ✅ IN REVIEW (logo após PR criada)
Fase 7: IN REVIEW + evidências anexadas (finalização com contexto)
```

## 🔍 Detecção de Projeto Linear

A skill identifica o projeto automaticamente:

```
1. Ler `.git/config` para encontrar origin URL
2. Mapear GitHub repo → Workspace Linear
   Exemplo: github.com/eduardosanson/athlete-android → SofIA BR
3. Se projeto não encontrado:
   → Perguntar ao usuário qual workspace
4. Buscar projeto no Linear baseado em padrão de nome
   (ex: "Android App", "Backend", "Frontend Web")
```

Se houver **dúvida**, sempre **perguntar ao usuário** (100% de certeza).

## 📸 Tipos de Evidências Capturadas

A skill captura evidências conforme possível para cada contexto:

### ✅ Sempre Possível
- ✅ **Estrutura de Arquivos** - Lista arquivos criados/modificados com contagem de linhas
- ✅ **Outputs de Compilação** - Logs de build/compile para validar sucesso
- ✅ **Commits e histórico Git** - Hashes, mensagens, arquivos alterados
- ✅ **Dependências Adicionadas** - Libs/packages incluídas com versões

### ⚠️ Possível com Contexto
- ⚠️ **Screenshots** - Se houver UI (Android/iOS/Web)
  - Android: Capturar via `adb screenshot` ou emulador
  - Web: Usar Chrome DevTools
  - iOS: Usar Xcode simulator
  - CLI: Não há UI visual, documentar output de texto em seu lugar

- ⚠️ **Testes Automatizados** - Se houver suite de testes
  - Android: `gradle test`, `gradle connectedAndroidTest`
  - Web: `npm test`, `jest`, `cypress`
  - Backend: `pytest`, `gotest`, `cargo test`
  - Resultado: ✅ 5/5 testes passaram ou ❌ logs de falha

- ⚠️ **Performance Metrics** - Se ferramentas estiverem disponíveis
  - Load time, memory, CPU usage
  - Pode usar profilers nativos ou logs de debug

- ⚠️ **Logs de Runtime** - Se aplicação escreve logs
  - Android: `adb logcat`
  - Web: Browser console
  - Backend: Application logs
  - CLI: stdout/stderr

### ❌ Não Possível & Alternativa
- ❌ **Gravação em Vídeo** - Tecnicamente complexo em todas as plataformas
  - Alternativa: Screenshots de estados-chave + documentação de fluxo

- ❌ **Teste Interativo em Tempo Real** - Requer ação humana
  - Alternativa: Skill `linear-test-validator` (separada) executa testes automáticos

- ❌ **Validação de UX** - Requer feedback humano
  - Alternativa: Screenshots + instruções claras para revisão manual

## ⚙️ Configuração

Para usar a skill, você precisa:

✅ **Linear CLI autenticado** (`linear` command disponível)
✅ **GitHub CLI autenticado** (`gh` command disponível)
✅ **Git com worktree support** (Git 2.34+)
✅ **Projeto no Linear com tasks em TODO**
✅ **Arquivos `.codex/*.md`** no repositório (padrões de código)

## 🤝 Integração com Skill de Testes

A skill `linear-test-validator` complementa o workflow automatizando testes:

```
linear-pr-workflow (implementação + documentação)
           ↓
   Cria evidências de teste (cenários)
           ↓
linear-test-validator (executa testes)
           ↓
   Fornece resultados para validação
```

**Como usar em sequência:**
```
Usuario: "processa SOF-20 com testes completos"

→ linear-pr-workflow: Implementa, abre PR, documenta testes
→ linear-test-validator: Executa testes automaticamente
→ Resultados anexados à PR
```

## 📌 Exemplos de Uso

### Exemplo 1: Processar Próxima Tarefa com Evidências
```
Usuario: "processa a próxima tarefa do Linear com evidências"

Workflow:
1. Identifica projeto (athlete-android → SofIA BR)
2. Busca tasks em TODO por prioridade
3. Encontra SOF-20 (priority=3)
4. Agent implementa
5. PR aberta #9
6. Codex review aplicado
7. @codex solicitado
8. **Evidências capturadas:**
   - Linear: funcionalidades, arquivos criados, impacto
   - PR: cenários de teste, pré-requisitos, validação
9. Tarefa → In Review (com documentação completa)
```

### Exemplo 2: Processar Tarefa com Testes Automáticos
```
Usuario: "implemente SOF-32 offline mode com testes"

Workflow:
1. linear-pr-workflow:
   - Detecta ID (SOF-32)
   - Implementa funcionalidade
   - Abre PR com guia de teste
   - Documenta cenários (produto + testes)

2. linear-test-validator:
   - Executa testes unitários
   - Valida cenários documentados
   - Anexa resultados à PR

3. Tarefa → In Review (pronta para merge após codex)
```

## 🔄 Status da Tarefa ao Longo do Fluxo

```
Inicial: TODO
  ↓ (Fase 2: implementação)
In Progress
  ↓ (Fase 3: PR aberta + status update)
⚡ IN REVIEW ← GARANTIDO ao abrir PR
  ↓ (Fase 4-5: codex review)
IN REVIEW (aguardando validação codex)
  ↓ (Fase 6: evidências capturadas)
IN REVIEW (com documentação completa)
  ↓ (Fase 7: finalização)
IN REVIEW (pronta para merge após codex aprovação)
  ↓
Done (após merge bem-sucedido)
```

**⚡ Garantia Crítica:**
- Tarefa SEMPRE em `IN REVIEW` assim que PR é criada (Fase 3)
- Não volta para status anterior
- Continua acumulando evidências até merge

## ⚡ Tratamento de Erros

| Erro | Ação |
|------|------|
| Projeto Linear não encontrado | Perguntar ao usuário (100% certeza) |
| Nenhuma task em TODO | Informar e abortar |
| Compilação falha | Abortar, exibir erros |
| PR não conseguiu abrir | Tentar novamente ou abortar |
| Codex não conseguiu corrigir | Exibir diffs e perguntar se continua |

## 🎓 Convenções de Commit

A skill usa commits padronizados:

```
feat(TASK-ID): [Título resumido]
[Linha em branco]
[Descrição com contexto]

Co-Authored-By: Claude Haiku <noreply@anthropic.com>
```

Exemplo:
```
feat(SOF-20): Add inline editing for reps/kg in WorkoutDetailScreen

Corrige bugs na tela de detalhes do treino:
- Nome do treino agora exibe corretamente
- Edição inline de reps/kg implementada
- Cards clicáveis para ativar modo edição

Co-Authored-By: Claude Haiku <noreply@anthropic.com>
```

## 📊 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ Usuario Invoca Skill                                        │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Detect Linear Project & Select Task                │
│ - Ler git remote origin                                      │
│ - Mapear para workspace Linear                              │
│ - Fetch tasks em TODO ordenadas por prioridade              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Implementation Agent                               │
│ - Create feature/TASK-ID branch                             │
│ - Implement functionality                                   │
│ - Commit changes                                            │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Open PR & Move Status to In Review                 │
│ - Push branch to origin                                     │
│ - Create PR with auto-generated description                │
│ - ⚡ Update Linear: TODO → IN REVIEW                        │
│ - Add PR link to Linear task                                │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Codex Review Agent                                 │
│ - Read .codex guidelines                                    │
│ - Review modified files                                     │
│ - Apply corrections & commit refactor                       │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 5: Request Codex Validation                           │
│ - Add @codex comment on PR                                  │
│ - Link task in Linear                                       │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 6: Capture Evidence & Document Tests                  │
│ - Documenting product/functionality to Linear               │
│ - Creating test scenarios & validation guide to PR          │
│ - Capturing screenshots, outputs, logs                      │
│ - Listing files created/modified                            │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 7: Update Linear Status                               │
│ - Mark task as "In Review"                                  │
│ - Attach evidence documentation                             │
│ - Link to PR with test instructions                         │
│ - Skill complete, ready for codex validation & testing      │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Próximos Passos Após Skill Completa

1. Codex valida PR (via comentário @codex)
2. Approva ou solicita mudanças
3. Ao aprovar: user faz merge
4. Marca tarefa como "Done" no Linear

---

## 📚 Referências

- Linear API: https://linear.app/api-reference
- GitHub CLI: https://cli.github.com/
- Padrões de Projeto: Ler `.codex/` do repositório
