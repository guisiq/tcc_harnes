---
title: "Arquiteturas de modelos"
aliases:
  - "04 arquiteturas modelos"
tags:
  - tcc
  - revisao-literatura
status: draft
---

# Arquiteturas de modelos

## Decoder-only autoregressivo

Fatorização típica:

\[
p(x) = \prod_t p(x_t | x_{<t})
\]

Propriedade:
- geração estritamente condicionada ao prefixo anterior.

Hipótese de interesse:
- boa consistência sintática sequencial;
- possível propagação de erros durante reescritas longas.

Representante:
[Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)

---

## Encoder-decoder

Estrutura:

```text
input sequence
   ↓ encoder
representation
   ↓ decoder
output sequence
```

Adequado a transformações:

```text
old state + update -> new state
```

Representante:
[T5Gemma B-B PrefixLM-IT](https://huggingface.co/google/t5gemma-b-b-prefixlm-it)

Paper:
**Encoder-Decoder Gemma: Improving the Quality-Efficiency Trade-Off via Adaptation**
https://arxiv.org/abs/2504.06225

---

## Diffusion language model

Em masked/block diffusion, tokens/blocks são refinados iterativamente em vez de sempre serem comprometidos em ordem estritamente esquerda→direita.

Propriedades de interesse:
- condicionamento bidirecional;
- revisão iterativa;
- potencial para infilling/rewriting;
- custo associado a múltiplos passos de denoising.

### DiffuLLaMA / DiffuGPT

**Scaling Diffusion Language Models via Adaptation from Autoregressive Models**

Modelos convertidos de AR para diffusion em escalas pequenas e grandes.

https://arxiv.org/abs/2410.17891

### Scaling up Masked Diffusion Models on Text

https://arxiv.org/abs/2410.18514

### DiffusionGemma

https://deepmind.google/models/gemma/diffusiongemma/

Comentário:
> relevante como estado da arte, mas grande demais para o experimento local principal.

## Comparação responsável

Não escrever:

> "Arquitetura X é superior."

Preferir:

> "No conjunto de modelos compactos selecionados, o representante X apresentou..."

Isso reduz inferências causais excessivas.
