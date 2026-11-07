---
title: "Ficha do tema — avaliação de memory writers para checkpoints JSON"
aliases:
  - "Ficha do tema"
tags:
  - tcc
  - projeto
  - checkpoint-json
status: draft
---

# Ficha do tema — Trabalho de Conclusão de Curso

## Identificação

| Campo | Preenchimento |
| --- | --- |
| Aluno(a) | Guilherme Henrique Siqueira Lopes |
| Curso / Semestre | Sistemas de Informação - 2025/2 |
| Orientador(a) | Alex Coelho - a confirmar |

## Tema

**Modelos de linguagem compactos como escritores de memória: avaliação da atualização incremental de checkpoints JSON para agentes.**

O artigo em Markdown é a fonte de verdade para o escopo, método, objetivos e métricas desta proposta: [artigo_tcc_unitins.md](../07_Artigo_TCC/artigo_tcc_unitins.md). As observações nesta ficha são um resumo de delimitação, não substituem o artigo.

## Delimitação

| Faceta | Delimitação vigente |
| --- | --- |
| Objeto | Atualização incremental de checkpoints JSON pelo método GU-JSON; o escritor recebe o estado anterior e uma nova observação e gera o checkpoint completo. |
| Contexto | Componente de escrita de memória de agentes; não se avalia o desempenho de agentes em tarefas downstream. |
| Modelos | Qwen3-0.6B (*decoder-only*), T5Gemma B-B PrefixLM-IT (*encoder-decoder*) e Qwen3-0.6B BD3LM (difusão em blocos). São representantes específicos; diferenças não permitem atribuir causalidade à arquitetura isoladamente. |
| Dados | SUMIE é o benchmark principal. Uma amostra de FactConsolidation-SH é apenas uma verificação complementar opcional, se houver tempo após o experimento principal. |
| Protocolo | Prompt *zero-shot*, schema `{"state": {"chave": "valor"}}`, geração determinística *prompt-only* e limite de saída de 1.200 tokens por transição. |
| Métricas | Validade JSON e schema; State Precision, Recall e F1; taxa de alucinação; Preservation Accuracy e Update Accuracy, separada em ADD e UPDATE. |
| Ambiente | Execução local no Lenovo IdeaPad Gaming 3i, GTX 1650 e 24 GB RAM; compatibilidade, VRAM e precisão numérica ainda precisam ser confirmadas no piloto. |

Os detalhes, as definições operacionais e as exceções estão no [artigo principal](../07_Artigo_TCC/artigo_tcc_unitins.md), em especial nas seções de introdução e materiais e métodos.

## Problema de pesquisa

Cada atualização de um checkpoint reescreve o estado persistente. O escritor pode produzir JSON inválido, omitir informação válida, alterar valores indevidamente ou gerar conteúdo sem suporte. A proposta compara três modelos compactos sob o mesmo protocolo GU-JSON no SUMIE; a lacuna de pesquisa continua dependente de revisão bibliográfica focal.

## Pergunta de pesquisa

**Como representantes compactos dos paradigmas autoregressivo *decoder-only*, *encoder-decoder* e de difusão em blocos diferem na qualidade da atualização incremental de checkpoints pelo método GU-JSON no benchmark SUMIE, sob schema e limite de memória fixos?**

## Objetivo geral

**Comparar** a qualidade da atualização incremental de checkpoints JSON produzida pelos modelos compactos Qwen3-0.6B (*decoder-only*), T5Gemma B-B (*encoder-decoder*) e Qwen3-0.6B BD3LM (difusão em blocos), atuando como escritores de memória no método GU-JSON, no benchmark SUMIE e sob condições experimentais controladas.

## Objetivos específicos

1. Avaliar a conformidade estrutural dos checkpoints produzidos por cada escritor a partir das taxas de validade sintática do JSON e de aderência ao schema ao longo das transições.
2. Comparar a fidelidade do estado mantido por cada escritor ao longo dos turnos de atualização do SUMIE, utilizando precisão, revocação, F1 do estado e taxa de alucinação.
3. Analisar o perfil de erro dos escritores segundo o tipo de operação exigida no SUMIE, contrastando a preservação de atributos inalterados com a adição e a atualização de informações.

Os objetivos acima foram alinhados à introdução do [artigo principal](../07_Artigo_TCC/artigo_tcc_unitins.md). Se o artigo for alterado, atualize esta ficha a partir dele para evitar versões divergentes.

## Avaliação preliminar do tema

> Autoavaliação de trabalho, não é nota oficial nem validação institucional. Rever após a conferência das fontes, do hardware e da viabilidade do piloto.

