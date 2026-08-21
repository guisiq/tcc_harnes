# Ordem de leitura para a reunião com o orientador

Todas as 14 referências de `citacoes_academicas/` já estão na coleção **tcc_harnes_slm** do Zotero (adicionadas via API local em 2026-08-21). Abaixo, a ordem de leitura organizada em **4 blocos de 3-4 artigos**, do mais crítico para o menos crítico. Cada bloco fecha um arco de compreensão sozinho — se o tempo acabar, pare ao final de um bloco completo, nunca no meio.

> Critério de priorização: o que o orientador mais provavelmente vai questionar é a **originalidade do recorte** (H1/H2/H3 — JSON vs. sumarização) e a **motivação do problema**. Isso vem primeiro. Modelos candidatos ao piloto vêm por último, pois são detalhe de implementação, não de fundamentação teórica.

---

## Bloco 1 — Núcleo da hipótese: estrutura da memória importa (LER PRIMEIRO, MESMO SE SÓ DER TEMPO PARA ISSO)
**Ao final:** você consegue defender por que faz sentido comparar checkpoint JSON com resumo textual, e por que essa comparação ainda é uma lacuna aberta.

- [ ] **Zeng et al. (2024)** — *On the Structural Memory of LLM Agents* — [[03-benchmarks-de-memoria-e-long-horizon]] / [[02-estruturas-de-memoria-sumarizacao-e-json]]
  Por quê primeiro: é a evidência mais direta de que **a estrutura da memória afeta desempenho** — a premissa que sustenta toda a pergunta de pesquisa.
- [ ] **Hwang et al. (2024)** — *Enhancing Incremental Summarization with Structured Representations*
  Por quê: é o estudo **mais próximo** de "JSON vs. texto livre" que existe na literatura levantada — mas não é sobre agentes interrompidos, então prepare a explicação de por que seu recorte ainda é original.
- [ ] **Yuen et al. (2025)** — *Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory*
  Por quê: reforça a plausibilidade de memória estruturada por agente, complementando Zeng e Hwang.
- [ ] **Muhoberac et al. (2025)** — *State and Memory is All You Need for Robust and Reliable AI Agents*
  Por quê: fecha o bloco com a motivação maior — por que agentes precisam de estado/memória persistente para confiabilidade em tarefas de múltiplas etapas.

---

## Bloco 2 — Como a literatura avalia memória (justifica sua metodologia)
**Ao final:** você consegue explicar por que optou por tarefas sintéticas/determinísticas em vez de replicar benchmarks conversacionais, e quais métricas (tokens, latência) são padrão na área.

- [ ] **Hu, Wang & McAuley (2025)** — *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions* (MemoryAgentBench)
  Por quê: mostra que memória é **subavaliada** como competência própria — justifica a necessidade do seu experimento.
- [ ] **Maharana et al. (2024)** — *Evaluating Very Long-Term Conversational Memory of LLM Agents* (LoCoMo)
  Por quê: principal benchmark conversacional citado — útil para contrastar com seu recorte determinístico (diferente de memória conversacional).
- [ ] **Xu et al. (2026)** — *Chain-of-Memory: Lightweight Memory Construction with Dynamic Evolution for LLM Agents*
  Por quê: mostra por que **tokens e latência** são métricas relevantes de custo/eficiência de memória, reforçando suas variáveis dependentes.

---

## Bloco 3 — Viabilidade técnica: SLMs locais e quantização
**Ao final:** você consegue justificar a escolha de SLMs de 1-4B, quantizados, rodando localmente, e as métricas de eficiência (latência, memória, VRAM).

- [ ] **Lu et al. (2024)** — *Small Language Models: Survey, Measurements, and Insights*
  Por quê: panorama geral de SLMs e a origem das métricas de latência/footprint de memória que você usa. *(já estava no Zotero antes desta importação, em `03_base`.)*
- [ ] **Lee et al. (2025)** — *Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size...*
  Por quê: mostra que **modelos pequenos sofrem mais com quantização agressiva** — relevante para justificar riscos do seu piloto.
- [ ] **Yuan et al. (2025)** — *EfficientLLM: Efficiency in Large Language Models*
  Por quê: fornece o vocabulário/framework de métricas de eficiência (memória, latência, energia) que você pode citar diretamente.

---

## Bloco 4 — Modelos candidatos ao piloto (detalhe de implementação, menor prioridade)
**Ao final:** você tem a referência acadêmica de cada modelo específico cogitado para o piloto. Menos crítico para a discussão teórica com o orientador; leia só se sobrar tempo.

- [ ] **Nguyen, Nguyen & Vu (2026)** — *Parameter-efficient fine-tuning of small language models for code generation: Gemma, Qwen 2.5, Llama 3.2*
- [ ] **Abdin et al. (2024)** — *Phi-3 Technical Report*
- [ ] **Botev et al. (2024)** — *RecurrentGemma*
- [ ] **Galim et al. (2024)** — *Parameter-Efficient Fine-Tuning of State Space Models* (Mamba)

---

## Observações sobre a importação no Zotero

- Coleção usada: **tcc_harnes_slm** (nível raiz do projeto), via API local (`http://127.0.0.1:23119`).
- A API local do Zotero só permite criar itens através do endpoint do conector (`/connector/saveItems`); não há suporte a `PATCH`/`DELETE` por essa via, então não foi possível mover os itens automaticamente para uma subcoleção nem apagar itens de teste por API.
- **Ação manual necessária:** ao explorar o endpoint para descobrir o formato correto, dois itens de teste foram criados na coleção `tcc_harnes_slm` e precisam ser apagados manualmente no Zotero:
  - "Test Zotero Connector Save"
  - "Test Zotero Connector Save 2"
- O item de Lu et al. (2024) já existia na sua biblioteca (subcoleção `03_base`) e não foi duplicado.
