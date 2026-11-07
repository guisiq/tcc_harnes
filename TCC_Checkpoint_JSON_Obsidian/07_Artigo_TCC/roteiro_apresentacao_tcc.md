---
title: "Roteiro de Apresentação e Guia de Defesa — TCC I (Unitins 2026/2)"
subtitle: "Modelos de linguagem compactos como escritores de memória: avaliação da atualização incremental de checkpoints JSON para agentes"
author: "Guilherme Henrique Siqueira Lopes"
advisor: "Prof. Alex Coelho"
date: "2026-11-06"
lang: pt-BR
---

# Roteiro de Apresentação e Guia de Defesa — TCC I

> **Documento-base rastreado:** [artigo_tcc_unitins.md](./artigo_tcc_unitins.md)  
> **Diretrizes aplicadas:** Relatório da [Aula de 31/10/2026](../../AULAS/2026-2/relatorios/2026-10-31.md), [Checklist Consolidado (C51–C60)](../../AULAS/2026-2/checklist_tcc.md) e [Anexo V — Ficha de Avaliação da Apresentação Oral](../../AULAS/2026-2/anexos/Recursos/Manual-de-TCC/anexos/tcc-anexo-v.docx).  
> **Arquivos PowerPoint gerados:**
> - Defesa completa (15–20 min, meta 18 min): [apresentacao_tcc_unitins.pptx](./apresentacao_tcc_unitins.pptx) (15 slides com *Speaker Notes* completas)
> - Simulação de 3 minutos (3MT — 07/11): [apresentacao_3mt_unitins.pptx](./apresentacao_3mt_unitins.pptx) (3 slides enxutos com *Speaker Notes* cronometradas)

---

## 1. Alinhamento com as Diretrizes da Aula e com a Ficha de Avaliação (Anexo V)

Na aula de 31/10/2026, foram estabelecidas regras explícitas para a apresentação de TCC I (50% da nota final da disciplina, avaliada em 5,0 pontos pela banca no Anexo V):

| Critério do Anexo V (Valor) | Diretriz da Aula de 31/10/2026 | Como este Roteiro e os Slides Atendem |
|---|---|---|
| **1. Apresentação (1,0 pt)** | Visual sóbrio, fundo limpo e alto contraste; 3 a 4 tópicos curtos por slide; sem poluição visual; postura profissional e modulação de voz. | Paleta acadêmica sóbria (azul-marinho institucional, cinza-escuro e fundo claro), no máximo 3 a 4 blocos concisos por slide e marcações de `[PAUSA]` e `[ÊNFASE]` no roteiro. |
| **2. Capacidade de Síntese (1,0 pt)** | *Storytelling* com início, meio e fim; usar a capa de forma útil (~2 min); não ler listas extensas nem explicar cronograma linha por linha; meta de **18 minutos** (faixa oficial de 15 a 20 min). | Narrativa encadeada em 15 slides com orçamento exato de 18m00s, margem segura de 2 min abaixo do teto de 20 min e 3 min acima do piso de 15 min. |
| **3. Metodologia e Sequência Lógica (1,0 pt)** | Explicar a transição do Ponto A (problema) ao Ponto B (resultado esperado); justificar por que cada escolha foi feita e por que alternativas foram descartadas; dedicar **5 a 7 minutos** à análise dos trabalhos relacionados e à metodologia; **não criar diagramas, métricas ou abordagens que não constem no texto entregue**. | 8m30s dedicados ao núcleo Trabalhos Relacionados + Materiais e Métodos (Slides 5 a 11). Todo o conteúdo reproduz exclusivamente as equações (1 a 6) e os Quadros 1 a 6 do artigo entregue. |
| **4. Ênfase nos Resultados e Contribuições (1,0 pt)** | Em TCC I, apresentar **expectativas de resultados** e **contribuições pretendidas**, usando o tempo verbal correto (*"O objetivo é..."* no presente; *"Serão executados / Espera-se obter..."* para os experimentos). | Slide 12 detalha os 4 conjuntos de evidências esperadas vinculados aos objetivos `a`, `b` e `c`, diferenciando rigorosamente o que já foi especificado/verificado (Fase 0) do que será executado no TCC II (Fases 1 e 2). |
| **5. Domínio, Clareza, Objetividade e Segurança (1,0 pt)** | Dominar cada conceito, fórmula, métrica e trabalho citado; saber responder perguntas críticas sem decorar respostas prontas; justificar escolhas com base na literatura. | Seção 4 deste documento traz o **Caderno de Arguição** com 10 perguntas críticas/desconfortáveis da banca, a resposta técnica fundamentada e o ponto exato do artigo a revisar. |

---

## 2. Mapa de Tempo da Defesa Completa (Meta: 18m00s | Faixa: 15–20 min)

| Bloco | Slides | Tempo do Bloco | Tempo Acumulado | Peso na Apresentação |
|---|---:|---:|---:|---|
| **1. Abertura, Contexto e Problema** | Slides 1 e 2 | 2m30s | 02:30 | Contextualização na capa + funil da Introdução |
| **2. Pergunta de Pesquisa e Objetivos** | Slides 3 e 4 | 1m30s | 04:00 | Pergunta, Objetivo Geral e 3 Objetivos Específicos |
| **3. Fundamentação e Trabalhos Relacionados** | Slides 5 e 6 | 3m00s | 07:00 | Conceitos-chave e análise assintótica/comparativa (Quadro 1) |
| **4. Materiais e Métodos (Núcleo)** | Slides 7 a 11 | 5m30s | 12:30 | Variáveis (Quadro 2), SUMIE, Modelos, *Harness*, Métricas (Quadro 3) e Rastreabilidade (Quadro 4) |
| **5. Resultados Esperados e Contribuições** | Slide 12 | 2m30s | 15:00 | As 4 entregas empíricas esperadas no TCC II |
| **6. Cronograma Integrado (TCC I e II)** | Slide 13 | 1m30s | 16:30 | Síntese quinzenal (Quadros 5 e 6) sem leitura linha a linha |
| **7. Limitações, Trabalhos Futuros e Fechamento** | Slides 14 e 15 | 1m30s | 18:00 | Validade (interna, construção, externa), continuidades e conclusão |

---

## 3. Roteiro Slide a Slide — Defesa de TCC I (18 minutos)

> **Convenções de oratória no roteiro:**
> - **Negrito na fala**: palavra mais importante da frase — elevar levemente o tom de voz (**modulação**, conforme orientado em `[00:23:02]` da aula).
> - `[PAUSA]`: pausa respiratória curta (1 a 2 segundos) para dar peso à ideia e evitar vícios de linguagem (*"né"*, *"tá"*, *"então"*).
> - **Tempo verbal:** objetivos e desenho metodológico no **presente** (*"O objetivo deste trabalho é..."*); coleta principal e análise dos resultados no **futuro / expectativa** (*"serão avaliados"*, *"espera-se obter"*).

---

### SLIDE 1 — Capa (Usada como Slide Útil de Abertura e Contextualização)
- **Tempo previsto:** 1m15s (Acumulado: 01:15)
- **Rastreabilidade no artigo:** Cabeçalho, Resumo e Seção 1 (parágrafo 1)

**Conteúdo visual do slide:**
- **Universidade Estadual do Tocantins (Unitins) — Bacharelado em Sistemas de Informação**
- **Título:** Modelos de linguagem compactos como escritores de memória: avaliação da atualização incremental de checkpoints JSON para agentes
- **Acadêmico:** Guilherme Henrique Siqueira Lopes
- **Orientador:** Prof. Alex Coelho
- **Local e ano:** Palmas – TO, 2026

