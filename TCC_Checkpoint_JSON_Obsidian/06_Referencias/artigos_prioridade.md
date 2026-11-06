---
title: "Lista priorizada de artigos"
aliases:
  - "artigos prioridade"
tags:
  - tcc
  - referencias
status: draft
---

# Lista priorizada de artigos

## Prioridade A — ler e fichar integralmente

| Artigo | Motivo |
|---|---|
| [[06_Referencias/referencias#Hwang et al. — structured incremental summarization\|Hwang, Findings EMNLP 2024]] | fundamento direto de GU-JSON, sem alegar superioridade sobre CoK |
| [[06_Referencias/referencias#Hwang et al. — SUMIE\|SUMIE, COLING 2025]] | dataset principal; preservar perspectivas e adaptar avaliação |
| [[06_Referencias/referencias#Hu et al. — MemoryAgentBench\|MemoryAgentBench, 2025/2026]] | contraste temporal de supersession; avaliação original por respostas |
| [[06_Referencias/referencias#PRISM\|PRISM, EMNLP 2025]] | memória persistente por revisões programáticas, alternativa conceitual a GU |
| [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents\|Intrinsic Memory Agents, revisão 2026]] | atualização contextual; nem toda variante exige JSON |
| [[06_Referencias/referencias#Qwen3 Technical Report\|Qwen3, 2025]] | caracterização do writer autoregressivo |
| [[06_Referencias/referencias#T5Gemma\|T5Gemma, 2025]] | caracterização do writer encoder-decoder |
| [[06_Referencias/referencias#Block Diffusion\|Block Diffusion, 2025]] + relatório do checkpoint exato | fundamento de BD3LM; origem do candidato Qwen ainda pendente |

## Prioridade B — trabalhos relacionados fortes

| Artigo | Motivo |
|---|---|
| On the Structural Memory of LLM Agents | taxonomia empírica de estruturas |
| Chain-of-Memory | organização da construção e uso de memória |
| LoCoMo | literatura sobre memória conversacional longa; fora dos datasets experimentais |
| [[06_Referencias/referencias#LongMemEval\|LongMemEval, 2025]] | atualização de conhecimento; apenas fundamentação |
| [[06_Referencias/referencias#Diffusion em workflows de agentes\|Lu et al., 2026]] | contraponto: chamadas de ferramentas versus memória textual, não GU-json compacto |
| Scaling Diffusion Language Models via Adaptation from AR Models | base conceitual diffusion |
| Scaling up Masked Diffusion Models on Text | scaling e propriedades MDM |

## Prioridade C — structured output

| Artigo | Motivo |
|---|---|
| JSONSchemaBench | mostra que validade JSON/constrained decoding já é campo próprio |
| Grammar-Constrained Decoding | formalização de constraints |
| Constrained Decoding of Diffusion LLMs | relação direta diffusion + estrutura |
| Agents of Diffusion | structured data com diffusion |

As fontes deste grupo não demonstram superioridade ou inferioridade inerente de um paradigma no GU-json. Distinguir prompt-only, constrained decoding e sistemas multiagente. [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al., 2025]]; [[06_Referencias/referencias#Agents of Diffusion|Khanal et al., 2026]].

## Prioridade D — metodologia de revisão

| Artigo | Motivo |
|---|---|
| Petersen 2008 | systematic mapping |
| Petersen 2015 | atualização das guidelines |
| Wohlin 2014 | snowballing |
| Kitchenham 2010 | contexto de SLR/tertiary study |

Priorizar as diretrizes atualizadas de Petersen 2015 junto da origem de 2008; Kitchenham 2010 é estudo terciário, não manual procedural completo. Datas e links auditados estão em [[06_Referencias/referencias|Referências]]. As prioridades não indicam leituras já concluídas.

## Ficha padrão para cada artigo

```text
Título:
Ano:
Venue:
Versão consultada e data:
Publicação confirmada nos anais ou informada pelos autores:
Pergunta:
Método:
Modelos:
Dataset:
Memória:
Atualização:
Métricas:
Principais resultados:
Limitações:
Relação com meu TCC:
Citação que quero usar:
Afirmação que a fonte não sustenta:
Contraponto ou fonte complementar:
Código:
Dataset:
Licença e revisão dos artefatos:
Nível da leitura (integral, seção metodológica ou resumo/metadados):
```
