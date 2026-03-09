---
name: evidence-capture
description: Capture implementation evidence, validation outputs, and human verification steps. Use during VERIFY and EVIDENCE before declaring work complete.
---

# Evidence Capture

## Resumo

Captura as evidências operacionais da entrega, incluindo resultados de validação, comportamento esperado e passos de verificação humana.

## Quando usar

- Durante `VERIFY`
- Durante `EVIDENCE`
- Antes de marcar a tarefa como concluída
- Antes de abrir ou atualizar revisão/PR

## O que esta skill faz

1. Reúne outputs de build, testes e validações manuais
2. Resume o comportamento implementado do ponto de vista do usuário
3. Registra pré-requisitos e passos de validação humana
4. Destaca limitações, casos de borda e riscos aceitos
5. Organiza o material para PR, review ou handoff

## Saída esperada

- funcionalidades implementadas
- evidências automatizadas
- passo a passo de validação humana
- observações de borda ou limitações conhecidas

## Regra operacional

Não declarar conclusão sem evidência rastreável de que a validação foi executada.
