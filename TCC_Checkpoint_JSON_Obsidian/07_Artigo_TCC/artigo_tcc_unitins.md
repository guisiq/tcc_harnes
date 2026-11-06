---
title: "Modelos de linguagem compactos como escritores de memória"
subtitle: "avaliação da atualização incremental de checkpoints JSON para agentes"
author:
  - "LOPES, Guilherme Henrique Siqueira^[Acadêmico do curso de Bacharelado em Sistemas de Informação da Universidade Estadual do Tocantins (Unitins), Palmas – TO. E-mail: [inserir].]"
  - "COELHO, Alex^[Orientador. Docente do curso de Bacharelado em Sistemas de Informação da Unitins. [Nome completo e vínculo a confirmar.]]"
date: "Palmas – TO, 2026"
lang: pt-BR
# Configuração usada na etapa de geração do DOCX (filtro zotero.lua do Better BibTeX).
zotero:
  csl-style: associacao-brasileira-de-normas-tecnicas
  scannable-cite: false
---

<!--
CITAÇÕES — LEIA ANTES DE EDITAR
As citações estão em sintaxe Pandoc e usam as citation keys da biblioteca Zotero local
(campo nativo "Citation Key" do Zotero 7 / Better BibTeX):
  [@chave]          -> (AUTOR, ano)
  [@chave1; @chave2] -> (AUTOR1, ano; AUTOR2, ano)
  @chave            -> Autor (ano)
Não digite referências manualmente. Na etapa do DOCX, cada [@chave] será convertida em
campo vivo do Zotero (ADDIN ZOTERO_ITEM) e a lista de Referências será gerada pelo Zotero
com o estilo CSL "Associação Brasileira de Normas Técnicas (Português - Brasil)".
-->

**Resumo:** Agentes baseados em modelos de linguagem que recebem informações em etapas precisam manter um estado persistente, e checkpoints JSON tornam esse estado explícito e verificável. Contudo, cada reescrita do checkpoint pode omitir fatos válidos, reter informação obsoleta, inventar conteúdo ou gerar estrutura inválida. Este trabalho propõe comparar representantes compactos de três paradigmas gerativos, autoregressivo decoder-only (Qwen3-0.6B), encoder-decoder (T5Gemma B-B) e difusão em blocos (Qwen3-0.6B BD3LM), atuando exclusivamente como escritores de memória no método Generate-Update em JSON (GU-JSON). Trata-se de pesquisa aplicada, quantitativa e experimental, na qual método de atualização, schema, prompt, orçamento de 300 tokens e dados são mantidos fixos, variando apenas o modelo escritor. O cenário principal é o benchmark SUMIE, de sumarização incremental de entidades, complementado por uma amostra delimitada do FactConsolidation-SH para observar a substituição de fatos obsoletos. A avaliação combinará validade do JSON e do schema; precisão, revocação e F1 do estado; acurácias de preservação, atualização e substituição; e taxas de fatos obsoletos e alucinados, analisadas por turno e por tipo de operação, com intervalos de confiança por bootstrap. Como contribuição esperada, o estudo fornecerá um protocolo reprodutível e evidências sobre os perfis de erro de modelos compactos na manutenção de estado, sem atribuir as diferenças exclusivamente à arquitetura.

**Palavras-chave:** memória de agentes; checkpoint JSON; modelos de linguagem compactos; avaliação experimental.

**Title:** *Compact language models as memory writers: evaluating incremental updates of JSON checkpoints for agents*

**Abstract:** Language-model-based agents that receive information in steps need to maintain a persistent state, and JSON checkpoints make this state explicit and verifiable. However, each rewrite of the checkpoint may omit valid facts, retain outdated information, invent content or produce an invalid structure. This work proposes to compare compact representatives of three generative paradigms, autoregressive decoder-only (Qwen3-0.6B), encoder-decoder (T5Gemma B-B) and block diffusion (Qwen3-0.6B BD3LM), acting exclusively as memory writers in the Generate-Update in JSON (GU-JSON) method. It is an applied, quantitative and experimental study in which the update method, schema, prompt, 300-token budget and data are kept fixed, varying only the writer model. The main scenario is the SUMIE incremental entity summarization benchmark, complemented by a delimited sample of FactConsolidation-SH to observe the supersession of outdated facts. The evaluation will combine JSON and schema validity; state precision, recall and F1; preservation, update and supersession accuracies; and stale and hallucinated fact rates, analyzed by turn and by operation type, with bootstrap confidence intervals. As an expected contribution, the study will provide a reproducible protocol and evidence on the error profiles of compact models in state maintenance, without attributing the differences exclusively to architecture.

**Keywords:** agent memory; JSON checkpoint; small language models; experimental evaluation.

# 1 Introdução

Agentes baseados em modelos de linguagem vêm sendo empregados em tarefas que se desenrolam em múltiplas etapas, nas quais a informação chega de forma incremental e as decisões posteriores dependem do que foi registrado anteriormente. Nesse cenário, a capacidade de manter um estado persistente e confiável deixa de ser um detalhe de implementação e passa a condicionar a confiabilidade do agente. Trabalhos recentes associam a consciência de estado e a memória à robustez de fluxos agênticos extensos [@muhoberacStateMemoryAll2025] e propõem avaliar a memória de agentes justamente sob interações incrementais e de longo prazo [@huEvaluatingMemoryLLM2025; @wuLongMemEvalBenchmarkingChat2024; @maharanaEvaluatingVeryLongTerm2024].

Uma estratégia para lidar com esse problema consiste em condensar as interações anteriores em uma representação persistente estruturada, atualizada a cada nova observação. Em sumarização incremental com memória limitada, @hwangEnhancingIncrementalSummarization2024 relatam vantagem da atualização sobre representações em JSON em relação à atualização sobre texto livre. Um checkpoint JSON torna explícitos os campos do estado e permite compará-lo automaticamente com referências estruturadas. Entretanto, cada reescrita do checkpoint é também uma oportunidade de erro: o componente que o atualiza pode omitir fatos ainda válidos, manter informação obsoleta, alterar valores indevidamente, inventar conteúdo sem suporte ou produzir uma estrutura sintaticamente inválida.

Esse problema tem vínculo direto com a área de Sistemas de Informação. O checkpoint funciona como o repositório de informação do qual o agente depende para agir, e sua utilidade é determinada por atributos de qualidade da informação como exatidão, completude, atualidade e consistência. Avaliar o componente que escreve esse repositório é, portanto, avaliar a qualidade da informação mantida por um sistema baseado em inteligência artificial. Soma-se a isso uma dimensão organizacional: modelos de linguagem compactos podem ser executados localmente, com menor custo e maior controle sobre os dados, o que os torna candidatos a componentes especializados de sistemas agênticos [@luSmallLanguageModels2025; @sharmaSmallLanguageModels2025].

