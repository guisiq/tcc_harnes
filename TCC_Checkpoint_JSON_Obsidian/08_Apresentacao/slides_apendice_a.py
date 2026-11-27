"""Apêndice (parte 1): divisória com índice, trabalhos relacionados e revisão sistemática.

Layout uniforme: título, lista em coluna única ou quadro fiel ao artigo, com a fonte abaixo.
Os códigos A1, A2, ... são sequenciais, na ordem de criação dos slides.
"""

from __future__ import annotations

from pptx_kit import *


def ap(d, key, tag, title):
    return d.new(key, tag, title, code=f"A{len(d.appendix) + 1}", title_size=24)


def _obrigado(d):
    return d.refs["obrigado"].split()[-1]


def divisoria(d):
    s = d.new("apendice", "Apêndice", "Conteúdo complementar do artigo")
    text(s, MX, 1.4, CW, 0.4, "Fora do tempo de apresentação. No Modo do Apresentador, digite "
         "o número do slide e tecle Enter.", size=14, color=MUTED, space_after=0)
    d._meta(s)["code"] = "Índice"
    d.apoio(s, ["Fim da apresentação principal. Mostre este slide só se precisar navegar.",
                "Para ir a um apêndice: digite o número do slide e tecle Enter; para voltar "
                f"ao encerramento, digite {_obrigado(d)} e Enter."])
    return s


def indice(d, s):
    items = d.appendix
    half = (len(items) + 1) // 2
    gap = 0.4
    w = (CW - gap) / 2
    for col, chunk in enumerate((items[:half], items[half:])):
        text(s, MX + col * (w + gap), 1.95, w, 4.95,
             [P(f"**{c}** · {t} — slide {n}", size=11.5, space_after=4) for c, t, n in chunk])


# ------------------------------------------------------------- literatura ---

