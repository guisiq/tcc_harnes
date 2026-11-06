# Memória e persistência em agentes

Revisão de citações: 2026-11-06. O recorte atual compara writers GU-json; retomada após interrupção pertence à formulação anterior. [Bibliografia auditada](../../../../TCC_Checkpoint_JSON_Obsidian/06_Referencias/referencias.md).

## Afirmações sustentadas

- Há sistemas de agentes que mantêm memória contextual atualizada entre etapas, com mecanismos distintos: [Intrinsic Memory Agents](https://arxiv.org/abs/2508.08997) e [PRISM](https://aclanthology.org/2025.emnlp-main.517/).
- Memória persistente e consciência de estado podem contribuir para planejamento, recuperação após falhas e consistência operacional.
- As avaliações revelam limitações dependentes de tarefa, modelo e contexto; atualização de conhecimento é examinada por [MemoryAgentBench](https://arxiv.org/abs/2507.05257) e [LongMemEval](https://arxiv.org/abs/2410.10813), sem medir diretamente fidelidade de checkpoints JSON.

## Referências e limites de uso

As fontes inicialmente localizadas via SciSpace foram complementadas com a auditoria. Muhoberac permanece fonte do acervo anterior; seu texto não foi reavaliado nesta auditoria de 19 entradas do vault principal.

### Muhoberac et al. (2025) — *State and Memory is All You Need for Robust and Reliable AI Agents*
DOI: 10.48550/arxiv.2507.00081

O trabalho apresenta o SciBORG, no qual agentes usam memória baseada em autômatos de estados finitos para rastreamento persistente de estado e decisões dependentes de contexto. Os autores relatam uso em fluxos científicos de múltiplas etapas e recuperação de falhas de ferramenta/execução, concluindo que memória e consciência de estado são habilitadores importantes de planejamento e confiabilidade.

**Uso na ficha:** sustenta diretamente a necessidade de estado operacional consistente e a relevância de persistência em tarefas de múltiplas etapas.

### Hu, Wang & McAuley (2025/2026) — *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*
DOI: 10.48550/arxiv.2507.05257

Propõe o MemoryAgentBench e identifica quatro competências centrais de memória: recuperação precisa, aprendizado em tempo de teste, compreensão de longo alcance e resolução de conflitos. Os resultados indicam que métodos atuais não dominam todas essas competências.

**Uso na ficha:** sustenta que memória é um componente crítico e ainda insuficientemente avaliado em agentes.

Preprint de 2025, revisão v4 de junho de 2026; aceitação no ICLR 2026 informada no repositório. FactConsolidation define precedência temporal e avalia respostas finais, não remoção de fatos do estado. Complementar com [LongMemEval](https://arxiv.org/abs/2410.10813) para atualização de conhecimento; não inferir a H2 dos writers compactos a partir desses resultados.

### Zeng et al. (2024) — *On the Structural Memory of LLM Agents*
DOI: 10.48550/arxiv.2412.15266

Avalia diferentes estruturas de memória (chunks, triplas de conhecimento, fatos atômicos, resumos e memória mista) e diferentes métodos de recuperação. Mostra que a estrutura de memória afeta o desempenho e que diferentes estruturas têm vantagens distintas conforme a tarefa.

**Uso na ficha:** sustenta diferenças entre representação e recuperação. Não fundamenta reescrita GU-json, supersession ou retomada após interrupção. Para atualização persistente, substituir seu uso central por [Hwang, 2024](https://aclanthology.org/2024.findings-emnlp.220/) e [PRISM, 2025](https://aclanthology.org/2025.emnlp-main.517/), mantendo Zeng como contexto.

## Grau de evidência

**Direta em configurações específicas** para os mecanismos e limitações estudados; não estabelece superioridade universal de representação ou método.

**Moderado** para a afirmação específica de que “retomada após interrupção” é um subproblema suficientemente coberto pela literatura; há evidência relacionada, mas o recorte exato do TCC permanece uma lacuna a verificar.
