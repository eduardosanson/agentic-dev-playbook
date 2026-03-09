---
name: workspace-editor-sync
description: Export workspace rule files for editor agents such as Cursor and Windsurf from this repository's canonical rule assets. Use when a project workspace should be prepared or updated for editor-specific agent behavior.
---

# Workspace Editor Sync

## Resumo

Materializa arquivos de regras de workspace para editores como Cursor e Windsurf a partir dos overlays versionados no repositório.

## O que esta skill faz

1. Lê os overlays em `agent-rules/`
2. Exporta regras de workspace para:
   - Cursor
   - Windsurf
3. Atualiza os arquivos de workspace quando o padrão do repositório mudar
4. Informa o que foi gerado e onde

## Comandos

Auditar disponibilidade:

```bash
skills/workspace-editor-sync/scripts/sync_workspace_editors.py --repo-root /path/to/repo --workspace-root /path/to/workspace
```

Aplicar no workspace:

```bash
skills/workspace-editor-sync/scripts/sync_workspace_editors.py --repo-root /path/to/repo --workspace-root /path/to/workspace --apply
```

## Regras

- não apagar arquivos fora do escopo gerenciado
- materializar apenas os arquivos de workspace suportados
- registrar claramente o que é compatibilidade oficial e o que é compatibilidade mantida pelo projeto
