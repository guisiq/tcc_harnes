---
title: "Mapa da literatura"
aliases:
  - "00 mapa literatura"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Mapa da literatura

## Eixo 1 — memória estruturada

Pergunta:
**Como representar informação persistente de agentes?**

Trabalhos:
- Zeng et al. — chunks, triples, atomic facts, summaries, mixed memory.
- Yuen et al. — memória estruturada específica por agente.
- Hwang et al. — JSON estruturado para sumarização incremental.

## Eixo 2 — atualização incremental

Pergunta:
**Como atualizar a representação sem reler todo o histórico?**

Trabalhos:
- Hwang et al. — Generate-Update, Generate-Merge, Chain-of-Key.
- Yuen et al. — LLM atualizando memória JSON a cada turno.
- ACE / adaptive context — contexto acumulado e refinado incrementalmente.

## Eixo 3 — avaliação de memória agente

Pergunta:
**Quais competências devem ser medidas?**

Trabalhos:
- MemoryAgentBench — Accurate Retrieval, Test-Time Learning, Long-Range Understanding, Selective Forgetting.
- LoCoMo — QA, event summarization e diálogo de muito longo prazo.
- LongMemEval — memória conversacional de longo prazo.


## Eixo 4 — construção de sistemas de memória
Pergunta:
**Como são organizados os componentes de construção e uso da memória?**

Trabalhos:
- Chain-of-Memory — discute a organização da construção e utilização da memória.
- MemEngine — framework modular para métodos de memória.

## Eixo 5 — structured generation

Pergunta:
**Como garantir estrutura JSON correta?**

Trabalhos:
- JSONSchemaBench — constrained decoding e conformidade com JSON Schema.
- Grammar-Constrained Decoding — gramáticas formais.
- Constrained decoding para diffusion LMs — geração estruturada não autoregressiva.

## Eixo 6 — arquiteturas gerativas

Pergunta:
**Como diferentes paradigmas geram transformações texto→estrutura?**

Trabalhos:
- T5Gemma — encoder-decoder adaptado de decoder-only.
- DiffuLLaMA/DiffuGPT — adaptação AR→diffusion.
- masked diffusion scaling.
- DiffusionGemma.
- trabalhos recentes de JSON/structured data com diffusion.

## Posição do TCC

```text
memory structure
      │
      └── JSON fixo
             │
incremental update
      │
      └── GU-JSON fixo
             │
generator paradigm
      ├── AR decoder-only
      ├── encoder-decoder
      └── diffusion
             │
evaluation
      ├── correctness
      ├── persistence
      ├── forgetting
      ├── quality by update turn
      ├── quality by operation
      └── FactCon-SH supersession contrast
```
