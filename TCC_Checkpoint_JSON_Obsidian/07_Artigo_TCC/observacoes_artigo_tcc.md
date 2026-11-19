# Relatório de Revisão Parágrafo por Parágrafo — Artigo de TCC (UNITINS)

- **Arquivo analisado:** `artigo_tcc_unitins_corrigido (1).pdf` (55 páginas, 248 itens/parágrafos extraídos)
- **Harness de revisão:** `ferramentas/RevisorArtigoTcc` (.NET 9 + `GitHub.Copilot.SDK`)
- **Modelo econômico utilizado:** `mai-code-2-flash` (chamadas à API: `0`, leituras de cache: `16`)
- **Referenciais de auditoria cruzada:**
  1. **Diagrama de Revisão do Texto / Cuidados Finais** (*Vieira, 2011 — A Arte da Escrita Técnica; Wazlawick — Metodologia de Pesquisa para Ciência da Computação*)
  2. **Acervo `artigos/05-metodologia-e-escrita-cientifica/`** (*Wazlawick UFOP/UFU; Zucolotto USP Módulos 1–8; Gerhardt & Silveira UFRGS 2009; Prodanov & Freitas Feevale 2013; TCCs Unitins*)
  3. **Checklist Oficial do TCC 1** (`Formulario-Checklist_para_o_texto_do_TCC1.pdf`)

## 1. Resumo Executivo e Estatísticas

| Métrica | Valor |
|---|---|
| Total de itens/parágrafos analisados (`#001` a `#248`) | **248** |
| Itens aprovados sem ressalvas (`✅ OK`) | **180** (72,6%) |
| Itens com recomendação de melhoria/concisão (`⚠️ AJUSTAR`) | **51** (20,6%) |
| Itens com falha crítica/editorial obrigatória (`❌ CRÍTICO`) | **17** (6,9%) |
| Obras únicas citadas no corpo × listadas nas Referências | **36** citadas / **36** nas Referências |
| Citações órfãs / Referências não citadas | **0** / **0** |

### Top 10 Correções Prioritárias (Obrigatórias antes da entrega)

1. **Remover marcadores residuais de comentários do Word (`[GS1]`, `[GS2]`, `[GS3]`, `[GS4]`):** presentes na Seção 2.7 (`#055`, `#057`, p. 16), no título do Quadro 1 (`#060`, p. 18) e no início da Seção 3 (`#066`, p. 21).
2. **Corrigir a frase truncada na Seção 3.1, alínea `c)` (`#071`, p. 22):** o item termina abruptamente em *"Quatro foram recuperados; Intrinsic Memory Agents (Yuen et al., 2025) e Supersede não foram"* (faltou *"recuperados."*).
3. **Corrigir o fragmento solto e a pontuação na Seção 3.1 (`#080`, p. 24):** remover o fragmento isolado *"Com isso."* após a nota de rodapé 3 e corrigir *"já triados ; Por isso,"* para *"já triados; por isso,"*.
4. **Corrigir numeração corrompida de alíneas (`#027` e `#076`):** na Introdução (`#027`, p. 10) está escrito `c)a) analisar o perfil de erro...`; na Seção 3.1 (`#076`, p. 23) está escrito `g) 7. Extração e síntese:`.
5. **Atualizar a paginação do Sumário (`#014`, p. 8):** no Sumário, a subseção `2.7 Comparação estatística de modelos` aparece com página `20`, antes de `2.8 Trabalhos relacionados` na página `16` (no texto, a seção 2.7 está na página 16).
6. **Corrigir artefato LaTeX na lista de Referências (`#201`, p. 48):** em `HWANG, Tao; DIAO, Yishi`, corrigir `AMU:Admission` (inserir espaço após dois-pontos) e `Conversations---Structured` (substituir `---` por travessão ou hífen com espaços).
7. **Corrigir enumeração sem conjunção na Seção 3.8 (`#132`, p. 36):** em *"a proporção de casos encaminhados ao juiz, a proporção de decisões incertas."*, inserir *"e"* antes do último item.
8. **Regularizar as 4 subfiguras da Figura 1 (`#116`–`#119`, p. 31–33):** as legendas *"Figura 1 — detalhe ampliado 1..4"* não constam na Lista de Ilustrações, não possuem linha `Fonte:` e não são chamadas nominalmente no texto da Seção 3.7.
9. **Inserir marcadores textuais (`X`) na Tabela 1 de Cronograma (`#182`–`#183`, p. 45):** as células das quinzenas Q1–Q20 usam apenas cor de fundo, ficando vazias na extração de texto e dificultando leitura em impressão monocromática.
10. **Explicitar o vínculo com Sistemas de Informação e vantagens/desvantagens no Quadro 1 (`#019`, `#060`–`#061`, `#066`):** no item `#066` (Seção 3), incluir *Sistemas de Informação* ao lado de Ciência da Computação (atendendo ao item 15 do Checklist TCC1) e destacar explicitamente vantagens/limitações das abordagens no Quadro 1 (item 10 do Checklist TCC1).

---

## 2. Avaliação contra `Formulario-Checklist_para_o_texto_do_TCC1.pdf`

