---
title: "Metodologia de revisão e busca"
aliases:
  - "05 metodologia revisao"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Metodologia de revisão e busca

## Papel desta parte

A revisão do TCC pode usar uma busca estruturada, sem necessariamente transformar o trabalho em uma revisão sistemática completa.

A auditoria de 2026-11-06 foi uma busca selecionada de fontes diretas e contrapontos, não comprovação exaustiva de novidade. As conferências de metadados e as leituras de método estão discriminadas em [[06_Referencias/referencias|Referências]]; não equivalem à execução integral do protocolo abaixo.

## Petersen et al. — systematic mapping

Systematic mapping é apropriado para:

- estruturar uma área;
- classificar contribuições;
- identificar tópicos e lacunas;
- observar frequência de tipos de estudo.

Referências:
- [[06_Referencias/referencias#Systematic mapping — Petersen 2008|Petersen et al., 2008]] — origem do procedimento.
- [[06_Referencias/referencias#Systematic mapping — Petersen 2015|Petersen et al., 2015]] — priorizar as diretrizes atualizadas.

## Kitchenham et al.

Útil para diferenciar:

- SLR;
- systematic mapping;
- síntese de evidência;
- estudo terciário.

[[06_Referencias/referencias#Kitchenham et al. 2010|Kitchenham et al., 2010]] fornece evidência terciária, não um manual completo de revisão. Usar em conjunto com Petersen 2015 para posicionamento metodológico, sem confundir seus objetivos.

## Wohlin — snowballing

Procedimento útil:

### Backward snowballing
examinar referências de artigos núcleo.

### Forward snowballing
examinar artigos que citam os artigos núcleo.

Fundamento: [[06_Referencias/referencias#Wohlin 2014|Wohlin, 2014]]; complementar a seleção/classificação com [[06_Referencias/referencias#Systematic mapping — Petersen 2015|Petersen et al., 2015]].

## Estratégia sugerida para este TCC

### Seed papers

1. Hwang — structured incremental summarization
2. SUMIE — dados e política de preservação
3. MemoryAgentBench — supersession temporal
4. PRISM — memória tipada e revisões programáticas
5. Yuen — Intrinsic Memory Agents, revisão de 2026
6. Qwen3 e T5Gemma — relatórios dos modelos
7. Block Diffusion — fundamento específico de BD3LM
8. Lu et al. e Mündler et al. — contrapontos sobre difusão e estrutura

Links e ordem detalhada: [[06_Referencias/artigos_prioridade|Artigos prioritários]]. Zeng/LoCoMo/Chain-of-Memory permanecem contexto complementar, não substituem fontes diretas de GU-json.

### Strings conceituais

```text
("LLM agent" OR "language model agent")
AND memory
AND (structured OR JSON OR state)
AND (update OR incremental OR consolidation)
```

```text
("diffusion language model")
AND (structured OR JSON OR infilling OR rewriting)
```

```text
("encoder-decoder" OR "seq2seq")
AND ("structured generation" OR JSON)
```

## Planilha de extração

Campos:

- título
- ano
- venue
- ano do preprint, revisão e publicação, separadamente
- venue confirmado nos anais ou apenas informado pelos autores
- modelo(s)
- tamanho
- tipo de memória
- update method
- dataset
- métrica
- estrutura
- código disponível?
- licença, revisão e acesso a dados/pesos
- relação com RQ
- limitações
- evidência direta, indireta ou contraponto
- nível de leitura e afirmações não sustentadas

Não promover uma referência apenas por ser mais nova. Registrar duas citações quando sustentarem aspectos complementares da mesma afirmação, explicitando quando os métodos, modelos ou métricas diferirem. Metadados de TI/PLN não certificam indexação em Scopus, Web of Science ou Qualis, que não foi verificada nesta auditoria.

## Critério de parada

Interromper snowballing quando duas iterações consecutivas não adicionarem estudos primários relevantes ao recorte.
