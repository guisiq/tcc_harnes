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

## 8. Realocação: a arquitetura passa a ser a Seção 3.6 de Materiais e métodos

A antiga Seção 4.2, "Arquitetura proposta", passou a ser a **Seção 3.6, "Arquitetura do *harness*"**, logo após a 3.5. As demais seções deste documento usam a numeração anterior, em que 4.2 é a Arquitetura proposta e o Quadro 5 é o das etapas do *harness*.

| Alteração | Justificativa |
|---|---|
| Arquitetura movida do capítulo 4 para a 3.6. | A arquitetura descreve o instrumento de medição: o fluxo planejado que garante que só o escritor varie. É método, não resultado. As diretrizes da Unitins pedem que Materiais e métodos traga o necessário para a "reprodução do estudo". Na aula de 26/09/2026 (01:01:39 e 01:26:19), o professor afirmou que, no TCC I, o capítulo principal é Materiais e métodos e que o capítulo de resultados ainda "não existe". |
| Colocada logo após a 3.5 (*harness*). | A 3.5 lista as nove etapas e a 3.6 as ilustra com a Figura 1, o Quadro 3 e a Figura 2. O texto vai do enunciado à representação sem salto de capítulo. |
| Retirada a ressalva "fluxo planejado, e não resultados experimentais". | Dentro do capítulo de métodos, a ressalva é desnecessária. Ela só existia porque a seção estava no capítulo de resultados. |
| Seções seguintes renumeradas: Métricas → 3.7, Procedimento → 3.8, Rastreabilidade → 3.9, Limitações → 3.10. Remissões internas atualizadas, inclusive dentro da 3.6. | Mantém as referências cruzadas corretas. |
| Quadros renumerados pela ordem de aparição: etapas do *harness* → Quadro 3, métricas → Quadro 4, rastreabilidade → Quadro 5. | Os quadros devem ser numerados na ordem em que aparecem no texto (manual da Unitins). |
| Capítulo 4 renumerado: 4.1 Resultados e contribuições esperadas e 4.2 Cronograma. A frase de abertura e a da introdução do capítulo 3 foram ajustadas. | A frase-tópico deve anunciar as subseções que realmente existem (Zucolotto, módulo 8). |

**Ponto em aberto para o orientador:** na mesma aula, o professor sugeriu que, no TCC I, os resultados esperados fiquem como seção de Materiais e métodos, sem um capítulo "Resultados". Essa mudança não foi feita e depende do modelo da Unitins e do orientador.

## 9. Revisão sistemática na metodologia (nova Seção 3.1) e Quadro 1 ampliado

Foi criada a **Seção 3.1, "Revisão sistemática da literatura"**. As seções seguintes do capítulo 3 avançaram um número: Arquitetura → 3.7, Métricas → 3.8, Procedimento → 3.9, Rastreabilidade → 3.10, Limitações → 3.11. Os quadros também avançaram: Variáveis → 3, Etapas do *harness* → 4, Métricas → 5, Rastreabilidade → 6. As Seções 1 a 8 deste documento mantêm a numeração da época em que foram escritas.

