# Memória e persistência em agentes

## Afirmações sustentadas

- Agentes baseados em modelos de linguagem precisam de mecanismos de memória/estado para manter continuidade em interações extensas e tarefas de múltiplas etapas.
- Memória persistente e consciência de estado podem contribuir para planejamento, recuperação após falhas e consistência operacional.
- Sistemas atuais ainda apresentam limitações de memória de longo prazo, o que justifica avaliações específicas desse componente.

## Referências localizadas via SciSpace

### Muhoberac et al. (2025) — *State and Memory is All You Need for Robust and Reliable AI Agents*
DOI: 10.48550/arxiv.2507.00081

O trabalho apresenta o SciBORG, no qual agentes usam memória baseada em autômatos de estados finitos para rastreamento persistente de estado e decisões dependentes de contexto. Os autores relatam uso em fluxos científicos de múltiplas etapas e recuperação de falhas de ferramenta/execução, concluindo que memória e consciência de estado são habilitadores importantes de planejamento e confiabilidade.

**Uso na ficha:** sustenta diretamente a necessidade de estado operacional consistente e a relevância de persistência em tarefas de múltiplas etapas.

### Hu, Wang & McAuley (2025) — *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*
DOI: 10.48550/arxiv.2507.05257

Propõe o MemoryAgentBench e identifica quatro competências centrais de memória: recuperação precisa, aprendizado em tempo de teste, compreensão de longo alcance e resolução de conflitos. Os resultados indicam que métodos atuais não dominam todas essas competências.

**Uso na ficha:** sustenta que memória é um componente crítico e ainda insuficientemente avaliado em agentes.

### Zeng et al. (2024) — *On the Structural Memory of LLM Agents*
DOI: 10.48550/arxiv.2412.15266

Avalia diferentes estruturas de memória (chunks, triplas de conhecimento, fatos atômicos, resumos e memória mista) e diferentes métodos de recuperação. Mostra que a estrutura de memória afeta o desempenho e que diferentes estruturas têm vantagens distintas conforme a tarefa.

**Uso na ficha:** sustenta a premissa de que a forma de persistir memória pode influenciar o comportamento do agente.

## Grau de evidência

**Forte** para a importância de memória/estado persistente em agentes e para a existência de limitações atuais.

**Moderado** para a afirmação específica de que “retomada após interrupção” é um subproblema suficientemente coberto pela literatura; há evidência relacionada, mas o recorte exato do TCC permanece uma lacuna a verificar.
