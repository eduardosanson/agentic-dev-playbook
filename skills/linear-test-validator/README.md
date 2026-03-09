# Linear Test Validator Skill

Executa testes automaticamente em tarefas do Linear e documenta resultados em PRs.

## Instalação

```bash
# A skill já está instalada em:
~/.claude/skills/linear-test-validator/
```

## Como Usar

### Trigger automático
```
"execute os testes de SOF-20"
"valide os testes da PR #9"
"rodar testes completos"
"teste automatizado com coverage"
```

### Requisitos

- ✅ Projeto com suite de testes (Jest, pytest, Gradle, Cypress, etc)
- ✅ GitHub CLI autenticado (`gh` command)
- ✅ Linear CLI autenticado (`linear` command)
- ✅ Git branch feat/TASK-ID

## Workflow

```
1. Detectar Contexto (branch, PR, tarefa) ↓
2. Descobrir Framework de Testes ↓
3. Executar Testes ↓
4. Capturar Resultados ↓
5. Criar Relatório Markdown ↓
6. Anexar à PR ↓
7. Reportar Status
```

## Scripts Disponíveis

- `detect_tests.py` - Detecta frameworks de teste disponíveis
- `run_tests.py` - Executa testes com framework detectado
- `parse_results.py` - Parseia outputs de teste
- `generate_report.py` - Cria relatório markdown

## Exemplos

### Executar testes da tarefa atual
```
"execute os testes da tarefa"

→ Detecta branch (feat/SOF-20)
→ Encontra PR associada
→ Executa testes
→ Anexa relatório
```

### Validar PR com coverage
```
"teste a PR #9 com coverage"

→ Checkout branch
→ Roda testes com coverage
→ Gera relatório com percentual
→ Comenta na PR
```

## Formatos Suportados

**JavaScript/TypeScript:**
- Jest
- Vitest
- Cypress
- Playwright
- Mocha

**Python:**
- pytest
- unittest

**Android/Kotlin:**
- Gradle test
- Espresso

**Go:**
- go test

**Ruby:**
- RSpec

**PHP:**
- PHPUnit

## Output Esperado

```
🎉 Todos os testes passaram!

✅ 5/5 testes unitários
✅ 3/3 testes de integração
📊 Coverage: 87%
⏱️ Tempo: 45s

[Detalhes completos na PR]
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Nenhum framework detectado | Criar suite de testes ou informar ao skill |
| Testes falhando | Ver logs, corrigir código, re-executar |
| Timeout | Se > 10 min, aumentar limite e re-executar |
| Branch não encontrada | Usar branch feat/TASK-ID |

## Integração com linear-pr-workflow

Use sequencialmente:

```bash
# 1. Implementar e abrir PR
"processa SOF-20"

# 2. Executar testes
"execute os testes de SOF-20"

# Ambos documentam em Linear e PR
```

## Próximas Melhorias

- [ ] Suporte a testes paralelos
- [ ] Integração com CI/CD (GitHub Actions)
- [ ] Alertas de performance
- [ ] Histórico de testes por tarefa
- [ ] Relatórios de regressão
