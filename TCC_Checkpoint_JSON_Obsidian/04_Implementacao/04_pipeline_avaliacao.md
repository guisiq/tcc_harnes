---
title: "Pipeline de avaliação"
aliases:
  - "04 pipeline avaliacao"
tags:
  - tcc
  - implementacao
status: draft
---

# Pipeline de avaliação

> Nota técnica complementar; não confundir o exemplo operacional com uma regra já validada. Confira as métricas e o protocolo no [artigo em Markdown](../07_Artigo_TCC/artigo_tcc_unitins.md).

## Passo 1 — parse

```text
raw output -> JSON parser
```

Sem heurística de correção no resultado principal.

## Passo 2 — schema

```text
parsed JSON -> JSON Schema validator
```

## Passo 3 — normalização

Quando necessário:

- ordem de chaves não importa;
- arrays: definir se ordem importa por campo;
- strings: evitar normalização semântica excessiva;
- números: preservar tipo esperado.

Definir e validar valores canônicos antes da coleta: igualdade textual ingênua pode penalizar paráfrases corretas. O SUMIE original combina correspondência exata e avaliação semântica por LLM; esta normalização determinística é uma adaptação, não reprodução de seu F1. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; consultar as [métricas do artigo](../07_Artigo_TCC/artigo_tcc_unitins.md#3-materiais-e-métodos).

## Passo 4 — comparação de estado

Converter estado para unidades comparáveis, por exemplo:

```text
(path, value)
```

Exemplo:

```text
("state.hotel.price", "290")
```

## Passo 5 — métricas de transição

Comparar:

```text
previous_state
expected_state
predicted_state
```

para identificar:

- campo que deveria ficar igual;
- campo que deveria mudar;
- campo novo.

Usar a política da tarefa e rótulos validados: preservar perspectivas conflitantes no SUMIE; marcar supersession somente diante de invalidação explícita. MemoryAgentBench avalia respostas, portanto suas métricas não substituem essa inspeção de estado. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

## Passo 6 — agregação

Agrupar por:

- writer;
- dataset;
- turn;
- operation type;
- erro estrutural vs. erro semântico.

## Estatística

Sugestão:

- médias e medianas;
- bootstrap 95% CI por amostra;
- diferenças pareadas, pois os três modelos veem os mesmos casos;
- effect size quando aplicável.

O contraste SUMIE/FactConsolidation-SH não separa efeito da operação e efeito do dataset. Não interpretar ausência de diferença detectada como prova de equivalência entre modelos.

## Visualizações

1. F1 por turno
2. Preservation por turno
3. Supersession por modelo
4. JSON validity por modelo
5. sucesso por condição
5. State F1 e Preservation Accuracy por writer
