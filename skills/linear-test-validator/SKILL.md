---
name: linear-test-validator
description: |
  Executa testes automaticamente em tarefas do Linear e documenta resultados em PRs.

  Use esta skill quando você quer:
  - Executar testes unitários, integração ou e2e automaticamente
  - Validar cenários de teste documentados na PR
  - Capturar outputs de testes e logs
  - Documentar resultados de teste no formato markdown
  - Validar antes de fazer merge da PR
  - Integrar com linear-pr-workflow para fluxo completo de testes

  Exemplos de triggers: "execute os testes de SOF-20", "valide os testes da PR #9", "rodar testes completos", "teste automatizado SOF-32", "validar testes com coverage"
---

# Linear Test Validator Skill

Executa testes automaticamente em implementações do Linear, capturando resultados e documentando evidências de validação.

## 📋 O que esta skill faz

1. **Detecta Contexto** → Identifica branch atual, PR associada, tarefa do Linear
2. **Descobre Testes** → Encontra suite de testes (Jest, pytest, Gradle, etc)
3. **Executa Testes** → Roda testes unitários, integração, e2e
4. **Captura Resultados** → Coleta outputs, logs, coverage reports
5. **Documenta** → Cria relatório markdown com resultados
6. **Anexa à PR** → Comenta na PR com evidências de teste

## 🎯 Fluxo Passo-a-Passo

### Fase 1: Descoberta de Contexto

```
Usuario executa skill
    ↓
Detectar branch atual (ex: feat/SOF-20)
    ↓
Encontrar PR associada no GitHub
    ↓
Buscar tarefa correspondente no Linear
    ↓
Ler cenários de teste documentados na PR
```

**Resultado:** Contexto completo para execução de testes

### Fase 2: Detecção de Framework de Testes

Agent detecta automaticamente qual framework está em uso:

**JavaScript/TypeScript:**
- Jest: `npm test` ou `yarn test`
- Vitest: `vitest run`
- Cypress: `cypress run`
- Playwright: `playwright test`

**Python:**
- pytest: `pytest --verbose --cov`
- unittest: `python -m unittest discover`

**Android/Kotlin:**
- Gradle: `gradle test connectedAndroidTest`
- Espresso: Testes de integração via emulador

**Go:**
- `go test ./... -v -cover`

**Ruby:**
- RSpec: `rspec --format documentation`

**PHP:**
- PHPUnit: `./vendor/bin/phpunit`

Se múltiplos frameworks encontrados, executa todos e reporta separadamente.

### Fase 3: Execução de Testes

Agent executa testes com flags para capturar máximo de informação:

```bash
# Exemplo JavaScript
npm test -- --verbose --coverage --collectCoverageFrom="src/**/*.js"

# Exemplo Python
pytest --verbose --tb=short --cov=src --cov-report=html

# Exemplo Android
gradle test connectedAndroidTest --info --stacktrace
```

**Timeout Padrão:** 10 minutos por suite de testes

**Parada em Erro:** Se testes falharem, continua para capturar todos os erros

### Fase 4: Captura de Resultados

Agent coleta:

- ✅ **Resultado Geral** - X/Y testes passaram
- ✅ **Testes que Passaram** - Lista de testes bem-sucedidos (por nome)
- ❌ **Testes que Falharam** - Lista com motivos específicos
- 📊 **Coverage Report** - % de cobertura de código (se disponível)
- 📋 **Logs Detalhados** - Output completo do teste (últimas 500 linhas se muito grande)
- ⏱️ **Tempo de Execução** - Quanto tempo levou cada suite
- 🐛 **Stack Traces** - Erros detalhados para debugging

### Fase 5: Documentação Markdown

Agent cria relatório estruturado para anexar à PR:

```markdown
## 🧪 Resultados de Testes Automáticos

### Resumo
- ✅ **5/5** testes unitários passaram
- ✅ **3/3** testes de integração passaram
- ✅ **Coverage:** 87% de cobertura de código

### Execução Total
- ⏱️ Tempo: 45 segundos
- 📦 Testes executados em: [plataforma]

---

### Detalhes por Suite

#### Unit Tests
\`\`\`
✅ sum() returns correct result
✅ validateEmail() rejects invalid emails
✅ parseJSON() handles edge cases
✅ cacheManager stores and retrieves data
✅ middleware logs all requests
\`\`\`

**Tempo:** 12s | **Coverage:** 92%

#### Integration Tests
\`\`\`
✅ Database connection works
✅ API endpoints respond correctly
✅ Authentication flow completes
\`\`\`

**Tempo:** 8s | **Coverage:** 81%

#### End-to-End Tests
\`\`\`
✅ User signup flow
✅ Login and session management
✅ Logout clears session
\`\`\`

**Tempo:** 25s

---

### Coverage Report

| Arquivo | Linhas | Cobertas | % |
|---------|--------|----------|---|
| src/utils.js | 150 | 138 | 92% |
| src/api.js | 200 | 165 | 82% |
| src/auth.js | 100 | 100 | 100% |

**Total:** 87% de cobertura

---

### Logs Completos

\`\`\`
[Test run output - últimas 500 linhas]
...
\`\`\`

### ✅ Validação

- ✅ Todos os testes passaram
- ✅ Coverage acima de 80%
- ✅ Sem warnings ou deprecations
- ✅ Performance dentro dos limites
```

