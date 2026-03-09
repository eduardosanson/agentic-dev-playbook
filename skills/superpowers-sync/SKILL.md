---
name: superpowers-sync
description: Install or update obra/superpowers for Codex, synchronize project skills against the active environment, replace overlapping local skills with Superpowers equivalents, and remove previously managed local skills that no longer exist in the project.
---

# Superpowers Sync

## Resumo

Instala ou atualiza o Superpowers para Codex, sincroniza as skills do projeto com o ambiente local, substitui skills locais sobrepostas por equivalentes do Superpowers e remove skills gerenciadas que deixaram de existir no projeto.

## Repositório Oficial

- `https://github.com/obra/superpowers`

## O que esta skill faz

1. Instala ou atualiza `obra/superpowers` em `~/.codex/superpowers`
2. Cria ou corrige o link `~/.agents/skills/superpowers`
3. Sincroniza as skills do projeto em `~/.codex/skills`
4. Substitui skills locais gerenciadas que foram mapeadas para equivalentes do Superpowers
5. Remove skills locais previamente gerenciadas que foram removidas do projeto
6. Gera log e manifesto do que foi alterado

## Substituições padrão

- `phase-refinement` -> `superpowers/brainstorming`
- `systematic-debugging` -> `superpowers/systematic-debugging`
- `evidence-capture` -> `superpowers/verification-before-completion`

## Saídas

- manifesto em `~/.codex/rules/agentic-dev-playbook-superpowers-state.json`
- log em `~/.codex/rules/agentic-dev-playbook-superpowers-log.jsonl`

## Comandos

Auditar sem alterar:

```bash
skills/superpowers-sync/scripts/sync_superpowers.py --repo-root /path/to/repo
```

Instalar ou atualizar e sincronizar:

```bash
skills/superpowers-sync/scripts/sync_superpowers.py --repo-root /path/to/repo --apply
```

## Regras

- criar backup antes de sobrescrever ou remover skill local
- não apagar skills não gerenciadas por este fluxo
- usar o repositório oficial do Superpowers como origem
- registrar toda alteração no log
