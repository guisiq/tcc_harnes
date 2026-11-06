# Artigos (não versionados)

Esta pasta guarda cópias locais dos PDFs da
[bibliografia atual do TCC](../TCC_Checkpoint_JSON_Obsidian/06_Referencias/referencias.md)
e arquivos de planejamentos anteriores, mantidos como histórico.

O conteúdo de `artigos/*` está no `.gitignore` — PDFs, Markdown extraídos e imagens **não**
são enviados ao repositório público (risco de direitos autorais). O Zotero continua sendo a fonte de verdade do corpus;
este README registra quais arquivos já foram
baixados aqui.

Ao baixar um artigo manualmente, salve-o nesta pasta com o nome de arquivo indicado e marque
o status abaixo.

## Bibliografia focal auditada — 2026-11-06

A bibliografia do TCC está em [referencias.md](../TCC_Checkpoint_JSON_Obsidian/06_Referencias/referencias.md), com [prioridades de leitura](../TCC_Checkpoint_JSON_Obsidian/06_Referencias/artigos_prioridade.md). As 23 referências dessa bibliografia estão disponíveis no acervo local e no Zotero. O lote de aquisição abaixo se limita a essa lista, sem ampliar a busca ao planejamento antigo ou às bibliografias internas dos PDFs.

| Fonte | Papel e atualização |
| --- | --- |
| [Hwang, Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.220/) + [SUMIE, COLING 2025](https://aclanthology.org/2025.coling-main.721/) | Método e dados, artigos distintos; estados canônicos exigem adaptação. |
| [PRISM, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.517/) | Atualizar o título antigo de 2024; promover para atualização persistente. |
| [Intrinsic Memory Agents](https://arxiv.org/abs/2508.08997) | Preprint 2025, revisão janeiro/2026; nem toda variante exige JSON. |
| [MemoryAgentBench](https://arxiv.org/abs/2507.05257) + [LongMemEval](https://arxiv.org/abs/2410.10813) | Atualização de conhecimento; apenas FactConsolidation-SH entra como contraste amostrado. |
| [Qwen3](https://arxiv.org/abs/2505.09388), [T5Gemma](https://arxiv.org/abs/2504.06225), [Block Diffusion](https://arxiv.org/abs/2503.09573) | Relatórios de 2025; checkpoint Qwen BD3LM ainda a confirmar. |
| [JSONSchemaBench](https://arxiv.org/abs/2501.10868) | Usar o título atualizado: JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models. |
| [Lu et al., 2026](https://arxiv.org/abs/2601.12979) + [Mündler et al., 2025](https://arxiv.org/abs/2508.10111) | Contrapontos sobre difusão, sem antecipar resultado no GU-json compacto. |

### Acervo local conferido — 2026-11-06

- **13 artigos ausentes** baixados de ACL Anthology/arXiv e importados em `tcc_harnes_slm > 02_dominio`, com o PDF anexado ao registro bibliográfico.
- **10 artigos existentes** reutilizados sem alterar seus itens, anexos ou coleções no Zotero. Suas versões locais foram preservadas; o link oficial pode apontar para uma revisão posterior.
- **23 pastas por artigo**, com PDF e Markdown juntos; `img/` contém as imagens raster incorporadas extraídas, quando presentes. Figuras vetoriais continuam disponíveis no PDF.
- **22 conversões novas** e a conversão anterior de Zeng preservada. PDFs conferidos, cópias local/Zotero idênticas por SHA-256 e **215 links de imagens locais** validados.

Os nomes abreviados das novas pastas evitam caminhos excessivamente longos no Windows. As cópias e os nomes anteriores permanecem intactos; os títulos completos e metadados para citação continuam na bibliografia e no Zotero.

| Referência / fonte oficial | Pasta local com PDF e Markdown | Zotero | PDF local |
| --- | --- | --- | --- |
| [Hwang 2024 — GU-json](https://aclanthology.org/2024.findings-emnlp.220/) | [pasta](03-memoria-de-agentes/Hwang%20et%20al.%20-%202024%20-%20Structured%20Incremental%20Summarization/) | [abrir](zotero://select/library/items/8ECF6DHI) | Existente preservado |
| [SUMIE — COLING 2025](https://aclanthology.org/2025.coling-main.721/) | [pasta](03-memoria-de-agentes/Hwang%20et%20al.%20-%202025%20-%20SUMIE/) | [abrir](zotero://select/library/items/6W64CHBX) | Novo; versão publicada |
| [Intrinsic Memory Agents](https://arxiv.org/abs/2508.08997) | [pasta](03-memoria-de-agentes/Yuen%20et%20al.%20-%202025%20-%20Intrinsic%20Memory%20Agents/) | [abrir](zotero://select/library/items/V4BVXK9U) | Existente preservado |
| [On the Structural Memory of LLM Agents](https://arxiv.org/abs/2412.15266) | [pasta](03-memoria-de-agentes/Zeng%20et%20al.%20-%202024%20-%20On%20the%20Structural%20Memory%20of%20LLM%20Agents/) | [abrir](zotero://select/library/items/7EPCIINZ) | Existente preservado |
| [MemoryAgentBench](https://arxiv.org/abs/2507.05257) | [pasta](03-memoria-de-agentes/Hu%20et%20al.%20-%202025%20-%20MemoryAgentBench/) | [abrir](zotero://select/library/items/FDZ4ESMG) | Existente preservado |
| [LoCoMo](https://arxiv.org/abs/2402.17753) | [pasta](03-memoria-de-agentes/Maharana%20et%20al.%20-%202024%20-%20LoCoMo/) | [abrir](zotero://select/library/items/HGGXZZ8N) | Existente preservado |
| [Chain-of-Memory](https://arxiv.org/abs/2601.14287) | [pasta](03-memoria-de-agentes/Xu%20et%20al.%20-%202026%20-%20Chain-of-Memory/) | [abrir](zotero://select/library/items/386GEDCC) | Existente preservado |
| [T5Gemma — Encoder-Decoder Gemma](https://arxiv.org/abs/2504.06225) | [pasta](02-slm-modelos-pequenos/Zhang%20et%20al.%20-%202025%20-%20T5Gemma/) | [abrir](zotero://select/library/items/4BS6W8J9) | Novo; arXiv v1 |
| [Scaling Diffusion via Adaptation](https://arxiv.org/abs/2410.17891) | [pasta](02-slm-modelos-pequenos/Gong%20et%20al.%20-%202024%20-%20Scaling%20Diffusion%20via%20Adaptation/) | [abrir](zotero://select/library/items/KK44XS3M) | Novo; arXiv v3 |
| [Scaling up Masked Diffusion Models on Text](https://arxiv.org/abs/2410.18514) | [pasta](02-slm-modelos-pequenos/Nie%20et%20al.%20-%202024%20-%20Scaling%20up%20Masked%20Diffusion%20Models%20on%20Text/) | [abrir](zotero://select/library/items/MTYA4MFG) | Novo; arXiv v3 |
| [PRISM — EMNLP 2025](https://aclanthology.org/2025.emnlp-main.517/) | [pasta](03-memoria-de-agentes/Jayalath%20et%20al.%20-%202025%20-%20PRISM/) | [abrir](zotero://select/library/items/9GCE4MWG) | Novo; versão publicada |
| [JSONSchemaBench](https://arxiv.org/abs/2501.10868) | [pasta](04-harness-e-avaliacao/Geng%20et%20al.%20-%202025%20-%20JSONSchemaBench/) | [abrir](zotero://select/library/items/JUHDARXC) | Novo; arXiv v3 |
| [Grammar-Constrained Decoding — EMNLP 2023](https://aclanthology.org/2023.emnlp-main.674/) | [pasta](04-harness-e-avaliacao/Geng%20et%20al.%20-%202023%20-%20Grammar-Constrained%20Decoding/) | [abrir](zotero://select/library/items/2K8C6DM4) | Novo; versão publicada |
| [Constrained Decoding of Diffusion LLMs](https://arxiv.org/abs/2508.10111) | [pasta](04-harness-e-avaliacao/Mundler%20et%20al.%20-%202025%20-%20Constrained%20Decoding%20of%20Diffusion%20LLMs/) | [abrir](zotero://select/library/items/6VUW8TAN) | Novo; arXiv v1 |
| [Agents of Diffusion](https://arxiv.org/abs/2601.07152) | [pasta](04-harness-e-avaliacao/Khanal%20et%20al.%20-%202026%20-%20Agents%20of%20Diffusion/) | [abrir](zotero://select/library/items/6ZZFUKDP) | Novo; arXiv v1 |
| [Petersen 2008 — Systematic Mapping Studies](https://doi.org/10.14236/ewic/ease2008.8) | [pasta](01-metodologia-revisao/Petersen%20et%20al.%20-%202008%20-%20Systematic%20Mapping%20Studies/) | [abrir](zotero://select/library/items/LTF95YLK) | Existente preservado |
| [Petersen 2015 — Mapping Guidelines](https://doi.org/10.1016/j.infsof.2015.03.007) | [pasta](01-metodologia-revisao/Petersen%20et%20al.%20-%202015%20-%20Systematic%20Mapping%20Guidelines/) | [abrir](zotero://select/library/items/AZQIGMHU) | Existente preservado |
| [Wohlin 2014 — Snowballing](https://doi.org/10.1145/2601248.2601268) | [pasta](01-metodologia-revisao/Wohlin%20-%202014%20-%20Guidelines%20for%20Snowballing/) | [abrir](zotero://select/library/items/9KRGQ4FM) | Existente preservado |
| [Kitchenham 2010 — Tertiary Study](https://doi.org/10.1016/j.infsof.2010.03.006) | [pasta](01-metodologia-revisao/Kitchenham%20et%20al.%20-%202010%20-%20Systematic%20Literature%20Reviews/) | [abrir](zotero://select/library/items/53RY4CDP) | Existente preservado |
| [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) | [pasta](02-slm-modelos-pequenos/Yang%20et%20al.%20-%202025%20-%20Qwen3%20Technical%20Report/) | [abrir](zotero://select/library/items/LNITDSY9) | Novo; arXiv v1 |
| [Block Diffusion](https://arxiv.org/abs/2503.09573) | [pasta](02-slm-modelos-pequenos/Arriola%20et%20al.%20-%202025%20-%20Block%20Diffusion/) | [abrir](zotero://select/library/items/NH96Q3CG) | Novo; arXiv v3 |
| [The Bitter Lesson of Diffusion for Agentic Workflows](https://arxiv.org/abs/2601.12979) | [pasta](04-harness-e-avaliacao/Lu%20et%20al.%20-%202026%20-%20Bitter%20Lesson%20of%20Diffusion%20for%20Agentic%20Workflows/) | [abrir](zotero://select/library/items/9PD3J7EZ) | Novo; arXiv v3 |
| [LongMemEval](https://arxiv.org/abs/2410.10813) | [pasta](03-memoria-de-agentes/Wu%20et%20al.%20-%202024%20-%20LongMemEval/) | [abrir](zotero://select/library/items/NJTS6Q8P) | Novo; arXiv v2 |

O bloco sincronizado ao final deste README lista as cópias planas da raiz; o catálogo acima aponta para as pastas organizadas. Usar ano/versão/publicação da bibliografia na citação acadêmica. Metadados e pendências de surveys e demais itens do planejamento antigo, fora do escopo deste lote, não foram revalidados.

## Referências — Domínio

| Chave (Zotero) | Autor(es) / Ano | Título | Fonte | Arquivo esperado | Status |
|---|---|---|---|---|---|
| belcak2025 | Belcak et al., 2025 | Small Language Models are the Future of Agentic AI | arXiv:2506.02153 | `Belcak_2025_Small_Language_Models_are_the_Future_of_Agentic_AI.pdf` | ✅ baixado |
| lu2025 | Lu et al., 2025 | Small Language Models: Survey, Measurements, and Insights | arXiv:2409.15790 | `Lu_2025_Small_Language_Models_Survey_Measurements_Insights.pdf` | ✅ baixado |
| sharma2025 | Sharma & Mehta, 2025 | Small Language Models for Agentic Systems: A Survey | arXiv:2510.03847 | `Sharma_Mehta_2025_Small_Language_Models_for_Agentic_Systems.pdf` | ✅ baixado |
| nguyen2025 | Nguyen et al., 2025 | A Survey on Small Language Models (RANLP 2025) | sem arXiv ID confirmado no documento | `nguyen2025_survey_slm.pdf` | ⬜ pendente |
| gao2021harness | Gao et al., 2021 | A framework for few-shot language model evaluation (lm-evaluation-harness — origem do termo) | Zenodo, doi:10.5281/zenodo.5371629 | `gao2021_lm_evaluation_harness.pdf` | ⬜ pendente |
| ge2026harness | Ge et al., 2026 | Stop Comparing LLM Agents Without Disclosing the Harness | arXiv:2605.23950 | `ge2026_stop_comparing_harness.pdf` | ⬜ pendente |
| ning2026codeharness | Ning et al., 2026 | Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems | arXiv:2605.18747 | `ning2026_code_as_agent_harness.pdf` | ⬜ pendente |
| meng2026harness | Meng et al., 2026 | Agent Harness for Large Language Model Agents: A Survey | Preprints, doi:10.20944/preprints202604.0428.v3 | `meng2026_agent_harness_survey.pdf` | ⬜ pendente |
| li2026engineering | Li et al., 2026 | Agent Harness Engineering: A Survey | preprint sob revisão, sem arXiv ID confirmado | `li2026_agent_harness_engineering_survey.pdf` | ⬜ pendente |
| moghadasi2026disclose | Moghadasi & Ghaderi, 2026 | What Twelve LLM Agent Benchmark Papers Disclose About Themselves: A Pilot Audit and an Open Scoring Schema | arXiv:2605.21404 | `moghadasi2026_disclose_audit.pdf` | ⬜ pendente |
| lee2026metaharness | Lee et al., 2026 | Meta-Harness: End-to-End Optimization of Model Harnesses | arXiv:2603.28052 | `lee2026_meta_harness.pdf` | ⬜ pendente |

## Referências — Metodológicas

| Chave (Zotero) | Autor(es) / Ano | Título | Fonte | Arquivo esperado | Status |
|---|---|---|---|---|---|
| petersen2008 | Petersen et al., 2008 | Systematic Mapping Studies in Software Engineering | [DOI verificado](https://doi.org/10.14236/ewic/ease2008.8) | [PDF](01-metodologia-revisao/Petersen%20et%20al.%20-%202008%20-%20Systematic%20Mapping%20Studies/Petersen%20et%20al.%20-%202008%20-%20Systematic%20Mapping%20Studies.pdf) | ✅ PDF local e anexo Zotero verificados |
| petersen2015 | Petersen et al., 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | [DOI verificado](https://doi.org/10.1016/j.infsof.2015.03.007) | [PDF](01-metodologia-revisao/Petersen%20et%20al.%20-%202015%20-%20Systematic%20Mapping%20Guidelines/Petersen%20et%20al.%20-%202015%20-%20Systematic%20Mapping%20Guidelines.pdf) | ✅ PDF local e anexo Zotero verificados |
| kitchenham2007 | Kitchenham & Charters, 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | EBSE-2007-01 (technical report) | `kitchenham2007_slr_guidelines.pdf` | ⬜ pendente |
| wohlin2014 | Wohlin, 2014 | Guidelines for snowballing in systematic literature studies and a replication in software engineering | [DOI verificado](https://doi.org/10.1145/2601248.2601268) | [PDF](01-metodologia-revisao/Wohlin%20-%202014%20-%20Guidelines%20for%20Snowballing/Wohlin%20-%202014%20-%20Guidelines%20for%20Snowballing.pdf) | ✅ PDF local e anexo Zotero verificados |

Priorizar Petersen 2015 junto da origem de 2008. [Kitchenham et al., 2010](https://doi.org/10.1016/j.infsof.2010.03.006), disponível no catálogo focal acima, complementa com evidência terciária, sem substituir as diretrizes de 2007. Kitchenham 2007 e os demais itens históricos fora da bibliografia atual não foram adquiridos neste lote.

## Como manter rastreável

1. Confira DOI, identificador arXiv e título no Zotero antes de criar um registro, evitando duplicatas.
2. Obtenha o PDF de uma fonte oficial ou por acesso autorizado; importe os metadados e anexe o PDF ao item correspondente no Zotero.
3. Preserve os arquivos existentes. Crie a conversão Markdown em uma nova subpasta por artigo, dentro da categoria pertinente, e depois reúna nela o PDF e as imagens extraídas.
4. Não execute novamente um conversor sobre uma pasta que contenha notas ou arquivos a preservar; use uma pasta distinta para outra versão.
5. Atualize o catálogo com a fonte oficial, a pasta local, a versão efetivamente salva e o link do item no Zotero.
6. Confira a abertura do PDF, o conteúdo do Markdown, os links das imagens e a igualdade entre o PDF local e o anexo do Zotero.

Para repetir a sincronização automaticamente no Windows, execute na raiz do
projeto:

```powershell
.\sincronizar-zotero.ps1
```

O script copia PDFs do armazenamento local do Zotero para a raiz de `artigos`,
não sobrescreve arquivos existentes e atualiza automaticamente a lista de links abaixo.
Ele não baixa referências novas, não importa itens no Zotero, não converte PDFs e não
atualiza o catálogo focal das subpastas; essas etapas são separadas.

<!-- ZOTERO-PDFS-START -->
## PDFs sincronizados do Zotero

Links por contexto:

### Metodologia e revisão sistemática

- [2026 - (PDF) Systematic Mapping Studies in Software Engineering.pdf](2026%20-%20%28PDF%29%20Systematic%20Mapping%20Studies%20in%20Software%20Engineering.pdf)
- [Kitchenham et al. - 2010 - Systematic literature reviews in software engineering – A tertiary study.pdf](Kitchenham%20et%20al.%20-%202010%20-%20Systematic%20literature%20reviews%20in%20software%20engineering%20%E2%80%93%20A%20tertiary%20study.pdf)
- [Petersen et al. - 2008 - Systematic Mapping Studies in Software Engineering.pdf](Petersen%20et%20al.%20-%202008%20-%20Systematic%20Mapping%20Studies%20in%20Software%20Engineering.pdf)
- [Petersen et al. - 2015 - Guidelines for conducting systematic mapping studies in software engineering An update_UZ7GJIZL.pdf](Petersen%20et%20al.%20-%202015%20-%20Guidelines%20for%20conducting%20systematic%20mapping%20studies%20in%20software%20engineering%20An%20update_UZ7GJIZL.pdf)
- [Petersen et al. - 2015 - Guidelines for conducting systematic mapping studies in software engineering An update.pdf](Petersen%20et%20al.%20-%202015%20-%20Guidelines%20for%20conducting%20systematic%20mapping%20studies%20in%20software%20engineering%20An%20update.pdf)
- [van Eck e Waltman - 2010 - Software survey VOSviewer, a computer program for bibliometric mapping.pdf](van%20Eck%20e%20Waltman%20-%202010%20-%20Software%20survey%20VOSviewer%2C%20a%20computer%20program%20for%20bibliometric%20mapping.pdf)
- [Wohlin - 2014 - Guidelines for snowballing in systematic literature studies and a replication in software engineerin.pdf](Wohlin%20-%202014%20-%20Guidelines%20for%20snowballing%20in%20systematic%20literature%20studies%20and%20a%20replication%20in%20software%20engineerin.pdf)

### SLM e modelos pequenos

- [Abdin et al. - 2024 - Phi-3 Technical Report A Highly Capable Language Model Locally on Your Phone.pdf](Abdin%20et%20al.%20-%202024%20-%20Phi-3%20Technical%20Report%20A%20Highly%20Capable%20Language%20Model%20Locally%20on%20Your%20Phone.pdf)
- [Botev et al. - 2024 - RecurrentGemma Moving Past Transformers for Efficient Open Language Models.pdf](Botev%20et%20al.%20-%202024%20-%20RecurrentGemma%20Moving%20Past%20Transformers%20for%20Efficient%20Open%20Language%20Models.pdf)
- [Galim et al. - 2024 - Parameter-Efficient Fine-Tuning of State Space Models.pdf](Galim%20et%20al.%20-%202024%20-%20Parameter-Efficient%20Fine-Tuning%20of%20State%20Space%20Models.pdf)
- [Lee et al. - 2025 - Exploring the Trade-Offs Quantization Methods, Task Difficulty, and Model Size in Large Language Mo.pdf](Lee%20et%20al.%20-%202025%20-%20Exploring%20the%20Trade-Offs%20Quantization%20Methods%2C%20Task%20Difficulty%2C%20and%20Model%20Size%20in%20Large%20Language%20Mo.pdf)
- [Lu et al. - 2025 - Small Language Models Survey, Measurements, and Insights.pdf](Lu%20et%20al.%20-%202025%20-%20Small%20Language%20Models%20Survey%2C%20Measurements%2C%20and%20Insights.pdf)
- [Nguyen et al. - 2026 - Parameter-efficient fine-tuning of small language models for code generation a comparative study of.pdf](Nguyen%20et%20al.%20-%202026%20-%20Parameter-efficient%20fine-tuning%20of%20small%20language%20models%20for%20code%20generation%20a%20comparative%20study%20of.pdf)
- [Yuan et al. - 2025 - EfficientLLM Efficiency in Large Language Models.pdf](Yuan%20et%20al.%20-%202025%20-%20EfficientLLM%20Efficiency%20in%20Large%20Language%20Models.pdf)

### Memória de agentes

- [Hu et al. - 2025 - Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions.pdf](Hu%20et%20al.%20-%202025%20-%20Evaluating%20Memory%20in%20LLM%20Agents%20via%20Incremental%20Multi-Turn%20Interactions.pdf)
- [Hwang et al. - 2024 - Enhancing Incremental Summarization with Structured Representations.pdf](Hwang%20et%20al.%20-%202024%20-%20Enhancing%20Incremental%20Summarization%20with%20Structured%20Representations.pdf)
- [Maharana et al. - 2024 - Evaluating Very Long-Term Conversational Memory of LLM Agents.pdf](Maharana%20et%20al.%20-%202024%20-%20Evaluating%20Very%20Long-Term%20Conversational%20Memory%20of%20LLM%20Agents.pdf)
- [Muhoberac et al. - 2025 - State and Memory is All You Need for Robust and Reliable AI Agents.pdf](Muhoberac%20et%20al.%20-%202025%20-%20State%20and%20Memory%20is%20All%20You%20Need%20for%20Robust%20and%20Reliable%20AI%20Agents.pdf)
- [Xu et al. - 2026 - Chain-of-Memory Lightweight Memory Construction with Dynamic Evolution for LLM Agents.pdf](Xu%20et%20al.%20-%202026%20-%20Chain-of-Memory%20Lightweight%20Memory%20Construction%20with%20Dynamic%20Evolution%20for%20LLM%20Agents.pdf)
- [Yuen et al. - 2025 - Intrinsic Memory Agents Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory.pdf](Yuen%20et%20al.%20-%202025%20-%20Intrinsic%20Memory%20Agents%20Heterogeneous%20Multi-Agent%20LLM%20Systems%20through%20Structured%20Contextual%20Memory.pdf)
- [Zeng et al. - 2024 - On the Structural Memory of LLM Agents.pdf](Zeng%20et%20al.%20-%202024%20-%20On%20the%20Structural%20Memory%20of%20LLM%20Agents.pdf)

### Harness e avaliação de agentes

- [2026 - Agent Harness Engineering A Survey.pdf](2026%20-%20Agent%20Harness%20Engineering%20A%20Survey.pdf)
- [Sharma e Mehta - 2025 - Small Language Models for Agentic Systems A Survey of Architectures, Capabilities, and Deployment T.pdf](Sharma%20e%20Mehta%20-%202025%20-%20Small%20Language%20Models%20for%20Agentic%20Systems%20A%20Survey%20of%20Architectures%2C%20Capabilities%2C%20and%20Deployment%20T.pdf)

<!-- ZOTERO-PDFS-END -->
