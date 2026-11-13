# Mapeamento focado de trabalhos relacionados

**Janela:** 01/07/2025 a 12/11/2026; data do primeiro depósito no arXiv.  
**Coleta:** 2026-11-12T20:27:34.9144207+00:00; fonte: arXiv API. Este documento não altera o artigo do TCC.

## Metodologia

O procedimento é um mapeamento sistematizado e limitado, inspirado no planejamento, busca, triagem e extração de [Petersen et al. (2015)](https://doi.org/10.1016/j.infsof.2015.03.007). A calibração exploratória com trabalhos conhecidos foi inspirada no uso de estudos de referência por [Zhang et al. (2011)](https://doi.org/10.1016/j.infsof.2010.12.010), sem representar uma validação independente nem uma estimativa geral de cobertura.
A exposição de objetivo, procedimentos e limitações também segue a orientação geral de organização do trabalho científico de [Prodanov e Freitas (2013)](<../../artigos/05-metodologia-e-escrita-cientifica/Prodanov_Freitas_2013_Metodologia_do_Trabalho_Cientifico/Prodanov_Freitas_2013_Metodologia_do_Trabalho_Cientifico.md>), presente no material metodológico indicado.
A questão é identificar quais estudos aproximam escrita incremental de memória estruturada, modelos compactos, avaliação do estado e paradigmas gerativos. As consultas combinam essas facetas nos campos título e resumo. O recorte cobre preprints no arXiv, não toda a literatura; trabalhos fora dessa fonte ou com primeiro depósito anterior à janela podem ficar ausentes.
OpenAlex e Semantic Scholar responderam HTTP 429 às tentativas da busca focada e não integram esta coleta. Seus resultados antigos não foram apresentados como novas buscas.

| Consulta | Faceta | Total informado | Registros coletados |
|---|---|---:|---:|
| F1 | Memória estruturada ou entidades com atualização incremental | 52 | 52 |
| F2 | Modelos compactos que escrevem ou gerem memória | 71 | 71 |
| F3 | Difusão em memória de agentes ou estado de planejamento editável | 2 | 2 |
| F4 | JSON estruturado relacionado a memória, estado ou entidades em modelos compactos ou de difusão | 10 | 10 |
| F5 | Referências explícitas ao método GU-JSON ou ao benchmark SUMIE | 7 | 7 |
| F6 | Estado ou memória estruturados com atualização ou rastreamento por modelos pequenos | 26 | 26 |

As expressões completas e a janela `submittedDate` estão no [protocolo focado](mapeamento_sistematico/protocolo/protocolo_focado_estrito.json). Todos os resultados de cada consulta foram paginados; os totais por consulta se sobrepõem.

Após deduplicação por identificador arXiv: **158 candidatos** na janela; 0 registros fora dela pela data do primeiro depósito. A triagem por IA do título e resumo classificou **13 CORE**, 91 CONTEXT e 54 EXCLUDE.
CORE exige estudo primário, atualização incremental de memória textual estruturada e, além disso, ao menos uma dimensão: escritor ou gestor compacto de até aproximadamente 4B parâmetros; avaliação direta da fidelidade ou correção do estado; ou comparação pertinente de paradigmas gerativos. CONTEXT indica proximidade parcial ou evidência insuficiente; EXCLUDE abrange estudos secundários, memória de hardware, modalidade não textual principal e outros temas sem contribuição pertinente.
A revisão final registrou decisões para todos os 13 CORE e para 6 outros candidatos selecionados por proximidade: manteve 5 CORE e excluiu 8. A classificação e a revisão foram assistidas por IA, sem avaliação humana independente.
Como exceção explícita, a revisão pode incluir comparadores CONTEXT que avaliem paradigmas gerativos em memória de agentes ou estado de planejamento revisável, mesmo sem cumprir o núcleo; também pode corrigir uma decisão inicial mediante justificativa individual. Não se trata de alegar que todos os CONTEXT foram reavaliados integralmente.

Para diagnosticar perdas, as consultas recuperaram **4/6** controles previamente conhecidos; esses controles não foram acrescentados artificialmente aos resultados. São uma amostra dirigida, não uma medida de cobertura geral.
- Intrinsic Memory Agents ([arXiv:2508.08997](https://arxiv.org/abs/2508.08997)): não recuperado.
- The Bitter Lesson of Diffusion Language Models for Agentic Workflows ([arXiv:2601.12979](https://arxiv.org/abs/2601.12979)): recuperado.
- AMU ([arXiv:2609.36976](https://arxiv.org/abs/2609.36976)): recuperado.
- MemReader ([arXiv:2604.07877](https://arxiv.org/abs/2604.07877)): recuperado.
- Supersede ([arXiv:2606.27472](https://arxiv.org/abs/2606.27472)): não recuperado.
- DiffuPlan ([arXiv:2610.24717](https://arxiv.org/abs/2610.24717)): recuperado.

O quadro inclui **10 estudos da busca focada**: 8 no núcleo após a revisão e 2 comparadores. Na triagem inicial, eram 5 CORE, 5 CONTEXT e 0 EXCLUDE. Acrescenta dois fundamentos anteriores ao recorte e a linha da proposta. Não há corte arbitrário por ranking.

## Quadro comparativo

| Trabalho | Representação da memória | Atualização | Modelos e escala | Objeto da avaliação | Compara paradigmas gerativos |
|---|---|---|---|---|---|
| [Hwang et al. (2024), fundamento](https://doi.org/10.18653/v1/2024.findings-emnlp.220) | Texto e JSON | GU-JSON e alternativas; reescrita do estado | Gemini Ultra e Pro | Fidelidade de resumos incrementais | Não identificado como comparação de paradigmas |
| [SUMIE (2025), fundamento](https://aclanthology.org/2025.coling-main.721/) | Entidades, atributos e valores | Integra informações e preserva perspectivas | Modelos de linguagem de grande porte | Precisão, revocação e F1 do resumo | Não identificado como comparação de paradigmas |
| [MemLoRA: Distilling Expert Adapters for On-Device Memory Systems](https://arxiv.org/abs/2512.04763v1) (2025; núcleo; IA: CONTEXT; [T](https://arxiv.org/html/2512.04763v1)) | Fatos textuais; operações em JSON com id, texto e evento, não reescrita integral GU-JSON | Adaptadores especializados decidem adição, atualização e exclusão de entradas Mem0 | Qwen2.5-1.5B e Gemma2-2B, com adaptadores LoRA destilados | QA conversacional no LoCoMo, latência e eficiência; extensão visual separada | Não identificado |
| [The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Reality Check](https://arxiv.org/abs/2601.12979v3) (2026; comparador; IA: CONTEXT; [T](https://arxiv.org/html/2601.12979v3)) | Resumos textuais de memória; chamadas de ferramentas em JSON são outra tarefa | Sumarização do histórico do agente, sem checkpoint GU-JSON | LLaDA-8B e Dream-7B versus Qwen-8B e Ministral-8B, entre outros | Desempenho de agentes e chamadas de ferramentas; sumarização e formato JSON em experimentos distintos | Sim, difusão versus autoregressão em tarefas agênticas |
| [AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment](https://arxiv.org/abs/2603.26680v2) (2026; núcleo; IA: CORE; [T](https://arxiv.org/html/2603.26680v2)) | Registros de preferências com identificador, tipo, categoria, valor e confiança | Retenção, adição e modificação a partir de novos diálogos | LLMs e sistemas de memória, incluindo DeepSeek-v3.2 e Qwen3-max; não foca escritores de até 4B | F1 por correspondência semântica entre memória atualizada e referência humana; também recuperação e uso | Não identificado |
| [MemReader: From Passive to Active Extraction for Long-Term Agent Memory](https://arxiv.org/abs/2604.07877v2) (2026; núcleo; IA: CORE; [T](https://arxiv.org/html/2604.07877v2)) | Entradas estruturadas de memória extraídas de conversas | Extração passiva ou escrita seletiva com recuperação, adiamento e descarte | MemReader-0.6B para extração passiva; MemReader-4B para gestão ativa | QA e gestão de memória em LoCoMo, LongMemEval e HaluMem; atualização de conhecimento e alucinação | Não identificado |
| [DimMem: Dimensional Structuring for Efficient Long-Term Agent Memory](https://arxiv.org/abs/2605.15759v3) (2026; núcleo; IA: CORE; [T](https://arxiv.org/html/2605.15759v3)) | Registros atômicos tipados com tempo, local, motivo, finalidade e palavras-chave | Identificação e atualização de memórias por dimensões e ordem temporal | Extrator Qwen3-4B ajustado ao esquema; outros extratores de maior porte | Acurácia de QA em LoCoMo e LongMemEval e eficiência de recuperação/atualização | Não identificado |
| [CMI-Mem: Toward Generalizable Long-Term Memory Management via CMI-Augmented Reinforcement Learning](https://arxiv.org/abs/2607.20553v2) (2026; núcleo; IA: CONTEXT; [T](https://arxiv.org/html/2607.20553v2)) | Estado dividido em memória central, episódica, semântica e procedural | Agentes por tipo aplicam operações como adicionar, substituir, fundir e atualizar | Gestor CMI-Mem-4B baseado em Qwen3-4B; também versão 8B | QA e generalização; recompensa de informação por operação, não uma medida direta de fidelidade do estado | Não identificado |
| [PGMem: Tightly Coupled Persona-Memory Graph for Lifelong Personalized Agents](https://arxiv.org/abs/2608.01708v2) (2026; núcleo; IA: CONTEXT; [T](https://arxiv.org/html/2608.01708v2)) | Grafo de eventos e persona com nós e arestas de evidência tipados | Acrescenta nós e liga evidências de apoio, contradição e mudança entre turnos | Qwen3-1.7B e Gemma-3-1B nos experimentos | QA e validação humana de 25 arestas por tipo; acerto de 36% em contradição e 52% em mudança | Não identificado |
| [Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents](https://arxiv.org/abs/2609.01272v1) (2026; núcleo; IA: CORE; [T](https://arxiv.org/pdf/2609.01272v1)) | Registro tipado de intenções prospectivas | Código controla ciclo de vida, reagendamento e cancelamento; o modelo participa da seleção | Gemma-E2B e Qwen3.5-4B, além de DeepSeek-Chat e Qwen3-8B | Set-F1 de intenções devidas e erros de atualização no PM-Bench, não fidelidade do registro completo | Não identificado |
| [AMU:Admission and Memory Update for Personalized Conversations---Structured Memory with SLM Guided Control](https://arxiv.org/abs/2609.36976v2) (2026; núcleo; IA: CORE; [T](https://arxiv.org/html/2609.36976v2)) | Registros estruturados de memória pessoal | Filtragem de admissão; mantém, descarta duplicatas ou funde atualizações | Qwen3.5-2B para gestão; Qwen3-Embedding-0.6B para recuperação | Correção das ações de escrita, redundância e recuperação; avaliação adicional de respostas | Não identificado |
| [DiffuPlan: Editable Planning State for Diffusion Language Model Agents](https://arxiv.org/abs/2610.24717v1) (2026; comparador; IA: CONTEXT; [T](https://arxiv.org/html/2610.24717v1)) | Plano intermediário textual editável | Reconstrói passos afetados quando chegam novas evidências | LLaDA2.0-mini e seu modelo de origem autoregressivo Ling-mini-2.0 | F1 de respostas em busca multi-hop e custo de geração, não fidelidade de checkpoint | Sim, estado editável versus append-only em difusão e autoregressão |
| **Proposta do TCC** | Checkpoint JSON de esquema fixo | Reescrita integral GU-JSON | Representantes compactos autoregressivo, encoder-decoder e difusão em blocos | Validade e fidelidade por transição, turno e operação no SUMIE | Sim, sob o mesmo protocolo |

A categoria final distingue núcleo e comparador; CORE/CONTEXT/EXCLUDE são os rótulos da triagem inicial por IA, não uma avaliação independente. R indica título e resumo; T aponta para a versão do texto integral da qual também foram conferidos trechos, não necessariamente o artigo completo. Confirme método, modelos e resultados no texto integral antes de citar.

## Síntese

- MemReader, DimMem e AMU já aproximam modelos compactos e escrita ou gestão de memória estruturada. Portanto, essa combinação isoladamente não constitui uma lacuna nova.
- AlpsBench avalia diretamente a memória atualizada, além das respostas. Assim, não é seguro afirmar que todos os benchmarks de memória avaliam apenas respostas finais.
- PGMem mede diretamente a qualidade de uma parte do estado: os rótulos de suas arestas. Isso não equivale à fidelidade de um checkpoint JSON completo.
- DiffuAgent compara difusão e autoregressão em tarefas agênticas; sua sumarização de memória e suas chamadas JSON são avaliações distintas. DiffuPlan estuda a revisão de um plano textual, não um checkpoint GU-JSON do SUMIE.
- No escopo examinado, a proposta diferencia-se pela combinação de GU-JSON, esquema e transições do SUMIE, três escritores compactos e avaliação de validade e fidelidade por atualização. A busca limitada não comprova ausência universal de trabalhos similares, e comparar modelos pré-treinados diferentes não isola causalmente o efeito da arquitetura.

## Referências dos estudos selecionados

- Massimo Bini; Ondrej Bohdal; Umberto Michieli; Zeynep Akata; Mete Ozay; Taha Ceritli. **MemLoRA: Distilling Expert Adapters for On-Device Memory Systems**. arXiv, 2025. [Registro 2512.04763v1](https://arxiv.org/abs/2512.04763v1). Primeiro depósito: 2025-12-04.
- Qingyu Lu; Liang Ding; Kanjian Zhang; Jinxia Zhang; Dacheng Tao. **The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Reality Check**. arXiv, 2026. [Registro 2601.12979v3](https://arxiv.org/abs/2601.12979v3). Primeiro depósito: 2026-01-19.
- Jianfei Xiao; Xiang Yu; Chengbing Wang; Wuqiang Zheng; Xinyu Lin; Kaining Liu; Hongxun Ding; Yang Zhang; Wenjie Wang; Fuli Feng; Xiangnan He. **AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment**. arXiv, 2026. [Registro 2603.26680v2](https://arxiv.org/abs/2603.26680v2). Primeiro depósito: 2026-03-09.
- Jingyi Kang; Chunyu Li; Ding Chen; Bo Tang; Feiyu Xiong; Zhiyu Li. **MemReader: From Passive to Active Extraction for Long-Term Agent Memory**. arXiv, 2026. [Registro 2604.07877v2](https://arxiv.org/abs/2604.07877v2). Primeiro depósito: 2026-04-09.
- Wentao Qiu; Haotian Hu; Fanyi Wang; Jinwei Kong; Yu Zhang. **DimMem: Dimensional Structuring for Efficient Long-Term Agent Memory**. arXiv, 2026. [Registro 2605.15759v3](https://arxiv.org/abs/2605.15759v3). Primeiro depósito: 2026-05-15.
- Yubo Wang; Qiuyu Zhao; Zenghui Sun; Shichao Dong; Jinsong Lan; Xiaoyong Zhu; Haoyang Li; Bo Zheng; Lei Chen. **CMI-Mem: Toward Generalizable Long-Term Memory Management via CMI-Augmented Reinforcement Learning**. arXiv, 2026. [Registro 2607.20553v2](https://arxiv.org/abs/2607.20553v2). Primeiro depósito: 2026-07-15.
- Wonjun Choi; Yerim Kim; Yukyung Lee; Susik Yoon. **PGMem: Tightly Coupled Persona-Memory Graph for Lifelong Personalized Agents**. arXiv, 2026. [Registro 2608.01708v2](https://arxiv.org/abs/2608.01708v2). Primeiro depósito: 2026-08-03.
- Jinqing Zhao; Chengcan Wu. **Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents**. arXiv, 2026. [Registro 2609.01272v1](https://arxiv.org/abs/2609.01272v1). Primeiro depósito: 2026-09-01.
- Tao Hwang; Yishi Diao. **AMU:Admission and Memory Update for Personalized Conversations---Structured Memory with SLM Guided Control**. arXiv, 2026. [Registro 2609.36976v2](https://arxiv.org/abs/2609.36976v2). Primeiro depósito: 2026-09-29.
- Qisheng Zhou; Zhen Xiong; Qiaoyu Tan. **DiffuPlan: Editable Planning State for Diffusion Language Model Agents**. arXiv, 2026. [Registro 2610.24717v1](https://arxiv.org/abs/2610.24717v1). Primeiro depósito: 2026-10-17.

## Reprodutibilidade e limitações

- [Inventário e decisões](./mapeamento_focado_inventario_2025_2026.csv); [RIS dos selecionados](./mapeamento_focado_selecionados_2025_2026.ris). O comando gera o RIS, mas não cria nem importa uma coleção no Zotero.
- [Roteiro da triagem](mapeamento_sistematico/protocolo/roteiro_triagem_focado.md), [revisão final](mapeamento_sistematico/dados/execucao_focada_estrita_2026-11-12/revisao_final.json), snapshots por consulta, manifesto com hashes e decisões estão em `mapeamento_sistematico/dados/execucao_focada_estrita_2026-11-12/`.
- A triagem desta execução registrou 16,00 créditos contabilizados em `custo_llm.jsonl`; despesas de pilotos anteriores são separadas.
- Para reproduzir sem rede e sem novas chamadas a modelos, execute `dotnet run scripts/busca_focada.cs -- offline` a partir da pasta `mapeamento_sistematico`.
- As consultas são deliberadamente estreitas: sua precisão tende a melhorar, mas sua sensibilidade pode cair. Os controles não recuperados, os estudos sem palavras explícitas no título/resumo e os trabalhos fora do arXiv exigem verificação adicional.
- Os nomes de autores no RIS são convertidos do nome completo fornecido pelo arXiv pela última palavra; nomes compostos ou institucionais devem ser conferidos após a importação.
