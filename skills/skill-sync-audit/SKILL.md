---
name: skill-sync-audit
description: Audit and optionally update the installed skills for the current agent against the skills in this repository. Use when the user wants to know which skills are installed, missing, outdated, similar, or updated after synchronization.
---

# Skill Sync Audit

## Resumo

Compara as skills deste repositório com as skills instaladas do agente atualmente em uso, detecta o que está ausente ou desatualizado, procura skills parecidas e atualiza o que for permitido.

## O que esta skill faz

1. Lê as skills do repositório em `skills/`
2. Detecta qual agente está em execução ou recebe isso explicitamente por parâmetro
3. Compara com o diretório de skills do agente-alvo
4. Para cada skill do repositório:
   - verifica se existe com o mesmo nome
   - verifica se está atualizada
   - se não existir, procura skills parecidas por nome e descrição
5. Com `--apply`, atualiza skills desatualizadas
6. Com `--install-missing`, instala skills ausentes mesmo que existam skills parecidas
7. Ao final, mostra:
   - agente auditado
   - skills presentes
   - skills ausentes
   - skills desatualizadas
   - skills atualizadas
   - skills instaladas
   - skills parecidas já existentes no ambiente do usuário

## Comandos

Auditar sem alterar:

```bash
skills/skill-sync-audit/scripts/sync_skills.py --repo-root /path/to/repo --agent codex
```

Atualizar skills já instaladas:

```bash
skills/skill-sync-audit/scripts/sync_skills.py --repo-root /path/to/repo --agent claude --apply
```

Atualizar e instalar ausentes:

```bash
skills/skill-sync-audit/scripts/sync_skills.py --repo-root /path/to/repo --agent claude --apply --install-missing
```

## Regras

- Nunca apagar skills do usuário automaticamente
- Criar backup antes de sobrescrever uma skill instalada
- Se o agente não puder ser detectado, pedir ou exigir `--agent`
- Se existir skill parecida mas não idêntica, relatar isso ao usuário sem bloquear a instalação da skill ausente
