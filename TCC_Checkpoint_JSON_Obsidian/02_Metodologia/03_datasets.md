---
title: "Datasets"
aliases:
  - "03 datasets"
tags:
  - tcc
  - metodologia
status: draft
---

# Datasets

## 1. SUMIE — principal

**SUMIE: A Synthetic Benchmark for Incremental Entity Summarization**

Objetivo do benchmark: testar atualização incremental de resumos de entidades.

Características úteis para este TCC:

- informações chegam em etapas;
- há atributos e valores esperados;
- permite medir precisão, recall e F1;
- contém repetição, informação nova, conflito e distração;
- é o cenário diretamente estudado por Hwang et al. para sumarização incremental com `GU_json` sob limite de memória.

**Foco do experimento:** avaliar os três writers no SUMIE com a mesma configuração GU-JSON e um orçamento fixo. A motivação é a vantagem relatada de JSON estruturado sobre GU-text em condições de memória limitada, não a afirmação de que GU-json seja superior a todos os métodos.

Link:
https://aclanthology.org/2025.coling-main.721/

Referências complementares: [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE, COLING 2025]] descreve os dados; [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., Findings EMNLP 2024]] fundamenta o protocolo GU-json.

O prompt UPDATE publicado preserva atributos/valores existentes e integra opiniões conflitantes. Não aplicar a regra de que o valor mais recente sempre vence: conflito de opinião não implica `SUPERSEDE`.

### Uso proposto

Cada etapa será convertida em:

```json
{
  "previous_state": {},
  "observation": "...",
  "expected_state": {}
}
```

O dataset público fornece anotações por parágrafo, não checkpoints acumulados canônicos nem rótulos prontos de ADD/UPDATE/PRESERVE/SUPERSEDE. A construção de `expected_state`, a representação de múltiplas perspectivas e a canonicalização devem ser documentadas e validadas antes da coleta. Verificar a compatibilidade dos estados de referência com o teto fixo de 300 tokens, sem introduzir ablação de orçamento.

A avaliação original usa correspondência exata e avaliação semântica de evidências por LLM. As métricas determinísticas de estado deste projeto são uma adaptação, não números diretamente comparáveis ao F1 publicado. [[02_Metodologia/05_metricas|Métricas]]

Dados: https://github.com/google-deepmind/sumie. O repositório é identificado como Apache-2.0; registrar revisão e licença do artefato utilizado.

### Métricas principais

- State Precision
- State Recall
- State F1
- Preservation Accuracy
- Update Accuracy
- Hallucination Rate

---

## Contraste exploratório — amostra FactConsolidation-SH

Parte do **MemoryAgentBench**.

Uso no TCC: conjunto de contraste, limitado a uma amostra de transições que envolvam substituição de informação (*supersession*). Não será executado como segundo benchmark completo nem usado para afirmar generalização ampla.

Este conjunto não é o cenário em que Hwang et al. demonstraram a vantagem de GU-json; serve apenas para verificar se os perfis observados no SUMIE aparecem também em casos de substituição de fatos.

### Razão de escolha

O contraste verifica se os padrões observados no SUMIE também aparecem numa condição diferente, que enfatiza:

- conflito;
- atualização de conhecimento;
- substituição de fatos obsoletos;
- retenção seletiva.

### Uso proposto

Selecionar e documentar uma amostra de casos relevantes para `SUPERSEDE` antes da coleta confirmatória. O tamanho da amostra será fixado após verificar a distribuição das operações e antes de comparar os writers.

FactConsolidation usa ordem temporal explícita para invalidar o fato antigo. O benchmark original avalia respostas finais; construir estados esperados e rótulos de transição é uma adaptação local. A diferença entre SUMIE e este contraste não isola causalmente a dificuldade de supersession. [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]]; [[06_Referencias/referencias#LongMemEval|LongMemEval, motivação complementar para atualização de conhecimento]].

Repositório/dataset:
https://huggingface.co/datasets/ai-hyz/MemoryAgentBench

Há divergência entre a licença MIT indicada no cartão do dataset e CC BY 4.0 para artefatos no artigo v4. Confirmar licença da revisão utilizada e condições dos dados de terceiros antes da coleta. O código do repositório é MIT, o que não resolve automaticamente a licença dos dados.

---


## Fora do escopo

FactConsolidation-MH-6K, LoCoMo, LongMemEval e BooookScore não serão incluídos na coleta. BooookScore é o segundo dataset do estudo de Hwang, mas não é necessário para responder à comparação focal no SUMIE; os demais ampliariam o domínio e as tarefas sem testar diretamente a pergunta principal.
