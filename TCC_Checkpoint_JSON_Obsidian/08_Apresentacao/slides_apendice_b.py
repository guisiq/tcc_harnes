"""Apêndice (parte 2): prompt, harness, modelos, juiz, métricas, estatística, cronograma e
referências. Mesmo layout uniforme da parte 1 (listas ou quadros fiéis ao artigo)."""

from __future__ import annotations

from pptx_kit import *
from referencias import slides_apendice as refs_apendice
from slides_apendice_a import ap, build_apendice_a, indice
from slides_principais_c import GANTT_Q, MESES

PROMPT = """You are the memory-state updater of an autonomous agent.

Your task is to update a persistent JSON state.

Rules:
1. Preserve existing information that is still valid.
2. Apply information explicitly introduced by the new observation.
3. Replace old facts only when the observation or task explicitly establishes
   that they are no longer valid. Preserve differing opinions and still-valid
   perspectives rather than assuming that the newest opinion wins.
4. Do not invent unsupported facts.
5. Respect the schema.
6. Return only the complete updated JSON object.

SCHEMA:
{{SCHEMA}}

CURRENT STATE:
{{CURRENT_STATE}}

NEW OBSERVATION:
{{OBSERVATION}}

UPDATED STATE:"""


def prompt(d):
    s = ap(d, "prompt", "Método · Seção 3.3 e Apêndice A", "~~Prompt-base~~ do escritor de memória")
    text(s, MX, 1.5, 7.3, 5.4, [P(line, space_after=0) for line in PROMPT.split("\n")],
         font="Consolas", size=11.5, markup=False, lang="en-US", color=NAVY, space_after=0)
    bullets(s, [
        heading("Marcadores substituídos pelo ~~harness~~", size=16),
        "**{{SCHEMA}}** → sempre o mesmo esquema S",
        "**{{CURRENT_STATE}}** → M^{*}_{t−1}",
        "**{{OBSERVATION}}** → O_{t}",
        "Em inglês, idioma dos dados e dos modelos; idêntico para os três escritores.",
        heading("Seis instruções (Seção 3.3)", size=16, space_before=8),
        "preservar o que continua válido;",
        "incorporar o que a observação introduz;",
        "substituir só com invalidade explícita, mantendo perspectivas divergentes;",
        "não inventar fatos; respeitar o esquema;",
        "retornar só o objeto JSON completo.",
    ], y=1.5, x=8.05, w=4.68, size=14, space_after=4)
    d.apoio(s, ["Esquema mínimo {\"state\": {\"chave\": \"valor\"}}; orçamento de 1.200 tokens.",
                "A regra 3 traduz a política de acumulação do SUMIE."])


_Q4 = [("(i) Preparar transição", "Script de preparação sobre o SUMIE; rotulador "
        "PRESERVE/ADD/UPDATE (Seção 3.4)", "Fixo; regras congeladas após a Fase 1",
        "Tupla (M^{*}_{t−1}, O_{t}, M^{*}_{t}), anotações e rótulos"),
       ("(ii) Montar ~~prompt~~", "~~Prompt-base~~ do Apêndice A: texto e esquema S fixos; "
        "M^{*}_{t−1} e O_{t} inseridos a cada transição", "Fixo",
        "~~Prompt~~ preenchido, entrada do escritor, registrado na proveniência"),
       ("(iii) Gerar ~~checkpoint~~", "Adaptador do escritor: Qwen3-0.6B, T5Gemma B-B ou "
        "Qwen3-0.6B BD3LM (Seções 3.5 e 3.6)", "Variável: um escritor por execução; limite de "
        "1.200 ~~tokens~~ fixo", "Texto produzido M_{t}"),
       ("(iv) Gravar saída bruta", "Arquivo em disco, sem reparo", "Fixo",
        "Saída original do escritor"),
       ("(v) Validar sintaxe", "Analisador JSON padrão (json.loads)", "Fixo",
        "~~JSON Validity~~"),
       ("(vi) Validar esquema", 'Validador do esquema {"state": {"chave": "valor"}}', "Fixo",
        "~~Schema Validity~~"),
       ("(vii) Correspondência direta", "Comparação de pares caminho-valor normalizados",
        "Fixo; normalização definida na Fase 1", "Resultados estritos e divergências"),
       ("(viii) Julgamento semântico", "Gemma 3 1B Instruct em GGUF Q4_K_M, executado "
        "localmente", "Fixo; congelado antes da Fase 2; acionado só para divergências",
        "Decisões híbridas e casos incertos"),
       ("(ix) Registrar", "Registros JSON", "Fixo", "Métricas por transição, turno e operação")]