| Critério | Nota | Justificativa |
| --- | --- | --- |
| Relevância | 2 | Persistir e atualizar estado é uma função pertinente em agentes multi-etapas. |
| Alinhamento | 2 | O tema relaciona Sistemas de Informação, modelos de linguagem e avaliação experimental. |
| Viabilidade temporal | 1 | Há três modelos e um benchmark; a execução local e o tempo total ainda precisam ser medidos. |
| Acesso a dados | 1 | SUMIE é público, mas a preparação dos estados de referência e as regras de avaliação precisam ser verificadas. |
| Delimitação | 2 | O protocolo principal fixa o método, o schema, o orçamento e o benchmark. A análise externa de supersession é opcional. |
| Originalidade | 1 | A comparação proposta é específica; a lacuna não deve ser apresentada como ausência geral de estudos sem revisão focal. |
| **Total** | **9/12** | **Estimativa provisória; revisar depois das verificações listadas no Anexo A.** |

## Anexo A — Argumentos, fontes e pontos para validação pessoal

Este anexo reúne o que deve ser conferido antes de tratar a ficha ou o artigo como versão final. Os registros abaixo são pistas de leitura, não substituem a consulta às fontes originais.

### A.1 Argumentos do recorte

- **Manter o método de escrita fixo:** GU-JSON permite comparar os escritores sem introduzir outro algoritmo de memória como variável. A fundamentação e as alternativas estão em [Atualização incremental e GU-JSON](../07_Artigo_TCC/artigo_tcc_unitins.md#2-memória-persistente-em-agentes-baseados-em-modelos-de-linguagem).
- **Usar o SUMIE como cenário principal:** o benchmark contém sequências de sumarização incremental de entidades com anotações por parágrafo. A adaptação para estado acumulado e a diferença em relação à avaliação original devem ser conferidas em [Dados e preparação das transições](../07_Artigo_TCC/artigo_tcc_unitins.md#3-materiais-e-métodos).
- **Tratar as métricas como proposta do TCC:** comparação determinística após normalização não é automaticamente equivalente à avaliação semântica original do SUMIE. Confira as regras e limites na seção de [métricas](../07_Artigo_TCC/artigo_tcc_unitins.md#3-materiais-e-métodos) e no artigo do benchmark.
- **Não generalizar da arquitetura:** cada condição é um modelo concreto, com treinamento, tokenizador e implementação próprios. As conclusões devem se referir aos modelos avaliados, não declarar superioridade universal de uma arquitetura.
- **Manter FactConsolidation-SH como opcional:** não é parte necessária do experimento principal. Só considerar a amostra complementar se o SUMIE estiver concluído e houver tempo.

### A.2 Conferências prioritárias

1. Conferir no artigo original do SUMIE quais modelos foram avaliados e revisar a afirmação do artigo do TCC de que eram “apenas modelos proprietários de grande porte”. A consulta anterior identificou Gemini-Nano entre os modelos avaliados; confirmar essa informação na fonte antes de corrigir a frase.
2. Validar o que o SUMIE considera acerto semântico, incluindo a ordem entre correspondência exata e uso de juiz LLM, e distinguir isso da métrica determinística proposta no TCC.
3. Definir e testar a normalização, os múltiplos valores por atributo e a regra de suporte usada para identificar alucinações; o texto atual ainda precisa de validação operacional detalhada.
4. Verificar os cartões e checkpoints exatos dos três modelos, seus limites de contexto e a interface do modelo BD3LM.
5. Medir a VRAM disponível e executar um piloto em cada modelo; confirmar FP16/BF16, tempo por transição e se o teto de 1.200 tokens acomoda todos os estados de referência.
6. Confirmar quais partes serão revisadas manualmente. A validação humana não deve ser descrita como realizada se ainda não tiver sido feita.
7. Conferir as citações, a justificativa do orçamento de 1.200 tokens, a análise estatística e o cronograma antes de gerar o documento final.

### A.3 Notas de apoio a revisar

Estas notas foram mantidas para leitura pessoal e podem conter argumentos antigos ou ainda não verificados. O artigo principal prevalece em caso de divergência.

- [Justificativa e lacuna](03_justificativa_lacuna.md)
- [Ameaças à validade — rascunho para revisão](../02_Metodologia/08_ameacas_validade.md)
- [Artigos núcleo — notas de leitura](../03_Revisao_Literatura/01_artigos_nucleo.md)
- [Lista priorizada de artigos](../06_Referencias/artigos_prioridade.md)
- [Notas de leitura a validar](../06_Referencias/leituras_para_validar/README.md)
- [Arquitetura do harness](../04_Implementacao/01_arquitetura_harness.md)
- [Prompt-base](../04_Implementacao/02_prompt_base.md)
- [Formato dos dados](../04_Implementacao/03_formato_dados.md)
- [Pipeline de avaliação](../04_Implementacao/04_pipeline_avaliacao.md)