_Q1 = [
    ("Yuen et al. (2025)", "Memória textual de cada agente organizada por modelo de seções",
     "Reescrita da memória a cada turno a partir da memória anterior e da saída do agente",
     "Llama-3.2-3B", "Desempenho em PDDL, FEVER e ALFWorld e qualidade de soluções em projeto "
     "de ~~pipeline~~ de dados", "Não"),
    ("Fioresi et al. (2026)", "Banco compartilhado de pares chave-valor textuais com resumos "
     "de passos intermediários", "Controlador decide admitir ou não cada passo na memória",
     "Controlador baseado no Qwen3-0.6B, treinado por reforço", "Taxa de admissão, revocação "
     "e reuso da memória; tempo de execução (AssistantBench e GAIA)", "Não"),
    ("Zhang et al. (2026)", "~~Memory Bank~~ estruturado", "Operações de criação, leitura, "
     "atualização e remoção em fases de manutenção", "Política baseada no Qwen3-4B, treinada "
     "por GRPO", "Respostas e erros de formação da memória (escritas incorretas e entradas "
     "obsoletas); rastreamento de estado no Ledger-QA", "Não"),
    ("Kang et al. (2026)", "Entradas de memória extraídas em JSON", "Gestão ativa: adicionar, "
     "adiar, buscar ou ignorar", "MemReader-0.6B e MemReader-4B", "Recuperação, atualização "
     "e respostas, com revocação, precisão, alucinação e omissão (LoCoMo, LongMemEval e "
     "HaluMem)", "Não"),
    ("Wang et al. (2026)", "Memórias central, episódica, semântica e procedural", "Ações de "
     "atualização por sessão, aprendidas por reforço", "Gestor baseado no Qwen3-4B",
     "Respostas e ablações (LongMemEval, LoCoMo e MemoryAgentBench)", "Não"),
    ("Lee; Pfister (2026)", "Estado de diálogo em pares ~~slot~~-valor sobre esquema",
     "Correção do estado a cada turno por operadores restritos (votar, adicionar e trocar) "
     "verificados pelo áudio", "Editor OLMo-2-1B com LoRA", "Acurácia conjunta de objetivos "
     "(JGA) do estado por turno", "Não"),
    ("Qin; Lu (2026)", "Grafo de proveniência tipado com pares chave-valor em JSON",
     "Registro do valor atual na escrita, preservando os valores substituídos", "Anotador "
     "Qwen3-4B congelado, com JSON restrito por esquema", "Preservação do valor atual por "
     "chave e respostas (LongMemEval, ALFWorld-Revision e MemoryAgentBench)", "Não"),
    ("Zheng et al. (2026)", "Mensagens literais por falante e estados derivados por pessoa "
     "e grupo", "Escrita incremental, com atualizações encadeadas que preservam o histórico",
     "Escritor Qwen2.5-3B treinado por GRPO", "Similaridade das entradas escritas com a "
     "referência e respostas", "Não"),
    ("Li et al. (2026)", "Memória textual limitada, com fatos confirmados e trechos "
     "pendentes", "Política decide promover, manter ou descartar evidências; verificador "
     "aceita apenas fatos apoiados na fonte", "Qwen3.5-4B e Qwen3.5-9B", "F1 de respostas e "
     "fidelidade dos fatos confirmados à fonte", "Não"),
    ("Hwang; Diao (2026)", "Registros estruturados de memória pessoal", "Admissão; "
     "manutenção, descarte de duplicatas ou fusão", "Qwen3.5-2B como gestor", "Correção das "
     "ações de escrita, redundância e recuperação", "Não"),
    ("Ali; Abdallah; Jatowt (2026)", "Grafo de fatos por turno, com dependências e "
     "contradições", "Operações de revisar, abandonar e reativar tópicos, com uma chamada "
     "por turno", "Escritor Ministral-3-3B com LoRA, destilado de memórias de referência",
     "Acurácia das operações de revisão e qualidade da busca (ConvRevise)", "Não"),
    ("Zhao et al. (2026)", "Registros textuais de memória", "Operações de adição, "
     "atualização, remoção ou nenhuma ação, com leitura seletiva", "Gestor Qwen3-4B ajustado "
     "por SFT", "Métrica ECA sobre respostas e registros selecionados, sob desatualização e "
     "envenenamento", "Não"),
    ("Este trabalho", "~~Checkpoint~~ JSON de esquema fixo", "GU-JSON, com reescrita integral "
     "pelo escritor", "Três representantes compactos (~0,6B: autoregressivo, "
     "~~encoder-decoder~~ e difusão em blocos)", "Validade estrutural e fidelidade do estado "
     "por transição, turno e operação no SUMIE", "Sim, sob protocolo controlado"),
]
_Q1_HDR = ["Trabalho", "Representação da memória", "Atualização", "Modelos e escala",
           "Objeto da avaliação", "Compara paradigmas gerativos"]
_Q1_W = [1.45, 2.25, 2.5, 2.0, 2.73, 1.2]


def quadro1(d):
    for part, rows in ((1, _Q1[:6]), (2, _Q1[6:])):
        s = ap(d, f"quadro1_{part}", "Trabalhos relacionados · Seção 2.8",
               f"Quadro 1 – Comparação entre trabalhos relacionados e a proposta ({part}/2)")
        body = [[r[0], *r[1:5], {"t": r[5], "align": "center"}] for r in rows]
        add_table(s, MX, 1.45, [[{"t": h, "size": 10.5} for h in _Q1_HDR]] + body, _Q1_W,
                  size=10, row_h=[0.42] + [0.75 if part == 1 else 0.66] * len(body))
        fonte(s, 6.62)
        d.apoio(s, ["Os 12 estudos do núcleo combinam memória estruturada, atualização "
                    "incremental, escritor de até ~4B e avaliação direta do estado.",
                    "Na maioria, o modelo emite operações aplicadas por código, em vez de "
                    "reescrever o estado completo.",
                    "Nenhum estudo do núcleo compara paradigmas gerativos: todos os escritores "
                    "são autoregressivos."] + (["Yuen et al. (2025) reescreve a memória, mas "
                                               "avalia o desempenho nas tarefas."]
                                              if part == 1 else
                                              ["A última linha resume a proposta."]))


