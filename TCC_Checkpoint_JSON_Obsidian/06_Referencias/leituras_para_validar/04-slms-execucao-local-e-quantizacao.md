# SLMs, execução local e quantização

Nota do acervo histórico. A auditoria de 2026-11-06 não reavaliou integralmente os três trabalhos abaixo; seus resultados não acrescentam métricas ou condições ao TCC atual. O estudo mede qualidade de estado, não latência, throughput ou uso de RAM/VRAM. Consulte os [modelos e o ambiente no artigo atual](../../07_Artigo_TCC/artigo_tcc_unitins.md#3-materiais-e-métodos).

Para caracterizar os representantes atuais, priorizar [Qwen3 Technical Report, 2025](https://arxiv.org/abs/2505.09388) e [T5Gemma, 2025](https://arxiv.org/abs/2504.06225). Para BD3LM, complementar [Block Diffusion, 2025](https://arxiv.org/abs/2503.09573) com o relatório do checkpoint Qwen exato, ainda não confirmado. Escala aproximada não garante execução no hardware local.

## Afirmações sustentadas

- SLMs na faixa de centenas de milhões a poucos bilhões de parâmetros são estudados como alternativa para execução eficiente em dispositivos e ambientes com recursos limitados.
- Estudos de implantação local examinam métricas computacionais, que não são variáveis dependentes do protocolo vigente.
- Quantização reduz uso de memória e custo de inferência, mas pode introduzir perdas de qualidade, especialmente em modelos menores e níveis agressivos de compressão.

## Referências localizadas via SciSpace

### Lu et al. (2024) — *Small Language Models: Survey, Measurements, and Insights*
DOI: 10.48550/arxiv.2409.15790

Revisa 59 SLMs open source entre 100M e 5B parâmetros e mede, entre outros aspectos, latência de inferência e footprint de memória em execução on-device.

**Uso no acervo:** contexto geral de SLMs. Não fundamenta incluir métricas computacionais no recorte vigente; os relatórios dos modelos escolhidos são fontes mais diretas para sua caracterização.

### Lee et al. (2025) — *Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Language Models From Edge to Giant*
DOI: 10.24963/ijcai.2025/902

Avalia modelos instruction-tuned de 1B a 405B sob diferentes métodos de quantização. Relata que modelos menores podem sofrer quedas importantes em 4-bit e que a robustez depende do método e da tarefa.

**Uso na ficha:** sustenta que quantização é viável para implantação compacta, mas precisa ser tratada como condição experimental capaz de afetar resultados.

### Yuan et al. (2025) — *EfficientLLM: Efficiency in Large Language Models*
DOI: 10.48550/arxiv.2505.13840

Define métricas de eficiência como utilização de memória, latência, throughput, energia e compressão e compara técnicas de quantização em modelos de 0.5B a 72B.

**Uso no acervo:** contexto de implantação e compressão; não define métricas do experimento atual.

## Grau de evidência

Os estudos descritos são contexto de implantação, não prova de qualidade de writers GU-json ou de compatibilidade local. A configuração de 6 GB de VRAM/16 GB RAM pertence à formulação antiga; consultar o [ambiente descrito no artigo vigente](../../07_Artigo_TCC/artigo_tcc_unitins.md#3-materiais-e-métodos). Não extrapolar essas fontes para confirmar as hipóteses atuais.