### Fase 6: Anexação à PR

Agent adiciona comentário na PR com:

1. Relatório markdown (Fase 5)
2. Link para coverage report (se HTML disponível)
3. Instruções para rodá-los localmente
4. Próximos passos (merge ou correções necessárias)

```markdown
@user Testes automaticamente executados e validados! ✅

**Status:** Pronto para merge
**Coverage:** 87%
**Testes:** 11/11 passaram

[Ver relatório completo acima]

Para rodar localmente:
\`\`\`bash
npm test -- --coverage
\`\`\`

---

*Testado via linear-test-validator em YYYY-MM-DD HH:MM:SS*
```

## 📊 Relatório de Testes - Formato Estruturado

O skill sempre produz um relatório com esta estrutura:

```json
{
  "task_id": "SOF-20",
  "pr_number": 9,
  "timestamp": "2026-03-08T15:30:00Z",
  "summary": {
    "total_tests": 11,
    "passed": 11,
    "failed": 0,
    "skipped": 0,
    "coverage_percent": 87
  },
  "suites": [
    {
      "name": "Unit Tests",
      "total": 5,
      "passed": 5,
      "failed": 0,
      "duration_ms": 1200,
      "coverage_percent": 92,
      "tests": [
        {
          "name": "sum() returns correct result",
          "status": "passed",
          "duration_ms": 15
        }
      ]
    }
  ],
  "logs": {
    "stdout": "...",
    "stderr": ""
  },
  "errors": [],
  "status": "success"
}
```

## 🔄 Integração com linear-pr-workflow

**Workflow completo:**

```
1. linear-pr-workflow executa
   ↓
   Implementa código
   Abre PR
   Documenta cenários de teste
   ↓
2. linear-test-validator executa
   ↓
   Rodas testes automaticamente
   Valida cenários documentados
   Anexa resultados
   ↓
3. Tarefa → In Review (com testes validados)
```

## ⚙️ Requisitos

✅ **Framework de Testes** - Projeto deve ter suite de testes (Jest, pytest, Gradle, etc)
✅ **Git Branch** - Estar em uma branch feat/TASK-ID
✅ **GitHub CLI** (`gh` command disponível)
✅ **Linear CLI** (`linear` command disponível)

## 📋 Como Usar

### Caso 1: Executar testes da tarefa atual

```
Usuario: "execute os testes da tarefa"

Skill:
1. Detecta branch (feat/SOF-20)
2. Encontra PR associada
3. Lê cenários de teste documentados
4. Executa framework detectado
5. Anexa resultados à PR
6. Reporta status
```

### Caso 2: Validar PR específica

```
Usuario: "valide os testes da PR #9"

Skill:
1. Encontra PR #9
2. Checkout branch associada
3. Executa testes
4. Comenta com resultados
```

### Caso 3: Coverage Report

```
Usuario: "rodar testes com coverage completo"

Skill:
1. Executa testes
2. Gera coverage report em HTML
3. Calcula percentual
4. Anexa links à PR
```

## ⚠️ Tratamento de Erros

| Erro | Ação |
|------|------|
| Nenhum framework de teste detectado | Informar ao usuário e listar diretórios de teste encontrados |
| Testes falhando | Mostrar motivos de falha e sugerir correções |
| Timeout em testes | Parar execução, reportar quais testes ficaram presos |
| Sem permissão em arquivo | Pedir permissões necessárias |

## 📝 Exemplos de Output

### ✅ Sucesso Total
```
🎉 Todos os testes passaram!

✅ 11/11 testes validados
📊 Coverage: 87%
⏱️ Tempo total: 45s

[Detalhes anexados à PR #9]
```

### ⚠️ Alguns Falharam
```
⚠️ 2/11 testes falharam

❌ TestUserAuthentication.testInvalidPassword
   → Expected true, got false (linha 45)

❌ TestDatabaseConnection.testTimeout
   → Connection timeout after 30s

[Logs detalhados na PR - revisar e corrigir]
```

### ❌ Sem Testes
```
ℹ️ Nenhuma suite de testes detectada

Diretórios procurados:
- tests/
- __tests__/
- test/
- spec/

[Criar testes e executar novamente]
```

## 🚀 Próximos Passos Após Execução

1. **Se todos passaram:** PR pronta para merge (aguardar codex)
2. **Se alguns falharam:** Corrigir código, rodar skill novamente
3. **Se sem testes:** Criar testes e re-executar skill

## 📚 Referências

- Jest: https://jestjs.io/
- pytest: https://pytest.org/
- Gradle Test: https://docs.gradle.org/current/userguide/testing_gradle_projects.html
- Cypress: https://www.cypress.io/
- Coverage Reports: https://istanbul.js.org/

---

## 💡 Dicas de Uso

1. **Use junto com linear-pr-workflow** - Ativa testes automáticos após implementação
2. **Configure timeout** - Se testes levam mais que 10 min, informar skill
3. **Valide coverage** - Mínimo 80% recomendado para PRs
4. **Re-execute se corrigir** - Depois de corrigir falhas, rode skill novamente
