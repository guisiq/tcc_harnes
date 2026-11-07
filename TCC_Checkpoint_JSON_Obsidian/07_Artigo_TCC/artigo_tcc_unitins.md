---
title: "Modelos de linguagem compactos como escritores de memória"
subtitle: "avaliação da atualização incremental de checkpoints JSON para agentes"
author:
  - "LOPES, Guilherme Henrique Siqueira^[Acadêmico do curso de Bacharelado em Sistemas de Informação da Universidade Estadual do Tocantins (Unitins), Palmas – TO.]"
  - "COELHO, Alex^[Orientador. Mestre e Docente do curso de Bacharelado em Sistemas de Informação da Universidade Estadual do Tocantins (Unitins), Palmas – TO.]"
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

**Resumo:** Agentes baseados em modelos de linguagem que operam em múltiplas etapas dependem de um estado persistente para registrar as informações recebidas incrementalmente. Representar esse estado como um checkpoint JSON atualizado pelo método Generate-Update em JSON (GU-JSON) explicita atributos e valores sob memória limitada, mas exige que o modelo escritor reescreva toda a estrutura a cada turno, expondo o estado a falhas sintáticas, omissão de fatos válidos, alterações indevidas ou alucinações. Embora modelos de linguagem compactos sejam candidatos naturais a executar essa operação localmente com menor custo, a literatura validou o GU-JSON apenas em modelos de grande porte e ainda não comparou como diferentes paradigmas gerativos compactos se comportam nessa tarefa. Este trabalho compara três representantes compactos — Qwen3-0.6B (autoregressivo *decoder-only*), T5Gemma B-B (*encoder-decoder*) e Qwen3-0.6B BD3LM (difusão em blocos) — atuando exclusivamente como escritores de memória no método GU-JSON. O experimento controlado utiliza as sequências de sumarização incremental de entidades do benchmark SUMIE, mantendo constantes o schema JSON, o prompt *zero-shot* e o orçamento de saída de 1.200 tokens, e variando apenas o modelo escritor. A qualidade de cada transição será avaliada pela validade sintática do JSON e conformidade com o schema; pela precisão, revocação, F1 do estado e taxa de alucinação ao longo dos turnos; e pelas acurácias de preservação, adição e atualização por tipo de operação, com intervalos de confiança via *bootstrap* e comparações pareadas.

**Palavras-chave:** Memória de agentes. Checkpoint JSON. Modelos de linguagem compactos. Sumarização incremental.

**Title:** *Compact language models as memory writers: evaluating incremental updates of JSON checkpoints for agents*

**Abstract:** Language-model-based agents operating across multiple steps rely on a persistent state to record information received incrementally. Representing this state as a JSON checkpoint updated through the Generate-Update in JSON (GU-JSON) method makes attributes and values explicit under limited memory, but requires the writer model to regenerate the entire structure at every turn, exposing the state to syntactic failures, omission of valid facts, unintended modifications or hallucinations. Although compact language models are natural candidates to perform this operation locally at lower cost, prior work has validated GU-JSON only with large models and has not yet compared how compact models from distinct generative paradigms behave in this role. This study compares three compact representatives — Qwen3-0.6B (autoregressive decoder-only), T5Gemma B-B (encoder-decoder) and Qwen3-0.6B BD3LM (block diffusion) — acting exclusively as memory writers under the GU-JSON method. The controlled experiment uses the incremental entity summarization sequences from the SUMIE benchmark, holding the JSON schema, zero-shot prompt and 1,200-token output budget constant while varying only the writer model. Transition quality will be evaluated through JSON syntactic validity and schema compliance; state precision, recall, F1 and hallucination rate across turns; and preservation, addition and update accuracies stratified by operation type, using bootstrap confidence intervals and paired comparisons.

**Keywords:** Agent memory. JSON checkpoint. Small language models. Incremental summarization.

# 1 Introdução

Agentes baseados em modelos de linguagem vêm sendo empregados em tarefas de múltiplas etapas, nas quais novas observações chegam de forma sequencial e as decisões subsequentes dependem das informações registradas em turnos anteriores. Nesses fluxos, a manutenção de um estado persistente e consistente condiciona diretamente a confiabilidade operacional do sistema [@muhoberacStateMemoryAll2025]. Por essa razão, benchmarks recentes passaram a avaliar a memória de agentes sob interações incrementais e de longo alcance, examinando a capacidade de reter fatos relevantes, integrar novas evidências e lidar com atualizações ao longo de múltiplos turnos [@huEvaluatingMemoryLLM2025; @wuLongMemEvalBenchmarkingChat2024; @maharanaEvaluatingVeryLongTerm2024].

Como o acúmulo irrestrito do histórico de interações rapidamente excede ou degrada o uso da janela de contexto, uma abordagem recorrente consiste em consolidar as observações em uma representação estruturada persistente. Em tarefas de sumarização incremental com orçamento restrito de memória, @hwangEnhancingIncrementalSummarization2024 demonstraram que o método *Generate-Update* em JSON (GU-JSON) — no qual o modelo recebe o estado anterior e a nova observação e regenera o objeto JSON atualizado — alcança maior fidelidade que a atualização equivalente em texto livre. O uso de um checkpoint JSON explicita os pares de atributo e valor armazenados e permite inspecionar o estado de forma direta a cada transição [@jayalathPRISMEfficientLongRange2025; @yuenIntrinsicMemoryAgents2025]. Entretanto, como o método exige reescrever integralmente o objeto a cada etapa, o componente responsável pela escrita (*memory writer*) torna-se um ponto crítico de falha: a atualização pode tanto corromper a sintaxe do JSON ou violar o schema estipulado [@gengJSONSchemaBenchRigorousBenchmark2025] quanto omitir fatos ainda válidos, alterar valores indevidamente ou introduzir informações sem respaldo na entrada.

Uma vez que a reescrita do checkpoint ocorre repetidamente a cada turno de interação, delegar essa operação a modelos de grande porte eleva o custo computacional e a latência do agente. Modelos de linguagem compactos (*small language models*, SLMs), que viabilizam execução local e menor consumo de recursos em subtarefas bem delimitadas e restritas por schema [@luSmallLanguageModels2025; @sharmaSmallLanguageModels2025], apresentam-se como alternativa para atuar como escritores dedicados de memória. Contudo, transformar um estado JSON anterior e uma nova observação textual em um novo objeto JSON completo impõe demandas distintas conforme o paradigma gerativo do modelo. Modelos autoregressivos *decoder-only* produzem a estrutura token a token da esquerda para a direita [@yangQwen3TechnicalReport2025]; modelos *encoder-decoder* separam a codificação bidirecional da entrada da decodificação sequencial do novo estado [@zhangEncoderDecoderGemmaImproving2025]; e modelos de difusão em blocos combinam geração autoregressiva entre blocos com refinamento paralelo de tokens mascarados no interior de cada bloco [@arriolaBlockDiffusionInterpolating2025].

