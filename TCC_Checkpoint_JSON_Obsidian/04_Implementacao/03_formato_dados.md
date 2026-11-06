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

```json
{
  "dataset": "sumie",
  "sample_id": "entity_001",
  "turn": 3,
  "previous_state": {
    "state": {}
  },
  "observation": "New information...",
  "expected_state": {
    "state": {}
  },
  "operations": [
    {
      "type": "UPDATE",
      "path": "state.price",
      "old": "100",
      "new": "120"
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
  "supersession_accuracy": 1.0,
  "hallucinated_facts": 1,
  "stale_facts": 0
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
