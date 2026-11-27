"""Slides principais 1–9: abertura, contexto, justificativa, lacuna, pergunta, objetivos e
hipóteses. Layout único: etiqueta + título + texto em coluna única (sem caixas)."""

from __future__ import annotations

from pptx_kit import *


def capa(d):
    s = d.new("capa", footer=False)
    rect(s, 0, 0, SLIDE_W, 0.16, NAVY)
    rect(s, 0, 0.16, SLIDE_W, 0.05, ACCENT)
    d.img(s, "logo", (SLIDE_W - 4.6) / 2, 0.45, w=4.6)
    text(s, MX, 1.45, CW, 0.75, [
        "UNIVERSIDADE ESTADUAL DO TOCANTINS – UNITINS",
        "Campus de Palmas – TO · Curso de Bacharelado em Sistemas de Informação"],
        size=14, color=MUTED, align="center", space_after=2)
    text(s, 1.0, 2.35, SLIDE_W - 2.0, 1.75, [
        P("MODELOS DE LINGUAGEM COMPACTOS COMO ESCRITORES DE MEMÓRIA:", size=30),
        P("AVALIAÇÃO DA ATUALIZAÇÃO INCREMENTAL DE ESTADOS JSON PARA AGENTES", size=22)],
        bold=True, color=NAVY, align="center", anchor="middle", space_after=4)
    text(s, MX, 4.2, CW, 0.45, "Projeto de Trabalho de Conclusão de Curso (TCC I)",
         size=18, bold=True, color=ACCENT, align="center")
    text(s, MX, 4.85, CW, 1.0, [
        "**Acadêmico:** Guilherme Henrique Siqueira Lopes",
        "**Orientador:** Prof. Me. Alex Coelho"], size=18, align="center", space_after=4)
    text(s, MX, 6.35, CW, 0.4, "Palmas/TO · 2026", size=14, color=MUTED, align="center")
    rect(s, 0, SLIDE_H - 0.12, SLIDE_W, 0.12, NAVY)
    d.script(s, "Apresentar-se, o orientador e o título; abrir com calma.",
             "Boa tarde a todos e à banca. Eu sou Guilherme Henrique Siqueira Lopes, do curso de "
             "Sistemas de Informação, e apresento o meu projeto de TCC, orientado pelo professor "
             "Alex Coelho: Modelos de linguagem compactos como escritores de memória — uma "
             "avaliação da atualização incremental de estados JSON para agentes.",
             "Começo pelo contexto do problema.",
             "Não corte; é a abertura.",
             ["Cumprimentar a banca", "Nome, curso, orientador e título completo"])


def contexto(d):
    s = d.new("contexto", "Introdução · Contexto",
              "Agentes dependem de um estado persistente entre etapas")
    bullets(s, [
        "Agentes baseados em modelos de linguagem executam tarefas de **múltiplas etapas**: as "
        "decisões dependem das informações registradas em turnos anteriores "
        "(Hu; Wang; McAuley, 2025).",
        "O gerenciamento de memória envolve a **geração, a atualização e a recuperação** de "
        "informações relevantes (Zeng et al., 2024).",
        "Um estado persistente e consistente condiciona a **confiabilidade operacional** do "
        "sistema (Muhoberac et al., 2025).",
        "O acúmulo irrestrito do histórico excede ou degrada a janela de contexto → consolidar as "
        "observações em uma **representação estruturada persistente**.",
        "~~Harness~~ de agentes: camada de software que envolve o modelo — seleciona o contexto, "
        "disponibiliza ferramentas e coordena ações; a memória integra essa camada.",
        "**Recorte:** apenas a **escrita incremental** da memória, sem avaliar a recuperação nem "
        "o desempenho de um agente completo."], size=19)
    d.script(s, "Situar o problema da memória em agentes e já delimitar o recorte.",
             "Agentes baseados em modelos de linguagem executam tarefas de várias etapas, e cada "
             "decisão depende do que foi registrado antes. Por isso, gerenciar a memória é parte "
             "central do harness — a camada de software que envolve o modelo, seleciona o "
             "contexto, oferece ferramentas e coordena as ações. Guardar todo o histórico estoura "
             "ou degrada a janela de contexto; a saída recorrente é consolidar as observações numa "
             "representação estruturada. Um recorte importante: aqui eu estudo apenas a escrita "
             "dessa memória — não a recuperação, nem o agente completo.",
             "Uma forma de consolidar esse estado é o método GU-JSON.",
             "Pule a definição de harness; diga só o recorte (apenas escrita).",
             ["Múltiplas etapas → estado persistente",
              "Harness = contexto + ferramentas + coordenação", "Recorte: só a escrita"])


