# Linear PR Workflow Skill

Automatiza o ciclo completo de desenvolvimento com Linear e GitHub.

## Instalação

```bash
# A skill já está instalada em:
~/.claude/skills/linear-pr-workflow/
```

## Como Usar

### Trigger automático
```
"processa as tarefas do linear"
"implemente SOF-20"
"fluxo completo de desenvolvimento"
"codex workflow"
```

### Requisitos

- ✅ Linear CLI autenticado (`linear` command)
- ✅ GitHub CLI autenticado (`gh` command)
- ✅ Git 2.34+ com worktree support
- ✅ Padrões de código em `.codex/*.md`

## Workflow

```
1. Detectar Projeto Linear ↓
2. Buscar Tasks em TODO (ordenadas por prioridade) ↓
3. Implementar Automaticamente (Agent) ↓
4. Abrir PR ↓
5. Revisar Codex (Agent) ↓
6. Solicitar Validação @codex ↓
7. Atualizar Status no Linear ↓
8. Pronto para Merge
```

## Scripts Disponíveis

- `detect_project.py` - Detecta projeto Linear baseado em Git remote
- `fetch_tasks.py` - Busca tasks em TODO ordenadas por prioridade
- `create_pr.py` - Cria PR no GitHub
- `update_linear_status.py` - Atualiza status de tarefa no Linear

## Estrutura

```
linear-pr-workflow/
├── SKILL.md                 # Definição da skill
├── README.md               # Este arquivo
├── scripts/
│   ├── detect_project.py   # Detectar projeto Linear
│   ├── fetch_tasks.py      # Buscar tasks
│   ├── create_pr.py        # Criar PR
│   └── update_linear_status.py  # Atualizar status
└── references/
    └── (nenhum por enquanto)
```

## Exemplos

### Processar próxima tarefa automática
```
"processa a próxima tarefa"

→ Detecta projeto (SofIA BR)
→ Busca tasks TODO por prioridade
→ Implementa SOF-20
→ Abre PR #9
→ Aplica codex guidelines
→ Solicita @codex review
→ Marca como "In Review"
```

### Implementar tarefa específica
```
"implemente SOF-32 offline mode"

→ Localiza SOF-32 no Linear
→ Implementa funcionalidade
→ Abre PR
→ Codex review automático
→ PR pronta para merge
```

## Status do Workflow

Cada tarefa passa por:

```
TODO → In Progress → In Review → Done
       (implementação)  (codex)     (após merge)
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Projeto não detectado | Skill pergunta ao usuário (100% certeza) |
| Sem tasks em TODO | Skill informa e aborta |
| Build falha | Mostrar erros e abortar |
| @codex não responde | Aguardar e permitir que user continue |

## Próximas Melhorias

- [ ] Suporte a múltiplos workspaces Linear
- [ ] Merge automático após @codex approve
- [ ] Integração com CI/CD checks
- [ ] Logging de histórico de workflows
- [ ] Configuração de timeouts
- [ ] Suporte a dependent tasks
