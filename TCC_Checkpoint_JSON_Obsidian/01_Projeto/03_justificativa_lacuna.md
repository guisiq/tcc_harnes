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

Referências: [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]]; [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE, COLING 2025]].

## Evidência de que JSON é usado dentro de agentes

Yuen et al. atualizam memória contextual a partir da memória anterior e de novas saídas dos agentes, comparando templates manuais, genéricos e gerados por LLM. Na revisão de janeiro de 2026, a variante genérica não exige JSON; templates genéricos/gerados superam os manuais em vários testes.

PRISM (EMNLP 2025) também mantém memória estruturada persistente, mas aplica operações de caminho/valor programaticamente, em vez de reescrever o JSON inteiro.

**Leitura para este TCC:** há precedentes próximos de atualização de memória, não prova de superioridade do schema fixo ou de GU. Fixá-los é um controle experimental; não será acrescentada uma comparação de templates ou métodos.

Referências: [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al., 2025/2026]]; [[06_Referencias/referencias#PRISM|Jayalath et al., 2025]].

## Estrutura de memória não é a mesma coisa que método de escrita

Zeng et al. comparam chunks, knowledge triples, atomic facts, summaries e memória mista, além de estratégias de retrieval, em quatro tarefas e seis datasets. Relatam vantagens distintas por tarefa: chunks/summaries em contexto longo, triples/atomic facts em raciocínio relacional e precisão, e mixed memory como opção mais equilibrada.

**Leitura para este TCC:** o artigo fornece contexto sobre representação/recuperação, não estuda GU-json nem demonstra preservação em checkpoints reescritos. Para atualização persistente, os fundamentos mais próximos são Hwang, PRISM e Yuen; não foi identificado qual era o artigo originalmente lembrado.

Referência contextual: [[06_Referencias/referencias#Zeng et al. — Structural Memory|Zeng et al., 2024]].

## A avaliação incremental é importante

MemoryAgentBench argumenta que agentes de memória recebem informações incrementalmente e propõe competências que incluem `Selective Forgetting`.

LongMemEval inclui atualização de conhecimento e raciocínio temporal. Ambos avaliam respostas, não fidelidade interna do JSON. O TCC adapta essa motivação para inspeção direta de estado, distinguindo conformidade estrutural de correção factual.

**Leitura para este TCC:** no SUMIE, preservar perspectivas conflitantes é parte da tarefa; em FactConsolidation-SH, a regra é substituir fatos temporalmente obsoletos. Não tratar as duas políticas como equivalentes, nem atribuir diferenças entre datasets apenas à operação.

Referências: [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]]; [[06_Referencias/referencias#LongMemEval|LongMemEval]]; [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]].

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
6. Propõe avaliar fidelidade contra estados esperados estruturados sem LLM-as-judge nas métricas centrais, condicionada a uma política validada de canonicalização. Não replica diretamente o F1 original do SUMIE, que também usa avaliação semântica de evidências.

Lu et al. encontram dificuldades de difusão em chamadas de ferramentas e resultados competitivos em memória textual; Mündler et al. mostram que restrições gramaticais podem melhorar a sintaxe. Esses contrapontos impedem antecipar inferioridade da difusão em checkpoints JSON. Nenhum deles responde diretamente à comparação de writers compactos deste projeto. [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al., 2026]]; [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al., 2025]].