Embora a literatura investigue separadamente a organização da memória em agentes [@zengStructuralMemoryLLM2024; @jayalathPRISMEfficientLongRange2025; @yuenIntrinsicMemoryAgents2025], a conformidade na geração de JSON [@gengJSONSchemaBenchRigorousBenchmark2025; @mundlerConstrainedDecodingDiffusion2025] e a sumarização incremental estruturada [@hwangEnhancingIncrementalSummarization2024; @hwangSUMIESyntheticBenchmark2025], o efeito do paradigma gerativo em escritores compactos de estado JSON permanece em aberto. O método GU-JSON e o benchmark de sumarização incremental de entidades SUMIE foram avaliados originalmente apenas com modelos proprietários de grande porte [@hwangEnhancingIncrementalSummarization2024; @hwangSUMIESyntheticBenchmark2025], ao passo que comparações recentes entre modelos autoregressivos e de difusão em fluxos agênticos concentraram-se em modelos de 7 a 8 bilhões de parâmetros operando sobre memória em texto livre [@luBitterLessonDiffusion2026]. Não se identificou, na literatura consultada, uma comparação controlada entre representantes compactos de paradigmas gerativos distintos atuando exclusivamente como escritores de um mesmo checkpoint JSON sob orçamento fixo de tokens.

Diante dessa lacuna, este trabalho busca responder à seguinte pergunta de pesquisa: como representantes compactos dos paradigmas autoregressivo *decoder-only*, *encoder-decoder* e de difusão em blocos diferem na qualidade da atualização incremental de checkpoints pelo método GU-JSON no benchmark SUMIE, sob schema e limite de memória fixos?

O objetivo geral é comparar a qualidade da atualização incremental de checkpoints JSON produzida pelos modelos compactos Qwen3-0.6B (*decoder-only*), T5Gemma B-B (*encoder-decoder*) e Qwen3-0.6B BD3LM (difusão em blocos), atuando como escritores de memória no método GU-JSON, no benchmark SUMIE e sob condições experimentais controladas. Para alcançá-lo, definem-se três objetivos específicos:

a) avaliar a conformidade estrutural dos checkpoints produzidos por cada escritor a partir das taxas de validade sintática do JSON e de aderência ao schema ao longo das transições;

b) comparar a fidelidade do estado mantido por cada escritor ao longo dos turnos de atualização do SUMIE, utilizando precisão, revocação, F1 do estado e taxa de alucinação;

c) analisar o perfil de erro dos escritores segundo o tipo de operação exigida no SUMIE, contrastando a preservação de atributos inalterados com a adição e a atualização de informações.

O restante deste artigo está organizado da seguinte forma: a seção 2 apresenta a fundamentação teórica sobre memória persistente estruturada em agentes e posiciona os trabalhos relacionados; a seção 3 detalha os materiais e métodos do experimento; a seção 4 descreve os resultados esperados e o cronograma de execução; e a seção 5 apresenta as considerações finais.

# 2 Memória persistente em agentes baseados em modelos de linguagem

A manutenção de estado estruturado em agentes envolve decisões sobre o formato de representação da memória, o mecanismo de atualização incremental, os critérios de avaliação de fidelidade, a garantia de conformidade sintática e a escolha do modelo gerador. As subseções a seguir discutem esses cinco eixos e sintetizam os trabalhos mais próximos da presente proposta.

## 2.1 Representação estruturada da memória

A escolha do formato de armazenamento condiciona a capacidade do agente de reter e consultar informações ao longo de interações extensas. Ao investigar diferentes estruturas de memória em agentes, @zengStructuralMemoryLLM2024 identificaram vantagens distintas conforme o formato adotado, evidenciando que resumos favorecem a condensação de contextos longos e que unidades factuais explícitas favorecem a precisão na retenção de detalhes — propriedades combinadas quando o estado de uma entidade é mantido como um conjunto estruturado de pares atributo-valor, ainda que aquele estudo avalie estratégias de recuperação e não a reescrita incremental do estado.

Sistemas voltados à persistência de estado ao longo de múltiplas etapas adotam mecanismos variados para estruturar e atualizar essa memória. O PRISM organiza a memória em um schema hierárquico tipado e realiza atualizações por meio de operações de caminho e valor validadas e aplicadas programaticamente [@jayalathPRISMEfficientLongRange2025]. De forma distinta, os Intrinsic Memory Agents reescrevem a memória contextual de cada agente a partir do estado anterior e da saída mais recente, avaliando templates manuais, genéricos e gerados pelo próprio modelo [@yuenIntrinsicMemoryAgents2025]. Outras arquiteturas recorrem a autômatos finitos para rastrear o estado operacional em fluxos científicos extensos, como o SciBORG [@muhoberacStateMemoryAll2025], ou priorizam a construção dinâmica de fragmentos para raciocínio em múltiplas etapas, como a Chain-of-Memory [@xuChainofMemoryLightweightMemory2026].

Em conjunto, esses estudos demonstram que o formato de representação da memória e o mecanismo empregado para atualizá-la constituem dimensões independentes de projeto. Enquanto abordagens como o PRISM dependem de controladores programáticos externos e sistemas multiagente avaliam apenas o desempenho na tarefa final, a adoção de um schema JSON único e fixo permite isolar experimentalmente o processo de reescrita do estado e medir diretamente a fidelidade de cada transição.

## 2.2 Atualização incremental e o método Generate-Update em JSON

@hwangEnhancingIncrementalSummarization2024 investigaram a manutenção de resumos incrementais sob orçamento restrito de memória, comparando as estratégias *Generate-Once* (GO), *Generate-Update* (GU) e *Generate-Merge* (GM) em representações textuais e em JSON nos conjuntos SUMIE e BooookScore, utilizando os modelos Gemini Ultra e Gemini Pro. Sob limite de tokens, a atualização sobre representações em JSON (GU-JSON) superou consistentemente a atualização equivalente em texto livre (GU-Text). Os autores também propuseram o *Chain-of-Key* em JSON (CoK-JSON), que decompõe a tarefa selecionando chaves específicas antes da atualização.

No método GU-JSON, a cada nova observação o modelo escritor recebe o schema, o checkpoint corrente e a observação, gerando diretamente o checkpoint completo atualizado, conforme a Equação 1:

$$
M_t = G\left(S,\ M_{t-1},\ O_t\right) \qquad (1)
$$

