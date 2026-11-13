# Mapeamento sistemático de trabalhos relacionados: escritores compactos de memória JSON

**Recorte:** 1º de julho de 2025 a 12 de novembro de 2026, inclusive.  
**Data da busca e da triagem:** 12 de novembro de 2026.  
**Objeto:** atualização incremental de estados estruturados, modelos compactos como escritores de memória e geração estruturada por diferentes paradigmas.

Este arquivo complementa o artigo do TCC e não altera seu texto. Esta é a **versão 2** do mapeamento. A versão anterior examinava apenas os 20 a 25 primeiros resultados de consultas em linguagem livre ordenadas por relevância. Os totais informados pelas bases nessas consultas, como 361.695 no Crossref, não delimitavam o universo de busca: mediam apenas a correspondência parcial de termos. Também não era possível auditar a triagem. Esta versão substitui esse procedimento por um protocolo calibrado com estudos de controle, strings booleanas aplicadas a título e resumo e recuperadas integralmente, *snowballing* e triagem de todos os candidatos pela leitura de título e resumo.

## 1. Metodologia do mapeamento

### 1.1 Objetivo e perguntas

O mapeamento procurou identificar e classificar trabalhos próximos da comparação de modelos compactos como escritores de um *checkpoint* JSON atualizado pelo método *Generate-Update* (GU-JSON), no conjunto SUMIE.

- **QP1 — Representação e atualização:** como os estudos representam a memória e como incorporam, preservam, substituem ou removem informações?
- **QP2 — Modelos:** quais estudos empregam modelos compactos para escrever ou gerir memória, e quais comparam geração autoregressiva e por difusão?
- **QP3 — Avaliação:** quais trabalhos inspecionam diretamente o estado após as atualizações e quais avaliam principalmente respostas ou tarefas posteriores?
- **QP4 — Posicionamento:** em que aspectos os estudos se aproximam ou se afastam do protocolo proposto no TCC?

O protocolo segue as diretrizes de mapeamento sistemático de Petersen et al. (2008; 2015) e de revisão de Kitchenham et al. (2010). A construção e a validação das strings seguem o procedimento de *quasi-gold standard* (QGS) de Zhang, Babar e Tell (2011). O *snowballing* segue Wohlin (2014). A forma de relatar o trabalho se apoia em Prodanov e Freitas (2013). Os textos metodológicos foram consultados em `artigos\01-metodologia-revisao` e `artigos\05-metodologia-e-escrita-cientifica`.

### 1.2 Calibração com estudos conhecidos

As strings e os critérios foram derivados dos estudos já selecionados, citados e analisados, e não de termos escolhidos *a priori*.

1. **Conjunto de controle positivo (QGS):** reuniu os 29 estudos recentes do corpus anterior, E01–E29 na seção 5.2. Para cada estudo, título, resumo, data e referências foram obtidos no OpenAlex.
2. **Conjunto de controle negativo:** reuniu os 213 registros excluídos na versão anterior.
3. **Análise de termos:** foram comparadas as frequências de termos nos dois conjuntos. A palavra “memory” aparecia em 63% dos negativos e, sozinha, não discriminava os grupos. Os termos discriminantes eram combinações como *memory update*, *structured memory*, *small language model* e *diffusion language model*, associadas a agentes ou modelos de linguagem.
4. **Diagnóstico da triagem anterior:** o critério antigo I1, aplicado mecanicamente, aceitava 95 dos 213 registros excluídos. Entre eles estavam estudos claramente pertinentes, como *Small Language Models as Persistent Memory Controllers*, *MemFlow*, *SF-AMS* e *When Memory Updates but Behavior Does Not*. As exclusões anteriores eram, portanto, inconsistentes. Na nova triagem, {{NEG_CORE}} desses registros foram classificados como CORE (seção 1.6).
5. **Sensibilidade das strings:** o objetivo era recuperar pelo menos 80% do QGS, em linha com a faixa de referência de Zhang, Babar e Tell (2011). A sensibilidade observada é apresentada na seção 1.3.

### 1.3 Fontes, strings e recuperação

**Fontes.** Foram usadas duas bases bibliográficas abertas com indexação ampla de anais, periódicos e *preprints* de computação: **OpenAlex** e **Semantic Scholar**. O Crossref, usado na versão anterior, foi substituído pelo Semantic Scholar porque não oferece busca booleana restrita a título e resumo. ACL Anthology, arXiv, PMLR, ICLR e as páginas dos estudos serviram apenas para verificar metadados dos itens do Quadro 1.

**Strings.** As seis strings abaixo cobrem as facetas das questões de pesquisa. No OpenAlex, foram aplicadas por `filter=title_and_abstract.search:<string>,from_publication_date:2025-07-01,to_publication_date:2026-11-12`. No Semantic Scholar, foram aplicadas por `/paper/search/bulk` com a sintaxe equivalente: `+` corresponde a AND, `|` a OR e o filtro usado foi `publicationDateOrYear=2025-07-01:2026-11-12`.

Seja `LM = ("language model" OR "language models" OR LLM OR LLMs OR SLM OR SLMs OR agent OR agents OR agentic)`.

{{TABELA_STRINGS}}

**Recuperação integral.** Diferentemente da versão anterior, foram coletados **todos** os registros retornados por cada string, sem corte por ranking:

| String | OpenAlex: total = coletados | Semantic Scholar: total = coletados |
|---|---:|---:|
{{TABELA_RECUPERACAO}}

No OpenAlex, a paginação foi feita com `page=` e `per-page=200`, totalizando {{OA_PAGINAS}} páginas. A paginação por `cursor` exige chave de API, que não estava disponível. No Semantic Scholar, a paginação foi feita por `token`.

