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

### Uso proposto

Cada etapa será convertida em:

```json
{
  "previous_state": {},
  "observation": "...",
  "expected_state": {}
}
```

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

Repositório/dataset:
https://huggingface.co/datasets/ai-hyz/MemoryAgentBench

---


## Fora do escopo

FactConsolidation-MH-6K, LoCoMo e BooookScore não serão incluídos na coleta. BooookScore é o segundo dataset do estudo de Hwang, mas não é necessário para responder à comparação focal no SUMIE; os demais ampliariam o domínio e as tarefas sem testar diretamente a pergunta principal.