def gu_json(d):
    s = d.new("gujson", "Referencial teórico · Seção 2.3",
              "GU-JSON: o escritor reescreve o checkpoint inteiro a cada observação")
    equation(s, 1.55, 0.8, "M_{t} = G(S, M_{t−1}, O_{t})      (1)", size=34)
    text(s, MX, 2.35, CW, 0.45,
         "**S** esquema · **M_{t−1}** ~~checkpoint~~ anterior · **O_{t}** nova observação · "
         "**G** modelo escritor · **M_{t}** ~~checkpoint~~ resultante",
         size=16, color=MUTED, align="center", space_after=0)
    bullets(s, [
        "Hwang et al. (2024): sob orçamento restrito de memória (SUMIE e BooookScore; Gemini "
        "Ultra e Pro), o **GU-JSON superou consistentemente o GU-Text**.",
        "Propriedade central: toda a manutenção do estado ocorre em **uma única chamada** ao "
        "modelo G, que precisa, ao mesmo tempo:",
        P("preservar os campos inalterados, integrar as novas informações e manter a estrutura "
          "JSON válida.", bullet=True, level=1),
        "Sem algoritmos auxiliares de mesclagem → o comportamento do **escritor** é avaliado "
        "diretamente.",
        "O ~~checkpoint~~ JSON explicita os pares atributo-valor e permite inspecionar o estado a "
        "cada transição (Jayalath et al., 2025; Yuen et al., 2025)."], y=3.0, size=19)
    d.script(s, "Explicar o GU-JSON e por que ele isola o escritor.",
             "Uma forma de fazer essa consolidação é o GU-JSON, de Hwang e colegas, de 2024. A "
             "cada nova observação, o escritor G recebe o esquema, o checkpoint anterior e a "
             "observação, e regenera o checkpoint completo. Naquele estudo, com modelos Gemini "
             "de grande porte e memória restrita, a atualização em JSON superou a atualização em "
             "texto livre. Para este trabalho, a propriedade central é a chamada única: o próprio "
             "modelo precisa preservar o que não mudou, integrar o que é novo e manter o JSON "
             "válido. Assim dá para avaliar o escritor diretamente.",
             "Mas essa mesma propriedade cria um risco.",
             "Leia a equação e diga só a propriedade de chamada única.",
             ["Equação 1: M_t = G(S, M_t−1, O_t)", "GU-JSON > GU-Text (Hwang 2024)",
              "Chamada única isola o escritor"])