**Fala sugerida (Storytelling):**
> "Bom dia a todos os membros da banca e aos presentes. Meu nome é **Guilherme Henrique Siqueira Lopes**, sou orientado pelo professor **Alex Coelho**, e apresento o projeto de TCC I intitulado *Modelos de linguagem compactos como escritores de memória: avaliação da atualização incremental de checkpoints JSON para agentes*. `[PAUSA]`
>
> Para situar o problema logo de partida: agentes baseados em modelos de linguagem hoje executam tarefas em **múltiplas etapas**, nas quais novas informações chegam turno a turno. Como a janela de contexto não pode crescer indefinidamente sem degradar o desempenho e elevar o custo, o agente precisa manter um **estado persistente externo** — um checkpoint em **JSON** que resume tudo o que permanece válido até aquele instante. `[PAUSA]`
>
> O ponto central que motiva esta pesquisa é: o que acontece quando delegamos a **reescrita turno a turno** desse checkpoint JSON para **modelos de linguagem compactos**, de cerca de **0,6 bilhão de parâmetros**, executados localmente sob três paradigmas gerativos diferentes?"

---

### SLIDE 2 — Introdução: Contexto, Problema e Justificativa Acadêmica
- **Tempo previsto:** 1m15s (Acumulado: 02:30)
- **Rastreabilidade no artigo:** Seção 1 (parágrafos 2, 3 e 4)

**Conteúdo visual do slide:**
- **Título:** Contexto, Problema e Lacuna na Literatura
- **Tópico 1 — Checkpoint em JSON (GU-JSON):** Consolidar o estado como pares `atributo: valor` supera resumos em texto livre sob memória restrita (Hwang et al., 2024), mas exige **reescrever todo o JSON** a cada turno.
- **Tópico 2 — Ponto crítico de falha (*memory writer*):** Reescritas sucessivas com modelos de grande porte são custosas; modelos compactos (~0,6B) viabilizam execução local, mas expõem o estado a **erros sintáticos**, **omissão de fatos válidos** e **alucinações**.
- **Tópico 3 — Lacuna científica:** O método GU-JSON e o benchmark SUMIE foram validados apenas em **modelos proprietários de grande porte**; não há comparação controlada entre **paradigmas gerativos compactos** (*decoder-only*, *encoder-decoder* e difusão em blocos) atuando sobre um mesmo checkpoint JSON.

**Fala sugerida (Storytelling):**
> "Na literatura de memória para agentes, Hwang e colaboradores demonstraram em 2024 que atualizar o estado de forma estruturada pelo método **Generate-Update em JSON** — o **GU-JSON** — preserva mais informação sob orçamento restrito de tokens do que atualizar texto livre. `[PAUSA]`
>
> Contudo, o GU-JSON impõe uma exigência severa ao modelo escritor, o chamado *memory writer*: a cada novo turno, ele precisa **regenerar o objeto JSON inteiro**. Se usarmos um modelo de grande porte em cada turno, o custo computacional e a latência crescem rapidamente. Por isso, **modelos compactos** — os SLMs — surgem como candidatos naturais para rodar localmente como escritores dedicados de memória. `[PAUSA]`
>
> Porém, ao revisar a literatura, identificamos uma **lacuna clara**: tanto o GU-JSON quanto o benchmark **SUMIE** foram avaliados apenas com modelos proprietários de grande porte, como Gemini Pro e Ultra. Já estudos recentes que comparam geração autoregressiva e difusão em agentes avaliaram modelos de 7 a 8 bilhões de parâmetros em **texto livre**, sem restrição de checkpoint JSON. Portanto, ainda não sabemos como paradigmas gerativos distintos se comportam na escala de **0,6 bilhão de parâmetros** quando precisam manter simultaneamente a **sintaxe JSON** e a **fidelidade factual**."

---

### SLIDE 3 — Pergunta de Pesquisa e Objetivo Geral
- **Tempo previsto:** 0m45s (Acumulado: 03:15)
- **Rastreabilidade no artigo:** Seção 1 (parágrafos 5 e 6)

**Conteúdo visual do slide:**
- **Título:** Pergunta de Pesquisa e Objetivo Geral
- **Pergunta de Pesquisa (RQ1):** Como representantes compactos dos paradigmas autoregressivo *decoder-only*, *encoder-decoder* e de difusão em blocos diferem na qualidade da atualização incremental de checkpoints pelo método GU-JSON no benchmark SUMIE, sob schema e limite de memória fixos?
- **Objetivo Geral:** Comparar o desempenho dos modelos compactos **Qwen3-0.6B** (*decoder-only*), **T5Gemma B-B** (*encoder-decoder*) e **Qwen3-0.6B BD3LM** (difusão em blocos) como escritores de memória no método **GU-JSON** sobre o benchmark **SUMIE**, mantendo constantes o schema, o prompt e o orçamento de saída de **300 tokens**.

**Fala sugerida (Storytelling):**
> "Diante dessa lacuna, formulamos a seguinte **pergunta de pesquisa**: como representantes compactos dos paradigmas autoregressivo *decoder-only*, *encoder-decoder* e de difusão em blocos diferem na qualidade da atualização incremental de checkpoints pelo método GU-JSON no benchmark SUMIE, sob schema e limite de memória fixos? `[PAUSA]`
>
> Derivado diretamente dessa pergunta, o **objetivo geral** do trabalho **é comparar** o desempenho de três representantes na faixa de 0,6 bilhão de parâmetros — **Qwen3-0.6B**, **T5Gemma B-B** e **Qwen3-0.6B BD3LM** — atuando exclusivamente como escritores de memória no método GU-JSON sobre o benchmark SUMIE, mantendo fixos o schema, o prompt *zero-shot* e o limite máximo de **300 tokens** de saída."

---

### SLIDE 4 — Objetivos Específicos
- **Tempo previsto:** 0m45s (Acumulado: 04:00)
- **Rastreabilidade no artigo:** Seção 1 (parágrafo 6, alíneas `a`, `b`, `c`)

**Conteúdo visual do slide:**
- **Título:** Objetivos Específicos (Entregas Verificáveis)
- **Objetivo (a) — Conformidade Estrutural:** Avaliar a conformidade estrutural dos checkpoints produzidos por cada escritor a partir das taxas de **validade sintática do JSON** e de **aderência ao schema** ao longo das transições.
- **Objetivo (b) — Fidelidade Global e Longitudinal:** Comparar a fidelidade do estado mantido por cada escritor ao longo dos turnos de atualização do SUMIE, utilizando **precisão, revocação, F1 do estado** e **taxa de alucinação**.
- **Objetivo (c) — Perfil por Tipo de Operação:** Analisar o perfil de erro dos escritores segundo a operação exigida no SUMIE, contrastando a **preservação** de atributos inalterados (`PRESERVE`) com a **adição** (`ADD`) e a **atualização** (`UPDATE`) de informações.

**Fala sugerida (Storytelling):**
> "Para alcançar o objetivo geral, definimos **três objetivos específicos**, estruturados não como tarefas operacionais de projeto, mas como **dimensões analíticas verificáveis**: `[PAUSA]`
>
> O **primeiro** é avaliar a **conformidade estrutural** de cada escritor, medindo quanto das saídas brutas constituem JSON válido e obedecem estritamente ao schema.
> O **segundo** é comparar a **fidelidade semântica do estado** ao longo dos turnos do SUMIE por meio de precisão, revocação, F1 do estado e taxa de alucinação.
> E o **terceiro** é decompor o perfil de erro segundo o **tipo de operação** exigida em cada atributo: preservar o que não mudou, adicionar um atributo novo ou atualizar um atributo existente."