em que $S$ é o schema, $M_{t-1}$ é o checkpoint anterior, $O_t$ é a nova observação, $G$ é o modelo escritor e $M_t$ é o checkpoint resultante.

Para a comparação entre modelos escritores compactos, o GU-JSON apresenta uma propriedade metodológica central: ele concentra toda a operação de manutenção do estado em uma única chamada ao modelo $G$. Diferentemente de métodos que decompõem a atualização em etapas de seleção de caminhos ou aplicam modificações parciais por código externo [@hwangEnhancingIncrementalSummarization2024; @jayalathPRISMEfficientLongRange2025], a reescrita integral exige que o próprio modelo preserve os campos inalterados, integre as novas informações e mantenha a estrutura JSON válida simultaneamente, permitindo avaliar diretamente o comportamento do escritor sem interferência de algoritmos auxiliares de mesclagem.

## 2.3 Avaliação de memória e de atualização de conhecimento

O benchmark SUMIE foi desenvolvido especificamente para avaliar a sumarização incremental de entidades a partir de sequências de parágrafos que introduzem fatos novos, repetições, informações distratoras e pontos de vista divergentes [@hwangSUMIESyntheticBenchmark2025]. Cada parágrafo conta com anotações de atributos e valores relevantes da entidade descrita. Uma característica central do SUMIE é sua política de acumulação: como diferentes fontes ou parágrafos podem expressar perspectivas distintas sobre um mesmo atributo, o prompt de atualização de referência determina a preservação dos atributos prévios e a integração de visões conflitantes, sem que uma nova opinião invalide automaticamente a anterior. No estudo original, os autores observaram perfis contrastantes de precisão e revocação entre os modelos de grande porte avaliados.

Outros benchmarks recentes examinam a memória sob interações de múltiplos turnos, porém com foco na resposta a perguntas ao final da sequência. O MemoryAgentBench avalia quatro competências de memória — incluindo a consolidação de fatos e o esquecimento seletivo sob regras de precedência temporal [@huEvaluatingMemoryLLM2025] —, enquanto o LongMemEval enfatiza a atualização de conhecimento e o raciocínio temporal em assistentes conversacionais [@wuLongMemEvalBenchmarkingChat2024], e o LoCoMo investiga diálogos muito longos distribuídos em múltiplas sessões [@maharanaEvaluatingVeryLongTerm2024].

A análise conjunta desses benchmarks revela que avaliações baseadas apenas em respostas finais podem mascarar degradações progressivas do estado interno, como a perda silenciosa de atributos antigos ao longo dos turnos. Ao tomar o SUMIE como cenário experimental e inspecionar diretamente o checkpoint gerado em cada transição $M_t$, torna-se possível quantificar separadamente a capacidade do escritor de preservar atributos existentes, adicionar novos campos e atualizar valores já presentes.

## 2.4 Geração estruturada: validade sintática e conformidade com schema

A utilização de JSON como formato de estado exige distinguir a correção formal da saída de sua correção semântica. O benchmark JSONSchemaBench demonstra que modelos de linguagem apresentam taxas não triviais de falha sintática e de violação de restrições quando submetidos a JSON Schemas de diferentes complexidades [@gengJSONSchemaBenchRigorousBenchmark2025]. Para contornar essas falhas em modelos autoregressivos, técnicas de decodificação restrita por gramática filtram tokens inválidos durante a inferência sem necessidade de ajuste fino [@gengGrammarConstrainedDecodingStructured2023]. Mais recentemente, mecanismos análogos baseados em gramáticas livres de contexto [@mundlerConstrainedDecodingDiffusion2025] e em aprendizado por reforço multiagente [@khanalAgentsDiffusionEnhancing2026] foram propostos para elevar a conformidade sintática em modelos de linguagem por difusão.

Na avaliação de escritores de memória, essa literatura impõe dois cuidados experimentais. Primeiro, a conformidade com o schema é condição necessária para a leitura automatizada do estado, mas não suficiente para garantir fidelidade: um objeto JSON sintaticamente válido pode omitir atributos essenciais ou conter valores alucinados, razão pela qual métricas estruturais e semânticas devem ser apuradas de forma independente. Segundo, como os motores de decodificação restrita atuam de maneira distinta sobre a geração sequencial e sobre o refinamento iterativo por difusão, a avaliação em regime puramente instrucional (*prompt-only*) é necessária para observar a capacidade intrínseca de cada modelo de preservar a sintaxe e o conteúdo do checkpoint.

## 2.5 Paradigmas gerativos e modelos de linguagem compactos

Os três paradigmas gerativos considerados neste estudo processam a relação entre entrada e saída sob princípios distintos. Modelos autoregressivos *decoder-only* fatoram a probabilidade da sequência da esquerda para a direita, gerando cada token condicionado ao prefixo já produzido; a família Qwen3 exemplifica esse paradigma em múltiplas escalas, incluindo modelos compactos de 0,6 bilhão de parâmetros [@yangQwen3TechnicalReport2025]. Modelos *encoder-decoder*, por sua vez, empregam um codificador com atenção bidirecional sobre toda a sequência de entrada antes de gerar a saída no decodificador; o T5Gemma obtém essa arquitetura pela adaptação de modelos *decoder-only* pré-treinados, visando combinar representação bidirecional do contexto com eficiência de inferência [@zhangEncoderDecoderGemmaImproving2025].

Já os modelos de linguagem baseados em difusão formulam a geração como um processo iterativo de remoção de ruído sobre posições mascaradas, permitindo atualizar múltiplos tokens paralelamente [@nieScalingMaskedDiffusion2024], inclusive a partir da adaptação de pesos autoregressivos [@gongScalingDiffusionLanguage2024]. A arquitetura de difusão em blocos (*Block Diffusion*, BD3LM) interpola ambos os mecanismos ao gerar blocos de tokens de maneira autoregressiva enquanto aplica difusão discreta dentro de cada bloco [@arriolaBlockDiffusionInterpolating2025]. Em avaliação recente de modelos de difusão de 7 a 8 bilhões de parâmetros em fluxos agênticos, @luBitterLessonDiffusion2026 observaram fragilidades na geração de chamadas de ferramentas com sintaxe estrita, mas desempenho competitivo na sumarização de memória em texto livre — contraste que motiva investigar como um modelo compacto de difusão em blocos se comporta quando a sumarização de memória exige produzir um objeto JSON estruturado.