def justificativa(d):
    s = d.new("justificativa", "Introdução · Justificativa",
              "O escritor é ponto crítico de falha — e é chamado a cada turno")
    bullets(s, [
        "Como o GU-JSON reescreve integralmente o objeto a cada etapa, o escritor "
        "(~~memory writer~~) pode:",
        P("corromper a sintaxe do JSON ou violar o esquema estipulado (Geng et al., 2025);",
          bullet=True, level=1),
        P("omitir fatos ainda válidos, alterar valores indevidamente ou introduzir informações "
          "sem respaldo na entrada.", bullet=True, level=1),
        "A reescrita ocorre **a cada turno**: delegá-la a modelos de grande porte eleva o "
        "**custo computacional** e a **latência** do agente.",
        "Modelos de linguagem compactos (**SLMs**) viabilizam **execução local** e menor consumo "
        "em subtarefas bem delimitadas e restritas por esquema (Lu et al., 2025; Sharma; Mehta, "
        "2025) → alternativa como escritores dedicados de memória.",
        "Transformar um estado JSON anterior e uma nova observação textual em um novo objeto "
        "JSON completo impõe **demandas distintas conforme o paradigma gerativo** do modelo."],
        size=19)
    d.script(s, "Justificar o problema e a escolha por modelos compactos.",
             "Essa mesma propriedade é o problema. Como o objeto é reescrito inteiro a cada etapa, "
             "o escritor vira um ponto crítico de falha: ele pode quebrar a sintaxe ou violar o "
             "esquema, omitir fatos ainda válidos, alterar valores ou inventar informação. E como "
             "a reescrita acontece a cada turno, usar modelos grandes eleva o custo e a latência. "
             "Modelos de linguagem compactos, os SLMs, viabilizam execução local e menor consumo "
             "em subtarefas delimitadas e restritas por esquema — por isso são candidatos a "
             "escritores dedicados de memória. Mas essa tarefa impõe demandas diferentes conforme "
             "o paradigma gerativo do modelo.",
             "Quais são esses paradigmas?",
             "Cite só os modos de falha e a frase final.",
             ["Modos de falha do escritor", "Custo/latência → SLMs locais",
              "Paradigma gerativo importa"])


def paradigmas(d):
    s = d.new("paradigmas", "Referencial teórico · Seção 2.6",
              "Três paradigmas gerativos, uma mesma tarefa de escrita")
    bullets(s, [
        "**Autoregressivo ~~decoder-only~~:** fatora a sequência da esquerda para a direita; cada "
        "~~token~~ é condicionado ao prefixo já produzido (Yang et al., 2025).",
        P("Representante: **Qwen3-0.6B** — linha de base autoregressiva.", bullet=True, level=1),
        "**~~Encoder-decoder~~:** um codificador com atenção bidirecional lê toda a entrada antes "
        "de o decodificador gerar a saída (Zhang et al., 2025).",
        P("Representante: **T5Gemma B-B PrefixLM-IT** — adaptado de modelos ~~decoder-only~~ "
          "pré-treinados.", bullet=True, level=1),
        "**Difusão em blocos (BD3LM):** gera blocos de forma autoregressiva e aplica difusão "
        "discreta — remoção de ruído sobre ~~tokens~~ mascarados — dentro de cada bloco "
        "(Arriola et al., 2025).",
        P("Representante: **Qwen3-0.6B Diffusion BD3LM**.", bullet=True, level=1),
        "Os três: escala aproximada de **~0,6 bilhão de parâmetros**, pesos abertos e execução "
        "em ~~hardware~~ local."], size=19)
    d.script(s, "Apresentar os três paradigmas e seus representantes.",
             "Considero três paradigmas. No autoregressivo decoder-only, o modelo gera token a "
             "token, da esquerda para a direita; o representante é o Qwen3 de 0,6 bilhão de "
             "parâmetros, a linha de base. No encoder-decoder, um codificador lê toda a entrada "
             "com atenção bidirecional antes de o decodificador gerar a saída; o representante é "
             "o T5Gemma B-B. E na difusão em blocos, os blocos são gerados em sequência, mas "
             "dentro de cada bloco os tokens mascarados são refinados em paralelo; o "
             "representante é o Qwen3-0.6B BD3LM. Os três têm cerca de 0,6B, pesos abertos e "
             "execução local.",
             "E o que a literatura já fez com isso?",
             "Uma frase por paradigma + nome do modelo.",
             ["Decoder-only → Qwen3-0.6B", "Encoder-decoder → T5Gemma B-B",
              "Difusão em blocos → Qwen3-0.6B BD3LM", "~0,6B, pesos abertos"])