---

### SLIDE 5 — Fundamentação Teórica: GU-JSON e Paradigmas Gerativos
- **Tempo previsto:** 1m30s (Acumulado: 05:30)
- **Rastreabilidade no artigo:** Seções 2.1 a 2.5 e Equação 1

**Conteúdo visual do slide:**
- **Título:** Fundamentação: Método GU-JSON e Paradigmas Gerativos
- **Formulação do GU-JSON (Equação 1):**
  $$M_t = G(S,\ M_{t-1},\ O_t)$$
  *(Concentra preservação, integração e formatação JSON em uma única chamada ao modelo $G$, sem código externo de mesclagem).*
- **Três mecanismos distintos de geração sob ~0,6B parâmetros:**
  - **Autoregressivo *decoder-only* (Qwen3-0.6B):** geração sequencial esquerda-direita token a token condicionada ao prefixo.
  - ***Encoder-decoder* (T5Gemma B-B PrefixLM-IT):** codificação bidirecional completa de $(S, M_{t-1}, O_t)$ antes da decodificação autoregressiva.
  - **Difusão discreta em blocos (Qwen3-0.6B BD3LM):** geração autoregressiva de blocos combinada com refinamento iterativo paralelo de tokens mascarados.

**Fala sugerida (Storytelling):**
> "Na fundamentação teórica, destacamos por que o método **GU-JSON**, formalizado na Equação 1, é o instrumento ideal para isolar o escritor de memória. Em $M_t = G(S, M_{t-1}, O_t)$, o modelo recebe o schema $S$, o estado anterior $M_{t-1}$ e a nova observação $O_t$, e gera sozinho o novo JSON $M_t$. Diferente de arquiteturas que usam controladores programáticos externos para editar caminhos da árvore, o GU-JSON obriga o **próprio modelo** a copiar o que permanece válido e integrar o que é novo em uma única chamada. `[PAUSA]`
>
> E por que comparar três paradigmas gerativos nessa tarefa? Porque reescrever um JSON exige comportamentos diferentes de cada arquitetura:
> O modelo ***decoder-only*** gera token a token da esquerda para a direita; qualquer erro em uma chave ou vírgula propaga para o resto da sequência.
> O modelo ***encoder-decoder*** lê o estado anterior e o novo parágrafo com **atenção bidirecional** no codificador antes de iniciar a escrita.
> Já a **difusão em blocos (BD3LM)** atualiza múltiplos tokens em paralelo dentro de cada bloco por remoção iterativa de ruído — um mecanismo que, segundo Lu e colaboradores em 2026, vai bem em sumarização textual livre, mas apresenta fragilidade em sintaxe estrita."

---

### SLIDE 6 — Análise Comparativa dos Trabalhos Relacionados (Quadro 1)
- **Tempo previsto:** 1m30s (Acumulado: 07:00)
- **Rastreabilidade no artigo:** Seção 2.6 e Quadro 1

**Conteúdo visual do slide:**
- **Título:** Análise Comparativa dos Trabalhos Relacionados (Quadro 1)
- **Tabela comparativa (síntese do Quadro 1 do artigo):**

| Trabalho | Representação e Atualização | Modelos / Escala | Objeto Avaliado | Compara Paradigmas? |
|---|---|---|---|---|
| **Hwang et al. (2024); SUMIE (2025)** | Texto e JSON (GO, GU, GM, CoK) | Gemini Ultra e Pro (grande porte) | Fidelidade de resumos incrementais (SUMIE / BooookScore) | Não |
| **PRISM (Jayalath et al., 2025)** | Schema hierárquico + patch programático | Modelos de contexto curto | Tarefa final de longo alcance | Não |
| **Intrinsic Memory (Yuen et al., 2025)** | Templates JSON por agente | LLMs em sistemas multiagente | Desempenho da tarefa multiagente | Não |
| **MemoryAgentBench (Hu et al., 2025)** | Múltiplos sistemas de memória | Diversos agentes | Respostas finais (QA) após múltiplos turnos | Não |
| **Lu et al. (2026)** | Texto livre e *tool calling* | Difusão vs. AR (7B a 8B) | Fluxos agênticos gerais | Sim (sem checkpoint JSON) |
| **JSONSchemaBench (Geng et al., 2025)** | JSON Schema estático | Decodificação restrita | Conformidade sintática estática | Não |
| **Este trabalho** | **Checkpoint JSON fixo (GU-JSON)** | **3 SLMs (~0,6B): AR, Enc-Dec e BD3LM** | **Validade e fidelidade por transição, turno e operação no SUMIE** | **Sim, sob protocolo controlado** |

**Fala sugerida (Storytelling):**
> "No Quadro 1 do artigo, realizamos a **análise assintótica e comparativa** dos trabalhos relacionados sob cinco dimensões. `[PAUSA]`
>
> Observe três contrastes fundamentais que justificam nossas escolhas:
> Primeiro: sistemas como **PRISM**, **Intrinsic Memory Agents** e **MemoryAgentBench** avaliam a memória apenas pela **resposta final da tarefa**. Se o modelo perder silenciosamente um atributo no terceiro turno e a pergunta final não cobrar aquele atributo, a falha passa despercebida. Por isso, nossa avaliação inspeciona **diretamente o estado JSON em cada transição**. `[PAUSA]`
>
> Segundo: **JSONSchemaBench** avalia geração estruturada em passo único estático, enquanto nós avaliamos **reescrita incremental ao longo de múltiplos turnos**.
> E terceiro: **Hwang et al.** estabeleceram o GU-JSON e o SUMIE apenas em modelos gigantes, e **Lu et al.** compararam difusão e autoregressão em 7 a 8B sem checkpoint JSON. **Nosso trabalho** preenche exatamente a interseção vazia dessa matriz: comparar três paradigmas na escala compacta de **0,6B**, sob protocolo controlado de atualização JSON turno a turno."

---

### SLIDE 7 — Materiais e Métodos: Desenho Experimental e Controle de Variáveis (Quadro 2)
- **Tempo previsto:** 1m15s (Acumulado: 08:15)
- **Rastreabilidade no artigo:** Seções 3.1, 3.2, 3.3 e Quadro 2

**Conteúdo visual do slide:**
- **Título:** Desenho Experimental e Controle de Variáveis (Quadro 2)
- **Princípio de controle ("uma coisa de cada vez"):**
  - **Variável Independente Única:** Modelo escritor (`Qwen3-0.6B` vs. `T5Gemma B-B` vs. `Qwen3-0.6B BD3LM`).
  - **Variáveis Controladas:** Método GU-JSON; schema mínimo `{"state": {"chave": "valor"}}`; prompt *zero-shot* único em inglês; orçamento máximo de **300 tokens**; contexto de até 8.192 tokens; regime ***prompt-only*** (sem decodificação restrita por gramática).
- **Por que descartamos alternativas?**
  - *Sem decodificação restrita externa:* motores de gramática atuam de modo assimétrico entre geração autoregressiva e difusão; o regime *prompt-only* mede a capacidade intrínseca do modelo.
  - *Estado anterior padrão-ouro ($M_{t-1}^*$):* garante que os três modelos recebam exatamente a mesma entrada em cada turno $t$, isolando o erro da transição.
