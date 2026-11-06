---
title: "Justificativa e lacuna de pesquisa"
aliases:
  - "03 justificativa lacuna"
tags:
  - tcc
  - projeto
status: draft
---

# Justificativa e lacuna de pesquisa

## Evidência de que JSON estruturado é relevante

Hwang et al. comparam GO, GU e GM em texto e JSON no SUMIE e no BooookScore. Sob limite de memória, `GU_json` supera `GU_text`; o artigo também introduz `CoK_json`, que atualiza caminhos da estrutura e obtém resultados superiores às baselines comparadas. Os escritores avaliados são Gemini Ultra e Gemini Pro, portanto a evidência direta não é sobre modelos compactos.

**Leitura para este TCC:** GU-json é um método estabelecido para sumarização incremental estruturada sob memória limitada, não o método universalmente superior. Ele será fixado para isolar a comparação entre modelos escritores.

Referência: [[06_Referencias/referencias#hwang-structured|Hwang et al. — Enhancing Incremental Summarization with Structured Representations]]

## Evidência de que JSON é usado dentro de agentes

Yuen et al. usam memória JSON atualizada continuamente por LLMs em agentes e comparam templates manuais, genéricos e gerados por LLM.

**Leitura para este TCC:** existe precedente de checkpoint estruturado em um agente real, mas o foco daquele estudo é template/memória multiagente, não uma comparação controlada entre paradigmas de geração compactos.

Referência: [[06_Referencias/referencias#yuen-intrinsic|Yuen et al. — Intrinsic Memory Agents]]

## Estrutura de memória não é a mesma coisa que método de escrita

Zeng et al. comparam chunks, knowledge triples, atomic facts, summaries e memória mista, além de estratégias de retrieval, em quatro tarefas e seis datasets. Relatam vantagens distintas por tarefa: chunks/summaries em contexto longo, triples/atomic facts em raciocínio relacional e precisão, e mixed memory como opção mais equilibrada.

**Leitura para este TCC:** este é provavelmente o artigo lembrado sobre adequar características de memória a cenários, mas não estuda GU-json nem algoritmos de escrita incremental. Ele orienta o recorte por tarefa, não determina qual modelo writer será melhor.

Referência: [[06_Referencias/referencias#zeng-structural|Zeng et al. — On the Structural Memory of LLM Agents]]

## A avaliação incremental é importante

MemoryAgentBench argumenta que agentes de memória recebem informações incrementalmente e propõe competências que incluem `Selective Forgetting`.

**Leitura para este TCC:** medir apenas JSON válido é insuficiente. O protocolo deve incluir atualização, preservação e substituição de informação ao longo do tempo.

Referência: [[06_Referencias/referencias#hu-memoryagentbench|Hu et al. — MemoryAgentBench]]

## Lacuna operacional proposta

A lacuna pode ser formulada de maneira cautelosa:

> A lacuna proposta é comparar representantes compactos de diferentes paradigmas como writers de GU-json no cenário diretamente relacionado do SUMIE, com uma amostra delimitada de FactConsolidation-SH para observar supersession fora do cenário de sumarização de entidades.

### Importante

O estudo **não pode atribuir causalidade puramente à arquitetura** porque os modelos diferem em:

- dados de pré-treinamento;
- objetivos de treinamento;
- instruction tuning;
- tokenizador;
- número exato de parâmetros.

A formulação correta é:

> "entre representantes compactos dos paradigmas avaliados..."

e não:

> "encoder-decoder é intrinsecamente melhor que decoder-only".

## Por que este recorte é defensável

1. Mantém o método de memória constante.
2. Mantém o schema constante.
3. Usa SUMIE, o cenário diretamente alinhado à avaliação de GU-json em sumarização incremental de entidades.
4. Mantém um único orçamento de memória para não introduzir outra variável.
5. Usa apenas uma amostra de FactConsolidation-SH como contraste para supersession.
6. Permite avaliar fidelidade contra estados esperados estruturados sem LLM-as-judge nas métricas centrais.