def quadro4(d):
    s = ap(d, "quadro4", "Método · Seção 3.7",
           "Quadro 4 – Etapas do ~~harness~~, tecnologias e artefatos produzidos")
    rows = [["Etapa", "Componente e tecnologia", "Controle", "Saída usada na avaliação"]]
    rows += [list(r) for r in _Q4]
    add_table(s, MX, 1.5, rows, [2.1, 4.5, 3.0, 2.533], size=12,
              row_h=[0.4, 0.6, 0.6, 0.6, 0.34, 0.34, 0.34, 0.45, 0.6, 0.34])
    fonte(s, 6.62)
    d.apoio(s, ["Só a etapa (iii) varia: o escritor. Todas as outras são fixas.",
                "A saída é gravada antes de validar; nenhum reparo é aplicado.",
                "O identificador do escritor não vai no pedido de julgamento."])


def modelos(d):
    s = ap(d, "modelos", "Método · Seções 3.5 e 3.6",
           "Modelos escritores, adaptadores e ambiente de execução")
    bullets(s, [
        heading("3.5 Modelos avaliados (~0,6B, pesos abertos, execução local)", size=16),
        "**Qwen3-0.6B** (Yang et al., 2025): autoregressivo ~~decoder-only~~, licença "
        "Apache-2.0; linha de base autoregressiva.",
        "**T5Gemma B-B PrefixLM-IT** (Zhang et al., 2025): ~~encoder-decoder~~ ajustado por "
        "instruções, com codificador bidirecional e decodificador autoregressivo.",
        "**Qwen3-0.6B Diffusion BD3LM** (Arriola et al., 2025): difusão discreta em blocos, "
        "com geração sequencial de blocos e refinamento paralelo de ~~tokens~~ mascarados.",
        "Diferenças de pré-treinamento, tokenização e ajuste por instruções → sem causalidade "
        "exclusiva do paradigma; ~~commit hashes~~ e configuração numérica no manifesto.",
        heading("3.6 Adaptadores e ambiente", size=16, space_before=8),
        "Adaptadores aplicam só o ~~template~~ de conversa e os ~~tokens~~ especiais de cada "
        "tokenizador, sem alterar o ~~prompt-base~~; ~~thinking~~ do Qwen3-0.6B desativado.",
        "Decodificação determinística, sem amostragem e com semente fixa; no BD3LM, tamanho de "
        "bloco, passos de remoção de ruído e critério de desmascaramento fixados.",
        "Lenovo IdeaPad Gaming 3i: Intel Core i5 (10ª geração), 24 GB de RAM e NVIDIA GeForce "
        "GTX 1650; ponto flutuante uniforme entre os modelos (FP16 ou BF16).",
    ], y=1.5, size=15, space_after=5)
    d.apoio(s, ["Critérios de seleção: ~0,6B, pesos abertos e execução local.",
                "Contexto de entrada até 8.192 tokens; saída até 1.200 tokens (Quadro 3)."])


