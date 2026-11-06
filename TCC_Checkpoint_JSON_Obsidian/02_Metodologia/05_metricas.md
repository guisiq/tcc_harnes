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

Base bibliográfica: [[06_Referencias/referencias#JSONSchemaBench|JSONSchemaBench]] e [[06_Referencias/referencias#Grammar-Constrained Decoding|Geng et al., 2023]] distinguem requisitos estruturais; [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]] e [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]] motivam avaliar conteúdo e atualização. As definições operacionais abaixo são do TCC, não métricas integralmente copiadas desses trabalhos.

O State F1 determinístico exige valores canônicos e normalização validada para não penalizar paráfrases corretas. O SUMIE original também usa avaliação de evidências por LLM; MemoryAgentBench mede respostas finais. Nenhum desses escores deve ser apresentado como diretamente equivalente ao State F1 deste protocolo.

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

Aplicável somente quando houver invalidação explícita, especialmente no contraste FactConsolidation-SH. Opiniões divergentes do SUMIE não são automaticamente valores obsoletos. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].


### Stale Fact Rate

Quantidade/proporção de fatos que deveriam ter sido invalidados mas continuam na memória.

Registrar como não aplicável quando a transição não exigir invalidação; não atribuir erro à preservação de perspectivas válidas.

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
