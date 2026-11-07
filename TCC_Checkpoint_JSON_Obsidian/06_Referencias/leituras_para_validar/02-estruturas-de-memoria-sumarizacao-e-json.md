# Estruturas de memória: sumarização, fatos estruturados e JSON

Atualização bibliográfica: 2026-11-06. A comparação atual é entre writers sob GU-json fixo, não JSON versus texto nem retomada após interrupção. [Artigo atual](../../07_Artigo_TCC/artigo_tcc_unitins.md); [bibliografia auditada](../referencias.md).

## Afirmações sustentadas

- A representação pode afetar resultados em configurações específicas; [Zeng](https://arxiv.org/abs/2412.15266) estuda estruturas e recuperação, enquanto [Hwang](https://aclanthology.org/2024.findings-emnlp.220/) estuda atualização incremental.
- Resumos são apenas uma entre várias estruturas possíveis de memória; fatos atômicos, triplas e estruturas mistas podem ter vantagens distintas.
- Hwang relata vantagem de GU-json sobre GU-text sob memória limitada, mas CoK supera as baselines; isso não torna GU universalmente superior.
- [PRISM, 2025](https://aclanthology.org/2025.emnlp-main.517/) e [Intrinsic Memory Agents, revisão 2026](https://arxiv.org/abs/2508.08997) oferecem mecanismos próximos de atualização persistente, sem demonstrar vantagem do schema fixo do TCC.

## Referências e limites de uso

### Zeng et al. (2024) — *On the Structural Memory of LLM Agents*
DOI: 10.48550/arxiv.2412.15266

Compara estruturas de memória formadas por chunks, triplas de conhecimento, fatos atômicos, resumos e combinações dessas estruturas em quatro tarefas e seis datasets. O estudo conclui que estruturas distintas apresentam vantagens distintas e que memória mista pode ser resiliente a ruído.

**Uso na ficha:** contexto de representação e recuperação, não evidência direta de checkpoint JSON reescrito. Para esse argumento, priorizar Hwang e PRISM.

### Hwang et al. (2024) — *Enhancing Incremental Summarization with Structured Representations*
DOI: 10.48550/arxiv.2407.15021

O trabalho introduz representações de conhecimento estruturadas em JSON para sumarização incremental e relata ganhos de desempenho em dois datasets, além de uma estratégia de atualização incremental da estrutura.

**Uso na ficha:** fundamento direto do protocolo GU-json, publicado em Findings EMNLP 2024. Não estuda os três writers compactos propostos. [Versão publicada](https://aclanthology.org/2024.findings-emnlp.220/).

### Yuen et al. (2025/2026) — *Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory*
DOI: 10.48550/arxiv.2508.08997

Propõe atualização de memórias específicas por agente. A revisão de janeiro de 2026 inclui template genérico com representação livre; templates genéricos/gerados superam os manuais em vários testes.

**Uso na ficha:** precedente de atualização contextual, não evidência de que JSON manual fixo seja superior; resultados de sistemas multiagente não equivalem a fidelidade por transição.

### Jayalath et al. (2025) — *PRISM: Efficient Long-Range Reasoning With Short-Context LLMs*

[EMNLP 2025](https://aclanthology.org/2025.emnlp-main.517/). Substitui o título do preprint de 2024. Mantém memória tipada com operações validadas e aplicadas programaticamente, não por reescrita integral GU. Complementa Hwang e substitui Zeng como apoio central à atualização persistente, sem provar superioridade sobre GU-json.

### Hwang et al. (2025) — SUMIE

[COLING 2025](https://aclanthology.org/2025.coling-main.721/). O prompt UPDATE preserva valores e perspectivas conflitantes. Anotações por parágrafo devem ser adaptadas para checkpoints acumulados; o State F1 determinístico não equivale automaticamente ao F1 original, que inclui avaliação semântica de evidências.

## Grau de evidência

**Direta** para GU-json no cenário de Hwang e para os mecanismos descritos em cada artigo. **Indireta** para os três writers compactos: não antecipar vencedor, superioridade de schema ou confirmação das hipóteses atuais.
