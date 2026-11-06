---
title: "Prompt base"
aliases:
  - "02 prompt base"
tags:
  - tcc
  - implementacao
status: draft
---

# Prompt base

## Objetivo

Criar uma instrução sem informação específica da arquitetura.

A regra de atualização deve preservar opiniões conflitantes no SUMIE e substituir fatos somente quando houver invalidação explícita, como em FactConsolidation-SH. O mesmo prompt-base é usado pelos writers; não adicionar correção externa de estado. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

## Template inicial

```text
You are the memory-state updater of an autonomous agent.

Your task is to update a persistent JSON state.

Rules:
1. Preserve existing information that is still valid.
2. Apply information explicitly introduced by the new observation.
3. Replace old facts only when the observation or task explicitly establishes that they are no longer valid. Preserve differing opinions and still-valid perspectives rather than assuming that the newest opinion wins.
4. Do not invent unsupported facts.
5. Respect the schema.
6. Return only the complete updated JSON object.

SCHEMA:
{{SCHEMA}}

CURRENT STATE:
{{CURRENT_STATE}}

NEW OBSERVATION:
{{OBSERVATION}}

UPDATED STATE:
```

## Política de idioma

Preferencialmente manter benchmark e prompt em inglês se os modelos/datasets originais forem avaliados assim.

Não introduzir tradução no experimento principal sem necessidade.

## Few-shot

Configuração inicial:
**zero-shot/instruction-only**.

Se algum writer falhar sistematicamente em entender o formato, avaliar:
- 1 exemplo único e idêntico para todos;
- documentar como nova condição.

Não adaptar exemplos individualmente por modelo.

## Output

Sem markdown fences.

Correto:

```json
{"state":{"budget":800}}
```

Incorreto:

````text
Here is the JSON:
```json
...
```
````