def base(d):
    s = ap(d, "base", "Trabalhos relacionados · Seções 2.3, 2.4 e 2.8",
           "Estudos de base e comparadores de paradigmas")
    bullets(s, [
        heading("Estudos de base (levantamento anterior à revisão sistemática)"),
        "**Hwang et al. (2024):** GO, GU e GM em texto e em JSON (SUMIE e BooookScore; Gemini "
        "Ultra e Pro); sob limite de ~~tokens~~, o GU-JSON superou o GU-Text; propuseram o "
        "CoK-JSON.",
        "**Hwang et al. (2025) — SUMIE:** atualização incremental de atributos e valores, "
        "mantendo perspectivas divergentes; perfis contrastantes de precisão e revocação entre "
        "modelos de grande porte.",
        "**Jayalath et al. (2025) — PRISM:** memória tipada com operações estruturadas "
        "aplicadas por código.",
        "**Zeng et al. (2024):** representações e estratégias de recuperação para memória em "
        "agentes.",
        "**Geng et al. (2025):** conformidade sintática e de esquema na geração estruturada.",
        heading("Comparação entre difusão e autoregressão (fora do núcleo)", space_before=10),
        "**Zhou, Xiong e Tan (2026):** planos textuais editáveis; não cumpre os critérios do "
        "núcleo.",
        "**Lu et al. (2026):** fluxos agênticos, com memória em texto livre e modelos de 7 a 8 "
        "bilhões de parâmetros.",
        P("Esses estudos apoiam a base conceitual, mas não entram no Quadro 1, que se restringe "
          "aos 12 estudos do núcleo. Yuen et al. (2025), também do levantamento anterior, foi "
          "recuperado pela revisão e integra o núcleo.", size=14, color=MUTED, space_before=8),
    ], y=1.5, size=16, space_after=6)
    d.apoio(s, ["Hwang 2024 e 2025 usam modelos de grande porte → o trabalho testa compactos.",
                "PRISM aplica operações por código; aqui o próprio escritor reescreve tudo.",
                "Comparações de paradigma existentes não usam estado estruturado nem ~0,6B."])


def rev_22_24(d):
    s = ap(d, "rev_22_24", "Referencial teórico · Seções 2.2 e 2.4",
           "Representação da memória e avaliação de memória")
    bullets(s, [
        heading("2.2 Representação estruturada da memória"),
        "**Zeng et al. (2024):** resumos condensam contextos longos; unidades factuais "
        "explícitas favorecem a precisão — propriedades combinadas em pares atributo-valor.",
        "**PRISM:** esquema hierárquico tipado, com operações de caminho e valor aplicadas por "
        "código (Jayalath et al., 2025).",
        "**Intrinsic Memory Agents:** reescrevem a memória a partir do estado anterior e da "
        "saída mais recente (Yuen et al., 2025).",
        "**SciBORG:** autômatos finitos (Muhoberac et al., 2025); **Chain-of-Memory:** "
        "fragmentos dinâmicos (Xu et al., 2026).",
        "Formato e mecanismo de atualização são dimensões independentes; um esquema JSON único "
        "e fixo isola a reescrita do estado.",
        heading("2.4 Avaliação de memória e de atualização de conhecimento", space_before=8),
        "**SUMIE:** fatos novos, repetições, distratores e pontos de vista divergentes, com "
        "anotações de atributos e valores (Hwang et al., 2025).",
        "**MemoryAgentBench** (Hu; Wang; McAuley, 2025), **LongMemEval** (Wu et al., 2024) e "
        "**LoCoMo** (Maharana et al., 2024): foco na resposta ao final da sequência.",
        "Respostas finais podem mascarar a perda silenciosa de atributos; por isso o "
        "~~checkpoint~~ M_{t} é inspecionado a cada transição.",
    ], y=1.5, size=15, space_after=5)
    d.apoio(s, ["Por que JSON de esquema fixo: isola a reescrita e permite medir a fidelidade "
                "de cada transição.",
                "Por que SUMIE: os outros benchmarks avaliam respostas no fim da sequência."])