| Alteração | Justificativa |
|---|---|
| Passo a passo da revisão como Seção 3.1, em sete etapas (protocolo, fonte e consultas, controles, deduplicação, triagem, elegibilidade, extração e síntese). | O Quadro 1 e a lacuna da introdução dependiam de uma busca que não estava descrita no artigo. Material e métodos deve permitir reproduzir o estudo (diretrizes Unitins), e isso inclui reproduzir como os trabalhos relacionados foram selecionados. As etapas seguem Petersen et al. (2015), já citado no protocolo do mapeamento. |
| A seção ficou como a primeira do capítulo 3. | A revisão é anterior ao desenho experimental e o justifica: primeiro se delimita o que existe e depois se define o experimento. |
| Novo **Quadro 2 – Consultas da revisão sistemática no arXiv**, com faceta e número de registros. | As seis consultas e o total após a deduplicação são o núcleo reproduzível da busca. Em prosa, as expressões booleanas ficariam ilegíveis. Por isso o quadro mostra a faceta, e as expressões completas ficam no repositório (`protocolo_focado_estrito.json`). |
| Limitações da revisão declaradas no fim da 3.1: uma única fonte de *preprints*, consultas estreitas, dois controles não recuperados, triagem assistida por modelo sem avaliador humano e texto integral verificado em parte. | Apresentar a revisão como abrangente seria uma afirmação sem respaldo. Os números saem de `mapeamento_focado_trabalhos_relacionados_2025_2026.md` e de `decisoes/_execucao_llm.json`, que registra o modelo `claude-haiku-5.5`. |
| **Quadro 1** dividido em "Estudos de base" e "Estudos selecionados na revisão sistemática", com os dez estudos selecionados. O *Bitter Lesson* passou ao segundo grupo, e os dois comparadores estão marcados. | Distingue o que veio do levantamento bibliográfico do que veio do procedimento sistemático. As colunas são as mesmas da extração (etapa g), o que liga o quadro ao método. |
| Parágrafo de síntese da 2.7 reescrito. | A revisão contradiz duas afirmações antigas. "Os *benchmarks* de memória avaliam respostas finais" não vale para o AlpsBench, que avalia a memória atualizada. E escritores compactos já existem (MemReader, DimMem, AMU). A lacuna foi reformulada como uma combinação que ainda não foi encontrada: GU-JSON, SUMIE, três paradigmas compactos e avaliação por operação. A ressalva de escopo foi mantida. |
| Introdução: uma frase sobre escritores compactos já existentes, e "na literatura consultada" trocado por "na revisão sistemática realizada (Seção 3.1)". | Mantém a introdução coerente com o novo Quadro 1 e dá base verificável à afirmação da lacuna. |
| Parágrafo de organização da introdução corrigido. | O texto ainda dizia que a seção 4 continha a arquitetura, o que não vale desde a realocação da Seção 8. |
| Cronograma, atividade 2: incluída a revisão sistemática. | A atividade passou a ser descrita no método e precisa aparecer no planejamento. |

**Pendências que o autor precisa resolver:**

1. **Chaves do Zotero:** apenas `luBitterLessonDiffusion2026` e `petersenGuidelinesConductingSystematic2015` existem na biblioteca. As outras nove chaves foram previstas pelo padrão do Better BibTeX (sobrenome do primeiro autor, três palavras do título e ano) e **precisam ser conferidas** depois de importar [mapeamento_focado_selecionados_2025_2026.ris](./mapeamento_focado_selecionados_2025_2026.ris). As chaves previstas são:
   - `biniMemLoRADistillingExpert2025`
   - `xiaoAlpsBenchLLMPersonalization2026`
   - `kangMemReaderPassiveActive2026`
   - `qiuDimMemDimensionalStructuring2026`
   - `wangCMIMemGeneralizableLongTerm2026`
   - `choiPGMemTightlyCoupled2026`
   - `zhaoMakingProspectiveMemory2026`
   - `hwangAMUAdmissionMemory2026`
   - `zhouDiffuPlanEditablePlanning2026`

   O Zotero tem três registros duplicados do Petersen (2015); convém mesclá-los.
2. **Conferência no texto integral:** o relatório do mapeamento recomenda confirmar método, modelos e resultados de cada estudo antes da versão final.
3. **Supersede** não tem chave nem citação no artigo, apenas o nome, porque não foi recuperado e não está no Zotero.
4. **Avaliador humano:** se houver tempo no TCC II, uma dupla verificação humana de uma amostra das decisões reduziria a principal limitação da revisão.

## 10. Seção 2.7 mantida e citação dos artefatos da revisão

### 10.1 Por que a 2.7 não foi retirada

A 2.7 foi mantida no Referencial Teórico. O que está na 3.1 é o **procedimento** da busca; o que está na 2.7 é o **produto** dela (o Quadro 1 e a análise da lacuna). São funções diferentes, então não há redundância.

