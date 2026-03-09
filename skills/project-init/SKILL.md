---
name: project-init
description: Inicializa um projeto Kotlin ou Python com CLAUDE.md otimizado e skills de build/test. Use quando começar a trabalhar em um projeto pela primeira vez ou quando as skills do projeto não existirem ainda.
---

# Skill: project-init

## Resumo

Inicializa a automação operacional de um projeto detectando a stack e gerando instruções e skills básicas de build e teste.

## O que esta skill faz

Executa o setup completo de um projeto em **uma única invocação**:
1. Detecta a stack do projeto
2. Gera `CLAUDE.md` completo com comandos reais
3. Cria `.claude/skills/[projeto]-build/SKILL.md`
4. Cria `.claude/skills/[projeto]-test/SKILL.md`

## Passo 1 — Detectar a stack

Verificar a presença dos seguintes arquivos no diretório raiz do projeto:

| Arquivo encontrado | Stack |
|---|---|
| `build.gradle.kts` + `app/AndroidManifest.xml` | Kotlin Android |
| `build.gradle.kts` sem `AndroidManifest.xml` | Kotlin Backend |
| `pyproject.toml` | Python (uv/poetry) |
| `requirements.txt` sem `pyproject.toml` | Python (pip) |
| Ambos Gradle + Python | Multi-stack — gerar CLAUDE.md único com seções separadas; nomear skills como `[projeto]-build-kotlin`, `[projeto]-build-python`, `[projeto]-test-kotlin`, `[projeto]-test-python` |

**Se nenhum padrão for encontrado:**
Perguntar ao usuário: "Não consegui detectar a stack automaticamente. Este projeto é Kotlin Android, Kotlin Backend, Python, ou outro?"
Aguardar resposta antes de prosseguir com o passo 2.

Para Kotlin, identificar também:
- Linter: verificar em `build.gradle.kts` pelos plugins:
  - ktlint: buscar `id("org.jlleitschuh.gradle.ktlint")`
  - detekt: buscar `id("io.gitlab.arturbosch.detekt")`
  - Se nenhum encontrado, usar `ktlintCheck` como padrão (mais comum em projetos Android)
- Versão do Gradle: ler `gradle/wrapper/gradle-wrapper.properties`; se não existir, executar `./gradlew --version`

Para Python, identificar:
- Gerenciador: `uv` (existe `uv.lock`?), `poetry` (existe `poetry.lock`?), ou `pip`
- Linter: `ruff` (em `pyproject.toml` ou `ruff.toml`?), `flake8`, `black`
- Test runner: `pytest` (existe `pytest.ini` ou seção `[tool.pytest]`?)

## Passo 2 — Identificar nome do projeto

- Nome do projeto = nome do diretório raiz do repositório
- Confirmar com: `basename $(git rev-parse --show-toplevel)`

## Passo 3 — Gerar CLAUDE.md

Criar ou sobrescrever `CLAUDE.md` na raiz do projeto com o template correspondente à stack detectada.

### Template: Kotlin Android

```markdown
# [NOME_PROJETO] — Regras de Desenvolvimento

## Stack
Kotlin, Android, Gradle [VERSAO_GRADLE]
Linter: [ktlint | detekt]

## Comandos

| Ação | Comando |
|---|---|
| Build debug | `./gradlew assembleDebug` |
| Build release | `./gradlew assembleRelease` |
| Testes unitários | `./gradlew test` |
| Testes instrumentados | `./gradlew connectedAndroidTest` |
| Teste específico | `./gradlew test --tests "com.pacote.Classe.metodo"` |
| Lint check | `./gradlew ktlintCheck` |
| Lint fix | `./gradlew ktlintFormat` |

## Skills disponíveis
- `[NOME_PROJETO]-build` — build completo com reporte de erros
- `[NOME_PROJETO]-test` — lint + testes com cobertura

## Arquitetura
[preencher: Clean Architecture, MVVM, camadas do projeto]

## Convenções
- Pacote raiz: `com.[empresa].[projeto]`
- Estrutura de módulos: [preencher]
- Padrão de nomes de testes: `[Classe]Test.kt`

## Fluxo de trabalho
Seguir o fluxo global definido em `~/.claude/CLAUDE.md`.

## Integração com o Linear
[Adicionar se o projeto usar Linear — ver template no CLAUDE.md global]
```

### Template: Kotlin Backend

```markdown
# [NOME_PROJETO] — Regras de Desenvolvimento

## Stack
Kotlin, [Ktor | Spring Boot], Gradle [VERSAO_GRADLE]
Linter: [ktlint | detekt]

## Comandos

| Ação | Comando |
|---|---|
| Build | `./gradlew build` |
| Run local | `./gradlew run` |
| Testes | `./gradlew test` |
| Teste específico | `./gradlew test --tests "com.pacote.Classe.metodo"` |
| Lint check | `./gradlew ktlintCheck` |
| Lint fix | `./gradlew ktlintFormat` |

## Skills disponíveis
- `[NOME_PROJETO]-build` — build completo com reporte de erros
- `[NOME_PROJETO]-test` — lint + testes com cobertura

## Arquitetura
[preencher: Clean Architecture, camadas, padrões de módulos]

## Convenções
- Pacote raiz: `com.[empresa].[projeto]`
- Padrão de nomes de testes: `[Classe]Test.kt`

## Fluxo de trabalho
Seguir o fluxo global definido em `~/.claude/CLAUDE.md`.
```

### Template: Python