def rev_25_26(d):
    s = ap(d, "rev_25_26", "Referencial teórico · Seções 2.5 e 2.6",
           "Geração estruturada, paradigmas gerativos e modelos compactos")
    bullets(s, [
        heading("2.5 Validade sintática e conformidade com esquema"),
        "**JSONSchemaBench:** falhas sintáticas e de restrições não triviais (Geng et al., "
        "2025).",
        "Decodificação restrita por gramática (Geng et al., 2023); para difusão, gramáticas "
        "livres de contexto (Mündler; Dekoninck; Vechev, 2025) e reforço multiagente (Khanal "
        "et al., 2026).",
        "Esquema válido é necessário, mas não suficiente → métricas estruturais e semânticas "
        "independentes; regime ~~prompt-only~~ para observar a capacidade intrínseca.",
        heading("2.6 Paradigmas gerativos e modelos compactos", space_before=8),
        "**Autoregressivo:** família Qwen3, inclusive 0,6B (Yang et al., 2025). "
        "**~~Encoder-decoder~~:** T5Gemma, adaptado de ~~decoder-only~~ (Zhang et al., 2025).",
        "**Difusão:** remoção iterativa de ruído em posições mascaradas (Nie et al., 2024), "
        "inclusive a partir de pesos autoregressivos (Gong et al., 2024); **BD3LM:** blocos "
        "autoregressivos com difusão em cada bloco (Arriola et al., 2025).",
        "**Compactos:** execução local e menor custo (Lu et al., 2025); eficazes em subtarefas "
        "agênticas delimitadas (Sharma; Mehta, 2025); sensíveis à quantização (Lee et al., "
        "2025).",
    ], y=1.5, size=15, space_after=5)
    d.apoio(s, ["Prompt-only: sem gramática, para não mascarar a capacidade de cada paradigma.",
                "Precisão numérica uniforme por causa da sensibilidade de SLMs à quantização."])


# ------------------------------------------------------ revisão sistemática ---

_Q2 = [("E1", "Memória estruturada nomeada no título, com atualização; ou no resumo, com "
              "atualização e modelo compacto ou avaliação do estado", "177"),
       ("E2", "Gestão ou atualização de memória com modelo compacto e representação "
              "estruturada", "136"),
       ("E3", "Gestão ou atualização de memória com avaliação direta do conteúdo atualizado "
              "(atualização de conhecimento, supersessão, memória obsoleta)", "168"),
       ("E4", "Modelos de difusão ou não autorregressivos aplicados a memória, estado, "
              "planejamento ou saída estruturada em agentes ou diálogo", "67"),
       ("E5", "Sumarização incremental ou recorrente, GU-JSON, SUMIE ou estado de entidades, "
              "com atualização", "15"),
       ("E6", "Estado ou memória em JSON ou esquema tipado, atualizado por modelo compacto",
        "129"),
       ("E7", "Gestor de memória compacto treinado (reforço, destilação, adaptadores ou "
              "ajuste fino)", "158"),
       ("E8", "Memória estruturada com operações de atualização avaliadas por ~~benchmark~~ "
              "de ciclo de vida", "55"),
       ("Total", "Após a deduplicação pelo identificador do arXiv", "738")]


def quadro2(d):
    s = ap(d, "quadro2", "Revisão sistemática · Seção 3.1",
           "Quadro 2 – Consultas da revisão sistemática no arXiv")
    rows = [["Consulta", "Faceta buscada", {"t": "Registros", "align": "center"}]]
    rows += [[{"t": c, "align": "center"}, f, {"t": n, "align": "center"}] for c, f, n in _Q2]
    add_table(s, MX, 1.5, rows, [1.25, 9.43, 1.45], size=13, row_h=[0.42] + [0.5] * 9)
    fonte(s, 6.62)
    d.apoio(s, ["Cada consulta combina facetas do problema, em vez de termos isolados.",
                "A soma das consultas (905) passa de 738 porque um mesmo estudo aparece em mais "
                "de uma consulta — a união é feita pelo identificador do arXiv.",
                "Blocos de termos e expressões compactas: slides finais desta parte."])