A literatura relacionada oferece bases para cada parte do problema, mas de forma fragmentada. Há estudos sobre representação estruturada da memória [@zengStructuralMemoryLLM2024; @jayalathPRISMEfficientLongRange2025; @yuenIntrinsicMemoryAgents2025], sobre métodos de atualização incremental [@hwangEnhancingIncrementalSummarization2024], sobre avaliação de memória em agentes [@hwangSUMIESyntheticBenchmark2025; @huEvaluatingMemoryLLM2025] e sobre geração de saídas estruturadas [@gengJSONSchemaBenchRigorousBenchmark2025]. Contudo, a evidência direta sobre o método Generate-Update em JSON (GU-JSON) foi obtida com modelos de grande porte, e os estudos que comparam paradigmas gerativos distintos, como o autoregressivo e o de difusão, tratam de outras tarefas e escalas [@luBitterLessonDiffusion2026]. Na busca bibliográfica realizada até o momento, não foi identificada uma comparação controlada entre representantes compactos de paradigmas gerativos diferentes atuando exclusivamente como escritores (*memory writers*) do mesmo checkpoint JSON. Essa lacuna é formulada de maneira operacional e permanece sujeita à confirmação pela revisão focal descrita na seção 3.2.

Diante disso, este trabalho é orientado pela seguinte pergunta de pesquisa: como representantes compactos de três paradigmas gerativos diferem na qualidade de atualizações GU-JSON no SUMIE, sob schema e limite de memória fixos?

O objetivo geral é comparar representantes compactos autoregressivo decoder-only, encoder-decoder e de difusão como escritores de memória GU-JSON no cenário focal do SUMIE, mantendo fixos o schema, o orçamento de memória e o protocolo experimental. Para alcançá-lo, definem-se os seguintes objetivos específicos:

a) medir a validade sintática do JSON e a conformidade com o schema dos checkpoints produzidos por cada escritor;
b) comparar a precisão, a revocação e o F1 do estado ao longo das atualizações do SUMIE;
c) analisar a preservação, a adição e a atualização de informação por tipo de operação;
d) verificar, em uma amostra delimitada do FactConsolidation-SH, o comportamento dos escritores na substituição de fatos obsoletos (*supersession*).

A relevância do estudo manifesta-se em três dimensões. Do ponto de vista científico, propõe um protocolo que separa a conformidade estrutural da fidelidade semântica do estado e examina sua evolução por turno e por tipo de operação. Do ponto de vista prático, produz evidências para a escolha de modelos compactos como componentes de memória em agentes executados localmente. Do ponto de vista metodológico, privilegia a reprodutibilidade, com artefatos versionados e preservação das saídas brutas. O estudo não pretende determinar um método de escrita universalmente superior nem atribuir as diferenças observadas exclusivamente à arquitetura dos modelos.

Além desta introdução, o artigo está organizado da seguinte forma: a seção 2 apresenta a fundamentação sobre memória persistente em agentes e os trabalhos relacionados; a seção 3 descreve os materiais e métodos; a seção 4 apresenta os resultados esperados e o cronograma; e a seção 5 traz as considerações finais.

# 2 Memória persistente em agentes baseados em modelos de linguagem

Esta seção organiza a fundamentação em cinco eixos: a representação estruturada da memória, o método de atualização incremental, a avaliação de memória, a geração de saídas estruturadas e os paradigmas gerativos dos modelos compactos. Ao final, os trabalhos mais próximos são comparados com a proposta.

## 2.1 Representação estruturada da memória

@zengStructuralMemoryLLM2024 compararam diferentes estruturas de memória, como trechos de texto (*chunks*), triplas de conhecimento, fatos atômicos, resumos e uma memória mista, combinadas a estratégias de recuperação, em quatro tarefas e seis conjuntos de dados. Os autores relatam vantagens dependentes da tarefa: trechos e resumos favorecem contextos longos, triplas e fatos atômicos favorecem raciocínio relacional e precisão, e a memória mista apresenta o comportamento mais equilibrado. O estudo contextualiza a escolha da representação, mas trata de recuperação de informação, e não da fidelidade de um estado reescrito a cada etapa.

Mais próximos do objeto deste trabalho estão os sistemas que mantêm uma memória estruturada persistente e a atualizam incrementalmente. O PRISM mantém uma memória tipada, organizada por um schema hierárquico, e a atualiza por meio de operações de caminho e valor validadas e aplicadas programaticamente [@jayalathPRISMEfficientLongRange2025]. Os Intrinsic Memory Agents atualizam a memória contextual de cada agente a partir da memória anterior e da saída mais recente, comparando templates manuais, genéricos e gerados pelo próprio modelo; na revisão de 2026, a variante genérica não exige JSON, e templates genéricos ou gerados superam os manuais em vários testes [@yuenIntrinsicMemoryAgents2025]. No SciBORG, agentes são acoplados a uma memória baseada em autômatos finitos para rastrear estado persistente em fluxos científicos extensos [@muhoberacStateMemoryAll2025]. Já a Chain-of-Memory concentra-se na construção da memória e no raciocínio sobre fragmentos recuperados [@xuChainofMemoryLightweightMemory2026].

Em conjunto, esses trabalhos mostram que a estrutura da memória e o método de escrita são decisões distintas. Eles fornecem precedentes para memórias estruturadas atualizadas incrementalmente, mas não demonstram a superioridade de um schema fixo nem avaliam a fidelidade de cada transição de estado. Neste trabalho, o schema fixo é uma escolha de controle experimental, e não uma tese sobre a melhor representação.

## 2.2 Atualização incremental e o método Generate-Update em JSON

@hwangEnhancingIncrementalSummarization2024 investigaram como manter resumos incrementais com memória limitada, comparando as estratégias Generate-Once (GO), Generate-Update (GU) e Generate-Merge (GM) em representações textuais e em JSON, nos conjuntos SUMIE e BooookScore, com os modelos Gemini Ultra e Gemini Pro. Sob memória limitada, a variante GU em JSON superou a variante GU em texto. Os autores também propuseram o Chain-of-Key em JSON (CoK-JSON), que atualiza caminhos específicos da estrutura e obteve resultados superiores às estratégias de base comparadas.

No GU-JSON, a cada nova observação o escritor recebe o schema, o checkpoint corrente e a observação, e gera o checkpoint completo atualizado, conforme a Equação 1:

$$
M_t = G\left(S,\ M_{t-1},\ O_t\right) \qquad (1)
$$

em que $S$ é o schema, $M_{t-1}$ é o checkpoint anterior, $O_t$ é a nova observação, $G$ é o modelo escritor e $M_t$ é o checkpoint resultante.

Esse método não é adotado por ser o melhor disponível, já que o próprio estudo de origem relata desempenho superior do CoK-JSON. Ele é adotado por ser uma estratégia publicada, simples e replicável, que concentra toda a atualização no modelo escritor. Diferentemente de abordagens com operações programáticas, como o PRISM, o GU-JSON dispensa algoritmo de mesclagem, escolha de caminhos, recuperação de informação e mecanismos externos de resolução de conflito. Essa característica permite variar apenas o escritor, sem variar simultaneamente o algoritmo de atualização.

## 2.3 Avaliação de memória e de atualização de conhecimento

O SUMIE é um benchmark sintético de sumarização incremental de entidades, no qual parágrafos sobre uma entidade chegam em sequência e devem ser incorporados a um resumo de atributos e valores [@hwangSUMIESyntheticBenchmark2025]. O conjunto contém repetição, informação nova, conflito e distração, e suas anotações são feitas por parágrafo. Um aspecto decisivo para este trabalho é a política de atualização do benchmark: o prompt de atualização publicado preserva atributos e valores anteriores e integra perspectivas conflitantes, de modo que uma opinião divergente não invalida automaticamente a anterior. A avaliação original combina correspondência exata com avaliação semântica de evidências por modelo de linguagem, e os autores relatam perfis distintos de precisão e revocação entre os modelos avaliados.

