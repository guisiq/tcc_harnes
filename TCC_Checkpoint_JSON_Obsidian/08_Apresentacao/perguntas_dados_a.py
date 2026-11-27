"""Perguntas de treino, grupos 1 a 4 (problema, lacuna, revisão e modelos).

Cada pergunta: p (pergunta), r (resposta direta), ev (evidências), lim (limite honesto),
alerta (ponto fraco a preparar: o artigo não traz a informação ou ela precisa ser conferida)
e apoio (chaves de slides; "@chave" aponta para a referência no final do apêndice).
"""


def q(p, r, ev=(), apoio=(), lim=None, alerta=None):
    return {"p": p, "r": r, "ev": list(ev), "apoio": list(apoio), "lim": lim, "alerta": alerta}


GRUPOS_A = [
    ("Problema, escopo e relevância", [
        q("Qual é o problema do trabalho, em uma frase?",
          "No GU-JSON o escritor reescreve o *checkpoint* inteiro a cada turno, o que pode "
          "corromper a sintaxe/esquema ou omitir, alterar e inventar fatos; não se sabe como "
          "escritores compactos de paradigmas gerativos diferentes se comportam nessa função.",
          ["GU-JSON supera a atualização em texto livre sob orçamento de *tokens* "
           "(Hwang et al., 2024).",
           "O escritor vira ponto crítico de falha: JSON inválido ou fora do esquema "
           "(Geng et al., 2025) e perda/distorção de fatos.",
           "Reescrever a cada turno com modelos grandes eleva custo e latência; SLMs permitem "
           "execução local (Lu et al., 2025; Sharma; Mehta, 2025)."],
          ["contexto", "gujson", "justificativa"]),
        q("O que é um *harness* de agentes e qual a diferença para o *harness* experimental?",
          "*Harness* de agentes é a camada de software que envolve o modelo: seleciona o "
          "contexto, disponibiliza ferramentas e coordena ações. O *harness* experimental deste "
          "trabalho só padroniza as entradas, a execução dos escritores e a avaliação.",
          ["A memória integra o *harness*: geração/atualização e recuperação "
           "(Sumers et al., 2024; Zeng et al., 2024).",
           "O estudo investiga só a escrita incremental, sem recuperação nem agente completo."],
          ["contexto", "harness"]),
        q("Por que estudar só a escrita da memória, e não a recuperação ou o agente completo?",
          "Porque a fidelidade da escrita condiciona o que estará disponível para recuperação; "
          "isolar a escrita permite medir diretamente cada transição.",
          ["Avaliações só pela resposta final podem mascarar a perda silenciosa de atributos "
           "(Seção 2.4).",
           "Um esquema JSON único e fixo isola a reescrita do estado (Seção 2.2)."],
          ["contexto", "rev_22_24", "limitacoes"],
          lim="Não mede o impacto do *checkpoint* nas decisões do agente (validade externa)."),
        q("O que é exatamente um *checkpoint* JSON neste trabalho?",
          "É o estado persistente da entidade, no esquema `{\"state\": {\"chave\": \"valor\"}}`, "
          "regenerado por completo a cada turno pelo escritor.",
          ["Pares atributo-valor explícitos permitem inspecionar o estado a cada transição "
           "(Jayalath et al., 2025; Yuen et al., 2025).",
           "Esquema plano: atributos como chaves textuais e conteúdos como valores em texto."],
          ["gujson", "prompt"]),
        q("Por que usar modelos compactos como escritores de memória?",
          "Porque a reescrita acontece a cada turno: com modelos grandes, custo e latência "
          "crescem; SLMs permitem execução local e menor consumo em subtarefas delimitadas e "
          "restritas por esquema.",
          ["Lu et al. (2025); Sharma; Mehta (2025).",
           "Modelos de até ~4B já atuam como extratores ou gestores de memória (Fioresi et al., "
           "2026; Hwang; Diao, 2026; Kang et al., 2026; Zheng et al., 2026)."],
          ["justificativa", "paradigmas"],
          lim="Modelos menores são mais sensíveis à quantização (Lee et al., 2025); por isso a "
              "precisão numérica é padronizada."),
        q("Qual é a relação do trabalho com Sistemas de Informação?",
          "Avalia a confiabilidade de um componente de software — a memória persistente de "
          "sistemas baseados em agentes —, envolvendo persistência e validação de dados "
          "estruturados (JSON), avaliação experimental de componentes e execução local com "
          "recursos limitados.",
          [], ["contexto", "harness"],
          alerta="O artigo não explicita esse vínculo; prepare 2 ou 3 frases próprias ligando "
                 "o trabalho a disciplinas do curso."),
        q("Qual é a contribuição esperada?",
          "Evidência empírica comparativa entre os três escritores e um protocolo com *harness* "
          "reutilizável para avaliar escritores compactos de memória.",
          ["Quatro conjuntos de evidências: robustez estrutural; fidelidade global e "
           "longitudinal; perfil de erro por operação; relação entre validade sintática e "
           "fidelidade semântica."],
          ["resultados"]),
    ]),
    ("Lacuna e trabalhos relacionados", [
        q("Qual é, exatamente, a lacuna?",
          "Não se identificou comparação controlada entre representantes compactos de "
          "paradigmas gerativos distintos atuando só como escritores de um mesmo *checkpoint* "
          "JSON sob orçamento fixo de *tokens*.",
          ["GU-JSON e SUMIE foram avaliados só com modelos proprietários de grande porte "
           "(Hwang et al., 2024; 2025).",
           "AR × difusão em fluxos agênticos: modelos de 7 a 8B e memória em texto livre "
           "(Lu et al., 2026).",
           "SLMs como gestores operam sobre registros, sem comparar paradigmas (Hwang; Diao, "
           "2026; Kang et al., 2026)."],
          ["lacuna", "quadro1_1", "quadro1_2"]),
        q("Se modelos compactos já atuam como gestores de memória, a lacuna não desaparece?",
          "Não: o uso isolado de um escritor compacto não é a lacuna. A lacuna é a combinação "
          "de GU-JSON com reescrita integral, transições do SUMIE, três paradigmas e avaliação "
          "da validade e da fidelidade por operação.",
          ["No núcleo, o modelo costuma emitir operações aplicadas por código; a avaliação "
           "recai sobre ações de escrita, chaves isoladas ou estado de diálogo (Ali; Abdallah; "
           "Jatowt, 2026; Lee; Pfister, 2026; Qin; Lu, 2026).",
           "Yuen et al. (2025) reescrevem a memória, mas avaliam o desempenho na tarefa."],
          ["lacuna", "quadro1_1", "quadro1_2"]),
        q("Qual trabalho é o mais próximo do seu e em que difere?",
          "Pelo mecanismo, Yuen et al. (2025): reescrevem a memória a cada turno a partir da "
          "anterior, mas com Llama-3.2-3B, memória textual por seções e avaliação das tarefas, "
          "não do estado. Como fundamento, Hwang et al. (2024; 2025): GU-JSON e SUMIE, porém "
          "com modelos Gemini de grande porte.",
          [], ["quadro1_1", "base"]),
        q("Algum estudo já compara difusão e autoregressão?",
          "No núcleo, nenhum: todos os escritores são autoregressivos. Na revisão apareceu só "
          "um estudo sobre planos textuais editáveis (Zhou; Xiong; Tan, 2026), fora dos "
          "critérios; em fluxos agênticos, Lu et al. (2026), com 7 a 8B e memória em texto "
          "livre.",
          [], ["lacuna", "elegibilidade"]),
        q("Por que Hwang, Jayalath, Zeng e Geng não aparecem no Quadro 1?",
          "São estudos de base do levantamento anterior à revisão; fundamentam o trabalho, mas o "
          "Quadro 1 se restringe aos 12 estudos do núcleo. Yuen et al. (2025) também era de base "
          "e foi recuperado pela revisão, por isso integra o núcleo.",
          [], ["base", "quadro1_1"]),
        q("Como garantir que a lacuna é real, e não um efeito da busca?",
          "Não se afirma a inexistência: o Quadro 1 indica os estudos mais próximos no escopo "
          "examinado.",
          ["Oito consultas por facetas; 12 estudos de controle, todos recuperados.",
           "Grupos atribuídos por regras do *script* e trechos literais conferidos."],
          ["revisao", "busca", "elegibilidade"],
          lim="Fonte única (arXiv), codificação por um único modelo sem revisor humano e "
              "estudos sem o tamanho do escritor ficam fora do núcleo."),
    ]),
    ("Revisão sistemática", [
        q("Como foi feita a revisão sistemática?",
          "Sete etapas: protocolo versionado; busca na API do arXiv (título e resumo, oito "
          "consultas); 12 estudos de controle; deduplicação e exclusão por termos (738 → 696); "
          "triagem codificada por C1–C7; elegibilidade com texto integral; extração e síntese "
          "(12 estudos no núcleo).",
          [], ["revisao", "quadro2", "busca", "triagem", "elegibilidade"]),
        q("Por que buscar só no arXiv?",
          "A fonte única é uma limitação declarada. Argumento possível: a área é recente, a "
          "janela é curta (jul./2025 a nov./2026), os trabalhos circulam primeiro como "
          "*preprints* e a API permite uma busca automatizada e reprodutível.",
          [], ["revisao", "busca"],
          alerta="O artigo declara a limitação, mas não justifica a escolha; prepare o argumento "
                 "e diga se pretende ampliar as fontes no TCC II."),
        q("Por que a janela de 1º/07/2025 a 19/11/2026?",
          "Ela capta os trabalhos recentes posteriores aos estudos de base, que vieram do "
          "levantamento anterior, e termina na data da execução da busca.",
          [], ["busca"],
          alerta="O artigo não justifica o início em julho de 2025; tenha essa justificativa "
                 "pronta."),
        q("Usar um modelo de linguagem na triagem não compromete a validade?",
          "O modelo não decide a inclusão: ele só registra S, I ou N para C1–C7 e códigos de "
          "exclusão; os grupos e as classes são atribuídos por regras do *script*.",
          ["Triagem: claude-haiku-5.5 via GitHub Copilot SDK 1.0.31, roteiro fixo, resposta "
           "validada por esquema JSON, lotes de 20 registros.",
           "Elegibilidade: cada S exige trecho literal (20 a 400 caracteres) conferido no texto, "
           "senão vira I; C5 vira N se o trecho só cita modelos acima de 4,5B."],
          ["triagem", "elegibilidade"],
          lim="Um único modelo, sem revisor humano independente: as regras reduzem, mas não "
              "eliminam, erros de codificação."),
        q("Quais são os critérios C1 a C7?",
          "C1 estudo primário; C2 memória textual mantida por modelo de linguagem; C3 "
          "atualização incremental; C4 estrutura explícita; C5 escritor ou gestor de até ~4B; "
          "C6 avaliação direta do estado ou das operações de escrita; C7 comparação entre "
          "paradigmas gerativos.",
          [], ["triagem"]),
        q("Por que o núcleo não exige C7?",
          "Porque C7 é justamente a lacuna: exigir comparação de paradigmas esvaziaria o núcleo. "
          "C7 serve para identificar comparadores gerativos, que formam classe própria "
          "(1 estudo).",
          [], ["elegibilidade", "lacuna"],
          alerta="O artigo não explica isso no texto; a resposta é uma inferência sua, então "
                 "formule-a com segurança."),
        q("Por que o limite de ~4 bilhões de parâmetros?",
          "É o critério C5 de escritor compacto; trechos que só citam modelos acima de 4,5B "
          "rebaixam C5 a ausente.",
          ["No núcleo, vários gestores e escritores ficam nessa faixa (Qwen3-4B, Qwen3.5-4B, "
           "Ministral-3-3B, Qwen2.5-3B)."],
          ["triagem", "elegibilidade", "quadro1_1"],
          alerta="O artigo não justifica o corte em 4B; argumento possível: é a faixa em que a "
                 "literatura já usa gestores compactos e que ainda roda localmente."),
        q("Como os números da revisão se fecham?",
          "As 8 consultas somam 905 registros (com sobreposição): 738 únicos → −42 por termos "
          "no título → 696 triados → 189 para elegibilidade (22 prováveis + 165 incertos + "
          "2 comparadores) → 12 núcleo, 2 pendentes, 1 comparador, 8 escritor compacto, "
          "52 avaliação do estado, 70 memória estruturada e 44 exclusões.",
          ["Os outros 507 triados: 42 incertos sem base, 59 de contexto e 406 exclusões.",
           "As 44 exclusões: 8 por ausência e 36 por critério não demonstrado."],
          ["quadro2", "triagem", "elegibilidade"]),
        q("Os estudos de controle validam a busca?",
          "Não de forma independente: os 12 foram todos recuperados, mas orientaram a "
          "construção das consultas e não foram acrescentados manualmente.",
          [], ["busca", "revisao"]),
        q("A revisão é reprodutível?",
          "Em grande parte: protocolo, livro de códigos, roteiros, termos de exclusão, *scripts* "
          "em C# (.NET 10), expressões completas, respostas brutas da API com *hash* SHA-256, "
          "codificações com trechos conferidos e *hashes* dos textos integrais estão no "
          "repositório público, versão v2.1.0.",
          ["Os textos integrais não são redistribuídos, mas o *script* os reconstitui e confere "
           "os *hashes*."],
          ["revisao", "busca"],
          lim="Reexecutar a codificação por modelo de linguagem pode gerar respostas diferentes; "
              "por isso as codificações estão versionadas."),
        q("Que diretriz metodológica orientou a revisão?",
          "O protocolo segue as etapas usuais de estudos secundários em engenharia de software: "
          "planejamento, busca, triagem, elegibilidade, extração e síntese.",
          [], ["revisao", "@petersen"],
          alerta="Petersen, Vakkalanka e Kuzniarz (2015) está nas referências, mas não é citado "
                 "no texto; cite-o na Seção 3.1 (ou retire-o) e saiba dizer o que adotou dele."),
    ]),
    ("Modelos e paradigmas gerativos", [
        q("Por que esses três modelos?",
          "Representam três paradigmas gerativos — autoregressivo *decoder-only*, "
          "*encoder-decoder* e difusão em blocos — em escala aproximada (~0,6B), com pesos "
          "públicos e execução local viável.",
          [], ["paradigmas", "modelos"]),
        q("Qual a diferença entre os três paradigmas?",
          "*Decoder-only*: gera *token* a *token*, da esquerda para a direita (Qwen3). "
          "*Encoder-decoder*: um codificador bidirecional lê toda a entrada e o decodificador "
          "gera a saída (T5Gemma, adaptado de *decoder-only*). Difusão em blocos: blocos "
          "gerados em sequência, com remoção de ruído paralela dos *tokens* mascarados dentro de "
          "cada bloco (BD3LM).",
          ["Yang et al. (2025); Zhang et al. (2025); Nie et al. (2024); Arriola et al. (2025)."],
          ["paradigmas"]),
        q("As diferenças poderão ser atribuídas ao paradigma gerativo?",
          "Não de forma causal isolada: os modelos diferem também em corpus de pré-treinamento, "
          "tokenizador e pós-treinamento. Compara-se o desempenho efetivo de representantes.",
          ["Mitigação: *zero-shot*, *prompt-only*, precisão numérica padronizada e sem "
           "decodificação restrita."],
          ["limitacoes", "modelos"]),
        q("Por que 0,6B, e não 1B a 4B?",
          "É a escala em que os três paradigmas têm representantes públicos comparáveis e que "
          "roda no *hardware* local.",
          [], ["modelos", "harness"],
          alerta="O artigo justifica pela escala comum e pela execução local, mas não discute "
                 "escalas maiores; tenha o argumento pronto (disponibilidade de representantes "
                 "e memória da GPU)."),
        q("De onde vem o Qwen3-0.6B BD3LM?",
          "É o representante de difusão em blocos; o nome indica derivação do Qwen3-0.6B, "
          "adaptando pesos autoregressivos para difusão (Gong et al., 2024; Arriola et al., "
          "2025).",
          [], ["modelos", "paradigmas"],
          alerta="Diferentemente do Qwen3 e do T5Gemma, o artigo não traz nota de rodapé com o "
                 "*checkpoint* do BD3LM; tenha em mãos o identificador exato, quem o publicou, "
                 "a licença e a confirmação de que deriva do Qwen3-0.6B."),
        q("O T5Gemma B-B tem mesmo ~0,6B? Por que a variante PrefixLM-IT?",
          "O artigo o coloca na faixa de 0,6B (codificador e decodificador de tamanho *base*); a "
          "variante IT é ajustada por instruções, necessária para seguir o *prompt* *zero-shot* "
          "como os demais.",
          [], ["modelos"],
          alerta="Confira no *model card* (google/t5gemma-b-b-prefixlm-it) o número exato de "
                 "parâmetros e o que significa o objetivo de adaptação PrefixLM."),
        q("Por que desativar o modo *thinking* do Qwen3?",
          "Para que o orçamento de 1.200 *tokens* seja consumido só pelo objeto JSON.",
          [], ["modelos", "harness"]),
        q("Por que não usar decodificação restrita por gramática?",
          "Para observar a capacidade intrínseca de cada modelo: os motores de decodificação "
          "restrita atuam de modo distinto sobre a geração sequencial e sobre o refinamento por "
          "difusão, o que confundiria a comparação.",
          ["Geng et al. (2023; 2025); Mündler; Dekoninck; Vechev (2025); Khanal et al. (2026)."],
          ["paradigmas", "desenho"]),
        q("Por que não fazer ajuste fino (*fine-tuning*)?",
          "O desenho é *zero-shot* e *prompt-only* para comparar os representantes sem "
          "introduzir variáveis de treinamento; vários estudos do núcleo treinam gestores "
          "(GRPO, LoRA, SFT), mas aqui se mede o comportamento instrucional.",
          [], ["desenho", "quadro1_1"]),
        q("Os modelos cabem na GTX 1650?",
          "A Fase 0 valida o carregamento dos três escritores e do juiz; a precisão numérica "
          "(FP16 ou BF16) será uniforme entre os modelos.",
          [], ["harness", "fases"],
          alerta="A GTX 1650 tem 4 GB de VRAM e não tem suporte nativo a BF16 (arquitetura "
                 "Turing); na prática a precisão uniforme tende a ser FP16 ou FP32. Tenha um "
                 "plano B (por exemplo, CPU com os 24 GB de RAM) e meça o uso de memória."),
    ]),
]