- **Hipóteses ($H_0$ e $H_1$):** Teste de igualdade ($H_0$) vs. diferença estatisticamente significativa ($H_1$) em *State F1*, *Preservation Accuracy* e *Update Accuracy*.

**Fala sugerida (Storytelling):**
> "Entrando em **Materiais e Métodos**, esta é uma pesquisa experimental quantitativa guiada por um princípio estrito de controle: **modificar apenas uma variável por vez**. `[PAUSA]`
>
> Como sintetiza o Quadro 2 do artigo, a única variável independente é o **modelo escritor**. Todas as demais condições permanecem constantes: o método GU-JSON, o schema plano `{\"state\": {\"chave\": \"valor\"}}`, o prompt *zero-shot* em inglês e o teto de **300 tokens** de saída. `[PAUSA]`
>
> Aqui cabe justificar **duas escolhas metodológicas importantes**:
> Primeiro, por que **não usar decodificação restrita por gramática**? Porque os algoritmos de restrição gramatical operam de forma diferente em decodificadores esquerda-direita e em modelos de difusão mascarada; se os ativássemos, estaríamos medindo o motor externo de gramática, e não a capacidade intrínseca de cada modelo manter o JSON.
> Segundo, por que alimentar cada turno $t$ com o **estado anterior de referência $M_{t-1}^*$ padrão-ouro**, em vez da própria saída anterior do modelo? Porque, se um modelo quebrasse a sintaxe JSON logo no turno 2, ele ficaria sem entrada válida para os turnos 3 em diante, inviabilizando a comparação pareada nas mesmas instâncias."

---

### SLIDE 8 — Materiais e Métodos: Dados (SUMIE) e Rotulagem de Operações
- **Tempo previsto:** 1m05s (Acumulado: 09:20)
- **Rastreabilidade no artigo:** Seção 3.4

**Conteúdo visual do slide:**
- **Título:** Conjunto de Dados SUMIE e Preparação das Transições
- **Benchmark SUMIE (Hwang et al., 2025 — licença Apache-2.0):**
  - Sequências ordenadas de parágrafos sobre entidades com fatos novos, repetições, informações distratoras e perspectivas divergentes.
- **Construção das tuplas de transição $(M_{t-1}^*,\ O_t,\ M_t^*)$:**
  - $M_{t-1}^*$: checkpoint acumulado de referência até o turno $t-1$.
  - $O_t$: parágrafo da nova observação no turno $t$.
  - $M_t^*$: checkpoint esperado após integrar $O_t$.
- **Rotulagem determinística por operação em cada atributo de $M_t^*$:**
  - `PRESERVE`: atributo de $M_{t-1}^*$ não alterado por $O_t$ (deve ser mantido intacto).
  - `ADD`: atributo inédito introduzido em $O_t$.
  - `UPDATE`: atributo já presente em $M_{t-1}^*$ que recebe informação complementar ou perspectiva divergente em $O_t$.

**Fala sugerida (Storytelling):**
> "Para os dados do experimento, utilizamos o benchmark público **SUMIE**, distribuído pela Google DeepMind sob licença Apache-2.0. Nele, cada entidade é descrita por uma sequência de parágrafos com gabarito explícito de atributos e valores em cada etapa. `[PAUSA]`
>
> A partir dessas sequências, estruturamos cada passo $t$ como uma tupla padronizada contendo o estado acumulado anterior $M_{t-1}^*$, a observação $O_t$ e o estado esperado $M_t^*$. Comparando determinísticamente o gabarito anterior com o atual, cada atributo recebe um entre três rótulos de operação: **`PRESERVE`**, quando o atributo não foi tocado pela nova observação e precisa ser preservado sem corrupção; **`ADD`**, quando é um atributo novo; e **`UPDATE`**, quando um atributo já existente recebe informação complementar ou uma perspectiva divergente que deve ser integrada."

---

### SLIDE 9 — Materiais e Métodos: Ambiente Local, *Harness* e Fases (0, 1 e 2)
- **Tempo previsto:** 1m05s (Acumulado: 10:25)
- **Rastreabilidade no artigo:** Seções 3.5, 3.6 e 3.8

**Conteúdo visual do slide:**
- **Título:** Ambiente de Execução, *Harness* Experimental e Fases
- **Hardware local e controle numérico:**
  - Execução principal: Notebook Core i5 (10ª ger.), 24 GB RAM, GPU **NVIDIA GTX 1650**, com precisão de ponto flutuante uniforme (`FP16`/`BF16`) e *commit hashes* fixados em manifesto.
- **Pipeline do *Harness* em 8 etapas por transição:**
  - `(1)` Leitura de $(M_{t-1}^*, O_t, M_t^*)$ $\rightarrow$ `(2)` Template de prompt fixo $\rightarrow$ `(3)` Inferência (teto de 300 tokens) $\rightarrow$ `(4)` Gravação da saída bruta $\rightarrow$ `(5)` *Parser* `json.loads` sem reparo $\rightarrow$ `(6)` Validador de schema `state` $\rightarrow$ `(7)` Cálculo determinístico de métricas $\rightarrow$ `(8)` Log auditável em JSON Lines.
- **Três fases sequenciais de execução:**
  - **Fase 0 (TCC I):** Verificação funcional em 15 transições sintéticas e testes unitários do validador.
  - **Fase 1 (Piloto — TCC II):** 25 entidades do SUMIE para calibrar canonicalização e checar comprimento $\le 300$ tokens.
  - **Fase 2 (Principal — TCC II):** Execução completa dos 3 escritores no conjunto de avaliação do SUMIE.

**Fala sugerida (Storytelling):**
> "Toda a inferência foi desenhada para rodar em **hardware local** — um equipamento com GPU dedicada **GTX 1650** e 24 GB de RAM — mantendo o mesmo formato de ponto flutuante entre os três modelos, já que SLMs sofrem degradação assimétrica sob quantização agressiva. `[PAUSA]`
>
> Para garantir reprodutibilidade, o experimento é executado por um ***harness* modular de oito etapas**: ele lê a tupla, monta o prompt fixo, invoca o adaptador do modelo com limite de 300 tokens, salva a saída bruta em disco sem nenhum pós-processamento ou reparo de sintaxe, valida o JSON e o schema, calcula as métricas e grava tudo em JSON Lines. `[PAUSA]`
>
> Seguindo a recomendação da disciplina de validar a viabilidade técnica ainda no projeto, dividimos o procedimento em três fases: a **Fase 0**, com 15 transições sintéticas e testes unitários do avaliador para validar o ambiente local; a **Fase 1**, um estudo piloto em 25 entidades do SUMIE para calibrar a canonicalização textual; e a **Fase 2**, o experimento completo no SUMIE."

---

### SLIDE 10 — Materiais e Métodos: Métricas (Quadro 3) e Análise Estatística
- **Tempo previsto:** 1m15s (Acumulado: 11:40)
- **Rastreabilidade no artigo:** Seções 3.7, 3.8, Equações 2 a 6 e Quadro 3

**Conteúdo visual do slide:**
- **Título:** Métricas de Avaliação (Quadro 3) e Plano Estatístico
- **Três famílias de métricas complementares:**
  1. **Estruturais (todas as transições):** *JSON Validity* (`json.loads` sem reparo) e *Schema Validity* (objeto raiz `state` válido).
  2. **Fidelidade de Estado (Equações 2–4):** *State Precision* ($P = \frac{TP}{TP+FP}$), *State Recall* ($R = \frac{TP}{TP+FN}$), ***State F1*** ($F_1 = \frac{2PR}{P+R}$, primária) e *Hallucination Rate*.
  3. **Fidelidade por Operação (Equações 5–6):** ***Preservation Accuracy*** ($PA$, sobre `PRESERVE`) e ***Update Accuracy*** ($UA$, agregada e separada em `ADD` e `UPDATE`).