def lacuna(d):
    s = d.new("lacuna", "Trabalhos relacionados · Seção 2.8",
              "Lacuna: paradigmas gerativos não comparados como escritores")
    bullets(s, [
        "GU-JSON e SUMIE foram avaliados originalmente só com **modelos proprietários de grande "
        "porte** (Hwang et al., 2024; Hwang et al., 2025).",
        "Comparações entre difusão e autoregressão em fluxos agênticos: modelos de **7 a 8 "
        "bilhões** de parâmetros com memória em **texto livre** (Lu et al., 2026).",
        "Revisão sistemática → **12 estudos no núcleo** (Quadro 1): modelos de até ~4B já atuam "
        "como extratores, gestores ou escritores de memória.",
        P("O escritor compacto, isoladamente, **não constitui lacuna**.", bullet=True, level=1),
        P("Na maioria, o modelo emite **operações sobre registros, grafos ou ~~slots~~**, "
          "aplicadas por código, e a avaliação recai sobre ações de escrita, chaves isoladas ou "
          "estado de diálogo.", bullet=True, level=1),
        P("**Nenhum compara paradigmas gerativos**: todos os escritores são autoregressivos.",
          bullet=True, level=1),
        P("Não se identificou uma comparação controlada entre representantes compactos de "
          "paradigmas gerativos distintos atuando **exclusivamente como escritores** de um mesmo "
          "~~checkpoint~~ JSON sob orçamento fixo de ~~tokens~~.", bold=False, color=NAVY,
          size=19, space_before=6)], size=18, space_after=8)
    d.script(s, "Mostrar a lacuna a partir da literatura e do Quadro 1.",
             "Onde está a lacuna? O GU-JSON e o SUMIE foram avaliados só com modelos "
             "proprietários de grande porte. A comparação entre difusão e autoregressão em fluxos "
             "agênticos usou modelos de 7 a 8 bilhões e memória em texto livre. E a revisão "
             "sistemática encontrou 12 estudos em que modelos compactos já escrevem ou gerenciam "
             "memória — então um escritor compacto, sozinho, não é lacuna. Mas, nesses estudos, o "
             "modelo geralmente emite operações aplicadas por código, e todos os escritores são "
             "autoregressivos. Falta uma comparação controlada entre paradigmas atuando só como "
             "escritores do mesmo checkpoint JSON.",
             "Dessa lacuna vem a pergunta de pesquisa.",
             "Leia apenas a frase final da lacuna.",
             ["Compacto sozinho não é lacuna", "Núcleo: operações por código, todos AR",
              "Lacuna: paradigmas como escritores do mesmo checkpoint"])


def pergunta(d):
    s = d.new("pergunta", "Introdução · Problema", "Pergunta de pesquisa e objetivo geral")
    text(s, MX, 1.6, CW, 5.3, [
        heading("Pergunta de pesquisa", size=20),
        P("Como representantes compactos dos paradigmas autoregressivo ~~decoder-only~~, "
          "~~encoder-decoder~~ e de difusão em blocos diferem na qualidade da atualização "
          "incremental de ~~checkpoints~~ pelo método GU-JSON no ~~benchmark~~ SUMIE, sob esquema "
          "e limite de memória fixos?", size=21, space_after=24),
        heading("Objetivo geral", size=20),
        P("Comparar a qualidade da atualização incremental de ~~checkpoints~~ JSON produzida "
          "pelos modelos compactos **Qwen3-0.6B** (~~decoder-only~~), **T5Gemma B-B** "
          "(~~encoder-decoder~~) e **Qwen3-0.6B BD3LM** (difusão em blocos), atuando como "
          "escritores de memória no método GU-JSON, no ~~benchmark~~ SUMIE e sob condições "
          "experimentais controladas.", size=21)])
    d.script(s, "Ler a pergunta e o objetivo geral com ênfase.",
             "Daí a pergunta de pesquisa: como representantes compactos dos paradigmas "
             "autoregressivo decoder-only, encoder-decoder e de difusão em blocos diferem na "
             "qualidade da atualização incremental de checkpoints pelo método GU-JSON no "
             "benchmark SUMIE, sob esquema e limite de memória fixos? O objetivo geral é comparar "
             "essa qualidade entre o Qwen3-0.6B, o T5Gemma B-B e o Qwen3-0.6B BD3LM, atuando como "
             "escritores de memória, sob condições controladas.",
             "Esse objetivo se desdobra em três objetivos específicos.",
             "Leia só a pergunta; o objetivo está no slide.",
             ["Ler a pergunta pausadamente", "Três modelos nomeados no objetivo geral"])