O MemoryAgentBench propõe avaliar agentes de memória por meio de interações incrementais de múltiplos turnos, organizadas em quatro competências, entre elas o esquecimento seletivo [@huEvaluatingMemoryLLM2025]. Seu subconjunto FactConsolidation adota uma regra temporal explícita: o fato mais recente invalida o anterior. O LongMemEval inclui a atualização de conhecimento e o raciocínio temporal entre as habilidades avaliadas em assistentes conversacionais [@wuLongMemEvalBenchmarkingChat2024], e o LoCoMo examina a memória em conversas muito longas, com centenas de turnos distribuídos em diversas sessões [@maharanaEvaluatingVeryLongTerm2024].

Esses benchmarks avaliam sobretudo respostas finais, e não a fidelidade interna do estado mantido. Além disso, adotam políticas diferentes: no SUMIE, preservar perspectivas conflitantes faz parte da tarefa; no FactConsolidation, substituir o fato temporalmente obsoleto é o comportamento esperado. Este trabalho adapta essa motivação para a inspeção direta do checkpoint e trata as duas políticas como distintas, sem atribuir diferenças entre conjuntos de dados apenas ao tipo de operação.

## 2.4 Geração estruturada: validade sintática e conformidade com schema

A produção de saídas estruturadas por modelos de linguagem envolve requisitos que podem ser verificados separadamente. O JSONSchemaBench avalia a conformidade de saídas com JSON Schemas reais de diferentes complexidades e compara frameworks de decodificação restrita [@gengJSONSchemaBenchRigorousBenchmark2025]. Antes dele, @gengGrammarConstrainedDecodingStructured2023 mostraram que gramáticas formais podem restringir a decodificação em tarefas estruturadas de processamento de linguagem natural sem ajuste fino. Para modelos de difusão, @mundlerConstrainedDecodingDiffusion2025 propõem decodificação restrita por gramáticas livres de contexto, mitigando falhas sintáticas, e @khanalAgentsDiffusionEnhancing2026 combinam modelos de difusão a aprendizado por reforço multiagente para gerar dados estruturados.

Duas consequências orientam o protocolo deste trabalho. A primeira é que JSON válido e conforme ao schema não garante memória correta: um checkpoint pode ser estruturalmente impecável e, ainda assim, perder fatos ou reter informação obsoleta. Por isso, métricas estruturais e semânticas são tratadas separadamente. A segunda é que mecanismos de decodificação restrita não estão igualmente disponíveis para os três paradigmas e acrescentariam uma variável ao experimento. Assim, o experimento principal é conduzido apenas por instrução (*prompt-only*), sem decodificação restrita.

## 2.5 Paradigmas gerativos e modelos de linguagem compactos

Os modelos autoregressivos decoder-only geram texto token a token, da esquerda para a direita, condicionando cada token aos anteriores. A família Qwen3 é um exemplo recente, com modelos de diversas escalas, inclusive compactos [@yangQwen3TechnicalReport2025]. Os modelos encoder-decoder separam a leitura da entrada, feita por um codificador com atenção bidirecional, da geração da saída, feita por um decodificador. O T5Gemma obtém modelos desse tipo pela adaptação de modelos decoder-only pré-treinados, buscando melhor equilíbrio entre qualidade e eficiência [@zhangEncoderDecoderGemmaImproving2025]. A transformação de estado anterior e nova observação em novo estado é naturalmente compatível com esse formato de sequência para sequência.

Os modelos de linguagem por difusão geram texto por remoção iterativa de ruído sobre posições mascaradas, podendo refinar vários tokens em paralelo. @nieScalingMaskedDiffusion2024 estudaram o escalonamento de modelos de difusão mascarada em texto, e @gongScalingDiffusionLanguage2024 mostraram que modelos de difusão podem ser obtidos pela adaptação de modelos autoregressivos pré-treinados. A difusão em blocos (BD3LM) interpola os dois paradigmas: gera os blocos sequencialmente, de forma autoregressiva, e aplica difusão dentro de cada bloco [@arriolaBlockDiffusionInterpolating2025]. Quanto ao uso em agentes, @luBitterLessonDiffusion2026 avaliaram modelos de difusão de 7 a 8 bilhões de parâmetros e encontraram resultados dependentes da tarefa: dificuldades em controle e em chamadas de ferramentas, mas desempenho competitivo na sumarização de memória textual. Esses resultados, obtidos com modelos maiores e memória em texto livre, não permitem antecipar o desempenho de um escritor compacto de checkpoints JSON.

Os modelos de linguagem compactos (*small language models*, SLMs) têm atraído interesse por tornarem a inteligência artificial mais acessível, econômica e eficiente, inclusive em dispositivos locais [@luSmallLanguageModels2025]. Há também a posição de que modelos pequenos são suficientes, e muitas vezes preferíveis, em cargas agênticas que exigem precisão sob restrições de schema e de API [@sharmaSmallLanguageModels2025]. Por outro lado, a execução em hardware modesto frequentemente depende de quantização, e modelos menores tendem a sofrer maiores perdas de acurácia sob quantização agressiva [@leeExploringTradeOffsQuantization2025]. Essas observações justificam avaliar modelos compactos como componentes especializados, desde que a precisão numérica e as condições de execução sejam controladas e registradas.

## 2.6 Trabalhos relacionados

O Quadro 1 sintetiza os trabalhos mais próximos da proposta segundo cinco critérios: a representação da memória, o mecanismo de atualização, os modelos e sua escala, o objeto da avaliação e a existência de comparação entre paradigmas gerativos. A última linha posiciona este trabalho em relação aos demais.

**Quadro 1 – Comparação entre trabalhos relacionados e a proposta**

| Trabalho | Representação da memória | Atualização | Modelos e escala | Objeto da avaliação | Compara paradigmas gerativos |
|---|---|---|---|---|---|
| @hwangEnhancingIncrementalSummarization2024 | Texto e JSON | GO, GU, GM e CoK, executados pelo próprio modelo | Gemini Ultra e Gemini Pro (grande porte) | Qualidade de resumos incrementais (SUMIE e BooookScore) | Não |
| @hwangSUMIESyntheticBenchmark2025 | Atributos e valores de entidades | Atualização com preservação de perspectivas | Diversos modelos de linguagem de grande porte | Precisão, revocação e F1 de atributos, com avaliação de evidências por modelo de linguagem | Não |
| @jayalathPRISMEfficientLongRange2025 | Memória tipada hierárquica | Operações de caminho e valor aplicadas programaticamente | Modelos de contexto curto | Raciocínio de longo alcance (tarefa final) | Não |
| @yuenIntrinsicMemoryAgents2025 | Memória contextual por agente; JSON em algumas variantes | Reescrita a partir da memória anterior e da saída recente | Modelos de linguagem em sistemas multiagente | Desempenho do sistema multiagente | Não |
| @zengStructuralMemoryLLM2024 | Trechos, triplas, fatos atômicos, resumos e memória mista | Construção e recuperação | Modelos de linguagem de propósito geral | Desempenho em quatro tarefas e seis conjuntos de dados | Não |
| @huEvaluatingMemoryLLM2025 | Diversos sistemas de memória | Interações incrementais de múltiplos turnos | Diversos agentes de memória | Respostas finais em quatro competências | Não |
| @luBitterLessonDiffusion2026 | Texto livre e chamadas de ferramentas | Não se aplica | Modelos de difusão e autoregressivos de 7 a 8 bilhões de parâmetros | Desempenho em fluxos agênticos | Sim, sem checkpoint JSON |
| @gengJSONSchemaBenchRigorousBenchmark2025 | JSON Schema | Não se aplica | Frameworks de decodificação restrita | Conformidade estrutural | Não |
| **Proposta deste trabalho** | Checkpoint JSON de schema fixo | GU-JSON, com reescrita integral pelo escritor | Três representantes de cerca de 0,6 bilhão de parâmetros (autoregressivo, encoder-decoder e difusão) | Fidelidade do estado por transição, turno e operação, além da validade estrutural | Sim, sob protocolo controlado |

