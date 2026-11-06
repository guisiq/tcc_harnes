---
title: "Perguntas de pesquisa e hipóteses"
aliases:
  - "02 perguntas hipoteses"
tags:
  - tcc
  - projeto
status: draft
---

# Perguntas de pesquisa e hipóteses

## Pergunta principal

**RQ1. Como representantes compactos autoregressivos decoder-only, encoder-decoder e diffusion diferem na qualidade das atualizações GU-json no SUMIE, com schema e limite de 300 tokens fixos?**

## Perguntas secundárias

**RQ2.** Como as diferenças de fidelidade entre os writers variam ao longo da sequência de atualizações do SUMIE?

**RQ3.** Quais diferenças entre writers aparecem na adição, integração e preservação de informação no SUMIE, respeitando sua política de manter perspectivas conflitantes?

**RQ4.** Na subamostra de contraste FactConsolidation-SH, focada em supersession, quais padrões observados no SUMIE se mantêm?

## Evidência prévia e hipóteses

Hwang et al. relatam vantagem de `GU_json` sobre `GU_text` sob memória limitada em SUMIE e BooookScore; `CoK_json` obtém resultados superiores às baselines comparadas. Isso fundamenta GU-json como método fixo, não universalmente superior. O artigo do SUMIE relata perfis distintos de precisão/recall entre modelos, mas não testa os três representantes deste projeto. [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]]; [[06_Referencias/referencias#Hwang et al. — SUMIE|Hwang et al., 2025]]

> As hipóteses abaixo são proposições sobre esta comparação entre writers compactos, não resultados antecipados.

### H1 — perfis de erro por writer
Sob GU-json, schema e orçamento fixos, os modelos selecionados apresentam diferenças mensuráveis na preservação de estado antigo e na incorporação de informação nova. Não se prevê uma ordenação dos modelos nem se atribuem diferenças somente à arquitetura.

Os perfis observados no SUMIE e a variação por tarefa encontrada por Lu et al. motivam testar essa hipótese, sem demonstrá-la previamente para modelos de 0,6B ou memória JSON. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al., 2026]]

### H2 — supersession (exploratória)
As diferenças entre writers podem ser mais visíveis quando a informação nova substitui uma informação anterior do que em simples adições.

MemoryAgentBench e LongMemEval motivam a análise de atualização de conhecimento, mas não demonstram esta hipótese para os writers escolhidos. A comparação SUMIE/FactConsolidation-SH mistura operação e dataset; sem casos comparáveis dentro do mesmo cenário, a H2 permanece exploratória, não um teste isolado do efeito de supersession. [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]]; [[06_Referencias/referencias#LongMemEval|LongMemEval]]

## Operações que devem ser rotuladas

```text
ADD        informação nova
UPDATE     valor existente é modificado
PRESERVE   valor existente deve permanecer
SUPERSEDE  valor novo invalida valor antigo
```

Esses rótulos permitem analisar os mesmos resultados por tipo de operação sem multiplicar o número de execuções.

No SUMIE, UPDATE integra nova informação sem invalidar automaticamente valores ou opiniões anteriores. SUPERSEDE exige regra explícita de invalidação, presente no contraste FactConsolidation-SH; não deve ser inferido apenas de mudança de sentimento ou valor entre parágrafos. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]]