O recorte em modelos compactos fundamenta-se na viabilidade de executá-los localmente com menor custo energético e financeiro [@luSmallLanguageModels2025] e na evidência de que modelos de menor escala podem atuar com eficácia em subtarefas agênticas repetitivas e bem delimitadas [@sharmaSmallLanguageModels2025]. Como a execução em hardware local frequentemente recorre à redução de precisão numérica e modelos menores apresentam maior sensibilidade à quantização agressiva [@leeExploringTradeOffsQuantization2025], a comparação experimental requer padronizar e documentar as condições de precisão e inferência.

## 2.6 Trabalhos relacionados

O Quadro 1 sintetiza os estudos mais próximos da presente pesquisa segundo a representação da memória, o mecanismo de atualização, a escala dos modelos avaliados, o objeto da avaliação e a presença de comparação entre paradigmas gerativos.

**Quadro 1 – Comparação entre trabalhos relacionados e a proposta**

| Trabalho | Representação da memória | Atualização | Modelos e escala | Objeto da avaliação | Compara paradigmas gerativos |
|---|---|---|---|---|---|
| @hwangEnhancingIncrementalSummarization2024 | Texto e JSON | GO, GU, GM e CoK, executados pelo próprio modelo | Gemini Ultra e Gemini Pro (grande porte) | Qualidade de resumos incrementais (SUMIE e BooookScore) | Não |
| @hwangSUMIESyntheticBenchmark2025 | Atributos e valores de entidades | Atualização incremental com preservação de perspectivas | Modelos de linguagem de grande porte | Precisão, revocação e F1 de atributos no resumo | Não |
| @jayalathPRISMEfficientLongRange2025 | Memória tipada hierárquica | Operações de caminho e valor aplicadas programaticamente | Modelos de contexto curto | Raciocínio de longo alcance (tarefa final) | Não |
| @yuenIntrinsicMemoryAgents2025 | Memória contextual por agente (JSON em variantes específicas) | Reescrita a partir da memória anterior e da saída recente | Modelos de linguagem em sistemas multiagente | Desempenho do sistema multiagente | Não |
| @zengStructuralMemoryLLM2024 | Trechos, triplas, fatos atômicos, resumos e memória mista | Construção e recuperação | Modelos de linguagem de propósito geral | Desempenho de recuperação em tarefas finais | Não |
| @huEvaluatingMemoryLLM2025 | Diversos sistemas de memória | Interações incrementais de múltiplos turnos | Diversos agentes de memória | Respostas finais em quatro competências | Não |
| @luBitterLessonDiffusion2026 | Texto livre e chamadas de ferramentas | Sumarização textual | Modelos de difusão e autoregressivos de 7 a 8B | Desempenho em fluxos agênticos | Sim, sem checkpoint JSON |
| @gengJSONSchemaBenchRigorousBenchmark2025 | JSON Schema | Não se aplica (geração estática) | Frameworks de decodificação restrita | Conformidade sintática e de schema | Não |
| **Este trabalho** | Checkpoint JSON de schema fixo | GU-JSON, com reescrita integral pelo escritor | Três representantes compactos (~0,6B: autoregressivo, *encoder-decoder* e difusão em blocos) | Validade estrutural e fidelidade do estado por transição, turno e operação no SUMIE | Sim, sob protocolo controlado |

Fonte: elaborado pelo autor (2026).

Como evidencia o Quadro 1, os estudos que introduzem o GU-JSON e o SUMIE empregam modelos de grande porte; as propostas de memória estruturada como o PRISM utilizam operações programáticas em vez de reescrita integral pelo modelo; os benchmarks de memória avaliam respostas finais; e a comparação existente entre paradigmas autoregressivo e de difusão analisa modelos dez vezes maiores com memória em texto livre. Este trabalho preenche essa interseção ao manter constantes o método GU-JSON, o schema, o orçamento de tokens e as sequências do SUMIE para avaliar diretamente a qualidade estrutural e semântica dos checkpoints produzidos pelos três escritores compactos.

# 3 Materiais e métodos

Este estudo segue um delineamento experimental, aplicado e quantitativo em Ciência da Computação, comparando o perfil de erros estruturais e semânticos de três escritores compactos de memória ao longo dos turnos e das operações de atualização do benchmark público SUMIE. Como os experimentos utilizam exclusivamente conjuntos de dados sintéticos públicos e modelos de pesos abertos, sem envolvimento de seres humanos ou dados pessoais, o protocolo dispensa submissão a Comitê de Ética em Pesquisa. As subseções a seguir detalham as variáveis e hipóteses do experimento, o método GU-JSON e o prompt utilizado, a preparação das transições do SUMIE, os modelos avaliados, o *harness* de execução local, as métricas e o plano de análise estatística.

## 3.1 Desenho experimental e variáveis

O experimento manipula como única variável independente o modelo escritor (*memory writer*) e mantém constantes o método de atualização, o schema, o prompt, o limite de tokens e as sequências de entrada, conforme sintetizado no Quadro 2.

**Quadro 2 – Variáveis do experimento**

| Tipo | Variável | Operacionalização |
|---|---|---|
| Independente | Modelo escritor | Qwen3-0.6B (autoregressivo *decoder-only*); T5Gemma B-B PrefixLM-IT (*encoder-decoder*); Qwen3-0.6B Diffusion BD3LM (difusão em blocos) |
| Controlada | Método de atualização | GU-JSON, com reescrita integral do checkpoint a cada turno |
| Controlada | Schema | `{"state": {"chave": "valor"}}`, idêntico para todos os escritores e instâncias |
| Controlada | Prompt | Prompt-base *zero-shot* em inglês, sem instruções específicas por arquitetura |
| Controlada | Orçamento de saída | Limite máximo fixo de 1.200 tokens gerados por transição |
| Controlada | Contexto de entrada | Limite de até 8.192 tokens |
| Controlada | Dados de entrada | Mesmas sequências do SUMIE, na mesma ordem, com os mesmos estados anteriores de referência |
| Controlada | Decodificação | Geração determinística sem decodificação restrita por gramática (*prompt-only*) |
| Dependente | Conformidade estrutural | Taxa de validade sintática do JSON (*JSON Validity*) e taxa de conformidade com o schema (*Schema Validity*) |
| Dependente | Fidelidade global do estado | Precisão (*State Precision*), revocação (*State Recall*), F1 do estado (*State F1*) e taxa de alucinação (*Hallucination Rate*) |
| Dependente | Fidelidade por operação | Acurácia de preservação (*Preservation Accuracy*) e acurácia de atualização (*Update Accuracy*, desdobrada em adição e modificação) |

Fonte: elaborado pelo autor (2026).

