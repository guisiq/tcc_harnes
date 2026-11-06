---
title: "Memória em agentes LLM"
aliases:
  - "02 memoria agentes"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Memória em agentes LLM

## Conceitos úteis

### Memória contextual externa
Estado persistido fora dos pesos do modelo e reinjetado em interações futuras.

### Memória estruturada
Representação com unidades explícitas:
- JSON;
- triples;
- atomic facts;
- graphs;
- summaries organizados.

### Construção vs. utilização
Uma distinção importante encontrada na literatura:

```text
raw interaction
      ↓
memory construction
      ↓
memory store
      ↓
retrieval / organization
      ↓
agent reasoning
```

Este TCC isola principalmente **memory construction/update**.

## Zeng et al.

O estudo separa estruturas:

- chunks;
- knowledge triples;
- atomic facts;
- summaries;
- mixed.

Também separa retrieval:

- single-step;
- reranking;
- iterative.

Comentário:
> Excelente referência para mostrar que "estrutura da memória" é uma dimensão diferente de "arquitetura do modelo que escreve a memória".

## Yuen et al.

Memórias específicas por agente são mantidas em JSON e atualizadas após interações.

Ablations:
- manual template;
- generic template;
- LLM-generated template.

Comentário:
> Para o TCC, usar schema fixo evita transformar template design em uma segunda variável independente.

## Chain-of-Memory

O artigo argumenta que construção de memória excessivamente complexa pode gerar alto custo com ganho marginal.

Comentário:
> Reforça a justificativa prática de estudar writers pequenos e estruturas leves.

## MemoryAgentBench

Competências:

1. Accurate Retrieval
2. Test-Time Learning
3. Long-Range Understanding
4. Selective Forgetting

Comentário:
> `Selective Forgetting` deve inspirar as métricas de supersession e stale-fact rate.

## LoCoMo

Conversas:
- centenas de turnos;
- múltiplas sessões;
- eventos temporais;
- QA e summarization.

Comentário:
> Referência de literatura sobre diálogo de longo prazo; não integra a coleta deste TCC, que se limita ao SUMIE e ao contraste delimitado de FactConsolidation-SH.
