"""Slides principais 10–16: revisão sistemática, desenho (Quadro 3), SUMIE, Figuras 2 e 1,
métricas e fases. Layout único: etiqueta + título + lista, quadro ou figura do artigo."""

from __future__ import annotations

from pptx_kit import *


def revisao(d):
    s = d.new("revisao", "Metodologia · Seção 3.1",
              "Revisão sistemática: 738 candidatos → 12 estudos no núcleo")
    bullets(s, [
        "**Protocolo versionado:** questão orientadora, fonte, consultas, livro de códigos e "
        "regras lidos pelos ~~scripts~~; janela de **1º/07/2025 a 19/11/2026**.",
        "**Fonte:** API do arXiv (título e resumo); **8 consultas** que combinam facetas do "
        "problema (Quadro 2).",
        "**12 estudos de controle**, usados para compor as consultas: todos recuperados.",
        "**Deduplicação:** 738 candidatos; termos de exclusão no título removeram 42 → "
        "**696**.",
        "**Triagem por título e resumo:** sim, incerto ou não para sete características "
        "(C1–C7); grupos atribuídos por regras do ~~script~~ → **189** seguiram.",
        "**Elegibilidade com texto integral:** cada característica presente exigiu um **trecho "
        "literal** conferido no texto → **12 estudos no núcleo** (C1 a C6 presentes).",
        "**Extração:** representação da memória, mecanismo de atualização, modelos e escala, "
        "objeto da avaliação e comparação entre paradigmas → **Quadro 1**."], size=18,
        space_after=9)
    d.script(s, "Mostrar que a lacuna foi delimitada por um procedimento reprodutível.",
             "A lacuna veio de uma revisão sistemática com protocolo versionado. Busquei no "
             "arXiv, por título e resumo, trabalhos depositados entre julho de 2025 e novembro "
             "de 2026, com oito consultas que combinam as facetas do problema. Doze estudos de "
             "controle foram todos recuperados. Foram 738 candidatos; termos de exclusão "
             "deixaram 696. A triagem codificou sete características por título e resumo e "
             "levou 189 estudos ao texto integral, em que cada característica precisou de um "
             "trecho literal. Ficaram 12 estudos no núcleo, que compõem o Quadro 1.",
             "Com a lacuna definida, passo ao desenho do experimento.",
             "Diga só o funil: 738 → 696 → 189 → 12.",
             ["arXiv, 8 consultas, controles recuperados", "Funil 738 → 696 → 189 → 12",
              "Trecho literal na elegibilidade"])


_Q3 = [
    ("Independente", "Modelo escritor",
     "Qwen3-0.6B (autoregressivo ~~decoder-only~~); T5Gemma B-B PrefixLM-IT "
     "(~~encoder-decoder~~); Qwen3-0.6B Diffusion BD3LM (difusão em blocos)"),
    ("Controlada", "Método de atualização",
     "GU-JSON, com reescrita integral do ~~checkpoint~~ a cada turno"),
    ("Controlada", "Esquema",
     '{"state": {"chave": "valor"}}, idêntico para todos os escritores e instâncias'),
    ("Controlada", "~~Prompt~~",
     "~~Prompt-base zero-shot~~ em inglês, sem instruções específicas por arquitetura"),
    ("Controlada", "Orçamento de saída",
     "Limite máximo fixo de 1.200 ~~tokens~~ gerados por transição"),
    ("Controlada", "Contexto de entrada", "Limite de até 8.192 ~~tokens~~"),
    ("Controlada", "Dados de entrada",
     "Mesmas sequências do SUMIE, na mesma ordem, com os mesmos estados anteriores de "
     "referência"),
    ("Controlada", "Decodificação",
     "Geração determinística apenas por instrução (~~prompt-only~~), sem decodificação "
     "restrita por gramática"),
    ("Dependente", "Conformidade estrutural",
     "Taxa de validade sintática do JSON (~~JSON Validity~~) e taxa de conformidade com o "
     "esquema (~~Schema Validity~~)"),
    ("Dependente", "Fidelidade global do estado",
     "Precisão (~~State Precision~~), revocação (~~State Recall~~), F1 do estado "
     "(~~State F1~~) e taxa de alucinação (~~Hallucination Rate~~)"),
    ("Dependente", "Fidelidade por operação",
     "Acurácia de preservação (~~Preservation Accuracy~~) e acurácia de atualização "
     "(~~Update Accuracy~~, desdobrada em adição e modificação)"),
]