- **Dupla visão de reporte:** **Condicional** (apenas sobre JSONs válidos, isolando semântica) e **Global / *end-to-end*** (atribuindo zero às falhas sintáticas).
- **Análise estatística pareada:** IC 95% via *bootstrap* não paramétrico (10.000 reamostragens por entidade) + teste de **Friedman** global e **Wilcoxon pareado** com correção de Holm-Bonferroni ($\alpha = 0{,}05$).

**Fala sugerida (Storytelling):**
> "No Quadro 3 e nas Equações 2 a 6, estruturamos as métricas para separar com exatidão **forma** e **conteúdo**. `[PAUSA]`
>
> Na dimensão **estrutural**, medimos a validade sintática do JSON e a aderência ao schema sobre todas as transições.
> Na dimensão de **estado**, convertemos o JSON em pares canônicos `atributo-valor` e calculamos Precisão, Revocação, **F1 do estado** e Taxa de Alucinação.
> E na dimensão de **operação**, calculamos separadamente a **Acurácia de Preservação** ($PA$) para os atributos `PRESERVE` e a **Acurácia de Atualização** ($UA$) para `ADD` e `UPDATE`. `[PAUSA]`
>
> Reportaremos essas métricas tanto na visão **condicional** — apenas onde o JSON foi válido, para isolar a capacidade semântica — quanto na visão **global**, atribuindo zero quando o JSON quebra. E como os três escritores percorrem exatamente as mesmas entidades, aplicaremos *bootstrap* em nível de entidade com 10 mil reamostragens e testes não paramétricos pareados de **Friedman** e **Wilcoxon** com correção de Holm-Bonferroni."

---

### SLIDE 11 — Matriz de Rastreabilidade Metodológica (Quadro 4)
- **Tempo previsto:** 0m50s (Acumulado: 12:30)
- **Rastreabilidade no artigo:** Seção 3.9 e Quadro 4

**Conteúdo visual do slide:**
- **Título:** Rastreabilidade: Objetivos $\rightarrow$ Artefatos $\rightarrow$ Evidências (Quadro 4)

| Objetivo Específico | Artefato / Procedimento | Evidência Produzida | Métrica e Critério de Análise |
|---|---|---|---|
| **a) Conformidade estrutural** | *Parser* JSON, validador de schema e log bruto sem reparo | Tabela de validade por escritor, curva por turno e distribuição dos tipos de erro sintático | *JSON Validity* e *Schema Validity* (IC 95% via *bootstrap* e diferenças pareadas) |
| **b) Fidelidade do estado ao longo dos turnos** | Estados de referência ($M_t^*$) e avaliador determinístico de pares | Tabela comparativa global e condicional; curvas longitudinais ao longo dos turnos $t$ | *State P*, *R*, ***State F1*** (primária) e *Hallucination Rate* (IC 95%, Friedman/Wilcoxon) |
| **c) Perfil de erro por operação** | Rotulador determinístico (`PRESERVE`, `ADD`, `UPDATE`) | Tabela e gráfico estratificado por operação e curva de retenção de atributos | ***Preservation Accuracy*** e ***Update Accuracy*** (`ADD`/`UPDATE`) com IC 95% e teste pareado |

**Fala sugerida (Storytelling):**
> "O Quadro 4 do artigo consolida a matriz de rastreabilidade metodológica, garantindo que nenhum objetivo fique sem verificação empírica e que nenhuma métrica exista sem responder a uma pergunta. `[PAUSA]`
>
> O **Objetivo (a)** é verificado pelo *parser* e validador de schema, gerando a tabela de validade e a distribuição das falhas sintáticas.
> O **Objetivo (b)** é verificado pelo comparador determinístico contra $M_t^*$, produzindo as curvas de *State F1* e alucinação ao longo dos turnos $t$.
> E o **Objetivo (c)** é verificado pelo rotulador de operações, contrastando diretamente *Preservation Accuracy* e *Update Accuracy*."

---

### SLIDE 12 — Resultados e Contribuições Esperadas (Seção 4.1)
- **Tempo previsto:** 2m30s (Acumulado: 15:00)
- **Rastreabilidade no artigo:** Seção 4.1 (itens 1 a 4)

**Conteúdo visual do slide:**
- **Título:** Resultados e Contribuições Esperadas (TCC II)
- **1. Caracterização da robustez estrutural (Objetivo a):** Quantificação das taxas de *JSON Validity* e *Schema Validity* em regime *prompt-only* e classificação dos modos de falha (truncamento aos 300 tokens, chaves malformadas ou texto extra).
- **2. Fidelidade longitudinal por turno $t$ (Objetivo b):** Curvas de degradação de *State F1* e *Hallucination Rate* conforme o checkpoint acumulado cresce e se aproxima do teto de 300 tokens.
- **3. Decomposição por operação de estado (Objetivo c):** Distinção empírica entre escritores **conservadores** (alta *Preservation Accuracy*, baixa adição) e escritores **propensos a esquecimento/sobrescrita** ao aplicar `ADD` e `UPDATE`.
- **4. Contribuição técnica e científica:** Demonstração empírica da dissociação entre validade sintática e fidelidade semântica em SLMs (~0,6B) + entrega de protocolo e *harness* reprodutíveis.

**Fala sugerida (Storytelling):**
> "Como estamos na defesa da proposta de TCC I, destacamos na Seção 4.1 os **quatro conjuntos de resultados e contribuições que se espera obter** com a execução da Fase 2 no TCC II: `[PAUSA]`
>
> **Primeiro**, vinculado ao Objetivo (a), espera-se caracterizar a estabilidade sintática intrínseca de cada paradigma na escala de 0,6B — identificando se falhas estruturais decorrem de truncamento no limite de 300 tokens, perda de delimitadores ou emissão de texto fora do JSON. `[PAUSA]`
>
> **Segundo**, vinculado ao Objetivo (b), espera-se mapear por meio das curvas longitudinais em qual ponto da sequência de turnos o crescimento do checkpoint passa a degradar o *State F1* de cada escritor. `[PAUSA]`
>
> **Terceiro**, vinculado ao Objetivo (c), a estratificação por operação permitirá distinguir perfis opostos de falha: por exemplo, um escritor excessivamente **conservador**, que copia bem o estado anterior mas falha em adicionar fatos novos, versus um escritor que integra fatos novos mas **esquece ou corrompe** atributos antigos que deveriam ser preservados. `[PAUSA]`
>
> **Por fim**, como contribuição prática e científica para Sistemas de Informação, o trabalho entregará tanto o *harness* experimental auditável quanto evidências objetivas para orientar quando um modelo compacto local de 0,6B é suficiente para manter checkpoints JSON e onde ele exige mecanismos adicionais de controle."

---

### SLIDE 13 — Cronograma Físico Integrado: TCC I e TCC II (Quadros 5 e 6)
- **Tempo previsto:** 1m30s (Acumulado: 16:30)
- **Rastreabilidade no artigo:** Seção 4.2 e Quadros 5 e 6

