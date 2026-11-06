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

Essa representação mínima é uma escolha de controle do TCC, cuja adequação aos estados acumulados do SUMIE precisa ser validada. As anotações originais são por parágrafo e podem conter múltiplas perspectivas sobre um atributo; não reduzir opiniões conflitantes automaticamente a um único valor vencedor. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE, 2025]].

Esse é o único schema usado no experimento, tanto no SUMIE quanto na amostra FactConsolidation-SH. Os campos são convertidos para pares atributo-valor dentro de `state`; não serão adicionados campos específicos por dataset.

## Critério de escolha

O schema mínimo deve ser **idêntico para todos os writers e exemplos**, evitando que a complexidade ou adaptação do schema se torne outra variável.

Hwang oferece o precedente direto de GU-json; Yuen e PRISM mostram outras escolhas de representação e atualização, sem provar que este schema mínimo seja superior. A política de canonicalização e representação das perspectivas deve ser documentada sem alterar o schema entre writers. [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]]; [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al., 2025/2026]]; [[06_Referencias/referencias#PRISM|PRISM, 2025]].

## Limite de memória

Configuração principal sugerida:

```text
max checkpoint output = 300 tokens
```

O limite de 300 tokens é fixo em todas as condições, evitando transformar orçamento em uma segunda variável independente. Hwang et al. estudam memória limitada no SUMIE com limites de 200 e 300 tokens; o protocolo deste TCC adota um único teto de saída de 300 tokens, inspirado nesse cenário, mas sem alegar replicação idêntica da contagem de tokens do artigo.

Fonte: [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]]. Antes da coleta, verificar se os estados de referência e a política de representação cabem nesse teto; não penalizar o writer como se retenção integral impossível fosse necessariamente erro semântico.

## Regras semânticas de atualização

1. Preservar fatos ainda válidos.
2. Substituir fatos apenas quando houver invalidação temporal explícita; preservar opiniões divergentes válidas no SUMIE.
3. Não inventar valores ausentes.
4. Não duplicar a mesma informação em campos diferentes.
5. Retornar somente JSON.

As duas políticas vêm de tarefas distintas: [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]] e [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|FactConsolidation/MemoryAgentBench]].
