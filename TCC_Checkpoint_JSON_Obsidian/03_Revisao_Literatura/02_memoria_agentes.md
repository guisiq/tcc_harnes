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

Para atualização persistente, priorizar [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]] e [[06_Referencias/referencias#PRISM|PRISM, 2025]]. GU reescreve o estado completo; PRISM aplica revisões programáticas. JSON é uma representação, não uma estratégia de recuperação.

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
> Referência contextual para distinguir representação e recuperação; não demonstra preservação em checkpoints reescritos. [[06_Referencias/referencias#Zeng et al. — Structural Memory|Zeng et al., 2024]].

## Yuen et al.

Memórias específicas por agente são atualizadas a partir do estado anterior e de novas saídas dos agentes. Algumas variantes usam JSON; a genérica permite representação livre na revisão de janeiro de 2026.

Ablations:
- manual template;
- generic template;
- LLM-generated template.

Comentário:
> Para o TCC, usar schema fixo evita transformar template design em uma segunda variável independente.

Essa é uma decisão de controle, não conclusão de superioridade: templates genéricos/gerados superam os manuais em vários testes. [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al., 2025/2026]]; [[06_Referencias/referencias#PRISM|PRISM, memória tipada com outro mecanismo de atualização]].

## Chain-of-Memory

O artigo estuda construção de memória e organização de fragmentos recuperados para raciocínio.

Comentário:
> Contexto sobre sistemas de memória, não evidência direta a favor de writers compactos no GU-json. [[06_Referencias/referencias#Xu et al. — Chain-of-Memory|Xu et al., 2026]].

## MemoryAgentBench

Competências:

1. Accurate Retrieval
2. Test-Time Learning
3. Long-Range Understanding
4. Selective Forgetting

Comentário:
> `Selective Forgetting` deve inspirar as métricas de supersession e stale-fact rate.

FactConsolidation define precedência temporal; o benchmark mede respostas, não o estado interno. LongMemEval também aborda atualização de conhecimento. Em contraste, SUMIE preserva perspectivas conflitantes: não rotular toda divergência como fato obsoleto. [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]]; [[06_Referencias/referencias#LongMemEval|LongMemEval]]; [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]].

## LoCoMo

Conversas:
- centenas de turnos;
- múltiplas sessões;
- eventos temporais;
- QA e summarization.

Comentário:
> Referência de literatura sobre diálogo de longo prazo; não integra a coleta deste TCC, que se limita ao SUMIE e ao contraste delimitado de FactConsolidation-SH.

[[06_Referencias/referencias#Maharana et al. — LoCoMo|Maharana et al., 2024]]. Para atualização de conhecimento, priorizar as referências da seção anterior, sem acrescentar datasets ao experimento.