Fonte: elaborado pelo autor (2026).

Como mostra o Quadro 1, os trabalhos que fundamentam o GU-JSON utilizam modelos de grande porte; os que tratam de memória estruturada empregam mecanismos de atualização diferentes da reescrita integral; os benchmarks de memória avaliam respostas finais; e o estudo que compara paradigmas gerativos em agentes não examina checkpoints estruturados. A proposta diferencia-se por manter fixos o método, o schema, os dados e o orçamento, variando apenas o modelo escritor, e por avaliar diretamente a fidelidade do estado produzido a cada transição.

# 3 Materiais e métodos

Esta seção descreve o procedimento adotado para responder à pergunta de pesquisa. O desenho foi organizado de modo que cada objetivo específico corresponda a pelo menos um experimento, a um artefato e a evidências mensuráveis, conforme sintetizado na seção 3.11.

## 3.1 Caracterização da pesquisa

Quanto à natureza, a pesquisa é aplicada, pois busca gerar conhecimento para a escolha e a avaliação de componentes de memória em sistemas agênticos. Quanto à abordagem, é quantitativa, baseada em métricas calculadas automaticamente sobre os checkpoints produzidos. Quanto aos objetivos, é descritiva e comparativa, com hipóteses de trabalho explícitas. Quanto aos procedimentos, combina pesquisa bibliográfica e experimento computacional controlado, no qual uma única variável independente é manipulada e as demais condições são mantidas constantes. A pesquisa não envolve participantes humanos e utiliza apenas dados e modelos publicamente disponíveis, observadas as respectivas licenças.

## 3.2 Procedimento de revisão da literatura

A revisão adota uma busca estruturada, sem constituir uma revisão sistemática completa. Os conceitos de mapeamento sistemático orientam a classificação das contribuições e a identificação de lacunas [@petersenSystematicMappingStudies2008; @petersenGuidelinesConductingSystematic2015], e a distinção entre mapeamento e revisão sistemática da literatura delimita o alcance das conclusões [@kitchenhamSystematicLiteratureReviews2010a]. O procedimento compreende as seguintes etapas:

a) definição de um conjunto inicial de artigos-semente: o estudo de Hwang et al. sobre sumarização incremental estruturada, o SUMIE, o MemoryAgentBench, o PRISM, os Intrinsic Memory Agents, os relatórios técnicos do Qwen3 e do T5Gemma, o trabalho sobre difusão em blocos e, como contrapontos, os estudos de Lu et al. e de Mündler et al. sobre difusão;
b) busca por expressões conceituais que combinam agentes e memória estruturada com atualização incremental, por exemplo `("LLM agent" OR "language model agent") AND memory AND (structured OR JSON OR state) AND (update OR incremental OR consolidation)`, além de expressões sobre modelos de difusão e modelos encoder-decoder aplicados à geração estruturada, adaptadas à sintaxe de cada base consultada;
c) aplicação de critérios de inclusão, que abrangem trabalhos sobre memória persistente ou estruturada em agentes, atualização incremental de estado, avaliação de memória, geração estruturada em JSON ou caracterização dos paradigmas avaliados, com texto completo acessível; e de critérios de exclusão, que afastam trabalhos centrados em recuperação aumentada ou bancos vetoriais sem atualização de estado, em ajuste fino extenso ou sem descrição suficiente do método;
d) expansão por *snowballing* para trás, examinando as referências dos artigos-semente, e para frente, examinando os trabalhos que os citam [@wohlinGuidelinesSnowballingSystematic2014], encerrada quando duas iterações consecutivas não acrescentarem estudos primários relevantes;
e) extração padronizada de título, ano, veículo, versões de preprint e de publicação, modelos e escala, tipo de memória, método de atualização, conjunto de dados, métricas, disponibilidade de código, licenças, relação com as perguntas de pesquisa, limitações e tipo de evidência, se direta, indireta ou contraponto.

As referências são gerenciadas no Zotero, priorizando-se a versão publicada sobre o preprint e registrando-se separadamente as datas de preprint, revisão e publicação. Uma auditoria bibliográfica preliminar, concluída em novembro de 2026, verificou metadados, versões e o método das fontes centrais; os registros de cada busca serão preservados para permitir a reprodução do procedimento.

## 3.3 Desenho experimental e variáveis

O experimento manipula uma única variável independente, o modelo escritor, e mantém constantes todas as demais condições, conforme o Quadro 2.

**Quadro 2 – Variáveis do experimento**

| Tipo | Variável | Operacionalização |
|---|---|---|
| Independente | Modelo escritor | Qwen3-0.6B (autoregressivo decoder-only); T5Gemma B-B PrefixLM-IT (encoder-decoder); Qwen3-0.6B Diffusion BD3LM (difusão em blocos) |
| Controlada | Método de atualização | GU-JSON, com reescrita integral do checkpoint |
| Controlada | Schema | `{"state": {"chave": "valor"}}`, idêntico para todos os escritores e exemplos |
| Controlada | Prompt | Mesmo prompt-base, sem exemplos (*zero-shot*), em inglês |
| Controlada | Orçamento de saída | 300 tokens |
| Controlada | Contexto de entrada | Até 8 mil tokens |
| Controlada | Dados | Mesmas sequências, na mesma ordem, com os mesmos estados anteriores e estados esperados |
| Controlada | Decodificação | Política determinística fixa e documentada, sem decodificação restrita |
| Dependente | Qualidade estrutural | Validade do JSON e conformidade com o schema |
| Dependente | Qualidade do estado | Precisão, revocação e F1 do estado; taxa de alucinação |
| Dependente | Qualidade da transição | Acurácias de preservação, atualização e substituição; taxa de fatos obsoletos |

Fonte: elaborado pelo autor (2026).

A pergunta principal (RQ1) indaga como os representantes compactos diferem na qualidade das atualizações GU-JSON no SUMIE, com schema e limite de 300 tokens fixos. As perguntas secundárias examinam como as diferenças de fidelidade variam ao longo da sequência de atualizações (RQ2); quais diferenças aparecem na adição, na integração e na preservação de informação, respeitando a política do SUMIE de manter perspectivas conflitantes (RQ3); e quais padrões observados no SUMIE se mantêm na amostra de contraste do FactConsolidation-SH, focada em substituição (RQ4).

