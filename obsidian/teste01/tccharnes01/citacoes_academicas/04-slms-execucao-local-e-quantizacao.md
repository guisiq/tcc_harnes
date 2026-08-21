# SLMs, execução local e quantização

## Afirmações sustentadas

- SLMs na faixa de centenas de milhões a poucos bilhões de parâmetros são estudados como alternativa para execução eficiente em dispositivos e ambientes com recursos limitados.
- Latência e consumo de memória são métricas relevantes para avaliar implantação local.
- Quantização reduz uso de memória e custo de inferência, mas pode introduzir perdas de qualidade, especialmente em modelos menores e níveis agressivos de compressão.

## Referências localizadas via SciSpace

### Lu et al. (2024) — *Small Language Models: Survey, Measurements, and Insights*
DOI: 10.48550/arxiv.2409.15790

Revisa 59 SLMs open source entre 100M e 5B parâmetros e mede, entre outros aspectos, latência de inferência e footprint de memória em execução on-device.

**Uso na ficha:** fundamenta o recorte de SLMs pequenos e a escolha de latência/memória como métricas de eficiência.

### Lee et al. (2025) — *Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Language Models From Edge to Giant*
DOI: 10.24963/ijcai.2025/902

Avalia modelos instruction-tuned de 1B a 405B sob diferentes métodos de quantização. Relata que modelos menores podem sofrer quedas importantes em 4-bit e que a robustez depende do método e da tarefa.

**Uso na ficha:** sustenta que quantização é viável para implantação compacta, mas precisa ser tratada como condição experimental capaz de afetar resultados.

### Yuan et al. (2025) — *EfficientLLM: Efficiency in Large Language Models*
DOI: 10.48550/arxiv.2505.13840

Define métricas de eficiência como utilização de memória, latência, throughput, energia e compressão e compara técnicas de quantização em modelos de 0.5B a 72B.

**Uso na ficha:** sustenta o uso de latência e memória/VRAM como variáveis de eficiência e a existência de trade-offs entre compressão e qualidade.

## Grau de evidência

**Forte** para a pertinência de SLMs e métricas de eficiência em execução limitada por hardware.

A restrição específica de **6 GB de VRAM e 16 GB de RAM** é uma decisão de viabilidade do experimento, não um fato bibliográfico universal.
