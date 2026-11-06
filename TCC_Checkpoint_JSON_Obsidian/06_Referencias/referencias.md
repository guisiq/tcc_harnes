---
title: "Referências bibliográficas"
aliases:
  - "referencias"
tags:
  - tcc
  - referencias
status: draft
---

# Referências bibliográficas

Auditoria bibliográfica: 2026-11-06. Busca selecionada, não revisão sistemática exaustiva. Distinguir ano do preprint, revisão consultada e publicação; venues informados apenas pelos autores estão assinalados. Referências complementares não acrescentam métodos, datasets ou métricas ao experimento.

## Hwang et al. — structured incremental summarization

Hwang, E.; Zhou, Y.; Wendt, J. B.; Gunel, B.; Vo, N.; Xie, J.; Tata, S. **Enhancing Incremental Summarization with Structured Representations.** Findings of EMNLP, 2024, p. 3830–3842. DOI: 10.18653/v1/2024.findings-emnlp.220.

https://aclanthology.org/2024.findings-emnlp.220/

Relação com TCC:
- GUjson;
- GMjson;
- Chain-of-Key;
- JSON vs. texto;
- atualização incremental.

Fundamento direto do protocolo GU-json. O artigo também encontra resultados superiores com CoK; não demonstra superioridade universal de GU. Comparações de métodos e de JSON/texto permanecem fora do experimento.

---

## Hwang et al. — SUMIE

Hwang, E.; Zhou, Y.; Gunel, B.; Wendt, J. B.; Tata, S. **SUMIE: A Synthetic Benchmark for Incremental Entity Summarization.** Proceedings of COLING 2025.

https://aclanthology.org/2025.coling-main.721/

Relação:
- dataset principal;
- anotações de atributos, valores e evidências por parágrafo, a adaptar para estados acumulados.

Preprint de 2024; citar a versão publicada no COLING 2025. Dataset: https://github.com/google-deepmind/sumie (repositório identificado como Apache-2.0).

Na Figura 14 da versão publicada, o prompt UPDATE preserva atributos e valores anteriores e integra perspectivas conflitantes. Conflito de opinião não implica supersession temporal. A avaliação original combina correspondência exata e avaliação de evidências por LLM; State F1 determinístico é uma adaptação que exige política de canonicalização validada.

---
## Yuen et al. — Intrinsic Memory Agents

Yuen, S.; Gomez Medina, F.; Su, T.; Du, Y.; Sobey, A. J. **Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory.** Preprint, 2025; versão 2 de 12 de janeiro de 2026.

https://arxiv.org/abs/2508.08997

Relação:
- memória contextual por agente, com JSON em algumas variantes;
- update prompt;
- templates manual/generic/LLM-generated.

A atualização a partir da memória anterior e da nova saída do agente é próxima da reescrita de estado. Entretanto, a variante genérica não exige JSON e templates genéricos/gerados superam os manuais em vários testes. Os resultados de sistemas multiagente não demonstram fidelidade por transição nem superioridade de um schema fixo.

---
## Zeng et al. — Structural Memory

Zeng, R.; Fang, J.; Liu, S.; Meng, Z. **On the Structural Memory of LLM Agents.** 2024.

https://arxiv.org/abs/2412.15266

Código:
https://github.com/zengrh3/StructuralMemory

Relação:
- tipos de estrutura;
- retrieval methods;
- distinção entre representação e atualização.

Referência contextual, não fundamento de GU-json: o estudo compara estruturas e recuperação, não a fidelidade de checkpoints JSON reescritos. Para atualização persistente, priorizar Hwang, PRISM e Intrinsic Memory Agents, respeitando as diferenças entre seus mecanismos.

---
## Hu et al. — MemoryAgentBench

Hu, Y.; Wang, Y.; McAuley, J. **Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions.** Preprint de 2025; versão 4 de 28 de junho de 2026. Aceitação no ICLR 2026 informada no repositório dos autores; anais não confirmados nesta auditoria.

https://arxiv.org/abs/2507.05257

Código: https://github.com/HUST-AI-HYZ/MemoryAgentBench

Relação:
- benchmark incremental;
- selective forgetting;
- FactConsolidation.

Dataset:
https://huggingface.co/datasets/ai-hyz/MemoryAgentBench