**Sensibilidade frente ao QGS.** As strings do OpenAlex recuperaram **{{QGS_OA}} dos {{QGS_N}}** estudos de controle ({{QGS_OA_PCT}}). Ficaram fora: {{QGS_OA_FALTANTES}}. As strings do Semantic Scholar recuperaram **{{QGS_S2}} dos {{QGS_N}}** ({{QGS_S2_PCT}}); as perdas decorreram sobretudo de anais de 2026 ainda não indexados com data. A união das bases com o *snowballing* recuperou **{{QGS_UNIAO}} dos {{QGS_N}}**. Durante a calibração, *persistent memory* e *writable memory* foram acrescentados a S1 porque MemTxn não era recuperado sem esses termos.

**Snowballing.** No Semantic Scholar, foram coletadas as citações recebidas (*forward*) e as referências (*backward*) de {{SB_N}} sementes: os quatro fundamentos F1–F4 e E01–E09. Só entraram registros com data exata dentro do recorte. Registros no recorte por semente (*forward*/*backward*): {{SB_DETALHE}}. Sementes não resolvidas no Semantic Scholar, nem por título nem por DOI: {{SB_NAO_RESOLVIDAS}}. O *snowballing* acrescentou **{{ORIG_SB}} registros** que não haviam sido recuperados pelas strings; **{{SB_CORE}}** deles foram classificados como CORE.

### 1.4 Deduplicação e pré-triagem por regras

Os registros das duas bases e do *snowballing* foram unidos por DOI e por título normalizado, com minúsculas e sem caracteres não alfanuméricos. Restaram **{{TOTAL}} registros únicos**:

| Origem | Registros |
|---|---:|
| OpenAlex e Semantic Scholar | {{ORIG_AMBAS}} |
| Somente OpenAlex | {{ORIG_OA}} |
| Somente strings do Semantic Scholar | {{ORIG_S2}} |
| Somente *snowballing* | {{ORIG_SB}} |
| Somente sementes dirigidas | {{ORIG_SEED}} |

Em seguida, regras léxicas executáveis organizaram os registros em três faixas. Uma faceta temática T1–T5 só era reconhecida quando os termos coocorriam na mesma frase. As regras também aplicavam as exclusões E2–E6 e verificavam o critério G1. O resultado foi: **núcleo provável = {{TIER_CORE}}**, **contexto = {{TIER_CONTEXT}}** e **excluído = {{TIER_EXCL}}**.

Essa pré-triagem serviu **apenas para priorizar e organizar** os registros, não como filtro final. Em uma auditoria preliminar, estudos centrais, como *Agent-Controlled Forgetting*, *RGMem* e *Causally Sound Memory Invalidation*, apareceram nas faixas de contexto ou exclusão. Por isso, todos os registros do núcleo e do contexto foram lidos, assim como os {{LIDOS_EXCL}} excluídos que não tinham resumo e tinham termos de memória no título.

### 1.5 Critérios de seleção

Os critérios foram reformulados com base no QGS. A versão anterior aceitava qualquer estudo que tratasse de memória; a atual exige que o estudo trate da **escrita ou atualização** da memória, de **escritores compactos**, de **estado estruturado incremental** ou de **geração estruturada por compactos ou por difusão**.

**Critérios gerais.** CORE e CONTEXT exigem os três critérios:

- **G1:** o estudo usa modelos de linguagem (LLM, SLM ou dLLM) ou agentes baseados neles.
- **G2:** é um estudo primário, como método, sistema, *benchmark* ou avaliação empírica.
- **G3:** o objeto é memória ou estado **textual** de modelos de linguagem, ou geração estruturada textual.

**Critérios de inclusão no núcleo.** CORE exige pelo menos um destes critérios:

| Código | Critério |
|---|---|
| IC1 | **Atualização de memória:** propõe, analisa ou avalia como a memória ou o estado persistente é escrito, atualizado, revisado, consolidado, substituído, reconciliado diante de conflitos ou esquecido. Armazenar e recuperar informações não basta. |
| IC2 | **Escritor compacto:** um modelo de até cerca de 4B parâmetros escreve, extrai, atualiza ou gerencia a memória. |
| IC3 | **Estado estruturado incremental:** a memória tem estrutura explícita, como JSON, esquema, entidades e atributos, tabela, registros tipados ou grafo de fatos, e é mantida ao longo de várias entradas, turnos ou sessões. Inclui sumarização incremental de entidades. |
| IC4 | **Geração estruturada por compactos ou difusão:** inclui geração de JSON, esquemas ou chamadas de ferramenta por SLMs ou por modelos de difusão, e comparações entre geração autoregressiva e por difusão em tarefas estruturadas ou agênticas. |

**CONTEXT.** Inclui estudos sobre memória de agentes baseados em modelos de linguagem que não atendem a IC1–IC4. Exemplos: estudos centrados em recuperação ou RAG, arquiteturas gerais, memória procedural ou de experiências e *benchmarks* de recordação que não medem atualização. Esses estudos entram nas contagens, mas não nos quadros.

**Exclusão.**

| Código | Motivo |
|---|---|
| E1 | Fora do recorte temporal |
| E2 | Memória no sentido computacional: KV cache, VRAM, quantização ou hardware |
| E3 | Estudo secundário: *survey*, revisão, posição, tutorial ou visão |
| E4 | Modalidade principal não textual: vídeo, imagem, GUI, robótica ou áudio |
| E5 | Foco principal em segurança, privacidade, ataques, envenenamento ou *unlearning* |
| E6 | Aplicação de domínio em que o modelo de linguagem ou a memória é apenas ferramenta |
| E8 | Informação insuficiente para decidir |
| E9 | Fora do tema |

**Relevância dos estudos CORE.**

- **3 — diretamente comparável ao TCC:** avalia a fidelidade ou correção do estado após atualizações; ou usa SLM como escritor ou gestor de memória com avaliação; ou atualiza incrementalmente um estado estruturado; ou compara paradigmas gerativos em geração estruturada.
- **2:** atende a um critério IC, mas usa tarefa ou medida distante da do TCC.
- **1:** atende a um critério IC apenas de forma secundária.

Em caso de dúvida entre CORE e CONTEXT, foi escolhido CORE com relevância 1, como medida de inclusão conservadora. Não houve restrição de idioma nem exigência de revisão por pares. *Preprints* e depósitos em Zenodo ou Research Square foram identificados pelo DOI e não foram tratados como evidência consolidada.

### 1.6 Triagem por leitura e concordância

Os {{LIDOS}} registros lidos foram divididos em {{LOTES_N}} lotes de {{LOTE_MIN}} a {{LOTE_MAX}} registros, embaralhados com sementes fixas. Cada lote foi triado por um agente de IA (GitHub Copilot), que leu título e resumo e aplicou o roteiro acima. Para cada registro, o agente registrou decisão, códigos, relevância e justificativa curta. Os {{QGS_N}} estudos do QGS foram distribuídos nos lotes sem marcação e, assim, funcionaram como **controles ocultos**.

| Medida | Resultado |
|---|---|
| Controles do QGS classificados como CORE | **{{CTRL_CORE}} de {{QGS_N}}** ({{CTRL_CORE_PCT}}) |
| Controles do QGS classificados como CORE ou CONTEXT | **{{CTRL_CORE_CTX}} de {{QGS_N}}** ({{CTRL_CORE_CTX_PCT}}); MemoryArena foi classificado como CONTEXT por avaliar o uso da memória, não sua atualização |
| Controle excluído | PRISM, excluído automaticamente por E1 porque o OpenAlex informa somente o ano de 2025 no campo de data. Foi publicado no EMNLP em novembro de 2025 e mantido por inclusão dirigida |
| {{NEG_N}} exclusões da versão anterior | {{NEG_RECUP}} foram recuperadas pelas novas strings: **{{NEG_CORE}} CORE**, {{NEG_CTX}} CONTEXT e {{NEG_EXC}} EXCLUDE. As outras {{NEG_NAO_RECUP}} não foram recuperadas pelas strings booleanas |
| Concordância da leitura com as regras | Núcleo provável: {{TX_core_CORE}} CORE, {{TX_core_CONTEXT}} CONTEXT e {{TX_core_EXCLUDE}} EXCLUDE. Contexto: {{TX_context_CORE}} CORE, {{TX_context_CONTEXT}} CONTEXT e {{TX_context_EXCLUDE}} EXCLUDE. Excluídos sem resumo: {{TX_excluded_CORE}} CORE, {{TX_excluded_CONTEXT}} CONTEXT e {{TX_excluded_EXCLUDE}} EXCLUDE |

{{AUDITORIA}}

### 1.7 Fluxo e resultados

```text
{{FLUXO}}
```

**Distribuição dos {{CORE}} estudos CORE.** Por critério, há {{CORE_IC1}} estudos em IC1, {{CORE_IC3}} em IC3, {{CORE_IC4}} em IC4 e {{CORE_IC2}} em IC2; um estudo pode ter mais de um código. Por período, {{CORE_2025}} são do segundo semestre de 2025 e {{CORE_2026}} são de 2026. Entre os {{CORE_R3}} estudos de relevância 3, há {{R3_IC1}} em IC1, {{R3_IC3}} em IC3, {{R3_IC2}} em IC2 e {{R3_IC4}} em IC4. A concentração em 2026 e em IC1 indica que a **atualização da memória de agentes** se tornou uma subárea muito ativa. Já as interseções diretamente ligadas ao TCC, como escritor compacto com estado estruturado ou difusão comparada à geração autoregressiva em estado editável, continuam pequenas.

O inventário completo está em [mapeamento_2025_2026_inventario_triagem.csv](./mapeamento_2025_2026_inventario_triagem.csv). Ele contém título, data, link, origem por string ou semente, faixa da pré-triagem, indicação de leitura, decisão, códigos, relevância e justificativa.

### 1.8 Extração e níveis de verificação

- **Nível 1:** os estudos E01–E29 e F1–F4 tiveram metadados confirmados em fonte primária. **T** indica que trechos do texto integral foram examinados; **R** indica síntese baseada em resumo e metadados. T foi atribuído a AMU, EntityBB, LightMem, CAST e Bilgin et al. **NR** significa “não relatado no material verificado”.
- **Nível 2 e Apêndice A:** a coluna de contribuição resume título e resumo e foi redigida na triagem. Escala dos modelos, tarefa e métricas devem ser confirmadas no texto integral antes de qualquer citação no artigo. O símbolo † indica que a base informou apenas o ano.

### 1.9 Ameaças à validade

- **Triagem assistida por IA, sem segundo avaliador humano:** a concordância foi estimada apenas pelos 29 controles ocultos e pela auditoria amostral. Não há coeficiente kappa entre pessoas. A divergência entre regras e leitura mostra que os registros de fronteira são sensíveis ao critério adotado.
- **Cobertura:** foram usadas duas bases. A ACM Digital Library, a IEEE Xplore e o Scopus não foram consultados diretamente; a cobertura de anais pelo OpenAlex e pelo Semantic Scholar atenua essa limitação, mas não a elimina. A sensibilidade das strings foi medida em um QGS construído pelo próprio autor, o que pode superestimá-la.
- **Datas e indexação:** algumas bases registram apenas o ano, como no caso de PRISM. Anais recentes podem ainda não ter data no Semantic Scholar. No *snowballing backward*, referências sem data exata foram descartadas, o que tende a reduzir esse ramo.
- **Exclusões sem leitura:** {{AUTO_EXCL}} registros foram excluídos por regra. A taxa estimada de perdas está na seção 1.6.
- **Proliferação de *preprints*:** grande parte dos estudos de 2026 são *preprints* em arXiv ou depósitos em Zenodo. Os resultados desses estudos não foram verificados e podem mudar.
- **Reprodutibilidade temporal:** as bases mudam continuamente. As strings, os scripts, os *snapshots* e o inventário permitem auditar e reproduzir esta execução, mas uma repetição pode produzir outros totais.
- **Heterogeneidade:** diferenças entre tarefas, modelos e métricas impedem comparar diretamente os resultados numéricos dos estudos.

## 2. Quadros de trabalhos relacionados

### 2.1 Nível 1 — Estudos verificados e proposta

O Quadro 1 mantém a comparação detalhada dos estudos verificados. Na nova triagem, {{CTRL_CORE}} desses estudos foram classificados como CORE, MemoryArena [E19] foi classificado como CONTEXT e PRISM [E01] foi mantido por inclusão dirigida. As referências entre colchetes estão na seção 5. **Não informado** não equivale a **não se aplica**. A última linha apresenta uma proposta, não um resultado experimental.

**Quadro 1 — Comparação dos trabalhos prioritários e da proposta**

| Trabalho e condição | Representação | Atualização | Modelos e escala verificados | Objeto de avaliação | Paradigmas gerativos |
|---|---|---|---|---|---|
| GU-JSON [F1], fundamento | Texto e JSON | Reescrita integral GU e alternativas GO, GM e CoK | Gemini Ultra e Pro | Resumos incrementais sob orçamento | Sem comparação entre paradigmas |
| SUMIE [F2], fundamento | Atributos e valores de entidades | Integra novas observações e preserva perspectivas divergentes | LLMs no estudo original | Fidelidade de resumos de entidades | Sem comparação entre paradigmas |
| Zeng et al. [F3], fundamento | Trechos, triplas, fatos, resumos e combinações | Construção e recuperação | LLMs; escala NR | Efeito da estrutura e recuperação em tarefas finais | Sem comparação identificada |
| JSONSchemaBench [F4], fundamento | Saídas sob JSON Schema | Geração estática; sem estado incremental | Frameworks de decodificação restrita | Cobertura, eficiência e qualidade da saída | Não é comparação de escritores de memória |
| PRISM [E01], 2025, R | Esquema hierárquico tipado | Operações de caminho e valor aplicadas por controlador | LLMs de contexto curto; porte paramétrico NR | Raciocínio de longo alcance | Sem comparação de paradigmas do escritor |
| Intrinsic Memory Agents [E02], 2025, R | Memória contextual por agente; JSON em variantes | Reescrita a partir da memória e das saídas recentes | Sistema multiagente; escala NR | Qualidade das tarefas do sistema | Sem comparação identificada |
| MemoryAgentBench [E03], 2026, R | Diversas memórias de agentes | Interações incrementais e esquecimento seletivo | Diversos agentes | Competências de memória e respostas posteriores | Não isola paradigmas de um escritor JSON |
| DiffuAgent [E04], 2026, R | Sumarização textual e chamadas estruturadas em avaliações distintas | Sumarização de memória; não GU-JSON | Modelos de difusão e autoregressivos de 7–8B | Fluxos agênticos e chamadas de ferramentas | **Sim**; não sobre o mesmo *checkpoint* JSON |
| AMU [E05], 2026, T | Registros estruturados de memória pessoal | Admissão; descartar duplicata; inserir ou fundir atualização | Qwen3.5-2B como gestor padrão | Qualidade da escrita e recuperação | Não compara os paradigmas do TCC |
| LightMem [E06], 2026, T | Memória de curto, médio e longo prazo | Escrita e fusão online; consolidação offline | SLMs locais, Llama-3.2-1B padrão; consolidação offline por LLM | LoCoMo, DialSim, qualidade e eficiência | Não compara os paradigmas do TCC |
| EntityBB [E07], 2026, T | Estado corrente e histórico de entidades | Chamadas `add`/`update`/`reject` e salvaguardas | Qwen3-4B | Coerência factual da sumarização de documentos longos | Não; não é GU-JSON puro |
| CAST [E08], 2026, T | Saídas de agentes de memória em etapas | Decomposição e *scaffolding* de operações | Qwen3-4B principal; Qwen3-0.6B no apêndice | Qualidade da gestão de memória em LoCoMo e MemoryAgentBench | Não compara os três paradigmas; já examina escritor de 0,6B |
| Bilgin et al. [E09], 2026, T | Tabela persistente de lembretes, sob contrato JSON | Reescrita integral versus operações explícitas de adição/remoção | Llama-3.1-8B e Qwen3.5-397B-A17B | Captura, retenção e liberação de lembretes | Não; a ablação de formato relatada usa o modelo maior |
| AgenticLOCI [E10], 2026, R | Estado de deliberação versionado | Acumula versões e atualiza preferências | Qwen2.5-7B | Preservação e atualização de campos, além de recuperação | Sem comparação identificada |
| Supersede [E11], 2026, R | Memória com fatos sujeitos a mudança | Favorece o valor atual e descarta o substituído | Inclui Qwen2.5-3B ajustado | Atualização de conhecimento e respostas atuais | Não; política distinta da acumulação do SUMIE |
| MemTxn [E12], 2026, R | Estado com versões e registros de recuperação | Validação de escrita, resolução temporal e restauração | Modelos de resposta variados; escala NR | Suporte da fonte e recuperação completa após falhas | Não isola um escritor GU-JSON |
| MemTX [E13], 2026, R | Registros com evidência, proveniência e validade | Transações, validação e reparo de consequências | Cinco modelos de três famílias; escalas NR | Segurança de ações e reparo transacional | Não isola um escritor GU-JSON |
| Self-Healing JSON [E14], 2026, R | JSON sob esquema | Geração e reparo estáticos | Modelos compactos de aproximadamente 360M–1,5B | Validade estrutural e correção dos campos | Não avalia atualização de memória |
| Agents of Diffusion [E15], 2026, R | Dados estruturados, inclusive JSON | Geração guiada por otimizador de *prompt* e juiz | Difusão e referências autoregressivas; escala NR | Conformidade e diversidade em geração estruturada | **Sim**; não é GU-JSON |
| CLAG [E16], 2026, R | Memórias agrupadas com perfis | Um SLM roteia novas memórias e organiza grupos | Três modelos compactos; escalas NR | Respostas e robustez da recuperação | Sem comparação identificada |
| Panini [E17], 2026, R | Rede de entidades, eventos e pares de perguntas e respostas | Acumulação e consolidação contínuas | Modelos de linguagem; escala NR | Respostas sobre conhecimento estruturado | Sem comparação identificada |
| Memora [E18], 2026, R | Memórias pessoais evolutivas | Consolidação e esquecimento de fatos inválidos | Quatro LLMs e seis agentes de memória | Lembrar, raciocinar e recomendar; métrica FAMA | Sem comparação identificada |
| **Proposta do TCC** | *Checkpoint* JSON de esquema fixo | Reescrita integral GU-JSON | Qwen3-0.6B, T5Gemma B-B e Qwen3-0.6B BD3LM | Validade e fidelidade por transição, turno e operação no SUMIE | **Sim**, entre representantes compactos sob o mesmo protocolo |

AMU usa **Qwen3-Embedding-0.6B para embeddings**, não como o escritor padrão. No CAST, o resultado com Qwen3-0.6B é adicional ao experimento principal; não deve ser omitido para afirmar que ninguém estudou modelos dessa escala em gestão de memória.

**Quadro 2 — Estudos recentes complementares do corpus verificado**

| Trabalho | Contribuição e distância em relação ao TCC |
|---|---|
| MemoryArena [E19], R; CONTEXT na v2 | Avalia memória em tarefas multi-sessão interdependentes; mede uso da memória para ação, não fidelidade de cada *checkpoint*. |
| MIRIX [E20], R | Coordena atualização e recuperação de seis tipos de memória, inclusive multimodal; avalia o sistema multiagente. |
| Hindsight [E21], R | Distingue fatos, experiências, resumos e crenças, com operações de retenção e reflexão; avalia uma arquitetura completa. |
| BeliefMem [E22], R | Mantém conclusões alternativas e probabilidades atualizadas por evidências; sua política não é a reescrita integral GU-JSON. |
| PAMU [E23], R | Atualiza uma representação de preferências por médias móveis; avalia qualidade de respostas em LoCoMo. |
| StructMem [E24], R | Preserva vínculos entre eventos e consolida conexões temporalmente; focaliza raciocínio temporal e *multi-hop*. |
| COSMIR [E25], R | Agentes executam extração, inferência e refinamento em memória compartilhada; mede respostas em contexto longo. |
| NarraWorld [E26], R | Organiza fatos, crenças de personagens e possíveis desenvolvimentos em grafo rastreável; aplica-se à escrita narrativa. |
| MemWeaver [E27], R | Combina grafo temporal, experiências e passagens de evidência; focaliza raciocínio e recuperação rastreáveis. |
| Evo-Memory [E28], R | Compara módulos de memória em fluxos de tarefas; avalia evolução e reutilização da experiência. |
| EvoMemBench [E29], R | Compara métodos por escopo e conteúdo da memória; não isola a reescrita GU-JSON. |

Fonte dos quadros: elaboração própria a partir das fontes identificadas em 5.1 e 5.2. Para *preprints* e itens lidos somente por resumo, recomenda-se confirmar detalhes experimentais no texto integral antes de incorporar afirmações ao TCC.

### 2.2 Nível 2 — Novos estudos nas interseções do TCC

Os Quadros 3 e 4 trazem estudos CORE de relevância 3 identificados pela nova busca e ausentes do Quadro 1. O Quadro 3 reúne estudos com **escritor ou gestor compacto (IC2)** ou que combinam **difusão com estado editável (IC1 + IC4)**. O Quadro 4 reúne estudos de **geração estruturada por SLMs ou modelos de difusão (IC4)**. A contribuição foi extraída de título e resumo.

**Quadro 3 — Escritores e gestores compactos de memória e estado editável por difusão ({{Q3_N}} estudos)**

{{QUADRO3}}

**Quadro 4 — Geração estruturada por modelos compactos ou por difusão ({{Q4_N}} estudos)**

{{QUADRO4}}

Os outros {{R3_OUTROS}} estudos CORE de relevância 3, majoritariamente IC1 ou IC1 + IC3, tratam de atualização, revisão, supersessão, consolidação e esquecimento em memórias de agentes baseados em LLMs de grande porte. Eles estão listados no Apêndice A.

## 3. Síntese crítica e posicionamento da proposta

**A atualização da memória tornou-se um objeto explícito de avaliação.** Dos {{CORE}} estudos CORE, {{CORE_IC1}} tratam da escrita ou atualização da memória. Uma parte relevante deixa de medir apenas respostas finais e passa a medir o estado após atualizações. Exemplos são Supersede (lacuna de atualização com fatos substituídos), STALE (validade de memórias obsoletas), MemOps (operações do ciclo de vida da memória), MemTrace (estado atual, estado anterior e trajetória), *Can Agent Memory Systems Track Evolving State?*, DRIFTBENCH (fidelidade da atualização) e CreatorMemBench (memória mutável). Isso reforça a escolha do TCC de avaliar cada transição, e não apenas a resposta final. Ao mesmo tempo, enfraquece qualquer afirmação de que “a atualização não é avaliada”.

**Já há bastante evidência com escritores compactos.** O Quadro 3 mostra estudos em que modelos de até cerca de 4B extraem, escrevem ou gerenciam memória:

- MemReader-0.6B produz entradas estruturadas consistentes com esquema, e MemReader-4B decide escritas.
- DimMem ajusta um extrator Qwen3-4B.
- MemLoRA usa adaptadores para operações de extração e atualização.
- *A Model That Does Not Forget* usa um *logbook* versionado com Qwen3-0.6B.
- truthllm e *Truth for Believable AI* usam um armazém de crenças com revisão e Qwen2.5-0.5B.
- *Learning from the User* usa um SLM de 352M.
- O *Prospective Intention Store* usa estado tipado com Gemma-E2B.
- *Memory That Doesn't Expire* varia o extrator de 3B a 14B e encontra degradação com a redução da escala, principalmente no ancoramento temporal.

Também estão no corpus LightMem, AMU, CAST e CLAG (Quadro 1). Portanto, a novidade do TCC **não** está em usar SLMs como escritores de memória.

**Ainda são poucas as comparações de paradigmas gerativos sobre estado editável.** DiffuPlan mantém um estado de planejamento editável em um agente de difusão. Sob os mesmos dados e treinamento, a edição melhora o agente de difusão em 2,44 F1 e o modelo autoregressivo de origem em 0,47. Plan-and-Patch compara DreamReasoner-8B, de difusão, com Qwen3-8B, autoregressivo, no reparo localizado de planos: a taxa de sucesso foi de 53,7% contra 27,0% sem treino específico. Esses são os achados **mais próximos da pergunta sobre paradigmas**. Mesmo assim, Plan-and-Patch usa modelos de 8B, e o resumo de DiffuPlan não informa a escala. Os dois tratam de planos ou estado de busca, não de memória de entidades, e trabalham com reparo de regiões, não com a reescrita integral GU-JSON. DiffuAgent [E04] e *Agents of Diffusion* [E15] também comparam ou aplicam difusão em tarefas estruturadas, mas não sobre o mesmo *checkpoint*.

**Validade sintática e correção semântica precisam ser separadas.** *Constrained Decoding Eliminates Structural Failures in Small LLMs* compara cinco modelos de 0,6B a 4B. A decodificação restrita eleva a validade de esquema a 100%, mas permanece uma lacuna semântica que depende da escala. *The Constraint Tax* também mede o compromisso entre validade e correção em SLMs com menos de 3B. *Structure Is Cheap, Grounding Is Not* discute o mesmo problema em chamadas de ferramenta com modelos de 103M a 135M. Esses trabalhos sustentam a avaliação do TCC em dois eixos, estrutural e de fidelidade. Também indicam que um JSON válido não basta como critério de sucesso.

**Representação não determina a política de atualização.** PRISM e EntityBB aplicam operações ou salvaguardas; AMU separa duplicação e atualização; MemTxn e MemTX validam e recuperam o estado. Supersede e grande parte dos *benchmarks* de IC1 assumem **supersessão**, ou seja, o valor novo substitui o antigo. No SUMIE, perspectivas divergentes podem coexistir. Tratar automaticamente uma contradição como substituição mudaria a tarefa.

**Lacuna delimitada ao material examinado.** Entre os {{CORE}} estudos CORE, não foi identificado nenhum que compare representantes compactos **autoregressivo, *encoder-decoder* e de difusão em blocos** como escritores do **mesmo *checkpoint* JSON** pelo método GU-JSON. Também não foi identificado estudo que faça essa comparação com esquema, sequências do SUMIE e orçamento de saída controlados, e com análise estrutural e semântica por transição. Os estudos mais próximos cobrem partes do problema: escritor compacto (Quadro 3), difusão com estado editável (DiffuPlan e Plan-and-Patch), validade e semântica em SLMs (Quadro 4) e fidelidade da atualização (Apêndice A). Isso não prova que a comparação inexista fora do material examinado. Como os modelos diferem em família, dados e treinamento, o TCC compara **representantes** e não pode atribuir as diferenças apenas ao paradigma gerativo.

## 4. Texto sugerido para adaptação ao artigo

> Um mapeamento sistemático de {{TOTAL}} registros publicados entre julho de 2025 e novembro de 2026, no OpenAlex e no Semantic Scholar, identificou {{CORE}} estudos primários sobre escrita e atualização de memória, escritores compactos, estado estruturado incremental ou geração estruturada por SLMs e modelos de difusão. Modelos compactos já são usados como escritores ou gestores de memória: por exemplo, LightMem, AMU, MemReader-0.6B e MemReader-4B, DimMem com Qwen3-4B e sistemas com Qwen3-0.6B ou Qwen2.5-0.5B. *Benchmarks* recentes passaram a medir o estado após atualizações, como Supersede, STALE e MemOps. Em paralelo, estudos com SLMs mostram que a decodificação restrita garante validade de esquema sem garantir correção semântica. Comparações entre difusão e geração autoregressiva sobre estado editável surgiram em planejamento, com DiffuPlan e Plan-and-Patch, este último com modelos de 8B. No conjunto examinado, continua específica a comparação de representantes compactos autoregressivo, *encoder-decoder* e de difusão em blocos como escritores do mesmo esquema GU-JSON no SUMIE, com avaliação estrutural e semântica a cada transição.

Antes de usar esse trecho no artigo, confirmar nos textos integrais os detalhes dos estudos de Nível 2 citados e importar as referências no Zotero. Não foram criadas chaves Pandoc ou Better BibTeX.

## 5. Referências

### 5.1 Fundamentos anteriores ao recorte

- **[F1]** HWANG, EunJeong et al. *Enhancing Incremental Summarization with Structured Representations*. Findings of EMNLP, 2024. [DOI](https://doi.org/10.18653/v1/2024.findings-emnlp.220).
- **[F2]** HWANG, Eunjeong et al. *SUMIE: A Synthetic Benchmark for Incremental Entity Summarization*. COLING, janeiro de 2025; *preprint* de 2024. [ACL Anthology](https://aclanthology.org/2025.coling-main.721/).
- **[F3]** ZENG, Ruihong et al. *On the Structural Memory of LLM Agents*. *Preprint*, 2024. [arXiv:2412.15266](https://arxiv.org/abs/2412.15266).
- **[F4]** GENG, Saibo et al. *JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models*. *Preprint*, janeiro de 2025. [arXiv:2501.10868](https://arxiv.org/abs/2501.10868).

### 5.2 Estudos recentes selecionados

- **[E01]** JAYALATH, Dulhan et al. *PRISM: Efficient Long-Range Reasoning With Short-Context LLMs*. EMNLP, 2025; *preprint* de 2024. [DOI](https://doi.org/10.18653/v1/2025.emnlp-main.517).
- **[E02]** YUEN, Sizhe et al. *Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory*. *Preprint*, 2025, versão revista em 2026. [arXiv:2508.08997](https://arxiv.org/abs/2508.08997).
- **[E03]** HU, Yuanzhe; WANG, Yu; McAULEY, Julian. *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*. ICLR, 2026; *preprint* de 2025. [Anais ICLR](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fd1eff9dd295df50a41f2521942fa31d-Abstract-Conference.html).
- **[E04]** LU, Qingyu et al. *The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Reality Check*. ACL, 2026. [DOI](https://doi.org/10.18653/v1/2026.acl-long.2036).
- **[E05]** HWANG, Tao; DIAO, Yishi. *AMU: Admission and Memory Update for Personalized Conversations — Structured Memory with SLM Guided Control*. NORA, 2026. [DOI](https://doi.org/10.18653/2026.nora-1.1).
- **[E06]** ZHANG, Jiaquan et al. *Lightweight LLM Agent Memory with Small Language Models*. ACL, 2026. [DOI](https://doi.org/10.18653/v1/2026.acl-long.588).
- **[E07]** LIU, Ruyi et al. *Entity Blackboard: Structured Agent Memory for Long Document Summarization*. Findings of EMNLP, 2026. [DOI](https://doi.org/10.18653/2026.findings-emnlp.384).
- **[E08]** YANG, Seunghan et al. *From Monolithic Prompts to Scaffolded Execution for Memory Agents with Small Language Models*. Findings of EMNLP, 2026. [DOI](https://doi.org/10.18653/2026.findings-emnlp.968).
- **[E09]** BILGIN, Deniz; SCHEWIOR, Jonas; WENDEMUTH, Andreas. *Capture Is Easy, Forgetting Is Hard: Benchmarking Prospective Memory in Conversational Agents*. REALM, 2026. [DOI](https://doi.org/10.18653/2026.realm-1.43).
- **[E10]** SCHEWIOR, Jonas et al. *AgenticLOCI: A Multi-Agent Memory Framework for Conversational AI with Longitudinal Personalization*. REALM, 2026. [DOI](https://doi.org/10.18653/2026.realm-1.42).
- **[E11]** PATEL, Vedant. *Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents*. *Preprint*, 2026. [arXiv:2606.27472](https://arxiv.org/abs/2606.27472).
- **[E12]** CUI, Hanshuai et al. *MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory*. *Preprint*, 2026. [arXiv:2607.27834](https://arxiv.org/abs/2607.27834).
- **[E13]** LI, Xiaoyang et al. *MemTX: Transactional Belief Commit for Stateful Agent Memory*. *Preprint*, 2026. [arXiv:2607.23929](https://arxiv.org/abs/2607.23929).
- **[E14]** ABDELRAHMAN, Ahmad. *Self-Healing JSON Generation in Small Language Models: A Systematic Evaluation of Syntax Repair, Schema Coercion, and Validator Feedback*. *Preprint*, Research Square, 2026. [DOI](https://doi.org/10.21203/rs.3.rs-11641294/v1). O Crossref registra “Ahmad”; o OpenAlex apresenta grafia divergente.
- **[E15]** KHANAL, Aja et al. *Agents of Diffusion: Enhancing Diffusion Language Models with Multi-Agent Reinforcement Learning for Structured Data Generation*. AAMAS, 2026. [DOI](https://doi.org/10.65109/GGJL7344); [versão estendida](https://arxiv.org/abs/2601.07152).
- **[E16]** ROH, Taeyun et al. *CLAG: Adaptive Memory Organization via Agent-Driven Clustering for Small Language Model Agents*. Findings of ACL, 2026. [DOI](https://doi.org/10.18653/v1/2026.findings-acl.824).
- **[E17]** RAJESH, Shreyas et al. *Panini: Continual Learning in Token Space via Structured Memory*. *Preprint*, 2026. [arXiv:2602.15156](https://arxiv.org/abs/2602.15156).
- **[E18]** UDDIN, Md Nayem et al. *From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents*. Findings of ACL, 2026. [DOI](https://doi.org/10.18653/v1/2026.findings-acl.1337).
- **[E19]** HE, Zexue et al. *Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks*. ICML/PMLR, 2026. [Anais PMLR](https://proceedings.mlr.press/v306/he26am.html); [preprint MemoryArena](https://arxiv.org/abs/2602.16313).
- **[E20]** WANG, Yu; CHEN, Xi. *MIRIX: Multi-Agent Memory System for LLM-Based Agents*. *Preprint*, 2025. [arXiv:2507.07957](https://arxiv.org/abs/2507.07957).
- **[E21]** LATIMER, Chris et al. *Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects*. *Preprint*, 2025. [arXiv:2512.12818](https://arxiv.org/abs/2512.12818); [demonstração relacionada em ACL 2026](https://aclanthology.org/2026.acl-demo.27/).
- **[E22]** LIAO, Junfeng et al. *Belief Memory: Agent Memory Under Partial Observability*. *Preprint*, 2026. [arXiv:2605.05583](https://arxiv.org/abs/2605.05583).
- **[E23]** SUN, Haoran; ZHANG, Zekun; ZENG, Shaoning. *Preference-Aware Memory Update for Long-Term LLM Agents*. Findings of ACL, 2026. [DOI](https://doi.org/10.18653/v1/2026.findings-acl.38).
- **[E24]** XU, Buqiang et al. *StructMem: Structured Memory for Long-Horizon Behavior in LLMs*. ACL, 2026. [DOI](https://doi.org/10.18653/v1/2026.acl-short.12).
- **[E25]** GUPTA, Naman et al. *COSMIR: Chain Orchestrated Structured Memory for Iterative Reasoning over Long Context*. *Preprint*, 2025. [arXiv:2510.04568](https://arxiv.org/abs/2510.04568).
- **[E26]** TIAN, Qiuyu et al. *Shared Worlds, Private Minds: Structured Memory for Long-Form Writing as World Creation*. *Preprint*, 2026. [arXiv:2609.32401](https://arxiv.org/abs/2609.32401).
- **[E27]** YE, Juexiang et al. *MemWeaver: Weaving Hybrid Memories for Traceable Long-Horizon Agentic Reasoning*. *Preprint*, 2026. [arXiv:2601.18204](https://arxiv.org/abs/2601.18204).
- **[E28]** WEI, Tianxin et al. *Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory*. *Preprint*, 2025. [arXiv:2511.20857](https://arxiv.org/abs/2511.20857).
- **[E29]** WANG, Yuyao et al. *EvoMemBench: Benchmarking Agent Memory from a Self-Evolving Perspective*. *Preprint*, 2026; aceito para NeurIPS 2026 segundo o registro consultado. [arXiv:2605.18421](https://arxiv.org/abs/2605.18421).
### 5.3 Referências metodológicas

- PETERSEN, Kai et al. *Systematic Mapping Studies in Software Engineering*. EASE, 2008. [DOI](https://doi.org/10.14236/ewic/EASE2008.8).
- PETERSEN, Kai; VAKKALANKA, Sairam; KUZNIARZ, Ludwik. *Guidelines for conducting systematic mapping studies in software engineering: An update*. Information and Software Technology, 2015. [DOI](https://doi.org/10.1016/j.infsof.2015.03.007).
- KITCHENHAM, Barbara et al. *Systematic literature reviews in software engineering: A tertiary study*. Information and Software Technology, 2010. [DOI](https://doi.org/10.1016/j.infsof.2010.03.006).
- ZHANG, He; BABAR, Muhammad Ali; TELL, Paolo. *Identifying relevant studies in software engineering*. Information and Software Technology, v. 53, n. 6, p. 625–637, 2011. [DOI](https://doi.org/10.1016/j.infsof.2010.12.010).
- WOHLIN, Claes. *Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering*. EASE, 2014. [DOI](https://doi.org/10.1145/2601248.2601268).
- PRODANOV, Cleber Cristiano; FREITAS, Ernani Cesar de. *Metodologia do trabalho científico: métodos e técnicas da pesquisa e do trabalho acadêmico*. 2. ed. Novo Hamburgo: Feevale, 2013. Material disponível na pasta metodológica indicada.

### 5.4 Fontes de dados

- OpenAlex API. [Documentação](https://docs.openalex.org/). Filtro `title_and_abstract.search`.
- Semantic Scholar Academic Graph API. [Documentação](https://api.semanticscholar.org/api-docs/graph). Endpoints `/paper/search/bulk`, `/paper/{id}/citations` e `/paper/{id}/references`.

## Apêndice A — Estudos CORE de relevância 3 ({{CORE_R3}})

Os estudos estão ordenados por combinação de critérios e data. Os Quadros 1, 3 e 4 incluem parte deles. A coluna de contribuição foi extraída de título e resumo. O símbolo † indica que a base informou apenas o ano.

{{APENDICE_A}}

## Apêndice B — Reprodução

Este documento é gerado. O protocolo, os scripts .NET (*file-based apps*), os *snapshots* das bases e as decisões da triagem estão em [mapeamento_sistematico/](./mapeamento_sistematico/README.md). As etapas são:

1. **Calibração:** `dotnet run scripts/mapeamento.cs -- calibrar` obtém no OpenAlex os metadados do QGS ({{QGS_N}} positivos), dos {{NEG_N}} negativos e dos fundamentos.
2. **Coleta:** `sensibilidade`, `coletar-openalex` e `coletar-s2` aplicam as strings S1–S6 do [protocolo](./mapeamento_sistematico/protocolo/protocolo.json) e fazem o *snowballing*.
3. **Pré-triagem e lotes:** `pretriar` deduplica e aplica as regras; `lotes` gera os lotes de leitura e a amostra de auditoria.
4. **Triagem por leitura:** `dotnet run scripts/triagem.cs` envia os lotes ao GitHub Copilot pelo Copilot SDK, com o [roteiro de triagem](./mapeamento_sistematico/protocolo/roteiro_triagem.md) como mensagem de sistema. O script usa apenas os modelos de menor preço por token listados pelo SDK e impõe um teto acumulado de 1.000 créditos de IA, registrado em `custo_llm.jsonl` e repassado ao servidor como limite de sessão.
5. **Consolidação e relatório:** `consolidar` mede a concordância com os controles; `relatorio` gera este documento, o inventário CSV e o RIS.

A execução de {{DATA_EXECUCAO}} pode ser reproduzida sem acesso às bases nem ao LLM com `pwsh mapeamento_sistematico/executar.ps1 -Offline`, que recalcula as etapas 3 e 5 a partir dos *snapshots* e das decisões salvas.

## 6. Arquivos e organização no Zotero

- [Inventário completo da triagem (CSV)](./mapeamento_2025_2026_inventario_triagem.csv): {{TOTAL}} registros com decisão, códigos, relevância e justificativa.
- [RIS do Nível 2](./mapeamento_gu_json_nivel2_2025_2026.ris): {{NIVEL2_N}} estudos dos Quadros 3 e 4. Contém título, data, DOI, URL, resumo e palavras-chave com os critérios. Os autores vêm do Semantic Scholar e constam em {{RIS_AUTORES}} dos {{NIVEL2_N}} registros. Para os demais, após a importação, usar **Recuperar metadados** ou importar pelo DOI no Zotero com “Adicionar item por identificador”.
- [RIS do Nível 1](./mapeamento_gu_json_2025_2026.ris): 29 estudos e quatro fundamentos, total de 33 registros. O arquivo [RIS sem duplicatas conhecidas](./mapeamento_gu_json_novos_2025_2026.ris) contém 24 registros e exclui nove trabalhos que já estavam na biblioteca.
- **Pendências no Zotero 9.0.6, não concluídas nesta sessão:**
  - renomear `01_metodologicosi` para `01_metodologicos`;
  - remover a coleção vazia duplicada na raiz de `tcc_harnes_slm`;
  - importar os arquivos RIS na subcoleção `02_dominio > mapeamento_sistematico_2025_2026`.
- **Limitação técnica:** a API local com gravação exige Zotero 10, e não havia CLI disponível. Não afirmar que os registros já estão na biblioteca antes de confirmar a importação.
