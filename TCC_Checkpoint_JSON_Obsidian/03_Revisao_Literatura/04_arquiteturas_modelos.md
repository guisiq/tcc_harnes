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

Questão empírica:
- geração condicionada ao prefixo não garante sintaxe correta nem preservação semântica;
- diferenças de fidelidade devem ser medidas, não deduzidas apenas da fatorização.

Representante:
[Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)

[[06_Referencias/referencias#Qwen3 Technical Report|Qwen3 Technical Report, 2025]]. O cartão oficial disponibiliza modos com e sem thinking; fixar essa configuração para não tornar ambíguo o orçamento de saída.

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

O B-B pertence à série T5-compatible, não é simplesmente uma conversão do Gemma 2 2B. O relatório e cartão caracterizam o modelo, mas não demonstram vantagem no GU-json. [[06_Referencias/referencias#T5Gemma|T5Gemma, 2025]].

---

## Diffusion language model

Em difusão mascarada, tokens são refinados iterativamente. Em BD3LM, há geração sequencial entre blocos e difusão dentro de cada bloco; não tratar todos os modelos de difusão como geração inteiramente paralela. [[06_Referencias/referencias#Block Diffusion|Arriola et al., 2025]]; [[06_Referencias/referencias#Scaling masked diffusion|Nie et al., 2024/2025]].

Propriedades de interesse:
- condicionamento bidirecional;
- revisão iterativa;
- potencial para infilling/rewriting;
- custo associado a múltiplos passos de denoising.

### DiffuLLaMA / DiffuGPT

**Scaling Diffusion Language Models via Adaptation from Autoregressive Models**

Modelos convertidos de AR para diffusion em escalas pequenas e grandes.

https://arxiv.org/abs/2410.17891

Preprint de 2024; ICLR 2025 informado no arXiv. Fundamenta adaptação geral, não a origem do candidato Qwen3-0.6B BD3LM. [[06_Referencias/referencias#Diffusion adaptation|Referência completa]].

### Scaling up Masked Diffusion Models on Text

https://arxiv.org/abs/2410.18514

### Block Diffusion e contrapontos

[[06_Referencias/referencias#Block Diffusion|Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models, 2025]] é a referência específica para BD3LM. Confirmar checkpoint, treinamento e API antes de atribuir suas propriedades ao candidato Qwen.

Lu et al. (2026) relatam dificuldades em ferramentas e resultados competitivos em memória textual; Mündler et al. (2025) mostram melhora sintática com restrições. São contrapontos em configurações distintas, não previsão de resultados para GU-json prompt-only. [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al.]]; [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al.]].

## Comparação responsável

Não escrever:

> "Arquitetura X é superior."

Preferir:

> "No conjunto de modelos compactos selecionados, o representante X apresentou..."

Isso reduz inferências causais excessivas.
