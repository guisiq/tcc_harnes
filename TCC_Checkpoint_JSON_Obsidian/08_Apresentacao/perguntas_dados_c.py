"""Perguntas de treino, grupos 8 a 10 (estatística, limitações e ética, resultados e cronograma)."""

from perguntas_dados_a import q

GRUPOS_C = [
    ("Hipóteses e análise estatística", [
        q("Quais são as hipóteses?",
          "H0: não há diferença estatisticamente significativa nas métricas primárias (State "
          "F1, Preservation Accuracy e Update Accuracy) entre os três escritores. H1: há "
          "diferenças significativas na preservação do estado e na incorporação de novas "
          "informações, refletindo perfis de erro distintos.",
          [], ["desenho", "estatistica"]),
        q("Você espera que algum paradigma vença?",
          "Não há hipótese direcional: H1 afirma que há diferença, não qual escritor é melhor. "
          "O desenho permite verificar se a codificação bidirecional ou a difusão em blocos "
          "são mais ou menos estáveis que a geração autoregressiva.",
          [], ["resultados", "desenho"]),
        q("Por que Friedman e Wilcoxon, e não ANOVA ou teste t?",
          "São testes não paramétricos pareados: os três escritores são avaliados nas mesmas "
          "unidades e não se supõe normalidade. Friedman compara os três pelos postos médios; "
          "Wilcoxon pareado compara dois a dois (Demšar, 2006).",
          ["Wilcoxon interpretado como diferença de localização pressupõe diferenças "
           "aproximadamente simétricas."],
          ["estatistica"]),
        q("Por que a correção de Holm-Bonferroni?",
          "São três comparações dois a dois por métrica; Holm ordena os valores p e os "
          "compara com limites ajustados, controlando a probabilidade de pelo menos uma "
          "rejeição indevida (Holm, 1979), com menos perda de poder que o Bonferroni simples.",
          ["α = 0,05."],
          ["estatistica"]),
        q("Qual é a unidade de análise?",
          "A entidade: as diferenças pareadas são calculadas no nível de entidade, porque as "
          "transições de uma mesma entidade não são independentes e os testes exigem unidades "
          "independentes.",
          [], ["estatistica"],
          alerta="O artigo não diz como a métrica por entidade é agregada (média das transições "
                 "ou contagem conjunta dos pares); defina isso e leve pronto."),
        q("E se o teste de Friedman não for significativo?",
          "H0 não é rejeitada para aquela métrica; os resultados descritivos (média, mediana, "
          "curvas por turno e perfil por operação) continuam informativos.",
          [], ["estatistica"],
          alerta="O artigo não diz se os Wilcoxon serão feitos mesmo sem rejeição global; "
                 "seguindo Demšar (2006), o *post-hoc* vem depois da rejeição no Friedman. "
                 "Deixe isso explícito."),
        q("Você vai reportar tamanho de efeito ou intervalo de confiança?",
          "O plano prevê média, mediana, testes pareados e curvas por turno.",
          [], ["estatistica"],
          alerta="A sigla IC (Intervalo de Confiança) está na lista de siglas, mas não é usada "
                 "no texto; retire a sigla ou inclua IC (por exemplo, *bootstrap* por "
                 "entidade) e um tamanho de efeito no plano de análise."),
        q("Uma única execução é suficiente?",
          "A decodificação é determinística (sem amostragem e com semente fixa), então repetir "
          "a execução daria a mesma saída; a variabilidade analisada vem das entidades.",
          [], ["harness", "estatistica"],
          alerta="Pequenas diferenças numéricas de *hardware* ou de precisão podem alterar "
                 "saídas; garanta que versões, *hashes* e configuração fiquem no manifesto."),
        q("Como será a análise longitudinal?",
          "Curvas de State F1, Preservation Accuracy e JSON Validity em função do índice do "
          "turno $t$, para ver como a qualidade se degrada à medida que o estado cresce e se "
          "aproxima dos 1.200 *tokens*.",
          [], ["estatistica", "resultados"]),
    ]),
    ("Limitações, ética e reprodutibilidade", [
        q("Quais são as principais ameaças à validade?",
          "Interna: os modelos diferem além da arquitetura. De construção: possível viés do "
          "juiz. Externa: sumarização de entidades, esquema plano e transições com estado de "
          "referência, sem medir o impacto nas tarefas do agente.",
          [], ["limitacoes"]),
        q("Há questões éticas envolvidas?",
          "Não há participantes humanos nem coleta de dados pessoais: os dados são sintéticos "
          "e públicos (SUMIE, Apache-2.0) e os modelos têm pesos abertos (Qwen3 sob Apache-2.0; "
          "juiz sob a licença Gemma).",
          [], ["harness", "sumie"]),
        q("Como se garante a reprodutibilidade do experimento?",
          "Manifesto com os *commit hashes* dos pesos e a configuração de inferência; "
          "decodificação determinística; saídas brutas gravadas antes de qualquer validação e "
          "sem reparo; registros JSON com proveniência; versão, *hash* e contexto do juiz "
          "registrados.",
          [], ["harness", "quadro4"]),
        q("Por que não reparar o JSON inválido?",
          "Porque o reparo esconderia justamente a falha que o Objetivo a mede; a saída original "
          "é preservada e, na visão global, a falha estrutural recebe zero.",
          [], ["harness", "metricas"]),
        q("Quais são as nove etapas do *harness*?",
          "(i) ler a transição; (ii) montar o *prompt*; (iii) invocar o adaptador com limite de "
          "1.200 *tokens*; (iv) gravar a saída bruta; (v) validar a sintaxe; (vi) validar o "
          "esquema; (vii) correspondência direta; (viii) juiz só para divergências; "
          "(ix) registrar.",
          [], ["harness", "quadro4"]),
        q("O que o adaptador de cada modelo pode mudar?",
          "Só o que é específico do modelo: o *template* de conversa e os *tokens* especiais, "
          "sem alterar o *prompt-base*. A decodificação também é fixada: *thinking* desativado "
          "no Qwen3 e, no BD3LM, tamanho de bloco, passos de remoção de ruído e critério de "
          "desmascaramento.",
          [], ["fig2", "harness"]),
        q("O que fica como trabalho futuro?",
          "Extensões que o recorte exclui: propagar a saída do escritor entre turnos, esquemas "
          "aninhados, decodificação restrita, outras escalas e o impacto do *checkpoint* nas "
          "tarefas do agente.",
          [], ["limitacoes", "consideracoes"],
          alerta="O artigo não tem seção de trabalhos futuros; essas extensões derivam das "
                 "limitações (Seções 2.5 e 3.11). Apresente-as como possibilidades, não como "
                 "compromisso."),
    ]),
    ("Resultados esperados e cronograma", [
        q("Que resultados o trabalho vai entregar?",
          "Quatro conjuntos de evidências — robustez estrutural com categorias de falha; "
          "fidelidade global e longitudinal; perfil de erro por operação; relação entre "
          "validade sintática e fidelidade semântica — além de um protocolo e um *harness* "
          "reutilizáveis.",
          [], ["resultados"]),
        q("O que seria um escritor \"conservador\" e um que sobrescreve?",
          "Conservador: preserva bem o estado anterior (PA alta), mas falha em incorporar novos "
          "atributos (UA baixa). O outro integra a informação nova, mas esquece ou sobrescreve "
          "campos válidos (PA baixa).",
          [], ["resultados", "equacoes"]),
        q("E se nenhum modelo gerar JSON válido com frequência?",
          "Isso já é resultado do Objetivo a: a visão global atribui zero e a classificação das "
          "falhas (truncamento, chaves malformadas, texto fora do objeto) caracteriza os modos "
          "de falha de cada escritor.",
          [], ["resultados", "metricas"],
          alerta="A visão condicional pode ficar com poucas transições; diga como reportará "
                 "(por exemplo, o número de transições válidas por escritor)."),
        q("Quais são as fases do experimento?",
          "Fase 0: 15 transições sintéticas, verificação funcional e pico de memória do juiz até "
          "4 GiB. Fase 1: piloto em 25 entidades separadas, para normalização, comprimento em "
          "*tokens*, ausência de truncamento, auditoria e congelamento do juiz. Fase 2: os três "
          "escritores em toda a partição de avaliação.",
          [], ["fases"]),
        q("Como está organizado o cronograma?",
          "São 15 atividades em 20 quinzenas. TCC I (ago.–dez./2026, Q1–Q10): tema, revisão, "
          "protocolo, verificação dos modelos, texto e apresentação. TCC II (fev.–jun./2027, "
          "Q11–Q20): preparação do SUMIE, *harness*, Fases 0 a 2, estatística, redação e "
          "defesa.",
          [], ["cronograma", "crono_det"]),
        q("Quais são os riscos do cronograma e o plano B?",
          "A Fase 0 detecta cedo problemas de carregamento e memória, e a Fase 1 fixa as regras "
          "antes do experimento principal.",
          [], ["cronograma", "fases"],
          alerta="O artigo não lista riscos nem contingências; prepare dois ou três (modelo que "
                 "não cabe na GPU, tempo de inferência do BD3LM, juiz reprovado na auditoria)."),
        q("Como os objetivos se ligam às evidências?",
          "Pelos Quadros 6 a 8: a) analisador e validador → JSON e Schema Validity; "
          "b) estados de referência, correspondência e juiz → precisão, revocação, F1 e "
          "alucinação; c) rotulador de operações → PA e UA; todos com comparações pareadas.",
          [], ["quadro6", "quadro7", "quadro8"]),
    ]),
]