def juiz(d):
    s = ap(d, "juiz", "Método · Seções 3.6, 3.8 e 3.11", "Juiz semântico local")
    bullets(s, [
        heading("Configuração", size=16),
        "Gemma 3 1B Instruct (google/gemma-3-1b-it), independente dos escritores; GGUF Q4_K_M, "
        "execução local, licença Gemma.",
        "Aceito no piloto só se o pico de memória residente do processo não exceder 4 GiB; "
        "registra versão, ~~hash~~ dos pesos, ambiente, tamanho de contexto e latência.",
        heading("Funcionamento", size=16, space_before=6),
        "Acionado só para pares divergentes após a correspondência direta; recebe M^{*}_{t−1}, "
        "O_{t}, M^{*}_{t}, as anotações pertinentes e o estado gerado M_{t}, sem a identidade "
        "do escritor.",
        "Decide: equivalente, ausente/contradito ou incerto; a equivalência só conta se apoiada "
        "nas anotações e compatível com a política de acumulação; correspondência um-para-um.",
        "Incertos não contam como acerto e são reportados à parte; não infere suporte por "
        "plausibilidade geral.",
        heading("Controle de viés", size=16, space_before=6),
        "Versão, quantização e ~~prompt~~ congelados antes da Fase 2; decisões cegas ao "
        "escritor; amostra auditada manualmente no piloto.",
        "Divulgados: resultados estritos sem juiz, frequência de casos enviados ao juiz, "
        "incertos e pico de memória.",
    ], y=1.5, size=15, space_after=4)
    d.apoio(s, ["A avaliação original do SUMIE também usa modelo de linguagem como juiz.",
                "Métricas primárias = procedimento híbrido; estritas = transparência."])


_Q5 = [("Estrutural", "Validade do JSON (~~JSON Validity~~)", "Proporção de saídas brutas "
        "interpretáveis por json.loads sem reparo sintático", "Todas as transições"),
       ("Estrutural", "Conformidade com o esquema (~~Schema Validity~~)", "Proporção de saídas "
        "que contêm exclusivamente o objeto raiz state mapeando chaves textuais a valores",
        "Todas as transições"),
       ("Estado", "Precisão do estado (~~State Precision~~)", "Fração dos pares atributo-valor "
        "gerados em M_{t} que correspondem diretamente ou são julgados semanticamente "
        "equivalentes e sustentados pelas anotações (Equação 2)",
        "Transições válidas; reporte híbrido e estrito"),
       ("Estado", "Revocação do estado (~~State Recall~~)", "Fração dos fatos esperados em "
        "M^{*}_{t} representados diretamente ou por equivalência semântica julgada em M_{t} "
        "(Equação 3)", "Transições válidas; reporte híbrido e estrito"),
       ("Estado", "F1 do estado (~~State F1~~)", "Média harmônica entre precisão e revocação; "
        "métrica semântica primária no procedimento híbrido",
        "Transições válidas; reporte híbrido e estrito"),
       ("Estado", "Taxa de alucinação (~~Hallucination Rate~~)", "Proporção de pares gerados "
        "sem correspondência esperada e sem suporte nas anotações, em M^{*}_{t−1} ou em O_{t}; "
        "divergências não exatas são submetidas ao juiz", "Transições com JSON válido"),
       ("Operação", "Acurácia de preservação (~~Preservation Accuracy~~)", "Fração dos "
        "atributos de M^{*}_{t−1} não alterados por O_{t} que foram retidos corretamente "
        "(Equação 6); métrica primária", "Atributos rotulados como PRESERVE"),
       ("Operação", "Acurácia de atualização (~~Update Accuracy~~)", "Fração das inclusões e "
        "modificações introduzidas por O_{t} aplicadas corretamente (Equação 5), reportada de "
        "forma agregada e separada para ADD e UPDATE; métrica primária",
        "Atributos rotulados como ADD ou UPDATE")]


def quadro5(d):
    s = ap(d, "quadro5", "Método · Seção 3.8", "Quadro 5 – Métricas de avaliação do experimento")
    rows = [["Categoria", "Métrica", "Definição operacional", "Escopo de cálculo"]]
    rows += [list(r) for r in _Q5]
    add_table(s, MX, 1.45, rows, [1.15, 2.6, 5.85, 2.533], size=11.5,
              row_h=[0.38, 0.45, 0.5, 0.62, 0.5, 0.5, 0.62, 0.62, 0.62])
    fonte(s, 6.62)
    d.apoio(s, ["Estruturais sobre todas as transições; semânticas sobre as válidas (visão "
                "condicional) ou com zero nas inválidas (visão global).",
                "Primárias: State F1, Preservation Accuracy e Update Accuracy."])