def desenho(d):
    s = d.new("desenho", "Metodologia · Seção 3.2",
              "Desenho experimental: uma única variável independente")
    caption(s, 1.45, "Quadro 3 – Variáveis do experimento")
    rows = [["Tipo", "Variável", "Operacionalização"]] + [list(r) for r in _Q3]
    heights = [0.32, 0.5] + [0.3] * 5 + [0.5, 0.5, 0.5, 0.5]
    add_table(s, MX, 1.82, rows, [1.55, 2.75, 7.833], size=12.5, row_h=heights)
    fonte(s, 6.62)
    d.script(s, "Mostrar o controle experimental: só o escritor muda.",
             "O Quadro 3 resume o desenho. A única variável independente é o modelo escritor. "
             "Ficam constantes o método GU-JSON, o esquema, o prompt zero-shot em inglês, o "
             "limite de 1.200 tokens de saída e 8.192 de entrada, as mesmas sequências do SUMIE "
             "e a decodificação determinística, sem gramática restrita. As variáveis dependentes "
             "acompanham os três objetivos: conformidade estrutural, fidelidade global do estado "
             "e fidelidade por operação.",
             "Os dados vêm do benchmark SUMIE.",
             "Aponte só a primeira linha e as três últimas.",
             ["Única VI: o escritor", "Constantes: método, esquema, prompt, 1.200 tokens, dados",
              "Três grupos de VD = três objetivos"])


def sumie(d):
    s = d.new("sumie", "Metodologia · Seção 3.4",
              "SUMIE: cada turno vira uma transição com operação rotulada")
    bullets(s, [
        "~~Benchmark~~ SUMIE (Hwang et al., 2025; Apache-2.0): cada instância é uma **entidade** "
        "descrita por uma sequência ordenada de parágrafos, com anotações de atributos e "
        "valores."], y=1.55, h=0.95, size=18)
    equation(s, 2.45, 0.7, "( M^{*}_{t−1} ,  O_{t} ,  M^{*}_{t} )", size=30)
    text(s, MX, 3.12, CW, 0.42,
         "**M^{*}_{t−1}** estado acumulado de referência até t−1 · **O_{t}** parágrafo do turno t "
         "· **M^{*}_{t}** estado acumulado esperado", size=15, color=MUTED, align="center",
         space_after=0)
    bullets(s, [
        "Cada atributo esperado em M^{*}_{t} recebe um **rótulo determinístico** de operação:",
        P("**PRESERVE:** já presente em M^{*}_{t−1}, sem alteração em O_{t}; deve ser mantido "
          "intacto.", bullet=True, level=1),
        P("**ADD:** ausente em M^{*}_{t−1} e introduzido pela primeira vez em O_{t}.",
          bullet=True, level=1),
        P("**UPDATE:** já existente, recebe informação complementar ou nova perspectiva, "
          "integrando visões divergentes sem descartar o registro anterior.", bullet=True,
          level=1),
        "Os estados esperados devem caber nos **1.200 ~~tokens~~**: omissões são atribuídas ao "
        "escritor, e não a truncamento."], y=3.65, size=18, space_after=8)
    d.script(s, "Explicar a transição e os três rótulos de operação.",
             "Os dados vêm do SUMIE, um benchmark público em que cada instância é uma entidade "
             "descrita parágrafo a parágrafo, com anotações de atributos e valores. Cada turno "
             "vira uma tupla: o estado de referência até o turno anterior, o parágrafo novo e o "
             "estado esperado depois dele. Comparando os dois estados, cada atributo recebe um "
             "rótulo: PRESERVE, se deve ser mantido; ADD, se é novo; e UPDATE, se recebe "
             "informação complementar. E os estados esperados precisam caber nos 1.200 tokens, "
             "para que uma omissão seja culpa do escritor, e não do limite.",
             "A Figura 2 mostra o que o escritor recebe e o que devolve.",
             "Diga só a tupla e os três rótulos.",
             ["Tupla (M*t−1, Ot, M*t)", "PRESERVE / ADD / UPDATE", "Estados cabem em 1.200 tokens"])