def objetivos(d):
    s = d.new("objetivos", "Introdução · Objetivos", "Objetivos específicos")
    text(s, MX, 1.7, CW, 5.2, [
        P("**a)** avaliar a **conformidade estrutural** dos ~~checkpoints~~ produzidos por cada "
          "escritor a partir das taxas de validade sintática do JSON e de aderência ao esquema "
          "ao longo das transições;"),
        P("**b)** comparar a **fidelidade do estado** mantido por cada escritor ao longo dos "
          "turnos de atualização do SUMIE, utilizando precisão, revocação, F1 do estado e taxa "
          "de alucinação;"),
        P("**c)** analisar o **perfil de erro** dos escritores segundo o tipo de operação exigida "
          "no SUMIE, contrastando a preservação de atributos inalterados com a adição e a "
          "atualização de informações.")], size=22, space_after=26)
    d.script(s, "Mostrar que cada objetivo específico tem métricas próprias.",
             "São três objetivos específicos. O primeiro, conformidade estrutural: o checkpoint é "
             "um JSON válido e respeita o esquema? O segundo, fidelidade do estado: o conteúdo "
             "está certo, medido por precisão, revocação, F1 e alucinação? O terceiro, perfil de "
             "erro por operação: o modelo erra mais ao preservar o que não mudou ou ao adicionar e "
             "atualizar informações?",
             "Para orientar o teste, formulei duas questões analíticas e as hipóteses.",
             "Diga só a pergunta-guia de cada objetivo (válido? certo? onde erra?).",
             ["a) é válido?", "b) está certo?", "c) onde erra: preservar × adicionar/atualizar"])


def hipoteses(d):
    s = d.new("hipoteses", "Metodologia · Seção 3.2", "Questões analíticas e hipóteses")
    bullets(s, [
        heading("Questões analíticas", size=20),
        "Como a conformidade estrutural e a fidelidade do estado evoluem ao longo da sequência "
        "de turnos de atualização?",
        "Como os escritores diferem entre as operações de preservação de atributos anteriores, "
        "adição de novos atributos e atualização de atributos existentes no SUMIE?",
        heading("Hipóteses", size=20, space_before=14),
        P("**H_{0}:** não há diferença estatisticamente significativa nas métricas primárias de "
          "fidelidade do estado (F1 do estado, acurácia de preservação e acurácia de "
          "atualização) entre os três modelos escritores sob o protocolo GU-JSON no SUMIE."),
        P("**H_{1}:** os representantes avaliados apresentam diferenças estatisticamente "
          "significativas na preservação do estado prévio e na incorporação de novas "
          "informações ao longo das transições, refletindo perfis de erro distintos sob o mesmo "
          "orçamento de geração.")], size=19, space_after=10)
    d.script(s, "Apresentar as questões analíticas e as hipóteses.",
             "Além da pergunta principal, há duas questões analíticas: como a conformidade e a "
             "fidelidade evoluem ao longo dos turnos, e como os escritores diferem entre "
             "preservar, adicionar e atualizar atributos. A hipótese nula é de que não há "
             "diferença significativa nas métricas primárias — F1 do estado e acurácias de "
             "preservação e de atualização. A alternativa é de que os escritores têm perfis de "
             "erro distintos sob o mesmo orçamento.",
             "Antes do experimento, a revisão sistemática delimitou os trabalhos relacionados.",
             "Leia só H0 e H1.",
             ["Duas questões analíticas: turnos e operações", "H0 × H1 nas métricas primárias"])


def build_a(d):
    for f in (capa, contexto, gu_json, justificativa, paradigmas, lacuna, pergunta, objetivos,
              hipoteses):
        f(d)