**Conteúdo visual do slide:**
- **Título:** Cronograma Integrado: TCC I (2026/2) e TCC II (2027/1)
- **TCC I — 2026/2 (Atividades 1 a 8 — Quinzenal, Ago a Dez):**
  - **Ago–Out (Concluídas):** `(1)` Tema/problema/objetivos; `(2)` Revisão bibliográfica; `(3)` Protocolo experimental e métricas.
  - **Out–Nov (Em conclusão):** `(4)` Verificação de licenças e requisitos locais; `(5)` Estrutura base do *harness* e testes unitários; `(6)` Execução da **Fase 0** (15 transições sintéticas); `(7)` Redação e revisão do projeto.
  - **Nov–Dez:** `(8)` Defesa do projeto de TCC I e incorporação das recomendações da banca.
- **TCC II — 2027/1 (Atividades 9 a 15 — Quinzenal, Fev a Jun):**
  - **Fev – Mar 1ª:** `(9)` Preparação completa do SUMIE ($M_t^*$ e rótulos) e `(10)` **Fase 1 (Piloto em 25 entidades)**.
  - **Mar 2ª – Abr:** `(11)` **Fase 2 (Experimento principal com os 3 modelos)** e `(12)` Processamento estatístico (*bootstrap* e testes pareados).
  - **Abr 2ª – Jun:** `(13)` Tabelas/gráficos, `(14)` Redação de resultados e discussão e `(15)` Revisão final e defesa do TCC II.

**Fala sugerida (Storytelling):**
> "Nos Quadros 5 e 6 do artigo, apresentamos o **cronograma integrado de TCC I e TCC II**, organizado em janelas quinzenais com dependências explícitas entre as 15 atividades. `[PAUSA]`
>
> Sem ler linha por linha, destaco a lógica de transição entre os dois semestres:
> Aqui no **TCC I**, entre agosto e novembro, concluímos a delimitação do problema, a revisão da literatura, a especificação matemática do protocolo e a construção da base do *harness* com a **Fase 0 de verificação funcional sintética**, garantindo que a infraestrutura não fique para ser testada apenas no último semestre. `[PAUSA]`
>
> Já no **TCC II**, iniciamos em fevereiro com a geração dos estados acumulados do SUMIE, executamos o **estudo piloto na primeira quinzena de março**, rodamos o **experimento principal entre março e abril**, realizamos a análise estatística pareada em abril e dedicamos maio e junho à redação da discussão crítica e à defesa final."

---

### SLIDE 14 — Limitações Metodológicas e Ameaças à Validade (Seção 3.10)
- **Tempo previsto:** 0m45s (Acumulado: 17:15)
- **Rastreabilidade no artigo:** Seção 3.10 (alíneas `a`, `b`, `c`)

**Conteúdo visual do slide:**
- **Título:** Limitações Metodológicas e Ameaças à Validade
- **Validade Interna (Representantes vs. Arquitetura Pura):**
  - Os três modelos (~0,6B) diferem em corpus de pré-treinamento e tokenizador; portanto, os resultados comparam o desempenho efetivo dos **representantes avaliados**, sem alegar causalidade isolada da arquitetura em abstrato.
- **Validade de Construção (Avaliação Determinística vs. Juiz Neural):**
  - Substitui o avaliador baseado em LLM por correspondência determinística após canonicalização textual — eliminando viés e variância de juiz neural, calibrada na Fase 1 (piloto).
- **Validade Externa (Isolamento por Transição):**
  - O uso do estado anterior padrão-ouro ($M_{t-1}^*$) isola com rigor o erro de cada turno, mas não mede o acúmulo composto de erros em execução livre nem o impacto na tarefa final do agente.

**Fala sugerida (Storytelling):**
> "Toda pesquisa experimental rigorosa precisa explicitar o alcance do seu método. Na Seção 3.10, documentamos três ameaças à validade e como o protocolo lida com elas: `[PAUSA]`
>
> Quanto à **validade interna**, como Qwen3, T5Gemma e BD3LM não foram pré-treinados exatamente no mesmo corpus, nossas conclusões referem-se aos **três representantes na escala de 0,6B**, sem extrapolar causalidade absoluta para os paradigmas em abstrato.
> Quanto à **validade de construção**, trocamos o juiz neural original do SUMIE por comparação determinística canonicalizada, eliminando variância de avaliador externo e calibrando a normalização no piloto.
> E quanto à **validade externa**, o uso do estado anterior padrão-ouro isola o erro por transição individual, delimitando o escopo em relação à execução livre encadeada."

---

### SLIDE 15 — Considerações Finais e Trabalhos Futuros (Seção 5)
- **Tempo previsto:** 0m45s (Acumulado: 18:00)
- **Rastreabilidade no artigo:** Seção 5

**Conteúdo visual do slide:**
- **Título:** Considerações Finais e Desdobramentos Futuros
- **Síntese do projeto:**
  - Protocolo experimental controlado para avaliar escritores compactos de memória (~0,6B) sob GU-JSON no benchmark SUMIE, dissociando **validade estrutural**, **fidelidade longitudinal** e **acurácia por operação** (`PRESERVE`, `ADD`, `UPDATE`).
- **Trabalhos futuros (pós-TCC II):**
  1. Avaliação em **regime autoregressivo encadeado** (usando a própria saída $M_{t-1}$ do modelo como entrada de $t$ para medir erro composto).
  2. Extensão para cenários de **substituição temporal explícita de fatos** (*supersession*, como no FactConsolidation-SH).
  3. Comparação direta entre reescrita integral (**GU-JSON**) e atualização seletiva de chaves (**CoK-JSON**) e avaliação do efeito de **decodificação restrita por gramática**.
- **Encerramento:** Agradecimento e abertura para arguição da banca.

**Fala sugerida (Storytelling):**
> "Para concluir: este projeto estabelece um protocolo experimental controlado e auditável para responder se modelos compactos locais de **0,6 bilhão de parâmetros** conseguem sustentar a reescrita incremental de checkpoints JSON pelo método GU-JSON, separando falhas sintáticas de falhas semânticas por turno e por operação. `[PAUSA]`
>
> E como continuidades científicas **posteriores à conclusão do projeto completo no TCC II**, destacamos quatro frentes: avaliar o acúmulo composto de erros em execução livre encadeada; estender o protocolo para substituição temporal explícita de fatos no FactConsolidation-SH; comparar o GU-JSON contra o *Chain-of-Key* em JSON; e medir o ganho de motores de decodificação restrita por gramática em cada paradigma. `[PAUSA]`
>
> Agradeço a atenção da banca e coloco-me à disposição para as perguntas e contribuições. Muito obrigado."

---

## 4. Roteiro da Simulação de 3 Minutos (3MT — Three Minute Thesis | 07/11/2026)

> **Orientações da aula de 31/10 (`[01:00:03]` a `[01:07:03]`):**
> - **Duração máxima:** 3 minutos (falar de forma ordenada e pausada, sem acelerar para tentar comprimir os 18 minutos em 3).
> - **Foco obrigatório:** Problema complexo explicado com clareza $\rightarrow$ Objetivo e método essencial $\rightarrow$ Principal resultado esperado e contribuição.
> - **Logística:** Chegada às **08h00** (início às **08h05**), **câmera aberta** na altura dos olhos, **slide compartilhado**, ordem alfabética e permanência até o encerramento da aula.
> - **Arquivo PowerPoint específico:** [apresentacao_3mt_unitins.pptx](./apresentacao_3mt_unitins.pptx) (3 slides enxutos: Capa/Problema, Desenho Experimental e Contribuição Esperada).

### Cronometragem Segundo a Segundo (Total: 2m45s — margem segura de 15s antes dos 3m00s)