| # | Item do Checklist | Descrição / Pergunta | Situação | Itens de Evidência | Observação Objetiva |
|---|---|---|---|---|---|
| 1 | **Título** | O título reflete com precisão o conteúdo do trabalho? | **Atende Parcialmente** | `#001, #002, #007` | O título ('Modelos de Linguagem Compactos como Escritores de Memória: Avaliação da Atualização Incremental de Estados JSON para Agentes') delimita bem o objeto, o método (JSON incremental) e o recorte (SLMs), com palavras-chave fortes (Zucolotto Mód. 1). Ressalva: por se tratar de projeto de TCC1 ainda sem resultados empíricos coletados, convém alinhar com o orientador se o subtítulo deve indicar 'Proposta/Protocolo de Avaliação' ou manter o título definitivo do TCC. |
| 2 | **Resumo** | O resumo fornece uma visão geral concisa, mas abrangente, da pesquisa e suas conclusões? | **Atende** | `#003..#010` | Resumo (#004) e Abstract (#008) seguem os movimentos de Aluísio/Zucolotto (Contexto, Lacuna, Propósito, Método GU-JSON/SUMIE e Critérios de Avaliação) em parágrafo único, voz ativa/terceira pessoa e com 4 palavras-chave separadas por ponto. |
| 3 | **Introdução** | A introdução declara claramente a questão de pesquisa e sua relevância? Ela inclui os objetivos do trabalho? | **Atende Parcialmente** | `#015..#028` | A Introdução afunila do contexto geral (#016-#017) ao problema do GU-JSON (#018), motivação para SLMs e paradigmas (#019), lacuna (#020), pergunta de pesquisa (#021), objetivo geral (#022-#023), objetivos específicos (#024-#027) e organização do artigo (#028). Porém, há erro tipográfico na alínea 'c)a)' (#027) e falta explicitar de forma mais direta o vínculo prático com Sistemas de Informação. |
| 4 | **Revisão de literatura** | A revisão de literatura é suficientemente detalhada e atualizada? Ela contextualiza a pesquisa dentro do campo de estudo? | **Atende Parcialmente** | `#029..#064` | Revisão altamente atualizada (2023–2026) cobrindo harness, memória estruturada, GU-JSON, SUMIE, geração restrita, paradigmas gerativos e testes estatísticos. Porém, a Seção 2.7 (#055-#057) contém marcadores residuais de comentário do Word ('[GS1]' e '[GS2]') e o Quadro 1 (#060) contém '[GS3]'. |
| 5 | **Metodologia** | A metodologia está claramente descrita? Os métodos usados são adequados para responder à questão de pesquisa? | **Atende Parcialmente** | `#065..#184` | Protocolo experimental rigoroso (variáveis no Quadro 3, hipóteses H0/H1, tuplas SUMIE, 3 escritores ~0,6B, juiz local Gemma 3 1B, 9 etapas do harness, métricas e testes de Friedman/Wilcoxon). Porém, há falhas editoriais críticas na Seção 3: marcador '[GS4]' (#066), frase truncada no item 'c)' (#071: '...não foram'), numeração 'g) 7.' (#076), fragmento solto 'Com isso.' e erro 'triados ; Por isso' (#080). Além disso, segundo Wazlawick, a revisão sistemática (Seção 3.1) deve ser claramente apresentada como etapa de fundamentação da lacuna, e não confundida com o método experimental em si. |
| 6 | **Resultados** | Os resultados estão claramente apresentados? Existem tabelas, gráficos ou outras representações visuais para apoiar a apresentação dos resultados? Não se espera para TCC1. | **Não Esperado (TCC1)** | `#158..#163` | Conforme indicado no próprio formulário ('Não se espera para TCC1'), o texto apresenta na Seção 3.12 (#158-#163) os 'Resultados e contribuições esperadas' vinculados aos objetivos específicos a, b e c, além da matriz de rastreabilidade no Quadro 6 (#150-#152). |
| 7 | **Discussão** | A discussão interpreta os resultados no contexto da questão de pesquisa e da literatura existente? Ela aponta limitações da pesquisa? Não se espera para TCC1. | **Não Esperado (TCC1)** | `#153..#157` | Não se espera discussão de resultados empíricos no TCC1, mas o trabalho já antecipa de forma exemplar na Seção 3.11 (#153-#157) as limitações metodológicas e ameaças à validade interna, de construção e externa. |
| 8 | **Conclusão** | A conclusão resume os principais pontos do trabalho e as principais descobertas? | **Atende** | `#185..#188` | A Seção 4 (Considerações Finais, #185-#188) faz o movimento inverso da Introdução (Específico -> Geral, conforme Zucolotto Mód. 4), retomando o problema, o protocolo proposto sobre o SUMIE, os limites de inferência e três desdobramentos futuros objetivos. |
| 9 | **Referências** | Todas as fontes mencionadas no texto estão corretamente citadas e listadas na seção de referências? | **Atende Parcialmente** | `#189..#225` | 100% de correspondência bidirecional: todas as 36 obras citadas no texto constam na lista de Referências e todas as 36 entradas de Referências são citadas no texto. Contudo, o item #201 (Hwang; Diao, 2026) apresenta falha de formatação ('AMU:Admission' sem espaço e travessão LaTeX bruto '---Structured'). |
| 10 | **Trabalhos relacionados** | Apresenta tabela descrevendo os trabalhos relacionados, vantagens, desvantagens e semelhanças de abordagens? | **Atende Parcialmente** | `#058..#064` | Apresenta o Quadro 1 (#060-#061) comparando 10 estudos da revisão sistemática mais a proposta em 5 colunas (Representação, Atualização, Modelos/escala, Objeto da avaliação, Compara paradigmas) e síntese nos parágrafos #063-#064. Porém, o Quadro 1 contém o marcador '[GS3]' na legenda (#060) e não rotula explicitamente 'vantagens e desvantagens' de cada abordagem como pede o checklist. |
| 11 | **Formatação** | O trabalho segue as diretrizes de formatação necessárias (ex.: ABNT, APA, etc.)? | **Não Atende** | `#014, #027, #055, #057, #060, #066, #076, #116..#119, #183, #201` | A estrutura geral segue o padrão ABNT/Unitins, mas há pendências formais impeditivas para entrega final: (1) Sumário (#014) com página errada na seção 2.7 (p. 20 antes da seção 2.8 na p. 16); (2) marcadores residuais '[GS1]' a '[GS4]'; (3) sublegendas 'Figura 1 — detalhe ampliado 1..4' (#116-#119) fora da Lista de Ilustrações e sem 'Fonte:'; (4) Tabela 1 de Cronograma (#183) sem marcadores textuais ('X') nas células Q1-Q20; (5) artefato '---' na referência #201. |
| 12 | **Gramática e Ortografia** | O texto foi revisado para possíveis erros gramaticais e ortográficos? | **Não Atende** | `#027, #071, #076, #080, #132` | A redação é culta e precisa na maior parte do texto, mas contém 5 erros objetivos de revisão: (1) alínea duplicada 'c)a)' na p. 10 (#027); (2) frase truncada no fim da alínea 'c)' na p. 22 (#071: '...e Supersede não foram'); (3) alínea 'g) 7.' na p. 23 (#076); (4) fragmento isolado 'Com isso.' e espaço antes de ponto e vírgula seguido de maiúscula 'triados ; Por isso' na p. 24 (#080); (5) enumeração sem conjunção 'e' em 'a proporção de casos encaminhados ao juiz, a proporção de decisões incertas.' na p. 36 (#132). |
| 13 | **Clareza de escrita** | O texto está claro e compreensível? Ele flui de maneira lógica e coerente? | **Atende Parcialmente** | `#016..#188` | O texto possui excelente precisão terminológica e encadeamento lógico entre seções, mas apresenta alguns períodos longos (> 48 palavras) que podem ser enxugados segundo o diagrama de Vieira (2011) e Zucolotto (Mód. 5 e 6), além dos truncamentos pontuais na Seção 3.1. |
| 14 | **Originalidade** | O trabalho é original e contribui de alguma forma para o campo de estudo? | **Atende** | `#020..#023, #063..#064, #158..#163` | A originalidade do recorte experimental é demonstrada pela revisão sistemática (158 registros no arXiv, 10 estudos no Quadro 1): nenhum estudo prévio combinou o método GU-JSON no benchmark SUMIE com a comparação controlada de três paradigmas gerativos (~0,6B: decoder-only, encoder-decoder e difusão em blocos) avaliando validade estrutural e fidelidade por operação. |
| 15 | **Relevância** | A pesquisa é relevante para a área de Sistemas de Informação? | **Atende Parcialmente** | `#016..#019, #066` | O problema (confiabilidade, custo computacional e latência de memória persistente em agentes locais) é altamente pertinente para Sistemas de Informação, mas o texto da Seção 3 (#066) declara um delineamento em 'Ciência da Computação' e nunca menciona explicitamente 'Sistemas de Informação' no corpo do artigo (apenas na Capa e Folha de Rosto). Recomenda-se explicitar o impacto para SI na Introdução e na Seção 3. |
| 16 | **Ética** | Se envolver pessoas ou animais, os procedimentos éticos foram seguidos? | **Atende** | `#066, #093, #099..#104` | A Seção 3 (#066) declara explicitamente que o experimento utiliza exclusivamente dados sintéticos públicos (SUMIE, Apache-2.0) e modelos de pesos abertos, sem envolver seres humanos ou dados pessoais, respeitando as licenças de uso. |

---

## 3. Avaliação contra o Diagrama (Mapa Mental: *Cuidados Finais / Revisão do Texto*)

| Eixo do Diagrama | Subitem do Mapa Mental | Diagnóstico no Artigo | Itens com Ocorrências / Evidências |
|---|---|---|---|
| **Propósito** | Garantir boa comunicação, melhorar compreensão e adaptar ao público-alvo | **Atende bem:** siglas e conceitos em inglês são traduzidos/explicados na 1ª ocorrência no Resumo e Introdução; a transição entre problema, método GU-JSON e métricas é didática. | `#004`, `#011`, `#014`–`#035` |
| **Localizar e destruir palavras** | **Geram ambiguidade:** *muitos, muito, muito grande, notável*, metáforas, analogias sem valor; usar números para precisar raciocínio | **Excelente precisão numérica geral** (0,6B, 1.200 tokens, 8.192 tokens, 4 GiB, 158 registros, 15/25 transições, α = 0,05). Pontos com quantificadores vagos (*muito, variados, diversos, bastante*) foram sinalizados para substituição ou precisão adicional. | `#037` (*variados*), `#043` (*muito longos*), `#049` (*múltiplas*), `#058` (*várias comparações*) |
| **Localizar e destruir palavras** | **Verborreia:** texto rebuscado e sem valor; textos longos e complicados | **Parcial:** não há adjetivação vazia nem metáforas, mas há **períodos com mais de 48 palavras** que acumulam muitas subordinadas e merecem divisão em duas frases diretas. | `#004`, `#016`, `#018`, `#021`, `#028`, `#040`, `#067`, `#069`, `#082`, `#087`, `#113`, `#125`, `#195` |
| **Imagens, tabelas e fórmulas** | Qualidade de leitura/construção, legenda autoexplicativa, obrigatoriedade de citar e explicar no texto | **Parcial:** Figuras 1 e 2, Quadros 1 a 7, Tabela 1 e Equações 1 a 6 são todos citados e explicados no texto. Porém: (1) Quadro 1 tem `[GS3]` na legenda (`#061`); (2) os 4 recortes `Figura 1 — detalhe ampliado 1..4` (`#117`–`#123`) não têm `Fonte:` nem citação individual no texto; (3) Tabela 1 (`#191`) marca quinzenas só com cor de fundo sem `X`. | `#039`–`#041`, `#061`–`#063`, `#079`–`#081`, `#084`–`#086`, `#115`–`#136`, `#141`–`#155`, `#161`–`#162`, `#190`–`#192`, `#238`–`#240` |
| **Leia todo o texto em voz alta** | Faz sentido o que está lendo? Esqueci algo importante? | **Falhas pontuais detectadas:** a leitura em voz alta revela imediatamente a frase incompleta no item `c)` (`#073`: *"...e Supersede não foram"*), o fragmento solto *"Com isso."* (`#082`), as alíneas `c)a)` (`#027`) e `g) 7.` (`#077`), a falta do `e` na enumeração (`#140`) e os marcadores `[GS1]`–`[GS4]`. | `#027`, `#056`, `#058`, `#061`, `#069`, `#073`, `#077`, `#082`, `#140` |
| **A introdução explica o que fez?** | Contextualização, Gap, Estado da arte, Propósito do trabalho, Estrutura do documento | **Atende integralmente os 5 elementos:** Contextualização (`#014`–`#016`), Motivação/SLMs (`#017`), Estado da arte + Gap (`#018`), Pergunta e Propósito/Objetivos (`#019`–`#027`), Estrutura do documento (`#028`). | `#014` a `#028` |
| **Cada seção e parágrafo é importante?** | Se remover um parágrafo ele faz falta? A sequência dos parágrafos e seções é adequada? | **Atende com 2 ressalvas estruturais:** cada parágrafo cumpre papel claro (sem gordura narrativa), mas (1) no Sumário (`#012`) a página da seção `2.7` está fora de ordem (`20` antes de `16`), e (2) na Seção `2.8` os parágrafos `#060` e `#065` repetem quase a mesma síntese de Hwang et al. (2024, 2025), Jayalath et al. (2025) e Geng et al. (2025) antes e depois do Quadro 1. | `#012`, `#060` vs `#065`, `#138` vs `#145` |
| **As conclusões concluem?** | Síntese do problema, contribuição do protocolo, limites de escopo e trabalhos futuros | **Atende (no escopo de TCC1):** a Seção 4 (`#193`–`#196`) sintetiza o problema, o desenho experimental proposto, as restrições de validade e os trabalhos futuros sem extrapolar resultados não coletados. | `#193`–`#196` |
| **Tenho todas as referências? Estão corretas?** | Toda obra citada está na referência? Toda obra da referência é citada? | **100% de paridade citação↔referência** (36 obras citadas = 36 obras listadas). Única correção formal na referência `#208` (`AMU:Admission` e `---Structured`). | `#197`–`#233` (destaque `#208`) |

---

## 4. Avaliação contra `artigos/05-metodologia-e-escrita-cientifica`

| Referência Metodológica | Critério / Princípio | Avaliação no Artigo e Parágrafos Relacionados |
|---|---|---|
| **Wazlawick (2009; UFOP; UFU Aula 3 e 5)** | **Escolha de objetivo verificável e distinção tema × objetivo:** usar verbos verificáveis (comparar, avaliar, analisar) ligados a hipótese testável; evitar 'fazer um estudo sobre' ou 'propor' vazio. | **Atende:** O objetivo geral (`#021`, *comparar*) e os específicos (`#025` *avaliar*, `#026` *comparar*, `#027` *analisar*) são estritamente mensuráveis pelas métricas do Quadro 5 e testáveis pelas hipóteses $H_0/H_1$ (`#088`). |
| **Wazlawick (UFU Aula 3, slides 16–18)** | **Problema em 3 partes e cuidado com 'não encontrei nada parecido':** enunciar a questão, demonstrar a lacuna pela literatura próxima e justificar a importância. | **Atende bem:** Em `#018` e `#066`–`#067`, o autor evita dizer que 'não existe nada parecido'; pelo contrário, demonstra que existem SLMs gestores de memória (Kang et al., 2026; Qiu et al., 2026) e comparações AR×difusão em 7B–8B (Lu et al., 2026), situando a lacuna na **interseção específica** (GU-JSON + SUMIE + 3 paradigmas ~0,6B + avaliação direta do estado), com ressalva explícita de escopo em `#082`. |
| **Wazlawick (UFU Aula 5, slide 9)** | **Revisão bibliográfica ≠ Método de pesquisa:** a revisão serve para definir o objetivo/lacuna e não deve ser confundida com o método de solução/experimento. | **Ponto de atenção (`#070`):** A revisão sistemática está alocada como Seção `3.1` dentro de `3 MATERIAIS E MÉTODOS`. Embora justificável por seguir protocolo formal de mapeamento (Petersen et al., 2015), recomenda-se explicitar na abertura da Seção 3.1 que ela é o método de seleção bibliográfica que sustenta a Seção 2.8, separando-a claramente do método experimental (Seções 3.2–3.9). |
| **Zucolotto (USP, Módulos 1 a 4)** | **Estrutura do Título, Abstract em 6 movimentos, Introdução em funil (Geral→Específico) e Conclusão piramidal (Específico→Geral).** | **Atende:** Resumo (`#004`) e Abstract (`#007`) cobrem os 6 movimentos (sendo resultados/conclusões substituídos pelos critérios de avaliação esperados do projeto de TCC1). Introdução (`#014`–`#028`) afunila em 5 movimentos até o propósito. Considerações Finais (`#193`–`#196`) partem do protocolo específico para as implicações e trabalhos futuros. |
| **Zucolotto (USP, Módulos 5 a 8)** | **Topic sentences, frases curtas, ação no verbo, evitar ambiguidade pronominal e redundâncias.** | **Atende parcialmente:** Os parágrafos possuem excelentes *topic sentences* iniciais (Mód. 8), mas há (1) **repetição entre `#060` e `#065`** na Seção 2.8 (antes e depois do Quadro 1) e entre `#138` e `#145` sobre o papel das Equações 5 e 6, e (2) **13 períodos acima de 48 palavras** que devem ser divididos para melhorar o ritmo de leitura (Mód. 5 e 6). |
| **Gerhardt & Silveira (UFRGS, 2009); Prodanov & Freitas (Feevale, 2013)** | **Classificação da pesquisa (natureza aplicada, abordagem quantitativa, procedimento experimental), variáveis e hipóteses.** | **Atende com ajuste de área (`#069`, `#083`–`#088`):** A classificação em `#069` (experimental, aplicada e quantitativa), o controle de variáveis no Quadro 3 (`#084`–`#085`) e as hipóteses $H_0/H_1$ (`#088`) estão rigorosamente alinhados a Prodanov & Freitas (2013) e Gerhardt & Silveira (2009). Apenas ajustar `#069` para vincular a pesquisa a **Sistemas de Informação**. |

---

## 5. Auditoria de Ilustrações, Quadros, Tabelas e Referências

### 5.1 Verificação de Ilustrações, Quadros e Tabelas (`[D-FIG]` / `[C-11]`)

| Elemento | Item / Página | Citado no Texto? | Possui `Fonte:`? | Na Lista Pré-Textual? | Diagnóstico |
|---|---|---|---|---|---|
| **Quadro 1** | `#060` (p. 19) | Sim | Sim | Sim | ⚠️ Contém marcador residual de comentário [GS]. |
| **Quadro 2** | `#077` (p. 24) | Sim | Sim | Sim | ✅ OK |
| **Quadro 3** | `#083` (p. 25) | Sim | Sim | Sim | ✅ OK |
| **Figura 1** | `#116` (p. 31) | Sim | Sim | Sim | ✅ OK |
| **Figura 1 (detalhe ampliado 1)** | `#118` (p. 32) | **Não** | **Não** | **Não** | ⚠️ Não citado nominalmente no corpo do texto. Sem indicação 'Fonte:' imediatamente após o elemento. Ausente na Lista de Ilustrações / Quadros e Tabelas. |
| **Figura 1 (detalhe ampliado 2)** | `#119` (p. 32) | **Não** | **Não** | **Não** | ⚠️ Não citado nominalmente no corpo do texto. Sem indicação 'Fonte:' imediatamente após o elemento. Ausente na Lista de Ilustrações / Quadros e Tabelas. |
| **Figura 1 (detalhe ampliado 3)** | `#120` (p. 33) | **Não** | **Não** | **Não** | ⚠️ Não citado nominalmente no corpo do texto. Sem indicação 'Fonte:' imediatamente após o elemento. Ausente na Lista de Ilustrações / Quadros e Tabelas. |
| **Figura 1 (detalhe ampliado 4)** | `#121` (p. 34) | **Não** | **Não** | **Não** | ⚠️ Não citado nominalmente no corpo do texto. Sem indicação 'Fonte:' imediatamente após o elemento. Ausente na Lista de Ilustrações / Quadros e Tabelas. |
| **Quadro 4** | `#124` (p. 35) | Sim | Sim | Sim | ✅ OK |
| **Figura 2** | `#128` (p. 36) | Sim | Sim | Sim | ✅ OK |
| **Quadro 5** | `#138` (p. 38) | Sim | Sim | Sim | ✅ OK |
| **Quadro 6** | `#150` (p. 41) | Sim | Sim | Sim | ✅ OK |
| **Tabela 1** | `#182` (p. 45) | Sim | Sim | Sim | ✅ OK |
| **Quadro 7** | `#231` (p. 53) | Sim | Sim | Sim | ✅ OK |

### 5.2 Verificação Cruzada de Citações × Referências (`[D-REF]` / `[C-09]`)

- **Total de obras únicas citadas no texto:** `36`
- **Total de obras listadas na seção REFERÊNCIAS:** `36`
- **Obras citadas no texto mas ausentes nas Referências:** **Nenhuma (0)** ✅
- **Obras nas Referências mas não citadas no texto:** **Nenhuma (0)** ✅
- **Alertas de formatação nas Referências:**
  - ❌ Item #201 (p. 49): 'HWANG, Tao; DIAO, Yishi. AMU:Admission and Memory Update for Personalized Conversatio...' contém '---' ou falta espaço após ':'.

---

## 6. Análise Parágrafo por Parágrafo / Item por Item (`#001` a `#248`)

Legenda de status: `✅ OK` (atende sem ressalvas) | `⚠️ AJUSTAR` (melhoria de concisão, estilo, clareza ou completude) | `❌ CRÍTICO` (erro gramatical, truncamento, marcador de comentário ou falha formal obrigatória).

### Seção: Capa

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#001` | 1 | `front_matter` | 40 (40) | ✅ OK | `C-01, C-11` | UNIVERSIDADE ESTADUAL DO TOCANTINS – UNITINS \| CAMPUS DE PALMAS – TO \| CURSO DE BACHARELADO EM SISTEMAS DE I... | Capa apresenta instituição, curso, autor, título, local e ano de forma adequada. |

### Seção: Folha de Rosto

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#002` | 2 | `front_matter` | 82 (75) | ✅ OK | `C-01, C-11` | UNIVERSIDADE ESTADUAL DO TOCANTINS – UNITINS CURSO DE BACHARELADO EM SISTEMAS DE INFORMAÇÃO \| GUILHERME HENRI... | Folha de rosto contém curso, autor, título, natureza, instituição, orientador, local e ano. |

### Seção: RESUMO

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#003` | 3 | `heading` | 1 (1) | ✅ OK | `D-PAR, C-11` | RESUMO | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#004` | 3 | `paragraph` | 237 (59) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, C-02` | Modelos de linguagem que operam em múltiplas etapas dependem de um estado persistente para registrar as inform... | [Regra D-VERB/M-ZUC] Período longo (59 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Há uma lacuna, objetivo, método, variáveis e métricas claros, mas uma sentença de 59 palavras prejudica a leitura. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir o primeiro período longo em frases menores, preferencialmente com até 45 palavras.* |
| `#005` | 3 | `paragraph` | 12 (4) | ✅ OK | `C-02` | Palavras-chave: Memória de agentes. Checkpoint JSON. Modelos de linguagem compactos. Sumarização incremental. | Palavras-chave são específicas e coerentes com o tema. |

### Seção: ABSTRACT

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#006` | 4 | `heading` | 1 (1) | ✅ OK | `D-PAR, C-11` | ABSTRACT | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#007` | 4 | `paragraph` | 213 (50) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, C-02` | Compact language models as memory writers: evaluating incremental updates of JSON checkpoints for agents Langu... | [Regra D-VERB/M-ZUC] Período longo (50 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Abstract apresenta lacuna, objetivo, método e avaliação, mas contém uma sentença de aproximadamente 50 palavras. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir o primeiro período em frases menores para melhorar fluidez e precisão.* |
| `#008` | 4 | `paragraph` | 10 (3) | ✅ OK | `C-02` | Keywords: Agent memory. JSON checkpoint. Small language models. Incremental summarization. | Keywords correspondem adequadamente ao conteúdo e à terminologia em inglês. |

### Seção: LISTA DE ILUSTRAÇÕES

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#009` | 5 | `front_matter_list` | 28 (28) | ✅ OK | `C-11, D-FIG` | LISTA DE ILUSTRAÇÕES Figura 1 – Visão geral do harness experimental para uma transição do SUMIE ...... 30 Figu... | Lista identifica todas as figuras, títulos e páginas de forma coerente. |

### Seção: LISTA DE QUADROS E TABELAS

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#010` | 6 | `front_matter_list` | 92 (92) | ✅ OK | `C-11, D-FIG` | LISTA DE QUADROS E TABELAS Quadro 1 – Comparação entre trabalhos relacionados e a proposta ...................... | Lista organiza quadros e tabela, com títulos e indicação de páginas. |

### Seção: LISTA DE ABREVIATURAS E SIGLAS

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#011` | 7 | `front_matter_list` | 86 (86) | ✅ OK | `C-11, D-REF` | LISTA DE ABREVIATURAS E SIGLAS ABNT – Associação Brasileira de Normas Técnicas AR – Autoregressivo (Autoregres... | Siglas estão definidas, em maioria com forma nacional e expansão em inglês. |

### Seção: SUMÁRIO

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#012` | 8 | `front_matter_list` | 203 (203) | ❌ CRÍTICO | `C-11, D-PAR, D-LEIT` | SUMÁRIO 1 INTRODUÇÃO ............................................................................................ | [Regra C-11/D-PAR] Numeração de página inconsistente no Sumário: a seção '2.7 Comparação estatística de modelos' indica página 20, enquanto '2.8 Trabalhos relacionados' indica página 16 (no corpo, a seção 2.7 inicia na página 16). \| A página 20 indicada para 2.7 e a página 16 indicada para 2.8 são incompatíveis com a ordem das seções. **Sugestão:** *Atualizar os campos do Sumário automático no Word antes da exportação para PDF. Corrigir a paginação e a sequência de 2.7 e 2.8 conforme o texto definitivo.* |

### Seção: 1 INTRODUÇÃO

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#013` | 9 | `heading` | 2 (2) | ✅ OK | `D-PAR, C-11` | 1 INTRODUÇÃO | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#014` | 9 | `paragraph` | 53 (31) | ✅ OK | `D-PAR, D-REF` | Agentes baseados em modelos de linguagem executam tarefas de múltiplas etapas, nas quais novas observações che... | Contextualização clara e pertinente; citações e articulação entre tarefa, memória e turnos estão coerentes. |
| `#015` | 9 | `paragraph` | 71 (39) | ✅ OK | `D-PAR, M-ZUC` | Nesses fluxos, a manutenção de um estado persistente e consistente condiciona diretamente a confiabilidade ope... | Estabelece relevância de estado persistente e conecta benchmarks ao problema de memória ao longo dos turnos. |
| `#016` | 9 | `paragraph` | 172 (58) | ❌ CRÍTICO | `D-VERB, M-ZUC` | Como o acúmulo irrestrito do histórico de interações rapidamente excede ou degrada o uso da janela de contexto... | [Regra D-VERB/M-ZUC] Período longo (58 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Há períodos excessivamente longos e densos, especialmente o último parágrafo, prejudicando leitura e separação de ideias. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir o texto em frases curtas: apresentar o problema GU-JSON, suas vantagens e, separadamente, suas possíveis falhas.* |
| `#017` | 9–10 | `paragraph` | 159 (60) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | Uma vez que a reescrita do checkpoint ocorre repetidamente a cada turno de interação, delegar essa operação a ... | [Regra D-VERB/M-ZUC] Período longo (60 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| O período sobre os três paradigmas é longo e acumula informações independentes. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar cada paradigma em frase própria e remover a repetição da expressão “modelos de linguagem”.* |
| `#018` | 10 | `paragraph` | 194 (38) | ⚠️ AJUSTAR | `D-PAR, M-WAZ` | Embora a literatura investigue separadamente a organização da memória em agentes (Jayalath et al., 2025; Yuen ... | Apresenta lacuna relevante, mas acumula demasiada revisão em um único parágrafo. **Sugestão:** *Separar a lacuna de cada contexto anteriormente estudado e finalizar com uma descrição direta da lacuna identificada.* |
| `#019` | 10–11 | `paragraph` | 47 (47) | ⚠️ AJUSTAR | `D-AMB, D-LEIT` | Diante dessa lacuna, este trabalho busca responder à seguinte pergunta de pesquisa: como representantes compac... | A pergunta contém uma quebra indevida em “decoder- only” e utiliza “qualidade” sem especificação imediata. **Sugestão:** *Reescrever como: “como … diferem na conformidade estrutural e na fidelidade factual ...?”* |
| `#020` | 11 | `paragraph` | 4 (4) | ✅ OK | `D-VERB, M-ZUC` | O objetivo geral é: | Introduz adequadamente o objetivo geral com formulação concisa. |
| `#021` | 11 | `paragraph` | 42 (42) | ⚠️ AJUSTAR | `M-WAZ, D-AMB` | comparar a qualidade da atualização incremental de checkpoints JSON produzida pelos modelos compactos Qwen3-0.... | O objetivo identifica variáveis e condições, mas “qualidade” permanece genérico sem métricas explícitas. **Sugestão:** *Substituir “qualidade” por “conformidade sintática, aderência ao esquema e fidelidade factual”.* |
| `#022` | 11 | `paragraph` | 6 (6) | ✅ OK | `D-VERB, M-ZUC` | Para alcançá-lo, definem-se três objetivos específicos: | Formulação clara que anuncia a enumeração dos objetivos específicos. |
| `#023` | 11 | `list_item` | 29 (29) | ✅ OK | `M-WAZ, M-MET` | a) avaliar a conformidade estrutural dos checkpoints produzidos por cada escritor a partir das taxas de valida... | Objetivo específico verificável, com taxas de validade sintática e aderência ao esquema como métricas. |
| `#024` | 11 | `list_item` | 28 (28) | ✅ OK | `M-WAZ, M-MET, C-05` | b) comparar a fidelidade do estado mantido por cada escritor ao longo dos turnos de atualização do SUMIE, util... | Objetivos mensuráveis e métricas pertinentes estão explicitamente definidos. |
| `#025` | 11 | `list_item` | 31 (31) | ❌ CRÍTICO | `C-12, D-LEIT` | c)a) analisar o perfil de erro dos escritores segundo o tipo de operação exigida no SUMIE, contrastando a pres... | [Regra C-12/D-LEIT] Numeração de alínea corrompida ou duplicada no início do item ('c)a)'). \| A marcação inicial “c)a)” está corrompida e impede identificar corretamente o item da lista. **Sugestão:** *Corrigir o marcador de lista 'c)a)' para manter apenas a alínea correta ('c)' ou 'g)'). Substituir “c)a)” por “c)”.* |
| `#026` | 11 | `paragraph` | 66 (66) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, D-LEIT, D-INTRO` | O restante deste artigo está organizado da seguinte forma: a seção 2 apresenta a revisão bibliográfica sobre h... | [Regra D-VERB/M-ZUC] Período longo (66 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| O período único acumula 66 palavras e três tarefas de estruturação, prejudicando a fluidez. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir em dois ou três períodos curtos: uma frase para as seções 2 e 3, outra para a seção 4.* |

### Seção: 2 REFERENCIAL TEÓRICO

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#027` | 11 | `heading` | 3 (3) | ✅ OK | `D-PAR, C-11` | 2 REFERENCIAL TEÓRICO | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#028` | 11–12 | `paragraph` | 63 (39) | ✅ OK | `D-PAR, D-INTRO, C-04` | A compreensão da escrita de memória exige situá-la na arquitetura mais ampla do harness e examinar decisões so... | O parágrafo apresenta claramente a abrangência da revisão e prepara a subsequente exposição temática. |

### Seção: 2.1 Harness de agentes e gerenciamento de memória

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#029` | 12 | `heading` | 9 (9) | ✅ OK | `D-PAR, C-11` | 2.1 Harness de agentes e gerenciamento de memória | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#030` | 12 | `paragraph` | 41 (29) | ✅ OK | `M-ZUC, D-PAR, C-04` | Neste trabalho, um harness de agentes é definido operacionalmente como a camada de software que envolve o mode... | Define operacionalmente o conceito central e mantém progressão direta entre suas funções. |
| `#031` | 12 | `paragraph` | 67 (31) | ✅ OK | `D-PAR, D-REF, C-04` | O gerenciamento de memória integra essa camada ao organizar informações que podem ser úteis em interações post... | Explica geração, atualização e recuperação com transição lógica e atribuição de fontes adequada. |
| `#032` | 12 | `paragraph` | 45 (23) | ✅ OK | `M-WAZ, D-PAR, C-04` | Neste trabalho, investiga-se apenas a escrita incremental da memória, sem avaliar os métodos de recuperação ne... | Delimita claramente o escopo da investigação e evita confundir harness experimental com método de recuperação. |

### Seção: 2.2 Representação estruturada da memória

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#033` | 12 | `heading` | 6 (6) | ✅ OK | `D-PAR, C-11` | 2.2 Representação estruturada da memória | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#034` | 12–13 | `paragraph` | 94 (73) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, C-04` | A escolha do formato de armazenamento condiciona a capacidade do agente de reter e consultar informações ao lo... | [Regra D-VERB/M-ZUC] Período longo (73 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Uma sentença de 73 palavras acumula síntese, comparação e ressalva, prejudicando a leitura técnica. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar a síntese da comparação da ressalva em períodos curtos e independentes.* |
| `#035` | 13 | `paragraph` | 129 (41) | ✅ OK | `D-PAR, D-REF, C-04` | Sistemas voltados à persistência de estado ao longo de múltiplas etapas adotam mecanismos variados para estrut... | Apresenta arquiteturas distintas em períodos claros, com referências completas e função comparativa consistente. |
| `#036` | 13 | `paragraph` | 69 (46) | ⚠️ AJUSTAR | `D-VERB, D-PAR, C-04` | Em conjunto, esses estudos demonstram que o formato de representação da memória e o mecanismo empregado para a... | O primeiro período tem 46 palavras e concentra a conclusão comparativa, tornando-a menos imediata. **Sugestão:** *Dividir após “de projeto.” e iniciar o segundo período com “As abordagens...”* |

### Seção: 2.3 Atualização incremental e o método Generate-Update em JSON

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#037` | 13 | `heading` | 10 (10) | ✅ OK | `D-PAR, C-11` | 2.3 Atualização incremental e o método Generate-Update em JSON | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#038` | 13 | `paragraph` | 84 (44) | ✅ OK | `D-REF, C-04, C-10` | Hwang et al. (2024) investigaram a manutenção de resumos incrementais sob orçamento restrito de memória, compa... | Apresenta de forma clara o estudo comparativo, os datasets, os modelos e os achados principais. |
| `#039` | 14 | `paragraph` | 29 (29) | ✅ OK | `D-INTRO, D-FIG, M-ZUC` | No método GU-JSON, a cada nova observação o modelo escritor recebe o esquema, o checkpoint corrente e a observ... | Introduz de maneira direta o método e prepara corretamente a apresentação da Equação 1. |
| `#040` | 14 | `equation` | 2 (2) | ✅ OK | `D-FIG, M-MET` | 𝑀𝑡= 𝐺(𝑆, 𝑀𝑡−1, 𝑂𝑡) (1) | Fórmula numerada, integrada à explicação das variáveis no parágrafo adjacente e coerente com as métricas do protocolo. |
| `#041` | 14 | `paragraph` | 23 (23) | ✅ OK | `D-FIG, M-ZUC` | em que 𝑆 é o esquema, 𝑀𝑡−1 é o checkpoint anterior, 𝑂𝑡 é a nova observação, 𝐺 é o modelo escritor e 𝑀𝑡... | Explica todas as variáveis da equação de forma concisa e inequívoca. |
| `#042` | 14 | `paragraph` | 94 (41) | ✅ OK | `M-ZUC, M-WAZ, C-13` | Para a comparação entre modelos escritores compactos, o GU-JSON apresenta uma propriedade metodológica central... | Argumenta com clareza a vantagem metodológica da reescrita integral em uma única chamada ao modelo. |

### Seção: 2.4 Avaliação de memória e de atualização de conhecimento

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#043` | 14 | `heading` | 10 (10) | ✅ OK | `D-PAR, C-11` | 2.4 Avaliação de memória e de atualização de conhecimento | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#044` | 14 | `paragraph` | 117 (50) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, D-PAR` | O benchmark SUMIE foi desenvolvido especificamente para avaliar a sumarização incremental de entidades a parti... | [Regra D-VERB/M-ZUC] Período longo (50 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A primeira frase possui 50 palavras e acumula informação suficiente para duas frases. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Divida após “pontos de vista divergentes”: uma frase para o benchmark e outra para as anotações.* |
| `#045` | 15 | `paragraph` | 81 (36) | ⚠️ AJUSTAR | `D-AMB, M-ZUC` | Outros benchmarks recentes examinam a memória sob interações de múltiplos turnos, porém com foco na resposta a... | [Regra D-AMB/M-ZUC] Uso de qualificadores/quantificadores potencialmente vagos ou subjetivos ('muito'). O diagrama recomenda substituir termos vagos por números ou especificações precisas. \| “Diálogos muito longos” é subjetivo e não permite dimensionar a propriedade avaliada. **Sugestão:** *Substituir o quantificador vago por dado quantitativo, intervalo numérico ou qualificação técnica precisa. Informe o número aproximado de turnos, mensagens, sessões ou tokens usados pelo LoCoMo.* |
| `#046` | 15 | `paragraph` | 67 (36) | ✅ OK | `D-PAR, M-ZUC, M-MET` | A análise conjunta desses benchmarks revela que avaliações baseadas apenas em respostas finais podem mascarar ... | Conecta a lacuna das avaliações finais às inspeções separadas de preservação, adição e atualização. |

### Seção: 2.5 Geração estruturada: validade sintática e conformidade com esquema

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#047` | 15 | `heading` | 10 (10) | ✅ OK | `D-PAR, C-11` | 2.5 Geração estruturada: validade sintática e conformidade com esquema | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#048` | 15 | `paragraph` | 116 (32) | ✅ OK | `C-04, C-10, D-REF` | A utilização de JSON como formato de estado exige distinguir a correção formal da saída de sua correção semânt... | Distingue validade sintática e semântica e relaciona estudos sobre falhas e decodificação restrita. |
| `#049` | 15–16 | `paragraph` | 107 (48) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | Na avaliação de escritores de memória, essa literatura impõe dois cuidados experimentais. Primeiro, a conformi... | Uma das sentenças acumula 48 palavras e duas condições experimentais em uma estrutura extensa. **Sugestão:** *Separe a segunda condição em duas frases: uma sobre motores de decodificação e outra sobre o regime prompt-only.* |

### Seção: 2.6 Paradigmas gerativos e modelos de linguagem compactos

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#050` | 16 | `heading` | 9 (9) | ✅ OK | `D-PAR, C-11` | 2.6 Paradigmas gerativos e modelos de linguagem compactos | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#051` | 16 | `paragraph` | 109 (49) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | Os três paradigmas gerativos considerados neste estudo processam a relação entre entrada e saída sob princípio... | [Regra D-VERB/M-ZUC] Período longo (49 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A sentença final possui 49 palavras e combina arquitetura, adaptação e finalidade em excesso. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separe o modelo T5Gemma em uma frase própria após explicar a arquitetura encoder-decoder.* |
| `#052` | 16 | `paragraph` | 76 (43) | ✅ OK | `D-PAR, D-VERB, D-REF` | Já os modelos de linguagem baseados em difusão formulam a geração como um processo iterativo de remoção de ruí... | Explica de forma clara e tecnicamente coerente os mecanismos difusivo, autoregressivo e híbrido, com fontes nas afirmações. |
| `#053` | 16–17 | `paragraph` | 83 (42) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, M-WAZ` | O recorte em modelos compactos fundamenta-se na viabilidade de executá-los localmente com menor custo energéti... | A justificativa do recorte é pertinente, mas o parágrafo poderia declarar diretamente o método requerido pela variável de precisão numérica. **Sugestão:** *Dividir em parágrafos e explicitar como precisão, hardware e inferência serão controlados ou documentados.* |

### Seção: 2.7 Comparação estatística de modelos

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#054` | 17 | `heading` | 6 (6) | ✅ OK | `D-PAR, C-11` | 2.7 Comparação estatística de modelos | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#055` | 17 | `paragraph` | 58 (25) | ❌ CRÍTICO | `C-11, D-LEIT` | [GS1]O teste de Friedman é um método não paramétrico utilizado para comparar três ou mais modelos avaliados na... | [Regra C-11/D-LEIT] Marcador residual de comentário de revisão do Word exportado no PDF ([GS1]). \| O marcador residual “[GS1]” é um artefato de revisão que compromete a apresentação formal do texto. **Sugestão:** *Remover o marcador [GS1] antes de exportar o documento final. Remover “[GS1]” antes da primeira palavra.* |
| `#056` | 17 | `paragraph` | 65 (20) | ✅ OK | `D-PAR, M-MET, D-LEIT` | O teste de Wilcoxon pareado compara dois modelos usando as diferenças entre seus resultados nas mesmas unidade... | A explicação é precisa, distingue pressupostos e unidades independentes e mantém sequência lógica clara. |
| `#057` | 17 | `paragraph` | 74 (37) | ❌ CRÍTICO | `C-11, D-LEIT, D-AMB, M-ZUC, D-VERB` | O valor p expressa, sob a hipótese nula e os pressupostos do teste, a probabilidade de obter um resultado tão ... | [Regra C-11/D-LEIT] Marcador residual de comentário de revisão do Word exportado no PDF ([GS2]). \| [Regra D-AMB/M-ZUC] Uso de qualificadores/quantificadores potencialmente vagos ou subjetivos ('várias'). O diagrama recomenda substituir termos vagos por números ou especificações precisas. \| Há o marcador residual “[GS2]”, além do termo “várias” que não especifica a quantidade de comparações. **Sugestão:** *Remover o marcador [GS2] antes de exportar o documento final. Substituir o quantificador vago por dado quantitativo, intervalo numérico ou qualificação técnica precisa. Remover “[GS2]” e substituir “várias” pelo número de comparações do protocolo.* |

### Seção: 2.8 Trabalhos relacionados

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#058` | 17 | `heading` | 4 (4) | ✅ OK | `D-PAR, C-11` | 2.8 Trabalhos relacionados | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#059` | 17–18 | `paragraph` | 144 (32) | ⚠️ AJUSTAR | `D-VERB, D-PAR, C-10, D-REF` | O levantamento bibliográfico anterior à revisão sistemática identificou estudos que definem os fundamentos des... | O parágrafo é longo e acumula sete trabalhos sem estabelecer contrastes claros de vantagens, limitações e semelhanças. **Sugestão:** *Separar os fundamentos dos trabalhos e organizar uma síntese comparativa antes da menção ao quadro.* |
| `#060` | 19 | `caption` | 10 (10) | ❌ CRÍTICO | `C-11, D-LEIT` | Quadro 1 – Comparação entre trabalhos relacionados e a proposta[GS3] | [Regra C-11/D-LEIT] Marcador residual de comentário de revisão do Word exportado no PDF ([GS3]). \| A legenda contém o marcador residual “[GS3]”, inadequado para a versão final do TCC. **Sugestão:** *Remover o marcador [GS3] antes de exportar o documento final. Remover “[GS3]” e revisar a legenda para torná-la autoexplicativa.* |
| `#061` | 19–20 | `table` | 444 (297) | ❌ CRÍTICO | `C-10, D-FIG, C-11` | Trabalho Representação da memória \| Atualização Modelos e escala Objeto da avaliação Compara \| paradigmas ge... | [Regra C-10] O Quadro 1 compara representação, atualização, modelos/escala, objeto de avaliação e comparação de paradigmas, mas o Checklist do TCC1 pergunta especificamente por 'vantagens, desvantagens e semelhanças de abordagens'. \| A tabela não apresenta explicitamente vantagens e desvantagens das abordagens, requisito específico do checklist. **Sugestão:** *Explicitar na coluna de avaliação/atualização ou no parágrafo de síntese do Quadro 1 as vantagens e limitações/desvantagens diretas de cada abordagem frente ao GU-JSON. Adicionar colunas ou sínteses de semelhanças, vantagens e desvantagens e corrigir a disposição de colunas.* |
| `#062` | 20 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |
| `#063` | 21 | `paragraph` | 88 (40) | ⚠️ AJUSTAR | `D-PAR, C-10, D-VERB` | O estudo fundacional de Hwang et al. (2024) validou o GU-JSON com modelos Gemini de grande porte, assim como H... | A síntese é clara, mas reduz os trabalhos a fundamentos e não explicita diferenças relevantes entre suas abordagens. **Sugestão:** *Acrescentar semelhanças e distinções diretamente relacionadas à combinação central da pesquisa.* |
| `#064` | 21 | `paragraph` | 215 (37) | ⚠️ AJUSTAR | `D-VERB, D-PAR, M-WAZ, C-10` | O Quadro 1 mostra que a revisão sistemática identificou dez estudos recentes próximos da proposta. Modelos de ... | A síntese identifica lacuna e propósito, mas o parágrafo extenso acumula dados e pode dificultar a leitura. **Sugestão:** *Separar evidência comparativa, lacuna não atendida e contribuição específica desta pesquisa.* |

### Seção: 3 MATERIAIS E MÉTODOS

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#065` | 22 | `heading` | 4 (4) | ✅ OK | `D-PAR, C-11` | 3 MATERIAIS E MÉTODOS | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#066` | 22 | `paragraph` | 118 (78) | ❌ CRÍTICO | `C-11, D-LEIT, D-VERB, M-ZUC, C-15, M-WAZ` | Este estudo segue um delineamento experimental, aplicado e quantitativo em Ciência da Computação, comparando o... | [Regra C-11/D-LEIT] Marcador residual de comentário de revisão do Word exportado no PDF ([GS4]). \| [Regra D-VERB/M-ZUC] Período longo (78 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| [Regra C-15/M-WAZ] O parágrafo situa o delineamento apenas em 'Ciência da Computação', mas o curso e o Checklist do TCC1 exigem explicitar a relevância para a área de Sistemas de Informação (SI). \| Contém marcador residual do Word, período excessivamente longo e não situa a relevância específica em Sistemas de Informação. **Sugestão:** *Remover o marcador [GS4] antes de exportar o documento final. Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Explicitar o vínculo com Sistemas de Informação (ex.: confiabilidade e custo operacional de sistemas de informação baseados em agentes com memória persistente local). Remover “[GS4]”, dividir em períodos curtos e acrescentar a contribuição do estudo para SI.* |

### Seção: 3.1 Revisão sistemática da literatura

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#067` | 22 | `heading` | 6 (6) | ⚠️ AJUSTAR | `M-WAZ, D-PAR` | 3.1 Revisão sistemática da literatura | [Regra M-WAZ/D-PAR] Wazlawick destaca que a revisão bibliográfica não deve ser confundida com o método de pesquisa em si (pois é etapa prévia para delimitar a lacuna e o objetivo), embora mapeamentos sistemáticos com protocolo formal costumem ser detalhados em seção própria ou apêndice. **Sugestão:** *Esclarecer logo no início da Seção 3.1 que a revisão sistemática constitui o procedimento auxiliar de delimitação da lacuna (Seção 2.8), distinguindo-a do método experimental principal (Seções 3.2–3.9).* |
| `#068` | 22 | `paragraph` | 78 (36) | ✅ OK | `M-WAZ, M-ZUC` | Os trabalhos relacionados apresentados no Quadro 1 e a lacuna enunciada na introdução foram delimitados por um... | Delimita claramente o tipo de revisão e apresenta uma sequência metodológica coerente. |
| `#069` | 22 | `list_item` | 83 (31) | ✅ OK | `M-WAZ, M-ZUC` | a) Planejamento e protocolo: antes da busca, foram registrados em arquivo versionado a questão orientadora, a ... | Apresenta protocolo, questão orientadora e janela temporal com informações suficientes para verificar o procedimento. |
| `#070` | 23 | `list_item` | 47 (27) | ✅ OK | `M-WAZ, D-LEIT` | b) Fonte e consultas: a busca foi realizada na API do repositório arXiv,1 nos campos de título e resumo, com t... | Descrição da fonte e das consultas é objetiva e remete corretamente ao quadro de consultas. |
| `#071` | 23 | `list_item` | 37 (23) | ❌ CRÍTICO | `D-LEIT, C-12` | c) Estudos de controle: seis estudos já conhecidos e pertinentes foram usados para diagnosticar perdas das con... | [Regra D-LEIT/C-12] Frase truncada / incompleta no final do item (termina abruptamente em: '...nts (Yuen et al., 2025) e Supersede não foram'). \| O item termina antes de completar a análise dos dois estudos de controle mencionados. **Sugestão:** *Completar a oração truncada e encerrar com pontuação adequada (ex.: 'não foram recuperados;'). Concluir a frase, indicando por que Intrinsic Memory Agents e Supersede não foram recuperados.* |
| `#072` | 23 | `list_item` | 21 (21) | ✅ OK | `M-WAZ, D-LEIT` | d) Deduplicação: os registros das seis consultas foram unidos pelo identificador do arXiv, resultando em 158 c... | A deduplicação está quantificada e o procedimento de identificação é explícito. |
| `#073` | 23 | `list_item` | 127 (42) | ⚠️ AJUSTAR | `D-VERB, D-LEIT, M-WAZ` | e) Triagem por título e resumo: cada candidato foi classificado em uma de três categorias. Núcleo (CORE) exigi... | O item reúne muitos conceitos em períodos extensos e pode dificultar a leitura técnica. **Sugestão:** *Dividir a descrição dos critérios, da classificação automática e dos resultados em frases menores.* |
| `#074` | 23 | `footnote` | 19 (19) | ✅ OK | `C-11` | 1 Disponível em: https://info.arxiv.org/help/api/index.html. 2 Disponível em: https://github.com/github/copilo... | Nota de rodapé informativa com URL pública de repositório/artefato técnico. |
| `#075` | 23–24 | `list_item` | 103 (37) | ✅ OK | `M-WAZ, D-REF` | f) Elegibilidade com consulta ao texto: todos os 13 estudos de núcleo e seis estudos de contexto escolhidos po... | Apresenta elegibilidade, reclassificação, critérios e totalização final de forma rastreável. |
| `#076` | 24 | `list_item` | 73 (33) | ❌ CRÍTICO | `C-12, D-LEIT, C-11` | g) 7. Extração e síntese: de cada estudo selecionado foram extraídos a representação da memória, o mecanismo d... | [Regra C-12/D-LEIT] Numeração de alínea corrompida ou duplicada no início do item ('g) 7.'). \| A numeração “g) 7.” está corrompida e cria ambiguidade na sequência da metodologia. **Sugestão:** *Corrigir o marcador de lista 'g) 7.' para manter apenas a alínea correta ('c)' ou 'g)'). Padronizar o marcador como “g) Extração e síntese:”.* |
| `#077` | 24 | `caption` | 8 (8) | ✅ OK | `D-FIG, C-11` | Quadro 2 – Consultas da revisão sistemática no arXiv | A legenda identifica corretamente o quadro e seu conteúdo temático. |
| `#078` | 24 | `table` | 101 (101) | ⚠️ AJUSTAR | `D-FIG, C-10, D-REF` | Consulta Faceta buscada Registros \| F1 Memória estruturada ou estado de entidades com atualização incremental... | A tabela apresenta dados brutos sem fonte, nota metodológica ou explicação das facetas. **Sugestão:** *Adicionar legenda, explicação da consulta e identificação da base bibliográfica.* |
| `#079` | 25 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |
| `#080` | 25 | `paragraph` | 124 (55) | ❌ CRÍTICO | `D-LEIT, C-12, D-VERB, M-ZUC` | Os artefatos da revisão — protocolo, roteiro de triagem, scripts em C# (.NET 10), expressões completas das con... | [Regra D-LEIT/C-12] Fragmento de frase isolado e sem predicado ('Com isso.') no meio do parágrafo. \| [Regra C-12] Espaço indevido antes de sinal de pontuação (ex.: 'triados ; Por isso') e inicial maiúscula após ponto e vírgula. \| [Regra D-VERB/M-ZUC] Período longo (55 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Há fragmento isolado, erro de pontuação, maiúscula indevida e período excessivamente longo. **Sugestão:** *Remover o fragmento solto 'Com isso.' ou integrá-lo sintaticamente à oração seguinte. Remover o espaço antes do ponto e vírgula e grafar 'por isso' com inicial minúscula (ou usar ponto final). Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Reescrever em períodos curtos e separar as limitações em frases completas.* |

