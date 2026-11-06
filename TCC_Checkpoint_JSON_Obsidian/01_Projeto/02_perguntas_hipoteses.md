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

**RQ3.** Quais diferenças entre writers aparecem nas operações de adicionar, atualizar, preservar e substituir informação no SUMIE?

**RQ4.** Na subamostra de contraste FactConsolidation-SH, focada em supersession, quais padrões observados no SUMIE se mantêm?

## Evidência prévia e hipóteses

Hwang et al. relatam vantagem de `GU_json` sobre `GU_text` sob memória limitada em SUMIE e BooookScore; `CoK_json` obtém resultados superiores às baselines comparadas. Isso fundamenta a escolha de GU-json como método fixo, sem tratá-lo como método universalmente superior. [[06_Referencias/referencias|Hwang et al.]]

> As hipóteses abaixo são proposições sobre esta comparação entre writers compactos, não resultados antecipados.

### H1 — perfis de erro por writer
Os representantes dos três paradigmas podem diferir na preservação de estado antigo e na incorporação de informação nova.

### H2 — supersession
As diferenças entre writers podem ser mais visíveis quando a informação nova substitui uma informação anterior do que em simples adições.

## Operações que devem ser rotuladas

```text
ADD        informação nova
UPDATE     valor existente é modificado
PRESERVE   valor existente deve permanecer
SUPERSEDE  valor novo invalida valor antigo
```

Esses rótulos permitem analisar os mesmos resultados por tipo de operação sem multiplicar o número de execuções.