def triagem(d):
    s = ap(d, "triagem", "Revisão sistemática · Seção 3.1, itens 1 a 5",
           "Planejamento, busca e triagem codificada por título e resumo")
    bullets(s, [
        "Protocolo versionado (questão orientadora, janela, fonte, consultas, termos de "
        "exclusão, livro de códigos, regras e estudos de controle), lido pelos ~~scripts~~.",
        "API do arXiv, título e resumo; união pelo identificador → 738 candidatos; termos de "
        "exclusão no título removeram 42 → 696.",
        "O modelo registrou sim, incerto ou não em sete características, em vez de atribuir "
        "diretamente uma categoria:",
        P("**C1** estudo primário · **C2** memória textual mantida por modelo de linguagem · "
          "**C3** atualização incremental · **C4** estrutura explícita", bullet=True, level=1),
        P("**C5** escritor ou gestor de até ~4 bilhões de parâmetros · **C6** avaliação direta "
          "do estado ou das operações de escrita · **C7** comparação entre paradigmas "
          "gerativos", bullet=True, level=1),
        "Execução: claude-haiku-5.5, via GitHub Copilot SDK 1.0.31, com roteiro fixo, lotes de "
        "20 registros e resposta validada por esquema JSON.",
        "Grupos atribuídos pelas regras do ~~script~~, e não pelo modelo: 22 prováveis, 165 "
        "incertos com memória textual incremental afirmada, 2 possíveis comparadores, 42 "
        "incertos sem essa base, 59 de contexto e 406 exclusões.",
        "Os 189 estudos dos três primeiros grupos seguiram para a elegibilidade.",
    ], y=1.5, size=16, space_after=7)
    d.apoio(s, ["O modelo só codifica características; as regras do script decidem o grupo.",
                "12 estudos de controle orientaram as consultas e foram todos recuperados — "
                "não é validação independente."])


def elegibilidade(d):
    s = ap(d, "elegibilidade", "Revisão sistemática · Seção 3.1, itens 6 e 7",
           "Elegibilidade com texto integral, extração e síntese")
    bullets(s, [
        "Os 189 estudos foram recodificados com o texto integral da mesma versão do arXiv (HTML "
        "ou, na falta, PDF; até 100 mil caracteres), um artigo por requisição.",
        "Cada característica marcada como presente exigiu um trecho literal, conferido pelo "
        "~~script~~ no texto salvo:",
        P("sem trecho encontrado → rebaixada a incerto;", bullet=True, level=1),
        P("escritor compacto cujo trecho só citava modelos acima de 4,5 bilhões de parâmetros "
          "→ rebaixado a ausente.", bullet=True, level=1),
        "Classes por regras ordenadas; o **núcleo** exige C1 a C4, C5 e C6 presentes.",
        "Resultado: 12 de núcleo, 2 pendentes, 1 comparador gerativo, 8 de escritor compacto, "
        "52 de avaliação do estado, 70 de memória estruturada e 44 exclusões.",
        "Extração: representação da memória, mecanismo de atualização, modelos e escala, objeto "
        "da avaliação e comparação entre paradigmas gerativos → colunas do Quadro 1.",
    ], y=1.5, size=17, space_after=8)
    d.apoio(s, ["Pendentes: C5 e C6 presentes, mas algum critério de base incerto.",
                "O Quadro 1 indica estudos próximos no escopo examinado; não prova inexistência."])


def rev_limites(d):
    s = ap(d, "rev_limites", "Revisão sistemática · Seção 3.1 e Apêndice B",
           "Artefatos e limitações da revisão sistemática")
    bullets(s, [
        heading("Artefatos publicados (repositório público, versão v2.1.0)"),
        "Protocolo, livro de códigos, roteiros de triagem, termos de exclusão e ~~scripts~~ em "
        "C# (.NET 10).",
        "Expressões completas das consultas e respostas brutas da API com seus ~~hashes~~ "
        "SHA-256.",
        "Codificações das duas etapas, com os trechos conferidos, e ~~hashes~~ dos textos "
        "integrais — reconstituíveis pelo ~~script~~, sem redistribuição.",
        P("github.com/guisiq/tcc_revisao_sistematica_sumarizacao_recorrente", size=14,
          color=MUTED, font="Consolas", markup=False, space_after=10),
        heading("Limitações"),
        "A busca cobriu uma única fonte, e os estudos de controle orientaram as consultas.",
        "Codificação por um único modelo de linguagem, sem revisor humano independente; regras "
        "e trechos literais reduzem, mas não eliminam, erros.",
        "Estudos que não informam o tamanho do escritor ou não avaliam o estado diretamente "
        "ficam fora do núcleo, ainda que próximos.",
        "O Quadro 1 indica estudos próximos no escopo examinado, mas não comprova a "
        "inexistência de trabalhos semelhantes fora dele.",
    ], y=1.5, size=16, space_after=6)
    d.apoio(s, ["Os textos integrais não são redistribuídos; o script confere seus hashes.",
                "Execução de 19/11/2026."])