def _frac(s, x, y, w, lhs, num, den, eq, size=15, font="Calibri", lhs_w=1.0):
    """Fração em texto, com traço fino; número da equação à direita."""
    text(s, x, y, lhs_w, 0.95, lhs, size=size + 6, font="Cambria Math", color=NAVY,
         anchor="middle", align="right", space_after=0)
    fx, fw = x + lhs_w + 0.1, w - lhs_w - 0.85
    text(s, fx, y, fw, 0.46, num, size=size, font=font, align="center", anchor="bottom",
         space_after=0)
    rect(s, fx + 0.05, y + 0.475, fw - 0.1, 0.015, INK)
    text(s, fx, y + 0.5, fw, 0.46, den, size=size, font=font, align="center", space_after=0)
    text(s, x + w - 0.7, y, 0.7, 0.95, f"({eq})", size=size, color=MUTED, anchor="middle",
         align="right", space_after=0)


def equacoes(d):
    s = ap(d, "equacoes", "Método · Seção 3.8 (Equações 2 a 6)",
           "Métricas de estado e de operação")
    w = (CW - 0.5) / 3
    for i, (lhs, num, den, eq) in enumerate((("P =", "TP", "TP + FP", 2),
                                              ("R =", "TP", "TP + FN", 3),
                                              ("F_{1} =", "2PR", "P + R", 4))):
        _frac(s, MX + i * (w + 0.25), 1.45, w, lhs, num, den, eq, size=20,
              font="Cambria Math", lhs_w=0.9)
    _frac(s, MX, 2.6, CW, "UA =", "atributos com operação ADD ou UPDATE registrados "
          "corretamente em M_{t}", "total de atributos com operação ADD ou UPDATE esperados "
          "em M^{*}_{t}", 5)
    _frac(s, MX, 3.7, CW, "PA =", "atributos inalterados de M^{*}_{t−1} mantidos corretamente "
          "em M_{t}", "total de atributos com operação PRESERVE esperados em M^{*}_{t}", 6)
    bullets(s, [
        "**TP:** pares correspondentes diretamente ou aceitos pelo juiz; **FP:** pares gerados "
        "não correspondentes ou não sustentados; **FN:** fatos esperados não representados no "
        "estado gerado.",
        "Em (5) e (6), acerto = correspondência direta após normalização ou equivalência "
        "confirmada pelo juiz e apoiada pelas anotações; incertos não entram como acerto.",
        "Pares (\"state.<atributo>\", \"<valor_normalizado>\"), sem ordem de chaves; visões "
        "condicional e global, com resultados estritos e híbridos.",
    ], y=4.9, size=15, space_after=6)
    d.apoio(s, ["Normalização: espaços, caixa e pontuação.",
                "Visão global: falha estrutural recebe zero."])


def estatistica(d):
    s = ap(d, "estatistica", "Método · Seções 2.7 e 3.9", "Comparação estatística dos escritores")
    bullets(s, [
        heading("2.7 Testes não paramétricos (Demšar, 2006; Holm, 1979)", size=16),
        "**Friedman:** três ou mais modelos nas mesmas unidades; compara os postos médios → "
        "diferença global, sem indicar quais pares diferem.",
        "**Wilcoxon pareado:** diferenças entre dois modelos nas mesmas unidades, ordenadas por "
        "magnitude e com sinais; como diferença de localização, pressupõe simetria aproximada.",
        "**Holm-Bonferroni:** ordena os valores p e os compara sequencialmente com limites "
        "ajustados, controlando a probabilidade de pelo menos uma rejeição indevida.",
        "**Valor p:** probabilidade, sob H_{0} e os pressupostos, de resultado tão ou mais "
        "extremo que o observado; α é o critério de decisão; unidades independentes.",
        heading("3.9 Aplicação na Fase 2", size=16, space_before=8),
        "Média e mediana de cada métrica por escritor.",
        "Diferenças pareadas no nível de entidade (os três escritores processam as mesmas "
        "transições): Friedman (global) → Wilcoxon pareado com Holm-Bonferroni (dois a dois), "
        "α = 0,05.",
        "Curvas de ~~State F1~~, ~~Preservation Accuracy~~ e ~~JSON Validity~~ em função do "
        "turno t.",
    ], y=1.5, size=15, space_after=5)
    d.apoio(s, ["H0/H1 testadas nas métricas primárias: State F1, PA e UA.",
                "Os testes são pareados porque as unidades são as mesmas para os três modelos."])


