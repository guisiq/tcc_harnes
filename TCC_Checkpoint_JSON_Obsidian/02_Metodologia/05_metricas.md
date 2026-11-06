---
title: "Métricas"
aliases:
  - "05 metricas"
tags:
  - tcc
  - metodologia
status: draft
---

# Métricas

## Métricas estruturais

### JSON Validity
Percentual de outputs parseáveis por parser JSON padrão.

### Schema Validity
Percentual de outputs que respeitam campos, tipos e cardinalidades definidos.

---

## Métricas semânticas

### State Precision

\[
P = \frac{TP}{TP + FP}
\]

Mede quanto do conteúdo persistido é correto.

### State Recall

\[
R = \frac{TP}{TP + FN}
\]

Mede quanto do estado esperado foi preservado/registrado.

### State F1

\[
F1 = \frac{2PR}{P+R}
\]

Deve ser uma das métricas centrais.

---

## Métricas de transição

### Update Accuracy

\[
UA = \frac{\text{atualizações corretas}}{\text{atualizações esperadas}}
\]

### Preservation Accuracy

\[
PA = \frac{\text{campos inalterados preservados corretamente}}
{\text{campos que deveriam permanecer inalterados}}
\]

### Supersession Accuracy

Percentual de valores obsoletos corretamente substituídos.


### Stale Fact Rate

Quantidade/proporção de fatos que deveriam ter sido invalidados mas continuam na memória.

### Hallucination Rate

Novos pares chave-valor sem suporte na entrada ou no estado anterior.

---

## Métricas longitudinais

Todas as métricas acima devem ser calculadas por número de atualização:

```text
t = 1, 2, 3, ..., n
```

Gráficos principais:

- F1 × turno
- Preservation Accuracy × turno
- Stale Fact Rate × turno

---

---

## Regra

Registrar métricas brutas por amostra. Nunca salvar apenas médias agregadas.
