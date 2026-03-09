---
name: agent-workflow-sync
description: Check whether the current agent's global instruction file is aligned with this repository's workflow and update it from the repository or GitHub when requested. Use when the user wants to sync the active agent configuration with the latest playbook.
---

# Agent Workflow Sync

## Resumo

Compara o workflow deste repositório com o arquivo global do agente atualmente em uso e, se solicitado, atualiza esse arquivo usando a variante específica do agente.

## O que esta skill faz

1. Detecta qual agente está em execução ou recebe isso explicitamente por parâmetro
2. Resolve o arquivo global correspondente ao agente atual
3. Usa a variante específica do agente quando ela existir no repositório:
   - `agent-rules/codex/AGENTS.md`
   - `agent-rules/claude/CLAUDE.md`
4. Se não existir variante específica, usa `AGENTS.md` como fallback
5. Opcionalmente busca a versão remota do GitHub para a variante correta
6. Compara conteúdo, informa o que está atualizado ou defasado
7. Quando `--apply` é usado, cria backup e atualiza apenas o arquivo do agente-alvo
6. Ao final, gera um relatório com:
   - agente detectado
   - arquivo alvo resolvido
   - status de atualização
   - fallback usado, se houver

## Comandos

Auditar sem alterar nada:

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py --repo-root /path/to/repo --agent codex
```

Buscar a versão do GitHub e aplicar atualizações:

```bash
skills/agent-workflow-sync/scripts/sync_agent_workflow.py --repo-root /path/to/repo --agent claude --fetch-remote --apply
```

## Regras

- Não sobrescrever sem criar backup
- Não tentar atualizar todos os agentes ao mesmo tempo por padrão
- Se o agente não puder ser detectado, pedir ou exigir `--agent`
- Alterações de workflow devem respeitar as especificidades de cada agente
- Só unificar ou mudar comportamento entre agentes quando houver 100% de certeza de que a mudança é segura para ambos
- Se `--fetch-remote` falhar, relatar e cair para a versão local