_Q9 = [
    ("a) Planejamento", "Janela temporal", "Primeiro depósito entre 01/07/2025 e 19/11/2026"),
    ("b) Busca", "Fonte e campos", "API do arXiv; título (ti) e resumo (abs)"),
    ("", "Filtro temporal", {"t": "submittedDate:[202507010000 TO 202611192359]",
                             "font": "Consolas", "markup": False}),
    ("", "Paginação e ordenação", "1.000 registros por página; todas as páginas recuperadas; "
                                  "ordenação crescente pela data de depósito"),
    ("", "Intervalo entre requisições", "4 segundos"),
    ("c) Estudos de controle", "Identificadores arXiv",
     "2603.26680 (AlpsBench); 2604.07877 (MemReader); 2605.15759 (DimMem); 2609.01272 "
     "(Prospective Intention Store); 2609.36976 (AMU); 2512.04763 (MemLoRA); 2607.20553 "
     "(CMI-Mem); 2608.01708 (PGMem); 2601.12979 (The Bitter Lesson of Diffusion Language "
     "Models); 2610.24717 (DiffuPlan); 2508.08997 (Intrinsic Memory Agents); 2606.27472 "
     "(Supersede). Todos recuperados"),
    ("d) Deduplicação e exclusão por termos", "Chave e resultado",
     "Identificador do arXiv; 738 registros únicos"),
    ("", "Termos no título", 'video, manipulation, motion, rendering, geometry, "visual '
                             'generation" (modalidade não textual) e quantum (fora do tema); '
                             '42 removidos, 696 restantes'),
    ("e) Triagem por título e resumo", "Modelo e interface",
     "claude-haiku-5.5, via GitHub Copilot SDK 1.0.31"),
    ("", "Lote e resposta", "20 registros por requisição; valores S, I ou N de C1 a C7 e "
                            "códigos de exclusão, validados por esquema JSON"),
    ("", "Teto de custo", "150 créditos; 36 requisições, 38 créditos consumidos"),
    ("", "Regras e resultado", "Provável (C3 e C4 = S e algum de C5 a C7 = S): 22; incerto (C2 "
                               "e C3 = S, C4 ≠ N e algum de C5 a C7 ≠ N): 165; possível "
                               "comparador (C7 ≠ N e C3 ≠ N): 2; incerto sem base: 42; contexto: "
                               "59; excluídos (código de exclusão, C1 ou C2 = N): 406"),
    ("f) Elegibilidade com texto integral", "Texto e resposta",
     "Mesma versão do arXiv (185 em HTML e 4 em PDF), até 100 mil caracteres; um artigo por "
     "requisição; cada S acompanhado de trecho literal (20 a 400 caracteres) conferido no "
     "texto, ou rebaixado a I; C5 rebaixado a N quando o trecho só cita modelos acima de 4,5B"),
    ("", "Teto de custo", "400 créditos; 189 requisições, cerca de 191 créditos consumidos"),
    ("", "Regras e resultado", "Núcleo (C1 a C6 = S): 12; pendente: 2; comparador gerativo: 1; "
                               "escritor compacto: 8; avaliação do estado: 52; memória "
                               "estruturada: 70; excluídos por ausência: 8; excluídos por "
                               "critério não demonstrado: 36"),
    ("g) Extração e síntese", "Campos extraídos", "Representação da memória; mecanismo de "
                                                  "atualização; modelos e escala; objeto da "
                                                  "avaliação; comparação entre paradigmas "
                                                  "gerativos"),
]


