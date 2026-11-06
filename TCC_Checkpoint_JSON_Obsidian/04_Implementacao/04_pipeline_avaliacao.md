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

## Visualizações

1. F1 por turno
2. Preservation por turno
3. Supersession por modelo
4. JSON validity por modelo
5. sucesso por condição
5. State F1 e Preservation Accuracy por writer
