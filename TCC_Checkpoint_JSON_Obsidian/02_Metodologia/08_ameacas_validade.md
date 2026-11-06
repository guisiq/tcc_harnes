---
title: "Ameaças à validade"
aliases:
  - "08 ameacas validade"
tags:
  - tcc
  - metodologia
status: draft
---

# Ameaças à validade

## Validade interna

### Modelos não são perfeitamente pareados
Qwen3, T5Gemma e Qwen-diffusion possuem treinamentos e tokenizadores diferentes.

Mitigação:
- aproximar escala;
- usar instruction-tuned quando possível;
- manter todas as demais condições fixas;
- evitar linguagem causal absoluta.

### Decoding diferente
Diffusion não possui exatamente o mesmo processo de geração que AR/seq2seq.

Mitigação:
- fixar budgets equivalentes;
- documentar parâmetros;
- evitar constrained decoding no experimento principal;

### Schema favorece um paradigma
Um JSON extremamente linear pode favorecer geração AR; um schema editável globalmente pode favorecer diffusion.

Mitigação:
- schema simples;
- justificar pelo problema de estado;
- mesma estrutura para todos.

---

## Validade de construção

### JSON válido não significa memória correta
Mitigação:
- usar F1, preservation, update, supersession e stale facts.

---

## Validade externa

SUMIE é sintético e representa sumarização incremental de entidades. A amostra de FactConsolidation-SH cobre apenas um contraste de supersession.

Mitigação:
- declarar que os resultados não demonstram generalização para diálogo longo, tarefas multi-hop ou todos os tipos de memória.

---

## Validade de conclusão

### Uma única execução determinística
Se geração for determinística, repetições idênticas não acrescentam variância.

Mitigação:
- usar ampla quantidade de amostras;
- bootstrap por amostras para intervalos de confiança;
- quando houver estocasticidade inevitável, rodar seeds adicionais em subconjunto.

### Muitas métricas
Risco de cherry-picking.

Mitigação:
- declarar métricas primárias antes:
  1. State F1
  2. Preservation Accuracy
  3. Supersession Accuracy

---

## Validade de implementação

- testes unitários para parser;
- validação automática do schema;
- armazenar output bruto antes de qualquer reparo;
- não corrigir JSON silenciosamente;
- diferenciar `raw_valid_json` de `repaired_json`.
