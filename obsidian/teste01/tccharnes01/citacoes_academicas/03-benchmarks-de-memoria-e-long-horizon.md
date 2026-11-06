# Benchmarks de memória e interações longas

Atualização bibliográfica: 2026-11-06. O protocolo atual usa SUMIE e somente uma amostra FactConsolidation-SH, sem avaliação downstream nem métricas de desempenho computacional. [Datasets atuais](../../../../TCC_Checkpoint_JSON_Obsidian/02_Metodologia/03_datasets.md).

## Afirmações sustentadas

- LoCoMo e LongMemEval são exemplos de avaliação conversacional longa; sua existência não demonstra predominância estatística desse cenário na literatura.
- Modelos ainda apresentam dificuldades em compreender relações temporais/causais de longo alcance e em manter consistência ao longo de interações extensas.
- Benchmarks recentes tratam memória como uma capacidade distinta de raciocínio, planejamento e execução.

## Referências localizadas via SciSpace

### Maharana et al. (2024) — *Evaluating Very Long-Term Conversational Memory of LLM Agents*
DOI: 10.48550/arxiv.2402.17753

Apresenta o LoCoMo, com conversas longas distribuídas em múltiplas sessões. Os experimentos mostram dificuldades dos LLMs em compreender conversações extensas e relações temporais/causais de longo alcance; estratégias de long context e RAG melhoram resultados, mas ainda ficam abaixo do desempenho humano.

**Uso na ficha:** exemplo contextual de memória conversacional, não fundamento direto do GU-json. Para atualização de conhecimento, priorizar [LongMemEval](https://arxiv.org/abs/2410.10813) junto de [MemoryAgentBench](https://arxiv.org/abs/2507.05257).

### Hu, Wang & McAuley (2025/2026) — *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*
DOI: 10.48550/arxiv.2507.05257

O MemoryAgentBench foi criado porque benchmarks de agentes enfatizavam raciocínio, planejamento e execução, enquanto a memória permanecia subavaliada. O benchmark cobre recuperação, aprendizado em teste, compreensão de longo alcance e resolução de conflitos.

**Uso na ficha:** sustenta que memória merece avaliação própria e que há lacunas metodológicas nos benchmarks existentes.

Preprint de 2025; revisão v4 de junho de 2026; ICLR 2026 informado no repositório dos autores. FactConsolidation determina que fatos mais recentes invalidem os anteriores. Os resultados dependem de modelo/contexto e medem respostas finais, não fidelidade de estado. A divergência de licenças entre cartão do dataset e artigo deve ser resolvida antes da coleta.

### Xu et al. (2026) — *Chain-of-Memory: Lightweight Memory Construction with Dynamic Evolution for LLM Agents*
DOI: 10.48550/arxiv.2601.14287

Estuda construção de memória e raciocínio sobre fragmentos recuperados, com avaliações no LongMemEval e LoCoMo. Preprint de janeiro de 2026, revisão de abril; ACL 2026 informado no repositório dos autores.

**Uso na ficha:** contexto de sistemas de memória, não justificativa de novas métricas ou prova de fidelidade GU-json. [Artigo](https://arxiv.org/abs/2601.14287).

### SUMIE e LongMemEval: papéis distintos

[SUMIE, COLING 2025](https://aclanthology.org/2025.coling-main.721/) fornece anotações por parágrafo e preserva perspectivas conflitantes, não aplica substituição automática. [LongMemEval, 2025](https://arxiv.org/abs/2410.10813) motiva atualização de conhecimento por avaliação de respostas, sem entrar na coleta.

SUMIE/FactConsolidation têm políticas e domínios distintos; uma diferença entre seus resultados não isola o efeito de supersession. [Bibliografia e limites](../../../../TCC_Checkpoint_JSON_Obsidian/06_Referencias/referencias.md).

## Grau de evidência

**Direta** para as tarefas e métricas examinadas em cada artigo. **Indireta** para fidelidade de checkpoints JSON, que exige adaptação dos estados e da avaliação; não prova predominância de um domínio nem confirma a H2.