### Seção: 3.2 Desenho experimental e variáveis

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#081` | 25 | `heading` | 6 (6) | ✅ OK | `D-PAR, C-11` | 3.2 Desenho experimental e variáveis | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#082` | 25 | `paragraph` | 37 (37) | ✅ OK | `M-MET, M-ZUC, D-PAR` | O experimento manipula como única variável independente o modelo escritor (memory writer) e mantém constantes ... | Define claramente variável independente, controladas e dependentes conforme o desenho citado. |
| `#083` | 25 | `caption` | 5 (5) | ✅ OK | `D-FIG, C-11` | Quadro 3 – Variáveis do experimento | A legenda é breve, específica e identifica o conteúdo do quadro. |
| `#084` | 25 | `footnote` | 12 (12) | ✅ OK | `C-11` | 3 Disponível em: https://github.com/guisiq/tcc_revisao_sistematica_sumarizacao_recorrente/tree/v1.0.0. | Nota de rodapé informativa com URL pública de repositório/artefato técnico. |
| `#085` | 25–26 | `table` | 177 (163) | ⚠️ AJUSTAR | `D-FIG, D-VERB, C-13` | Tipo Variável Operacionalização \| Independente Modelo escritor Qwen3-0.6B (autoregressivo decoder-only); T5Ge... | O quadro é amplo e repete cabeçalho no texto extraído, dificultando leitura e hierarquização. **Sugestão:** *Separar tipos em seções visuais claras e distribuir variáveis controladas em linhas uniformes.* |
| `#086` | 26 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |
| `#087` | 26 | `paragraph` | 78 (78) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, M-WAZ` | O desenho experimental responde à questão principal de pesquisa — como os três representantes compactos difere... | [Regra D-VERB/M-ZUC] Período longo (78 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| O período possui 78 palavras e combina objetivo principal com duas questões analíticas. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar o objetivo das duas questões em parágrafos ou períodos curtos.* |
| `#088` | 26–27 | `paragraph` | 87 (46) | ✅ OK | `M-MET, M-ZUC, D-CONC` | Para orientar o teste empírico, formula-se a hipótese nula (𝐻0) de que não há diferença estatisticamente sign... | Formula hipóteses nula e alternativa, ligando-as às métricas primárias e ao protocolo. |