def figura2(d):
    s = d.new("fig2", "Metodologia · Seção 3.7",
              "Entrada e saída do escritor em uma transição")
    caption(s, 1.45, "Figura 2 – Etapa de escrita do ~~checkpoint~~ (etapas ii e iii)")
    d.img(s, "fig2", 0.87, 1.88, w=11.59, h=4.75)
    fonte(s, 6.66, "Fonte: elaborado pelo autor (2026), com exemplo extraído do SUMIE "
                   "(Hwang et al., 2025).")
    d.script(s, "Mostrar o prompt preenchido e a saída esperada.",
             "Aqui está a etapa de escrita. A entrada é o prompt-base do Apêndice A já "
             "preenchido: o texto de instrução e o esquema são fixos; o estado anterior e a nova "
             "observação vêm do SUMIE, nos campos CURRENT STATE e NEW OBSERVATION. O escritor "
             "completa o UPDATED STATE com o objeto JSON completo. No exemplo, é o primeiro "
             "parágrafo de uma entidade, então o estado anterior é vazio, e o JSON à direita é a "
             "anotação do SUMIE, não a saída de um modelo.",
             "Essa etapa está dentro de um harness com nove etapas.",
             "Aponte os três campos e diga que o JSON é a anotação.",
             ["Prompt fixo + esquema S", "CURRENT STATE / NEW OBSERVATION / UPDATED STATE",
              "JSON do exemplo = anotação do SUMIE"])


def harness(d):
    s = d.new("harness", "Metodologia · Seções 3.6 e 3.7",
              "~~Harness~~ experimental: nove etapas por transição")
    caption(s, 1.45, "Figura 1 – Visão geral do ~~harness~~ experimental para uma transição "
                     "do SUMIE", w=6.6, size=12, h=0.4)
    d.img(s, "fig1", MX, 1.88, w=6.6, h=4.72)
    fonte(s, 6.64, "Fonte: elaborado pelo autor (2026), a partir do protocolo descrito na "
                   "Seção 3.", w=6.6, size=10)
    bullets(s, [
        "**Execução (i–iv):** ler a transição, montar o ~~prompt~~, gerar sob 1.200 ~~tokens~~ e "
        "gravar a saída bruta em disco.",
        "**Avaliação (v–ix):** sintaxe, esquema, correspondência direta, juiz só para "
        "divergências e registros JSON.",
        "Só S, M^{*}_{t−1} e O_{t} entram no ~~prompt~~; M^{*}_{t} e os rótulos seguem por "
        "**caminho separado**.",
        "Cada transição parte do estado de referência: **erros não se propagam**.",
        "**Nenhum reparo** na saída do escritor; o juiz não recebe a identidade do "
        "escritor."], x=7.45, w=5.28, y=1.55, size=16, space_after=10)
    d.script(s, "Explicar o fluxo do harness e as garantias do protocolo.",
             "A Figura 1 mostra o harness completo. Na execução, ele lê a transição, monta o "
             "prompt, chama o escritor com o limite de 1.200 tokens e grava a saída bruta antes "
             "de qualquer validação. Na avaliação, verifica a sintaxe e o esquema, faz a "
             "correspondência direta e só manda ao juiz o que divergir. Três garantias: a "
             "resposta esperada segue por um caminho separado e nunca chega ao escritor; cada "
             "transição parte do estado de referência, então os erros não se propagam; e nada é "
             "reparado.",
             "Dessas saídas saem as métricas.",
             "Diga execução, avaliação e as três garantias.",
             ["Execução i–iv / avaliação v–ix", "Esperado nunca entra no prompt",
              "Sem propagação, sem reparo"])