| Fonte | O que diz | Consequência |
|---|---|---|
| Aula de 19/09 ([P1 00:09:22](../../AULAS/2026-2/transcricoes/2026-09-19_parte-01.md#s0091) a [00:11:15](../../AULAS/2026-2/transcricoes/2026-09-19_parte-01.md#s0113)) | "Da revisão da literatura, a gente produz duas coisas [...] no capítulo de revisão, vocês vão ter pelo menos duas subseções": o estado da arte e "uma tabela de trabalhos relacionados", cuja "última linha [...] é o seu trabalho". | A tabela pertence ao capítulo de revisão. Retirar a 2.7 contraria a orientação da disciplina. |
| Aula de 19/09 ([P1 00:36:05](../../AULAS/2026-2/transcricoes/2026-09-19_parte-01.md#s0386)) | No enquadramento metodológico, a revisão deve registrar consulta, seleção, exclusões e critérios de comparação. | O passo a passo fica em Métodos (3.1), como já está. |
| Aula de 05/09 ([P2 00:34:02](../../AULAS/2026-2/transcricoes/2026-09-05_parte-02.md#s0370)) | "Foi feita essa consulta, como resultado foram tantos artigos, o critério de seleção foi [...] isso vai virar uma ou duas páginas no trabalho." | Confirma que a documentação da busca é um texto próprio, separado da análise. |
| Checklist da disciplina, [C17 e C21](../../AULAS/2026-2/checklist_tcc.md#c17) | C17 pede registrar protocolo e resultados da busca; C21 pede "construir análise e tabela de trabalhos relacionados". | São dois itens distintos, um de método e outro de revisão. |
| Wazlawick, *Preparação do trabalho de pesquisa* ([slide 11](../../artigos/05-metodologia-e-escrita-cientifica/Wazlawick_UFU_Preparacao_Trabalho_Pesquisa/Wazlawick_UFU_Preparacao_Trabalho_Pesquisa.md)) | "O capítulo de revisão bibliográfica vai apresentar os conceitos necessários [...] e os trabalhos relacionados ao objetivo." | Mesma divisão. |
| Gerhardt e Silveira (2009, seção 4.1.3, [texto](../../artigos/05-metodologia-e-escrita-cientifica/Gerhardt_Silveira_2009_Metodos_de_Pesquisa_UFRGS/Gerhardt_Silveira_2009_Metodos_de_Pesquisa_UFRGS.md)) | A revisão (estado da arte) deve "explicar no que seu trabalho vai se diferenciar dos trabalhos já produzidos". | É a função do parágrafo de síntese da 2.7. |
| Prodanov e Freitas (2013, p. 78, [texto](../../artigos/05-metodologia-e-escrita-cientifica/Prodanov_Freitas_2013_Metodologia_do_Trabalho_Cientifico/Prodanov_Freitas_2013_Metodologia_do_Trabalho_Cientifico.md)) | A revisão responde "quem já escreveu [...] quais as lacunas existentes na literatura" e situa o trabalho, "afunilando" a discussão. | A 2.7 fecha o funil do capítulo 2 com a lacuna, que a introdução retoma. |

**O que mudou:** a referência cruzada passou a existir nos dois sentidos. A 2.7 já remetia à Seção 3.1. Agora a abertura do capítulo 2 diz que os trabalhos mais próximos foram "selecionados pelo procedimento descrito na Seção 3.1", e o passo g) da 3.1 aponta o "Quadro 1 (Seção 2.7)". A remissão a uma seção posterior é aceitável porque o leitor é avisado de onde está o método.

### 10.2 Como citar os *scripts* e artefatos

Foram separados três casos, porque cada um tem uma forma correta diferente.

| Caso | Forma adotada | Justificativa |
|---|---|---|
| **Ferramentas de terceiros** (API do arXiv, GitHub Copilot SDK) | Nome e **versão** no texto (SDK 1.0.31, modelo `claude-haiku-5.5`) e nota de rodapé "Disponível em: URL." | É o mesmo padrão já usado no artigo para o SUMIE e para os modelos (notas na 3.4 e na 3.5). Na aula de 19/09 ([P2 00:23:11](../../AULAS/2026-2/transcricoes/2026-09-19_parte-02.md#s0269)), a versão do *software* aparece como informação relevante quando o resultado depende dela; aqui, a triagem depende do modelo e do SDK. A versão foi lida de `decisoes/_execucao_llm.json`. |
| **Artefatos produzidos pelo autor** (protocolo, *scripts*, respostas brutas, decisões) | Descrição do método no texto (3.1), **lista dos artefatos no Apêndice B** (Quadro 7) e uma nota de rodapé com o URL de um **repositório próprio da revisão**, fixado na **versão** `v1.0.0` (ver 10.3). | Prodanov e Freitas (2013, seção 6.1.14): o apêndice é o "material, elaborado pelo próprio autor, [...] que se destina apenas a complementar as ideias" do trabalho. A aula de 12/09 ([P1 00:27:00](../../AULAS/2026-2/transcricoes/2026-09-12_parte-01.md#s0286); [relatório](../../AULAS/2026-2/relatorios/2026-09-12.md)) recomenda "manter o método no texto, os experimentos em código versionado". A mesma aula ([P1 00:55:01](../../AULAS/2026-2/transcricoes/2026-09-12_parte-01.md#s0567)) indica apontar "para uma *tag* específica do GitHub", para saber qual versão foi usada. A etiqueta `v1.0.0` fixa o *commit* publicado e não muda se o ramo `main` receber novos *commits*. Os *scripts* não entram nas Referências porque não são obra publicada de outro autor: são material do próprio trabalho. |
| **Versão definitiva** (recomendada, a fazer pelo autor) | Depositar o pacote no **Zenodo** a partir da *release* `v1.0.0` e substituir a nota de rodapé por uma **referência** com DOI: autor, título, versão, ano, Zenodo, DOI. | A aula de 12/09 ([P1 00:53:04](../../AULAS/2026-2/transcricoes/2026-09-12_parte-01.md#s0534) a [01:04:26](../../AULAS/2026-2/transcricoes/2026-09-12_parte-01.md#s0674)) apresenta o Zenodo como repositório que registra data, autoria e versões com DOI, e o DOI de cada versão continua válido quando o pacote é atualizado. Só com um DOI o artefato vira uma obra referenciável; um link do GitHub pode mudar. |

**Verificação feita:** o comando do Apêndice B, `dotnet run scripts/busca_focada.cs -- offline`, foi executado em um **clone limpo** do repositório publicado. Ele conferiu os *hashes* do protocolo e das seis respostas, regenerou 158 candidatos, 13 CORE e 10 selecionados, e não alterou nenhum arquivo versionado (`git status` vazio). O CSV e o RIS são idênticos, *byte* a *byte*, aos gerados na pasta original do TCC. Ou seja, a síntese é reproduzível a partir dos artefatos citados.

**Pendências do autor:**

1. **Zenodo (opcional, recomendado).** Ativar o repositório em zenodo.org (GitHub → *Enable*) e publicar uma nova *release*; o Zenodo só arquiva *releases* criadas depois da ativação. Em seguida, trocar a nota de rodapé da 3.1 por uma referência com DOI.
2. **"Acesso em:".** Prodanov e Freitas (2013, seção sobre documentos em meio eletrônico) indicam "Disponível em: <URL>. Acesso em: data." para documentos *on-line*. As notas de rodapé já existentes no artigo não trazem "Acesso em", e as novas seguiram o mesmo padrão. Convém acrescentar a data de acesso em **todas** de uma vez, conforme o modelo da Unitins.

### 10.3 Repositório próprio para os artefatos da revisão

**Decisão:** em vez de citar o repositório de trabalho do TCC, os artefatos foram publicados em um repositório limpo, [guisiq/tcc_revisao_sistematica_sumarizacao_recorrente](https://github.com/guisiq/tcc_revisao_sistematica_sumarizacao_recorrente), com a etiqueta e a *release* `v1.0.0` e a licença MIT.

| Motivo | Justificativa |
|---|---|
| O leitor deve encontrar só o que o texto cita | O repositório do TCC mistura rascunhos, notas, aulas, materiais de terceiros e o mapeamento amplo descartado. Prodanov e Freitas (2013, seção 6.1.14) definem o apêndice como material que "se destina apenas a complementar as ideias" do trabalho; o pacote citado deve ter o mesmo recorte. A aula de 12/09 ([P1 00:27:00](../../AULAS/2026-2/transcricoes/2026-09-12_parte-01.md#s0286)) separa o método, no texto, dos experimentos em código versionado. |
| Versão fixa e citável | A etiqueta `v1.0.0` substitui a antiga `revisao-sistematica-v1`, que nunca foi enviada e foi apagada. A *release* é o ponto de entrada do Zenodo para o DOI (aula de 12/09, [P1 00:53:04](../../AULAS/2026-2/transcricoes/2026-09-12_parte-01.md#s0534)). |
| Licença explícita | O repositório do TCC não tem licença, o que impede o reuso legal. O novo repositório usa a MIT, conforme escolha do autor. |
| Transparência | Além da execução final, foram incluídos o piloto e o ensaio, com seus protocolos, porque o artigo e o README somam o custo das duas execuções (49 créditos) e mencionam o refinamento das consultas. O mapeamento amplo (v2) ficou de fora porque não alimenta o Quadro 1. |

**Diferenças em relação à origem**, registradas no README do novo repositório:

- `busca_focada.cs` grava em `resultados/`, e não mais na pasta pai. A citação de Prodanov e Freitas no relatório ficou em texto, porque o link apontava para um arquivo local que não pode ser redistribuído.
- `triagem.cs` lê `protocolo/triagem_llm.json`, uma cópia literal da seção `triagem` do `protocolo.json` amplo, que era o arquivo lido na execução original. Assim, o `protocolo.json` não precisou ser publicado.
- O `.gitattributes` desativa a conversão de fim de linha (`* -text`). Sem isso, um clone no Windows trocaria LF por CRLF, e a verificação SHA-256 dos *snapshots* falharia.

Dados, protocolos, decisões e a revisão final não foram alterados.

## 11. Arquivos alterados

- [artigo_tcc_unitins.md](./artigo_tcc_unitins.md): Seções 3.2, 3.4 c, 3.5 e 4.2 (com o novo Quadro 5). Depois, a arquitetura foi movida para a Seção 3.6, e as seções e quadros foram renumerados (ver Seção 8). Por fim, foram incluídos a Seção 3.1 e o Quadro 2, ampliado o Quadro 1 e ajustados a introdução, a 2.7 e o cronograma (ver Seção 9). Depois, foram incluídos as referências cruzadas entre o capítulo 2 e a Seção 3.1, as versões e notas das ferramentas, a nota com o repositório e o Apêndice B (Quadro 7) (ver Seção 10). Por último, a nota e o Apêndice B passaram a apontar para o repositório próprio da revisão (ver 10.3).
- [diagramas_pesquisa/gerar_figuras_harness.py](./diagramas_pesquisa/gerar_figuras_harness.py): novo gerador das figuras.
- [diagramas_pesquisa/fig1_harness_visao_geral.svg](./diagramas_pesquisa/fig1_harness_visao_geral.svg) e `.png`: nova Figura 1.
- [diagramas_pesquisa/fig2_harness_escrita.svg](./diagramas_pesquisa/fig2_harness_escrita.svg) e `.png`: nova Figura 2.
- Removidos: `a1_geracao_memoria.{svg,png}` e `a2_fluxo_experimental.{svg,png}`, substituídos pelas novas figuras.
- [../04_Implementacao/01_arquitetura_harness.md](../04_Implementacao/01_arquitetura_harness.md): links e descrições atualizados.

## 12. Correção e validação do DOCX institucional

### 12.1 Base normativa e uso dos exemplos

A exportação direta anterior não executava o fluxo institucional completo. A nova versão foi produzida pelo [script PowerShell existente](../../ferramentas/gerar-artigo-unitins.ps1), com o [preparador Python](../../ferramentas/gerar_artigo_unitins.py), o [cabeçalho oficial de 2025](../../anexos/Recursos/Cabeçalho%20oficial%202025.docx), o filtro Zotero e a paginação efetiva pelo Word.

As regras gerais foram conferidas nas [Diretrizes gerais de TCC](../../anexos/Recursos/diretrizes_gerais_tcc.pdf), especialmente nas seções 5.1–5.4 e 5.8, e no [Manual de Sistemas de Informação](../../anexos/Recursos/manual_sistemas_tcc_2024.pdf), seções 7.1.1, 7.1.6, 7.2 e Anexo II. Embora o nome desse último arquivo contenha “2024”, sua identificação institucional é **2025**. No PDF, a formatação está na página 14, o resumo na 16 e a estrutura de arquivamento do artigo na 25.

Os [TCC 596](../../artigos/05-metodologia-e-escrita-cientifica/TCC_Unitins_SI_596.pdf) e [TCC 1335](../../artigos/05-metodologia-e-escrita-cientifica/TCC_Unitins_SI_1335.pdf) foram usados como exemplos de aplicação, não como substitutos das normas: o primeiro se identifica como artigo de graduação; o segundo, como monografia. Capa, folha de rosto e listas foram preservadas porque o Anexo II distingue a apresentação para arquivamento institucional daquela exigida por um veículo de publicação. Não se presumiu que todo artigo deva ter a estrutura de uma monografia.

| Aspecto | Decisão e fundamento |
|---|---|
| Página e texto | A4; margens superior/esquerda de 3 cm e inferior/direita de 2 cm; Arial 12, justificado, entrelinha 1,5 e primeira linha de 1,25 cm, conforme as regras gerais consultadas. |
| Resumos e notas | Resumo e abstract em 11, parágrafo único e espaço simples; notas em Arial 10, simples e alinhadas à esquerda. O manual admite 10 ou 11 para o resumo; escolheu-se 11. |
| Títulos e legendas | Títulos sem indicativo numérico centralizados; legendas e fontes em 10 e espaço simples. As duas figuras receberam legendas reconhecidas pelo gerador e lista de ilustrações própria. |
| Tabelas e quadros | A seção 5.8 das Diretrizes exige título acima da tabela, sem fechamento lateral, e admite moldura nos quadros. O título do cronograma foi movido para cima da grade; os quadros mantiveram suas molduras. As larguras foram ajustadas à área útil de 16 cm e os cabeçalhos repetidos nas continuações. |
| Cronograma | A fonte foi ampliada de 7,5 para 10. Meses abreviados evitam que nomes como “setembro” se partam entre linhas. Quinzenas, atividades e 37 seleções foram preservadas; a grade cabe em uma página. |
| Figuras | O texto alternativo deixou de virar uma segunda legenda visível. Foram corrigidas duas remissões decorrentes da reorganização anterior: análise estatística na Figura 1 → Seção 3.9; esquema na Figura 2 → Seção 3.3. Fluxos, modelos e dados ilustrados não foram alterados. |
| Citações | As chaves passaram a usar a sintaxe Pandoc com `@`, inclusive seis ocorrências residuais de duas chaves. Os nove itens ausentes foram importados no Zotero com autorização do autor; as duas chaves residuais já existiam na biblioteca. A geração final contém 77 campos de citação e 34 referências. |
| Paginação | O Word estabilizou as 38 entradas do sumário e das listas. A capa não entra na contagem; as páginas preliminares seguintes são contadas sem número visível e o corpo recebe numeração superior direita. |

O estilo das notas foi declarado como nativo do Word. A validação passou a resolver os identificadores realmente usados nas notas e a formatação herdada: o Word pode traduzir identificadores e omitir propriedades que coincidam com os padrões do documento. Isso foi comprovado em uma gravação efetiva, não apenas em um DOCX preparado pelo Python.

### 12.2 Resultado verificado

Entrega: [artigo_tcc_unitins_formatado_20261113.docx](./artigo_tcc_unitins_formatado_20261113.docx), distinta da exportação simples anterior.

- **19 testes de regressão aprovados**, incluindo normalização de estilos pelo Word, herança de fonte/recuo, legendas, margens, tabelas e preservação do cronograma.
- Geração, gravação e reabertura pelo Word concluídas: **51 páginas** e **38 entradas paginadas conferidas**.
- Comparação automática com a fonte e o corpo preparado: **202 parágrafos**, **77 grupos de citação**, **34 referências**, **8 tabelas**, **37 seleções**, **91 expressões matemáticas** e **7 notas** preservados.
- Imagens do cabeçalho e das figuras preservadas durante a formatação, verificadas por hash em relação ao corpo preparado.
- Conversão de controle do DOCX final e inspeção de uma renderização PDF: capa, resumos, sumário/listas, quadros com continuação, duas figuras, cronograma e referências. No cronograma, os dez meses aparecem sem quebra interna e o título está acima da grade.
- Nenhum corte temporal da revisão sistemática, alteração do protocolo ou mudança dos resultados da seleção foi aplicado nesta etapa.

### 12.3 Pendências que a exportação não deve esconder

1. **Resumo em português:** contém **259 palavras**, enquanto o manual estabelece de 150 a 250. O abstract contém **202**. A redação foi preservada para a validação da versão atual; é necessária uma redução de pelo menos nove palavras no resumo antes da versão definitiva.
2. **Depósito definitivo:** ficha catalográfica e documento de aprovação dependem dos procedimentos institucionais e da defesa; não foram inventados nem simulados.
3. **Alcance da conferência:** os controles atestam os requisitos de formatação implementados e a preservação do conteúdo. Não substituem a revisão científica, a conferência dos metadados bibliográficos pelo autor ou a homologação do orientador/biblioteca.

## 13. Parâmetros da revisão sistemática no Apêndice B

Em 13/11/2026, o Apêndice B foi reformulado a pedido do autor. A tabela anterior enumerava caminhos de pastas e arquivos do repositório, informação operacional que não explicava ao leitor os valores metodológicos efetivamente empregados. A nova versão apresenta os parâmetros principais de cada etapa — janela temporal, fonte, campos, paginação, ordenação, controles, deduplicação, modelo, lote, teto de custo, resultados da triagem e elegibilidade e campos de extração — e reproduz as seis expressões de busca com os prefixos `ti` e `abs`. O filtro temporal comum é explicitado separadamente para evitar repetição nas seis expressões. A descrição de elegibilidade mantém a distinção entre estudos de núcleo e comparadores já estabelecida na Seção 3.1.

A referência ao Apêndice B na Seção 3.1 foi ajustada para apontar aos parâmetros e expressões; o repositório `v1.0.0` permanece citado como local dos artefatos técnicos e dos dados necessários à reprodutibilidade. Assim, o apêndice fica autossuficiente quanto à configuração da busca sem sugerir que a listagem de caminhos seja o próprio método ou substituir o acesso aos dados brutos.

A atualização foi exportada em [artigo_tcc_unitins_20261113_182305.docx](./artigo_tcc_unitins_20261113_182305.docx). O gerador confirmou 52 páginas e 38 entradas paginadas; verificou a preservação de 205 parágrafos, 77 grupos de citação, 34 referências, 8 tabelas, 37 seleções do cronograma, 91 expressões matemáticas e 7 notas. A validação refere-se à formatação e à preservação do conteúdo, não substituindo a revisão científica nem resolvendo a pendência de extensão do resumo em português registrada na Seção 12.3.
