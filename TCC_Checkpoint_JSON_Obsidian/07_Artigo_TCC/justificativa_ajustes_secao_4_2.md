---
title: "Justificativa dos ajustes na Seção 4.2 (Arquitetura proposta)"
tags:
  - tcc
  - artigo
  - revisao
status: para-revisao-do-orientador
---

# Justificativa dos ajustes na Seção 4.2 – Arquitetura proposta

Este documento registra cada inconsistência encontrada na Seção 4.2 de [artigo_tcc_unitins.md](./artigo_tcc_unitins.md), a alteração feita e a justificativa. As referências de escrita científica usadas foram:

- **Zucolotto (2013), módulos 3–4**: a legenda da figura fica abaixo dela; a figura deve ser compreensível sem o texto; o conteúdo deve ser equilibrado entre texto e legenda, sem repetição.
- **Zucolotto (2013), módulos 5–6**: evitar ambiguidade e redundância.
- **Zucolotto (2013), módulos 7–8**: cada parágrafo começa com uma frase-tópico (*topic sentence*).
- **Manual de TCC da Unitins** ([manual_tcc_v2.txt](../../anexos/Recursos/manual_tcc_v2.txt)): ilustrações "necessárias, autoexplicativas e que não se repitam"; título acima e fonte abaixo.
- **Moody (2009), *The "Physics" of Notations***: distinção perceptível entre símbolos, transparência semântica e não depender apenas da cor.

Também foi considerado o pedido do orientador ([tarefas_ajustes_artigo_tcc.md](./tarefas_ajustes_artigo_tcc.md), item 3): explicar como as tecnologias interagem e como o fluxo se liga aos parâmetros medidos.

## 1. Estrutura geral da seção

| Problema | Alteração | Justificativa |
|---|---|---|
| A seção começava pelo detalhe (A1) e só depois mostrava o contexto (A2). O leitor via o escritor sem saber onde ele se encaixa. | A ordem foi invertida. A **Figura 1** passou a ser a visão geral e a **Figura 2**, o detalhe da escrita. | A leitura vai do geral ao específico. A frase-tópico do primeiro parágrafo anuncia os dois níveis (Zucolotto, módulo 8). |
| Os rótulos "componente A1/A2" não eram definidos em nenhuma outra parte do artigo. | Os rótulos A1/A2 foram removidos. As figuras são citadas pelas etapas (i)–(ix) da Seção 3.5. | Evita termo sem definição (ambiguidade, módulos 5–6) e reaproveita a numeração já apresentada no método. |
| A seção não dizia por que a arquitetura existe. | O parágrafo de abertura passou a dizer que o objetivo é **variar apenas o escritor** (Quadro 2). | Liga a arquitetura ao desenho experimental da Seção 3.1. |
| A ressalva "fluxo planejado, não resultado experimental" aparecia duas vezes, nas duas fontes. | Passou a aparecer uma só vez, no parágrafo de abertura. As linhas "Fonte" ficaram só com a autoria e a origem. | Redundância (módulo 6). A linha "Fonte" deve indicar origem, não fazer ressalvas. |
| Faltava explicar como as tecnologias interagem (pedido do orientador). | Foi criado o **Quadro 5**, com as colunas Etapa, Componente e tecnologia, Controle (fixo/variável) e Saída usada na avaliação. | Ver a Seção 4. |

## 2. Figura 1 – visão geral (antiga A2)

| Problema na figura antiga | Correção | Justificativa |
|---|---|---|
| **A (o mais grave):** a caixa "Preparar" continha "anotações/operações" e tinha uma seta para o escritor, sugerindo vazamento da resposta esperada. | A referência ($M_t^*$, anotações e rótulos) fica numa região tracejada, "Somente avaliação (não enviada ao escritor)". Ela é alimentada por um caminho próprio a partir da etapa (i) e se liga só à correspondência direta e ao juiz. | Tornar visível o controle contra vazamento. O texto repete a regra em uma frase. |
| **B:** a leitura em Z obrigava o olhar a voltar. | Execução numa linha horizontal (i)→(iv) e avaliação numa coluna vertical (v)→(ix), dispostas em "L". | Um único sentido de leitura por fase. |
| **C:** o bloco "Validar e avaliar" juntava as etapas (v)–(viii) e escondia as decisões. | Losangos de decisão para "JSON válido?", "Esquema válido?" e "Há divergência?", com ramos "sim/não". | As decisões determinam as métricas (zero na visão global, juiz condicional) e por isso precisam aparecer. |
| **D:** não mostrava o que o juiz recebe. | A caixa (viii) informa: Gemma 3 1B Q4_K_M; recebe $M_{t-1}^*$, $O_t$, $M_t^*$ e $M_t$; não recebe a identidade do escritor. | Coerência com as Seções 3.5 e 3.6 e com o controle de viés da Seção 3.9 b. |
| **E:** não havia ligação com os objetivos nem com a análise estatística (pedido do orientador). | Três caixas de métricas (Estrutural · a, Estado · b, Operação · c, com os nomes do Quadro 3) e a barra "Análise estatística (Seção 3.7)". | Rastreabilidade com o Quadro 4. |
| **F:** títulos e notas repetidos dentro da imagem. | O título foi retirado da imagem; fica só o título do artigo, acima da figura. | Manual da Unitins (título acima) e Zucolotto (não repetir). |
| **G:** sem legenda de formas e cores. | Legenda com cilindro, retângulos por função, losango e contorno tracejado. A variável do experimento tem contorno laranja e também o texto "única variável". | Moody (2009): distinção perceptível sem depender só da cor. A figura passa a ser autoexplicativa (manual da Unitins). |
| **H:** notação ASCII ("M*_t-1"). | Subscritos e sobrescritos tipográficos ($M^*_{t-1}$, $O_t$, $M_t$). | A notação da figura passa a ser igual à das equações. |
| Falhas estruturais sem destino explícito. | Os ramos "não" de (v) e (vi) vão aos registros com o rótulo "falha estrutural: zero na visão global". | Explicita a regra da Seção 3.6 (visões condicional e global). |

