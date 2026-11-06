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

Conformidade estrutural e atualização semântica requerem evidências distintas: [[06_Referencias/referencias#JSONSchemaBench|JSONSchemaBench, 2025]]; [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]].

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
**JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models** (2025).

Objetivo:
avaliar sistemas de constrained decoding sobre grande quantidade de JSON Schemas.

https://arxiv.org/abs/2501.10868

Comentário:
> Reforça que "gerar JSON válido" por si só já é um tópico bem estudado. O diferencial do TCC deve ser **preservar estado semântico através de atualizações sucessivas**.

## Grammar-Constrained Decoding

Paper:
**Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning**

Geng, Josifoski, Peyrard e West, EMNLP 2023. [[06_Referencias/referencias#Grammar-Constrained Decoding|Referência completa]].

https://aclanthology.org/2023.emnlp-main.674/

Uso:
- background de structured generation.

## Diffusion e estrutura

Trabalhos recentes estudam constrained decoding e structured data em diffusion language models.

### Constrained Decoding of Diffusion LLMs with Context-Free Grammars
https://arxiv.org/abs/2508.10111

### Agents of Diffusion
https://arxiv.org/abs/2601.07152

Versão estendida de 2026, AAMAS informado no arXiv. Usa mecanismos multiagente adicionais, não o protocolo de writer isolado deste TCC. [[06_Referencias/referencias#Agents of Diffusion|Referência completa]].

Comentário:
> Mündler et al. mostram que restrições podem mitigar falhas sintáticas de difusão; não é correto afirmar impossibilidade inerente de gerar JSON. Lu et al. encontram dificuldades em chamadas de ferramentas, mas resultados competitivos em memória textual com modelos de 7–8B. Essas tarefas não demonstram inferioridade em checkpoints JSON compactos. [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al., 2025]]; [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al., 2026]].

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