O desenho experimental responde à pergunta principal de pesquisa (RQ1) — como os três representantes compactos diferem na qualidade das atualizações GU-JSON no SUMIE sob schema e limite de 1.200 tokens fixos — e a duas questões analíticas desdobradas: como a conformidade estrutural e a fidelidade do estado evoluem ao longo da sequência de turnos de atualização (RQ2); e como os escritores diferem entre as operações de preservação de atributos anteriores, adição de novos atributos e atualização de atributos existentes no SUMIE (RQ3).

Para orientar o teste empírico, formula-se a hipótese nula ($H_0$) de que não há diferença estatisticamente significativa nas métricas primárias de fidelidade do estado (F1 do estado, acurácia de preservação e acurácia de atualização) entre os três modelos escritores avaliados sob o protocolo GU-JSON no SUMIE. Em contrapartida, a hipótese alternativa ($H_1$) estabelece que os representantes avaliados apresentam diferenças estatisticamente significativas na preservação do estado prévio e na incorporação de novas informações ao longo das transições, refletindo perfis de erro distintos sob o mesmo orçamento de geração.

## 3.2 Método de memória, schema e prompt

Em cada transição do experimento, aplica-se a formulação do GU-JSON (Equação 1): o escritor recebe o schema, o checkpoint de referência do turno anterior ($M_{t-1}$) e o parágrafo correspondente à nova observação ($O_t$), devendo produzir exclusivamente o objeto JSON atualizado ($M_t$). O uso do estado anterior de referência ($M_{t-1}$ padrão-ouro) como entrada em cada turno garante que todos os escritores sejam avaliados sob exatamente as mesmas condições em cada passo da sequência, evitando que uma falha sintática no turno $t$ inviabilize a mensuração das transições seguintes.

Adota-se o schema mínimo `{"state": {"chave": "valor"}}`, no qual os atributos da entidade descrita no SUMIE são representados como chaves textuais dentro do objeto `state` e seus respectivos conteúdos como valores em texto. O prompt-base (Apêndice A) é redigido em inglês — idioma nativo do conjunto de dados — e estabelece seis instruções operacionais: preservar informações anteriores que permanecem válidas; incorporar informações explicitamente introduzidas pela nova observação; substituir valores prévios apenas quando a observação estabelecer sua invalidade, mantendo perspectivas divergentes válidas; não inventar fatos sem suporte; respeitar estritamente o schema; e retornar unicamente o objeto JSON completo. O orçamento máximo de saída é fixado em 1.200 tokens por transição, em consonância com o regime de memória limitada analisado por @hwangEnhancingIncrementalSummarization2024.

Os adaptadores de inferência de cada modelo limitam-se a aplicar o formato de entrada exigido pela respectiva interface (como marcadores de turno e desativação de blocos de raciocínio explícito no Qwen3 para que o orçamento de 1.200 tokens seja integralmente dedicado ao JSON), sem alterar o conteúdo instrucional do prompt.

## 3.3 Conjunto de dados e preparação das transições

O experimento utiliza o benchmark SUMIE [@hwangSUMIESyntheticBenchmark2025], disponibilizado publicamente sob licença Apache-2.0.^[Disponível em: https://github.com/google-deepmind/sumie.] No SUMIE, cada instância representa uma entidade descrita ao longo de uma sequência ordenada de parágrafos acompanhados das anotações de atributos e valores introduzidos ou mencionados em cada passo.

Para viabilizar a avaliação direta de transições de estado sob o método GU-JSON, cada etapa $t$ de uma entidade é estruturada como uma tupla $(M_{t-1}^*,\ O_t,\ M_t^*)$, em que $M_{t-1}^*$ é o estado acumulado de referência até o turno $t-1$, $O_t$ é o texto do parágrafo no turno $t$ e $M_t^*$ é o estado acumulado esperado após a incorporação de $O_t$. A partir da comparação entre $M_{t-1}^*$ e $M_t^*$, cada atributo esperado em $M_t^*$ recebe um rótulo determinístico de operação:

a) **PRESERVE:** atributo já presente em $M_{t-1}^*$ cujo valor não sofre alteração na observação $O_t$ e deve ser mantido intacto em $M_t$;
b) **ADD:** atributo ausente em $M_{t-1}^*$ e introduzido pela primeira vez na observação $O_t$;
c) **UPDATE:** atributo já existente em $M_{t-1}^*$ que recebe informação complementar ou nova perspectiva apresentada em $O_t$, respeitando a regra do SUMIE de integrar visões divergentes sem descartar arbitrariamente o registro anterior.

Durante a preparação dos dados no estudo piloto, são verificadas as regras de canonicalização textual (normalização de espaços, caixa e pontuação) e o comprimento em tokens dos estados acumulados de referência $M_t^*$, assegurando que os estados esperados caibam integralmente no orçamento de 1.200 tokens e que eventuais omissões observadas decorram do comportamento do modelo escritor, e não de truncamento forçado pelo limite de saída. Caso haja disponibilidade de tempo no cronograma após a conclusão integral dos experimentos no SUMIE, prevê-se como verificação complementar opcional a aplicação do mesmo protocolo a uma amostra delimitada do subconjunto FactConsolidation-SH do MemoryAgentBench [@huEvaluatingMemoryLLM2025], a fim de observar o comportamento dos escritores em cenários com substituição temporal explícita de fatos (*supersession*).

## 3.4 Modelos avaliados

Os três modelos escritores foram selecionados para representar paradigmas gerativos distintos mantendo escala aproximada (~0,6 bilhão de parâmetros), pesos publicamente acessíveis e viabilidade de execução em hardware local:

a) **Qwen3-0.6B** [@yangQwen3TechnicalReport2025]: representante do paradigma autoregressivo *decoder-only*, distribuído sob licença Apache-2.0, utilizado como linha de base autoregressiva;^[Disponível em: https://huggingface.co/Qwen/Qwen3-0.6B.]
b) **T5Gemma B-B PrefixLM-IT** [@zhangEncoderDecoderGemmaImproving2025]: representante do paradigma *encoder-decoder* ajustado por instruções, com codificador bidirecional e decodificador autoregressivo na faixa de 0,6 bilhão de parâmetros;^[Disponível em: https://huggingface.co/google/t5gemma-b-b-prefixlm-it.]
c) **Qwen3-0.6B Diffusion BD3LM** [@arriolaBlockDiffusionInterpolating2025]: representante do paradigma de difusão discreta em blocos (*block diffusion*), que combina geração sequencial de blocos com refinamento paralelo de tokens mascarados.

Como os três modelos possuem diferenças de pré-treinamento, tokenização e ajuste por instruções além da arquitetura de geração, a análise empírica compara o desempenho efetivo desses representantes compactos na tarefa de escrita de memória, sem extrapolar causalidade exclusiva para o paradigma gerativo em abstrato. Os identificadores exatos de revisão (*commit hashes*) dos pesos e a configuração numérica de inferência são fixados no arquivo de manifesto do experimento.

