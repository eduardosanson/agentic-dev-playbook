# Tutorial: Instalação e Uso

Este tutorial mostra como clonar, validar, configurar e usar o repositório `agentic-dev-playbook` no dia a dia.

## 1. Pré-requisitos

Você precisa ter pelo menos:

- `git`
- `bash`
- `python3`

Opcional, mas recomendado:

- acesso ao GitHub para `git push` e `git fetch`
- um ambiente agentico com arquivo global de instruções, como `~/.codex/AGENTS.md` ou `~/.claude/CLAUDE.md`

## 2. Clonar o repositório

```bash
git clone git@github.com:eduardosanson/agentic-dev-playbook.git
cd agentic-dev-playbook
```

Se preferir HTTPS:

```bash
git clone https://github.com/eduardosanson/agentic-dev-playbook.git
cd agentic-dev-playbook
```

## 3. Validar a instalação local

Rode os scripts base do repositório:

```bash
./scripts/validate_repo.sh
./scripts/build_docs.sh
```

Resultado esperado:

- `validate_repo.sh` confirma que a estrutura obrigatória existe
- `build_docs.sh` gera o diretório `dist/`

## 4. Entender a estrutura

Os diretórios principais são:

- `AGENTS.md`: regra global do workflow
- `skills/`: skills reutilizáveis
- `templates/`: templates para novos projetos
- `docs/`: documentação operacional e análises
- `scripts/`: validações e utilitários do próprio repositório

## 5. Workflow padrão

O fluxo recomendado é:

```text
DOR -> SPEC -> PLAN -> APPROVAL -> TDD -> VERIFY -> EVIDENCE -> REVIEW/PR -> DONE
```

Resumo rápido:

1. `DOR`: confirmar se a demanda está pronta
2. `SPEC`: documentar requisitos e critérios de aceite
3. `PLAN`: definir ordem de implementação
4. `APPROVAL`: obter autorização para implementar
5. `TDD`: implementar começando por teste
6. `VERIFY`: rodar validações
7. `EVIDENCE`: registrar outputs e passos humanos
8. `REVIEW/PR`: submeter para revisão
9. `DONE`: concluir com rastreabilidade

Veja também:

- [workflow-flowchart.md](/home/eduardosanson/Dev/projects/agentic-dev-playbook/docs/workflow-flowchart.md)

## 6. Como usar as skills do repositório

As skills ficam em `skills/`. As principais categorias são:

### Skills de workflow

- `phase-refinement`
- `phase-skill-router`
- `approval-checkpoint`
- `evidence-capture`
- `systematic-debugging`

### Skills operacionais

- `agent-workflow-sync`
- `skill-sync-audit`
- `git-local-rules-sync`
- `project-init`
- `superpowers-sync`

### Skills de integração com Linear

- `linear`
- `linear-dependency-analyzer`
- `linear-pr-workflow`
- `linear-test-validator`

## 7. Sincronizar o workflow global do agente

Se você quer alinhar o arquivo global do seu agente com este repositório, use:

### Apenas auditoria

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py \
  --repo-root "$(pwd)" \
  --agent codex
```

### Aplicar atualização

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py \
  --repo-root "$(pwd)" \
  --agent codex \
  --apply
```

### Buscar a versão remota do GitHub antes de aplicar

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py \
  --repo-root "$(pwd)" \
  --agent codex \
  --fetch-remote \
  --apply
```

O script:

- detecta divergência
- cria backup antes de sobrescrever
- atualiza apenas o agente-alvo

## 8. Auditar e atualizar skills instaladas

Para comparar as skills do repositório com as skills instaladas do agente:

### Apenas auditoria

```bash
skills/skill-sync-audit/scripts/sync_skills.py \
  --repo-root "$(pwd)" \
  --agent codex
```

### Atualizar skills existentes

```bash
skills/skill-sync-audit/scripts/sync_skills.py \
  --repo-root "$(pwd)" \
  --agent codex \
  --apply
```

### Atualizar e instalar skills ausentes

```bash
skills/skill-sync-audit/scripts/sync_skills.py \
  --repo-root "$(pwd)" \
  --agent codex \
  --apply \
  --install-missing
```

O relatório final informa:

- quais skills já existem
- quais estão faltando
- quais estão desatualizadas
- quais foram atualizadas
- quais foram instaladas
- quais skills parecidas o usuário já tem

## 9. Sincronizar regras locais de Git

Para instalar templates de commit, hook e include de Git:

```bash
skills/git-local-rules-sync/scripts/sync_git_rules.sh "$(pwd)"
```

Isso instala arquivos gerenciados em:

```text
~/.config/agentic-dev-playbook/git/
```

E adiciona o `include.path` correspondente ao Git global.

## 10. Instalar e sincronizar Superpowers

O projeto integra o repositório oficial:

- `https://github.com/obra/superpowers`

