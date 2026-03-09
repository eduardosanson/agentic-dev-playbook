---
name: agent-workflow-sync
description: Check whether the current agent's global instruction file is aligned with this repository's workflow and update it from the repository or GitHub when requested. Use when the user wants to sync the active agent configuration with the latest playbook.
---

# Agent Workflow Sync

## Resumo

Compara o workflow deste repositório com o arquivo global do agente atualmente em uso e, se solicitado, atualiza esse arquivo a partir da versão local ou da versão mais recente do GitHub.

## O que esta skill faz

1. Detecta qual agente está em execução ou recebe isso explicitamente por parâmetro
2. Resolve o arquivo global correspondente ao agente atual
2. Usa `AGENTS.md` deste repositório como fonte local
3. Opcionalmente busca `origin/main:AGENTS.md` para usar a versão remota do GitHub
4. Compara conteúdo, informa o que está atualizado ou defasado
5. Quando `--apply` é usado, cria backup e atualiza apenas o arquivo do agente-alvo
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
- Se `--fetch-remote` falhar, relatar e cair para a versão local
