---
title: "Metodologia de revisão e busca"
aliases:
  - "05 metodologia revisao"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Metodologia de revisão e busca

## Papel desta parte

A revisão do TCC pode usar uma busca estruturada, sem necessariamente transformar o trabalho em uma revisão sistemática completa.

## Petersen et al. — systematic mapping

Systematic mapping é apropriado para:

- estruturar uma área;
- classificar contribuições;
- identificar tópicos e lacunas;
- observar frequência de tipos de estudo.

Referências:
- Petersen et al. 2008
- Petersen et al. 2015

## Kitchenham et al.

Útil para diferenciar:

- SLR;
- systematic mapping;
- síntese de evidência;
- estudo terciário.

## Wohlin — snowballing

Procedimento útil:

### Backward snowballing
examinar referências de artigos núcleo.

### Forward snowballing
examinar artigos que citam os artigos núcleo.

## Estratégia sugerida para este TCC

### Seed papers

1. Hwang — structured incremental summarization
2. MemoryAgentBench
3. Yuen — Intrinsic Memory Agents
4. Zeng — Structural Memory
5. T5Gemma
6. DiffuLLaMA / diffusion adaptation

### Strings conceituais

```text
("LLM agent" OR "language model agent")
AND memory
AND (structured OR JSON OR state)
AND (update OR incremental OR consolidation)
```

```text
("diffusion language model")
AND (structured OR JSON OR infilling OR rewriting)
```

```text
("encoder-decoder" OR "seq2seq")
AND ("structured generation" OR JSON)
```

## Planilha de extração

Campos:

- título
- ano
- venue
- modelo(s)
- tamanho
- tipo de memória
- update method
- dataset
- métrica
- estrutura
- custo reportado
- código disponível?
- relação com RQ
- limitações

## Critério de parada

Interromper snowballing quando duas iterações consecutivas não adicionarem estudos primários relevantes ao recorte.
