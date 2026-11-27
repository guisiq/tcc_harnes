"""Slides principais 17–25: Quadros 6–8 (rastreabilidade), resultados esperados, limitações,
cronograma (Tabela 1), considerações finais, referências e encerramento."""

from __future__ import annotations

import referencias
from pptx_kit import *

_QUADROS = {
    "quadro6": ("Quadro 6 – Rastreabilidade do objetivo específico a: conformidade estrutural", [
        ("Objetivo específico", "a) Avaliar a conformidade estrutural dos ~~checkpoints~~ "
                                "produzidos por cada escritor"),
        ("Artefatos e procedimentos", "Analisador sintático de JSON, validador de esquema e log "
                                      "de saídas brutas sem reparo automático"),
        ("Evidências produzidas", "Tabela de validade por escritor, curva de validade por turno "
                                  "e distribuição das categorias de erro sintático (truncamento, "
                                  "chaves malformadas, texto extra)"),
        ("Métricas", "~~JSON Validity~~ e ~~Schema Validity~~"),
        ("Critério de análise", "Comparação das diferenças pareadas entre escritores."),
    ]),
    "quadro7": ("Quadro 7 – Rastreabilidade do objetivo específico b: fidelidade do estado", [
        ("Objetivo específico", "b) Comparar a fidelidade do estado mantido ao longo dos turnos "
                                "de atualização do SUMIE"),
        ("Artefatos e procedimentos", "Estados acumulados de referência (M^{*}_{t}), "
                                      "correspondência direta e juiz semântico condicional com "
                                      "acesso às anotações"),
        ("Evidências produzidas", "Tabelas estritas e híbridas, proporção de casos "
                                  "encaminhados/incertos e curvas longitudinais por escritor"),
        ("Métricas", "~~State Precision~~, ~~State Recall~~, ~~State F1~~ e ~~Hallucination "
                     "Rate~~"),
        ("Critério de análise", "Teste pareado entre escritores, com resultados estritos e "
                                "híbridos."),
    ]),
    "quadro8": ("Quadro 8 – Rastreabilidade do objetivo específico c: desempenho por operação", [
        ("Objetivo específico", "c) Analisar o perfil de erro dos escritores segundo o tipo de "
                                "operação no SUMIE"),
        ("Artefatos e procedimentos", "Rotulador de operações (PRESERVE, ADD, UPDATE) entre "
                                      "M^{*}_{t−1} e M^{*}_{t}"),
        ("Evidências produzidas", "Tabela e gráfico comparativo de desempenho estratificado por "
                                  "operação e curva de retenção de atributos ao longo dos turnos"),
        ("Métricas", "~~Preservation Accuracy~~ (primária) e ~~Update Accuracy~~ (ADD e UPDATE, "
                     "primária)"),
        ("Critério de análise", "Comparações pareadas entre escritores, com resultados "
                                "estratificados por operação."),
    ]),
}

_FALAS = {
    "quadro6": ("Mostrar como o objetivo a será respondido.",
                "O Quadro 6 liga o objetivo a às evidências. A conformidade estrutural é medida "
                "pelo analisador de JSON e pelo validador de esquema, sobre as saídas brutas sem "
                "reparo. As evidências são a validade por escritor, a curva por turno e os tipos "
                "de erro sintático — truncamento, chaves malformadas e texto extra.",
                "O objetivo b segue a mesma lógica.",
                ["JSON/Schema Validity", "Saídas brutas sem reparo", "Tipos de erro sintático"]),
    "quadro7": ("Mostrar como o objetivo b será respondido.",
                "No Quadro 7, a fidelidade do estado usa os estados de referência, a "
                "correspondência direta e o juiz condicional com as anotações. Produz tabelas "
                "estritas e híbridas, a proporção de casos enviados ao juiz ou incertos e curvas "
                "por turno, com teste pareado entre escritores.",
                "E o objetivo c olha para cada operação.",
                ["Precision, Recall, F1, Hallucination", "Estrito × híbrido",
                 "Curvas longitudinais"]),
    "quadro8": ("Mostrar como o objetivo c será respondido.",
                "No Quadro 8, o rotulador de operações separa PRESERVE, ADD e UPDATE. As "
                "evidências são o desempenho estratificado por operação e a curva de retenção "
                "de atributos ao longo dos turnos, com Preservation e Update Accuracy como "
                "métricas primárias.",
                "Com isso, chego às contribuições esperadas.",
                ["Rotulador PRESERVE/ADD/UPDATE", "Retenção ao longo dos turnos",
                 "Preservation e Update Accuracy"]),
}