```markdown
# [NOME_PROJETO] — Regras de Desenvolvimento

## Stack
Python [VERSAO], [FastAPI | Django | script puro]
Gerenciador: [uv | poetry | pip]
Linter: [ruff | flake8 + black]

## Comandos

| Ação | Comando |
|---|---|
| Instalar deps | `uv sync` (ou `poetry install` / `pip install -r requirements.txt`) |
| Rodar app | detectar: (1) `[project.scripts]` em `pyproject.toml`, (2) `python -m [modulo_raiz]` se tiver `__main__.py`, (3) `uvicorn [modulo]:app` se FastAPI, (4) `python manage.py runserver` se Django |
| Testes | `pytest` |
| Teste específico | `pytest tests/caminho/test_arquivo.py::test_funcao -v` |
| Lint check | `ruff check .` |
| Lint fix | `ruff check . --fix` |
| Format check | `ruff format --check .` |
| Format fix | `ruff format .` |

## Skills disponíveis
- `[NOME_PROJETO]-build` — instalação de deps + verificação de imports
- `[NOME_PROJETO]-test` — lint + testes com cobertura

## Arquitetura
[preencher: estrutura de módulos, camadas, padrões]

## Convenções
- Módulo raiz: `[nome_pacote]/`
- Padrão de nomes de testes: `test_[modulo].py`

## Fluxo de trabalho
Seguir o fluxo global definido em `~/.claude/CLAUDE.md`.
```

## Passo 4 — Criar skill [projeto]-build

Criar o arquivo `.claude/skills/[NOME_PROJETO]-build/SKILL.md` dentro do repositório do projeto.

### Para Kotlin Android/Backend:

```markdown
---
name: [NOME_PROJETO]-build
description: Build completo do projeto [NOME_PROJETO]. Use antes de qualquer commit.
---

# Skill: [NOME_PROJETO]-build

## Executar

```bash
./gradlew [assembleDebug | build]
```

## Interpretar resultado

- **BUILD SUCCESSFUL** em X segundos → ok, avançar
- **BUILD FAILED** → capturar: arquivo, linha, mensagem de erro e reportar ao usuário
- **> Task :modulo:compilação FAILED** → indica o módulo com problema

## Reportar sempre

- Status: PASSED ou FAILED
- Tempo de build
- Em caso de falha: lista de erros com `arquivo:linha — mensagem`
```

### Para Python:

```markdown
---
name: [NOME_PROJETO]-build
description: Instalação de dependências e verificação do projeto [NOME_PROJETO].
---

# Skill: [NOME_PROJETO]-build

## Executar

```bash
uv sync  # ou: poetry install / pip install -r requirements.txt
python -c "import [modulo_raiz]"
```

## Interpretar resultado

- Sem erros de import → ok
- `ModuleNotFoundError` → dependência faltando, verificar pyproject.toml
- Erro de sintaxe → reportar arquivo e linha

## Reportar sempre

- Status: PASSED ou FAILED
- Em caso de falha: mensagem exata + arquivo + linha
```

## Passo 5 — Criar skill [projeto]-test

Criar `.claude/skills/[NOME_PROJETO]-test/SKILL.md` dentro do repositório.

### Para Kotlin:

```markdown
---
name: [NOME_PROJETO]-test
description: Lint + testes completos do projeto [NOME_PROJETO]. Executar antes de qualquer commit.
---

# Skill: [NOME_PROJETO]-test

## Executar (sempre nesta ordem)

### 1. Lint
```bash
./gradlew ktlintCheck
```
Se falhar: `./gradlew ktlintFormat` e reportar arquivos corrigidos.

### 2. Testes
```bash
./gradlew test
```

Para teste específico:
```bash
./gradlew test --tests "com.pacote.ClasseTest.nomeDoMetodo"
```

## Interpretar resultado

- `X tests completed, 0 failed` → todos passando
- `X tests completed, Y failed` → listar testes que falharam com mensagem de erro

## Reportar sempre

- Lint: passou ou lista de violações
- Testes: X passou, Y falhou, Z ignorados
- Cobertura (se configurada)
- Em falha: nome do teste + mensagem + stack trace relevante
```

### Para Python:

```markdown
---
name: [NOME_PROJETO]-test
description: Lint + testes completos do projeto [NOME_PROJETO]. Executar antes de qualquer commit.
---

# Skill: [NOME_PROJETO]-test

## Executar (sempre nesta ordem)

### 1. Lint + Format check
```bash
ruff check .
ruff format --check .
```
Se falhar lint: `ruff check . --fix`
Se falhar format: `ruff format .`

### 2. Testes
```bash
pytest -v --tb=short
```

Para teste específico:
```bash
pytest tests/caminho/test_arquivo.py::test_funcao -v
```

## Interpretar resultado

- `X passed` → ok
- `X passed, Y failed` → listar falhas com mensagem

## Reportar sempre

- Lint: passou ou lista de violações (arquivo:linha — regra)
- Testes: X passou, Y falhou, Z ignorados
- Cobertura: se `pytest-cov` estiver configurado, incluir %
- Em falha: nome do teste + assert que falhou + valores reais vs esperados
```

## Checklist final

Após rodar esta skill, verificar:

- [ ] `CLAUDE.md` existe na raiz com comandos preenchidos
- [ ] `.claude/skills/[projeto]-build/SKILL.md` existe
- [ ] `.claude/skills/[projeto]-test/SKILL.md` existe
- [ ] Arquivos commitados no repositório
