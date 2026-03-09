# Shared Spec vs Agent Implementation

Este repositório define o fluxo compartilhado de desenvolvimento agentico, não a implementação detalhada de cada agente, editor ou runtime.

## O que este repositório deve definir

- fases obrigatórias do workflow
- checkpoint de aprovação
- guardrails de execução
- critérios de evidência e validação
- padrão de log de decisões
- convenções para skills locais de projeto
- sugestões de integrações opcionais

## O que este repositório não deve definir

- caminhos obrigatórios de configuração para Cursor, Windsurf ou outros editores
- formato interno de plugins de cada agente
- arquivos de workspace específicos quando isso for responsabilidade do runtime
- instalação obrigatória de ferramentas externas opcionais

## Regra para agentes específicos

Cada agente deve decidir como materializar essa especificação no seu próprio ambiente.

Exemplos:

- Codex pode usar `AGENTS.md`, `~/.codex/skills/` e integrações locais próprias
- Claude pode usar `CLAUDE.md`, `.claude/skills/` e integrações como Superpowers
- Cursor e Windsurf podem converter a especificação para os arquivos de regra que seus runtimes exigirem

## Regra para integrações opcionais

Integrações externas, como `Superpowers`, devem ser tratadas como recomendadas quando agregam valor, nunca como dependência obrigatória do workflow padrão.

O papel do repositório é:

- mencionar a integração
- explicar quando ela ajuda
- oferecer automação opcional quando fizer sentido

## Regra para mudanças no workflow

Qualquer mudança no fluxo compartilhado só deve ser feita quando houver 100% de certeza de que:

- a mudança é realmente parte do padrão
- ela não invade detalhes de implementação do agente
- ela é segura para todos os agentes que consomem a especificação

Na dúvida:

- manter a regra no nível de especificação
- documentar a adaptação específica por agente fora do núcleo compartilhado