#### [00:00 – 00:55] Slide 1: O Problema da Memória em Agentes e a Lacuna dos Modelos Compactos (55s)
> "Bom dia a todos. Meu nome é **Guilherme Henrique Siqueira Lopes**, sou orientado pelo professor **Alex Coelho**, e meu trabalho investiga **modelos de linguagem compactos como escritores de memória JSON para agentes**. `[PAUSA]`
>
> Quando um agente de IA executa uma tarefa longa em várias etapas, ele não pode guardar todo o histórico bruto indefinidamente. Uma solução eficaz na literatura é manter um **checkpoint em JSON** atualizado a cada turno pelo método **Generate-Update em JSON (GU-JSON)**. Porém, nesse método, o modelo escritor precisa **reescrever o objeto JSON inteiro** a cada nova informação. Usar modelos gigantes para isso a cada turno é caro e lento; já usar **modelos compactos locais**, de **0,6 bilhão de parâmetros**, reduz drasticamente o custo, mas cria um risco crítico: será que eles conseguem reescrever o JSON sem quebrar a sintaxe, sem esquecer fatos antigos e sem alucinar?"

#### [00:55 – 01:55] Slide 2: Objetivo e Desenho Experimental Controlado (60s)
> "Hoje, a literatura validou o GU-JSON apenas em modelos proprietários de grande porte e ainda não comparou diferentes paradigmas gerativos compactos nessa função. `[PAUSA]`
>
> Por isso, o **objetivo deste trabalho** é comparar três modelos compactos na faixa de **0,6B de parâmetros** representando paradigmas distintos: o **Qwen3-0.6B** (autoregressivo *decoder-only*), o **T5Gemma B-B** (*encoder-decoder* com atenção bidirecional) e o **Qwen3-0.6B BD3LM** (difusão discreta em blocos). `[PAUSA]`
>
> Em um experimento controlado sobre o benchmark **SUMIE**, mantemos fixos o schema JSON, o prompt *zero-shot* e o orçamento de **300 tokens**, variando **apenas o modelo escritor**. Em cada transição, avaliamos de forma independente a **validade estrutural do JSON**, a **fidelidade do estado** por precisão, revocação e F1, e a acurácia por operação: **preservar** atributos antigos, **adicionar** novos e **atualizar** existentes."

#### [01:55 – 02:45] Slide 3: Resultados Esperados e Principal Contribuição (50s)
> "Como **resultado esperado**, este estudo identificará o perfil exato de falha de cada paradigma compacto: distinguindo, por exemplo, se um modelo falha por corrupção sintática do JSON, se ele é conservador demais ao ignorar fatos novos, ou se ele sobrescreve e esquece fatos antigos à medida que o estado se aproxima dos 300 tokens. `[PAUSA]`
>
> A **principal contribuição** do trabalho é fornecer um protocolo experimental e um *harness* local totalmente reprodutíveis, entregando evidências empíricas para que desenvolvedores de sistemas agênticos saibam escolher e dimensionar modelos compactos locais na manutenção de estado estruturado. Muito obrigado!"

---

## 5. Caderno de Arguição — 10 Perguntas Críticas/"Desconfortáveis" da Banca e Respostas Técnicas

Conforme orientado na aula de 31/10 (`[00:40:02]`–`[00:43:05]`), a banca (os dois membros avaliadores convidados) fará perguntas durante 10 minutos para verificar **domínio real**, **justificativa das escolhas** e **consciência das limitações**. Abaixo estão as 10 perguntas mais exigentes que podem ser extraídas do texto, com a resposta técnica e onde revisar no artigo.

### Pergunta 1 — Por que usar o estado anterior padrão-ouro ($M_{t-1}^*$) em vez da própria saída do modelo no turno anterior? Isso não afasta o experimento do cenário real?
- **Onde está no artigo:** Seção 3.3 (parágrafo 1), Seção 3.10 (alínea `c`) e Seção 5.
- **Como responder tecnicamente:**
  > "Excelente pergunta, professor(a). Em execução livre encadeada (*rollout*), se um modelo de 0,6B produzir um JSON com erro sintático logo no turno 2, todas as transições seguintes daquela entidade (turnos 3, 4, 5...) ficam inviabilizadas ou contaminadas por uma entrada corrompida, impedindo a comparação pareada entre os três modelos no mesmo estado de entrada. Ao fornecer $M_{t-1}^*$ padrão-ouro em cada transição, nós **isolamos experimentalmente o erro daquela transição específica** em função do tamanho do estado acumulado no turno $t$. Reconhecemos explicitamente na Seção 3.10 que isso delimita a validade externa, e por isso a avaliação em regime autoregressivo encadeado está registrada na Seção 5 como o primeiro desdobramento futuro após isolarmos a capacidade por transição."

### Pergunta 2 — Os três modelos (Qwen3-0.6B, T5Gemma B-B e Qwen3-0.6B BD3LM) tiveram pré-treinamentos e tokenizadores diferentes. Como você pode afirmar que a diferença vem do paradigma gerativo?
- **Onde está no artigo:** Seção 3.5 (parágrafo 2), Seção 3.10 (alínea `a`) e Seção 5.
- **Como responder tecnicamente:**
  > "Nós não afirmamos causalidade isolada da arquitetura em abstrato — e esse cuidado está explicitado tanto na Seção 3.5 quanto nas ameaças à validade interna na Seção 3.10. Na literatura atual de SLMs, não existem três checkpoints abertos de ~0,6B treinados do zero exatamente com o mesmo corpus, mesmo tokenizador e mesmo pós-treinamento para *decoder-only*, *encoder-decoder* e difusão em blocos. Por isso, o trabalho é formulado como uma avaliação de **representantes compactos** de cada paradigma sob condições de inferência estritamente controladas (mesmo prompt, mesmo schema, mesmo orçamento de 300 tokens e mesma precisão numérica)."

### Pergunta 3 — Por que você não usou decodificação restrita por gramática (como Outlines, XGrammar ou CFG para difusão) para garantir 100% de JSON válido?
- **Onde está no artigo:** Seção 2.4 (parágrafo 2) e Seção 3.2 (Quadro 2).
- **Como responder tecnicamente:**
  > "Por duas razões metodológicas documentadas na Seção 2.4: primeiro, um dos nossos objetivos específicos — o Objetivo (a) — é justamente medir a **conformidade estrutural intrínseca** de cada modelo escritor sem auxílio externo. Segundo, os algoritmos de decodificação restrita atuam de forma diferente sobre geração autoregressiva esquerda-direita e sobre desmascaramento iterativo em difusão (como mostram Geng et al., 2025 e Mündler et al., 2025). Se aplicássemos decodificadores restritos distintos em cada família, introduziríamos uma variável confundidora externa ao modelo."

### Pergunta 4 — O artigo original do SUMIE usa um LLM como juiz (*LLM-as-a-judge*) para avaliar os resumos. Por que você trocou isso por comparação exata/determinística após canonicalização?
- **Onde está no artigo:** Seção 3.4 (parágrafo 3), Seção 3.7 (parágrafo 1) e Seção 3.10 (alínea `b`).
- **Como responder tecnicamente:**
  > "No estudo original de Hwang et al. (2025), o SUMIE avaliava também resumos em texto livre (GU-Text), onde um juiz neural era indispensável para verificar se um fato estava presente na prosa. No nosso recorte, o estado é restrito ao schema `{\"state\": {\"chave\": \"valor\"}}` e construído sobre os pares atributo-valor anotados no próprio SUMIE. Usar comparação determinística após canonicalização textual elimina a variância estocástica, o custo e o viés de preferência de um LLM juiz. Para mitigar o risco de falsos negativos por pequenas variações de grafia, incluímos a **Fase 1 (estudo piloto em 25 entidades)** especificamente para calibrar e auditar as regras de canonicalização antes da Fase 2."

