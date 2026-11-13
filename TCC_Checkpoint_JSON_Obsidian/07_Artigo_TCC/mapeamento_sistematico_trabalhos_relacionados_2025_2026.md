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
4. **Diagnóstico da triagem anterior:** o critério antigo I1, aplicado mecanicamente, aceitava 95 dos 213 registros excluídos. Entre eles estavam estudos claramente pertinentes, como *Small Language Models as Persistent Memory Controllers*, *MemFlow*, *SF-AMS* e *When Memory Updates but Behavior Does Not*. As exclusões anteriores eram, portanto, inconsistentes. Na nova triagem, 34 desses registros foram classificados como CORE (seção 1.6).
5. **Sensibilidade das strings:** o objetivo era recuperar pelo menos 80% do QGS, em linha com a faixa de referência de Zhang, Babar e Tell (2011). A sensibilidade observada é apresentada na seção 1.3.

### 1.3 Fontes, strings e recuperação

**Fontes.** Foram usadas duas bases bibliográficas abertas com indexação ampla de anais, periódicos e *preprints* de computação: **OpenAlex** e **Semantic Scholar**. O Crossref, usado na versão anterior, foi substituído pelo Semantic Scholar porque não oferece busca booleana restrita a título e resumo. ACL Anthology, arXiv, PMLR, ICLR e as páginas dos estudos serviram apenas para verificar metadados dos itens do Quadro 1.

**Strings.** As seis strings abaixo cobrem as facetas das questões de pesquisa. No OpenAlex, foram aplicadas por `filter=title_and_abstract.search:<string>,from_publication_date:2025-07-01,to_publication_date:2026-11-12`. No Semantic Scholar, foram aplicadas por `/paper/search/bulk` com a sintaxe equivalente: `+` corresponde a AND, `|` a OR e o filtro usado foi `publicationDateOrYear=2025-07-01:2026-11-12`.

Seja `LM = ("language model" OR "language models" OR LLM OR LLMs OR SLM OR SLMs OR agent OR agents OR agentic)`.

| Código | Faceta | String booleana (sintaxe OpenAlex) |
|---|---|---|
| S1 | Atualização de memória | `LM AND ("memory update" OR "memory updates" OR "memory updating" OR "update memory" OR "updating memory" OR "memory writing" OR "memory write" OR "memory management" OR "memory consolidation" OR "memory maintenance" OR "memory editing" OR "memory evolution" OR "memory forgetting" OR "memory admission" OR "persistent memory" OR "writable memory")` |
| S2 | Modelos compactos | `("small language model" OR "small language models" OR SLM OR SLMs OR "sub-billion" OR "lightweight language model" OR "compact language model") AND (memory OR "structured state" OR checkpoint OR "state tracking")` |
| S3 | Estado estruturado incremental | `("incremental summarization" OR "entity summarization" OR "incremental entity" OR "entity state" OR "structured memory" OR "structured state" OR "memory state") AND ("language model" OR "language models" OR LLM OR LLMs OR agent OR agents)` |
| S4 | Geração estruturada | `(JSON OR "structured output" OR "structured outputs" OR "structured generation" OR "constrained decoding" OR "JSON schema") AND ("small language model" OR "small language models" OR SLM OR SLMs OR "diffusion language model" OR "diffusion language models" OR "masked diffusion" OR "block diffusion" OR "encoder-decoder")` |
| S5 | Difusão em tarefas agênticas | `("diffusion language model" OR "diffusion language models" OR "diffusion LLM" OR "diffusion LLMs" OR dLLM OR dLLMs) AND (agent OR agents OR agentic OR "tool calling" OR "function calling" OR memory OR JSON)` |
| S6 | Avaliação de memória | `(benchmark OR benchmarking OR evaluation) AND ("long-term memory" OR "agent memory" OR "memory update" OR "knowledge update" OR "knowledge updates" OR "multi-session" OR forgetting) AND ("language model" OR "language models" OR LLM OR LLMs OR agent OR agents)` |

**Recuperação integral.** Diferentemente da versão anterior, foram coletados **todos** os registros retornados por cada string, sem corte por ranking:

| String | OpenAlex: total = coletados | Semantic Scholar: total = coletados |
|---|---:|---:|
| S1 | 2.318 (coletados 2.305) | 1.149 |
| S2 | 549 | 307 |
| S3 | 722 | 399 |
| S4 | 193 | 87 |
| S5 | 110 | 92 |
| S6 | 2.832 (coletados 2.819) | 1.786 |
| **Soma (com sobreposição entre strings)** | **6.698** | **3.820** |
| **Registros únicos na base** | **6.082** | **3.726**, incluindo o *snowballing* |

No OpenAlex, a paginação foi feita com `page=` e `per-page=200`, totalizando 36 páginas. A paginação por `cursor` exige chave de API, que não estava disponível. No Semantic Scholar, a paginação foi feita por `token`.

**Sensibilidade frente ao QGS.** As strings do OpenAlex recuperaram **27 dos 29** estudos de controle (93%). Ficaram fora: MemWeaver, PRISM. As strings do Semantic Scholar recuperaram **22 dos 29** (76%); as perdas decorreram sobretudo de anais de 2026 ainda não indexados com data. A união das bases com o *snowballing* recuperou **27 dos 29**. Durante a calibração, *persistent memory* e *writable memory* foram acrescentados a S1 porque MemTxn não era recuperado sem esses termos.

