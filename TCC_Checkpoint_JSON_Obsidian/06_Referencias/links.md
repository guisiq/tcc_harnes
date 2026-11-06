---
title: "Links úteis"
aliases:
  - "links"
tags:
  - tcc
  - referencias
status: draft
---

# Links úteis

## Modelos

### Qwen3-0.6B
https://huggingface.co/Qwen/Qwen3-0.6B

### Qwen3 Technical Report (2025)
https://arxiv.org/abs/2505.09388

### T5Gemma B-B PrefixLM-IT
https://huggingface.co/google/t5gemma-b-b-prefixlm-it

### T5Gemma report
https://arxiv.org/abs/2504.06225

### BD3LM: fundamento, não checkpoint Qwen confirmado
https://arxiv.org/abs/2503.09573

https://github.com/kuleshov-group/bd3lms

## Datasets

### SUMIE paper
https://aclanthology.org/2025.coling-main.721/

### SUMIE dados
https://github.com/google-deepmind/sumie

### MemoryAgentBench
https://huggingface.co/datasets/ai-hyz/MemoryAgentBench

https://arxiv.org/abs/2507.05257

https://github.com/HUST-AI-HYZ/MemoryAgentBench

### LongMemEval (somente fundamentação, fora da coleta)
https://arxiv.org/abs/2410.10813

https://github.com/xiaowu0162/LongMemEval

### LoCoMo
https://snap-research.github.io/locomo

## Memória

### Hwang: GU-json (Findings EMNLP 2024)
https://aclanthology.org/2024.findings-emnlp.220/

### PRISM (EMNLP 2025, título publicado)
https://aclanthology.org/2025.emnlp-main.517/

### Intrinsic Memory Agents (preprint 2025, revisão 2026)
https://arxiv.org/abs/2508.08997

### StructuralMemory code
https://github.com/zengrh3/StructuralMemory

### Chain-of-Memory code
https://github.com/Xiucheng-Xu/CoM

https://arxiv.org/abs/2601.14287

## Structured generation

### JSONSchemaBench
https://arxiv.org/abs/2501.10868

### Grammar-Constrained Decoding
https://aclanthology.org/2023.emnlp-main.674/

### Diffusion constrained decoding
https://arxiv.org/abs/2508.10111

### Agents of Diffusion
https://arxiv.org/abs/2601.07152

## Diffusion language models

### AR to diffusion adaptation
https://arxiv.org/abs/2410.17891

### Scaling masked diffusion
https://arxiv.org/abs/2410.18514

### Contraponto: difusão em workflows de agentes (2026)
https://arxiv.org/abs/2601.12979

Estuda ferramentas e memória textual, não checkpoints JSON compactos. [[06_Referencias/referencias#Diffusion em workflows de agentes|Limites de uso da evidência]].

## Metodologia

### Petersen 2008 DOI
https://doi.org/10.14236/ewic/ease2008.8

### Petersen 2015 DOI
https://doi.org/10.1016/j.infsof.2015.03.007

### Wohlin 2014 DOI
https://doi.org/10.1145/2601248.2601268

### Kitchenham 2010 DOI
https://doi.org/10.1016/j.infsof.2010.03.006

## Observação

Auditoria de 2026-11-06: texto público não implica pesos ou dados sem restrições. T5Gemma exige aceite da licença; MemoryAgentBench tem divergência entre licença do cartão de dados e artigo v4. Os clássicos metodológicos tiveram metadados conferidos, não acesso integral gratuito confirmado. [[06_Referencias/referencias|Bibliografia e ressalvas]].

Antes de congelar o experimento, salvar localmente:

- URL;
- commit/revision do modelo;
- hash/config;
- licença;
- versão do Transformers/PyTorch;
- data de acesso.