def quadro(d, key):
    legenda, linhas = _QUADROS[key]
    s = d.new(key, "Metodologia · Seção 3.10", legenda, title_size=24)
    rows = [["Elemento", "Descrição"]] + [
        [{"t": a, "bold": True}, b] for a, b in linhas]
    add_table(s, MX, 1.7, rows, [3.2, 8.933], size=18, row_h=[0.45] + [0.82] * 5)
    fonte(s, 6.35, size=12)
    objetivo, fala, transicao, pontos = _FALAS[key]
    d.script(s, objetivo, fala, transicao, "Leia só as linhas Métricas e Evidências.", pontos)


def resultados(d):
    s = d.new("resultados", "Resultados · Seção 4.1",
              "Contribuições esperadas: quatro conjuntos de evidências")
    text(s, MX, 1.6, CW, 5.3, [
        P("**1. Robustez estrutural por escritor (objetivo a):** ~~JSON Validity~~ e ~~Schema "
          "Validity~~ em regime ~~prompt-only~~, com a classificação das falhas sintáticas "
          "(fechamento incompleto por limite de ~~tokens~~, omissão de delimitadores ou texto "
          "fora do objeto JSON)."),
        P("**2. Fidelidade global e longitudinal do estado (objetivo b):** precisão, revocação, "
          "F1 e alucinação nas visões condicional e global; curvas por turno t mostram como a "
          "qualidade degrada à medida que o estado cresce e se aproxima dos 1.200 ~~tokens~~."),
        P("**3. Perfil de erro por operação (objetivo c):** ~~Preservation~~ × ~~Update "
          "Accuracy~~ distinguem um modelo conservador — preserva M^{*}_{t−1}, mas falha em "
          "incorporar O_{t} — de um modelo que sobrescreve ou esquece campos válidos."),
        P("**4. Validade sintática × fidelidade semântica:** em que medida ~~checkpoints~~ "
          "válidos ainda omitem atributos ou alucinam valores; protocolo e ~~harness~~ "
          "reutilizáveis para avaliar escritores compactos de memória.")],
        size=19, space_after=16)
    d.script(s, "Apresentar o que o trabalho vai entregar, ligado aos objetivos.",
             "A Fase 2 deve produzir quatro conjuntos de evidências. Primeiro, a robustez "
             "estrutural de cada escritor, com a classificação das falhas, para ver se a difusão "
             "em blocos ou o encoder-decoder são mais ou menos estáveis que o decoder-only. "
             "Segundo, a fidelidade do estado ao longo dos turnos, mostrando como a qualidade "
             "degrada quando o estado se aproxima do limite. Terceiro, o perfil por operação, "
             "que distingue um modelo conservador de um que sobrescreve campos válidos. E "
             "quarto, quanto um JSON válido ainda pode estar errado — além de um protocolo e um "
             "harness reutilizáveis.",
             "Esses resultados têm limites claros.",
             "Leia só os quatro títulos.",
             ["1 estrutura · 2 estado no tempo · 3 operação · 4 válido ≠ correto",
              "Harness reutilizável"])


