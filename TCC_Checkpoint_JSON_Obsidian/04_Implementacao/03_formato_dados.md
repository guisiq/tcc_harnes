---
title: "Formato dos dados"
aliases:
  - "03 formato dados"
tags:
  - tcc
  - implementacao
status: draft
---

# Formato dos dados

## Transition record

JSONL recomendado:

Exemplo fictício de integração de perspectivas, não registro extraído do dataset. SUMIE fornece anotações por parágrafo; os estados acumulados e rótulos são construídos e validados pelo projeto. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., GU-json]].

```json
{
  "dataset": "sumie",
  "sample_id": "entity_001",
  "turn": 3,
  "previous_state": {
    "state": {"price": "described as expensive"}
  },
  "observation": "Another reviewer describes the price as affordable.",
  "expected_state": {
    "state": {"price": "described as expensive by one reviewer and affordable by another"}
  },
  "operations": [
    {
      "type": "UPDATE",
      "path": "state.price",
      "old": "described as expensive",
      "new": "described as expensive by one reviewer and affordable by another"
    }
  ]
}
```

## Prediction record

```json
{
  "experiment_id": "exp_001",
  "writer": "qwen3_0_6b",
  "dataset": "sumie",
  "sample_id": "entity_001",
  "turn": 3,
  "raw_output": "...",
  "json_valid": true,
  "schema_valid": true,
  "parsed_state": {}
}
```

## Evaluation record

Valores apenas ilustrativos. Usar `null` para métricas sem transições aplicáveis, não sucesso artificial ou erro por preservar uma opinião válida. Supersession requer invalidação explícita, como a regra temporal de FactConsolidation-SH. [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

```json
{
  "sample_id": "entity_001",
  "turn": 3,
  "writer": "qwen3_0_6b",
  "precision": 0.91,
  "recall": 0.88,
  "f1": 0.895,
  "preservation_accuracy": 0.95,
  "update_accuracy": 0.84,
  "supersession_accuracy": null,
  "hallucinated_facts": 1,
  "stale_facts": null
}
```

## Reprodutibilidade

Nunca sobrescrever resultados crus.

Estrutura:

```text
results/
  raw/
  parsed/
  metrics/
  
  aggregates/
```