_ATIV = [
    "Delimitação do tema, formulação do problema e definição dos objetivos.",
    "Levantamento e fichamento da bibliografia sobre memória em agentes, geração estruturada e "
    "SLMs, e revisão sistemática dos trabalhos relacionados.",
    "Especificação do protocolo experimental: variáveis, esquema, ~~prompt-base~~ e métricas.",
    "Verificação de disponibilidade, licenças e requisitos de execução local dos modelos e do "
    "SUMIE.",
    "Redação e revisão do texto do projeto de TCC I.",
    "Apresentação do projeto de TCC I e incorporação das recomendações da banca.",
    "Preparação do conjunto SUMIE: construção dos estados acumulados M^{*}_{t} e rotulagem de "
    "operações (PRESERVE, ADD, UPDATE).",
    "Implementação da estrutura base do ~~harness~~: adaptadores, analisador sintático, "
    "validador e testes unitários.",
    "Execução da Fase 0 (verificação funcional local com transições sintéticas).",
    "Execução da Fase 1 (estudo piloto em 25 entidades do SUMIE) e calibração das regras de "
    "normalização textual.",
    "Execução da Fase 2 (experimento principal com os três modelos escritores em toda a "
    "partição de avaliação do SUMIE).",
    "Processamento estatístico (testes pareados, curvas por turno e estratificação por "
    "operação).",
    "Elaboração das tabelas, gráficos e análise crítica dos resultados frente à literatura.",
    "Redação do artigo final (TCC II).",
    "Revisão normativa e linguística, depósito final e defesa do TCC II.",
]


def _mes(q):
    i = (q - 1) // 2
    return MESES[i], 2026 if i < 5 else 2027


def _periodo(a, b):
    (m1, y1), (m2, y2) = _mes(a), _mes(b)
    if (m1, y1) == (m2, y2):
        per = f"{m1}/{y1}"
    else:
        per = f"{m1}–{m2}/{y1}" if y1 == y2 else f"{m1}/{y1} – {m2}/{y2}"
    return per + (f", Q{a}" if a == b else f", Q{a}–Q{b}")


def cronograma_det(d):
    s = ap(d, "crono_det", "Cronograma · Seção 4.2 e Tabela 1",
           "Atividades previstas e seus períodos")
    items = [P(f"**{i}.** {t} ~~({_periodo(a, b)})~~", size=13, space_after=3)
             for i, (t, (a, b)) in enumerate(zip(_ATIV, GANTT_Q), start=1)]
    text(s, MX, 1.45, CW, 5.2, items)
    fonte(s, 6.62, "Períodos da Tabela 1: Q1–Q10 = TCC I (ago.–dez./2026); Q11–Q20 = TCC II "
          "(fev.–jun./2027).")
    d.apoio(s, ["A redação final (14) corre em paralelo à execução, de Q12 a Q19.",
                "Fases 0, 1 e 2 em sequência: Q12–Q14, Q15 e Q16–Q17.",
                "A preparação do SUMIE (7) começa em Q10, ainda no fim do TCC I."])


def build_apendice(d):
    div = build_apendice_a(d)
    for f in (prompt, quadro4, modelos, juiz, quadro5, equacoes, estatistica, cronograma_det):
        f(d)
    refs_apendice(d, first_code=len(d.appendix) + 1)
    indice(d, div)
