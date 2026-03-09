---
name: systematic-debugging
description: Investigate failures and unexpected behavior using evidence-first debugging. Use when tests fail, runtime behavior diverges, or the root cause is unclear.
---

# Systematic Debugging

## Resumo

Conduz debugging baseado em evidências, evitando correções por palpite e exigindo isolamento da causa raiz antes da mudança.

## Quando usar

- Quando testes falham
- Quando o build quebra
- Quando o comportamento real diverge do esperado
- Quando a causa raiz não está clara

## O que esta skill faz

1. Reproduz a falha com o máximo de fidelidade possível
2. Coleta sinais observáveis: logs, stack traces, inputs, ambiente
3. Formula hipóteses e tenta falsificá-las
4. Isola a causa raiz antes de propor correção
5. Define a evidência que provará que o problema foi resolvido

## Saída esperada

- sintoma observado
- hipótese validada ou descartada
- causa raiz provável
- correção proposta
- evidência de verificação pós-correção

## Regra operacional

Não aplicar correção estrutural sem explicar qual evidência liga o sintoma à causa raiz.
