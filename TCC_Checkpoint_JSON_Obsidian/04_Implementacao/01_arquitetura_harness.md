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

> Nota técnica complementar; o protocolo científico vigente está no [artigo em Markdown](../07_Artigo_TCC/artigo_tcc_unitins.md).
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

O contrato é a reescrita integral GU-json de [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]], não o mecanismo de revisões programáticas de [[06_Referencias/referencias#PRISM|PRISM, 2025]]. O adapter de dados deve respeitar a política do SUMIE e qualquer contraste opcional, conforme definido no [artigo atual](../07_Artigo_TCC/artigo_tcc_unitins.md#3-materiais-e-métodos).

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

Caracterizar os adapters com os relatórios e cartões de [[06_Referencias/referencias#Qwen3 Technical Report|Qwen3]] e [[06_Referencias/referencias#T5Gemma|T5Gemma]]. [[06_Referencias/referencias#Block Diffusion|Block Diffusion]] fundamenta BD3LM, mas o checkpoint Qwen exato e sua API continuam pendentes. Fixar o modo thinking e registrar parâmetros específicos sem alegar equivalência de treinamento ou decoding.

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