def metricas(d):
    s = d.new("metricas", "Metodologia · Seção 3.8",
              "Métricas: estrutura, estado e operação")
    bullets(s, [
        "**Estruturais** (todas as transições): ~~JSON Validity~~ — interpretável por json.loads "
        "sem reparo — e ~~Schema Validity~~.",
        "**Estado:** o JSON vira pares caminho-valor (\"state.<atributo>\", valor normalizado), "
        "sem considerar a ordem das chaves.",
        P("~~State Precision~~, ~~State Recall~~, ~~State F1~~ (primária) e ~~Hallucination "
          "Rate~~.", bullet=True, level=1),
        "**Operação:** ~~Preservation Accuracy~~ (PRESERVE) e ~~Update Accuracy~~ (ADD e "
        "UPDATE) — primárias.",
        "**Correspondência:** primeiro direta, após normalização; só as divergências vão ao "
        "juiz local (equivalente, ausente/contradito ou incerto). Incertos não contam como "
        "acerto.",
        "**Duas visões:** condicional à validade estrutural e global, com pontuação zero para "
        "falha sintática.",
        "Resultados **estritos** e **híbridos** (com juiz) reportados separadamente."],
        size=18, space_after=9)
    d.script(s, "Ligar as métricas aos objetivos e explicar o papel do juiz.",
             "As métricas seguem os três objetivos. As estruturais medem se a saída é um JSON "
             "válido sem reparo e se respeita o esquema. As de estado convertem o JSON em pares "
             "atributo-valor e calculam precisão, revocação, F1 e alucinação. As de operação "
             "medem preservação e atualização. A comparação é primeiro direta; só o que diverge "
             "vai ao juiz local, e casos incertos não contam como acerto. Reporto duas visões — "
             "só saídas válidas e global, com zero para falha — e resultados estritos e "
             "híbridos.",
             "Essas métricas são coletadas em três fases.",
             "Diga os três grupos e 'juiz só para divergências'.",
             ["Estrutura / estado / operação", "Juiz só para divergências; incerto ≠ acerto",
              "Condicional × global; estrito × híbrido"])


def fases(d):
    s = d.new("fases", "Metodologia · Seções 3.6 e 3.9",
              "Procedimento em três fases e plano de análise")
    bullets(s, [
        "**Fase 0 — verificação funcional:** 15 transições sintéticas para validar escritores, "
        "juiz, limite de 1.200 ~~tokens~~, analisador, esquema e registros; juiz ≤ 4 GiB.",
        "**Fase 1 — piloto:** 25 entidades separadas da amostra principal; fixa a normalização, "
        "verifica o comprimento de M^{*}_{t} e audita o juiz, que é **congelado** antes da Fase 2.",
        "**Fase 2 — experimento principal:** os três escritores em todo o conjunto de avaliação "
        "do SUMIE.",
        "**Análise:** média e mediana; diferenças pareadas no nível de entidade; **Friedman** "
        "(global) e **Wilcoxon** pareado com correção de **Holm-Bonferroni**, α = 0,05; curvas "
        "de ~~State F1~~, ~~Preservation Accuracy~~ e ~~JSON Validity~~ por turno t.",
        "**Ambiente:** Lenovo IdeaPad Gaming 3i — Intel Core i5 10ª geração, 24 GB de RAM e "
        "NVIDIA GTX 1650; ponto flutuante uniforme entre os modelos."], size=18, space_after=11)
    d.script(s, "Apresentar as fases e a análise estatística.",
             "O procedimento tem três fases. A Fase 0 verifica o harness com 15 transições "
             "sintéticas. A Fase 1 é um piloto com 25 entidades, separadas da amostra principal, "
             "para fixar a normalização, conferir o tamanho dos estados e auditar o juiz, que "
             "fica congelado antes da Fase 2. A Fase 2 roda os três escritores em todo o "
             "conjunto de avaliação. Como todos veem as mesmas transições, a análise é pareada: "
             "Friedman para os três modelos e Wilcoxon com correção de Holm nas comparações dois "
             "a dois, com alfa de 5%. Tudo roda localmente, num notebook com GTX 1650.",
             "Os Quadros 6 a 8 ligam cada objetivo às evidências.",
             "Diga as três fases e 'Friedman + Wilcoxon/Holm'.",
             ["Fase 0: 15 sintéticas / Fase 1: 25 entidades / Fase 2: completo",
              "Friedman + Wilcoxon/Holm, α = 0,05", "Execução local (GTX 1650)"])


def build_b(d):
    for f in (revisao, desenho, sumie, figura2, harness, metricas, fases):
        f(d)