### Seção: 3.3 Método de memória, esquema e prompt

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#089` | 27 | `heading` | 8 (8) | ✅ OK | `D-PAR, C-11` | 3.3 Método de memória, esquema e prompt | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#090` | 27 | `paragraph` | 61 (47) | ✅ OK | `M-MET, D-FIG, M-ZUC` | Em cada transição do experimento, aplica-se a formulação do GU-JSON (Equação 1) com 𝑀𝑡−1 = 𝑀𝑡−1∗: o escrit... | Explica a transição, entradas e exclusividade da saída; contém uma referência clara à Equação 1. |
| `#091` | 27 | `paragraph` | 122 (62) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, C-13` | Adota-se o esquema mínimo {"state": {"chave": "valor"}}, no qual os atributos da entidade descrita no SUMIE sã... | [Regra D-VERB/M-ZUC] Período longo (62 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Um período acumula seis instruções e totaliza 62 palavras. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar o esquema, as seis instruções e o orçamento em blocos ou frases distintas.* |

### Seção: 3.4 Conjunto de dados e preparação das transições

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#092` | 27 | `heading` | 9 (9) | ✅ OK | `D-PAR, C-11` | 3.4 Conjunto de dados e preparação das transições | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#093` | 27 | `paragraph` | 46 (46) | ⚠️ AJUSTAR | `D-REF, C-12, D-LEIT` | O experimento utiliza o benchmark SUMIE (Hwang et al., 2025), disponibilizado publicamente sob licença Apache-... | A licença e a referência são úteis, mas “Apache-2.0.4” sugere artefato de nota ou pontuação mal formada. **Sugestão:** *Corrigir a referência do benchmark e posicionar a chamada de nota separadamente.* |
| `#094` | 27 | `footnote` | 8 (8) | ✅ OK | `C-11` | 4 Disponível em: https://github.com/google-deepmind/sumie. | Nota de rodapé informativa com URL pública de repositório/artefato técnico. |
| `#095` | 27–28 | `paragraph` | 72 (55) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | Para viabilizar a avaliação direta de transições de estado sob o método GU- JSON, cada etapa 𝑡 de uma entidad... | [Regra D-VERB/M-ZUC] Período longo (55 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A primeira frase soma 55 palavras e acumula definições e subordinadas. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir após a tupla: definir X, O e X* em frases próprias; depois explicar a classificação.* |
| `#096` | 28 | `list_item` | 20 (20) | ✅ OK | `M-ZUC, C-05` | a) PRESERVE: atributo já presente em 𝑀𝑡−1∗ cujo valor não sofre alteração na observação 𝑂𝑡 e deve ser mant... | A definição é específica e concentra uma única operação de transição. |
| `#097` | 28 | `list_item` | 13 (13) | ✅ OK | `M-ZUC, C-05` | b) ADD: atributo ausente em 𝑀𝑡−1∗ e introduzido pela primeira vez na observação 𝑂𝑡; | A definição identifica claramente o atributo ausente e sua introdução. |
| `#098` | 28 | `list_item` | 31 (31) | ✅ OK | `M-ZUC, C-05` | c) UPDATE: atributo já existente em 𝑀𝑡−1∗ que recebe informação complementar ou nova perspectiva apresentada... | A descrição distingue UPDATE de PRESERVE e vincula a operação à regra do SUMIE. |
| `#099` | 28 | `paragraph` | 89 (34) | ✅ OK | `M-WAZ, M-ZUC, C-05` | Durante a preparação dos dados no estudo piloto, são definidas regras de normalização textual que incluem espa... | O parágrafo apresenta regras, justificativa de controle e aplicação consistente aos dados. |

