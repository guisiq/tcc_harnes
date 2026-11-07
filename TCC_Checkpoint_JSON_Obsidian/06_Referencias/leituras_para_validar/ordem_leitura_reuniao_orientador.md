# Ordem de leitura para a reunião com o orientador

O registro anterior informa a importação de 14 referências na coleção **tcc_harnes_slm** do Zotero em 2026-08-21. Esta revisão de 2026-11-06 atualiza somente os Markdown; não afirma que as fontes acrescentadas já estejam no Zotero.

> Critério: proximidade da evidência ao recorte atual, comparação de writers compactos sob GU-json, schema e 1.200 tokens fixos. JSON versus texto, retomada de tarefas e desempenho computacional não integram o experimento. [Prioridades completas](../artigos_prioridade.md).

---

## Bloco 1 — Método e dados

- [ ] [Hwang, Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.220/) — GU-json como protocolo publicado; CoK impede alegar superioridade universal de GU.
- [ ] [SUMIE, COLING 2025](https://aclanthology.org/2025.coling-main.721/) — preservação de perspectivas, anotações por parágrafo e avaliação semântica original.
- [ ] [MemoryAgentBench, 2025/2026](https://arxiv.org/abs/2507.05257) — regra temporal de FactConsolidation e limites da avaliação por respostas.

---

## Bloco 2 — Memória persistente e contrapontos

- [ ] [PRISM, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.517/) — atualização tipada programática, mais próxima do argumento que recuperação em Zeng.
- [ ] [Intrinsic Memory Agents, revisão 2026](https://arxiv.org/abs/2508.08997) — atualização contextual; nem todas as variantes exigem JSON ou favorecem template manual.
- [ ] [LongMemEval, 2025](https://arxiv.org/abs/2410.10813) — atualização de conhecimento, apenas fundamentação complementar.

---

## Bloco 3 — Representantes e limites da inferência

- [ ] [Qwen3 Technical Report, 2025](https://arxiv.org/abs/2505.09388) — modelo autoregressivo e configuração de thinking.
- [ ] [T5Gemma, 2025](https://arxiv.org/abs/2504.06225) — caracterização encoder-decoder; verificar termos de acesso.
- [ ] [Block Diffusion, 2025](https://arxiv.org/abs/2503.09573) — fundamento de BD3LM; checkpoint Qwen exato ainda precisa ser confirmado.

---

## Bloco 4 — Estrutura e avaliação crítica

- [ ] [JSONSchemaBench, 2025](https://arxiv.org/abs/2501.10868) — validade estrutural não garante estado correto.
- [ ] [Lu et al., 2026](https://arxiv.org/abs/2601.12979) — dificuldades em ferramentas e memória textual competitiva, não teste de GU-json compacto.
- [ ] [Mündler et al., 2025](https://arxiv.org/abs/2508.10111) — restrições podem mitigar sintaxe; mecanismo fora do experimento principal.

Zeng, LoCoMo, Chain-of-Memory e as fontes anteriores sobre SLMs permanecem acervo complementar. A ordem não marca leituras como concluídas nem acrescenta modelos/datasets ao experimento. [Referências e situação editorial](../referencias.md).

---

## Observações sobre a importação no Zotero

- Coleção usada: **tcc_harnes_slm** (nível raiz do projeto), via API local (`http://127.0.0.1:23119`).
- A API local do Zotero só permite criar itens através do endpoint do conector (`/connector/saveItems`); não há suporte a `PATCH`/`DELETE` por essa via, então não foi possível mover os itens automaticamente para uma subcoleção nem apagar itens de teste por API.
- **Ação manual necessária:** ao explorar o endpoint para descobrir o formato correto, dois itens de teste foram criados na coleção `tcc_harnes_slm` e precisam ser apagados manualmente no Zotero:
  - "Test Zotero Connector Save"
  - "Test Zotero Connector Save 2"
- O item de Lu et al. (2024) já existia na sua biblioteca (subcoleção `03_base`) e não foi duplicado.
