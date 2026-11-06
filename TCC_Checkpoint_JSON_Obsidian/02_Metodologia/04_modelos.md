---
title: "Modelos do experimento"
aliases:
  - "04 modelos"
tags:
  - tcc
  - metodologia
status: draft
---

# Modelos do experimento

## Critérios de seleção

- pequenos o suficiente para execução local;
- abertos ou publicamente acessíveis;
- próximos em escala;
- adequados a geração de texto;
- representantes claros de paradigmas distintos;
- preferencialmente instruction-tuned.

## Writer 1 — decoder-only autoregressivo

### Qwen3-0.6B

Papel: baseline autoregressiva.

Razões:

- escala próxima dos demais;
- modelo pequeno e atual;
- forte ecossistema;
- o writer diffusion escolhido é derivado da mesma linhagem Qwen3, reduzindo parte do confundimento entre AR e diffusion.

Model card:
https://huggingface.co/Qwen/Qwen3-0.6B

---

## Writer 2 — encoder-decoder

### T5Gemma B-B PrefixLM-IT

Papel: representante encoder-decoder.

Razões:

- instruction-tuned;
- text-to-text;
- escala aproximada de ~0.6B;
- transformação `estado anterior + nova informação -> estado novo` é naturalmente compatível com seq2seq.

Model card:
https://huggingface.co/google/t5gemma-b-b-prefixlm-it

Technical report:
https://arxiv.org/abs/2504.06225

---

## Writer 3 — diffusion

### Qwen3-0.6B Diffusion BD3LM

Papel: representante diffusion/block diffusion.

Razões:

- deriva da linhagem Qwen3;
- escala pequena;
- geração iterativa/não puramente esquerda→direita;
- interessante para reescrita e correção global de estruturas.

Referência de família/pesquisa:
https://arxiv.org/abs/2410.17891

> Confirmar no início da implementação o repositório exato e a API recomendada do checkpoint BD3LM usado, pois modelos experimentais diffusion mudam rapidamente.

---

## DiffusionGemma — por que não é o principal

DiffusionGemma é cientificamente relevante, mas a variante oficial divulgada é muito maior que os writers locais selecionados.

Uso no TCC:

- estado da arte/contexto;
- discussão;
- trabalho futuro.

Não usar como condição principal na GTX 1650.

Página:
https://deepmind.google/models/gemma/diffusiongemma/

---

## Observação metodológica

A comparação é entre **representantes de paradigmas**, não uma inferência causal pura sobre arquitetura. Os modelos diferem em treinamento, tokenizer e pós-treinamento.