### Pergunta 5 — Uma GPU GTX 1650 (4 GB de VRAM) consegue rodar os três modelos de ~0,6B sem estourar memória ou precisar de quantização agressiva de 4 bits?
- **Onde está no artigo:** Seção 3.5 e Seção 3.6.
- **Como responder tecnicamente:**
  > "Sim, e essa foi uma razão central para escolhermos a faixa de **0,6 bilhão de parâmetros**. Em precisão de 16 bits (`FP16` ou `BF16`), os pesos de um modelo de 0,6B ocupam aproximadamente **1,2 GB de memória**, cabendo com folga nos 4 GB de VRAM da GTX 1650 junto com o cache KV para entradas curtas e saída máxima limitada a 300 tokens, sem necessidade de quantização de 4 bits (que, segundo Lee et al., 2025, degradaria modelos sub-1B). Além disso, a Fase 0 do cronograma verifica exatamente esse carregamento local."

### Pergunta 6 — Por que o limite de saída foi fixado em exatamente 300 tokens? E se o estado verdadeiro $M_t^*$ do SUMIE tiver mais de 300 tokens?
- **Onde está no artigo:** Seção 3.3 (parágrafo 2), Seção 3.4 (parágrafo 3) e Seção 3.8 (alínea `b`).
- **Como responder tecnicamente:**
  > "O orçamento de 300 tokens segue diretamente o regime de memória restrita estabelecido por Hwang et al. (2024) ao propor o método GU-JSON no SUMIE. E para garantir que nenhuma transição exija um estado de referência $M_t^*$ impossível de caber nesse teto, a preparação dos dados e a **Fase 1 (estudo piloto)** verificam explicitamente o comprimento em tokens de todos os estados acumulados $M_t^*$ nos tokenizadores dos modelos avaliados."

### Pergunta 7 — Por que usar os testes de Friedman e Wilcoxon pareado em vez de ANOVA e teste t de Student?
- **Onde está no artigo:** Seção 3.8 (parágrafo 2).
- **Como responder tecnicamente:**
  > "Porque taxas e proporções restritas ao intervalo $[0, 1]$ — como *State F1*, *Preservation Accuracy* e *JSON Validity* — frequentemente apresentam distribuição assimétrica, concentração nos extremos (0 ou 1) e violação de normalidade. Como os três modelos são avaliados exatamente sobre o mesmo conjunto de entidades (amostras dependentes/pareadas), o teste não paramétrico de **Friedman** é o equivalente robusto à ANOVA de medidas repetidas para três condições, seguido pelo teste pareado de **Wilcoxon** com correção de **Holm-Bonferroni** para controlar o erro familiar nas comparações dois a dois, além dos intervalos de confiança de 95% via *bootstrap* em nível de entidade."

### Pergunta 8 — Se um modelo gerar um JSON inválido em 40% das transições, mas nas 60% válidas tiver um F1 alto, ele não pareceria melhor do que realmente é?
- **Onde está no artigo:** Seção 3.7 (último parágrafo) e Quadro 3.
- **Como responder tecnicamente:**
  > "Exatamente por esse motivo o nosso protocolo reporta todas as métricas semânticas sob **duas visões complementares** (Seção 3.7): a visão **condicional à validade estrutural**, que avalia a qualidade semântica pura quando o JSON é válido; e a visão **global (*end-to-end*)**, que atribui pontuação zero a qualquer transição com falha sintática ou de schema. Assim, um modelo que quebra o JSON em 40% dos casos será imediatamente penalizado na métrica global, sem mascarar sua instabilidade estrutural."

### Pergunta 9 — Qual é a diferença prática entre o método GU-JSON e o CoK-JSON (Chain-of-Key) proposto pelos mesmos autores? Por que você escolheu o GU-JSON?
- **Onde está no artigo:** Seção 2.2 (parágrafos 1 e 3) e Seção 5.
- **Como responder tecnicamente:**
  > "No *Chain-of-Key* (CoK-JSON), a atualização é decomposta em duas etapas: primeiro o modelo seleciona apenas quais chaves devem ser alteradas e depois atualiza somente essas chaves, enquanto um código externo mantém o restante do dicionário. Já no **GU-JSON**, o modelo precisa regenerar o objeto JSON completo em uma única chamada. Escolhemos o GU-JSON porque queremos testar justamente a capacidade do escritor compacto de **preservar atributos inalterados (`PRESERVE`) enquanto integra novidades (`ADD` e `UPDATE`)** sem depender de mesclagem programática externa."

### Pergunta 10 — Como a regra do SUMIE trata opiniões ou fatos conflitantes? Isso não confunde o modelo sobre quando substituir um valor?
- **Onde está no artigo:** Seção 2.3 (parágrafo 1), Seção 3.3 (regra 3 do prompt) e Apêndice A.
- **Como responder tecnicamente:**
  > "No SUMIE, as sequências sobre entidades incluem múltiplos pontos de vista e informações complementares, e a regra explícita do benchmark — refletida na Regra 3 do nosso prompt-base no Apêndice A — é **preservar perspectivas divergentes ainda válidas**, substituindo um valor anterior apenas quando a nova observação estabelecer explicitamente que ele deixou de ser válido. É por isso que, no SUMIE, a operação `UPDATE` avalia a integração de novas informações em um atributo existente, e deixamos cenários de substituição temporal estrita (*supersession*, como o FactConsolidation-SH) claramente delimitados como trabalho futuro."

---

## 6. Checklist Operacional de Ensaio e Postura (Para Executar Antes da Banca)

- [ ] **Ensaio 1 (Individual com cronômetro contínuo):** Apresentar do Slide 1 ao 15 com o cronômetro ligado sem parar nem zerar em caso de tropeço (`[00:16:03]` da aula). Verificar se o tempo total ficou entre **15 e 20 minutos** (meta: **18 minutos**).
- [ ] **Ensaio 2 (Gravação no PowerPoint com câmera e áudio):** Usar `Apresentação de Slides -> Gravar` no PowerPoint (`[00:18:03]`). Assistir à gravação observando:
  - Existência de vícios de linguagem (*"né"*, *"tá"*, *"então"*, *"tipo"*);
  - Velocidade de fala nos slides de metodologia (Slides 7 a 11);
  - Modulação da voz (destaque nas palavras em **negrito** do roteiro e pausas reais onde há `[PAUSA]`).
- [ ] **Ensaio 3 (Simulação de 3 Minutos — 3MT):** Cronometrar separadamente os 3 slides do arquivo [apresentacao_3mt_unitins.pptx](./apresentacao_3mt_unitins.pptx) para garantir fechamento em **~2m45s** sem acelerar a dicção.
- [ ] **Ambiente e Postura Online/Presencial:**
  - Câmera posicionada na **altura dos olhos** (usar apoio sob o notebook se necessário);
  - Ambiente silencioso, iluminação frontal e vestimenta alinhada (camisa/camiseta sóbria);
  - Combinar previamente com um colega da turma para **anotar todas as perguntas e sugestões da banca** durante os 10 minutos de arguição (`[00:44:02]`), permitindo foco total nas respostas técnicas.