### Seção: 3.5 Modelos avaliados

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#100` | 28 | `heading` | 4 (4) | ✅ OK | `D-PAR, C-11` | 3.5 Modelos avaliados | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#101` | 28 | `paragraph` | 29 (29) | ⚠️ AJUSTAR | `D-AMB, M-WAZ, C-05` | Os três modelos escritores foram selecionados para representar paradigmas gerativos distintos mantendo escala ... | A expressão “escala aproximada” (~0,6 bilhão) reduz a precisão de seleção replicável. **Sugestão:** *Informar a contagem exata ou parametrizações aproximadas de cada modelo.* |
| `#102` | 28 | `footnote` | 9 (9) | ✅ OK | `C-11` | 5 Disponível em: https://huggingface.co/Qwen/Qwen3-0.6B. | Nota de rodapé informativa com URL pública de repositório/artefato técnico. |
| `#103` | 28 | `list_item` | 24 (24) | ✅ OK | `D-REF, M-MET, C-05` | a) Qwen3-0.6B (Yang et al., 2025): representante do paradigma autoregressivo decoder-only, distribuído sob lic... | O item identifica arquitetura, licença, escala geral e função como linha de base. |
| `#104` | 29 | `list_item` | 30 (30) | ✅ OK | `M-MET, C-05` | b) T5Gemma B-B PrefixLM-IT (Zhang et al., 2025): representante do paradigma encoder-decoder ajustado por instr... | A descrição diferencia claramente o representante encoder-decoder e sua faixa de parâmetros. |
| `#105` | 29 | `list_item` | 48 (48) | ❌ CRÍTICO | `M-WAZ, C-05, D-REF` | c) Qwen3-0.6B Diffusion BD3LM (Arriola et al., 2025): representante do paradigma de difusão discreta em blocos... | O checkpoint ainda não está confirmado, comprometendo a identificação exata e reprodução do experimento. **Sugestão:** *Fixar o identificador público do checkpoint e o commit/hash antes da execução.* |
| `#106` | 29 | `paragraph` | 67 (44) | ✅ OK | `M-MET, C-05` | Como os três modelos possuem diferenças de pré-treinamento, tokenização e ajuste por instruções além da arquit... | Limita corretamente a inferência causal e informa os controles de reprodutibilidade. |

### Seção: 3.6 Ambiente de execução e harness experimental

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#107` | 29 | `heading` | 8 (8) | ✅ OK | `D-PAR, C-11` | 3.6 Ambiente de execução e harness experimental | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#108` | 29 | `footnote` | 8 (8) | ✅ OK | `C-11` | 6 Disponível em: https://huggingface.co/google/t5gemma-b-b-prefixlm-it. | Nota de rodapé informativa com URL pública de repositório/artefato técnico. |
| `#109` | 29 | `paragraph` | 104 (39) | ✅ OK | `D-AMB, D-VERB, M-MET, C-05` | Os experimentos de inferência serão executados localmente em um computador portátil Lenovo IdeaPad Gaming 3i e... | Ambiente e configurações estão bem especificados, com hardware, memória e uniformidade de precisão. |
| `#110` | 30 | `paragraph` | 101 (85) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, D-AMB, M-MET` | Para avaliar semanticamente os casos que não forem resolvidos pela correspondência textual, prevê-se utilizar ... | [Regra D-VERB/M-ZUC] Período longo (85 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| O longo período acumula função do juiz, licença, critérios, registros e exceção. Precisar o critério de aceitação e separar responsabilidades. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir em frases: informar modelo/licença; estabelecer o limite de 4 GiB no piloto; listar registros; esclarecer por que não há limite temporal.* |
| `#111` | 30 | `paragraph` | 157 (40) | ✅ OK | `D-PAR, D-VERB, M-ZUC, M-MET, C-05` | Para aplicar um protocolo comum entre as execuções, o fluxo de processamento é encapsulado em um harness exper... | O fluxo modular é replicável e distingue validação, correspondência, julgamento e persistência. A sequência é clara apesar da enumeração longa. |
| `#112` | 30 | `footnote` | 11 (11) | ✅ OK | `C-11` | 7 Modelo e termos de acesso: https://huggingface.co/google/gemma-3-1b-it. | Nota de rodapé informativa com URL pública de repositório/artefato técnico. |
| `#113` | 30–31 | `paragraph` | 107 (37) | ✅ OK | `D-PAR, M-ZUC, M-MET, C-05` | Cada adaptador encapsula apenas o que é específico de um modelo: aplica o template de conversa e os tokens esp... | A adaptação por modelo, o orçamento de tokens e a decodificação determinística ficam explícitos e coerentes. |

