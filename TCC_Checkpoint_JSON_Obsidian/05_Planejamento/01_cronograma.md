---
title: "Cronograma sugerido"
aliases:
  - "01 cronograma"
tags:
  - tcc
  - planejamento
status: draft
---

# Cronograma sugerido

## Etapa 1 — revisão e especificação
**1–2 semanas**

- fechar RQs;
- fechar modelos;
- fechar schema;
- extrair método de Hwang;
- confrontar GU com PRISM e as variantes de Intrinsic Memory Agents, somente na revisão;
- estudar MemoryAgentBench;
- caracterizar modelos com Qwen3, T5Gemma e Block Diffusion;
- validar licenças/model cards.

Fontes e contrapontos: [[06_Referencias/artigos_prioridade|Ordem de leitura]]; [[06_Referencias/referencias|Bibliografia auditada]]. Não se acrescentam métodos ou datasets à coleta.

## Etapa 2 — harness mínimo
**1 semana**

- adapters;
- prompt;
- logger;
- parser;
- validator;
- métricas básicas.

## Etapa 3 — SUMIE
**1–2 semanas**

- adapter;
- piloto;
- validação do pipeline e das métricas de qualidade;
- validação de estados canônicos, preservação de perspectivas e adaptação do F1 original;
- execução completa;
- análise inicial.

## Etapa 4 — contraste FactConsolidation-SH
**1 semana**

- selecionar uma amostra de supersession;
- aplicar o mesmo schema, GU-json e limite de 300 tokens;
- analisar separadamente como contraste exploratório.

Respeitar a regra temporal de FactConsolidation; diferenças frente ao SUMIE não isolam o efeito da operação. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

## Etapa 5 — escrita
**contínua + 2 semanas finais**

Escrever resultados enquanto experimentos terminam.

## Regra de prioridade

Se houver atraso:

1. manter SUMIE;
2. manter três writers;
3. manter métricas longitudinais;
4. manter o orçamento fixo;
5. preservar logging e reprodutibilidade;
6. reduzir ou remover a amostra FactCon-SH antes de ampliar o escopo.