**Snowballing.** No Semantic Scholar, foram coletadas as citações recebidas (*forward*) e as referências (*backward*) de 13 sementes: os quatro fundamentos F1–F4 e E01–E09. Só entraram registros com data exata dentro do recorte. Registros no recorte por semente (*forward*/*backward*): F1 (4/0), F2 (0/0), F3 (31/0), F4 (99/0), E01 (2/0), E02 (16/0), E03 (312/8), E04 (6/6), E06 (15/3), E07 (0/0), E08 (0/0), E09 (0/0). Sementes não resolvidas no Semantic Scholar, nem por título nem por DOI: E05 (AMU). O *snowballing* acrescentou **293 registros** que não haviam sido recuperados pelas strings; **52** deles foram classificados como CORE.

### 1.4 Deduplicação e pré-triagem por regras

Os registros das duas bases e do *snowballing* foram unidos por DOI e por título normalizado, com minúsculas e sem caracteres não alfanuméricos. Restaram **6.298 registros únicos**:

| Origem | Registros |
|---|---:|
| OpenAlex e Semantic Scholar | 3.243 |
| Somente OpenAlex | 2.581 |
| Somente strings do Semantic Scholar | 179 |
| Somente *snowballing* | 293 |
| Somente sementes dirigidas | 2 |

Em seguida, regras léxicas executáveis organizaram os registros em três faixas. Uma faceta temática T1–T5 só era reconhecida quando os termos coocorriam na mesma frase. As regras também aplicavam as exclusões E2–E6 e verificavam o critério G1. O resultado foi: **núcleo provável = 1.103**, **contexto = 1.360** e **excluído = 3.835**.

Essa pré-triagem serviu **apenas para priorizar e organizar** os registros, não como filtro final. Em uma auditoria preliminar, estudos centrais, como *Agent-Controlled Forgetting*, *RGMem* e *Causally Sound Memory Invalidation*, apareceram nas faixas de contexto ou exclusão. Por isso, todos os registros do núcleo e do contexto foram lidos, assim como os 124 excluídos que não tinham resumo e tinham termos de memória no título.

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

Os 2.587 registros lidos foram divididos em 22 lotes de 110 a 124 registros, embaralhados com sementes fixas. Cada lote foi triado por um agente de IA (GitHub Copilot), que leu título e resumo e aplicou o roteiro acima. Para cada registro, o agente registrou decisão, códigos, relevância e justificativa curta. Os 29 estudos do QGS foram distribuídos nos lotes sem marcação e, assim, funcionaram como **controles ocultos**.

| Medida | Resultado |
|---|---|
| Controles do QGS classificados como CORE | **27 de 29** (93%) |
| Controles do QGS classificados como CORE ou CONTEXT | **28 de 29** (97%); MemoryArena foi classificado como CONTEXT por avaliar o uso da memória, não sua atualização |
| Controle excluído | PRISM, excluído automaticamente por E1 porque o OpenAlex informa somente o ano de 2025 no campo de data. Foi publicado no EMNLP em novembro de 2025 e mantido por inclusão dirigida |
| 213 exclusões da versão anterior | 84 foram recuperadas pelas novas strings: **34 CORE**, 8 CONTEXT e 42 EXCLUDE. As outras 129 não foram recuperadas pelas strings booleanas |
| Concordância da leitura com as regras | Núcleo provável: 509 CORE, 81 CONTEXT e 513 EXCLUDE. Contexto: 448 CORE, 204 CONTEXT e 708 EXCLUDE. Excluídos sem resumo: 15 CORE, 8 CONTEXT e 101 EXCLUDE |

**Auditoria dos excluídos sem leitura.** Uma amostra aleatória de 200 dos 3.711 registros excluídos por regra foi lida com o mesmo roteiro. O resultado foi 174 EXCLUDE, 8 CONTEXT e **18 CORE** (9,0%; IC 95% de Wilson: 5,8%–13,8%). Apenas **1** desses registros tem relevância 3 (0,5%; IC 95%: 0,1%–2,8%): *Truth Contradiction-and-Correction Benchmark v1.0*. Extrapolando a amostra, as regras podem ter deixado de fora entre 214 e 511 estudos CORE, em sua maioria de relevância 1 ou 2. Para relevância 3, a estimativa fica entre 3 e 103 estudos. Por isso, as contagens de CORE devem ser lidas como **limite inferior**, e os quadros de Nível 2 não esgotam todos os estudos de relevância 3. As decisões da auditoria estão em `mapeamento_sistematico/dados/<execução>/auditoria/` e não foram somadas às contagens do fluxo.

### 1.7 Fluxo e resultados

```text
Identificação
  OpenAlex, S1–S6: 6.698 ocorrências → 6.082 únicos
  Semantic Scholar, S1–S6 e snowballing: 3.820 ocorrências das strings, mais o snowballing → 3.726 únicos
  Sementes dirigidas: 2
        ↓ deduplicação por DOI e título normalizado
Registros únicos: 6.298
        ↓ pré-triagem por regras, usada para priorização
  Núcleo provável: 1.103 | Contexto: 1.360 | Excluídos: 3.835
        ↓
  Excluídos automaticamente sem leitura: 3.711
    sem faceta temática: 1.638 | E4: 622 | E2: 428 | E5: 408 | E6: 186
    G1: 173 | E3: 158 | sem resumo e sem termo de memória no título: 97 | E1: 1
  Lidos por título e resumo: 2.587 = 1.103 + 1.360 + 124
        ↓
  EXCLUDE após leitura: 1.322
    E9: 534 | E3: 327 | E6: 123 | E4: 104 | E5: 96 | E2: 93 | E8: 45
  CONTEXT: 293
  CORE: 972
    relevância 3: 238 | relevância 2: 425 | relevância 1: 309
        ↓
Síntese
  Nível 1, Quadros 1 e 2: 29 estudos verificados em metadados ou texto e 4 fundamentos
  Nível 2, Quadros 3 e 4: 50 novos estudos CORE de relevância 3 nas interseções do TCC
  Nível 3, Apêndice A: todos os 238 estudos CORE de relevância 3
  Inventário: todos os 6.298 registros com decisão e justificativa
```

**Distribuição dos 972 estudos CORE.** Por critério, há 753 estudos em IC1, 334 em IC3, 100 em IC4 e 65 em IC2; um estudo pode ter mais de um código. Por período, 79 são do segundo semestre de 2025 e 893 são de 2026. Entre os 238 estudos de relevância 3, há 203 em IC1, 113 em IC3, 29 em IC2 e 28 em IC4. A concentração em 2026 e em IC1 indica que a **atualização da memória de agentes** se tornou uma subárea muito ativa. Já as interseções diretamente ligadas ao TCC, como escritor compacto com estado estruturado ou difusão comparada à geração autoregressiva em estado editável, continuam pequenas.

O inventário completo está em [mapeamento_2025_2026_inventario_triagem.csv](./mapeamento_2025_2026_inventario_triagem.csv). Ele contém título, data, link, origem por string ou semente, faixa da pré-triagem, indicação de leitura, decisão, códigos, relevância e justificativa.

### 1.8 Extração e níveis de verificação

- **Nível 1:** os estudos E01–E29 e F1–F4 tiveram metadados confirmados em fonte primária. **T** indica que trechos do texto integral foram examinados; **R** indica síntese baseada em resumo e metadados. T foi atribuído a AMU, EntityBB, LightMem, CAST e Bilgin et al. **NR** significa “não relatado no material verificado”.
- **Nível 2 e Apêndice A:** a coluna de contribuição resume título e resumo e foi redigida na triagem. Escala dos modelos, tarefa e métricas devem ser confirmadas no texto integral antes de qualquer citação no artigo. O símbolo † indica que a base informou apenas o ano.

### 1.9 Ameaças à validade

- **Triagem assistida por IA, sem segundo avaliador humano:** a concordância foi estimada apenas pelos 29 controles ocultos e pela auditoria amostral. Não há coeficiente kappa entre pessoas. A divergência entre regras e leitura mostra que os registros de fronteira são sensíveis ao critério adotado.
- **Cobertura:** foram usadas duas bases. A ACM Digital Library, a IEEE Xplore e o Scopus não foram consultados diretamente; a cobertura de anais pelo OpenAlex e pelo Semantic Scholar atenua essa limitação, mas não a elimina. A sensibilidade das strings foi medida em um QGS construído pelo próprio autor, o que pode superestimá-la.
- **Datas e indexação:** algumas bases registram apenas o ano, como no caso de PRISM. Anais recentes podem ainda não ter data no Semantic Scholar. No *snowballing backward*, referências sem data exata foram descartadas, o que tende a reduzir esse ramo.
- **Exclusões sem leitura:** 3.711 registros foram excluídos por regra. A taxa estimada de perdas está na seção 1.6.
- **Proliferação de *preprints*:** grande parte dos estudos de 2026 são *preprints* em arXiv ou depósitos em Zenodo. Os resultados desses estudos não foram verificados e podem mudar.
- **Reprodutibilidade temporal:** as bases mudam continuamente. As strings, os scripts, os *snapshots* e o inventário permitem auditar e reproduzir esta execução, mas uma repetição pode produzir outros totais.
- **Heterogeneidade:** diferenças entre tarefas, modelos e métricas impedem comparar diretamente os resultados numéricos dos estudos.

## 2. Quadros de trabalhos relacionados

### 2.1 Nível 1 — Estudos verificados e proposta

O Quadro 1 mantém a comparação detalhada dos estudos verificados. Na nova triagem, 27 desses estudos foram classificados como CORE, MemoryArena [E19] foi classificado como CONTEXT e PRISM [E01] foi mantido por inclusão dirigida. As referências entre colchetes estão na seção 5. **Não informado** não equivale a **não se aplica**. A última linha apresenta uma proposta, não um resultado experimental.

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

**Quadro 3 — Escritores e gestores compactos de memória e estado editável por difusão (27 estudos)**

| Trabalho | Data | Critérios | Contribuição e aproximação com o TCC (título e resumo) |
|---|---|---|---|
| [MemLoRA: Distilling Expert Adapters for On-Device Memory Systems](<https://doi.org/10.48550/arxiv.2512.04763>) | 2025-12 | IC1, IC2 | Adaptadores para SLMs executarem operações de memória (extração, atualização) on-device. |
| [PGMem: Tightly Coupled Persona–Memory Graph for Lifelong Personalized Agents](<https://doi.org/10.18653/2026.emnlp-main.1891>) | 2026† | IC1, IC2, IC3 | Grafo persona-memória que revisa personas evolutivas, com backbones SLM. |
| [GRAM: Empowering Agent with Actively Managed Graph-Structured Memory via Reinforcement Learning](<https://doi.org/10.18653/2026.findings-emnlp.1183>) | 2026† | IC1, IC2, IC3 | SLMs <4B treinados por RL para gerir memória em grafo com consolidação. |
| [MemBuilder: Reinforcing LLMs for Long-Term Memory Construction via Attributed Dense Rewards](<https://doi.org/10.18653/v1/2026.acl-long.1284>) | 2026† | IC1, IC2 | RL treina modelo de 4B para construir memória de longo prazo. |
| [InfMem: Learning System-2 Memory Control for Long-Context Agent](<https://doi.org/10.48550/arxiv.2602.02704>) | 2026-02 | IC1, IC2 | Agente escreve/atualiza memória limitada; avaliado com Qwen3-1.7B e 4B. |
| [Epistemic Validation in AI Knowledge Systems: A System-2 Framework for Long-Term Memory](<https://doi.org/10.5281/zenodo.19357817>) | 2026-03 | IC1, IC2 | Validação epistêmica na escrita da memória, inclui validador local 3B |
| [MemReader: From Passive to Active Extraction for Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2604.07877>) | 2026-04 | IC1, IC2, IC3 | SLMs 0.6B/4B extraem e decidem escrita de memória estruturada. |
| [TSUBASA: Improving Long-Horizon Personalization via Evolving Memory and Self-Learning with Context Distillation](<https://doi.org/10.48550/arxiv.2604.07894>) | 2026-04 | IC1, IC2 | Escrita de memória com evolução dinâmica; Qwen3 a partir de 4B avaliado. |
| [Small Language Models as Persistent Memory Controllers for Lightweight LLM Agents](<https://openalex.org/W7220767060>) | 2026-05 | IC1, IC2 | SLM dedicado gerencia codificação, consolidação e sumarização da memória. |
| [DimMem: Dimensional Structuring for Efficient Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2605.15759>) | 2026-05 | IC1, IC2, IC3 | Unidades de memória tipadas com atualização; extrator Qwen3-4B ajustado. |
| [From Facts to Insights: A Persona-Driven Dual Memory Framework and Dataset for Role-Playing Agents](<https://doi.org/10.48550/arXiv.2605.25693>) | 2026-05 | IC2 | Modelo de 4B treinado para gerir memória dual de fatos e insights |
| [EdgeWisePersona: A Dataset for On-Device User Profiling from Natural Language Interactions](<https://doi.org/10.1145/3774935.3806788>) | 2026-06 | IC2, IC3 | SLMs reconstroem perfis estruturados a partir de interações multissessão |
| [G-Long: Graph-Enhanced Memory Management for Efficient Long-Term Dialogue Agents](<https://doi.org/10.48550/arxiv.2606.13115>) | 2026-06 | IC2, IC3 | sLM ajustado extrai triplas para memória em grafo de diálogo longo |
| [CMI-Mem: Toward Generalizable Long-Term Memory Management via CMI-Augmented Reinforcement Learning](<https://doi.org/10.48550/arxiv.2607.20553>) | 2026-07 | IC1, IC2 | Gestor de memória 4B treinado por RL com recompensa por operação. |
| [truthllm: Expression-and-Revision Layer over a Fixed Language Model — Reference Implementation, Benchmark, and Results (v1.0)](<https://doi.org/10.5281/zenodo.21462985>) | 2026-07 | IC1, IC2, IC3 | Armazém de crenças com revisão e benchmark de correção; Qwen 0.5B |
| [Memory That Doesn't Expire: Agentic Long-Term Memory for Conversational Agents on a Single Consumer GPU](<https://doi.org/10.5281/zenodo.21964737>) | 2026-08 | IC1, IC2, IC3 | Modelo local pequeno gerencia fatos tipados, datados e deduplicados |
| [Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation](<https://doi.org/10.48550/arxiv.2608.22215>) | 2026-08 | IC1, IC2 | Roteamento de escrita novo/atualização com cascata 1.7B/8B. |
| [Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents](<https://doi.org/10.48550/arxiv.2609.01272>) | 2026-09 | IC1, IC2, IC3 | Armazém tipado de intenções com ciclo de vida para agentes SLM (Gemma-E2B). |
| [PSD: Pseudo Self-Distillation of Memory Representation Capabilities for LLM Agents](<https://doi.org/10.48550/arxiv.2609.23449>) | 2026-09 | IC2 | SLM destilado para construir representações de memória hierárquica. |
| [Truth for Believable AI: Expressed Doubt, Provenance, and Belief Revision as an Engineerable Stance](<https://doi.org/10.48550/arxiv.2609.26035>) | 2026-09 | IC1, IC2 | Store persistente de revisão de crenças multi-sessão avaliado com Qwen2.5-0.5B. |
| [A Model That Does Not Forget. A Logbook That Corrects and a Sleep That Consolidates, on a Frozen Language Model](<https://doi.org/10.21203/rs.3.rs-11185020/v1>) | 2026-09 | IC1, IC2 | Logbook versionado e consolidação em Qwen3-0.6B; mede retenção de fatos que mudam. |
| [Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing](<https://doi.org/10.48550/arxiv.2610.22196>) | 2026-10 | IC1, IC2 | Escritor de memória MoE com 30B parâmetros totais e ~3B ativos, treinado por destilação e RL; não é SLM em parâmetros totais. |
| [DiffuPlan: Editable Planning State for Diffusion Language Model Agents](<https://doi.org/10.48550/arxiv.2610.24717>) | 2026-10 | IC1, IC4 | dLLM mantém estado de planejamento editável e reconstrói só passos afetados; compara com o modelo AR de origem sob mesmos dados. |
| [Memory, Know Your PLACE: Governing Lifecycle State and Query-Time Eligibility in Persistent-Memory Agents](<https://doi.org/10.48550/arxiv.2610.25179>) | 2026-10 | IC1, IC2 | Governança de escrita certifica estado de memória; Qwen2.5-3B avaliado. |
| [Learning from the User Without Learning Their Mistakes: A Preregistered Study of On-Device Personalisation for a Small Language Model](<https://doi.org/10.5281/zenodo.23485017>) | 2026-10 | IC1, IC2 | SLM 352M com filtro de admissão e nota de fatos do usuário |
| [Trail: Accurate Local Smart Home Control Using Decision Models](<https://doi.org/10.48550/arxiv.2611.00610>) | 2026-10 | IC3, IC4 | SLM local com decisões tipadas e memória estruturada multi-turno avaliada. |
| [Closing the Epistemic Loop Across the Five Layers of Agent Memory: Cryptographic Provenance, Paraconsistent Bilattices, and Z3-Quarantined Procedural Induction](<https://doi.org/10.5281/zenodo.23901682>) | 2026-11 | IC1, IC2, IC3 | Promoção verificada, contradições e supersede em memória; inclui modelos pequenos. |

**Quadro 4 — Geração estruturada por modelos compactos ou por difusão (23 estudos)**

| Trabalho | Data | Critérios | Contribuição e aproximação com o TCC (título e resumo) |
|---|---|---|---|
| [Unveiling the Potential of Diffusion Large Language Model in Controllable Generation](<https://doi.org/10.48550/arXiv.2507.04504>) | 2025-07 | IC4 | dLLM gera JSON confiável via andaime de esquema. |
| [Is Generative AI Hiding in Your Phone? Fine-tuning SLMs to Generate JSON-Adherent Output](<https://openalex.org/W7208795050>) | 2026† | IC4 | Fine-tuning de Qwen3-0.6B para saída JSON conforme esquema. |
| [Dgrammar: Efficient Constrained Decoding for DLMs](<https://doi.org/10.18653/2026.aacl-long.225>) | 2026† | IC4 | Decodificação restrita para modelos de difusão em JSON Schema. |
| [DiffResearch: Accelerating Deep Research with Diffusion Language Models](<https://doi.org/10.18653/2026.emnlp-industry.262>) | 2026† | IC4 | Compara backbone de difusão e autoregressivo em framework agêntico de pesquisa. |
| [DLLM Agent: See Farther, Run Faster](<https://doi.org/10.48550/arxiv.2602.07451>) | 2026-02 | IC4 | Compara difusão × autorregressivo em agentes com uso de ferramentas. |
| [Continuous Diffusion Models Can Obey Formal Syntax](<https://doi.org/10.48550/arxiv.2602.12468>) | 2026-02 | IC4 | Difusão contínua obedecendo sintaxe JSON/regex |
| [ScrapeGraphAI-100k: Dataset for Schema-Constrained LLM Generation](<https://www.semanticscholar.org/paper/171648754cf73825e1074b7838acd943ea5a5991>) | 2026-02 | IC4 | Dataset de geração restrita a esquema JSON; estudante 1,7B ajustado. |
| [Localized Diffusion Repair for Reliable Tool-Using LLM Agents](<https://doi.org/10.1109/ASENS69964.2026.11605180>) | 2026-03 | IC4 | Modelo de difusão repara chamadas de ferramenta JSON; compara com autoregressivo. |
| [The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models](<https://doi.org/10.48550/arxiv.2605.26128>) | 2026-05 | IC4 | Mede validade vs correção em saídas estruturadas de SLMs sub-3B. |
| [Are Diffusion Language Models Good Database Analysts?](<https://doi.org/10.48550/arxiv.2605.27791>) | 2026-05 | IC4 | Compara difusão × autoregressivo em NL2SQL estruturado. |
| [EPIC: Efficient and Parallel Inference under CFG Constraints for Diffusion Language Models](<https://doi.org/10.48550/arxiv.2606.00722>) | 2026-05 | IC4 | Decodificação restrita por gramática em modelos de difusão |
| [Dynamic Infilling Anchors for Format-Constrained Generation in Diffusion Large Language Models](<https://doi.org/10.48448/xmcc-9759>) | 2026-06 | IC4 | Geração com restrição de formato JSON em dLLMs |
| [Small Language Models and Spec-Driven Development for High-Accuracy Agentic AI Systems](<https://doi.org/10.67231/qqk79s36>) | 2026-06 | IC4 | SLMs ajustados para JSON e chamadas de ferramenta com esquema, avaliados. |
| [GenSIE Benchmark v1.0: Schema-Guided Information Extraction with Small Language Models in Spanish](<https://doi.org/10.5281/zenodo.21299326>) | 2026-07 | IC4 | Benchmark de extração JSON guiada por esquema com SLMs e fidelidade. |
| [Structure Is Cheap, Grounding Is Not: Three measurement faults and a negative result in tool calling at 103M-135M parameters](<https://doi.org/10.5281/zenodo.21725247>) | 2026-07 | IC4 | Chamadas de ferramenta por modelos de 103-135M com aterramento em estado. |
| [StructureBench: A Unified Benchmark Suite for Multi-Scenario Structured Generation Tasks with On-Device Models](<https://doi.org/10.24963/ijcai.2026/267>) | 2026-09 | IC4 | Benchmark de geração estruturada e decodificação restrita em modelos on-device. |
| [Resumen de GenSIE en IberLEF 2026: extracción de información guiada por esquemas con modelos de lenguaje pequeños en español](<https://openalex.org/W7222860814>) | 2026-09 | IC4 | Tarefa compartilhada de extração guiada por esquema JSON com SLMs. |
| [Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B Small Language Models for Edge Deployment](<https://doi.org/10.48550/arxiv.2609.07370>) | 2026-09 | IC4 | Benchmark de chamadas de ferramenta JSON em SLMs abaixo de 2B. |
| [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](<https://doi.org/10.48550/arxiv.2609.09476>) | 2026-09 | IC4 | SLMs 270M-1.7B geram chamadas de função com esquemas. |
| [Comparació de models de llenguatge de difusió i auto-regressius](<https://openalex.org/W7212349642>) | 2026-09 | IC4 | Compara difusão e autoregressivo com decodificação restrita e IFEval. |
| [Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap](<https://doi.org/10.48550/arXiv.2609.23742>) | 2026-09 | IC4 | Benchmark de saída estruturada em SLMs 0,6-4B com decodificação restrita. |
| [Plan-and-Patch: Diffusion Language Models for Agentic Planning](<https://doi.org/10.48550/arxiv.2610.10786>) | 2026-10 | IC4 | DreamReasoner-8B (difusão) × Qwen3-8B (AR) na geração e reparo localizado de planos estruturados. |
| [DConstrain: Compiling Context-Parameterized Transitions for Diffusion Language Model Constrained Decoding](<https://doi.org/10.48550/arxiv.2610.30920>) | 2026-10 | IC4 | Decodificação restrita por esquema para modelos de difusão. |

Os outros 173 estudos CORE de relevância 3, majoritariamente IC1 ou IC1 + IC3, tratam de atualização, revisão, supersessão, consolidação e esquecimento em memórias de agentes baseados em LLMs de grande porte. Eles estão listados no Apêndice A.

## 3. Síntese crítica e posicionamento da proposta

**A atualização da memória tornou-se um objeto explícito de avaliação.** Dos 972 estudos CORE, 753 tratam da escrita ou atualização da memória. Uma parte relevante deixa de medir apenas respostas finais e passa a medir o estado após atualizações. Exemplos são Supersede (lacuna de atualização com fatos substituídos), STALE (validade de memórias obsoletas), MemOps (operações do ciclo de vida da memória), MemTrace (estado atual, estado anterior e trajetória), *Can Agent Memory Systems Track Evolving State?*, DRIFTBENCH (fidelidade da atualização) e CreatorMemBench (memória mutável). Isso reforça a escolha do TCC de avaliar cada transição, e não apenas a resposta final. Ao mesmo tempo, enfraquece qualquer afirmação de que “a atualização não é avaliada”.

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

**Lacuna delimitada ao material examinado.** Entre os 972 estudos CORE, não foi identificado nenhum que compare representantes compactos **autoregressivo, *encoder-decoder* e de difusão em blocos** como escritores do **mesmo *checkpoint* JSON** pelo método GU-JSON. Também não foi identificado estudo que faça essa comparação com esquema, sequências do SUMIE e orçamento de saída controlados, e com análise estrutural e semântica por transição. Os estudos mais próximos cobrem partes do problema: escritor compacto (Quadro 3), difusão com estado editável (DiffuPlan e Plan-and-Patch), validade e semântica em SLMs (Quadro 4) e fidelidade da atualização (Apêndice A). Isso não prova que a comparação inexista fora do material examinado. Como os modelos diferem em família, dados e treinamento, o TCC compara **representantes** e não pode atribuir as diferenças apenas ao paradigma gerativo.

## 4. Texto sugerido para adaptação ao artigo

> Um mapeamento sistemático de 6.298 registros publicados entre julho de 2025 e novembro de 2026, no OpenAlex e no Semantic Scholar, identificou 972 estudos primários sobre escrita e atualização de memória, escritores compactos, estado estruturado incremental ou geração estruturada por SLMs e modelos de difusão. Modelos compactos já são usados como escritores ou gestores de memória: por exemplo, LightMem, AMU, MemReader-0.6B e MemReader-4B, DimMem com Qwen3-4B e sistemas com Qwen3-0.6B ou Qwen2.5-0.5B. *Benchmarks* recentes passaram a medir o estado após atualizações, como Supersede, STALE e MemOps. Em paralelo, estudos com SLMs mostram que a decodificação restrita garante validade de esquema sem garantir correção semântica. Comparações entre difusão e geração autoregressiva sobre estado editável surgiram em planejamento, com DiffuPlan e Plan-and-Patch, este último com modelos de 8B. No conjunto examinado, continua específica a comparação de representantes compactos autoregressivo, *encoder-decoder* e de difusão em blocos como escritores do mesmo esquema GU-JSON no SUMIE, com avaliação estrutural e semântica a cada transição.

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

## Apêndice A — Estudos CORE de relevância 3 (238)

Os estudos estão ordenados por combinação de critérios e data. Os Quadros 1, 3 e 4 incluem parte deles. A coluna de contribuição foi extraída de título e resumo. O símbolo † indica que a base informou apenas o ano.

| Trabalho | Data | Critérios | Contribuição e aproximação com o TCC (título e resumo) |
|---|---|---|---|
| [Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions](<https://doi.org/10.48550/arxiv.2507.05257>) | 2025-07 | IC1 | Benchmark de memória incluindo atualização e esquecimento seletivo. |
| [TrustMem: Learning Trustworthy Memory Consolidation for LLM Agents with Long-Term Memory](<https://doi.org/10.18653/2026.findings-emnlp.2419>) | 2026† | IC1 | Consolidação de memória com verificação de fidelidade das atualizações |
| [DeltaMem: Towards Agentic Memory Management via Reinforcement Learning](<https://doi.org/10.18653/2026.emnlp-main.1018>) | 2026† | IC1 | Gestor de memória treinado por RL com rótulos de operações de atualização. |
| [HaluMem: Evaluating Hallucinations in Memory Systems of Agents](<https://doi.org/10.18653/2026.emnlp-main.220>) | 2026† | IC1 | Avalia alucinações em extração e atualização de memória. |
| [A value-aware and conflict-sensitive memory management mechanism for agents in dynamic interaction scenarios](<https://openalex.org/W7167440653>) | 2026† | IC1 | Gestão do ciclo de vida da memória: add, update, merge, archive, suppress com conflitos. |
| [Probing Stability–Plasticity Tradeoffs in Agent Memory through Cognitive Experimental Paradigms](<https://doi.org/10.18653/2026.emnlp-main.2473>) | 2026† | IC1 | Diagnostica como sistemas de memória atualizam, preservam e atribuem fatos. |
| [Remember, Verify, or Ask? Evaluating Memory Decisions at Reuse Time](<https://doi.org/10.18653/2026.nora-1.2>) | 2026† | IC1 | Avalia decisões de persistir, verificar ou perguntar antes de atualizar memória |
| [TimlMemBench: A Diagnostic Benchmark for Governed Use of Long-Term Memory in Dialogue Agents](<https://doi.org/10.18653/2026.findings-emnlp.507>) | 2026† | IC1 | Benchmark de uso governado: revogação, substituição, atualizações de ciclo de vida |
| [AI Agents Need Memory Control Over More Context](<https://doi.org/10.48550/arxiv.2601.11653>) | 2026-01 | IC1 | Estado interno limitado atualizado a cada turno; evita deriva |
| [MemEmo: Evaluating Emotion in Memory Systems of Agents](<https://doi.org/10.48550/arxiv.2602.23944>) | 2026-02 | IC1 | Benchmark avalia extração e atualização de memória emocional em sistemas de memória. |
| [RUMA: Routed Updatable Memory Architecture for Versioned Document Updates](<https://doi.org/10.5281/zenodo.19563610>) | 2026-04 | IC1 | Memória atualizável com supersessão por linhagem e versões. |
| [From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents](<https://doi.org/10.48550/arxiv.2604.20006>) | 2026-04 | IC1 | Benchmark mede consolidação, atualizações e uso de memórias obsoletas. |
| [Evidence-Gated Memory Writing for Personalized Large Language Model Agents](<https://doi.org/10.1109/icipai70034.2026.11605481>) | 2026-05 | IC1 | Portão de escrita por evidência reduz poluição e contradições na memória. |
| [When Not to Write Memory: Governing False Promotion from Correlated Agent Traces](<https://doi.org/10.1109/mlise70044.2026.11607557>) | 2026-05 | IC1 | Governança do caminho de escrita da memória: promover, rejeitar, revisar |
| [MEMAUDIT: An Exact Package-Oracle Evaluation Protocol for Budgeted Long-Term LLM Memory Writing](<https://doi.org/10.48550/arxiv.2605.02199>) | 2026-05 | IC1 | Protocolo exato para avaliar escrita de memória e preservação de validade. |
| [STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?](<https://doi.org/10.48550/arxiv.2605.06527>) | 2026-05 | IC1 | Benchmark de revisão de crenças obsoletas com conflitos implícitos. |
| [CogniCheck: A Lightweight Hybrid Middleware for Memory-Consistent LLM-Driven NPCs](<https://doi.org/10.5281/zenodo.20099466>) | 2026-05 | IC1 | Detecta e resolve contradições de memória; mede estabilidade de crenças |
| [Episodic-Semantic Memory Architecture for Long-Horizon Scientific Agents](<https://doi.org/10.48550/arxiv.2605.17625>) | 2026-05 | IC1 | Consolidação episódico-semântica com evolução contraditória de parâmetros |
| [MINTEval: Evaluating Memory under Multi-Target Interference in Long-Horizon Agent Systems](<https://doi.org/10.48550/arXiv.2605.18565>) | 2026-05 | IC1 | Benchmark de memória sob atualizações frequentes e interferência. |
| [MemTrace: Tracing and Attributing Errors in Large Language Model Memory Systems](<https://doi.org/10.48550/arxiv.2605.28732>) | 2026-05 | IC1 | Rastreia evolução da memória e atribui erros como perda de informação. |
| [SAGE: A Novelty Gate for Efficient Memory Evolution in Agentic LLMs](<https://doi.org/10.48550/arxiv.2605.30711>) | 2026-05 | IC1 | Controle de escrita ADD/merge/NOOP de fatos extraídos na evolução da memória. |
| [Memcurrency: Memory Decay and Refresh Mechanism for Long-Running LLM Agents](<https://doi.org/10.1109/icetis70504.2026.11633479>) | 2026-06 | IC1 | Decaimento e atualização de memória por detecção de conflitos; acurácia temporal. |
| [Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning](<https://doi.org/10.48448/hq9p-kt44>) | 2026-06 | IC1 | Gestor de memória com ADD/UPDATE/DELETE treinado por RL. |
| [MemRefine: LLM-Guided Compression for Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2606.13177>) | 2026-06 | IC1 | LLM decide excluir, fundir ou preservar memórias sob orçamento |
| [Control-Plane Placement Shapes Forgetting: An Architectural Study of Agent Memory Across Thirteen System Configurations](<https://doi.org/10.48550/arxiv.2606.15903>) | 2026-06 | IC1 | Esquecimento e supersessão em memória de agentes; benchmark ForgetEval |
| [MemTrace: Probing What Final Accuracy Misses in Long-Term Memory](<https://doi.org/10.48550/arxiv.2606.17328>) | 2026-06 | IC1 | Benchmark de fatos tipados: estado atual, anterior e trajetória de mudança |
| [Verification-Gated Persona State Transitions for Memory-Augmented Language Agents](<https://doi.org/10.3390/sym18061037>) | 2026-06 | IC1 | Atualização verificada do estado de persona; mede violações após atualizações. |
| [GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents](<https://doi.org/10.48550/arxiv.2606.18829>) | 2026-06 | IC1 | Benchmark avalia atualizações de estado e esquecimento ativo em memória compartilhada |
| [MGBench: Memory Governance Benchmark for Agentic Long-Term Memory](<https://doi.org/10.5281/zenodo.20793096>) | 2026-06 | IC1 | Benchmark de governança: memória obsoleta, invalidada e contraditória. |
| [Are We Ready For An Agent-Native Memory System?](<https://doi.org/10.48550/arxiv.2606.24775>) | 2026-06 | IC1 | Avaliação empírica de 12 sistemas incluindo extração, manutenção e atualizações dinâmicas. |
| [RAMR — Retrieval-Augmented Memory Reliability](<https://doi.org/10.5281/zenodo.20818291>) | 2026-06 | IC1 | Benchmark mede supersessão, valor obsoleto e retenção após atualizações. |
| [Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents](<https://doi.org/10.48550/arxiv.2606.27472>) | 2026-06 | IC1 | Diagnostica e treina lacuna de atualização de memória com fatos substituídos. |
| [Write-Time Trust Gating for LLM Memory Systems: Preventing Hallucination at Write Time through Provenance-Anchored Confidence Scoring](<https://doi.org/10.5281/zenodo.23971694>) | 2026-07 | IC1 | Controle de escrita com proveniência e detecção de conflitos; avaliação rotulada. |
| [A-TMA: Decoupling State-Aware Memory Failures in Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2607.01935>) | 2026-07 | IC1 | Fatos superados versus atuais (ghost memory); benchmark com conflitos. |
| [SCM: Lifecycle Memory for Language Agents](<https://doi.org/10.5281/zenodo.21323876>) | 2026-07 | IC1 | Consolidação, esquecimento adaptativo e contradições entre sessões avaliados empiricamente. |
| [EvoMem: Timeline-Grounded Validity Adjudication for Non-Monotonic Multi-Agent Memory](<https://doi.org/10.1145/3805712.3809931>) | 2026-07 | IC1 | Adjudicação de validade com revisões e retratações; benchmark de erros desatualizados |
| [Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory](<https://doi.org/10.48550/arxiv.2607.17545>) | 2026-07 | IC1 | Seleção entre reter e consolidar memória (merge, abstract, rewrite). |
| [Ground Truth First: A Longitudinal Evaluation Instrument for Agent Memory, and the Tenure Crossover in Memory-Architecture Rankings](<https://doi.org/10.48550/arxiv.2607.21962>) | 2026-07 | IC1 | Benchmark com intervalos de validade e fatos voláteis avalia memória após mudanças. |
| [ConsistencyGate: Preventing Memory Contamination in LLM Agents via Self-Consistency Admission Control](<https://doi.org/10.48550/arxiv.2607.22962>) | 2026-07 | IC1 | Admissão na escrita avaliada contra contaminação plantada. |
| [When Does Memory Help? A Cost-Aware Evaluation of Long-Term Memory in Tool-Using LLM Agents](<https://doi.org/10.48550/arxiv.2609.05441>) | 2026-07 | IC1 | Benchmark mede recordação de fatos atualizados e corrupção de memória em agentes. |
| [ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory](<https://doi.org/10.48550/arxiv.2607.27773>) | 2026-07 | IC1 | Versionamento e rollback da memória; avalia comportamento após reversão. |
| [MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory](<https://doi.org/10.48550/arxiv.2607.27834>) | 2026-07 | IC1 | Valida atualizações, resolve conflitos e recupera estado de memória; avalia correção. |
| [Design and Evaluation of a Memory Consolidation Framework for Long-term LLM Agents: Mitigating Memory Drift, Contradictions, and Information Decay](<https://openalex.org/W7221291591>) | 2026-07 | IC1 | Consolidação contra deriva, contradições e informação obsoleta, com avaliação. |
| [DOMR-Mem: Detecting, Repairing, and Preserving Long-Term LLM Memories](<https://doi.org/10.1109/ccsb71176.2026.11716445>) | 2026-08 | IC1 | Detecção, reparo e consolidação de memórias conflitantes; avalia consistência. |
| [When Memory Updates but Behavior Does Not: Repairing Implicit Stale Dependencies in Personalized Agent Responses](<https://doi.org/10.48550/arxiv.2608.01619>) | 2026-08 | IC1 | Audita transições de estado antigo→novo e repara dependências obsoletas. |
| [TARL: Transaction-Aware Reliable Ledgers for Executable Memory Management in Long-Term Agents](<https://doi.org/10.48550/arxiv.2608.03699>) | 2026-08 | IC1 | Cinco ações de atualização de memória; benchmark com estados-alvo |
| [Verifiable Memory: Learning Unified Memory Management with Local and Global Verifiers for Large Language Model Agents](<https://doi.org/10.48550/arxiv.2608.03137>) | 2026-08 | IC1 | Política única adiciona/revisa/apaga memória com verificadores de consistência |
| [FACTWASH: Catching AI Rewrites That Wash Hearsay into Fact](<https://doi.org/10.48550/arxiv.2608.03372>) | 2026-08 | IC1 | Gate de escrita detecta perda de atribuição/hedging ao reescrever memórias. |
| [Controlled Memory Interference in Continual LLM Agents](<https://doi.org/10.48550/arxiv.2608.07622>) | 2026-08 | IC1 | Estuda interferência e plasticidade de atualização da memória de agentes. |
| [Confidence-Gated Long-Term Memory for Multi-Session LLM Assistants with Temporal Retrieval, Conflict Revision, and Selective Forgetting](<https://openalex.org/W7220024402>) | 2026-08 | IC1 | Escrita com gate, revisão de conflitos e esquecimento seletivo avaliados no LoCoMo. |
| [TEPA: Revoking Stale Memories for Conflict-Robust Language Agents](<https://doi.org/10.48550/arXiv.2608.07429>) | 2026-08 | IC1 | Revogação de memórias obsoletas sob conflito; avalia correção pós-atualização. |
| [From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents](<https://doi.org/10.48550/arxiv.2608.10502>) | 2026-08 | IC1 | Recuperação de estado persistente: desativa memórias falhas e propagadas. |
| [Prior versus Residual: Homeostatic and Allostatic Control Laws for Agent Memory Updates](<https://doi.org/10.5281/zenodo.22019046>) | 2026-08 | IC1 | Leis de controle para sobrescrita de memória; mede falsas atualizações |
| [When Errors Become Memories: Causal Pathway Tracing in Multi-Turn Memory-Augmented LLMs](<https://doi.org/10.48550/arxiv.2608.30198>) | 2026-08 | IC1 | Propagação de erros via atualização de memória; mede retenção de erros. |
| [Salience-Modulated Forgetting: Protecting Rare but Critical Memories in Budget-Constrained LLM Agents](<https://doi.org/10.1109/eecct71142.2026.11746548>) | 2026-09 | IC1 | Esquecimento e revogação de fatos superados em memória de agentes sob orçamento. |
| [Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems](<https://doi.org/10.48550/arxiv.2609.08258>) | 2026-09 | IC1 | Avalia revogação de fatos contraditos em sistemas de memória de agentes. |
| [What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory](<https://doi.org/10.48550/arxiv.2609.08279>) | 2026-09 | IC1 | Audita perdas irreversíveis por despejo/esquecimento na memória de agentes. |
| [The Immutable Past: Formalizing State Mutability and Conflict Resolution in Mutable RAG](<https://doi.org/10.48550/arxiv.2609.16073>) | 2026-09 | IC1 | Resolução de conflitos e mutabilidade de estado em memória RAG de agentes |
| [A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory](<https://doi.org/10.48550/arxiv.2609.30813>) | 2026-09 | IC1 | Benchmark de políticas de admissão de escrita em memória compartilhada; mede afirmações falsas |
| [Authority Before Utility: Non-Compensatory Control for Persistent LLM Memory](<https://doi.org/10.48550/arxiv.2609.37474>) | 2026-09 | IC1 | Exclusão de memórias após atualização/remoção; avalia estado de esquecimento |
| [The Epistemics of Agent Memory: Measuring, and Governing, the Consolidation Decision in Long-Horizon LLM Agents](<https://doi.org/10.48550/arxiv.2609.33013>) | 2026-09 | IC1 | Avalia qualidade das decisões de consolidação/esquecimento contra ótimo. |
| [Decision-Sufficient State Representations: Measuring and Reducing Write-Time Regret](<https://doi.org/10.48550/arXiv.2609.32805>) | 2026-09 | IC1 | Escritor reescreve estado; mede e reduz regret de escrita |
| [TRACE: Governing Memory Validity in Evolving Multi-Agent Systems](<https://doi.org/10.48550/arxiv.2609.33517>) | 2026-09 | IC1 | Resolve invalidação de memória após mudanças do estado compartilhado. |
| [Memory Is a Derivation: The Distributed-Evidence Paradox in Long-Term Agents](<https://doi.org/10.48550/arxiv.2609.36130>) | 2026-09 | IC1 | Audita se memórias escritas são suportadas pelo histórico. |
| [Learning What to Remember: Long-horizon Counterfactual Memory Optimization](<https://doi.org/10.48550/arxiv.2609.37930>) | 2026-09 | IC1 | Otimiza reescritas de memória textual medindo efeito em extração estruturada. |
| [CoEM: Empowering Long-Context Reasoning with Commit-on-Evidence Memory](<https://doi.org/10.48550/arxiv.2609.36935>) | 2026-09 | IC1 | Política aprendida de promover/descartar fatos na memória com verificador |
| [DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users](<https://doi.org/10.48550/arxiv.2610.03020>) | 2026-10 | IC1 | Benchmark com anotações de captura e atualização por sessão. |
| [Governed Persistent Memory Under Enterprise Churn Version 1.0](<https://doi.org/10.5281/zenodo.23175184>) | 2026-10 | IC1 | Memória mutável com contradição, supersessão e revogação; avaliação de recordação. |
| [When to Remember, When to Abstain: Category-Conditioned Retention for Reliable Agent Memory](<https://doi.org/10.48550/arxiv.2610.07100>) | 2026-10 | IC1 | Decisão de retenção na escrita avaliada por suporte das asserções. |
| [Whose Memory Is It? Scope-Aware Commit Rules for Long-Term LLM Memory](<https://doi.org/10.48550/arxiv.2610.09008>) | 2026-10 | IC1 | Regras de commit definem o que entra na memória durável; evita fatos espúrios. |
| [VitaBench: Memory Lifecycles Beyond Retrieval](<https://doi.org/10.48550/arxiv.2610.14731>) | 2026-10 | IC1 | Benchmark do ciclo de vida: manter, comprimir, consolidar ou apagar memórias |
| [Suggested Is Not Superseded: A Pre-Registered Evaluation of a System-One Model as a Memory-Retirement Gate](<https://doi.org/10.48550/arxiv.2610.15710>) | 2026-10 | IC1 | Avalia portão que decide substituição de afirmações armazenadas. |
| [Memory Echo in Single-Agent Long-Term Memory: Lifecycle Evaluation and Provenance-Guided Mitigation](<https://doi.org/10.48550/arxiv.2610.17763>) | 2026-10 | IC1 | Avalia write-back, persistência pós-correção e mitigação por proveniência |
| [CreatorMemBench v1.0: A Lifecycle Benchmark for Mutable Creator-Agent Memory](<https://doi.org/10.5281/zenodo.23371367>) | 2026-10 | IC1 | Benchmark de memória mutável: atualizações, esquecimento, retenção, ressurreição. |
| [Beyond Downstream QA: Rethinking How We Evaluate Agent Memory](<https://doi.org/10.48550/arxiv.2610.22209>) | 2026-10 | IC1 | Benchmark de evolução de fatos inspecionando o armazenamento após ingestões |
| [Let Them Sleep: Recursive Self-Pruning Memory for Long-Horizon LLM Agents](<https://doi.org/10.48550/arxiv.2610.25561>) | 2026-10 | IC1 | Consolidação, decaimento, poda e promoção de regras; mede consistência temporal. |
| [Why Bother Me Again? Benchmarking Personal Agent Memory for Interaction Preferences](<https://doi.org/10.48550/arxiv.2610.30485>) | 2026-10 | IC1 | Benchmark de memória de preferências com mudanças que testam atualização da memória. |
| [PreCoMem: Predictive Cognitive Memory for Self-Evolving Long-Term Dialogue Agents](<https://doi.org/10.48550/arxiv.2610.29467>) | 2026-10 | IC1 | Consolidação de crenças com manter/hipótese/corrigir fatos contraditórios. |
| [CALM: Conflict-Aware Lifecycle Memory Governance for Long-Horizon Language Agents](<https://doi.org/10.48550/arxiv.2610.38573>) | 2026-10 | IC1 | Atualiza validade e ciclo de vida das memórias com conflitos; avalia LongMemEval/LoCoMo |
| [PersistAIBench: an evaluation benchmark for AI agents' memory truthfulness over long multi-step tasks](<https://doi.org/10.5281/zenodo.23893974>) | 2026-11 | IC1 | Benchmark de veracidade de escritas de memória e políticas de escrita. |
| [LLM Memory, Records, and Continued Use: Content, Provenance, Updates, and Authorization — MRSI Collected Edition](<https://doi.org/10.5281/zenodo.23971185>) | 2026-11 | IC1 | Rastreia conteúdo salvo, atualizações, revogação e registros obsoletos. |
| [MemLoRA: Distilling Expert Adapters for On-Device Memory Systems](<https://doi.org/10.48550/arxiv.2512.04763>) | 2025-12 | IC1, IC2 | Adaptadores para SLMs executarem operações de memória (extração, atualização) on-device. |
| [Lightweight LLM Agent Memory with Small Language Models](<https://doi.org/10.18653/v1/2026.acl-long.588>) | 2026† | IC1, IC2 | SLMs fazem escrita, manutenção incremental e consolidação de memória. |
| [MemBuilder: Reinforcing LLMs for Long-Term Memory Construction via Attributed Dense Rewards](<https://doi.org/10.18653/v1/2026.acl-long.1284>) | 2026† | IC1, IC2 | RL treina modelo de 4B para construir memória de longo prazo. |
| [InfMem: Learning System-2 Memory Control for Long-Context Agent](<https://doi.org/10.48550/arxiv.2602.02704>) | 2026-02 | IC1, IC2 | Agente escreve/atualiza memória limitada; avaliado com Qwen3-1.7B e 4B. |
| [Epistemic Validation in AI Knowledge Systems: A System-2 Framework for Long-Term Memory](<https://doi.org/10.5281/zenodo.19357817>) | 2026-03 | IC1, IC2 | Validação epistêmica na escrita da memória, inclui validador local 3B |
| [TSUBASA: Improving Long-Horizon Personalization via Evolving Memory and Self-Learning with Context Distillation](<https://doi.org/10.48550/arxiv.2604.07894>) | 2026-04 | IC1, IC2 | Escrita de memória com evolução dinâmica; Qwen3 a partir de 4B avaliado. |
| [Small Language Models as Persistent Memory Controllers for Lightweight LLM Agents](<https://openalex.org/W7220767060>) | 2026-05 | IC1, IC2 | SLM dedicado gerencia codificação, consolidação e sumarização da memória. |
| [CMI-Mem: Toward Generalizable Long-Term Memory Management via CMI-Augmented Reinforcement Learning](<https://doi.org/10.48550/arxiv.2607.20553>) | 2026-07 | IC1, IC2 | Gestor de memória 4B treinado por RL com recompensa por operação. |
| [Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation](<https://doi.org/10.48550/arxiv.2608.22215>) | 2026-08 | IC1, IC2 | Roteamento de escrita novo/atualização com cascata 1.7B/8B. |
| [Truth for Believable AI: Expressed Doubt, Provenance, and Belief Revision as an Engineerable Stance](<https://doi.org/10.48550/arxiv.2609.26035>) | 2026-09 | IC1, IC2 | Store persistente de revisão de crenças multi-sessão avaliado com Qwen2.5-0.5B. |
| [A Model That Does Not Forget. A Logbook That Corrects and a Sleep That Consolidates, on a Frozen Language Model](<https://doi.org/10.21203/rs.3.rs-11185020/v1>) | 2026-09 | IC1, IC2 | Logbook versionado e consolidação em Qwen3-0.6B; mede retenção de fatos que mudam. |
| [Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing](<https://doi.org/10.48550/arxiv.2610.22196>) | 2026-10 | IC1, IC2 | Escritor de memória MoE com 30B parâmetros totais e ~3B ativos, treinado por destilação e RL; não é SLM em parâmetros totais. |
| [Memory, Know Your PLACE: Governing Lifecycle State and Query-Time Eligibility in Persistent-Memory Agents](<https://doi.org/10.48550/arxiv.2610.25179>) | 2026-10 | IC1, IC2 | Governança de escrita certifica estado de memória; Qwen2.5-3B avaliado. |
| [Learning from the User Without Learning Their Mistakes: A Preregistered Study of On-Device Personalisation for a Small Language Model](<https://doi.org/10.5281/zenodo.23485017>) | 2026-10 | IC1, IC2 | SLM 352M com filtro de admissão e nota de fatos do usuário |
| [CLAG: Adaptive Memory Organization via Agent-Driven Clustering for Small Language Model Agents](<https://doi.org/10.18653/v1/2026.findings-acl.824>) | 2026† | IC1, IC2, IC3 | SLM organiza e evolui memória por clusters com perfis gerados. |
| [AMU: Admission and Memory Update for Personalized Conversations —Structured Memory with SLM Guided Control](<https://doi.org/10.18653/2026.nora-1.1>) | 2026† | IC1, IC2, IC3 | SLM controla admissão e atualização de memória estruturada personalizada. |
| [PGMem: Tightly Coupled Persona–Memory Graph for Lifelong Personalized Agents](<https://doi.org/10.18653/2026.emnlp-main.1891>) | 2026† | IC1, IC2, IC3 | Grafo persona-memória que revisa personas evolutivas, com backbones SLM. |
| [GRAM: Empowering Agent with Actively Managed Graph-Structured Memory via Reinforcement Learning](<https://doi.org/10.18653/2026.findings-emnlp.1183>) | 2026† | IC1, IC2, IC3 | SLMs <4B treinados por RL para gerir memória em grafo com consolidação. |
| [MemReader: From Passive to Active Extraction for Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2604.07877>) | 2026-04 | IC1, IC2, IC3 | SLMs 0.6B/4B extraem e decidem escrita de memória estruturada. |
| [DimMem: Dimensional Structuring for Efficient Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2605.15759>) | 2026-05 | IC1, IC2, IC3 | Unidades de memória tipadas com atualização; extrator Qwen3-4B ajustado. |
| [truthllm: Expression-and-Revision Layer over a Fixed Language Model — Reference Implementation, Benchmark, and Results (v1.0)](<https://doi.org/10.5281/zenodo.21462985>) | 2026-07 | IC1, IC2, IC3 | Armazém de crenças com revisão e benchmark de correção; Qwen 0.5B |
| [Memory That Doesn't Expire: Agentic Long-Term Memory for Conversational Agents on a Single Consumer GPU](<https://doi.org/10.5281/zenodo.21964737>) | 2026-08 | IC1, IC2, IC3 | Modelo local pequeno gerencia fatos tipados, datados e deduplicados |
| [Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents](<https://doi.org/10.48550/arxiv.2609.01272>) | 2026-09 | IC1, IC2, IC3 | Armazém tipado de intenções com ciclo de vida para agentes SLM (Gemma-E2B). |
| [Closing the Epistemic Loop Across the Five Layers of Agent Memory: Cryptographic Provenance, Paraconsistent Bilattices, and Z3-Quarantined Procedural Induction](<https://doi.org/10.5281/zenodo.23901682>) | 2026-11 | IC1, IC2, IC3 | Promoção verificada, contradições e supersede em memória; inclui modelos pequenos. |
| [Mem-α: Learning Memory Construction via Reinforcement Learning](<https://doi.org/10.48550/arXiv.2509.25911>) | 2025-09 | IC1, IC3 | RL treina agente para construir e atualizar memória estruturada. |
| [MEMTRACK: Evaluating Long-Term Memory and State Tracking in Multi-Platform Dynamic Agent Environments](<https://doi.org/10.48550/arxiv.2510.01353>) | 2025-10 | IC1, IC3 | Benchmark de rastreamento de estado com informações conflitantes e resolução. |
| [D-SMART: Enhancing LLM Dialogue Consistency via Dynamic Structured Memory And Reasoning Tree](<https://doi.org/10.48550/arxiv.2510.13363>) | 2025-10 | IC1, IC3 | Grafo de conhecimento da conversa construído e mantido incrementalmente. |
| [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](<https://doi.org/10.3233/faia251160>) | 2025-10 | IC1, IC3 | Extração e consolidação dinâmica de memória com variante em grafo. |
| [APEX-MEM: Agentic Semi-Structured Memory with Temporal Reasoning for Long-Term Conversational AI](<https://doi.org/10.18653/v1/2026.acl-long.749>) | 2026† | IC1, IC3 | Grafo de propriedades centrado em entidades, append-only, resolve informações conflitantes. |
| [Entity Blackboard: Structured Agent Memory for Long Document Summarization](<https://doi.org/10.18653/2026.findings-emnlp.384>) | 2026† | IC1, IC3 | Memória de entidades atualizada incrementalmente com filtragem de escritas ruidosas. |
| [LatticeMind: A Conflict-Aware Memory Primitive for Multi-Agent Systems](<https://doi.org/10.18653/2026.emnlp-main.1564>) | 2026† | IC1, IC3 | Memória estruturada resolve contradições na escrita; avaliado em ConflictBank. |
| [Learning to Remember: End-to-End Training of Memory Agents for Long-Context Reasoning](<https://doi.org/10.18653/2026.emnlp-main.1299>) | 2026† | IC1, IC3 | Banco de memória estruturado com CRUD treinado; Ledger-QA mede rastreamento de estado. |
| [ProgMem: Programmatic Belief-State Memory for Long-Horizon Conversational Agents](<https://doi.org/10.18653/2026.findings-aacl.120>) | 2026† | IC1, IC3 | Programas de memória estruturada modelam escritas e mudanças de estado; avalia Qwen3-4B. |
| [PersonaTree: Structured Lifecycle Memory for Person Understanding in LLM Agents](<https://doi.org/10.18653/2026.findings-emnlp.822>) | 2026† | IC1, IC3 | Árvore de persona com escrita conservadora e consolidação guiada por confiança. |
| [COLLABMEM: A Diagnostic Benchmark for Collaborative Memory Operations in Multi-Agent LLM Systems](<https://doi.org/10.18653/2026.emnlp-main.1194>) | 2026† | IC1, IC3 | Benchmark de conflitos/atualização e memória em grafo com marcação CURRENT. |
| [Seamless: Self-Maintaining Knowledge Graph Memory for Retrieval-Augmented Language Models](<https://doi.org/10.1109/access.2026.3747787>) | 2026† | IC1, IC3 | Memória em grafo autoatualizável reconciliando fatos mutáveis |
| [DRIFTBENCH: Long-Horizon Memory Benchmark For AI Agents](<https://doi.org/10.51483/ijaiml.6.5s.2026.379-392>) | 2026† | IC1, IC3 | Benchmark com revisões factuais e métrica de fidelidade de atualização. |
| [Toward Robust Personalized Alignment for LLMs: Mitigating Persona Drift in Multi-Turn Dialogue](<https://doi.org/10.18653/2026.findings-emnlp.666>) | 2026† | IC1, IC3 | Revisão seletiva de estado de persona com fidelidade de slots |
| [WK-Drift: Benchmarking Procedural Memory Maintenance under World Knowledge Drift](<https://doi.org/10.18653/2026.findings-aacl.140>) | 2026† | IC1, IC3 | Manutenção de memória sob deriva; atualizações cirúrgicas em grafo |
| [Capture Is Easy, Forgetting Is Hard: Benchmarking Prospective Memory in Conversational Agents](<https://doi.org/10.18653/2026.realm-1.43>) | 2026† | IC1, IC3 | Benchmark de captura e esquecimento de pins; mede retirada correta do estado. |
| [LiCoMemory: Lightweight and Cognitive Agentic Memory for Efficient Long-Term Reasoning](<https://doi.org/10.18653/v1/2026.findings-acl.1835>) | 2026† | IC1, IC3 | Grafo de entidades/relações com atualização em tempo real; LoCoMo/LongMemEval |
| [AtomMem: Building Simple and Effective Memory System for LLM Agents via Atomic Facts](<https://doi.org/10.18653/2026.emnlp-main.2387>) | 2026† | IC1, IC3 | Extração de fatos atômicos e perfis temporais de usuário em evolução |
| [PACMI: Provenance-Aware Cascading Memory Invalidation for Long-Term LLM Agents](<https://doi.org/10.2139/ssrn.7480138>) | 2026† | IC1, IC3 | Invalidação em cascata de memórias obsoletas em grafo de proveniência, com benchmark. |
| [Memory Beyond Recall: A Dual-Process Cognitive Memory System for Self-Evolving LLM Agents](<https://doi.org/10.18653/2026.findings-emnlp.1918>) | 2026† | IC1, IC3 | Cadeias de substituição para revisão de crenças em hierarquia estruturada |
| [Task-Oriented Memory Compilation: Executable State Representations for Long-Context Language Models](<https://openalex.org/W7224148218>) | 2026† | IC1, IC3 | Compila registros de estado/relação rastreando fatos atualizados no BEAM. |
| [State Drift in Language-Conditioned Autonomous Agents: A Failure Mode of Long-Horizon Reasoning](<https://doi.org/10.20944/preprints202601.0910.v1>) | 2026-01 | IC1, IC3 | Compara estado textual de crenças com estado real ao longo de interações. |
| [AriadneMem: Threading the Maze of Lifelong Memory for LLM Agents](<https://doi.org/10.48550/arxiv.2603.03290>) | 2026-02 | IC1, IC3 | Memória estruturada com atualizações de estado e mesclagem consciente de conflitos |
| [Neuromem: A Granular Decomposition of the Streaming Lifecycle in External Memory for LLMs](<https://doi.org/10.48550/arxiv.2602.13967>) | 2026-02 | IC1, IC3 | Avalia memória em streaming com inserções, manutenção e consolidação. |
| [Panini: Continual Learning in Token Space via Structured Memory](<https://doi.org/10.48550/arxiv.2602.15156>) | 2026-02 | IC1, IC3 | Memória semântica estruturada de entidades/eventos consolidada continuamente. |
| [Thinking Like a NERD: Entity-Centered Memory for LLM Agents](<https://doi.org/10.36227/techrxiv.177156112.28008669/v1>) | 2026-02 | IC1, IC3 | Documentos por entidade consolidados incrementalmente por agente escritor. |
| [Theory of Code Space: Do Code Agents Understand Software Architecture?](<https://doi.org/10.48550/arxiv.2603.00601>) | 2026-02 | IC1, IC3 | Agentes mantêm e atualizam crenças estruturadas em JSON; mede manutenção. |
| [AMemGym: Interactive Memory Benchmarking for Assistants in Long-Horizon Conversations](<https://doi.org/10.48550/arxiv.2603.01966>) | 2026-03 | IC1, IC3 | Benchmark com evolução de estado estruturado do usuário e consistência. |
| [Ledger-Guided Memory for Agentic Web RL: Structured Cost–Risk Accounting in Long-Horizon Decision Models](<https://doi.org/10.6084/m9.figshare.31792771>) | 2026-03 | IC1, IC3 | Ledger estruturado chave-valor atualizado por parser; mede acurácia factual do ledger |
| [Graph-Native Cognitive Memory for AI Agents: Formal Belief Revision Semantics for Versioned Memory Architectures](<https://doi.org/10.48550/arXiv.2603.17244>) | 2026-03 | IC1, IC3 | Revisão de crenças AGM em memória de grafo versionada. |
| [An Empirical Study on Enhancing Large Language Models for Long-Term Conversations in Korean](<https://doi.org/10.3390/app16073175>) | 2026-03 | IC1, IC3 | Avalia tarefa de atualização de memória de persona/episódio em coreano. |
| [Neurons that Crash, Wire Together: Collision-Driven Knowledge Evolution through Addressable Structured Memory](<https://doi.org/10.5281/zenodo.19399683>) | 2026-04 | IC1, IC3 | Registra conflitos como arestas de grafo em memória estruturada. |
| [WorldDB: A Vector Graph-of-Worlds Memory Engine with Ontology-Aware Write-Time Reconciliation](<https://doi.org/10.48550/arxiv.2604.18478>) | 2026-04 | IC1, IC3 | Reconciliação na escrita: substituição e contradição em grafo de memória |
| [Can Agentic Memory Track Changing Beliefs? A Benchmark for Temporal Belief Reconstruction](<https://doi.org/10.5281/zenodo.20130102>) | 2026-05 | IC1, IC3 | Benchmark de crenças mutáveis, supersessão e obsolescência em cascata. |
| [Human-Inspired Memory Architecture for LLM Agents](<https://doi.org/10.48550/arxiv.2605.08538>) | 2026-05 | IC1, IC3 | Consolidação, esquecimento, reconsolidação e grafos de entidades avaliados. |
| [MEME: Multi-entity & Evolving Memory Evaluation](<https://doi.org/10.48550/arXiv.2605.12477>) | 2026-05 | IC1, IC3 | Benchmark de memória multientidade evolutiva, incluindo exclusão e dependências. |
| [Agentic Recommender System with Hierarchical Belief-State Memory](<https://doi.org/10.48550/arxiv.2605.14401>) | 2026-05 | IC1, IC3 | Ciclo completo de atualização de estado de crença estruturado de preferências |
| [Accurate and Efficient Long-Term Memory for LLM Agents](<https://doi.org/10.48550/arxiv.2607.16211>) | 2026-05 | IC1, IC3 | Memória em grafo tipado por entidades com resolução ativa de conflitos. |
| [PatchBoard: Schema-Grounded State Mutation for Reliable and Auditable LLM Multi-Agent Collaboration](<https://doi.org/10.48550/arxiv.2605.29313>) | 2026-05 | IC1, IC3 | Mutações JSON Patch validadas sobre estado estruturado compartilhado. |
| [Eywa: Provenance-Grounded Long-Term Memory for AI Agents](<https://doi.org/10.48550/arxiv.2605.30771>) | 2026-05 | IC1, IC3 | Fatos canônicos tipados validados, atualização e apagamento de memória. |
| [Profile-Graph Memory for LLM Agents: Implicit Cross-Entity Traversal through Narrative Profiles](<https://doi.org/10.48550/arxiv.2607.19359>) | 2026-06 | IC1, IC3 | Perfis de entidades atualizados por LLM com resíduos extraídos. |
| [GROWL: Self-Organizing Memory with Active Semantic Consolidation for Lifelong Language Agents](<https://doi.org/10.1109/IJCNN69854.2026.11728879>) | 2026-06 | IC1, IC3 | Memória em grafo que trata mudança de fatos; benchmark de rastreamento de estado. |
| [SaliMory: Orchestrating Cognitive Memory for Conversational Agents](<https://doi.org/10.48550/arxiv.2606.04120>) | 2026-06 | IC1, IC3 | Filtragem, consolidação de memória estruturada; mede factualidade das memórias. |
| [Less Context, More Accuracy: A Bi-Temporal Memory Engine for LLM Agents Where a Lean Retrieved Context Beats the Full History](<https://doi.org/10.48550/arxiv.2606.09900>) | 2026-06 | IC1, IC3 | Grafo bi-temporal de triplas com resolução de contradições e supersessão. |
| [REAL: A Reasoning-Enhanced Graph Framework for Long-Term Memory Management of LLMs](<https://doi.org/10.48550/arxiv.2606.10694>) | 2026-06 | IC1, IC3 | Grafo temporal de fatos com atualização não destrutiva e confiança. |
| [EvoArena: Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments](<https://doi.org/10.48550/arxiv.2606.13681>) | 2026-06 | IC1, IC3 | Memória baseada em patches com históricos estruturados de atualização. |
| [User as Code: Executable Memory for Personalized Agents](<https://doi.org/10.48550/arXiv.2606.16707>) | 2026-06 | IC1, IC3 | Estado do usuário em objetos tipados, checkpointado, resolve contradições. |
| [DynamicMem: A Long-Horizon Memory Benchmark in Real-World Settings](<https://doi.org/10.48550/arXiv.2606.22877>) | 2026-06 | IC1, IC3 | Benchmark de perfil do usuário com atributos que evoluem e precisam ser atualizados. |
| [MemAudit: Auditing Long-Term Agent Memory via Hidden User-State Recovery](<https://doi.org/10.48550/arxiv.2606.24595>) | 2026-06 | IC1, IC3 | Audita estado estruturado do usuário reconstruído da memória do agente. |
| [PatchOptic for Shared-State LLM Workflows with Projected Views and Verified Structured Updates](<https://doi.org/10.48550/arxiv.2607.05483>) | 2026-07 | IC1, IC3 | Atualizações estruturadas verificadas em estado compartilhado de workflows LLM. |
| [StateFuse: Deterministic Conflict-Preserving Memory for Multi-Agent Systems](<https://doi.org/10.48550/arXiv.2607.05844>) | 2026-07 | IC1, IC3 | Memória que preserva conflitos e correções, avaliada em MemoryAgentBench. |
| [AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment](<https://doi.org/10.1145/3805712.3808634>) | 2026-07 | IC1, IC3 | Benchmark com memórias estruturadas avaliando extração, atualização, recuperação e uso. |
| [MemOps: Benchmarking Lifecycle Memory Operations in Long-Horizon Conversations](<https://doi.org/10.48550/arxiv.2607.12893>) | 2026-07 | IC1, IC3 | Benchmark de operações de ciclo de vida da memória com traços estruturados. |
| [The Ledger Knows What the Weights Know: Entity-Level Parametric Memory with Provenance Guarantees for LLM Agents](<https://doi.org/10.5281/zenodo.21375428>) | 2026-07 | IC1, IC3 | Ledger de fatos por entidade com supersessão determinística e benchmark próprio. |
| [MemTX: Transactional Belief Commit for Stateful Agent Memory](<https://doi.org/10.48550/arxiv.2607.23929>) | 2026-07 | IC1, IC3 | Commit transacional de crenças com retração e reparo em cascata de registros tipados. |
| [A Graph-Native Bitemporal Memory Store for Conversational AI Agents](<https://doi.org/10.48550/arxiv.2607.26520>) | 2026-07 | IC1, IC3 | Grafo bitemporal versionado; atualiza fatos sem sobrescrever histórico |
| [Correctness Under Time: Bi-Temporal, Supersession-Aware Memory for AI Agents](<https://doi.org/10.5281/zenodo.21691913>) | 2026-07 | IC1, IC3 | Memória bitemporal com supersessão; avalia correção após atualizações de conhecimento. |
| [RICO-Mem: Conflict-Aware Memory Management for Long-Term LLM Agents](<https://doi.org/10.1109/ccsb71176.2026.11716419>) | 2026-08 | IC1, IC3 | Gestão de conflitos em grafo temporal de memória; distingue deriva e contradição. |
| [CoMemo: A Hybrid Vector and Graph Cognitive Memory Framework with Admission, Reinforcement, Decay and Lifecycle Management for AI Agents](<https://doi.org/10.1109/mercon71835.2026.11691517>) | 2026-08 | IC1, IC3 | Admissão, consolidação, contradição e decaimento em memória grafo+vetor |
| [TrajWiki: Source-Grounded Memory Trajectories for Long-Horizon Dialogue Agents](<https://doi.org/10.48550/arxiv.2608.00967>) | 2026-08 | IC1, IC3 | Memória por afirmações com ADD/REVISE/DEPRECATE e wiki estruturada incremental. |
| [MemSIF: From Structured Interactions to Dual-Track Fact Memory for LLM Agents](<https://doi.org/10.48550/arxiv.2608.01742>) | 2026-08 | IC1, IC3 | Memória de fatos guiada por esquema consolidada na escrita. |
| [EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift](<https://doi.org/10.48550/arxiv.2608.04278>) | 2026-08 | IC1, IC3 | Memória em grafo de afirmações revisadas sob deriva; avalia correção do estado. |
| [Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite](<https://doi.org/10.48550/arxiv.2608.05095>) | 2026-08 | IC1, IC3 | Memória hierárquica em grafo com reescrita por caminho |
| [Caching for the Future: Scrub Jay Episodic Memory Principles for Agent Memory Systems](<https://doi.org/10.48550/arxiv.2608.04746>) | 2026-08 | IC1, IC3 | Tuplas tipadas com decaimento e revisão retroativa de memórias. |
| [MELD: A Protocol for Merging Knowledge Across Distributed Agentic Memories -- reference implementation and experiments](<https://doi.org/10.5281/zenodo.21878274>) | 2026-08 | IC1, IC3 | Fusão de memórias com inserção/merge/conflito/rejeição sobre chaves de afirmação. |
| [Governed Persistent Memory: Source-Bound State Semantics and Fail-Closed Release for Long-Horizon Agents](<https://doi.org/10.48550/arxiv.2608.12476>) | 2026-08 | IC1, IC3 | Memória persistente governada: conflitos, retratação, exclusão, liberação estruturada avaliada |
| [MindMemOS: A Portable and Self-Evolving Memory Operating Layer for AI Agents](<https://doi.org/10.48550/arXiv.2608.12428>) | 2026-08 | IC1, IC3 | Estrutura entidade-propriedade-tempo, fusão de redundâncias e resolução de conflitos. |
| [What Does Each Memory Feature Buy? A Measured Audit of an Agent Memory System](<https://doi.org/10.5281/zenodo.22002653>) | 2026-08 | IC1, IC3 | Audita consolidação, resolução de conflitos e crenças bitemporais. |
| [Can Agent Memory Systems Track Evolving State?](<https://doi.org/10.48550/arxiv.2608.19652>) | 2026-08 | IC1, IC3 | Benchmark e método de rastreamento de estado com supersessão de fatos. |
| [Temporal Truth-Maintained Memory Graphs: Truth Maintenance for Long-Horizon Agent Memory](<https://doi.org/10.5281/zenodo.22115414>) | 2026-08 | IC1, IC3 | Grafo de afirmações com supersessão/contradição; mede valor atual após atualizações. |
| [Selective Forgetting: A Graph-Based Memory Framework for Long-Term LLM Agents](<https://doi.org/10.48550/arxiv.2608.28978>) | 2026-08 | IC1, IC3 | Grafo de entidades com poda seletiva; avaliado no LongMemEval. |
| [Agent Memory Is a Surface for Endogenous Authorization Laundering](<https://doi.org/10.48550/arxiv.2609.01836>) | 2026-09 | IC1, IC3 | Avalia LLMs como escritores de memória tipada incremental e fidelidade do estado. |
| [Consistent Conversational State for Virtual Agents: Slot-Based Memory for Accurate Fact Retrieval](<https://doi.org/10.1145/3806774.3832787>) | 2026-09 | IC1, IC3 | Compara políticas de escrita com slots sobrescritos; mede consistência e fatos obsoletos. |
| [MoM: Memory of Memory](<https://doi.org/10.48550/arXiv.2609.25054>) | 2026-09 | IC1, IC3 | Grafo tipado com valores atuais, supersessão e histórico preservado. |
| [ROAM: Robust Organization of Atomic Memories for Agents through Semantic Relations](<https://doi.org/10.48550/arXiv.2609.09778>) | 2026-09 | IC1, IC3 | Classifica relações entre memórias atômicas, resolve conflitos e funde atualizações. |
| [What Should an Agent Forget? Separating What Is Stored from What Is Used](<https://doi.org/10.48550/arXiv.2609.10263>) | 2026-09 | IC1, IC3 | Substituição de fatos superados em slots; avalia knowledge updating |
| [Propose, Verify, Commit: Evidence-Grounded Memory for Long-Horizon Multi-Actor Conversations](<https://doi.org/10.48550/arxiv.2609.23465>) | 2026-09 | IC1, IC3 | Protocolo propose-verify-commit para atualizar estados com histórico de revisões. |
| [SpeakerMem-R1: Speaker-Centered Dual-Track Memory for Multi-Party Dialogue](<https://doi.org/10.48550/arxiv.2609.26780>) | 2026-09 | IC1, IC3 | Memória estruturada por pessoa/grupo com estados derivados e redução de erros de atualização. |
| [EMIR$^2$: Evolution-Aware Memory with Intent-Guided Multi-Round Retrieval](<https://doi.org/10.48550/arxiv.2609.32584>) | 2026-09 | IC1, IC3 | Grafo de memória com estados evolutivos e atualizações baseadas em evidências. |
| [Contract Memory Compiler: Resolve, Then Traverse](<https://doi.org/10.48550/arXiv.2609.32658>) | 2026-09 | IC1, IC3 | Aplica atualizações de relações para determinar estado atual; FactConsolidation. |
| [Stashbird: Episode-Grounded Lifecycle Reconciliation for Conversational Agent Memory](<https://doi.org/10.48550/arxiv.2609.34242>) | 2026-09 | IC1, IC3 | Reconciliação de grafo com correções, substituições e exclusões; avalia estados finais. |
| [Mnemon: Raw Records, Fast Judgments, Slow Thoughts](<https://doi.org/10.48550/arxiv.2609.36059>) | 2026-09 | IC1, IC3 | Julga registros obsoletos e consolida em históricos de valores |
| [When Evidence Changes: Evaluating Memory Repair and Re-reading in Language-Model Agents](<https://doi.org/10.48550/arxiv.2610.03902>) | 2026-10 | IC1, IC3 | Avalia reparo/revisão de memória após revogação de evidências; reparo local em grafo. |
| [StateWise: Diagnosing and Repairing Persistent Operational State Before Agent Actions](<https://doi.org/10.48550/arxiv.2610.05241>) | 2026-10 | IC1, IC3 | Diagnostica e repara registros persistentes inválidos com linhagem. |
| [MINDSET: Energy-based Memory Evolution for Long Conversational Agents](<https://doi.org/10.48550/arxiv.2610.08586>) | 2026-10 | IC1, IC3 | Esquemas versionados com reforço, substituição e ramificação; avalia knowledge-update. |
| [Stale, Misattributed, or Late: Where Personal Memory Fails Before Generation](<https://doi.org/10.48550/arxiv.2610.10265>) | 2026-10 | IC1, IC3 | Mede valores obsoletos e resolução de revisões em slots de fatos. |
| [Event-Centric Memory with Query-Aware Graph Augmentation for Long-Term Conversational Agents](<https://doi.org/10.48550/arxiv.2610.11920>) | 2026-10 | IC1, IC3 | Consolidação de unidades de eventos em traços com estado atual |
| [SLICE-Mem: Salience-Gated Lightweight Information Curation for Efficient LLM Agent Memory](<https://doi.org/10.48550/arxiv.2610.33015>) | 2026-10 | IC1, IC3 | Admissão leve, extração predicado-centrada e consolidação offline de memória. |
| [Gated Memory: Admission-Controlled Memory Formation for Conversational AI](<https://doi.org/10.48550/arxiv.2610.11270>) | 2026-10 | IC1, IC3 | Controle de admissão na escrita de fatos/triplas na memória |
| [TEM: Temporal State Tracking Memory for Large Language Model Agents](<https://doi.org/10.48550/arxiv.2610.21900>) | 2026-10 | IC1, IC3 | Registros versionados rastreiam substituição de fatos entre sessões. |
| [MemDerive: A Diagnostic Benchmark for Agent Memory over Evolving Data](<https://doi.org/10.48550/arxiv.2610.25373>) | 2026-10 | IC1, IC3 | Benchmark de estado derivado em dados que evoluem; detecta estado desatualizado |
| [Persistent Memory Mechanisms and Storage Architecture Design for Agent-based Information Systems](<https://doi.org/10.38007/ijbdit.2026.070304>) | 2026-10 | IC1, IC3 | Cadeia de versões entidade-atributo para estado atual e histórico. |
| [A State Change Is Local, Its Consequences Are Not: Dependency-Aware State Revision for Long-Term Agent Memory](<https://doi.org/10.48550/arxiv.2611.02912>) | 2026-11 | IC1, IC3 | Revisão de estado com grafo de dependências; benchmark de mudanças de estado. |
| [Agent Memory as Rate-Limited Filtering: Explicit State Outlasts Long Context Beyond a Reader-Dependent Horizon](<https://doi.org/10.48550/arxiv.2611.02361>) | 2026-11 | IC1, IC3 | Estado explícito sob concessões/revogações versus contexto longo; mede correção e esquecimento. |
| [MemDTG: Dynamic Temporal Memory Graphs for Evidence-Admissible Agent Memory](<https://doi.org/10.1145/3799682.3841052>) | 2026-11 | IC1, IC3 | Grafo temporal de estados de entidades com supersessão |
| [EvoMemState: Evolving Memory State for Personal Agents](<https://doi.org/10.20944/preprints202611.0407.v1>) | 2026-11 | IC1, IC3 | Estados relacionais de fatos, conflitos e evolução da memória. |
| [SynapseMem: Deterministic Temporal Belief Invalidation and Ebbinghaus Memory Consolidation for Edge Language Models](<https://doi.org/10.5281/zenodo.23970379>) | 2026-11 | IC1, IC3 | Tuplas de crença que substituem estado obsoleto para SLMs na borda. |
| [DiffuPlan: Editable Planning State for Diffusion Language Model Agents](<https://doi.org/10.48550/arxiv.2610.24717>) | 2026-10 | IC1, IC4 | dLLM mantém estado de planejamento editável e reconstrói só passos afetados; compara com o modelo AR de origem sob mesmos dados. |
| [From Monolithic Prompts to Scaffolded Execution for Memory Agents with Small Language Models](<https://doi.org/10.18653/2026.findings-emnlp.968>) | 2026† | IC2 | SLMs executam agentes de memória com scaffolding; avaliado no LoCoMo e MemoryAgentBench. |
| [From Facts to Insights: A Persona-Driven Dual Memory Framework and Dataset for Role-Playing Agents](<https://doi.org/10.48550/arXiv.2605.25693>) | 2026-05 | IC2 | Modelo de 4B treinado para gerir memória dual de fatos e insights |
| [PSD: Pseudo Self-Distillation of Memory Representation Capabilities for LLM Agents](<https://doi.org/10.48550/arxiv.2609.23449>) | 2026-09 | IC2 | SLM destilado para construir representações de memória hierárquica. |
| [EdgeWisePersona: A Dataset for On-Device User Profiling from Natural Language Interactions](<https://doi.org/10.1145/3774935.3806788>) | 2026-06 | IC2, IC3 | SLMs reconstroem perfis estruturados a partir de interações multissessão |
| [G-Long: Graph-Enhanced Memory Management for Efficient Long-Term Dialogue Agents](<https://doi.org/10.48550/arxiv.2606.13115>) | 2026-06 | IC2, IC3 | sLM ajustado extrai triplas para memória em grafo de diálogo longo |
| [Evaluating Memory Structure in LLM Agents](<https://doi.org/10.48550/arxiv.2602.11243>) | 2026-02 | IC3 | Benchmark de organização de memória estruturada (ledgers, listas, árvores) |
| [LedgerAgent: Structured State for Policy-Adherent Tool-Calling Agents](<https://doi.org/10.48550/arxiv.2606.20529>) | 2026-06 | IC3 | Estado de tarefa estruturado em ledger mantido entre turnos para agentes de ferramentas. |
| [What Does Successful Execution Certify? An Executable Decomposition of LLM-Agent Handoffs](<https://doi.org/10.5281/zenodo.22668198>) | 2026-09 | IC3 | Reconstrói estado estruturado e mede fidelidade em handoffs |
| [Trail: Accurate Local Smart Home Control Using Decision Models](<https://doi.org/10.48550/arxiv.2611.00610>) | 2026-10 | IC3, IC4 | SLM local com decisões tipadas e memória estruturada multi-turno avaliada. |
| [Unveiling the Potential of Diffusion Large Language Model in Controllable Generation](<https://doi.org/10.48550/arXiv.2507.04504>) | 2025-07 | IC4 | dLLM gera JSON confiável via andaime de esquema. |
| [The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Reality Check](<https://doi.org/10.18653/v1/2026.acl-long.2036>) | 2026† | IC4 | Avalia dLLMs vs autoregressivos em chamadas de ferramenta JSON e agentes. |
| [Is Generative AI Hiding in Your Phone? Fine-tuning SLMs to Generate JSON-Adherent Output](<https://openalex.org/W7208795050>) | 2026† | IC4 | Fine-tuning de Qwen3-0.6B para saída JSON conforme esquema. |
| [Dgrammar: Efficient Constrained Decoding for DLMs](<https://doi.org/10.18653/2026.aacl-long.225>) | 2026† | IC4 | Decodificação restrita para modelos de difusão em JSON Schema. |
| [DiffResearch: Accelerating Deep Research with Diffusion Language Models](<https://doi.org/10.18653/2026.emnlp-industry.262>) | 2026† | IC4 | Compara backbone de difusão e autoregressivo em framework agêntico de pesquisa. |
| [DLLM Agent: See Farther, Run Faster](<https://doi.org/10.48550/arxiv.2602.07451>) | 2026-02 | IC4 | Compara difusão × autorregressivo em agentes com uso de ferramentas. |
| [Continuous Diffusion Models Can Obey Formal Syntax](<https://doi.org/10.48550/arxiv.2602.12468>) | 2026-02 | IC4 | Difusão contínua obedecendo sintaxe JSON/regex |
| [ScrapeGraphAI-100k: Dataset for Schema-Constrained LLM Generation](<https://www.semanticscholar.org/paper/171648754cf73825e1074b7838acd943ea5a5991>) | 2026-02 | IC4 | Dataset de geração restrita a esquema JSON; estudante 1,7B ajustado. |
| [Localized Diffusion Repair for Reliable Tool-Using LLM Agents](<https://doi.org/10.1109/ASENS69964.2026.11605180>) | 2026-03 | IC4 | Modelo de difusão repara chamadas de ferramenta JSON; compara com autoregressivo. |
| [The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models](<https://doi.org/10.48550/arxiv.2605.26128>) | 2026-05 | IC4 | Mede validade vs correção em saídas estruturadas de SLMs sub-3B. |
| [Agents of Diffusion: Enhancing Diffusion Language Models with Multi-Agent Reinforcement Learning for Structured Data Generation](<https://doi.org/10.65109/ggjl7344>) | 2026-05 | IC4 | Modelo de difusão gerando JSON com aderência a esquema |
| [Are Diffusion Language Models Good Database Analysts?](<https://doi.org/10.48550/arxiv.2605.27791>) | 2026-05 | IC4 | Compara difusão × autoregressivo em NL2SQL estruturado. |
| [EPIC: Efficient and Parallel Inference under CFG Constraints for Diffusion Language Models](<https://doi.org/10.48550/arxiv.2606.00722>) | 2026-05 | IC4 | Decodificação restrita por gramática em modelos de difusão |
| [Dynamic Infilling Anchors for Format-Constrained Generation in Diffusion Large Language Models](<https://doi.org/10.48448/xmcc-9759>) | 2026-06 | IC4 | Geração com restrição de formato JSON em dLLMs |
| [Small Language Models and Spec-Driven Development for High-Accuracy Agentic AI Systems](<https://doi.org/10.67231/qqk79s36>) | 2026-06 | IC4 | SLMs ajustados para JSON e chamadas de ferramenta com esquema, avaliados. |
| [GenSIE Benchmark v1.0: Schema-Guided Information Extraction with Small Language Models in Spanish](<https://doi.org/10.5281/zenodo.21299326>) | 2026-07 | IC4 | Benchmark de extração JSON guiada por esquema com SLMs e fidelidade. |
| [Structure Is Cheap, Grounding Is Not: Three measurement faults and a negative result in tool calling at 103M-135M parameters](<https://doi.org/10.5281/zenodo.21725247>) | 2026-07 | IC4 | Chamadas de ferramenta por modelos de 103-135M com aterramento em estado. |
| [StructureBench: A Unified Benchmark Suite for Multi-Scenario Structured Generation Tasks with On-Device Models](<https://doi.org/10.24963/ijcai.2026/267>) | 2026-09 | IC4 | Benchmark de geração estruturada e decodificação restrita em modelos on-device. |
| [Resumen de GenSIE en IberLEF 2026: extracción de información guiada por esquemas con modelos de lenguaje pequeños en español](<https://openalex.org/W7222860814>) | 2026-09 | IC4 | Tarefa compartilhada de extração guiada por esquema JSON com SLMs. |
| [Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B Small Language Models for Edge Deployment](<https://doi.org/10.48550/arxiv.2609.07370>) | 2026-09 | IC4 | Benchmark de chamadas de ferramenta JSON em SLMs abaixo de 2B. |
| [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](<https://doi.org/10.48550/arxiv.2609.09476>) | 2026-09 | IC4 | SLMs 270M-1.7B geram chamadas de função com esquemas. |
| [Comparació de models de llenguatge de difusió i auto-regressius](<https://openalex.org/W7212349642>) | 2026-09 | IC4 | Compara difusão e autoregressivo com decodificação restrita e IFEval. |
| [Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap](<https://doi.org/10.48550/arXiv.2609.23742>) | 2026-09 | IC4 | Benchmark de saída estruturada em SLMs 0,6-4B com decodificação restrita. |
| [Plan-and-Patch: Diffusion Language Models for Agentic Planning](<https://doi.org/10.48550/arxiv.2610.10786>) | 2026-10 | IC4 | DreamReasoner-8B (difusão) × Qwen3-8B (AR) na geração e reparo localizado de planos estruturados. |
| [DConstrain: Compiling Context-Parameterized Transitions for Diffusion Language Model Constrained Decoding](<https://doi.org/10.48550/arxiv.2610.30920>) | 2026-10 | IC4 | Decodificação restrita por esquema para modelos de difusão. |
| [Self-Healing JSON Generation in Small Language Models: A Systematic Evaluation of Syntax Repair, Schema Coercion, and Validator Feedback](<https://doi.org/10.21203/rs.3.rs-11641294/v1>) | 2026-11 | IC4 | Avalia reparo de JSON e validação de esquema em SLMs 360M-1.5B. |

## Apêndice B — Reprodução

Este documento é gerado. O protocolo, os scripts .NET (*file-based apps*), os *snapshots* das bases e as decisões da triagem estão em [mapeamento_sistematico/](./mapeamento_sistematico/README.md). As etapas são:

1. **Calibração:** `dotnet run scripts/mapeamento.cs -- calibrar` obtém no OpenAlex os metadados do QGS (29 positivos), dos 213 negativos e dos fundamentos.
2. **Coleta:** `sensibilidade`, `coletar-openalex` e `coletar-s2` aplicam as strings S1–S6 do [protocolo](./mapeamento_sistematico/protocolo/protocolo.json) e fazem o *snowballing*.
3. **Pré-triagem e lotes:** `pretriar` deduplica e aplica as regras; `lotes` gera os lotes de leitura e a amostra de auditoria.
4. **Triagem por leitura:** `dotnet run scripts/triagem.cs` envia os lotes ao GitHub Copilot pelo Copilot SDK, com o [roteiro de triagem](./mapeamento_sistematico/protocolo/roteiro_triagem.md) como mensagem de sistema. O script usa apenas os modelos de menor preço por token listados pelo SDK e impõe um teto acumulado de 1.000 créditos de IA, registrado em `custo_llm.jsonl` e repassado ao servidor como limite de sessão.
5. **Consolidação e relatório:** `consolidar` mede a concordância com os controles; `relatorio` gera este documento, o inventário CSV e o RIS.

A execução de 12 de novembro de 2026 pode ser reproduzida sem acesso às bases nem ao LLM com `pwsh mapeamento_sistematico/executar.ps1 -Offline`, que recalcula as etapas 3 e 5 a partir dos *snapshots* e das decisões salvas.

## 6. Arquivos e organização no Zotero

- [Inventário completo da triagem (CSV)](./mapeamento_2025_2026_inventario_triagem.csv): 6.298 registros com decisão, códigos, relevância e justificativa.
- [RIS do Nível 2](./mapeamento_gu_json_nivel2_2025_2026.ris): 50 estudos dos Quadros 3 e 4. Contém título, data, DOI, URL, resumo e palavras-chave com os critérios. Os autores vêm do Semantic Scholar e constam em 34 dos 50 registros. Para os demais, após a importação, usar **Recuperar metadados** ou importar pelo DOI no Zotero com “Adicionar item por identificador”.
- [RIS do Nível 1](./mapeamento_gu_json_2025_2026.ris): 29 estudos e quatro fundamentos, total de 33 registros. O arquivo [RIS sem duplicatas conhecidas](./mapeamento_gu_json_novos_2025_2026.ris) contém 24 registros e exclui nove trabalhos que já estavam na biblioteca.
- **Pendências no Zotero 9.0.6, não concluídas nesta sessão:**
  - renomear `01_metodologicosi` para `01_metodologicos`;
  - remover a coleção vazia duplicada na raiz de `tcc_harnes_slm`;
  - importar os arquivos RIS na subcoleção `02_dominio > mapeamento_sistematico_2025_2026`.
- **Limitação técnica:** a API local com gravação exige Zotero 10, e não havia CLI disponível. Não afirmar que os registros já estão na biblioteca antes de confirmar a importação.
