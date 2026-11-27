"""Perguntas de treino, grupos 5 a 7 (GU-JSON e prompt, SUMIE e dados, métricas e juiz)."""

from perguntas_dados_a import q

GRUPOS_B = [
    ("GU-JSON, esquema e *prompt*", [
        q("O que é o GU-JSON e por que ele, e não o CoK-JSON ou o GO/GM?",
          "*Generate-Update* em JSON: o escritor recebe o esquema, o estado anterior e a nova "
          "observação e regenera o JSON completo, $M_t = G(S, M_{t-1}, O_t)$. Toda a manutenção "
          "do estado fica em uma única chamada, sem algoritmos auxiliares de mesclagem.",
          ["Sob limite de *tokens*, o GU-JSON superou o GU-Text (Hwang et al., 2024).",
           "O CoK-JSON seleciona chaves antes de atualizar, o que acrescenta uma etapa "
           "auxiliar e dilui o efeito do escritor."],
          ["gujson", "rev_22_24"]),
        q("Por que reescrever o objeto inteiro em vez de aplicar operações parciais?",
          "A reescrita integral exige que o próprio modelo preserve, integre e mantenha a "
          "sintaxe ao mesmo tempo, e é exatamente essa capacidade que se quer medir. Operações "
          "aplicadas por código, como no PRISM (Jayalath et al., 2025), transferem parte do "
          "trabalho a um controlador externo.",
          [], ["gujson", "rev_22_24"],
          lim="O trabalho não compara GU-JSON com operações parciais."),
        q("Por que um esquema plano e mínimo?",
          "`{\"state\": {\"chave\": \"valor\"}}` é idêntico para todos os escritores e "
          "instâncias e isola a reescrita do estado.",
          [], ["prompt", "limitacoes"],
          lim="A validade externa fica restrita a esquemas planos de pares chave-valor."),
        q("Por que o *prompt* está em inglês?",
          "É o idioma nativo do SUMIE e dos modelos avaliados; o texto é idêntico para os três "
          "escritores.",
          [], ["prompt"]),
        q("Quais são as seis regras do *prompt-base*?",
          "Preservar o que continua válido; aplicar o que a observação introduz explicitamente; "
          "substituir só quando a observação estabelecer invalidade, mantendo perspectivas "
          "divergentes; não inventar fatos; respeitar o esquema; retornar só o JSON completo.",
          [], ["prompt"]),
        q("Por que limitar a saída a 1.200 *tokens*?",
          "Para seguir o regime de memória limitada de Hwang et al. (2024), com orçamento "
          "fixo para todos os escritores.",
          ["O piloto verifica se os estados esperados $M^*_t$ cabem inteiros no orçamento; "
           "assim, omissões são atribuídas ao escritor, e não a truncamento."],
          ["desenho", "sumie"]),
        q("E se algum estado esperado passar de 1.200 *tokens*?",
          "O protocolo exige que os estados esperados caibam inteiros no orçamento, e o piloto "
          "(Fase 1) verifica isso antes de fixar as regras.",
          [], ["sumie", "fases"],
          alerta="O artigo não diz o que fazer com transições acima do limite; decida (por "
                 "exemplo, excluí-las e reportá-las à parte) e leve a decisão pronta."),
        q("O orçamento de 1.200 *tokens* é justo entre tokenizadores diferentes?",
          "O limite vale na contagem de cada modelo; as diferenças de tokenizador são admitidas "
          "como parte do desempenho de cada representante.",
          [], ["harness", "quadro4"],
          alerta="O mesmo JSON pode ocupar números diferentes de *tokens* no Qwen3 e no "
                 "T5Gemma; proponha medir no piloto o comprimento de $M^*_t$ com cada "
                 "tokenizador."),
        q("Como se evita que a resposta esperada vaze para o escritor?",
          "Só o esquema, $M^*_{t-1}$ e $O_t$ entram no *prompt*; $M^*_t$, as anotações e os "
          "rótulos seguem por um caminho separado, usado apenas na avaliação.",
          [], ["harness", "fig2"]),
        q("Por que a entrada é o estado de referência, e não a saída do escritor no turno "
          "anterior?",
          "Para avaliar cada transição isoladamente: os erros de uma transição não se propagam "
          "para a seguinte.",
          [], ["sumie", "limitacoes"],
          lim="Não mede o acúmulo de erros que ocorreria em uso real."),
    ]),
    ("SUMIE e preparação dos dados", [
        q("O que é o SUMIE?",
          "*Benchmark* de sumarização incremental de entidades (Hwang et al., 2025): "
          "sequências de parágrafos com fatos novos, repetições, distratores e pontos de vista "
          "divergentes; cada parágrafo tem anotações de atributos e valores. Licença "
          "Apache-2.0.",
          [], ["sumie"]),
        q("Por que o SUMIE, e não LongMemEval, LoCoMo ou MemoryAgentBench?",
          "Esses *benchmarks* avaliam a memória pela resposta a perguntas no fim da sequência; o "
          "SUMIE anota atributos e valores por parágrafo, o que permite inspecionar o estado em "
          "cada transição.",
          ["Hu; Wang; McAuley (2025); Wu et al. (2024); Maharana et al. (2024)."],
          ["rev_22_24", "sumie"]),
        q("O que é a política de acumulação do SUMIE?",
          "Perspectivas distintas sobre um atributo são integradas: uma nova opinião não "
          "invalida automaticamente a anterior.",
          ["Está na regra 3 do *prompt*, na definição de UPDATE e no critério do juiz, que só "
           "aceita equivalências compatíveis com essa política."],
          ["sumie", "prompt"]),
        q("Como as transições são construídas?",
          "Cada etapa $t$ vira a tupla $(M^*_{t-1}, O_t, M^*_t)$: o estado acumulado de "
          "referência até $t-1$, o parágrafo do turno $t$ e o estado esperado depois de "
          "incorporá-lo.",
          [], ["sumie"]),
        q("Como são definidos PRESERVE, ADD e UPDATE?",
          "Por comparação determinística entre $M^*_{t-1}$ e $M^*_t$, atributo a atributo: "
          "PRESERVE já existia e não muda; ADD aparece pela primeira vez em $O_t$; UPDATE já "
          "existia e recebe complemento ou nova perspectiva.",
          [], ["sumie", "equacoes"]),
        q("Quantas entidades e transições serão avaliadas?",
          "Na Fase 2, toda a partição de avaliação do SUMIE; antes disso, 25 entidades "
          "separadas no piloto e 15 transições sintéticas na Fase 0.",
          [], ["fases", "sumie"],
          alerta="O artigo não informa o tamanho da partição de avaliação; levante o número de "
                 "entidades e de transições no repositório do SUMIE."),
        q("Os dados sintéticos não limitam as conclusões?",
          "Limitam o alcance: os resultados valem para sumarização incremental de entidades. Em "
          "troca, os dados são públicos, sem dados pessoais, e as entidades são mascaradas "
          "(por exemplo, ENTITY0).",
          [], ["fig2", "limitacoes"],
          lim="Validade externa: esquema plano e transições com estado de referência."),
        q("Como funciona a normalização textual?",
          "Espaços, caixa e pontuação são normalizados antes da correspondência direta; as "
          "regras são fixadas no piloto (Fase 1).",
          [], ["metricas", "fases"]),
    ]),
    ("Métricas e juiz semântico", [
        q("Quais métricas são primárias e por quê?",
          "State F1, Preservation Accuracy e Update Accuracy (agregada e separada em ADD e "
          "UPDATE): são as métricas das hipóteses. As estruturais e a taxa de alucinação "
          "completam o diagnóstico.",
          [], ["metricas", "quadro5", "desenho"]),
        q("Qual a diferença entre JSON Validity e Schema Validity?",
          "JSON Validity: a saída bruta é lida por `json.loads` sem reparo. Schema Validity: a "
          "saída contém exclusivamente o objeto raiz `state`, que mapeia chaves textuais a "
          "valores.",
          [], ["quadro5", "metricas"]),
        q("Como se calculam a precisão, a revocação e o F1 do estado?",
          "O JSON vira pares caminho-valor (`state.<atributo>`, valor normalizado), sem ordem "
          "de chaves. TP: pares correspondentes diretamente ou aceitos pelo juiz; FP: pares "
          "gerados não correspondentes ou não sustentados; FN: fatos esperados ausentes. "
          "$P = TP/(TP+FP)$, $R = TP/(TP+FN)$, $F_1 = 2PR/(P+R)$.",
          ["As correspondências são um-para-um."],
          ["equacoes", "metricas"]),
        q("Qual a diferença entre falso positivo e alucinação?",
          "Alucinação é o par gerado sem correspondência esperada e sem suporte nas anotações, "
          "em $M^*_{t-1}$ ou em $O_t$; FP inclui todo par gerado não correspondente ou não "
          "sustentado.",
          [], ["quadro5", "equacoes"],
          alerta="O artigo não explicita a relação; leia-a como \"alucinação ⊆ FP\": um FP com "
                 "apoio na entrada (por exemplo, um detalhe não anotado) não é alucinação."),
        q("O que são as visões condicional e global?",
          "Condicional: só as transições com JSON válido e aderente ao esquema, isolando a "
          "qualidade do conteúdo. Global (*end-to-end*): falhas estruturais recebem zero, "
          "refletindo a confiabilidade efetiva do escritor.",
          [], ["metricas"]),
        q("O que são os resultados estritos e os híbridos?",
          "Estritos: só correspondência direta após normalização. Híbridos: incluem as "
          "equivalências aceitas pelo juiz. Os dois são reportados; as métricas primárias usam "
          "o híbrido.",
          [], ["metricas", "juiz"]),
        q("Por que usar um modelo de linguagem como juiz?",
          "A avaliação original do SUMIE já usa um juiz para o alinhamento semântico; aqui ele "
          "só é chamado para as divergências que a correspondência direta não resolve.",
          ["Recebe $M^*_{t-1}$, $O_t$, $M^*_t$, as anotações e o estado gerado; decide entre "
           "equivalente, ausente/contradito ou incerto.",
           "Não pode inferir suporte por plausibilidade geral."],
          ["juiz", "metricas"]),
        q("Como se controla o viés do juiz?",
          "Versão, quantização e *prompt* congelados antes da Fase 2; julgamento cego à "
          "identidade do escritor; incertos reportados à parte, sem contar como acerto; "
          "amostra auditada manualmente; resultados estritos e proporção enviada ao juiz "
          "divulgados.",
          [], ["juiz", "limitacoes"]),
        q("O juiz Gemma 3 1B não favorece o T5Gemma, da mesma família?",
          "O juiz é independente dos três escritores e não sabe qual deles gerou a saída; os "
          "resultados estritos permitem verificar se o juiz muda a ordem dos escritores.",
          [], ["juiz", "modelos"],
          alerta="O T5Gemma é adaptado de modelos Gemma e o artigo não discute esse risco de "
                 "afinidade; prepare a resposta e proponha comparar estrito × híbrido por "
                 "escritor."),
        q("Um juiz de 1B quantizado em Q4_K_M é confiável?",
          "Foi escolhido por ser aberto, local e caber no limite de 4 GiB de memória residente; "
          "ele só decide divergências e é verificado no piloto por auditoria manual.",
          [], ["juiz", "fases"],
          alerta="Q4_K_M é uma quantização GGUF de cerca de 4 bits por peso; o artigo não "
                 "define o tamanho da amostra auditada nem o critério de aceite. Defina-os."),
        q("Como se calculam a Preservation Accuracy e a Update Accuracy?",
          "PA: atributos PRESERVE mantidos corretamente sobre o total de PRESERVE esperados. "
          "UA: atributos ADD ou UPDATE registrados corretamente sobre o total esperado, também "
          "separada por operação.",
          ["Correto = correspondência direta ou equivalência confirmada pelo juiz; incertos "
           "ficam à parte."],
          ["equacoes"]),
    ]),
]
