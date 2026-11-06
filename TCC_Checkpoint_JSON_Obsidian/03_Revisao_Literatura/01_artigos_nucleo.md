---
title: "Artigos núcleo"
aliases:
  - "01 artigos nucleo"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Artigos núcleo

## 1. Hwang et al. — Enhancing Incremental Summarization with Structured Representations

**Prioridade: máxima**

Contribuições relevantes:

- introduz memória estruturada JSON em sumarização incremental;
- compara text vs. JSON;
- define Generate-Update e outras estratégias;
- propõe Chain-of-Key;
- avalia sob orçamento de memória;
- fornece predecessor direto para GU-JSON.

Uso no texto:
- fundamentar método;
- justificar JSON;
- discutir resultados publicados sobre atualização incremental com memória estruturada.

[[06_Referencias/referencias#hwang-structured|Referência completa]]

---

## 2. SUMIE

**Prioridade: máxima**

Benchmark sintético especificamente para incremental entity summarization.

Uso:
- dataset principal;
- ground truth estruturado;
- métricas P/R/F1.

https://aclanthology.org/2025.coling-main.721/

---

## 3. Hu et al. — MemoryAgentBench

**Prioridade: máxima**

Contribuições:

- protocolo incremental;
- quatro competências;
- FactConsolidation;
- Selective Forgetting.

Uso:
- justificar avaliação de atualização e supersession;
- dataset secundário.

[[06_Referencias/referencias#hu-memoryagentbench|Referência completa]]

---

## 4. Yuen et al. — Intrinsic Memory Agents

**Prioridade: alta**

Contribuições:

- memória estruturada por agente;
- atualização JSON via LLM;
- templates manual, generic e LLM-generated;
- benchmark PDDL/FEVER/ALFWorld.

Uso:
- evidenciar checkpoint JSON em agentes;
- justificar schema fixo como variável controlada.

[[06_Referencias/referencias#yuen-intrinsic|Referência completa]]

---

## 5. Zeng et al. — On the Structural Memory of LLM Agents

**Prioridade: alta**

Contribuições:

- chunks;
- triples;
- atomic facts;
- summaries;
- mixed memory;
- retrieval single-step, reranking e iterative.

Uso:
- posicionar o TCC como estudo de *memory writing*, não de representação/retrieval.

[[06_Referencias/referencias#zeng-structural|Referência completa]]

---

## 6. Maharana et al. — LoCoMo

**Prioridade: média/alta**

Uso:
- referência sobre memória conversacional longa, fora dos datasets deste experimento;
- conversas longas;
- event summarization;
- temporal reasoning.

[[06_Referencias/referencias#maharana-locomo|Referência completa]]

---

## 7. Xu et al. — Chain-of-Memory

**Prioridade: média/alta**

Uso:
- contextualizar a organização e o uso de memória em agentes;
- discutir decisões de construção do sistema, sem tratá-las como variáveis experimentais deste TCC.

[[06_Referencias/referencias#xu-com|Referência completa]]