### Seção: 3.7 Arquitetura do harness

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#114` | 31 | `heading` | 5 (5) | ✅ OK | `D-PAR, C-11` | 3.7 Arquitetura do harness | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#115` | 31 | `paragraph` | 89 (63) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, D-FIG, C-13` | A arquitetura do harness mantém constantes os fatores comuns do Quadro 3 e admite as diferenças inerentes aos ... | [Regra D-VERB/M-ZUC] Período longo (63 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| O primeiro período é longo e concentra constantes, diferenças e três formas de apresentação. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar os fatores comuns e específicos do harness da descrição das figuras e do quadro.* |
| `#116` | 31 | `caption` | 12 (12) | ✅ OK | `D-FIG, C-11` | Figura 1 – Visão geral do harness experimental para uma transição do SUMIE | Legenda breve, específica e coerente com a Figura 1. |
| `#117` | 31 | `source_note` | 13 (13) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026), a partir do protocolo descrito na Seção 3. | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |
| `#118` | 32 | `caption` | 12 (12) | ⚠️ AJUSTAR | `D-FIG, C-11` | Figura 1 — detalhe ampliado 1: preparação da transição e montagem do prompt | [Regra D-FIG/C-11] Sublegenda 'Figura 1 — detalhe ampliado 1: preparação da transição e montagem do prompt' não consta na Lista de Ilustrações, não é chamada individualmente no corpo do texto e não traz nota 'Fonte:' própria. \| A sublegenda não aparece na chamada individual nem na Lista de Ilustrações e não contém indicação de autoria. **Sugestão:** *Referenciar os detalhes ampliados 1 a 4 explicitamente no texto da Seção 3.7 (ou numerá-los como Figuras/Subfiguras formais com Fonte). Padronizar a numeração das partes da Figura 1 e citar cada detalhe no texto; incluir “Fonte: elaboração própria” se aplicável.* |
| `#119` | 32 | `caption` | 11 (11) | ⚠️ AJUSTAR | `D-FIG, C-11` | Figura 1 — detalhe ampliado 2: escritor e gravação da saída bruta | [Regra D-FIG/C-11] Sublegenda 'Figura 1 — detalhe ampliado 2: escritor e gravação da saída bruta' não consta na Lista de Ilustrações, não é chamada individualmente no corpo do texto e não traz nota 'Fonte:' própria. \| A sublegenda não está vinculada a uma chamada individual nem à Lista de Ilustrações. **Sugestão:** *Referenciar os detalhes ampliados 1 a 4 explicitamente no texto da Seção 3.7 (ou numerá-los como Figuras/Subfiguras formais com Fonte). Renumerar como parte da Figura 1, chamar explicitamente no corpo e incluir nota de fonte.* |
| `#120` | 33 | `caption` | 9 (9) | ⚠️ AJUSTAR | `D-FIG, C-11` | Figura 1 — detalhe ampliado 3: validação sintática e estrutural | [Regra D-FIG/C-11] Sublegenda 'Figura 1 — detalhe ampliado 3: validação sintática e estrutural' não consta na Lista de Ilustrações, não é chamada individualmente no corpo do texto e não traz nota 'Fonte:' própria. \| A sublegenda carece de chamada individual, registro na lista e nota de autoria. **Sugestão:** *Referenciar os detalhes ampliados 1 a 4 explicitamente no texto da Seção 3.7 (ou numerá-los como Figuras/Subfiguras formais com Fonte). Integrar a legenda à numeração geral da Figura 1 e referenciá-la no texto.* |
| `#121` | 34 | `caption` | 9 (9) | ⚠️ AJUSTAR | `D-FIG, C-11` | Figura 1 — detalhe ampliado 4: correspondência, juiz e registros | [Regra D-FIG/C-11] Sublegenda 'Figura 1 — detalhe ampliado 4: correspondência, juiz e registros' não consta na Lista de Ilustrações, não é chamada individualmente no corpo do texto e não traz nota 'Fonte:' própria. \| A sublegenda não é referenciada isoladamente nem consta da Lista de Ilustrações. **Sugestão:** *Referenciar os detalhes ampliados 1 a 4 explicitamente no texto da Seção 3.7 (ou numerá-los como Figuras/Subfiguras formais com Fonte). Chamar o detalhe no corpo; padronizar numeração e adicionar indicação de autoria quando necessário.* |
| `#122` | 34 | `paragraph` | 116 (35) | ⚠️ AJUSTAR | `D-AMB, D-VERB, D-LEIT` | Na execução, etapas (i) a (iv) da Figura 1, o harness lê do SUMIE a tupla (𝑀𝑡−1∗, 𝑂𝑡, 𝑀𝑡∗) e os rótulos ... | “Etapas” e “Figura 1” ficam mal relacionados à frase inicial. **Sugestão:** *Reescrever: “Nas etapas (i) a (iv) da Figura 1, durante a execução, o harness lê do SUMIE...”* |
| `#123` | 34–35 | `paragraph` | 128 (38) | ✅ OK | `D-PAR, M-ZUC, C-13` | Na avaliação, etapas (v) a (ix), duas decisões estruturais precedem a análise semântica. Uma saída que falhe n... | Parágrafo organizado, decisão estrutural anterior ao julgamento e fluxo replicável claros. |
| `#124` | 35 | `caption` | 9 (9) | ✅ OK | `D-FIG, C-11` | Quadro 4 – Etapas do harness, tecnologias e artefatos produzidos | Legenda curta, objetiva e compatível com o quadro descrito. |
| `#125` | 35 | `table` | 191 (121) | ⚠️ AJUSTAR | `D-FIG, C-11, D-AMB` | Etapa Componente e tecnologia \| Controle Saída usada na avaliação \| (i) Preparar transição Script de prepara... | A extração deixa cabeçalhos implícitos e a estrutura visual pouco legível. **Sugestão:** *Separar formalmente Etapa, Componente/Tecnologia, Controle e Saída em colunas ABNT.* |
| `#126` | 35 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |
| `#127` | 35–36 | `paragraph` | 220 (43) | ⚠️ AJUSTAR | `D-VERB, D-LEIT, D-FIG` | A Figura 2 amplia as etapas (ii) e (iii). A entrada do escritor é o próprio prompt- base do Apêndice A já pree... | Há verbo especializado excessivo e explicação longa que dificulta a leitura. **Sugestão:** *Dividir o texto em dois parágrafos: descrição do prompt e explicação/limites do exemplo.* |
| `#128` | 36 | `caption` | 11 (11) | ✅ OK | `D-FIG, C-11` | Figura 2 – Etapa de escrita do checkpoint (etapas ii e iii) | Legenda identifica adequadamente a figura e seu alcance. |
| `#129` | 36 | `source_note` | 14 (14) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026), com exemplo extraído do SUMIE (Hwang et al., 2025). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |

### Seção: 3.8 Métricas de avaliação

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#130` | 36 | `heading` | 5 (5) | ✅ OK | `D-PAR, C-11` | 3.8 Métricas de avaliação | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#131` | 36–37 | `paragraph` | 185 (45) | ✅ OK | `M-MET, D-AMB, C-13` | Para a avaliação semântica dos checkpoints sintaticamente válidos e aderentes ao esquema, o objeto JSON produz... | Método de correspondência, classes de erro e uso do juiz estão definidos. |
| `#132` | 37 | `equation` | 5 (5) | ✅ OK | `D-FIG, M-MET` | 𝑃= 𝑇𝑃 𝑇𝑃+ 𝐹𝑃 (2) 𝑅= 𝑇𝑃 𝑇𝑃+ 𝐹𝑁 (3) 𝐹1 = 2𝑃𝑅 𝑃+ 𝑅 (4) | Fórmula numerada, integrada à explicação das variáveis no parágrafo adjacente e coerente com as métricas do protocolo. |
| `#133` | 37 | `paragraph` | 63 (28) | ✅ OK | `M-MET, C-13` | As métricas primárias serão calculadas com o procedimento híbrido descrito acima. Para transparência, também s... | Métricas secundárias e restrições ao juiz são explícitas e transparentes. |
| `#134` | 37 | `paragraph` | 40 (40) | ✅ OK | `M-MET, D-PAR` | Para avaliar o comportamento do escritor segundo a natureza da transição em cada atributo, calculam-se a acurá... | Transição das métricas gerais às precisões por operação está clara. |
| `#135` | 38 | `paragraph` | 37 (27) | ✅ OK | `M-MET, D-CONC, C-13` | Nas Equações 5 e 6, um atributo é considerado corretamente aplicado quando há correspondência direta após norm... | Define o critério de acerto e confirma a exclusão dos casos incertos. |
| `#136` | 38 | `equation` | 36 (36) | ✅ OK | `D-FIG, M-MET` | 𝑈𝐴 = atributos com operação ADD ou UPDATE registrados corretamente em 𝑀𝑡∗ (5) total de atributos com opera... | Fórmula numerada, integrada à explicação das variáveis no parágrafo adjacente e coerente com as métricas do protocolo. |
| `#137` | 38 | `paragraph` | 15 (15) | ✅ OK | `D-FIG` | O Quadro 5 sintetiza as métricas estruturais, de estado e de operação adotadas no protocolo. | A referência ao quadro é direta e identifica claramente sua função. |
| `#138` | 38 | `caption` | 7 (7) | ✅ OK | `D-FIG` | Quadro 5 – Métricas de avaliação do experimento | Legenda sucinta, específica e autoexplicativa. |
| `#139` | 38–39 | `table` | 236 (236) | ❌ CRÍTICO | `D-FIG, D-LEIT, C-11` | Categoria Métrica Definição operacional \| Escopo de cálculo \| Estrutural Validade do JSON (JSON Validity) \|... | O quadro apresenta cabeçalhos repetidos, símbolos e quebras que comprometem a leitura e a reconstrução das colunas. **Sugestão:** *Reformatar o quadro em linhas completas, com legenda única, três colunas estáveis e definições inequívocas.* |
| `#140` | 39 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |
| `#141` | 39–40 | `paragraph` | 79 (53) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | As métricas semânticas serão reportadas sob duas visões complementares: (i) condicional à validade estrutural,... | [Regra D-VERB/M-ZUC] Período longo (53 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A frase de 53 palavras acumula condições e explicações, prejudicando a fluidez técnica. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar as duas visões de reporte em períodos curtos e independentes.* |

### Seção: 3.9 Procedimento experimental e plano de análise

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#142` | 40 | `heading` | 8 (8) | ✅ OK | `D-PAR, C-11` | 3.9 Procedimento experimental e plano de análise | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#143` | 40 | `paragraph` | 12 (12) | ✅ OK | `M-ZUC, D-PAR` | A execução experimental organiza-se em três fases sequenciais sobre o benchmark SUMIE: | A frase abre a seção de modo claro e anuncia a estrutura subsequente. |
| `#144` | 40 | `list_item` | 74 (57) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | a) Fase 0 — Verificação funcional do harness: execução de 15 transições sintéticas de teste para validar o car... | [Regra D-VERB/M-ZUC] Período longo (57 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A sentença da Fase 0 ultrapassa 45 palavras e acumula verificações operacionais. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Redigir dois parágrafos ou itens curtos: objetivos da validação e critérios de memória.* |
| `#145` | 40 | `list_item` | 71 (54) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | b) Fase 1 — Estudo piloto no SUMIE: execução em um subconjunto de 25 entidades (separado da amostra de teste p... | [Regra D-VERB/M-ZUC] Período longo (54 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A sentença da Fase 1 combina procedimentos, amostragem e congelamento em excesso. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar descrição da amostra, auditorias realizadas e congelamento prévio da Fase 2.* |
| `#146` | 40 | `list_item` | 31 (31) | ✅ OK | `M-WAZ, D-PAR` | c) Fase 2 — Experimento principal no SUMIE: execução completa dos três escritores sobre o conjunto de avaliaçã... | A descrição define claramente o experimento principal, a unidade de execução e os registros esperados. |
| `#147` | 40–41 | `paragraph` | 104 (63) | ⚠️ AJUSTAR | `D-VERB, M-ZUC` | Na análise estatística dos resultados da Fase 2, serão apuradas a média e a mediana de cada métrica por escrit... | [Regra D-VERB/M-ZUC] Período longo (63 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A frase principal tem 63 palavras e combina estatística descritiva, inferencial e temporal. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar análise descritiva, teste global, comparações pareadas e evolução temporal em períodos distintos.* |

### Seção: 3.10 Rastreabilidade entre objetivos, experimentos e evidências

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#148` | 41 | `heading` | 8 (8) | ✅ OK | `D-PAR, C-11` | 3.10 Rastreabilidade entre objetivos, experimentos e evidências | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#149` | 41 | `paragraph` | 34 (34) | ✅ OK | `C-10, D-PAR` | O Quadro 6 explicita o alinhamento metodológico entre cada objetivo específico formulado na introdução, o comp... | A referência ao Quadro 6 anuncia rastreabilidade completa entre objetivos, coleta, evidência e critérios. |
| `#150` | 41 | `caption` | 11 (11) | ✅ OK | `D-FIG, C-11` | Quadro 6 – Matriz de rastreabilidade entre objetivos específicos, artefatos e evidências | Legenda identifica claramente o quadro e seu conteúdo. |
| `#151` | 41 | `table` | 185 (185) | ⚠️ AJUSTAR | `D-FIG, D-VERB, C-10` | Objetivo específico Artefato e \| Evidência produzida Métrica e critério de análise \| procedimento \| a) Aval... | A tabela é informativa, mas a extração textual apresenta separadores confusos e reduz a legibilidade. **Sugestão:** *Padronizar cabeçalhos e alinhar cada objetivo, procedimento, métrica e critério em linhas separadas.* |
| `#152` | 41 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |

### Seção: 3.11 Limitações metodológicas e ameaças à validade

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#153` | 41 | `heading` | 8 (8) | ✅ OK | `D-PAR, C-11` | 3.11 Limitações metodológicas e ameaças à validade | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#154` | 41 | `paragraph` | 33 (33) | ✅ OK | `D-PAR, M-ZUC` | O delineamento experimental controla o método de atualização, o esquema, o prompt, o orçamento de geração e os... | A frase introduz adequadamente as limitações e prepara o desdobramento em validade. |
| `#155` | 41–42 | `list_item` | 69 (26) | ⚠️ AJUSTAR | `D-VERB, M-MET, C-13` | a) Validade interna: os três modelos comparados não compartilham o mesmo corpus de pré-treinamento, tokenizado... | O item contém períodos longos e excessiva acumulação de condições metodológicas. **Sugestão:** *Dividir em dois períodos: diferenciar comparabilidade limitada e indicar explicitamente os controles aplicados.* |
| `#156` | 42 | `list_item` | 119 (36) | ✅ OK | `M-MET, M-ZUC, C-16` | b) Validade de construção: a avaliação original do SUMIE utiliza um modelo de linguagem como juiz para verific... | Descritores abrangentes e controles adequados para viés do juiz, cegamento e auditoria. |
| `#157` | 42 | `list_item` | 62 (36) | ✅ OK | `M-MET, D-PAR, C-13` | c) Validade externa: os resultados obtidos restringem-se à tarefa de sumarização incremental de entidades em u... | Delimita claramente o alcance externo e evita extrapolações indevidas dos resultados. |

