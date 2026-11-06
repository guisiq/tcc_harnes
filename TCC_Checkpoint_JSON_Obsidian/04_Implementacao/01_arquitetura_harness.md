---
title: "Arquitetura do harness"
aliases:
  - "01 arquitetura harness"
tags:
  - tcc
  - implementacao
status: draft
---

# Arquitetura do harness
      ↓
## Componentes

```text
Dataset Adapter
      ↓
Transition Stream
      ↓
Prompt Builder
      ↓
Memory Writer Adapter
      ↓
Raw Output Logger
      ↓
JSON Parser
      ↓
Schema Validator
      ↓
State Evaluator
      ↓
Result Store
```

## Interface comum do writer

Pseudo-interface:

```python
class MemoryWriter:
    def update(
        self,
        schema: dict,
        previous_state: dict,
        observation: str,
        max_output_tokens: int
    ) -> str:
        ...
```

Cada arquitetura implementa o mesmo contrato.

## Adapters

```text
QwenARWriter
T5GemmaWriter
QwenDiffusionWriter
```

## Regra crítica

O adapter pode adaptar APIs técnicas, mas **não deve alterar semanticamente o prompt** para favorecer um modelo.

Se templates especiais forem obrigatórios, documentar:

- template;
- role markers;
- BOS/EOS;
- generation parameters.

## Logging

Salvar sempre:

```text
experiment_id
dataset
sample_id
turn
writer
seed
prompt_hash
raw_prompt
raw_output
parsed_json
expected_json
error
```

## Estrutura sugerida de código

```text
src/
  datasets/
  writers/
  prompts/
  schemas/
  evaluation/
  
  cli/
configs/
results/
tests/
```
