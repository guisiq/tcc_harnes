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
- estudar MemoryAgentBench;
- validar licenças/model cards.

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
- execução completa;
- análise inicial.

## Etapa 4 — contraste FactConsolidation-SH
**1 semana**

- selecionar uma amostra de supersession;
- aplicar o mesmo schema, GU-json e limite de 300 tokens;
- analisar separadamente como contraste exploratório.

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
