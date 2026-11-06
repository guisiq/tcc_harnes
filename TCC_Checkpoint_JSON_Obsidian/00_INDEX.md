---
title: "TCC — Checkpoints JSON em agentes com SLMs locais"
aliases:
  - "00 INDEX"
tags:
  - tcc
  - indice
status: draft
---

# TCC — Checkpoints JSON em agentes com SLMs locais

> Pacote de projeto em Markdown preparado para importação no Notion.  
> Tema provisório: **Avaliação de paradigmas de geração para atualização incremental de checkpoints JSON em agentes baseados em SLMs locais**.

## Navegação

### Projeto
- [[01_Projeto/04_ficha_tema|Ficha do tema]]
- [[01_Projeto/01_visao_geral|Visão geral]]
- [[01_Projeto/02_perguntas_hipoteses|Perguntas de pesquisa e hipóteses]]
- [[01_Projeto/03_justificativa_lacuna|Justificativa e lacuna]]

### Metodologia
- [[02_Metodologia/01_metodo_memoria_GU_JSON|Método de memória: GU-JSON]]
- [[02_Metodologia/02_schema_checkpoint|Schema do checkpoint]]
- [[02_Metodologia/03_datasets|Datasets]]
- [[02_Metodologia/04_modelos|Modelos]]
- [[02_Metodologia/05_metricas|Métricas]]
- [[02_Metodologia/06_plano_experimental|Plano experimental]]
- [[02_Metodologia/07_hardware_tempos|Hardware e execução local]]
- [[02_Metodologia/08_ameacas_validade|Ameaças à validade]]

### Revisão de literatura
- [[03_Revisao_Literatura/00_mapa_literatura|Mapa da literatura]]
- [[03_Revisao_Literatura/01_artigos_nucleo|Artigos núcleo]]
- [[03_Revisao_Literatura/02_memoria_agentes|Memória em agentes]]
- [[03_Revisao_Literatura/03_geracao_estruturada_json|Geração estruturada e JSON]]
- [[03_Revisao_Literatura/04_arquiteturas_modelos|Arquiteturas de modelos]]
- [[03_Revisao_Literatura/05_metodologia_revisao|Metodologia de revisão]]

### Implementação
- [[04_Implementacao/01_arquitetura_harness|Arquitetura do harness]]
- [[04_Implementacao/02_prompt_base|Prompt base]]
- [[04_Implementacao/03_formato_dados|Formato dos dados]]
- [[04_Implementacao/04_pipeline_avaliacao|Pipeline de avaliação]]

### Planejamento
- [[05_Planejamento/01_cronograma|Cronograma]]
- [[05_Planejamento/02_checklist|Checklist]]
- [[05_Planejamento/03_resultados_esperados|Resultados esperados sem antecipar resultados]]

### Referências
- [[06_Referencias/referencias|Referências bibliográficas]]
- [[06_Referencias/artigos_prioridade|Lista priorizada de artigos]]
- [[06_Referencias/links|Links de modelos, datasets e código]]

## Decisão experimental atual

| Elemento | Escolha |
|---|---|
| Método de memória | Generate-Update em JSON (GU-JSON) |
| Variável independente principal | Paradigma/família do memory writer |
| Writer autoregressivo | Qwen3-0.6B |
| Writer encoder-decoder | T5Gemma B-B PrefixLM-IT |
| Writer diffusion | Qwen3-0.6B Diffusion BD3LM |
| Dataset principal | SUMIE |
| Contraste secundário | amostra FactConsolidation-SH focada em supersession |
| Schema | fixo |
| Budget de checkpoint | fixo em 300 tokens |
| Contexto máximo comum | até 8K no protocolo |
| Execução principal | PC 1 com GTX 1650 |
| Execução auxiliar | PC 2 para preparação, métricas e pós-processamento |

## Princípio de controle

O estudo deve modificar **uma coisa de cada vez**:

> mesmo dataset e sequência + mesmo schema + GU-json + mesmo prompt-base + mesmo limite de 300 tokens; muda apenas o modelo usado como `memory writer`.

Isso mantém a interpretação dos resultados mais limpa.

## Estado das decisões

- **Fechado:** foco em checkpoint JSON incremental.
- **Fechado:** GU-json como método fixo, não como alegação de método superior.
- **Fechado:** três paradigmas de geração.
- **Fechado:** modelos pequenos executáveis localmente.
- **Fechado:** SUMIE como cenário principal.
- **Em validação:** critérios e tamanho da amostra FactCon-SH de supersession.
- **Fora do escopo:** avaliação downstream, ablação de budget e terceiro dataset.