## 3.5 Ambiente de execução e harness experimental

Os experimentos de inferência serão executados localmente em um computador portátil Lenovo IdeaPad Gaming 3i equipado com processador Intel Core i5 de 10ª geração, 24 GB de memória RAM e unidade de processamento gráfico dedicada NVIDIA GeForce GTX 1650. Um segundo computador (Intel Core i5, 16 GB de RAM) será empregado nas etapas de pré-processamento do conjunto de dados, execução da suíte de testes unitários do validador e análise estatística dos resultados. Considerando a sensibilidade de modelos compactos à redução agressiva de precisão numérica [@leeExploringTradeOffsQuantization2025], o tipo de ponto flutuante (como `FP16` ou `BF16`) será mantido uniforme entre os modelos avaliados.

Para garantir que apenas o modelo escritor varie entre as execuções [@AgentHarnessEngineering2026], o pipeline é encapsulado em um *harness* experimental modular composto por oito etapas sequenciais por transição: (i) leitura da transição padronizada $(M_{t-1}^*,\ O_t,\ M_t^*)$; (ii) montagem do prompt a partir do template fixo; (iii) invocação do adaptador do escritor sob o limite de 1.200 tokens; (iv) gravação imediata da saída textual bruta em disco; (v) verificação de validade sintática por um *parser* JSON padrão; (vi) validação estrutural contra o schema definido; (vii) extração dos pares atributo-valor e cálculo das métricas semânticas de estado e de operação em relação a $M_{t-1}^*$ e $M_t^*$; e (viii) persistência dos indicadores da transição em registro estruturado (JSON Lines), acompanhado do identificador da amostra, turno, modelo, *hash* do prompt e versões das bibliotecas. Nenhuma etapa de pós-processamento ou reparo automático de sintaxe é aplicada sobre a saída bruta para o cálculo das métricas principais.

## 3.6 Métricas de avaliação

Para a avaliação semântica dos checkpoints sintaticamente válidos e aderentes ao schema, o objeto JSON produzido é convertido em um conjunto de pares canônicos caminho-valor da forma `("state.<atributo>", "<valor_normalizado>")`, desconsiderando a ordenação das chaves. A precisão ($P$), a revocação ($R$) e a medida $F_1$ do estado em cada transição são definidas pelas Equações 2 a 4, nas quais $TP$ representa o número de pares presentes no checkpoint gerado que coincidem com o estado esperado $M_t^*$, $FP$ o número de pares gerados ausentes ou divergentes de $M_t^*$ e $FN$ o número de pares de $M_t^*$ omitidos pelo escritor:

$$
P = \frac{TP}{TP + FP} \qquad (2)
$$

$$
R = \frac{TP}{TP + FN} \qquad (3)
$$

$$
F_1 = \frac{2PR}{P + R} \qquad (4)
$$

Para avaliar o comportamento do escritor segundo a natureza da transição em cada atributo, calculam-se a acurácia de atualização ($UA$), desdobrada nas operações `ADD` e `UPDATE`, e a acurácia de preservação ($PA$), correspondente à operação `PRESERVE`, conforme as Equações 5 e 6:

$$
UA = \frac{\text{atributos com operação ADD ou UPDATE registrados corretamente em } M_t}{\text{total de atributos com operação ADD ou UPDATE esperados em } M_t^*} \qquad (5)
$$

$$
PA = \frac{\text{atributos inalterados de } M_{t-1}^* \text{ mantidos corretamente em } M_t}{\text{total de atributos com operação PRESERVE esperados em } M_t^*} \qquad (6)
$$

O Quadro 3 sintetiza as métricas estruturais, de estado e de operação adotadas no protocolo.

**Quadro 3 – Métricas de avaliação do experimento**

| Categoria | Métrica | Definição operacional | Escopo de cálculo |
|---|---|---|---|
| Estrutural | Validade do JSON (*JSON Validity*) | Proporção de saídas brutas interpretáveis por `json.loads` sem reparo sintático | Todas as transições |
| Estrutural | Conformidade com o schema (*Schema Validity*) | Proporção de saídas que contêm exclusivamente o objeto raiz `state` mapeando chaves textuais a valores | Todas as transições |
| Estado | Precisão do estado (*State Precision*) | Fração dos pares atributo-valor gerados em $M_t$ que estão corretos (Equação 2) | Transições válidas e na análise global (atribuindo zero a falhas estruturais) |
| Estado | Revocação do estado (*State Recall*) | Fração dos pares esperados em $M_t^*$ recuperados corretamente em $M_t$ (Equação 3) | Transições válidas e na análise global |
| Estado | F1 do estado (*State F1*) | Média harmônica entre precisão e revocação do estado (Equação 4); métrica semântica primária | Transições válidas e na análise global |
| Estado | Taxa de alucinação (*Hallucination Rate*) | Proporção de pares gerados em $M_t$ sem correspondência nem suporte em $M_{t-1}^*$ ou $O_t$ | Transições com JSON válido |
| Operação | Acurácia de preservação (*Preservation Accuracy*) | Fração dos atributos de $M_{t-1}^*$ não alterados por $O_t$ que foram retidos corretamente (Equação 6); métrica primária | Atributos rotulados como `PRESERVE` |
| Operação | Acurácia de atualização (*Update Accuracy*) | Fração das inclusões e modificações introduzidas por $O_t$ aplicadas corretamente (Equação 5), reportada de forma agregada e separada para `ADD` e `UPDATE`; métrica primária | Atributos rotulados como `ADD` ou `UPDATE` |

Fonte: elaborado pelo autor (2026).

As métricas semânticas serão reportadas sob duas visões complementares: (i) **condicional à validade estrutural**, calculada sobre as transições em que o escritor produziu JSON válido e aderente ao schema, isolando a qualidade do conteúdo; e (ii) **global (*end-to-end*)**, atribuindo pontuação zero às transições com falha sintática, o que reflete a confiabilidade efetiva do escritor no pipeline.

## 3.7 Procedimento experimental e plano de análise

A execução experimental organiza-se em três fases sequenciais sobre o benchmark SUMIE:

a) **Fase 0 — Verificação funcional do *harness*:** execução de 15 transições sintéticas de teste para validar o carregamento local dos três modelos, a aplicação do prompt, o respeito ao orçamento de 1.200 tokens e a exatidão do *parser*, do validador de schema e do calculador de métricas (verificados por testes unitários);
b) **Fase 1 — Estudo piloto no SUMIE:** execução em um subconjunto de 25 entidades (separado da amostra de teste principal) para calibrar as regras de canonicalização textual, verificar o comprimento em tokens dos estados acumulados $M_t^*$ e confirmar a ausência de truncamento;
c) **Fase 2 — Experimento principal no SUMIE:** execução completa dos três escritores sobre o conjunto de avaliação do SUMIE, registrando todas as saídas brutas e métricas por transição, turno e operação.

