---
name: superpowers-sync
description: Install or update obra/superpowers for Codex, prepare project compatibility assets for Cursor and Windsurf, synchronize project skills against the active environment, replace overlapping local skills with Superpowers equivalents, and remove previously managed local skills that no longer exist in the project.
---

# Superpowers Sync

## Resumo

Instala ou atualiza o Superpowers para Codex, prepara compatibilidade de workspace para Cursor e Windsurf, sincroniza as skills do projeto com o ambiente local, substitui skills locais sobrepostas por equivalentes do Superpowers e remove skills gerenciadas que deixaram de existir no projeto.

## Repositório Oficial

- `https://github.com/obra/superpowers`

## O que esta skill faz

1. Instala ou atualiza `obra/superpowers` em `~/.codex/superpowers`
2. Cria ou corrige o link `~/.agents/skills/superpowers`
3. Exporta regras de workspace para Cursor e Windsurf quando `--workspace-root` é informado
4. Sincroniza as skills do projeto em `~/.codex/skills`
5. Substitui skills locais gerenciadas que foram mapeadas para equivalentes do Superpowers
6. Remove skills locais previamente gerenciadas que foram removidas do projeto
7. Gera log e manifesto do que foi alterado

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

Instalar ou atualizar e também materializar compatibilidade de workspace para Cursor e Windsurf:

```bash
skills/superpowers-sync/scripts/sync_superpowers.py --repo-root /path/to/repo --workspace-root /path/to/workspace --apply
```

## Regras

- criar backup antes de sobrescrever ou remover skill local
- não apagar skills não gerenciadas por este fluxo
- usar o repositório oficial do Superpowers como origem
- registrar toda alteração no log