FactConsolidation define precedência temporal explícita: o fato mais recente invalida o anterior. O benchmark mede respostas finais, não remoção física de fatos nem fidelidade do estado. Rótulos de transição e métricas de estado são adaptações deste TCC. A dificuldade varia com modelo e contexto; não prova que supersession sempre amplie diferenças entre writers.

Licença: código MIT; há divergência entre a indicação MIT no cartão do dataset e CC BY 4.0 para artefatos no artigo v4. Confirmar licença e revisão do artefato efetivamente utilizado, respeitando os materiais de terceiros.

---
## Maharana et al. — LoCoMo

Maharana, A.; Lee, D.-H.; Tulyakov, S.; Bansal, M.; Barbieri, F.; Fang, Y. **Evaluating Very Long-Term Conversational Memory of LLM Agents.** 2024.

https://arxiv.org/abs/2402.17753

https://snap-research.github.io/locomo

Contexto de memória conversacional; não integra o experimento. Para motivar atualização de conhecimento, priorizar LongMemEval e MemoryAgentBench.

---
## Xu et al. — Chain-of-Memory

Xu, X. et al. **Chain-of-Memory: Lightweight Memory Construction with Dynamic Evolution for LLM Agents.** 2026.

https://arxiv.org/abs/2601.14287

Preprint de 14 de janeiro de 2026; revisão de 24 de abril. Aceitação no ACL 2026 informada no repositório dos autores, não confirmada nos anais nesta auditoria.

Código:
https://github.com/Xiucheng-Xu/CoM

Relação:
- construção de memória e raciocínio sobre fragmentos recuperados;
- contexto complementar, não evidência direta de atualização GU-json.

---

## T5Gemma

Zhang, B. et al. **Encoder-Decoder Gemma: Improving the Quality-Efficiency Trade-Off via Adaptation.** 2025.

https://arxiv.org/abs/2504.06225

Model:
https://huggingface.co/google/t5gemma-b-b-prefixlm-it

Relatório vinculado pelo cartão oficial. O checkpoint B-B pertence à série T5-compatible; acesso aos pesos exige aceite dos termos Gemma. Caracteriza o representante encoder-decoder, mas não antecipa sua qualidade no GU-json nem confirma compatibilidade local.

---

## Diffusion adaptation

Gong, S. et al. **Scaling Diffusion Language Models via Adaptation from Autoregressive Models.** Preprint de 2024; ICLR 2025 informado no arXiv.

https://arxiv.org/abs/2410.17891

Relação:
- DiffuGPT;
- DiffuLLaMA;
- AR→diffusion.

Fundamento geral de adaptação, não comprovação da origem do candidato Qwen3-0.6B Diffusion BD3LM. Complementar com Block Diffusion e com a documentação do checkpoint exato, ainda pendente.

---

## Scaling masked diffusion

Nie, S. et al. **Scaling up Masked Diffusion Models on Text.** 2024.

https://arxiv.org/abs/2410.18514

Versão 3 de fevereiro de 2025; venue não confirmado. Fundamento de difusão mascarada, não evidência direta de atualização JSON.

---

## PRISM

Jayalath, D.; Wendt, J. B.; Monath, N.; Tata, S.; Gunel, B. **PRISM: Efficient Long-Range Reasoning With Short-Context LLMs.** EMNLP, 2025, p. 10196–10218. DOI: 10.18653/v1/2025.emnlp-main.517.

https://aclanthology.org/2025.emnlp-main.517/

https://arxiv.org/abs/2412.18914

Relação:
- structured in-context memory;
- typed hierarchy schema;
- incremental processing.

Atualiza memória tipada com operações de caminho/valor validadas e aplicadas programaticamente, não por reescrita integral GU. É fundamento mais próximo de memória persistente que Zeng, mas não comparação controlada que prove superioridade sobre GU-json. O preprint inicial tinha título diferente e data de 2024.

---

## JSONSchemaBench

Geng et al. **JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models.** 2025.

https://arxiv.org/abs/2501.10868

Fundamenta conformidade estrutural. JSON válido e schema válido não garantem preservação, atualização correta ou ausência de fatos inventados.

---

## Grammar-Constrained Decoding

Geng, S.; Josifoski, M.; Peyrard, M.; West, R. **Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning.** EMNLP 2023, p. 10932–10952.

https://aclanthology.org/2023.emnlp-main.674/