Duas hipóteses de trabalho orientam a análise. A H1 estabelece que, sob GU-JSON, schema e orçamento fixos, os modelos selecionados apresentam diferenças mensuráveis na preservação do estado antigo e na incorporação de informação nova, sem previsão de ordenação entre eles. A H2, de caráter exploratório, estabelece que as diferenças entre escritores podem ser mais visíveis quando a informação nova substitui uma anterior do que em simples adições. Como a comparação entre SUMIE e FactConsolidation-SH também muda o conjunto de dados, ela não isola o efeito da operação, e a H2 permanece exploratória.

## 3.4 Método de memória, schema e prompt

O experimento aplica o GU-JSON conforme a Equação 1: a cada transição, o escritor recebe o schema, o checkpoint anterior e a nova observação, e deve devolver apenas o checkpoint completo atualizado. O schema é mínimo e único, `{"state": {"chave": "valor"}}`, e os atributos de ambos os conjuntos de dados são convertidos em pares atributo-valor dentro de `state`, sem campos específicos por conjunto. Essa representação é uma escolha de controle, cuja adequação aos estados acumulados do SUMIE será verificada no piloto, sem reduzir automaticamente opiniões conflitantes a um único valor.

O prompt-base, apresentado no Apêndice A, não contém informação específica de nenhuma arquitetura e explicita cinco regras: preservar a informação ainda válida; aplicar a informação introduzida pela nova observação; substituir fatos apenas quando a observação ou a tarefa estabelecerem explicitamente sua invalidade, preservando opiniões divergentes; não inventar fatos sem suporte; e respeitar o schema, retornando somente o objeto JSON completo. O orçamento de saída é fixo em 300 tokens, inspirado no cenário de memória limitada de @hwangEnhancingIncrementalSummarization2024, sem que se alegue replicação idêntica de sua contagem de tokens.

Os adaptadores de cada modelo podem ajustar apenas aspectos técnicos da interface, como o template de conversa, os marcadores especiais e os parâmetros de geração, que serão documentados, sem alterar semanticamente o prompt. O modo de raciocínio explícito do Qwen3 será fixado e registrado, para que o raciocínio adicional não consuma o orçamento destinado ao JSON. A configuração inicial não utiliza exemplos; caso um escritor falhe sistematicamente em compreender o formato, poderá ser avaliado um único exemplo, idêntico para todos os escritores, documentado como nova condição.

## 3.5 Dados e preparação das transições

