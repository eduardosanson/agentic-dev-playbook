---
name: agentic-dev-playbook-test
description: Validate the structure and required content of the agentic-dev-playbook repository. Use before committing changes to this repository.
---

# Agentic Dev Playbook Test

## Resumo

Valida a estrutura mínima do repositório, os arquivos obrigatórios e a consistência básica do playbook antes de commit ou release.

Run the repository validation script:

```bash
./scripts/validate_repo.sh
```

Fail fast and report the missing or inconsistent file.