Para Codex, a instalação oficial do Superpowers usa:

- clone em `~/.codex/superpowers`
- link em `~/.agents/skills/superpowers`

Este projeto automatiza isso com:

```bash
skills/superpowers-sync/scripts/sync_superpowers.py --repo-root "$(pwd)" --apply
```

Esse comando:

- instala ou atualiza o clone do Superpowers
- cria ou corrige o link de skills
- substitui skills locais sobrepostas por equivalentes do Superpowers
- remove skills locais gerenciadas que deixaram de existir no projeto
- grava log e manifesto local

### Cursor e Windsurf

Para materializar compatibilidade de workspace:

```bash
skills/superpowers-sync/scripts/sync_superpowers.py --repo-root "$(pwd)" --workspace-root "$(pwd)" --apply
```

Isso gera:

- `.cursor/rules/agentic-dev-playbook.mdc`
- `.windsurf/rules/agentic-dev-playbook.md`

Observação:

- Cursor tem caminho oficial de instalação do Superpowers por marketplace no repositório upstream
- Windsurf, no material inspecionado do Superpowers, não expõe um instalador oficial equivalente; aqui a compatibilidade é por regra de workspace

Arquivos de controle:

```text
~/.codex/rules/agentic-dev-playbook-superpowers-state.json
~/.codex/rules/agentic-dev-playbook-superpowers-log.jsonl
```

## 11. Iniciar um novo projeto com este playbook

Se você quer reaplicar esse padrão em outro repositório:

1. copie ou adapte o `AGENTS.md`
2. use os templates em `templates/agent/`
3. adicione as skills relevantes em `skills/`
4. crie as skills específicas do projeto
5. configure hooks de validação e build

Arquivos úteis:

- [templates/agent/AGENTS.md](/home/eduardosanson/Dev/projects/agentic-dev-playbook/templates/agent/AGENTS.md)
- [templates/agent/spec.md](/home/eduardosanson/Dev/projects/agentic-dev-playbook/templates/agent/spec.md)
- [templates/agent/prompt_plan.md](/home/eduardosanson/Dev/projects/agentic-dev-playbook/templates/agent/prompt_plan.md)

## 12. Uso recomendado no dia a dia

Fluxo simples:

1. atualizar o repositório
2. validar a estrutura
3. sincronizar workflow do agente se necessário
4. auditar skills instaladas
5. seguir o workflow do `AGENTS.md`
6. registrar decisões
7. capturar evidências antes de concluir

Exemplo:

```bash
git pull
./scripts/validate_repo.sh
skills/agent-workflow-sync/scripts/sync_agent_workflow.py --repo-root "$(pwd)" --agent codex
skills/skill-sync-audit/scripts/sync_skills.py --repo-root "$(pwd)" --agent codex
skills/superpowers-sync/scripts/sync_superpowers.py --repo-root "$(pwd)"
```

## 13. Quando usar cada skill principal

- Use `phase-refinement` quando a demanda estiver ambígua.
- Use `phase-skill-router` quando precisar mapear fases para skills.
- Use `approval-checkpoint` antes de sair do planejamento.
- Use `evidence-capture` antes de concluir ou abrir review.
- Use `systematic-debugging` quando houver falha ou comportamento inesperado.
- Use `project-init` ao iniciar automação em um projeto novo.
- Use `agent-workflow-sync` quando o workflow global do agente estiver desatualizado.
- Use `skill-sync-audit` quando quiser saber se o ambiente do agente está alinhado com o repositório.
- Use `superpowers-sync` quando quiser instalar ou atualizar o Superpowers e racionalizar skills locais sobrepostas.

## 14. Solução de problemas

### `validate_repo.sh` falhou

Verifique:

- arquivos obrigatórios ausentes
- skill movida para caminho diferente
- referências desatualizadas em `README.md` ou `AGENTS.md`

### `sync_agent_workflow.py` não detecta o agente

Passe explicitamente:

```bash
--agent codex
```

ou

```bash
--agent claude
```

### `sync_skills.py` não instala skill ausente

Use:

```bash
--apply --install-missing
```

### `--fetch-remote` falhou

O script tenta cair para a cópia local do repositório. Se isso não for suficiente, verifique:

- conectividade de rede
- autenticação Git
- configuração do remoto `origin`

### `sync_superpowers.py` removeu uma skill local

Isso só deve acontecer para skills gerenciadas por esse fluxo ou para skills explicitamente substituídas por equivalentes do Superpowers.

Verifique:

- `~/.codex/rules/agentic-dev-playbook-superpowers-log.jsonl`
- backups criados com sufixo `.bak.<timestamp>`

## 15. Próximos passos recomendados

- manter o `README.md` alinhado com novas skills
- atualizar o fluxograma quando o workflow mudar
- versionar novas skills no próprio repositório
- evitar regras importantes apenas em contexto temporário do agente