O SUMIE é o conjunto de dados principal, por corresponder diretamente ao cenário em que o GU-JSON foi avaliado sob memória limitada.^[Disponível em: https://github.com/google-deepmind/sumie. O repositório é identificado como Apache-2.0; a revisão utilizada será registrada.] Cada etapa de uma sequência será convertida em uma transição composta pelo estado anterior, pela observação e pelo estado esperado. Como os dados públicos fornecem anotações por parágrafo, e não checkpoints acumulados nem rótulos de operação prontos, a construção dos estados esperados, a representação de múltiplas perspectivas, a política de canonicalização dos valores e os rótulos de operação (ADD, UPDATE e PRESERVE) serão documentados e validados no piloto, antes da coleta principal. Também será verificado se os estados de referência cabem no orçamento de 300 tokens, de modo que uma eventual impossibilidade de retenção integral não seja contabilizada como falha de preservação do escritor.

O contraste exploratório utiliza uma amostra do FactConsolidation-SH, subconjunto do MemoryAgentBench, restrita a transições que envolvem substituição de fatos.^[Disponível em: https://huggingface.co/datasets/ai-hyz/MemoryAgentBench.] Os critérios e o tamanho da amostra serão fixados e documentados após a verificação da distribuição das operações e antes da execução dos escritores. Como o benchmark original avalia respostas finais, a construção dos estados esperados e dos rótulos de substituição (SUPERSEDE) é uma adaptação deste trabalho. A licença dos dados será confirmada na revisão efetivamente utilizada, pois há divergência entre a indicação do cartão do conjunto de dados e a do artigo.

Ficam fora da coleta os conjuntos FactConsolidation-MH, LoCoMo, LongMemEval e BooookScore, que ampliariam o domínio e as tarefas sem testar diretamente a pergunta principal.

## 3.6 Modelos avaliados

Os modelos foram selecionados segundo os seguintes critérios: possibilidade de execução local, disponibilidade pública, escala próxima entre si, adequação à geração de texto, representação clara de paradigmas distintos e, preferencialmente, ajuste por instruções. Os representantes são:

a) Qwen3-0.6B, representante autoregressivo decoder-only e referência de comparação, com licença Apache-2.0 [@yangQwen3TechnicalReport2025];^[Disponível em: https://huggingface.co/Qwen/Qwen3-0.6B.]
b) T5Gemma B-B PrefixLM-IT, representante encoder-decoder ajustado por instruções, de escala aproximada de 0,6 bilhão de parâmetros, cujo acesso exige o aceite dos termos de uso do Gemma [@zhangEncoderDecoderGemmaImproving2025];^[Disponível em: https://huggingface.co/google/t5gemma-b-b-prefixlm-it.]
c) Qwen3-0.6B Diffusion BD3LM, representante de difusão em blocos [@arriolaBlockDiffusionInterpolating2025], cujo repositório, checkpoint exato e interface recomendada serão confirmados no início da implementação.

Os três modelos diferem também em dados e objetivos de treinamento, tokenizador e pós-treinamento. Por isso, as conclusões referem-se aos representantes avaliados, e não aos paradigmas em abstrato. Caso algum modelo se mostre incompatível com o ambiente local durante a validação, a seleção será revista e a alteração documentada.

## 3.7 Ambiente de execução e harness experimental

A execução dos escritores ocorrerá em um notebook Lenovo IdeaPad Gaming 3i, com processador Intel Core i5 de 10ª geração, 24 GB de memória RAM e placa de vídeo GeForce GTX 1650, cuja memória de vídeo disponível será confirmada antes da coleta. Um segundo computador, com processador Intel Core i5 e 16 GB de RAM, será utilizado na preparação dos dados, na validação de schema, no cálculo das métricas e na análise. A precisão numérica e eventual quantização de cada modelo serão registradas e mantidas tão homogêneas quanto possível, dado que modelos pequenos são sensíveis à quantização agressiva [@leeExploringTradeOffsQuantization2025].

Como a confiabilidade de agentes depende também da infraestrutura que envolve o modelo [@AgentHarnessEngineering2026], será construído um harness experimental que isola o escritor como único componente variável. O fluxo de cada transição segue as etapas: (i) um adaptador de conjunto de dados converte os dados de origem em transições; (ii) um construtor de prompt preenche o prompt-base com o schema, o estado anterior e a observação; (iii) um adaptador de escritor, com interface comum aos três modelos, recebe esses elementos e o orçamento de saída e devolve o texto gerado; (iv) a saída bruta é registrada antes de qualquer processamento; (v) um parser JSON verifica a validade sintática; (vi) um validador verifica a conformidade com o schema; (vii) um avaliador de estado compara o checkpoint produzido com o estado anterior e o estado esperado; e (viii) os resultados são armazenados por amostra, turno e escritor.

Para cada transição serão registrados o identificador do experimento, o conjunto de dados, a amostra, o turno, o escritor, a semente, o hash e o texto do prompt, a saída bruta, o JSON interpretado, o estado esperado e eventuais erros. A reprodutibilidade será assegurada pelo registro das versões das bibliotecas e do commit do harness, pelo uso dos mesmos exemplos para todos os escritores e pela separação entre os resultados do piloto e os da análise confirmatória. Nenhuma saída será corrigida silenciosamente: a validade do JSON bruto será distinguida de eventual JSON reparado, e o parser e o validador serão cobertos por testes unitários.

## 3.8 Métricas de avaliação

Para o cálculo das métricas semânticas, cada checkpoint será convertido em unidades comparáveis do tipo caminho e valor, por exemplo `("state.preco", "290")`. A ordem das chaves é desconsiderada, e a normalização dos valores será mínima e definida antes da coleta, de modo a não penalizar paráfrases corretas nem aceitar valores incorretos. Como a avaliação original do SUMIE combina correspondência exata e avaliação semântica por modelo de linguagem, o F1 de estado aqui proposto é uma adaptação determinística, e seus valores não são diretamente comparáveis aos publicados.

A precisão, a revocação e o F1 do estado são calculados conforme as Equações 2 a 4, em que $TP$ corresponde aos pares corretos presentes no checkpoint, $FP$ aos pares presentes, mas incorretos ou sem correspondência, e $FN$ aos pares esperados ausentes:

$$
P = \frac{TP}{TP + FP} \qquad (2)
$$

$$
R = \frac{TP}{TP + FN} \qquad (3)
$$

$$
F_1 = \frac{2PR}{P + R} \qquad (4)
$$

As acurácias de atualização ($UA$) e de preservação ($PA$) são definidas pelas Equações 5 e 6:

$$
UA = \frac{\text{modificações esperadas aplicadas corretamente}}{\text{modificações esperadas}} \qquad (5)
$$

$$
PA = \frac{\text{campos inalterados preservados corretamente}}{\text{campos que deveriam permanecer inalterados}} \qquad (6)
$$

O Quadro 3 reúne o conjunto completo de métricas e o domínio de aplicação de cada uma.

**Quadro 3 – Métricas de avaliação**

| Métrica | Definição | Aplicação |
|---|---|---|
| Validade do JSON (*JSON Validity*) | Percentual de saídas interpretáveis por um parser JSON padrão, sem reparo | Todas as transições |
| Conformidade com o schema (*Schema Validity*) | Percentual de saídas que respeitam campos, tipos e cardinalidades do schema | Todas as transições |
| Precisão do estado (*State Precision*) | Fração dos pares persistidos que estão corretos (Equação 2) | Todas as transições |
| Revocação do estado (*State Recall*) | Fração dos pares esperados presentes no checkpoint (Equação 3) | Todas as transições |
| F1 do estado (*State F1*) | Média harmônica entre precisão e revocação (Equação 4); métrica primária | Todas as transições |
| Acurácia de preservação (*Preservation Accuracy*) | Fração dos campos que deveriam permanecer inalterados e foram preservados (Equação 6); métrica primária | Transições com operação PRESERVE |
| Acurácia de atualização (*Update Accuracy*) | Fração das modificações esperadas aplicadas corretamente (Equação 5), reportada separadamente para ADD e UPDATE | Transições com operações ADD ou UPDATE |
| Acurácia de substituição (*Supersession Accuracy*) | Percentual de valores obsoletos corretamente substituídos; métrica primária | Somente transições com invalidação explícita |
| Taxa de fatos obsoletos (*Stale Fact Rate*) | Proporção de fatos que deveriam ter sido invalidados e permanecem no checkpoint | Somente transições com invalidação explícita |
| Taxa de alucinação (*Hallucination Rate*) | Proporção de pares sem suporte na observação nem no estado anterior | Todas as transições |

Fonte: elaborado pelo autor (2026).

Para reduzir o risco de seleção posterior de resultados favoráveis, as métricas primárias são declaradas antecipadamente: F1 do estado, acurácia de preservação e acurácia de substituição. No SUMIE, a preservação de perspectivas divergentes válidas não é contabilizada como fato obsoleto.

## 3.9 Fases experimentais

O experimento será conduzido em quatro fases sequenciais:

a) Fase 0 (verificação inicial): execução de 10 a 20 transições construídas manualmente para validar o carregamento dos modelos no ambiente local, o parser, o schema, o prompt e o formato de saída. Essa fase é realizada ainda no TCC I, para confirmar a viabilidade do ambiente, e seus resultados não integram a análise;
b) Fase 1 (piloto no SUMIE): execução com aproximadamente 25 entidades para confirmar a adaptação do conjunto de dados, a construção dos estados acumulados, a canonicalização, a representação de perspectivas conflitantes sob 300 tokens e o cálculo das métricas. Os problemas de implementação identificados serão corrigidos antes da coleta confirmatória, e os resultados do piloto não serão misturados aos da análise principal;
c) Fase 2 (experimento principal no SUMIE): execução dos três escritores nas mesmas sequências de sumarização incremental, com registro completo por transição;
d) Fase 3 (contraste de substituição): execução dos três escritores na amostra previamente delimitada do FactConsolidation-SH, tratada como contraste exploratório, e não como avaliação geral de memória de agentes.

Em caso de atraso, a ordem de prioridade é manter o SUMIE, os três escritores, as métricas longitudinais, o orçamento fixo e o registro para reprodutibilidade, reduzindo ou removendo a amostra do FactConsolidation-SH antes de qualquer ampliação de escopo.

## 3.10 Plano de análise

As métricas serão calculadas e armazenadas por amostra, por turno e por operação, nunca apenas como médias agregadas. A análise compreenderá: (i) a qualidade agregada por escritor no SUMIE; (ii) a qualidade por turno, com curvas de F1, de acurácia de preservação e de taxa de fatos obsoletos ao longo da sequência; (iii) a qualidade por operação no SUMIE, separando ADD, UPDATE e PRESERVE; e (iv) a análise separada da amostra do FactConsolidation-SH.

Serão reportadas médias e medianas, com intervalos de confiança de 95% estimados por bootstrap, reamostrando entidades para preservar a dependência entre transições de uma mesma sequência. Como os três escritores processam os mesmos casos, as comparações serão feitas por diferenças pareadas, acompanhadas de tamanho de efeito quando aplicável. Se a geração for determinística, repetições idênticas não acrescentam variância; havendo estocasticidade inevitável, sementes adicionais serão executadas em um subconjunto. A ausência de diferença detectada será interpretada como ausência de evidência sob o protocolo e a precisão estatística obtida, e não como prova de equivalência entre os modelos.

## 3.11 Relação entre objetivos, experimentos e evidências

O Quadro 4 relaciona cada objetivo específico ao artefato que o viabiliza, ao experimento que o executa, à evidência produzida e à métrica e ao critério de análise.

**Quadro 4 – Matriz de rastreabilidade entre objetivos, experimentos e evidências**

