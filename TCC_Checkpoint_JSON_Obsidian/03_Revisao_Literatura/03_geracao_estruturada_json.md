---
title: "Geração estruturada e JSON"
aliases:
  - "03 geracao estruturada json"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Geração estruturada e JSON

## Problema

Gerar JSON envolve pelo menos duas dimensões distintas:

1. **correção sintática**
2. **correção semântica**

Um output pode ser JSON válido e representar estado incorreto.

## Abordagens

### Prompt-only structured generation
O modelo recebe instruções e schema textual.

Vantagem:
- aplicável de forma relativamente uniforme aos três paradigmas.

Selecionado para o experimento principal.

### Constrained decoding
Um decoder externo impede sequências inválidas.

Exemplos:
- gramáticas CFG;
- JSON Schema;
- regex/automata;
- libraries como Guidance, Outlines, llama.cpp grammars e XGrammar.

Problema para este TCC:
- suporte e implementação podem variar por arquitetura;
- o estudo começaria a medir `modelo + decoder`.

Uso:
- revisão de literatura;
- possível baseline futuro.

## JSONSchemaBench

Paper:
**Generating Structured Outputs from Language Models: Benchmark and Studies**

Objetivo:
avaliar sistemas de constrained decoding sobre grande quantidade de JSON Schemas.

https://arxiv.org/abs/2501.10868

Comentário:
> Reforça que "gerar JSON válido" por si só já é um tópico bem estudado. O diferencial do TCC deve ser **preservar estado semântico através de atualizações sucessivas**.

## Grammar-Constrained Decoding

Paper:
**Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning**

https://aclanthology.org/2023.emnlp-main.674/

Uso:
- background de structured generation.

## Diffusion e estrutura

Trabalhos recentes estudam constrained decoding e structured data em diffusion language models.

### Constrained Decoding of Diffusion LLMs with Context-Free Grammars
https://arxiv.org/abs/2508.10111

### Agents of Diffusion
https://arxiv.org/abs/2601.07152

Comentário:
> Essa linha fortalece a relevância de avaliar diffusion em JSON, mas também mostra que estrutura rígida pode ser um ponto de dificuldade específico desse paradigma.

## Decisão experimental

Não usar reparo silencioso de JSON.

Registrar:

```text
raw_output
raw_json_valid
schema_valid
optional_repair_result
```

Se for criado um modo de reparo, ele deve ser análise separada.
