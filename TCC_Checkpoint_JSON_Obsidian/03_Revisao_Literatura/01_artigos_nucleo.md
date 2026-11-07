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

> **Notas de leitura para revisão pessoal.** Confirme os resultados e limites nas fontes originais antes de citá-los. O [artigo em Markdown](../07_Artigo_TCC/artigo_tcc_unitins.md) é a referência para o escopo atual.

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

GU-json é o protocolo fixo, não o método vencedor universal: o próprio artigo relata vantagem de CoK. [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., Findings EMNLP 2024]]; [[06_Referencias/referencias#PRISM|PRISM, alternativa programática de 2025]].

---

## 2. SUMIE

**Prioridade: máxima**

Benchmark sintético especificamente para incremental entity summarization.

Uso:
- dataset principal;
- anotações por parágrafo a adaptar para estados acumulados;
- motivação para métricas P/R/F1, sem equivalência automática com o State F1 local.

https://aclanthology.org/2025.coling-main.721/

Publicado no COLING 2025, após preprint de 2024. O prompt UPDATE preserva valores e perspectivas conflitantes; não define substituição automática pelo valor mais recente. A avaliação original inclui comparação semântica de evidências por LLM. [[06_Referencias/referencias#Hwang et al. — SUMIE|Referência completa]].

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
- amostra exploratória de FactConsolidation-SH, não segundo benchmark completo.

FactConsolidation usa precedência temporal explícita e avalia respostas finais. Não mede diretamente remoção de fatos do estado nem prova a H2. LongMemEval complementa a motivação de atualização de conhecimento. [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench, 2025/2026]]; [[06_Referencias/referencias#LongMemEval|LongMemEval, 2025]].

---

## 4. Yuen et al. — Intrinsic Memory Agents

**Prioridade: alta**

Contribuições:

- memória estruturada por agente;
- atualização contextual via LLM; JSON em algumas variantes;
- templates manual, generic e LLM-generated;
- benchmark PDDL/FEVER/ALFWorld.

Uso:
- evidenciar checkpoint JSON em agentes;
- discutir o schema fixo como controle do TCC, não como escolha universalmente superior.

A revisão de janeiro de 2026 permite representação livre no template genérico; templates genéricos/gerados superam os manuais em vários testes. São resultados de sistemas multiagente, não de fidelidade por transição. [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Referência completa]].

---

## 5. Zeng et al. — On the Structural Memory of LLM Agents

**Prioridade: complementar**

Contribuições:

- chunks;
- triples;
- atomic facts;
- summaries;
- mixed memory;
- retrieval single-step, reranking e iterative.

Uso:
- posicionar o TCC como estudo de *memory writing*, não de representação/retrieval.

Não fundamenta reescrita de checkpoints ou supersession. Para esses argumentos, usar Hwang/PRISM/Yuen e MemoryAgentBench, respectivamente. [[06_Referencias/referencias#Zeng et al. — Structural Memory|Referência completa]].

---

## 6. Maharana et al. — LoCoMo

**Prioridade: complementar**

Uso:
- referência sobre memória conversacional longa, fora dos datasets deste experimento;
- conversas longas;
- event summarization;
- temporal reasoning.

[[06_Referencias/referencias#Maharana et al. — LoCoMo|Referência completa]]; [[06_Referencias/referencias#LongMemEval|LongMemEval, mais próximo da motivação de atualização de conhecimento]].

---

## 7. Xu et al. — Chain-of-Memory

**Prioridade: complementar**

Uso:
- contextualizar a organização e o uso de memória em agentes;
- discutir decisões de construção do sistema, sem tratá-las como variáveis experimentais deste TCC.

O trabalho organiza construção e uso de fragmentos recuperados; não avalia diretamente a reescrita GU-json. [[06_Referencias/referencias#Xu et al. — Chain-of-Memory|Referência completa]].

---

## 8. PRISM — atualização de memória tipada

**Prioridade: alta**

Jayalath et al., EMNLP 2025. O título publicado é *PRISM: Efficient Long-Range Reasoning With Short-Context LLMs*; substitui o título do preprint de 2024.

Mantém memória hierárquica tipada com operações de caminho/valor aplicadas e validadas programaticamente. É precedente próximo de atualização persistente e alternativa conceitual ao GU, não comparação controlada contra GU-json. [[06_Referencias/referencias#PRISM|PRISM]]; [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al.]].

## 9. Difusão: fundamento e contrapontos

**Prioridade: alta para caracterização, sem ampliar o protocolo**

Block Diffusion fundamenta especificamente BD3LM, mas a origem do candidato Qwen3-0.6B ainda depende do checkpoint exato. Lu et al. (2026) encontram dificuldades em chamadas de ferramentas e resultados competitivos em memória textual com modelos maiores, sem testar GU-json compacto. Mündler et al. (2025) mostram mitigação de falhas sintáticas com restrições, excluídas deste experimento. [[06_Referencias/referencias#Block Diffusion|Arriola et al.]]; [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al.]]; [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al.]].
