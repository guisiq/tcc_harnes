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
- [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]] — JSON para sumarização incremental, fundamento direto de GU.
- [[06_Referencias/referencias#PRISM|PRISM, 2025]] — memória tipada com revisões programáticas.
- [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al., 2025/2026]] — memória por agente, não necessariamente JSON em todas as variantes.
- [[06_Referencias/referencias#Zeng et al. — Structural Memory|Zeng et al., 2024]] — contexto sobre estruturas e recuperação, não GU-json.

## Eixo 2 — atualização incremental

Pergunta:
**Como atualizar a representação sem reler todo o histórico?**

Trabalhos:
- [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al.]] — Generate-Update, Generate-Merge, Chain-of-Key.
- [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al.]] — atualização contextual pelo LLM.
- [[06_Referencias/referencias#PRISM|PRISM]] — operações validadas de caminho/valor, diferentes da reescrita integral.

## Eixo 3 — avaliação de memória agente

Pergunta:
**Quais competências devem ser medidas?**

Trabalhos:
- [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE, 2025]] — sumarização por etapas preservando perspectivas conflitantes; State F1 local exige adaptação.
- [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]] — quatro competências; FactConsolidation define substituição temporal explícita.
- [[06_Referencias/referencias#LongMemEval|LongMemEval, 2025]] — atualização de conhecimento e raciocínio temporal, apenas fundamentação.
- [[06_Referencias/referencias#Maharana et al. — LoCoMo|LoCoMo, 2024]] — contexto sobre diálogo longo; fora da coleta.


## Eixo 4 — construção de sistemas de memória
Pergunta:
**Como são organizados os componentes de construção e uso da memória?**

Trabalhos:
- [[06_Referencias/referencias#Xu et al. — Chain-of-Memory|Chain-of-Memory, 2026]] — construção e raciocínio sobre fragmentos recuperados, não avaliação direta de GU-json.

## Eixo 5 — structured generation

Pergunta:
**Como garantir estrutura JSON correta?**

Trabalhos:
- [[06_Referencias/referencias#JSONSchemaBench|JSONSchemaBench, 2025]] — conformidade com JSON Schema, distinta de fidelidade semântica.
- [[06_Referencias/referencias#Grammar-Constrained Decoding|Geng et al., 2023]] — gramáticas formais.
- [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al., 2025]] — mitigação de falhas sintáticas em difusão, com mecanismo excluído do protocolo principal.

## Eixo 6 — arquiteturas gerativas

Pergunta:
**Como diferentes paradigmas geram transformações texto→estrutura?**

Trabalhos:
- [[06_Referencias/referencias#Qwen3 Technical Report|Qwen3, 2025]] — representante autoregressivo.
- [[06_Referencias/referencias#T5Gemma|T5Gemma, 2025]] — representante encoder-decoder, série B-B T5-compatible.
- [[06_Referencias/referencias#Block Diffusion|Block Diffusion, 2025]] — fundamento específico de BD3LM, sem comprovar o checkpoint Qwen pretendido.
- [[06_Referencias/referencias#Diffusion adaptation|Gong et al., 2024/2025]] e [[06_Referencias/referencias#Scaling masked diffusion|Nie et al., 2024/2025]] — fundamentos gerais.
- [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al., 2026]] — contraponto: dificuldades em chamadas de ferramentas, resultados competitivos em memória textual de modelos maiores; não avalia GU-json compacto.

Este mapa prioriza a pertinência ao argumento, não apenas a data. A auditoria de 2026-11-06 não certifica novidade global nem transforma fontes complementares em condições experimentais.

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
