---
title: "Visão geral do projeto"
aliases:
  - "01 visao geral"
tags:
  - tcc
  - projeto
status: draft
---

# Visão geral do projeto

## Tema provisório

**Avaliação de paradigmas de geração para atualização incremental de checkpoints JSON em agentes baseados em SLMs locais.**

## Formulação curta

O trabalho compara modelos compactos de três paradigmas — **decoder-only autoregressivo, encoder-decoder e diffusion language model** — como writers de memória usando uma única técnica fixa: **Generate-Update em JSON (GU-json)**.

O cenário principal é a sumarização incremental de entidades do SUMIE, com schema e limite de memória fixos. Uma amostra de FactConsolidation-SH será usada apenas como contraste para substituição de informação.

SUMIE preserva perspectivas conflitantes; FactConsolidation-SH define invalidação temporal explícita. Essa diferença orienta a adaptação dos estados esperados e impede interpretar todo conflito como supersession. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE, 2025]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench, 2025/2026]].

## Problema

Agentes baseados em modelos de linguagem que executam tarefas multi-etapas precisam manter estado ao longo do tempo. Uma estratégia é condensar interações anteriores em uma representação persistente estruturada.

O problema experimental é que cada reescrita do estado pode:

- perder fatos ainda válidos;
- preservar fatos obsoletos;
- atualizar campos incorretamente;
- inventar valores;
- corromper partes imutáveis do estado;
- produzir checkpoints maiores do que o limite definido para a memória.

A literatura apresenta resultados favoráveis a representações estruturadas em configurações específicas, não uma superioridade universal de GU ou de schema fixo. Hwang fundamenta GU-json; PRISM usa revisões programáticas; Yuen inclui variantes que não exigem JSON. A busca selecionada não responde diretamente à comparação dos **representantes compactos escolhidos** no protocolo deste TCC, sem comprovar ausência global de estudos. [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]]; [[06_Referencias/referencias#PRISM|PRISM, 2025]]; [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al., 2025/2026]].

## Objeto experimental

A função central é:

```text
checkpoint anterior + nova observação + schema
                    ↓
              memory writer
                    ↓
            checkpoint atualizado
```

Formalmente:

\[
M_t = G(M_{t-1}, O_t, S)
\]

onde:

- `M_(t-1)` = checkpoint anterior;
- `O_t` = nova observação;
- `S` = schema fixo;
- `G` = memory writer;
- `M_t` = novo checkpoint.

## Escopo

O estudo **não** pretende comparar:

- RAG vs. memória estruturada;
- vários schemas;
- vários algoritmos de memória;
- avaliação de tarefas de agentes downstream;
- fine-tuning extenso;
- vector databases;
- diferentes retrieval strategies.

Esses elementos ficariam fora do núcleo para reduzir confundimento experimental.

## Contribuição pretendida

A contribuição é uma avaliação focal da qualidade e estabilidade de modelos compactos como writers GU-json no SUMIE. Uma amostra de FactConsolidation-SH oferece um contraste delimitado para supersession. O estudo não pretende determinar qual método de escrita é universalmente superior.

Veja também:
- [[01_Projeto/02_perguntas_hipoteses|Perguntas e hipóteses]]
- [[01_Projeto/03_justificativa_lacuna|Justificativa e lacuna]]
- [[02_Metodologia/06_plano_experimental|Plano experimental]]