### Seção: 3.12 Resultados e contribuições esperadas

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#158` | 42 | `heading` | 6 (6) | ✅ OK | `D-PAR, C-11` | 3.12 Resultados e contribuições esperadas | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#159` | 42 | `paragraph` | 24 (24) | ✅ OK | `D-PAR, M-WAZ, C-13` | A execução completa da Fase 2 sobre o benchmark SUMIE produzirá quatro conjuntos principais de evidências empí... | Introduz a principal expectativa de resultados e a vincula aos objetivos. |
| `#160` | 42–43 | `list_item` | 90 (56) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, C-13` | 1. Caracterização da robustez estrutural por escritor (Objetivo a): quantificação das taxas de JSON Validity e... | [Regra D-VERB/M-ZUC] Período longo (56 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Uma única sentença concentra hipótese comparativa, métricas, falhas e interpretação. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar quantificação das evidências da interpretação sobre estabilidade sintática entre arquiteturas.* |
| `#161` | 43 | `list_item` | 63 (36) | ✅ OK | `M-MET, C-13` | 2. Comparação da fidelidade global e longitudinal do estado (Objetivo b): apuração de State Precision, State R... | Métricas, visão global, longitudinalidade e orçamento são apresentados de modo verificável. |
| `#162` | 43 | `list_item` | 63 (39) | ✅ OK | `M-MET, C-13` | 3. Decomposição do perfil de erro por operação de estado (Objetivo c): comparação pareada entre Preservation A... | A estratificação por operação está coerente com variáveis e permite interpretar perfis conservador ou propenso a sobrescrever. |
| `#163` | 43 | `list_item` | 50 (49) | ❌ CRÍTICO | `D-VERB, M-ZUC` | 4. Relação entre validade sintática e fidelidade semântica: o cruzamento entre as métricas estruturais e semân... | [Regra D-VERB/M-ZUC] Período longo (49 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| Período único de 49 palavras acumula subordinadas e dificulta a leitura técnica. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir em duas frases: uma sobre a relação demonstrada e outra sobre o protocolo reutilizável.* |

### Seção: 3.13 Cronograma

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#164` | 43 | `heading` | 3 (3) | ✅ OK | `D-PAR, C-11` | 3.13 Cronograma | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#165` | 43 | `paragraph` | 47 (36) | ✅ OK | `D-VERB, D-PAR, C-05` | O cronograma abrange as etapas de elaboração e validação do projeto no TCC I (2026/2) e a implementação comple... | Cronograma claramente delimita TCC I, TCC II e periodicidade das atividades. |
| `#166` | 44 | `list_item` | 11 (10) | ✅ OK | `C-05, M-WAZ` | 1. Delimitação do tema, formulação do problema e definição dos objetivos. | A atividade delimita tema, problema e objetivos de modo verificável. |
| `#167` | 44 | `list_item` | 21 (20) | ✅ OK | `C-04, C-10` | 2. Levantamento e fichamento da bibliografia sobre memória em agentes, geração estruturada e SLMs, e revisão s... | A atividade contempla bibliografia específica e revisão dos trabalhos relacionados. |
| `#168` | 44 | `list_item` | 12 (11) | ✅ OK | `C-05, M-MET` | 3. Especificação do protocolo experimental: variáveis, esquema, prompt-base e métricas (1, 2). | Especifica elementos centrais do protocolo experimental e do plano de avaliação. |
| `#169` | 44 | `list_item` | 16 (15) | ✅ OK | `C-05, C-16` | 4. Verificação de disponibilidade, licenças e requisitos de execução local dos modelos e do SUMIE (3). | Prevê conferir modelos, licenças e requisitos técnicos antes da execução. |
| `#170` | 44 | `list_item` | 14 (13) | ✅ OK | `C-05, C-08` | 5. Redação e revisão do texto do projeto de TCC I (2, 3, 4). | Inclui redação e revisão do projeto, com dependências de etapas anteriores. |
| `#171` | 44 | `list_item` | 14 (13) | ✅ OK | `C-05, C-13` | 6. Apresentação do projeto de TCC I e incorporação das recomendações da banca (5). | A apresentação e incorporação das recomendações seguem temporalmente o projeto. |
| `#172` | 44 | `list_item` | 17 (16) | ⚠️ AJUSTAR | `D-AMB, C-05, M-MET` | 7. Preparação do conjunto SUMIE: construção dos estados acumulados 𝑀𝑡∗ e rotulagem de operações (PRESERVE, A... | Usar “conjunto acumulado” sem explicar PRESERVE, ADD e UPDATE pode exigir contexto anterior. **Sugestão:** *Definir brevemente as três operações ou remeter à seção em que foram formalizadas.* |
| `#173` | 44 | `list_item` | 16 (15) | ✅ OK | `C-05, M-WAZ` | 8. Implementação da estrutura base do harness: adaptadores, analisador sintático, validador e testes unitários... | Lista componentes concretos e testes necessários à implementação do harness. |
| `#174` | 44 | `list_item` | 12 (11) | ✅ OK | `D-PAR` | 9. Execução da Fase 0 (verificação funcional local com transições sintéticas) (8). | A atividade é específica e concisa, com descrição verificável da fase funcional. |
| `#175` | 44 | `list_item` | 21 (20) | ✅ OK | `D-PAR` | 10. Execução da Fase 1 (estudo piloto em 25 entidades do SUMIE) e calibração das regras de normalização textua... | Define claramente o piloto, a amostra de 25 entidades e a calibração pretendida. |
| `#176` | 44 | `list_item` | 21 (20) | ✅ OK | `D-PAR` | 11. Execução da Fase 2 (experimento principal com os três modelos escritores em toda a partição de avaliação d... | A atividade identifica o experimento, os três modelos e a partição integral. |
| `#177` | 44 | `list_item` | 13 (12) | ✅ OK | `D-PAR` | 12. Processamento estatístico (testes pareados, curvas por turno e estratificação por operação) (11). | Os procedimentos estatísticos estão explicitados de modo conciso e apropriado. |
| `#178` | 44 | `list_item` | 14 (13) | ✅ OK | `D-PAR` | 13. Elaboração das tabelas, gráficos e análise crítica dos resultados frente à literatura (12). | A atividade especifica tabelas, gráficos e comparação crítica com a literatura. |
| `#179` | 44 | `list_item` | 15 (14) | ✅ OK | `D-PAR` | 14. Redação das seções de resultados, discussão e conclusões do artigo final (TCC II) (13). | A redação prevista das seções finais está claramente delimitada. |
| `#180` | 44 | `list_item` | 13 (12) | ✅ OK | `D-PAR` | 15. Revisão normativa e linguística, depósito final e defesa do TCC II (14). | A revisão normativa e linguística, o depósito e a defesa estão bem identificados. |
| `#181` | 45 | `paragraph` | 34 (34) | ✅ OK | `D-PAR` | Os períodos quinzenais planejados para cada atividade ao longo dos dois semestres (Q1 a Q20, de agosto de 2026... | A referência à Tabela 1 e à relação numerada estabelece uma transição adequada. |
| `#182` | 45 | `caption` | 14 (14) | ⚠️ AJUSTAR | `D-FIG, C-11` | Tabela 1 – Cronograma de atividades para TCC I e II, com subdivisão quinzenal indicando | A legenda termina em “indicando” e não constitui uma descrição completa e autoexplicativa. **Sugestão:** *Completar: “Tabela 1 – Cronograma das atividades do TCC I e II, subdivididas por quinzenas.”* |
| `#183` | 45 | `table` | 55 (35) | ❌ CRÍTICO | `D-FIG, C-11, D-AMB` | tarefas realizadas e planejadas ao longo dos dois semestres. \| ago. set. out. nov. dez. fev. mar. abr. mai. j... | [Regra D-FIG/C-11] Na Tabela 1 (Cronograma), os períodos quinzenais Q1–Q20 estão marcados apenas por preenchimento visual de cor sem caractere textual ('X' ou '•'), ficando vazios em leitores de tela ou extração textual. \| Os períodos são representados apenas por cores, sem símbolos ou caracteres acessíveis. Isso impede leitura por extração textual e tecnologia assistiva. **Sugestão:** *Inserir marcador textual ('X' ou '■') dentro das células ativas de Q1 a Q20 além do sombreamento visual. Substituir ou complementar o preenchimento visual por marcas como “X” ou “•” em todas as células correspondentes.* |
| `#184` | 45 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |

### Seção: 4 CONSIDERAÇÕES FINAIS

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#185` | 46 | `heading` | 3 (3) | ✅ OK | `D-PAR, C-11` | 4 CONSIDERAÇÕES FINAIS | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#186` | 46 | `paragraph` | 105 (45) | ⚠️ AJUSTAR | `D-VERB, D-CONC, C-08, C-13` | A confiabilidade de agentes baseados em modelos de linguagem que operam em múltiplas etapas depende da integri... | O texto conclui adequadamente o problema, mas é excessivamente compactado e contém nominalizações que podem dificultar a leitura. **Sugestão:** *Separar em períodos menores e substituir expressões como “constitui um passo necessário” por uma afirmação direta.* |
| `#187` | 46 | `paragraph` | 121 (49) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, M-MET, C-05, C-13` | Para responder a essa questão, este projeto propõe um protocolo experimental controlado sobre o benchmark de s... | [Regra D-VERB/M-ZUC] Período longo (49 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A sentença de 49 palavras acumula método, controles e métricas. A articulação torna a replicação menos clara. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Separar os controles, a variação dos modelos e as métricas em três frases ou em listas metodológicas.* |
| `#188` | 47 | `paragraph` | 106 (60) | ⚠️ AJUSTAR | `D-VERB, M-ZUC, D-AMB, C-08, C-13` | Os resultados a serem obtidos estarão circunscritos aos três representantes avaliados, ao formato plano de par... | [Regra D-VERB/M-ZUC] Período longo (60 palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas. \| A sentença de 60 palavras combina limitações e desdobramentos futuros em uma estrutura pesada. **Sugestão:** *Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto. Dividir em dois períodos: um para limitações e outro para trabalhos futuros.* |

### Seção: REFERÊNCIAS

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#189` | 48 | `heading` | 1 (1) | ✅ OK | `D-PAR, C-11` | REFERÊNCIAS | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#190` | 48 | `reference` | 30 (11) | ✅ OK | `D-REF, C-09` | ARRIOLA, Marianne et al. Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models. ... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#191` | 48 | `reference` | 29 (11) | ✅ OK | `D-REF, C-09` | BINI, Massimo et al. MemLoRA: Distilling Expert Adapters for On-Device Memory Systems. arXiv:2512.04763v1, 202... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#192` | 48 | `reference` | 30 (12) | ✅ OK | `D-REF, C-09` | CHOI, Wonjun et al. PGMem: Tightly Coupled Persona-Memory Graph for Lifelong Personalized Agents. arXiv:2608.0... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#193` | 48 | `reference` | 23 (13) | ✅ OK | `D-REF, C-09` | DEMŠAR, Janez. Statistical Comparisons of Classifiers over Multiple Data Sets. Journal of Machine Learning Res... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#194` | 48 | `reference` | 55 (12) | ✅ OK | `D-REF, C-09` | GENG, Saibo et al. Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning. In: Proceedings o... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#195` | 48 | `reference` | 31 (13) | ✅ OK | `D-REF, C-09` | GENG, Saibo et al. JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models. arXiv:2501... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#196` | 48 | `reference` | 30 (17) | ✅ OK | `D-REF, C-09` | GONG, Shansan et al. Scaling Diffusion Language Models via Adaptation from Autoregressive Models. arXiv:2410.1... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#197` | 48 | `reference` | 21 (12) | ✅ OK | `D-REF, C-09` | HOLM, Sture. A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of Statistics, v. 6... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#198` | 48 | `reference` | 32 (13) | ✅ OK | `D-REF, C-09` | HU, Yuanzhe; WANG, Yu; MCAULEY, Julian. Evaluating Memory in LLM Agents via Incremental Multi-Turn Interaction... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#199` | 48 | `reference` | 49 (10) | ✅ OK | `D-REF, C-09` | HWANG, EunJeong et al. Enhancing Incremental Summarization with Structured Representations. In: Findings of th... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#200` | 49 | `reference` | 46 (9) | ✅ OK | `D-REF, C-09` | HWANG, EunJeong et al. SUMIE: A Synthetic Benchmark for Incremental Entity Summarization. In: Proceedings of t... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#201` | 49 | `reference` | 34 (17) | ❌ CRÍTICO | `D-REF, C-09, C-11, C-12` | HWANG, Tao; DIAO, Yishi. AMU:Admission and Memory Update for Personalized Conversations---Structured Memory wi... | [Regra D-REF/C-09/C-11]  Artefato de formatação na referência bibliográfica: falta de espaço após dois-pontos ('AMU:Admission') e travessão LaTeX literal não convertido ('---Structured'). \| A referência contém separadores LaTeX literais e ausência de espaço após dois-pontos, comprometendo apresentação e legibilidade. **Sugestão:** *Corrigir para 'AMU: Admission and Memory Update for Personalized Conversations — Structured Memory with SLM Guided Control.' Escrever “AMU: Admission and Memory Update for Personalized Conversations—Structured Memory with SLM-Guided Control.”* |
| `#202` | 49 | `reference` | 54 (12) | ✅ OK | `D-REF, C-09` | JAYALATH, Dulhan et al. PRISM: Efficient Long-Range Reasoning With Short- Context LLMs. In: Proceedings of the... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#203` | 49 | `reference` | 32 (14) | ✅ OK | `D-REF, C-09` | KANG, Jingyi et al. MemReader: From Passive to Active Extraction for Long- Term Agent Memory. arXiv:2604.07877... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#204` | 49 | `reference` | 38 (18) | ✅ OK | `D-REF, C-09` | KHANAL, Aja et al. Agents of Diffusion: Enhancing Diffusion Language Models with Multi-Agent Reinforcement Lea... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#205` | 49 | `reference` | 66 (15) | ✅ OK | `D-REF, C-09` | LEE, Jemin et al. Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Lan... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#206` | 49 | `reference` | 35 (14) | ✅ OK | `D-REF, C-09` | LU, Qingyu et al. The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Realit... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#207` | 49 | `reference` | 28 (8) | ✅ OK | `D-REF, C-09` | LU, Zhenyan et al. Small Language Models: Survey, Measurements, and Insights. arXiv:2409.15790v3, 2025. Dispon... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#208` | 49 | `reference` | 29 (16) | ✅ OK | `D-REF, C-09` | MAHARANA, Adyasha et al. Evaluating Very Long-Term Conversational Memory of LLM Agents. arXiv:2402.17753, 2024... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#209` | 50 | `reference` | 34 (21) | ✅ OK | `D-REF, C-09` | MUHOBERAC, Matthew et al. State and Memory is All You Need for Robust and Reliable AI Agents. arXiv:2507.00081... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#210` | 50 | `reference` | 31 (12) | ✅ OK | `D-REF, C-09` | MÜNDLER, Niels; DEKONINCK, Jasper; VECHEV, Martin. Constrained Decoding of Diffusion LLMs with Context-Free Gr... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#211` | 50 | `reference` | 28 (15) | ✅ OK | `D-REF, C-09` | NIE, Shen et al. Scaling up Masked Diffusion Models on Text. arXiv:2410.18514v3, 2024. Disponível em: https://... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#212` | 50 | `reference` | 52 (12) | ✅ OK | `D-REF, C-09` | PETERSEN, Kai; VAKKALANKA, Sairam; KUZNIARZ, Ludwik. Guidelines for conducting systematic mapping studies in s... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#213` | 50 | `reference` | 29 (11) | ✅ OK | `D-REF, C-09` | QIU, Wentao et al. DimMem: Dimensional Structuring for Efficient Long-Term Agent Memory. arXiv:2605.15759v3, 2... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#214` | 50 | `reference` | 36 (13) | ✅ OK | `D-REF, C-09` | SHARMA, Raghav; MEHTA, Manan. Small Language Models for Agentic Systems: A Survey of Architectures, Capabiliti... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#215` | 50 | `reference` | 29 (10) | ✅ OK | `D-REF, C-09` | SUMERS, Theodore R. et al. Cognitive Architectures for Language Agents. Transactions on Machine Learning Resea... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#216` | 50 | `reference` | 31 (13) | ✅ OK | `D-REF, C-09` | WANG, Yubo et al. CMI-Mem: Toward Generalizable Long-Term Memory Management via CMI-Augmented Reinforcement Le... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#217` | 50 | `reference` | 29 (11) | ✅ OK | `D-REF, C-09` | WU, Di et al. LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv:2410.10813v2, 2... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#218` | 50 | `reference` | 33 (15) | ✅ OK | `D-REF, C-09` | XIAO, Jianfei et al. AlpsBench: An LLM Personalization Benchmark for Real- Dialogue Memorization and Preferenc... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#219` | 50 | `reference` | 31 (13) | ✅ OK | `D-REF, C-09` | XU, Xiucheng et al. Chain-of-Memory: Lightweight Memory Construction with Dynamic Evolution for LLM Agents. ar... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#220` | 51 | `reference` | 24 (11) | ✅ OK | `D-REF, C-09` | YANG, An et al. Qwen3 Technical Report. arXiv:2505.09388v1, 2025. Disponível em: https://arxiv.org/abs/2505.09... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#221` | 51 | `reference` | 32 (12) | ✅ OK | `D-REF, C-09` | YUEN, Sizhe et al. Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextua... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#222` | 51 | `reference` | 28 (15) | ✅ OK | `D-REF, C-09` | ZENG, Ruihong et al. On the Structural Memory of LLM Agents. arXiv:2412.15266, 2024. Disponível em: https://ar... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#223` | 51 | `reference` | 29 (10) | ✅ OK | `D-REF, C-09` | ZHANG, Biao et al. Encoder-Decoder Gemma: Improving the Quality-Efficiency Trade-Off via Adaptation. arXiv:250... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#224` | 51 | `reference` | 31 (10) | ✅ OK | `D-REF, C-09` | ZHAO, Jinqing; WU, Chengcan. Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agen... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |
| `#225` | 51 | `reference` | 32 (12) | ✅ OK | `D-REF, C-09` | ZHOU, Qisheng; XIONG, Zhen; TAN, Qiaoyu. DiffuPlan: Editable Planning State for Diffusion Language Model Agent... | Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso). |

### Seção: APÊNDICE A – PROMPT-BASE DO ESCRITOR DE MEMÓRIA

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#226` | 52 | `heading` | 7 (7) | ✅ OK | `D-PAR, C-11` | APÊNDICE A – PROMPT-BASE DO ESCRITOR DE MEMÓRIA | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#227` | 52 | `paragraph` | 47 (25) | ✅ OK | `C-13, C-05, D-LEIT` | O prompt-base é mantido em inglês, idioma dos conjuntos de dados e dos modelos avaliados, e é idêntico para os... | Explica claramente a identidade do prompt e a substituição dos marcadores, com pronomes inequívocos. |
| `#228` | 52 | `code_or_query` | 96 (17) | ✅ OK | `M-MET` | You are the memory-state updater of an autonomous agent. Your task is to update a persistent JSON state. Rules... | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |

### Seção: APÊNDICE B – ARTEFATOS DA REVISÃO SISTEMÁTICA

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#229` | 53 | `heading` | 6 (6) | ✅ OK | `D-PAR, C-11` | APÊNDICE B – ARTEFATOS DA REVISÃO SISTEMÁTICA | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#230` | 53 | `paragraph` | 51 (22) | ✅ OK | `D-FIG, D-LEIT, C-05, C-13` | O Quadro 7 apresenta os principais parâmetros de cada etapa da revisão sistemática descrita na Seção 3.1. Os v... | Localiza o quadro, informa a data da execução e orienta a leitura das expressões de busca. |
| `#231` | 53 | `caption` | 7 (7) | ✅ OK | `D-FIG, C-11` | Quadro 7 – Parâmetros metodológicos da revisão sistemática | A legenda é concisa, específica e identifica corretamente o conteúdo metodológico do quadro. |
| `#232` | 53 | `table` | 218 (218) | ❌ CRÍTICO | `D-FIG, D-LEIT, C-05, C-11, C-13` | Etapa Parâmetro Valor adotado \| a) Planejamento Janela temporal Primeiro depósito entre 01/07/2025 e 12/11/20... | O conteúdo aparece em texto linear, com separadores artificiais e hierarquia inadequada, dificultando a interpretação tabular. **Sugestão:** *Formatar como tabela ABNT com linhas e colunas claras, agrupamento das etapas e indicação de fonte quando aplicável.* |
| `#233` | 53 | `source_note` | 5 (5) | ✅ OK | `D-FIG, C-11` | Fonte: elaborado pelo autor (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |

### Seção: Expressões de busca

| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |
|---|---|---|---|---|---|---|---|
| `#234` | 54 | `heading` | 3 (3) | ✅ OK | `D-PAR, C-11` | Expressões de busca | Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1. |
| `#235` | 54 | `paragraph` | 29 (16) | ✅ OK | `C-05, C-13, D-LEIT` | As seis consultas foram combinadas com o filtro temporal apresentado no Quadro 7. Dentro de cada faceta, os te... | Explica corretamente a combinação das facetas por OR e AND e remete a uma representação anterior. |
| `#236` | 54 | `list_item` | 10 (10) | ✅ OK | `C-05, C-13, D-AMB` | F1 – Memória estruturada ou entidades com atualização incremental (52 registros) | A consulta é específica, com número preciso de registros e descrição clara da estratégia de busca. |
| `#237` | 54 | `code_or_query` | 69 (69) | ✅ OK | `M-MET` | (ti:"entity summarization" OR abs:"entity summarization" OR ti:"entity state" OR abs:"entity state" OR ti:"str... | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |
| `#238` | 54 | `list_item` | 10 (10) | ⚠️ AJUSTAR | `D-AMB, C-13` | F2 – Modelos compactos que escrevem ou gerem memória (71 registros) | “Modelos compactos” e “gerem memória” podem ter significados variados sem critérios explícitos. **Sugestão:** *Especifique o critério de compactação e substitua “gerem” por uma ação precisa.* |
| `#239` | 54 | `code_or_query` | 85 (85) | ✅ OK | `M-MET` | (ti:"small language model" OR abs:"small language model" OR ti:"compact language model" OR abs:"compact langua... | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |
| `#240` | 54 | `list_item` | 13 (13) | ✅ OK | `D-FIG, C-13` | F3 – Difusão em memória de agentes ou estado de planejamento editável (2 registros) | Descrição técnica específica, com objeto de busca e quantidade registrada com precisão. |
| `#241` | 54 | `code_or_query` | 79 (79) | ✅ OK | `M-MET` | (ti:"diffusion language model" OR abs:"diffusion language model" OR ti:"block diffusion" OR abs:"block diffusi... | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |
| `#242` | 54 | `list_item` | 11 (11) | ⚠️ AJUSTAR | `D-VERB, D-AMB` | F4 – JSON estruturado relacionado a memória, estado ou entidades (10 registros) | “Relacionado a” é amplo e não define exatamente quais estruturas JSON foram consideradas. **Sugestão:** *Substitua “relacionado a” por “que codifica” ou “que representa”.* |
| `#243` | 54 | `code_or_query` | 57 (57) | ✅ OK | `M-MET` | (ti:JSON OR abs:JSON OR ti:"structured output" OR abs:"structured output") AND (ti:SLM OR abs:SLM OR ti:"small... | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |
| `#244` | 55 | `list_item` | 9 (9) | ⚠️ AJUSTAR | `D-AMB, D-REF` | F5 – Menções ao GU-JSON ou ao SUMIE (7 registros) | GU-JSON e SUMIE podem exigir expansão na primeira ocorrência para evitar ambiguidade. **Sugestão:** *Apresente a forma completa dos nomes ou explique que são os termos consultados.* |
| `#245` | 55 | `code_or_query` | 11 (11) | ✅ OK | `M-MET` | (ti:"GU-JSON" OR abs:"GU-JSON" OR ti:SUMIE OR abs:SUMIE) | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |
| `#246` | 55 | `list_item` | 11 (11) | ⚠️ AJUSTAR | `D-AMB, C-13` | F6 – Estado ou memória estruturados atualizados por modelos pequenos (26 registros) | “Modelos pequenos” é impreciso e pode reproduzir o critério não definido em “compactos”. **Sugestão:** *Defina o tamanho dos modelos ou use o mesmo critério técnico aplicado à expressão anterior.* |
| `#247` | 55 | `code_or_query` | 77 (77) | ✅ OK | `M-MET` | (ti:"small model" OR abs:"small model" OR ti:"small language model" OR abs:"small language model" OR ti:SLM OR... | Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática. |
| `#248` | 55 | `source_note` | 6 (6) | ✅ OK | `D-FIG, C-11` | Fonte: protocolo da revisão sistemática (2026). | Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros. |



---

## Auditoria Visual das Páginas Renderizadas

# Auditoria Visual das Páginas do PDF

- PDF: `D:\repos\tcc_harnes\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins_corrigido (1).pdf`
- Modelo com visão: `mai-code-2-flash`
- Resolução: `150 dpi`
- Páginas analisadas: `55`
- Chamadas à API: `6`
- Lotes servidos pelo cache: `0`

| Página | Status | Códigos | Observação | Sugestão |
|---|---|---|---|---|
| 1 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 2 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 3 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 4 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 5 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 6 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 7 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 8 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 9 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 10 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 11 | AJUSTAR | V-FMT, V-TEXT | O rótulo do terceiro objetivo aparece destacado como “e)a)” em vez de uma numeração correta. | Substituir “e)a)” por “c)” e remover o destaque verde residual. |
| 17 | CRITICO | V-PLACEHOLDER | O marcador residual “[GS2]” aparece ao final do parágrafo sobre o teste de Holm-Bonferroni. | Remover o marcador “[GS2]” e revisar eventuais marcadores GS residuais. |
| 19 | CRITICO | V-PLACEHOLDER | O título do Quadro 1 termina com o marcador residual “[GS3]”. | Remover “[GS3]” do título e verificar o restante do documento por marcadores semelhantes. |
| 21 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 22 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 23 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 24 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 25 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 26 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 27 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 28 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 29 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 30 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 31 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 32 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 33 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 34 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 35 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 36 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 37 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 38 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 39 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 40 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 41 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 42 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 43 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 44 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 45 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 46 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 47 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 48 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 49 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 50 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 51 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 52 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 53 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 54 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |
| 55 | OK | V-FMT | Nenhum problema visual relevante identificado. | - |

