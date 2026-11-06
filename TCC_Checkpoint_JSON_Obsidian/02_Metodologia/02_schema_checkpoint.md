---
title: "Schema do checkpoint"
aliases:
  - "02 schema checkpoint"
tags:
  - tcc
  - metodologia
status: draft
---

# Schema do checkpoint

## Princípio

O schema deve ser:

- fixo;
- simples;
- pequeno;
- suficiente para representar estado operacional;
- independente do dataset, quando possível;
- fácil de comparar automaticamente.

## Schema fixo do experimento

```json
{
  "state": {
    "key": "value"
  }
}
```

Essa versão é excelente para SUMIE e para avaliações de precisão/recall por pares atributo-valor.

Esse é o único schema usado no experimento, tanto no SUMIE quanto na amostra FactConsolidation-SH. Os campos são convertidos para pares atributo-valor dentro de `state`; não serão adicionados campos específicos por dataset.

## Critério de escolha

O schema mínimo deve ser **idêntico para todos os writers e exemplos**, evitando que a complexidade ou adaptação do schema se torne outra variável.

## Limite de memória

Configuração principal sugerida:

```text
max checkpoint output = 300 tokens
```

O limite de 300 tokens é fixo em todas as condições, evitando transformar orçamento em uma segunda variável independente. Hwang et al. estudam memória limitada no SUMIE com limites de 200 e 300 tokens; o protocolo deste TCC adota um único teto de saída de 300 tokens, inspirado nesse cenário, mas sem alegar replicação idêntica da contagem de tokens do artigo.

## Regras semânticas de atualização

1. Preservar fatos ainda válidos.
2. Substituir fatos contraditos por informação mais recente.
3. Não inventar valores ausentes.
4. Não duplicar a mesma informação em campos diferentes.
5. Retornar somente JSON.