def _merges(rows):
    """Mescla a célula de etapa com as linhas de continuação (etapa vazia)."""
    out, start = [], None
    for i, r in enumerate(rows, start=1):
        if r[0]:
            if start is not None and i - 1 > start:
                out.append((start, 0, i - 1, 0))
            start = i
    if start is not None and len(rows) > start:
        out.append((start, 0, len(rows), 0))
    return out


def _quadro9(d, key, part, rows, row_h, apoio):
    s = ap(d, key, "Revisão sistemática · Apêndice B",
           f"Quadro 9 – Parâmetros metodológicos da revisão sistemática ({part}/2)")
    body = [[{"t": a, "bold": True}, b, c] for a, b, c in rows]
    add_table(s, MX, 1.5, [["Etapa", "Parâmetro", "Valor adotado"]] + body,
              [2.15, 2.3, 7.683], size=12, row_h=[0.36] + row_h, merges=_merges(rows))
    fonte(s, 6.62)
    d.apoio(s, apoio)


def busca(d):
    _quadro9(d, "busca", 1, _Q9[:8], [0.34, 0.34, 0.34, 0.5, 0.34, 1.12, 0.34, 0.52],
             ["Valores da execução de 19/11/2026.",
              "Termos de exclusão derivados das justificativas de exclusão de "
              "execuções-piloto.",
              "Os 12 controles orientaram as consultas: a recuperação não é validação "
              "independente."])


def quadro9_2(d):
    _quadro9(d, "quadro9_2", 2, _Q9[8:], [0.34, 0.5, 0.34, 0.95, 0.95, 0.34, 0.75, 0.5],
             ["Triagem: o modelo codifica C1–C7; o script atribui os grupos.",
              "Elegibilidade: cada S exige trecho literal conferido no texto salvo.",
              "Campos extraídos = colunas do Quadro 1."])


_BLOCOS = [
    ("MEST", "memória estruturada", '"structured memory", "structured memories", "structured '
     'contextual memory", "memory schema", "typed memory", "memory graph", "graph memory", '
     '"graph-based memory", "JSON memory", "memory template", "memory records", "structured '
     'state", "entity memory", "memory slots", "key-value memory", "tabular memory", "memory '
     'table", "memory items", "memory units", "atomic memory", "memory entries", "intention '
     'store", "typed store"'),
    ("ATU", "atualização", "updat*, increment*, evolv*, maint*, revis*, consolid*, supersed*, "
     "overwrit*, edit*, CRUD, rewrit*, lifecycle"),
    ("GMEM", "gestão de memória", '"memory update", "memory updating", "update memory", '
     '"updating memory", "memory evolution", "evolving memory", "memory maintenance", "memory '
     'consolidation", "memory editing", "memory operations", "memory management", "memory '
     'manager", "memory writing", "write memory", "memory revision", "self-maintained '
     'memory", "knowledge update", "memory extraction", "memory construction", "memory '
     'admission"'),
    ("COMP", "modelo compacto", '"small language model", "small language models", SLM, SLMs, '
     '"small model", "small models", "small open model", compact, lightweight, "on-device", '
     "0.5B, 0.6B, 1B, 1.5B, 1.7B, 2B, 3B, 4B"),
    ("AVAL", "avaliação do estado", '"knowledge update", supersed*, stale, outdated, "memory '
     'quality", "memory accuracy", "memory fidelity", "update accuracy", "state accuracy", '
     '"memory correctness", "memory hallucination", "write accuracy", "memory evaluation", '
     '"memory F1"'),
    ("ESTR", "estrutura", 'structur*, schema*, typed, JSON, entit*, graph*, templat*, '
     '"key-value", slot*, record*, attribut*, tripl*'),
    ("DIF", "difusão ou não autorregressivo", '"diffusion language model", "diffusion '
     'language models", dLLM, dLLMs, "masked diffusion", "block diffusion", "discrete '
     'diffusion", "non-autoregressive"'),
    ("SUM", "sumarização incremental e estado de entidades", '"incremental summarization", '
     '"recurrent summarization", "recursive summarization", "entity summarization", "update '
     'summarization", "progressive summarization", "GU-JSON", SUMIE, "entity state", "entity '
     'states"'),
    ("TREINO", "treinamento do gestor", '"reinforcement learning", distil*, "fine-tuning", '
     '"fine-tuned", finetun*, adapter, LoRA, supervised'),
    ("BENCH", "~~benchmark~~", 'benchmark, benchmarks, "evaluation framework", lifecycle'),
]