## 3. Figura 2 – etapa de escrita (antiga A1)

| Problema na figura antiga | Correção | Justificativa |
|---|---|---|
| O limite de 1.200 *tokens* aparecia dentro do *prompt*. | O limite foi para a caixa do escritor ("um por execução · ≤ 1.200 tokens"). | O orçamento é um parâmetro de geração, não um texto enviado ao modelo (Seção 3.2). |
| A ordem das entradas era diferente da do Apêndice A. | Os campos aparecem na ordem do Apêndice A: instruções → `SCHEMA` → `CURRENT STATE` → `NEW OBSERVATION` → `UPDATED STATE`. | Correspondência direta com o Apêndice A. |
| **(Revisão posterior, observação do autor)** As entradas apareciam como caixas separadas, ligadas a campos vazios do *prompt*, com a nota "campos preenchidos pelo harness" ao lado de apenas alguns deles. Não ficava claro que o *prompt* preenchido **é** a entrada do escritor, isto é, a tripla $(S, M^*_{t-1}, O_t)$. | O *prompt*-base passou a ser desenhado já preenchido, com o conteúdo do exemplo dentro de cada campo. A seta até o escritor recebe o rótulo $(S, M^*_{t-1}, O_t)$. À esquerda, duas caixas indicam a origem dos campos: **Fixo** (instruções e esquema $S$, iguais em todas as transições) e **SUMIE** (cilindro de conjunto de dados, como na Figura 1: $M^*_{t-1}$ e $O_t$ de cada transição). `UPDATED STATE` indica onde o escritor começa a gerar $M_t$. | Representar a entrada como um único objeto evita a leitura de que o *prompt* seria um componente intermediário separado dos parâmetros da Equação 1. A origem de cada campo fica explícita. |
| O esquema aparecia como "atributo/texto". | Passou a `{"state": {"chave": "valor"}}`, igual à Seção 3.2. | Terminologia única. |
| Mistura de PT/EN e o nome "Gerador GU-JSON". | Rótulos em português; o escritor aparece como "Escritor $G$", com o paradigma de cada modelo. Os nomes dos campos ficam em inglês porque são o texto literal do *prompt*. | O texto fala em "escritor" e a Equação 1 usa $G$. |
| A observação era uma paráfrase e a saída, "hipotética". | A frase P9 agora é citada literalmente e a saída é o par anotado no SUMIE. | Verificado no conjunto público (Seção 6). Um exemplo real é mais forte do que um ilustrativo. |
| A equação não aparecia ligada à figura. | A Equação 1 aparece acima do escritor, com $M_{t-1}=M^*_{t-1}$ ("com o estado anterior de referência"). | Liga a figura às Seções 2.3 e 3.2. |
| `ENTITY0`, P9 e o estado vazio não eram explicados. | O parágrafo da Figura 2 explica cada item. | Evita pressuposto implícito (módulos 5–6). |

## 4. Nova tabela: Quadro 5

O Quadro 5 foi criado porque as figuras mostram **fluxo e dependências**, mas não comportam bem três informações pedidas pelo orientador e necessárias para reproduzir o experimento:

1. Qual tecnologia executa cada etapa (`json.loads`, validador de esquema, Gemma 3 1B GGUF `Q4_K_M`, JSON Lines).
2. O que é **fixo** e o que é **variável** em cada etapa, e quando cada regra é congelada (Fase 1 ou antes da Fase 2).
3. Qual artefato cada etapa entrega à avaliação, ligando cada etapa a uma métrica do Quadro 3.

