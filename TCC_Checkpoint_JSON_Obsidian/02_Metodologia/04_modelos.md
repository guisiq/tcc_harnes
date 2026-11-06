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
- a linhagem compartilhada com o candidato diffusion é uma possibilidade a confirmar pela documentação do checkpoint; não presumir pareamento de treinamento.

Model card:
https://huggingface.co/Qwen/Qwen3-0.6B

Fundamento: [[06_Referencias/referencias#Qwen3 Technical Report|Qwen3 Technical Report, 2025]]. Fixar e registrar o modo thinking, pois o cartão oferece modos distintos; não confundir limite total de geração com espaço disponível para o JSON final. Licença indicada no cartão: Apache-2.0.

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

O relatório é vinculado pelo cartão oficial. B-B pertence à série T5-compatible; acesso aos pesos exige aceite da licença Gemma. Caracterização bibliográfica não confirma execução local nem superioridade no GU-json. [[06_Referencias/referencias#T5Gemma|T5Gemma, 2025]].

---

## Writer 3 — diffusion

### Qwen3-0.6B Diffusion BD3LM

Papel: representante diffusion/block diffusion.

Características pretendidas, ainda dependentes da confirmação do checkpoint:

- linhagem Qwen3 e escala compacta;
- difusão dentro de blocos, com geração sequencial entre blocos;
- atualização de estado sob o mesmo protocolo, sem pressupor vantagem em correção de estruturas.

Fundamento específico: [[06_Referencias/referencias#Block Diffusion|Block Diffusion, Arriola et al., 2025]]. Complemento sobre adaptação AR→diffusion: [[06_Referencias/referencias#Diffusion adaptation|Gong et al., 2024/2025]]. Nenhum desses artigos, sozinho, confirma o candidato Qwen3-0.6B.

> Confirmar no início da implementação o repositório exato e a API recomendada do checkpoint BD3LM usado, pois modelos experimentais diffusion mudam rapidamente.

---

## Limites da evidência sobre difusão

Lu et al. (2026) avaliam modelos de 7–8B e encontram resultados dependentes da tarefa: dificuldades em ferramentas, mas memória textual competitiva. Mündler et al. (2025) mostram mitigação sintática com constrained decoding. Esses resultados não antecipam a qualidade do candidato compacto em GU-json prompt-only e não acrescentam condições ao experimento. [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al.]]; [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al.]].

---

## Observação metodológica

A comparação é entre **representantes de paradigmas**, não uma inferência causal pura sobre arquitetura. Os modelos diferem em treinamento, tokenizer e pós-treinamento.
