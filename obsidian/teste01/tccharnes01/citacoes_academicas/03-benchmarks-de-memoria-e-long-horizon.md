# Benchmarks de memória e interações longas

## Afirmações sustentadas

- Parte relevante da literatura recente de memória em agentes avalia conversações longas e multi-sessão.
- Modelos ainda apresentam dificuldades em compreender relações temporais/causais de longo alcance e em manter consistência ao longo de interações extensas.
- Benchmarks recentes tratam memória como uma capacidade distinta de raciocínio, planejamento e execução.

## Referências localizadas via SciSpace

### Maharana et al. (2024) — *Evaluating Very Long-Term Conversational Memory of LLM Agents*
DOI: 10.48550/arxiv.2402.17753

Apresenta o LoCoMo, com conversas longas distribuídas em múltiplas sessões. Os experimentos mostram dificuldades dos LLMs em compreender conversações extensas e relações temporais/causais de longo alcance; estratégias de long context e RAG melhoram resultados, mas ainda ficam abaixo do desempenho humano.

**Uso na ficha:** sustenta a afirmação de que grande parte da avaliação de memória recente está concentrada em memória conversacional e interações longas.

### Hu, Wang & McAuley (2025) — *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*
DOI: 10.48550/arxiv.2507.05257

O MemoryAgentBench foi criado porque benchmarks de agentes enfatizavam raciocínio, planejamento e execução, enquanto a memória permanecia subavaliada. O benchmark cobre recuperação, aprendizado em teste, compreensão de longo alcance e resolução de conflitos.

**Uso na ficha:** sustenta que memória merece avaliação própria e que há lacunas metodológicas nos benchmarks existentes.

### Xu et al. (2026) — *Chain-of-Memory: Lightweight Memory Construction with Dynamic Evolution for LLM Agents*
DOI: 10.48550/arxiv.2601.14287

Avalia memória no LongMemEval e LoCoMo, comparando precisão, consumo de tokens e latência. O trabalho mostra que desempenho e custo computacional podem variar substancialmente conforme a arquitetura de memória.

**Uso na ficha:** sustenta a inclusão de métricas de confiabilidade e eficiência, como acurácia/sucesso, tokens e latência.

## Grau de evidência

**Forte** para a predominância de contextos conversacionais/long-horizon entre benchmarks importantes e para a existência de limitações de memória de longo prazo.

**Indireto** para tarefas determinísticas interrompidas, já que LoCoMo/LongMemEval não reproduzem exatamente o protocolo proposto no TCC.
