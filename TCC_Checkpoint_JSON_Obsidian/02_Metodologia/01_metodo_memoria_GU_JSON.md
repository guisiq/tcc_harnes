---
title: "Método de memória — GU-JSON"
aliases:
  - "01 metodo memoria GU JSON"
tags:
  - tcc
  - metodologia
status: draft
---

# Método de memória — GU-JSON

## Definição

Será utilizado **Generate-Update em JSON (GU-JSON)**.

A cada nova observação, o memory writer recebe:

1. o schema;
2. o checkpoint atual;
3. a nova observação;
4. a instrução de atualização.

E gera **o checkpoint completo atualizado**.

```text
S + M_(t-1) + O_t -> G -> M_t
```

## Por que GU-JSON

GU-JSON é adequado porque reduz o número de variáveis independentes.

Ele evita introduzir:

- algoritmo programático de merge;
- escolha de JSONPath;
- retrieval;
- mecanismo externo que aplique resolução de conflito;
- geração dinâmica de schema.


## Evidência e escolha do método

Hwang et al. comparam Generate-Once (GO), Generate-Update (GU) e Generate-Merge (GM), em texto e JSON, nos datasets SUMIE e BooookScore, usando Gemini Ultra e Gemini Pro. Em cenário de memória limitada, `GU_json` supera `GU_text`; o artigo também relata que Chain-of-Key (`CoK_json`) supera as estratégias de baseline nos resultados apresentados.

Portanto, `GU_json` não é escolhido como o melhor método de escrita. Ele é fixado como uma estratégia incremental publicada, simples e replicável, para que o estudo investigue a variação entre os modelos escritores sem também variar o algoritmo de atualização. A comparação com `CoK_json`, GO e GM fica fora do escopo.

PRISM oferece um precedente de memória tipada atualizada por operações programáticas, diferente da reescrita integral. Serve como alternativa na fundamentação, não como nova condição experimental nem prova controlada contra GU-json. [[06_Referencias/referencias#Hwang et al. — structured incremental summarization|Hwang et al., 2024]]; [[06_Referencias/referencias#PRISM|PRISM, EMNLP 2025]].

A regra semântica da tarefa continua necessária: SUMIE preserva perspectivas conflitantes; FactConsolidation-SH invalida fatos antigos por precedência temporal explícita. O writer recebe essa regra, mas nenhum mecanismo externo corrige seu estado. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

## Relação com Yuen et al.

Yuen et al. implementam atualização a partir da memória anterior e da saída recente do agente. Há templates JSON, mas a variante genérica admite representação livre na revisão de janeiro de 2026.

**Uso no TCC:** precedente próximo de reescrita contextual em sistemas multiagente, não validação direta da fidelidade do GU-json compacto. Templates genéricos/gerados superam os manuais em vários testes; o schema fixo é controle do TCC, não resultado de superioridade atribuído ao artigo. [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al., 2025/2026]].

## Decisão

> Não comparar vários algoritmos de memória no experimento principal.

Isso mantém a variável principal concentrada na escolha do modelo que executa `G`.