---

## Constrained diffusion decoding

Mündler, N.; Dekoninck, J.; Vechev, M. **Constrained Decoding of Diffusion LLMs with Context-Free Grammars.** Preprint, 2025.

https://arxiv.org/abs/2508.10111

Contraponto à ideia de impossibilidade sintática inerente à difusão. Constrained decoding pode melhorar conformidade, sem garantir correção semântica; permanece fora do experimento principal prompt-only.

---

## Agents of Diffusion

Khanal et al. **Agents of Diffusion: Enhancing Diffusion Language Models with Multi-Agent Reinforcement Learning for Structured Data Generation (Extended Version).** 2026. AAMAS 2026 e DOI 10.65109/GGJL7344 informados no arXiv.

https://arxiv.org/abs/2601.07152

Triagem de resumo/metadados. Os resultados envolvem mecanismos multiagente adicionais, não o writer isolado com prompt fixo deste TCC.

---

## Systematic mapping — Petersen 2008

Petersen, K.; Feldt, R.; Mujtaba, S.; Mattsson, M. **Systematic Mapping Studies in Software Engineering.** 2008.

https://doi.org/10.14236/ewic/ease2008.8

Uso:
- estruturação de área;
- keywording;
- classification scheme.

---

## Systematic mapping — Petersen 2015

Petersen, K.; Vakkalanka, S.; Kuzniarz, L. **Guidelines for conducting systematic mapping studies in software engineering: An update.** Information and Software Technology, 2015.

DOI:
https://doi.org/10.1016/j.infsof.2015.03.007

---

## Wohlin 2014

Wohlin, C. **Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering.** 2014.

https://doi.org/10.1145/2601248.2601268

Uso:
- backward snowballing;
- forward snowballing.

---

## Kitchenham et al. 2010

Kitchenham et al. **Systematic literature reviews in software engineering — A tertiary study.** 2010.

https://doi.org/10.1016/j.infsof.2010.03.006

Uso:
- revisão sistemática;
- evidência terciária;
- posicionamento metodológico.

Os quatro clássicos metodológicos tiveram metadados verificados; acesso integral gratuito não confirmado. Priorizar Petersen 2015 para orientação atualizada e usar Kitchenham como evidência terciária, não como manual procedural completo.

---

## Qwen3 Technical Report

Qwen Team. **Qwen3 Technical Report.** 2025.

https://arxiv.org/abs/2505.09388

Modelo: https://huggingface.co/Qwen/Qwen3-0.6B

Caracteriza o representante autoregressivo. Fixar a configuração de thinking no protocolo: raciocínio adicional não pode tornar ambíguo o orçamento de saída. Não sustenta equivalência exata de treinamento ou parâmetros entre os três representantes.

---

## Block Diffusion

Arriola, M. et al. **Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models.** 2025. ICLR 2025 Oral informado no arXiv.

https://arxiv.org/abs/2503.09573

Código: https://github.com/kuleshov-group/bd3lms

Fundamento específico de BD3LM: geração sequencial entre blocos e difusão dentro deles. Triagem de resumo/metadados; não confirma a existência, origem ou viabilidade do checkpoint Qwen3-0.6B pretendido.

---

## Diffusion em workflows de agentes

Lu, Q.; Ding, L.; Zhang, K.; Zhang, J.; Tao, D. **The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Reality Check.** 2026. Versão 3 de 24 de abril; ACL 2026 Main informado no arXiv.

https://arxiv.org/abs/2601.12979

Contraponto empírico: dificuldades em controle e chamadas de ferramentas, mas resultados competitivos em sumarização de memória textual. Modelos de 7–8B, não os representantes compactos deste TCC. As chamadas usam sintaxe semelhante a Python; a memória é texto livre, não checkpoint JSON. Não inferir inferioridade de difusão no GU-json nem garantia sintática dos autoregressivos.

---

## LongMemEval

Wu, D. et al. **LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory.** Preprint de 2024; ICLR 2025 informado no arXiv.

https://arxiv.org/abs/2410.10813

Código: https://github.com/xiaowu0162/LongMemEval

Motivação complementar para atualização de conhecimento e raciocínio temporal, junto de MemoryAgentBench. Avalia respostas, não fidelidade interna de checkpoints; não integra os datasets experimentais. Triagem de resumo/metadados.
