# Estruturas de memória: sumarização, fatos estruturados e JSON

## Afirmações sustentadas

- A representação usada pela memória de um agente influencia desempenho e robustez.
- Resumos são apenas uma entre várias estruturas possíveis de memória; fatos atômicos, triplas e estruturas mistas podem ter vantagens distintas.
- Representações estruturadas em JSON podem reduzir sobrecarga de informação e melhorar a preservação/organização de conteúdo em tarefas de sumarização incremental.
- Não há, nas fontes encontradas, evidência direta suficiente para afirmar de antemão que “checkpoint JSON preserva mais restrições do que sumarização textual” no recorte exato deste TCC; isso permanece hipótese experimental.

## Referências localizadas via SciSpace

### Zeng et al. (2024) — *On the Structural Memory of LLM Agents*
DOI: 10.48550/arxiv.2412.15266

Compara estruturas de memória formadas por chunks, triplas de conhecimento, fatos atômicos, resumos e combinações dessas estruturas em quatro tarefas e seis datasets. O estudo conclui que estruturas distintas apresentam vantagens distintas e que memória mista pode ser resiliente a ruído.

**Uso na ficha:** fundamenta a comparação entre sumarização e uma representação estruturada, sem predeterminar qual estratégia será superior.

### Hwang et al. (2024) — *Enhancing Incremental Summarization with Structured Representations*
DOI: 10.48550/arxiv.2407.15021

O trabalho introduz representações de conhecimento estruturadas em JSON para sumarização incremental e relata ganhos de desempenho em dois datasets, além de uma estratégia de atualização incremental da estrutura.

**Uso na ficha:** evidência relacionada de que estruturas JSON podem organizar e preservar informação de forma útil em processamento incremental. Não é um estudo de retomada de agentes interrompidos; portanto, o suporte é indireto para H1/H3.

### Yuen et al. (2025) — *Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory*
DOI: 10.48550/arxiv.2508.08997

Propõe memórias estruturadas específicas por agente para preservar informação relevante à função, relatando ganhos em tarefas estruturadas de planejamento.

**Uso na ficha:** reforça a plausibilidade de estruturas explícitas de memória em tarefas estruturadas, mas não testa checkpoints JSON versus resumo textual.

## Grau de evidência

**Forte** para “a estrutura da memória importa”.

**Moderado/indireto** para vantagens de JSON/estrutura sobre texto livre.

**Ainda não demonstrado** para H1 no protocolo específico deste TCC; deve permanecer explicitamente como hipótese.