| Objetivo específico | Artefato | Experimento | Evidência | Métrica e critério |
|---|---|---|---|---|
| a) Medir a validade do JSON e a conformidade com o schema | Parser JSON, validador de schema e registro das saídas brutas | Fases 2 e 3 (artefato validado na Fase 0) | Proporção de saídas válidas por escritor, turno e conjunto de dados; tipologia das falhas estruturais | Validade do JSON e conformidade com o schema, com IC de 95% e diferenças pareadas, sem reparo das saídas |
| b) Comparar precisão, revocação e F1 do estado ao longo das atualizações | Estados esperados acumulados do SUMIE e avaliador de estado com canonicalização validada | Fase 2, após o piloto da Fase 1 | Resultados agregados por escritor e curvas de F1 por turno | Precisão, revocação e F1 do estado (primária), com IC de 95% e diferenças pareadas |
| c) Analisar preservação, adição e atualização por operação | Rótulos de operação ADD, UPDATE e PRESERVE validados | Fase 2, com análise estratificada por operação | Acurácias por operação e escritor; curva de preservação por turno | Acurácia de preservação (primária), acurácia de atualização e taxa de alucinação, com IC de 95% |
| d) Verificar o comportamento em substituição de fatos | Amostra delimitada e documentada do FactConsolidation-SH, com rótulos SUPERSEDE | Fase 3 | Taxas por escritor na amostra; confronto descritivo com os padrões do SUMIE | Acurácia de substituição (primária) e taxa de fatos obsoletos, em análise exploratória, sem inferência causal sobre a operação |

Fonte: elaborado pelo autor (2026).

## 3.12 Ameaças à validade

Quanto à validade interna, os modelos não são perfeitamente pareados, pois diferem em treinamento, tokenizador e pós-treinamento, e a origem do candidato de difusão ainda precisa ser confirmada. Para mitigar essa ameaça, a escala foi aproximada, foram preferidos modelos ajustados por instruções, as demais condições foram fixadas e evita-se linguagem causal sobre arquiteturas. Os processos de decodificação também diferem entre os paradigmas, o que será tratado com orçamentos equivalentes, documentação dos parâmetros e ausência de decodificação restrita. Por fim, o schema pode interagir com o paradigma em direção desconhecida, risco reduzido pela adoção de uma estrutura simples e idêntica para todos.

Quanto à validade de construção, JSON válido não significa memória correta, razão pela qual a avaliação combina métricas estruturais, de estado e de transição. A adaptação das anotações e das políticas de conflito dos conjuntos de dados será documentada e validada no piloto, assim como a capacidade dos estados de referência sob o orçamento de 300 tokens.

Quanto à validade externa, o SUMIE é sintético e representa a sumarização incremental de entidades, e a amostra do FactConsolidation-SH cobre apenas um contraste de substituição. Os resultados não serão generalizados para diálogos longos, tarefas de múltiplos saltos ou todos os tipos de memória.

Quanto à validade de conclusão, a comparação entre os conjuntos de dados confunde operação e domínio, o que mantém a H2 exploratória. O grande número de métricas é tratado pela declaração prévia das métricas primárias, e a eventual execução determinística única é compensada pelo uso de muitas amostras e de intervalos por bootstrap. Resultados obtidos com modelos de difusão maiores ou com decodificação restrita não serão extrapolados para o protocolo deste trabalho. Quanto à validade de implementação, o parser e o validador terão testes unitários, a saída bruta será sempre preservada e nenhum JSON será corrigido silenciosamente.

# 4 Resultados esperados e cronograma

Por se tratar da etapa de projeto, esta seção não apresenta resultados experimentais. São descritas as evidências que a execução deverá produzir para a discussão no TCC II e o cronograma que organiza as atividades até a conclusão do trabalho.

## 4.1 Evidências previstas

A execução das fases 2 e 3 deverá produzir: uma tabela de resultados agregados por escritor, com intervalos de confiança; curvas de F1, de acurácia de preservação e de taxa de fatos obsoletos por turno; uma tabela de acurácias por tipo de operação; a distribuição dos erros estruturais e semânticos por escritor; e uma tabela específica para a amostra de substituição. Esses artefatos são necessários para discutir o alcance de cada objetivo específico, conforme o Quadro 4.

O planejamento não pressupõe qual escritor apresentará melhor desempenho. Diferentes padrões são igualmente informativos: escritores com F1 agregado semelhante podem diferir em preservação ou em operações específicas, revelando perfis distintos de manutenção do estado; um escritor pode gerar JSON válido com alta frequência e, ainda assim, reter fatos obsoletos, o que evidenciaria que correção sintática não implica memória correta; e as diferenças observadas no SUMIE podem não se repetir na amostra de substituição, sugerindo dependência do tipo de informação e de operação. Caso não seja detectada diferença relevante, esse resultado também será relatado, delimitado pelo protocolo e pela precisão estatística alcançada.

Espera-se, como contribuição, um protocolo reprodutível de avaliação que separa a conformidade estrutural da fidelidade do estado e a examina por turno e por operação; um harness e uma adaptação documentada do SUMIE e do FactConsolidation-SH para transições de estado; e evidências sobre os perfis de erro de modelos compactos de paradigmas distintos atuando como escritores de memória.

## 4.2 Cronograma

O cronograma foi derivado dos experimentos e das entregas do trabalho, abrange o TCC I e o TCC II e está organizado em quinzenas. As atividades são as seguintes, com as respectivas dependências entre parênteses:

1. Delimitação do tema e elaboração da ficha de tema.
2. Revisão da literatura, com busca, *snowballing* e auditoria bibliográfica (1).
3. Especificação do protocolo experimental: perguntas, schema, prompt-base e métricas (1, 2).
4. Verificação de acesso e licenças de dados e modelos, incluindo a confirmação do checkpoint de difusão (3).
5. Implementação do harness mínimo: adaptadores, registro, parser, validador e métricas básicas (3).
6. Fase 0: verificação inicial e validação do ambiente local (4, 5).
7. Redação da proposta do TCC I (2, 3).
8. Apresentação à banca do TCC I e retificações (7).
9. Adaptação do SUMIE: estados esperados, canonicalização e rótulos de operação (4, 6).
10. Fase 1: piloto no SUMIE e correções do pipeline (9).
11. Fase 2: experimento principal no SUMIE (10).
12. Fase 3: seleção da amostra e execução no FactConsolidation-SH (4, 10).
13. Análise estatística e produção das visualizações (11, 12).
14. Redação dos resultados, da discussão e das considerações finais (11, 13).
15. Revisão final, depósito e defesa do TCC II (14).

Os Quadros 5 e 6 distribuem essas atividades no tempo.

**Quadro 5 – Cronograma quinzenal do TCC I (2026/2)**

| Atividade | Ago 1ª | Ago 2ª | Set 1ª | Set 2ª | Out 1ª | Out 2ª | Nov 1ª | Nov 2ª | Dez 1ª | Dez 2ª |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | X | X | | | | | | | | |
| 2 | | X | X | X | X | X | X | | | |
| 3 | | | X | X | X | X | | | | |
| 4 | | | | | X | X | X | | | |
| 5 | | | | | | X | X | X | | |
| 6 | | | | | | | X | X | | |
| 7 | | | X | X | X | X | X | X | | |
| 8 | | | | | | | | X | X | |