Na análise estatística dos resultados da Fase 2, serão apuradas a média e a mediana de cada métrica por escritor, acompanhadas de intervalos de confiança de 95% estimados por *bootstrap* não paramétrico (10.000 reamostragens no nível da entidade, preservando a estrutura de dependência longitudinal entre os turnos de uma mesma sequência). Como os três modelos avaliam exatamente as mesmas transições, a verificação das hipóteses $H_0$ e $H_1$ será realizada por meio das diferenças pareadas entre escritores no nível de entidade e por testes não paramétricos pareados (teste de Friedman para a comparação global entre os três modelos e teste de Wilcoxon pareado com correção de Holm-Bonferroni para comparações dois a dois, adotando $\alpha = 0{,}05$). A evolução temporal será examinada por curvas de *State F1*, *Preservation Accuracy* e *JSON Validity* em função do índice do turno $t$.

## 3.8 Rastreabilidade entre objetivos, experimentos e evidências

O Quadro 4 explicita o alinhamento metodológico entre cada objetivo específico formulado na introdução, o componente do *harness* responsável pela coleta, a evidência empírica gerada na Fase 2 e os critérios quantitativos de análise.

**Quadro 4 – Matriz de rastreabilidade entre objetivos específicos, artefatos e evidências**

| Objetivo específico | Artefato e procedimento | Evidência produzida | Métrica e critério de análise |
|---|---|---|---|
| a) Avaliar a conformidade estrutural dos checkpoints produzidos por cada escritor | *Parser* JSON, validador de schema e log de saídas brutas sem reparo automático | Tabela de validade por escritor, curva de validade por turno e distribuição das categorias de erro sintático (truncamento, chaves malformadas, texto extra) | *JSON Validity* e *Schema Validity* com IC de 95% por *bootstrap* e diferenças pareadas entre escritores |
| b) Comparar a fidelidade do estado mantido ao longo dos turnos de atualização do SUMIE | Estados acumulados de referência ($M_t^*$) e avaliador determinístico de pares atributo-valor | Tabela comparativa global e condicional por escritor; curvas longitudinais de fidelidade ao longo dos turnos $t$ | *State Precision*, *State Recall*, *State F1* (primária) e *Hallucination Rate*, com IC de 95%, teste pareado e curvas por turno |
| c) Analisar o perfil de erro dos escritores segundo o tipo de operação no SUMIE | Rotulador de operações (`PRESERVE`, `ADD`, `UPDATE`) entre $M_{t-1}^*$ e $M_t^*$ | Tabela e gráfico comparativo de desempenho estratificado por operação e curva de retenção de atributos ao longo dos turnos | *Preservation Accuracy* (primária) e *Update Accuracy* (`ADD` e `UPDATE`, primária), com IC de 95% e comparações pareadas |

Fonte: elaborado pelo autor (2026).

## 3.9 Limitações metodológicas e ameaças à validade

O delineamento experimental controla o método de atualização, o schema, o prompt, o orçamento de geração e os dados de entrada, mas está sujeito a limitações inerentes à comparação entre modelos pré-treinados distintos:

a) **Validade interna:** os três modelos comparados não compartilham o mesmo corpus de pré-treinamento, tokenizador nem procedimento de pós-treinamento. Assim, as diferenças medidas refletem o desempenho conjunto de cada modelo representante na escala de ~0,6B, e não o efeito isolado da arquitetura de geração. Para evitar distorções adicionais, todos os modelos são avaliados em regime *zero-shot prompt-only*, com precisão numérica padronizada e sem decodificação restrita externa;
b) **Validade de construção:** a avaliação original do SUMIE utiliza um modelo de linguagem como juiz para verificar o alinhamento semântico de evidências [@hwangSUMIESyntheticBenchmark2025], ao passo que este protocolo emprega correspondência determinística após canonicalização textual. Essa escolha elimina a variância e o viés de um avaliador neural, mas exige validar as regras de normalização no piloto (Fase 1) e verificar que os estados de referência não excedam os 1.200 tokens;
c) **Validade externa:** os resultados obtidos restringem-se à tarefa de sumarização incremental de entidades em um schema plano de pares chave-valor sob o método GU-JSON. O estudo avalia transições com estado anterior de referência ($M_{t-1}^*$ padrão-ouro) para isolar o erro por turno, não medindo a propagação acumulativa de erros em execução livre nem o impacto do checkpoint em tarefas finais de tomada de decisão do agente.

# 4 Resultados esperados e cronograma

Esta seção descreve os artefatos de análise e as contribuições esperadas a partir da execução do protocolo experimental no TCC II, bem como o cronograma físico das atividades.

## 4.1 Resultados e contribuições esperadas

A execução completa da Fase 2 sobre o benchmark SUMIE produzirá quatro conjuntos principais de evidências empíricas, diretamente vinculados aos objetivos específicos do trabalho:

1. **Caracterização da robustez estrutural por escritor (Objetivo a):** quantificação das taxas de *JSON Validity* e *Schema Validity* em regime *prompt-only* para o Qwen3-0.6B, o T5Gemma B-B e o Qwen3-0.6B BD3LM, acompanhada da classificação das falhas sintáticas (como fechamento incompleto por limite de tokens, omissão de delimitadores ou emissão de texto fora do objeto JSON). Esse resultado permitirá verificar se a geração iterativa por difusão em blocos ou a codificação bidirecional *encoder-decoder* apresentam maior ou menor estabilidade sintática que a geração autoregressiva *decoder-only* na escala de 0,6B.
2. **Comparação da fidelidade global e longitudinal do estado (Objetivo b):** apuração de *State Precision*, *State Recall*, *State F1* e *Hallucination Rate* (nas visões condicional e global) e construção das curvas de desempenho em função do turno $t$. Essas curvas permitirão identificar como a qualidade do checkpoint degrada à medida que o estado acumulado cresce e se aproxima do orçamento de 1.200 tokens.
3. **Decomposição do perfil de erro por operação de estado (Objetivo c):** comparação pareada entre *Preservation Accuracy* (`PRESERVE`) e *Update Accuracy* (`ADD` e `UPDATE`). Essa estratificação permitirá distinguir, por exemplo, um modelo conservador — que preserva com alta acurácia o estado anterior $M_{t-1}^*$, mas falha em incorporar novos atributos de $O_t$ — de um modelo propenso a sobrescrever ou esquecer campos válidos ao integrar novas informações.
4. **Relação entre validade sintática e fidelidade semântica:** o cruzamento entre as métricas estruturais e semânticas permitirá demonstrar empiricamente em que medida checkpoints sintaticamente válidos ainda sofrem de omissão de atributos ou alucinação de valores, fornecendo um protocolo e um *harness* reutilizáveis para a avaliação de escritores compactos de memória.