def limitacoes(d):
    s = d.new("limitacoes", "Metodologia · Seção 3.11",
              "Limitações metodológicas e ameaças à validade")
    bullets(s, [
        "**Validade interna:** os modelos não compartilham corpus de pré-treinamento, "
        "tokenizador nem pós-treinamento → as diferenças refletem o desempenho conjunto de cada "
        "representante na escala de ~0,6B, e não o efeito isolado da arquitetura.",
        P("Todos em regime ~~zero-shot~~ e ~~prompt-only~~, com precisão numérica padronizada e "
          "sem decodificação restrita externa.", bullet=True, level=1),
        "**Validade de construção:** o juiz local pode introduzir viés ou inconsistência.",
        P("Versão, quantização e ~~prompt~~ congelados; decisões cegas ao escritor; incertos "
          "reportados; amostra auditada; resultados estritos sem juiz também divulgados.",
          bullet=True, level=1),
        "**Validade externa:** restrita à sumarização incremental de entidades em esquema plano "
        "chave-valor sob GU-JSON.",
        P("Transições com estado de referência em cada turno; não mede o impacto do "
          "~~checkpoint~~ nas decisões finais do agente.", bullet=True, level=1)],
        size=19, space_after=10)
    d.script(s, "Reconhecer os limites antes que a banca pergunte.",
             "Há três ameaças. Validade interna: os modelos diferem em pré-treinamento, "
             "tokenizador e ajuste, então comparo representantes, e não o paradigma isolado; "
             "para não somar distorções, todos rodam zero-shot, sem decodificação restrita. "
             "Validade de construção: o juiz pode ter viés, por isso ele é congelado, cego ao "
             "escritor e auditado, e também reporto resultados sem juiz. Validade externa: os "
             "resultados valem para esse esquema plano e para transições com estado de "
             "referência, sem medir o agente completo.",
             "Por fim, o cronograma.",
             "Diga as três palavras: interna, construção, externa.",
             ["Representantes, não paradigma isolado", "Juiz congelado, cego e auditado",
              "Esquema plano; sem agente completo"])


MESES = ["ago.", "set.", "out.", "nov.", "dez.", "fev.", "mar.", "abr.", "mai.", "jun."]
GANTT_Q = [(1, 2), (1, 4), (3, 6), (4, 6), (3, 8), (7, 9), (10, 12), (11, 14), (12, 14),
           (15, 15), (16, 17), (18, 18), (18, 19), (12, 19), (20, 20)]
ATIV_CURTAS = [
    "Tema, problema e objetivos",
    "Bibliografia e revisão sistemática",
    "Protocolo experimental",
    "Disponibilidade e licenças dos modelos e do SUMIE",
    "Redação e revisão do projeto de TCC I",
    "Apresentação do TCC I e recomendações da banca",
    "Preparação do SUMIE (M^{*}_{t} e rótulos)",
    "Estrutura base do ~~harness~~",
    "Fase 0 (verificação funcional)",
    "Fase 1 (piloto) e calibração da normalização",
    "Fase 2 (experimento principal)",
    "Processamento estatístico",
    "Tabelas, gráficos e análise crítica",
    "Redação do artigo final (TCC II)",
    "Revisão, depósito final e defesa do TCC II",
]


def cronograma(d):
    s = d.new("cronograma", "Resultados · Seção 4.2",
              "Cronograma: TCC I (2026/2) e TCC II (2027/1)")
    tw = 0.6 + 0.33 * 20
    caption(s, 1.42, "Tabela 1 – Cronograma de atividades para TCC I e II, com subdivisão "
                     "quinzenal indicando tarefas realizadas e planejadas ao longo dos dois "
                     "semestres.", w=tw, size=12, h=0.45)
    hdr1 = [""] + sum(([{"t": m, "size": 10}, ""] for m in MESES), [])
    hdr2 = [{"t": "Ativ.", "size": 9}] + [{"t": f"Q{q}", "size": 8} for q in range(1, 21)]
    body = []
    for i, (a, b) in enumerate(GANTT_Q, start=1):
        row = [{"t": f"{i}-", "bold": True, "size": 10}]
        for q in range(1, 21):
            row.append({"t": "", "fill": GANTT} if a <= q <= b else "")
        body.append(row)
    merges = [(0, 1 + 2 * k, 0, 2 + 2 * k) for k in range(10)]
    add_table(s, MX, 1.95, [hdr1, hdr2] + body, [0.6] + [0.33] * 20, header_rows=2,
              size=10, merges=merges, row_h=0.27)
    fonte(s, 6.62, w=tw)
    text(s, 8.05, 1.42, 4.68, 0.36, "**Atividades (Seção 4.2)**", size=13, space_after=0)
    text(s, 8.05, 1.85, 4.68, 4.9,
         [P(f"**{i}.** {t}") for i, t in enumerate(ATIV_CURTAS, start=1)],
         size=12, space_after=3)
    d.script(s, "Mostrar o planejamento e onde estou nele.",
             "O cronograma está em quinzenas. No TCC I, de agosto a dezembro de 2026, ficam a "
             "delimitação do tema, a revisão, o protocolo, a redação e esta apresentação; em "
             "dezembro começa a preparação do SUMIE. No TCC II, de fevereiro a junho de 2027, "
             "vêm o harness, as três fases, a análise estatística, a redação do artigo final e a "
             "defesa.",
             "Para fechar, as considerações finais.",
             "Diga só a divisão TCC I × TCC II.",
             ["TCC I: Q1–Q10 (ago.–dez./2026)", "TCC II: Q11–Q20 (fev.–jun./2027)"])