Pôr essas informações nas figuras as deixaria sobrecarregadas. Repeti-las no texto criaria redundância. O quadro mantém o equilíbrio recomendado por Zucolotto (módulo 4): a figura mostra a sequência, o quadro dá os detalhes de cada etapa e o texto interpreta.

Não foram criados outros diagramas: as duas figuras e o quadro cobrem o fluxo, o detalhe da escrita e as tecnologias, sem sobreposição.

## 5. Ajustes no capítulo de métodos (para manter a harmonia com a 4.2)

| Seção | Problema | Alteração |
|---|---|---|
| 3.2 | Usava $M_{t-1}$, enquanto a 3.3 e as figuras usam $M^*_{t-1}$. Ficava subentendido que a saída anterior realimenta o turno seguinte. | Passou a dizer "Equação 1 com $M_{t-1}=M^*_{t-1}$", com remissão à Seção 3.3 e uma frase dizendo que a saída de um turno não volta como entrada. |
| 3.4 c | O BD3LM não tinha nota de rodapé nem identificador, ao contrário dos outros dois modelos. | Frase dizendo que o identificador público do *checkpoint* será confirmado na Fase 0 e registrado no manifesto. Nenhuma URL foi inventada. |
| 3.5 | "Adaptador", *template* de conversa, modo *thinking*, parâmetros de difusão e "determinística" eram usados sem definição. | Novo parágrafo: o adaptador aplica o *template* e os *tokens* BOS/EOS sem mudar o *prompt*; o *thinking* do Qwen3 é desativado; "determinística" significa sem amostragem e com semente fixa; no BD3LM, o tamanho de bloco, os passos e o critério de desmascaramento são fixados no manifesto. O parágrafo remete à Seção 4.2. |

## 6. Verificação do exemplo no SUMIE

Foi conferido no conjunto público (`dataset_sumie.jsonl`, chave `paragraph_summary_pairs`):

- `ENTITY0` é o nome mascarado ("ENTITY" + índice) de uma entidade da categoria *Computer & Video Games*.
- `P9` é o `sentence_id` da frase "The game's replayability is further enhanced by its multiple endings, encouraging players to revisit ENTITY0 and explore different narrative paths.", no primeiro parágrafo.
- O par anotado para essa frase é `Replayability: Multiple endings` (`sentence_ids: [P9]`).

A Figura 2 de Hwang et al. (2024) tem a legenda "Overall incremental summarization process with a structured memory representation based on user-defined schema". Isso confirma que a analogia citada no texto procede. Também confirma a ressalva: as perguntas em "LLM thoughts" daquela figura pertencem ao *Chain-of-Key*, que este protocolo não usa.

## 7. Decisões que dependem da aprovação do orientador

As alterações abaixo explicitam escolhas que antes estavam implícitas. Elas precisam ser confirmadas:

1. **Modo *thinking* do Qwen3-0.6B desativado** (Seção 3.5), para que os 1.200 *tokens* sejam gastos só com o JSON. Se mantido, deve entrar no manifesto e na Seção 3.9.
2. **Identificador do BD3LM:** ainda não confirmado. Pela redação adotada, será fixado na Fase 0. A nota de rodapé com a URL deve ser acrescentada quando houver confirmação.
3. **Atributos repetidos no SUMIE:** no mesmo parágrafo de `ENTITY0`, o atributo `Gameplay` aparece duas vezes, com valores diferentes. O esquema plano `{"chave": "valor"}` não comporta duas entradas com a mesma chave. É preciso definir, na Fase 1, uma regra de agregação (por exemplo, concatenar os valores) e citá-la na Seção 3.3. **O método não foi alterado; o ponto fica apenas sinalizado.**
4. **Numeração dos quadros:** o novo quadro é o Quadro 5. Se uma futura Seção 4.3 de mapeamento incluir outro quadro antes do cronograma, a numeração terá de ser revista.

## 8. Arquivos alterados

- [artigo_tcc_unitins.md](./artigo_tcc_unitins.md): Seções 3.2, 3.4 c, 3.5 e 4.2 (com o novo Quadro 5).
- [diagramas_pesquisa/gerar_figuras_harness.py](./diagramas_pesquisa/gerar_figuras_harness.py): novo gerador das figuras.
- [diagramas_pesquisa/fig1_harness_visao_geral.svg](./diagramas_pesquisa/fig1_harness_visao_geral.svg) e `.png`: nova Figura 1.
- [diagramas_pesquisa/fig2_harness_escrita.svg](./diagramas_pesquisa/fig2_harness_escrita.svg) e `.png`: nova Figura 2.
- Removidos: `a1_geracao_memoria.{svg,png}` e `a2_fluxo_experimental.{svg,png}`, substituídos pelas novas figuras.
- [../04_Implementacao/01_arquitetura_harness.md](../04_Implementacao/01_arquitetura_harness.md): links e descrições atualizados.
