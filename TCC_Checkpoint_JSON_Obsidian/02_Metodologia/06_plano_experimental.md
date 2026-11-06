---
title: "Plano experimental"
aliases:
  - "06 plano experimental"
tags:
  - tcc
  - metodologia
status: draft
---

# Plano experimental

## Variável independente principal

`writer_architecture`, com três níveis:

```text
AR_DECODER_ONLY
ENCODER_DECODER
DIFFUSION
```

O método GU-json, schema, prompt-base e orçamento de saída (300 tokens) são fixos. O experimento avalia a qualidade do checkpoint produzido; não inclui avaliação downstream nem comparação de métodos de escrita.

## Variáveis controladas

- mesmo dataset e ordem das entradas dentro de cada fase;
- mesmo schema e método GU-json;
- mesmo prompt-base;
- mesmo limite de saída de 300 tokens e limite de contexto;
- mesma política de determinismo;
- mesmos estados anteriores, observações e referências esperadas para os três writers.

## Fase 0 — sanity check

Usar 10–20 transições construídas manualmente para validar parser, schema, prompt e formato de saída. Não incluir esses resultados na análise principal.

## Fase 1 — piloto SUMIE

Usar aproximadamente 25 entidades para confirmar a adaptação do dataset, o cálculo das métricas e a execução correta dos três writers. Corrigir problemas de implementação antes da coleta confirmatória.

## Fase 2 — experimento principal no SUMIE

Executar os três writers nas mesmas sequências de sumarização incremental de entidades. SUMIE é o cenário principal por corresponder diretamente ao domínio em que Hwang et al. avaliam GU-json sob memória limitada.

Registrar por transição:

```json
{
  "sample_id": "...",
  "turn": 4,
  "writer": "...",
  "previous_state": {},
  "observation": "...",
  "prediction": {},
  "expected_state": {}
}
```

## Fase 3 — contraste de supersession

Usar uma amostra previamente delimitada de FactConsolidation-SH, contendo casos de supersession. Fixar e documentar os critérios e o tamanho da amostra antes de executar os writers. Tratar os resultados como contraste exploratório, não como avaliação geral de memória agente.

## Análises

1. Qualidade agregada por writer no SUMIE.
2. Qualidade por turno para observar como os perfis dos writers variam ao longo da sequência.
3. Qualidade por operação no SUMIE: ADD / UPDATE / PRESERVE / SUPERSEDE.
4. Análise separada da amostra FactConsolidation-SH para supersession.

## Repetibilidade

- registrar seed e versões de bibliotecas;
- registrar commit do harness;
- salvar prompts e outputs crus;
- usar os mesmos exemplos para todos os writers;
- não misturar resultados do piloto com a análise confirmatória.