def consideracoes(d):
    s = d.new("consideracoes", "Considerações finais · Seção 5", "Considerações finais")
    bullets(s, [
        "A confiabilidade de agentes de múltiplas etapas depende da **integridade do estado** "
        "persistido; regenerar o ~~checkpoint~~ GU-JSON a cada turno o torna vulnerável a "
        "falhas sintáticas e à perda ou distorção de informações.",
        "Investigar se modelos compactos reescrevem esse estado com fidelidade — e como cada "
        "paradigma gerativo se comporta — é passo necessário para **componentes locais de "
        "memória** em sistemas agênticos.",
        "**Protocolo controlado** no SUMIE: método, esquema, ~~prompt zero-shot~~ e 1.200 "
        "~~tokens~~ fixos; varia só o escritor — Qwen3-0.6B, T5Gemma B-B e Qwen3-0.6B BD3LM.",
        "Dissociar **conformidade estrutural**, **fidelidade semântica** e **acurácia por "
        "operação** permitirá caracterizar os modos de falha de cada escritor ao longo dos "
        "turnos.",
        "Resultados circunscritos aos três representantes, ao formato plano e às transições com "
        "estado de referência: **sem prova causal isolada** sobre arquiteturas."],
        size=19, space_after=12)
    d.script(s, "Fechar retomando problema, proposta e limites.",
             "Para concluir: a confiabilidade de um agente depende da integridade do estado, e "
             "reescrever o checkpoint a cada turno o deixa vulnerável. Saber se modelos "
             "compactos fazem essa reescrita com fidelidade — e como cada paradigma se comporta "
             "— é um passo para memórias locais em agentes. O projeto propõe um protocolo "
             "controlado, em que só o escritor varia, e que separa estrutura, conteúdo e "
             "operação. Os resultados valerão para esses três representantes, sem prova causal "
             "sobre arquiteturas.",
             "Estas são as principais referências.",
             "Leia só o primeiro e o último marcador.",
             ["Estado íntegro = agente confiável", "Protocolo: só o escritor varia",
              "Sem prova causal isolada"])


def refs(d):
    s = referencias.slide_principais(d)
    d.script(s, "Mostrar as referências centrais sem lê-las.",
             "Aqui estão as principais referências do trabalho; a lista completa está no final "
             "do apêndice.",
             "",
             "Passe direto.",
             ["Referências centrais; lista completa no apêndice"])


def obrigado(d):
    s = d.new("obrigado", footer=False)
    rect(s, 0, 0, SLIDE_W, 0.16, NAVY)
    rect(s, 0, 0.16, SLIDE_W, 0.05, ACCENT)
    text(s, MX, 1.9, CW, 1.1, "Obrigado!", size=54, bold=True, color=NAVY, align="center",
         anchor="middle")
    text(s, MX, 3.05, CW, 0.5, "Perguntas e contribuições da banca", size=24, color=ACCENT,
         align="center", bold=True)
    text(s, MX, 3.95, CW, 1.0, [
        "**Guilherme Henrique Siqueira Lopes** · Orientador: Prof. Me. Alex Coelho",
        "Bacharelado em Sistemas de Informação — UNITINS"], size=18, align="center",
         space_after=4)
    text(s, MX, 5.25, CW, 0.75, [
        "Artefatos da revisão sistemática (v2.1.0):",
        "github.com/guisiq/tcc_revisao_sistematica_sumarizacao_recorrente"],
         size=15, color=MUTED, align="center", space_after=2)
    rect(s, 0, SLIDE_H - 0.12, SLIDE_W, 0.12, NAVY)
    d.script(s, "Encerrar e abrir para a arguição.",
             "Era isso. Agradeço a atenção da banca e do meu orientador, e fico à disposição "
             "para as perguntas e contribuições.",
             "",
             "Não corte.",
             ["Agradecer", "Abrir para perguntas"])


def build_c(d):
    for k in ("quadro6", "quadro7", "quadro8"):
        quadro(d, k)
    for f in (resultados, limitacoes, cronograma, consideracoes, refs, obrigado):
        f(d)