## 4.2 Cronograma

O cronograma abrange as etapas de elaboração e validação do projeto no TCC I (2026/2) e a implementação completa, coleta experimental, análise estatística e redação final no TCC II (2027/1), organizadas em períodos quinzenais. As atividades previstas e suas dependências diretas são listadas a seguir:

1. Delimitação do tema, formulação do problema e definição dos objetivos.
2. Levantamento e fichamento da bibliografia sobre memória em agentes, geração estruturada e SLMs (1).
3. Especificação do protocolo experimental: variáveis, schema, prompt-base e métricas (1, 2).
4. Verificação de disponibilidade, licenças e requisitos de execução local dos modelos e do SUMIE (3).
5. Implementação da estrutura base do *harness*: adaptadores, *parser*, validador e testes unitários (3, 4).
6. Execução da Fase 0 (verificação funcional local com transições sintéticas) (5).
7. Redação e revisão do texto do projeto de TCC I (2, 3, 6).
8. Apresentação do projeto de TCC I e incorporação das recomendações da banca (7).
9. Preparação do conjunto SUMIE: construção dos estados acumulados $M_t^*$ e rotulagem de operações (`PRESERVE`, `ADD`, `UPDATE`) (4, 6).
10. Execução da Fase 1 (estudo piloto em 25 entidades do SUMIE) e calibração da canonicalização (9).
11. Execução da Fase 2 (experimento principal com os três modelos escritores no SUMIE) (10).
12. Processamento estatístico (*bootstrap*, testes pareados, curvas por turno e estratificação por operação) e verificação complementar opcional (11).
13. Elaboração das tabelas, gráficos e análise crítica dos resultados frente à literatura (12).
14. Redação das seções de resultados, discussão e conclusões do artigo final (TCC II) (13).
15. Revisão normativa e linguística, depósito final e defesa do TCC II (14).

Os períodos quinzenais planejados para cada atividade ao longo dos dois semestres (`Q1` a `Q20`, de agosto de 2026 a junho de 2027) estão sintetizados na Tabela 1, seguidos da relação numerada das atividades:

| Ativ. | Ago Q1 | Ago Q2 | Set Q3 | Set Q4 | Out Q5 | Out Q6 | Nov Q7 | Nov Q8 | Dez Q9 | Dez Q10 | Fev Q11 | Fev Q12 | Mar Q13 | Mar Q14 | Abr Q15 | Abr Q16 | Mai Q17 | Mai Q18 | Jun Q19 | Jun Q20 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1- | X | X | | | | | | | | | | | | | | | | | | |
| 2- | | X | X | X | X | X | | | | | | | | | | | | | | |
| 3- | | | X | X | X | X | | | | | | | | | | | | | | |
| 4- | | | | | X | X | X | | | | | | | | | | | | | |
| 5- | | | | | | X | X | X | | | | | | | | | | | | |
| 6- | | | | | | | X | X | | | | | | | | | | | | |
| 7- | | | X | X | X | X | X | X | | | | | | | | | | | | |
| 8- | | | | | | | | X | X | | | | | | | | | | | |
| 9- | | | | | | | | | | | X | X | | | | | | | | |
| 10- | | | | | | | | | | | | | X | | | | | | | |
| 11- | | | | | | | | | | | | | | X | X | | | | | |
| 12- | | | | | | | | | | | | | | | X | X | | | | |
| 13- | | | | | | | | | | | | | | | | X | X | | | |
| 14- | | | | | | | | | | | | | | X | X | X | X | X | | |
| 15- | | | | | | | | | | | | | | | | | | | X | X |

Tabela 1 – Cronograma de atividades para TCC I e II, com subdivisão quinzenal indicando tarefas realizadas e planejadas ao longo dos dois semestres.
Fonte: elaborado pelo autor (2026).

# 5 Considerações finais

A confiabilidade de agentes baseados em modelos de linguagem que operam em múltiplas etapas depende da integridade do estado persistido ao longo da interação. Embora a representação desse estado em checkpoints JSON atualizados pelo método GU-JSON ofereça uma estrutura explícita e compacta sob memória limitada, a necessidade de regenerar todo o objeto a cada turno torna o estado vulnerável a falhas sintáticas e à perda ou distorção de informações. Investigar se modelos de linguagem compactos são capazes de executar essa reescrita com fidelidade — e como diferentes paradigmas gerativos se comportam nessa função — constitui um passo necessário para viabilizar componentes locais de memória em sistemas agênticos.

Para responder a essa questão, este projeto delineou um protocolo experimental controlado sobre o benchmark de sumarização incremental de entidades SUMIE, mantendo fixos o método GU-JSON, o schema JSON, o prompt *zero-shot* e o limite de saída de 1.200 tokens, e variando exclusivamente o modelo escritor entre três representantes na escala de 0,6 bilhão de parâmetros: Qwen3-0.6B (autoregressivo *decoder-only*), T5Gemma B-B (*encoder-decoder*) e Qwen3-0.6B BD3LM (difusão em blocos). Ao dissociar a conformidade estrutural (*JSON Validity* e *Schema Validity*) da fidelidade semântica do estado (*State Precision*, *Recall*, *F1* e *Hallucination Rate*) e das acurácias por tipo de operação (`PRESERVE`, `ADD` e `UPDATE`), o desenho permite caracterizar com precisão os modos de falha de cada escritor ao longo dos turnos.

Os resultados do experimento estão circunscritos aos três representantes avaliados, ao formato plano de pares atributo-valor e à avaliação por transições com estado anterior de referência, não devendo ser interpretados como prova causal isolada sobre arquiteturas nem generalizados diretamente para diálogos abertos de longo prazo. Como desdobramentos futuros, destacam-se a avaliação da atualização em regime autoregressivo encadeado — no qual o estado gerado pelo próprio escritor em $t-1$ alimenta o turno $t$, permitindo medir o acúmulo composto de erros —; a extensão do protocolo para cenários de substituição temporal explícita de fatos (*supersession*), como o FactConsolidation-SH; a comparação com métodos que atualizam apenas caminhos específicos do JSON, como o CoK-JSON; e a análise do impacto de decodificação restrita por gramática sobre cada paradigma gerativo.

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
  