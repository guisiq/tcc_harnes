# Modelos do piloto

## Qwen2.5-3B-Instruct

A literatura encontrada via SciSpace inclui trabalhos com Qwen2.5 em escalas pequenas e avaliações voltadas a eficiência/local deployment. Um estudo comparativo de fine-tuning eficiente inclui explicitamente Qwen2.5 1.5B/3B e mostra o uso desses modelos como alternativas de menor custo para tarefas especializadas.

### Nguyen, Nguyen & Vu (2026) — *Parameter-efficient fine-tuning of small language models for code generation: a comparative study of Gemma, Qwen 2.5 and Llama 3.2*
DOI: 10.11591/ijece.v16i1.pp278-287

**Uso na ficha:** sustenta a existência e uso experimental de Qwen2.5-3B como SLM.

## Phi-3 Mini

### Abdin et al. (2024) — *Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone*
DOI: 10.48550/arxiv.2404.14219

Apresenta o Phi-3-mini com 3.8B parâmetros, descrevendo-o como pequeno o bastante para implantação em telefone e avaliando desempenho em benchmarks acadêmicos.

**Uso na ficha:** sustenta a inclusão de Phi-3 mini como baseline Transformer pequeno para execução local.

## RecurrentGemma 2B

### Botev et al. (2024) — *RecurrentGemma: Moving Past Transformers for Efficient Open Language Models*
DOI: 10.48550/arxiv.2404.07839

Apresenta RecurrentGemma, baseado na arquitetura Griffin, que combina recorrência linear e atenção local. O trabalho destaca estado de tamanho fixo, menor uso de memória em sequências longas e variante instruction-tuned de aproximadamente 2B parâmetros não-embedding.

**Uso na ficha:** sustenta diretamente a descrição arquitetural “Griffin, atenção local e recorrência” e sua inclusão como arquitetura híbrida recorrente.

## Mamba / State Space Models

### Galim et al. (2024) — *Parameter-Efficient Fine-Tuning of State Space Models*
DOI: 10.48550/arxiv.2410.09016

O estudo trata explicitamente de modelos State Space, incluindo Mamba, destacando inferência eficiente e escalabilidade linear com o comprimento da sequência.

**Uso na ficha:** sustenta a classificação de Mamba como arquitetura State Space Model (SSM). A variante exata “~2.8B instruction-tuned” ainda deve ser fixada e citada quando o checkpoint concreto do piloto for escolhido.

## Observação

A ficha menciona “Phi-3.5-mini-Instruct ou Gemma pequeno equivalente” e “Mamba aproximadamente 2.8B instruction-tuned”. Como essas escolhas ainda são alternativas, a referência acadêmica sustenta a família/arquitetura, mas o modelo/checkpoint final deve ser documentado após a seleção definitiva.