Fonte: elaborado pelo autor (2026).

**Quadro 6 – Cronograma quinzenal do TCC II (2027/1)**

| Atividade | Fev 1ª | Fev 2ª | Mar 1ª | Mar 2ª | Abr 1ª | Abr 2ª | Mai 1ª | Mai 2ª | Jun 1ª | Jun 2ª |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 9 | X | X | | | | | | | | |
| 10 | | | X | | | | | | | |
| 11 | | | | X | X | | | | | |
| 12 | | | | | X | X | | | | |
| 13 | | | | | | X | X | | | |
| 14 | | | | X | X | X | X | X | | |
| 15 | | | | | | | | | X | X |

Fonte: elaborado pelo autor (2026).

As datas do TCC II serão ajustadas ao calendário acadêmico de 2027/1. O cronograma será validado com o orientador e atualizado sempre que uma decisão metodológica alterar as atividades ou suas dependências.

# 5 Considerações finais

Este trabalho partiu do problema de manter um estado persistente e fiel em agentes baseados em modelos de linguagem que recebem informação em etapas, considerando que cada reescrita de um checkpoint JSON pode perder fatos válidos, reter informação obsoleta, inventar conteúdo ou corromper a estrutura. Para investigá-lo, propôs-se comparar representantes compactos dos paradigmas autoregressivo decoder-only, encoder-decoder e de difusão atuando exclusivamente como escritores de memória, com o objetivo de caracterizar como diferem quanto à validade estrutural, à fidelidade do estado, ao comportamento por operação e à substituição de fatos obsoletos.

O método proposto mantém fixos o GU-JSON, o schema, o prompt, o orçamento de 300 tokens e os dados, variando apenas o modelo escritor. A avaliação no SUMIE, complementada por uma amostra delimitada do FactConsolidation-SH, combina métricas estruturais, de estado e de transição, analisadas por turno e por operação, com intervalos de confiança e comparações pareadas. A principal contribuição esperada é um protocolo reprodutível que separa a correção sintática da fidelidade da memória, acompanhado de evidências sobre os perfis de erro de modelos compactos nessa função.

O desenho possui limitações que restringem a interpretação dos resultados. Os modelos não são pareados em treinamento e tokenização, o que impede atribuir as diferenças exclusivamente à arquitetura. O SUMIE é sintético, o F1 de estado é uma adaptação não diretamente comparável à avaliação original, e o contraste com o FactConsolidation-SH não isola o efeito da operação de substituição. Além disso, o estudo adota um único método de escrita, um único orçamento de memória e não avalia o impacto do checkpoint no desempenho final do agente. A confirmação do checkpoint de difusão e a validação do ambiente local permanecem como condições para a execução.

Como continuidade científica, sugere-se comparar, com os mesmos escritores, métodos de atualização alternativos, como a atualização por caminhos e as operações programáticas; avaliar o efeito da decodificação restrita em cada paradigma; variar o orçamento de memória e a complexidade do schema; investigar a atualização encadeada, em que os erros de cada escritor se propagam ao longo da sequência, e seu impacto em tarefas finais de agentes; empregar pares de modelos com treinamento mais controlado, como versões autoregressiva e de difusão derivadas de um mesmo modelo base, para aproximar a inferência sobre o paradigma; e construir casos de substituição dentro de um mesmo cenário, de modo a isolar o efeito dessa operação.

# Referências

::: {#refs}
:::

# Apêndice A – Prompt-base do escritor de memória

O prompt-base é mantido em inglês, idioma dos conjuntos de dados e dos modelos avaliados, e é idêntico para os três escritores. Os marcadores entre chaves duplas são substituídos pelo harness a cada transição.

```text
You are the memory-state updater of an autonomous agent.

Your task is to update a persistent JSON state.

Rules:
1. Preserve existing information that is still valid.
2. Apply information explicitly introduced by the new observation.
3. Replace old facts only when the observation or task explicitly establishes
   that they are no longer valid. Preserve differing opinions and still-valid
   perspectives rather than assuming that the newest opinion wins.
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

<!--
=====================================================================
NOTAS DE VALIDAÇÃO — NÃO FAZEM PARTE DO ARTIGO (remover antes do DOCX)
=====================================================================
1. Orientador: confirmar nome completo, titulação e vínculo (ficha: "Alex Coelho - a confirmar").
2. Semestre: a ficha diz "2025/2"; as aulas são de 2026.2. O texto usa 2026 (TCC I) e 2027/1 (TCC II, a confirmar).
3. Formato: o Manual de TCC de SI (NDE, 2025) define TCC I como Projeto de Pesquisa; o formato
   Artigo Completo vale para TCC II e exige submissão e aceite em veículo Qualis B2 ou superior.
   Este documento segue o roteiro de artigo do Manual (título, autor, resumo, abstract,
   palavras-chave, keywords, introdução, desenvolvimento com títulos temáticos, considerações
   finais e referências), com conteúdo de proposta. Confirmar com o orientador se o TCC I
   deve ser entregue neste formato ou na estrutura de projeto/monografia.
4. Objetivos específicos: mantidos os 4 da ficha. As aulas recomendaram 3 (orientação verbal,
   não norma). Alternativa: fundir b) e c) em "comparar a fidelidade do estado (P/R/F1) e por
   operação (preservação, adição e atualização) ao longo das atualizações do SUMIE".
5. Estado anterior: o plano experimental fala em "mesmos estados anteriores" para os três
   escritores (estado de referência a cada transição). Confirmar se a avaliação será por
   transição isolada (estado de referência) ou encadeada (estado gerado pelo próprio escritor).
   O texto assume a primeira e coloca a encadeada como trabalho futuro.
6. Checkpoint, repositório e API do Qwen3-0.6B Diffusion BD3LM: pendentes.
7. Licenças: MemoryAgentBench (MIT no cartão vs. CC BY 4.0 no artigo v4); termos do Gemma (T5Gemma).
8. Hardware: confirmar a VRAM da GTX 1650 e a geração do i5 do PC 2.
9. Zotero:
   - Hwang et al. (2024) está cadastrado como preprint; atualizar para Findings of EMNLP 2024,
     p. 3830-3842, DOI 10.18653/v1/2024.findings-emnlp.220.
   - "Agent Harness Engineering: A Survey" (AgentHarnessEngineering2026) está sem autores.
   - Duplicatas: Petersen 2015 (usar petersenGuidelinesConductingSystematic2015) e
     Kitchenham 2010 (usar kitchenhamSystematicLiteratureReviews2010a).
   - Conferir versões publicadas de preprints (ex.: Gong 2024, Arriola 2025, Wu 2024 – ICLR 2025).
   - Instalar o estilo CSL "Associação Brasileira de Normas Técnicas (Português - Brasil)":
     https://www.zotero.org/styles/associacao-brasileira-de-normas-tecnicas
   - Incluir uma referência de metodologia científica para a seção 3.1 (classificação da pesquisa).
10. Bases de busca (seção 3.2): registrar as bases efetivamente consultadas e a data de cada busca.
11. E-mail do autor na nota de rodapé.
=====================================================================
-->