def blocos(d):
    s = ap(d, "blocos", "Revisão sistemática · Apêndice B", "Expressões de busca: blocos de termos")
    items = [P(f"**{k}** ({desc}): {terms}", size=11, space_after=5) for k, desc, terms in
             _BLOCOS]
    items.append(P("ti(BLOCO) e abs(BLOCO) indicam a união por OR dos termos do bloco no título "
                   "ou no resumo; tiabs(BLOCO) une as duas formas; o asterisco indica "
                   "truncamento.", size=11, color=MUTED, space_before=4))
    text(s, MX, 1.45, CW, 5.1, items)
    fonte(s, 6.62, "Fonte: protocolo da revisão sistemática (2026).")
    d.apoio(s, ["Cada bloco é definido uma vez e reutilizado nas oito consultas.",
                "COMP inclui tamanhos explícitos (0.5B a 4B) para capturar escritores compactos."])


_CONSULTAS = [
    ("E1 – Memória estruturada com atualização (177 registros)",
     "(ti(MEST) AND abs(ATU)) OR (abs(MEST) AND abs(ATU) AND (tiabs(COMP) OR abs(AVAL)))"),
    ("E2 – Gestão de memória com modelo compacto e estrutura (136 registros)",
     "tiabs(GMEM) AND tiabs(COMP) AND tiabs(ESTR)"),
    ("E3 – Gestão de memória com avaliação direta do conteúdo atualizado (168 registros)",
     "tiabs(GMEM) AND abs(AVAL)"),
    ("E4 – Difusão ou não autorregressivo em memória, estado, planejamento ou saída "
     "estruturada (67 registros)",
     'tiabs(DIF) AND abs(memory OR state OR planning OR JSON OR "structured output" OR '
     '"structured generation" OR summarization) AND abs(agent* OR summar* OR dialogue OR '
     'convers* OR "multi-turn")'),
    ("E5 – Sumarização incremental, GU-JSON, SUMIE ou estado de entidades (15 registros)",
     'tiabs(SUM) AND abs("language model" OR "language models" OR LLM OR LLMs OR agent*) AND '
     'abs(ATU)'),
    ("E6 – Estado ou memória em JSON ou esquema tipado atualizado por modelo compacto "
     "(129 registros)",
     'tiabs(JSON OR schema* OR "structured output" OR typed) AND abs(memory OR "dialogue '
     'state" OR "entity state" OR "agent state" OR "structured state" OR "state tracking") '
     'AND tiabs(COMP) AND abs(ATU)'),
    ("E7 – Gestor de memória compacto treinado (158 registros)",
     "tiabs(GMEM) AND tiabs(COMP) AND abs(TREINO)"),
    ("E8 – Memória estruturada com operações avaliadas por ~~benchmark~~ de ciclo de vida "
     "(55 registros)",
     "tiabs(MEST) AND tiabs(GMEM) AND tiabs(BENCH)"),
]


def consultas(d):
    s = ap(d, "consultas", "Revisão sistemática · Apêndice B",
           "Expressões de busca: consultas E1–E8")
    items = []
    for lab, expr in _CONSULTAS:
        items.append(P(lab, bold=True, color=NAVY, size=12, space_after=1))
        items.append(P(expr, font="Consolas", size=10.5, markup=False, lang="en-US",
                       space_after=7))
    text(s, MX, 1.45, CW, 5.1, items)
    fonte(s, 6.62, "Fonte: protocolo da revisão sistemática (2026).")
    d.apoio(s, ["Todas combinadas com o filtro temporal do Quadro 9; expressões expandidas no "
                "protocolo publicado (v2.1.0).",
                "E4 busca a comparação entre paradigmas (difusão); E5 busca GU-JSON e SUMIE."])


def build_apendice_a(d):
    s = divisoria(d)
    for f in (quadro1, base, rev_22_24, rev_25_26, quadro2, triagem, elegibilidade,
              rev_limites, busca, quadro9_2, blocos, consultas):
        f(d)
    return s
