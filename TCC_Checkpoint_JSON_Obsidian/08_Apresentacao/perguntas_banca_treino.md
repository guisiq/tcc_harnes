---
title: "Perguntas da banca — treino da arguição"
aliases:
  - "perguntas banca treino"
tags:
  - tcc
  - apresentacao
status: draft
---

# Perguntas da banca — treino da arguição

86 perguntas prováveis, em 10 grupos, com base no artigo do TCC I. Arquivo gerado por `gerar_apresentacao.py`; edite as perguntas em `perguntas_dados_*.py`.

## Como treinar

1. Leia a pergunta e responda **em voz alta, em até 1 minuto**, nesta ordem: **resposta direta → evidência do trabalho → limite**.
2. Só então abra **Pontos-chave** e compare.
3. Se a resposta pedir detalhe, abra o slide indicado em **Apoio**: no Modo do Apresentador, digite o número do slide e tecle Enter; para voltar ao encerramento, digite 25 e Enter.
4. Os 23 itens marcados com ⚠️ são pontos fracos ou informações que o artigo não traz; a lista no final reúne o que preparar ou corrigir antes da banca.

## Grupos

1. [[#1. Problema, escopo e relevância|Problema, escopo e relevância]] (7)
2. [[#2. Lacuna e trabalhos relacionados|Lacuna e trabalhos relacionados]] (6)
3. [[#3. Revisão sistemática|Revisão sistemática]] (11)
4. [[#4. Modelos e paradigmas gerativos|Modelos e paradigmas gerativos]] (10)
5. [[#5. GU-JSON, esquema e prompt|GU-JSON, esquema e prompt]] (10)
6. [[#6. SUMIE e preparação dos dados|SUMIE e preparação dos dados]] (8)
7. [[#7. Métricas e juiz semântico|Métricas e juiz semântico]] (11)
8. [[#8. Hipóteses e análise estatística|Hipóteses e análise estatística]] (9)
9. [[#9. Limitações, ética e reprodutibilidade|Limitações, ética e reprodutibilidade]] (7)
10. [[#10. Resultados esperados e cronograma|Resultados esperados e cronograma]] (7)

## 1. Problema, escopo e relevância

### 1.1 Qual é o problema do trabalho, em uma frase?

> [!tip]- Pontos-chave
> **Resposta direta:** No GU-JSON o escritor reescreve o *checkpoint* inteiro a cada turno, o que pode corromper a sintaxe/esquema ou omitir, alterar e inventar fatos; não se sabe como escritores compactos de paradigmas gerativos diferentes se comportam nessa função.
>
> - GU-JSON supera a atualização em texto livre sob orçamento de *tokens* (Hwang et al., 2024).
> - O escritor vira ponto crítico de falha: JSON inválido ou fora do esquema (Geng et al., 2025) e perda/distorção de fatos.
> - Reescrever a cada turno com modelos grandes eleva custo e latência; SLMs permitem execução local (Lu et al., 2025; Sharma; Mehta, 2025).

**Apoio:** slide 2 · slide 3 · slide 4

### 1.2 O que é um *harness* de agentes e qual a diferença para o *harness* experimental?

> [!tip]- Pontos-chave
> **Resposta direta:** *Harness* de agentes é a camada de software que envolve o modelo: seleciona o contexto, disponibiliza ferramentas e coordena ações. O *harness* experimental deste trabalho só padroniza as entradas, a execução dos escritores e a avaliação.
>
> - A memória integra o *harness*: geração/atualização e recuperação (Sumers et al., 2024; Zeng et al., 2024).
> - O estudo investiga só a escrita incremental, sem recuperação nem agente completo.

**Apoio:** slide 2 · slide 14

### 1.3 Por que estudar só a escrita da memória, e não a recuperação ou o agente completo?

> [!tip]- Pontos-chave
> **Resposta direta:** Porque a fidelidade da escrita condiciona o que estará disponível para recuperação; isolar a escrita permite medir diretamente cada transição.
>
> - Avaliações só pela resposta final podem mascarar a perda silenciosa de atributos (Seção 2.4).
> - Um esquema JSON único e fixo isola a reescrita do estado (Seção 2.2).
>
> **Limite:** Não mede o impacto do *checkpoint* nas decisões do agente (validade externa).

**Apoio:** slide 2 · A4 (slide 30) · slide 21

### 1.4 O que é exatamente um *checkpoint* JSON neste trabalho?

> [!tip]- Pontos-chave
> **Resposta direta:** É o estado persistente da entidade, no esquema `{"state": {"chave": "valor"}}`, regenerado por completo a cada turno pelo escritor.
>
> - Pares atributo-valor explícitos permitem inspecionar o estado a cada transição (Jayalath et al., 2025; Yuen et al., 2025).
> - Esquema plano: atributos como chaves textuais e conteúdos como valores em texto.

**Apoio:** slide 3 · A14 (slide 40)

### 1.5 Por que usar modelos compactos como escritores de memória?

> [!tip]- Pontos-chave
> **Resposta direta:** Porque a reescrita acontece a cada turno: com modelos grandes, custo e latência crescem; SLMs permitem execução local e menor consumo em subtarefas delimitadas e restritas por esquema.
>
> - Lu et al. (2025); Sharma; Mehta (2025).
> - Modelos de até ~4B já atuam como extratores ou gestores de memória (Fioresi et al., 2026; Hwang; Diao, 2026; Kang et al., 2026; Zheng et al., 2026).
>
> **Limite:** Modelos menores são mais sensíveis à quantização (Lee et al., 2025); por isso a precisão numérica é padronizada.

**Apoio:** slide 4 · slide 5

### 1.6 ⚠️ Qual é a relação do trabalho com Sistemas de Informação?

> [!tip]- Pontos-chave
> **Resposta direta:** Avalia a confiabilidade de um componente de software — a memória persistente de sistemas baseados em agentes —, envolvendo persistência e validação de dados estruturados (JSON), avaliação experimental de componentes e execução local com recursos limitados.
>
> > [!warning] Preparar
> > O artigo não explicita esse vínculo; prepare 2 ou 3 frases próprias ligando o trabalho a disciplinas do curso.

**Apoio:** slide 2 · slide 14

### 1.7 Qual é a contribuição esperada?

> [!tip]- Pontos-chave
> **Resposta direta:** Evidência empírica comparativa entre os três escritores e um protocolo com *harness* reutilizável para avaliar escritores compactos de memória.
>
> - Quatro conjuntos de evidências: robustez estrutural; fidelidade global e longitudinal; perfil de erro por operação; relação entre validade sintática e fidelidade semântica.

**Apoio:** slide 20

## 2. Lacuna e trabalhos relacionados

### 2.1 Qual é, exatamente, a lacuna?

> [!tip]- Pontos-chave
> **Resposta direta:** Não se identificou comparação controlada entre representantes compactos de paradigmas gerativos distintos atuando só como escritores de um mesmo *checkpoint* JSON sob orçamento fixo de *tokens*.
>
> - GU-JSON e SUMIE foram avaliados só com modelos proprietários de grande porte (Hwang et al., 2024; 2025).
> - AR × difusão em fluxos agênticos: modelos de 7 a 8B e memória em texto livre (Lu et al., 2026).
> - SLMs como gestores operam sobre registros, sem comparar paradigmas (Hwang; Diao, 2026; Kang et al., 2026).

**Apoio:** slide 6 · A1 (slide 27) · A2 (slide 28)

### 2.2 Se modelos compactos já atuam como gestores de memória, a lacuna não desaparece?

> [!tip]- Pontos-chave
> **Resposta direta:** Não: o uso isolado de um escritor compacto não é a lacuna. A lacuna é a combinação de GU-JSON com reescrita integral, transições do SUMIE, três paradigmas e avaliação da validade e da fidelidade por operação.
>
> - No núcleo, o modelo costuma emitir operações aplicadas por código; a avaliação recai sobre ações de escrita, chaves isoladas ou estado de diálogo (Ali; Abdallah; Jatowt, 2026; Lee; Pfister, 2026; Qin; Lu, 2026).
> - Yuen et al. (2025) reescrevem a memória, mas avaliam o desempenho na tarefa.

**Apoio:** slide 6 · A1 (slide 27) · A2 (slide 28)

### 2.3 Qual trabalho é o mais próximo do seu e em que difere?

> [!tip]- Pontos-chave
> **Resposta direta:** Pelo mecanismo, Yuen et al. (2025): reescrevem a memória a cada turno a partir da anterior, mas com Llama-3.2-3B, memória textual por seções e avaliação das tarefas, não do estado. Como fundamento, Hwang et al. (2024; 2025): GU-JSON e SUMIE, porém com modelos Gemini de grande porte.

**Apoio:** A1 (slide 27) · A3 (slide 29)

### 2.4 Algum estudo já compara difusão e autoregressão?

> [!tip]- Pontos-chave
> **Resposta direta:** No núcleo, nenhum: todos os escritores são autoregressivos. Na revisão apareceu só um estudo sobre planos textuais editáveis (Zhou; Xiong; Tan, 2026), fora dos critérios; em fluxos agênticos, Lu et al. (2026), com 7 a 8B e memória em texto livre.

**Apoio:** slide 6 · A8 (slide 34)

### 2.5 Por que Hwang, Jayalath, Zeng e Geng não aparecem no Quadro 1?

> [!tip]- Pontos-chave
> **Resposta direta:** São estudos de base do levantamento anterior à revisão; fundamentam o trabalho, mas o Quadro 1 se restringe aos 12 estudos do núcleo. Yuen et al. (2025) também era de base e foi recuperado pela revisão, por isso integra o núcleo.

**Apoio:** A3 (slide 29) · A1 (slide 27)

### 2.6 Como garantir que a lacuna é real, e não um efeito da busca?

> [!tip]- Pontos-chave
> **Resposta direta:** Não se afirma a inexistência: o Quadro 1 indica os estudos mais próximos no escopo examinado.
>
> - Oito consultas por facetas; 12 estudos de controle, todos recuperados.
> - Grupos atribuídos por regras do *script* e trechos literais conferidos.
>
> **Limite:** Fonte única (arXiv), codificação por um único modelo sem revisor humano e estudos sem o tamanho do escritor ficam fora do núcleo.

**Apoio:** slide 10 · A10 (slide 36) · A8 (slide 34)

## 3. Revisão sistemática

### 3.1 Como foi feita a revisão sistemática?

> [!tip]- Pontos-chave
> **Resposta direta:** Sete etapas: protocolo versionado; busca na API do arXiv (título e resumo, oito consultas); 12 estudos de controle; deduplicação e exclusão por termos (738 → 696); triagem codificada por C1–C7; elegibilidade com texto integral; extração e síntese (12 estudos no núcleo).

**Apoio:** slide 10 · A6 (slide 32) · A10 (slide 36) · A7 (slide 33) · A8 (slide 34)

### 3.2 ⚠️ Por que buscar só no arXiv?

> [!tip]- Pontos-chave
> **Resposta direta:** A fonte única é uma limitação declarada. Argumento possível: a área é recente, a janela é curta (jul./2025 a nov./2026), os trabalhos circulam primeiro como *preprints* e a API permite uma busca automatizada e reprodutível.
>
> > [!warning] Preparar
> > O artigo declara a limitação, mas não justifica a escolha; prepare o argumento e diga se pretende ampliar as fontes no TCC II.

**Apoio:** slide 10 · A10 (slide 36)

### 3.3 ⚠️ Por que a janela de 1º/07/2025 a 19/11/2026?

> [!tip]- Pontos-chave
> **Resposta direta:** Ela capta os trabalhos recentes posteriores aos estudos de base, que vieram do levantamento anterior, e termina na data da execução da busca.
>
> > [!warning] Preparar
> > O artigo não justifica o início em julho de 2025; tenha essa justificativa pronta.

**Apoio:** A10 (slide 36)

### 3.4 Usar um modelo de linguagem na triagem não compromete a validade?

> [!tip]- Pontos-chave
> **Resposta direta:** O modelo não decide a inclusão: ele só registra S, I ou N para C1–C7 e códigos de exclusão; os grupos e as classes são atribuídos por regras do *script*.
>
> - Triagem: claude-haiku-5.5 via GitHub Copilot SDK 1.0.31, roteiro fixo, resposta validada por esquema JSON, lotes de 20 registros.
> - Elegibilidade: cada S exige trecho literal (20 a 400 caracteres) conferido no texto, senão vira I; C5 vira N se o trecho só cita modelos acima de 4,5B.
>
> **Limite:** Um único modelo, sem revisor humano independente: as regras reduzem, mas não eliminam, erros de codificação.

**Apoio:** A7 (slide 33) · A8 (slide 34)

### 3.5 Quais são os critérios C1 a C7?

> [!tip]- Pontos-chave
> **Resposta direta:** C1 estudo primário; C2 memória textual mantida por modelo de linguagem; C3 atualização incremental; C4 estrutura explícita; C5 escritor ou gestor de até ~4B; C6 avaliação direta do estado ou das operações de escrita; C7 comparação entre paradigmas gerativos.

**Apoio:** A7 (slide 33)

### 3.6 ⚠️ Por que o núcleo não exige C7?

> [!tip]- Pontos-chave
> **Resposta direta:** Porque C7 é justamente a lacuna: exigir comparação de paradigmas esvaziaria o núcleo. C7 serve para identificar comparadores gerativos, que formam classe própria (1 estudo).
>
> > [!warning] Preparar
> > O artigo não explica isso no texto; a resposta é uma inferência sua, então formule-a com segurança.

**Apoio:** A8 (slide 34) · slide 6

### 3.7 ⚠️ Por que o limite de ~4 bilhões de parâmetros?

> [!tip]- Pontos-chave
> **Resposta direta:** É o critério C5 de escritor compacto; trechos que só citam modelos acima de 4,5B rebaixam C5 a ausente.
>
> - No núcleo, vários gestores e escritores ficam nessa faixa (Qwen3-4B, Qwen3.5-4B, Ministral-3-3B, Qwen2.5-3B).
>
> > [!warning] Preparar
> > O artigo não justifica o corte em 4B; argumento possível: é a faixa em que a literatura já usa gestores compactos e que ainda roda localmente.

**Apoio:** A7 (slide 33) · A8 (slide 34) · A1 (slide 27)

### 3.8 Como os números da revisão se fecham?

> [!tip]- Pontos-chave
> **Resposta direta:** As 8 consultas somam 905 registros (com sobreposição): 738 únicos → −42 por termos no título → 696 triados → 189 para elegibilidade (22 prováveis + 165 incertos + 2 comparadores) → 12 núcleo, 2 pendentes, 1 comparador, 8 escritor compacto, 52 avaliação do estado, 70 memória estruturada e 44 exclusões.
>
> - Os outros 507 triados: 42 incertos sem base, 59 de contexto e 406 exclusões.
> - As 44 exclusões: 8 por ausência e 36 por critério não demonstrado.

**Apoio:** A6 (slide 32) · A7 (slide 33) · A8 (slide 34)

### 3.9 Os estudos de controle validam a busca?

> [!tip]- Pontos-chave
> **Resposta direta:** Não de forma independente: os 12 foram todos recuperados, mas orientaram a construção das consultas e não foram acrescentados manualmente.

**Apoio:** A10 (slide 36) · slide 10

### 3.10 A revisão é reprodutível?

> [!tip]- Pontos-chave
> **Resposta direta:** Em grande parte: protocolo, livro de códigos, roteiros, termos de exclusão, *scripts* em C# (.NET 10), expressões completas, respostas brutas da API com *hash* SHA-256, codificações com trechos conferidos e *hashes* dos textos integrais estão no repositório público, versão v2.1.0.
>
> - Os textos integrais não são redistribuídos, mas o *script* os reconstitui e confere os *hashes*.
>
> **Limite:** Reexecutar a codificação por modelo de linguagem pode gerar respostas diferentes; por isso as codificações estão versionadas.

**Apoio:** slide 10 · A10 (slide 36)

### 3.11 ⚠️ Que diretriz metodológica orientou a revisão?

> [!tip]- Pontos-chave
> **Resposta direta:** O protocolo segue as etapas usuais de estudos secundários em engenharia de software: planejamento, busca, triagem, elegibilidade, extração e síntese.
>
> > [!warning] Preparar
> > Petersen, Vakkalanka e Kuzniarz (2015) está nas referências, mas não é citado no texto; cite-o na Seção 3.1 (ou retire-o) e saiba dizer o que adotou dele.

**Apoio:** slide 10 · A23 (slide 49) (referência)

## 4. Modelos e paradigmas gerativos

### 4.1 Por que esses três modelos?

> [!tip]- Pontos-chave
> **Resposta direta:** Representam três paradigmas gerativos — autoregressivo *decoder-only*, *encoder-decoder* e difusão em blocos — em escala aproximada (~0,6B), com pesos públicos e execução local viável.

**Apoio:** slide 5 · A16 (slide 42)

### 4.2 Qual a diferença entre os três paradigmas?

> [!tip]- Pontos-chave
> **Resposta direta:** *Decoder-only*: gera *token* a *token*, da esquerda para a direita (Qwen3). *Encoder-decoder*: um codificador bidirecional lê toda a entrada e o decodificador gera a saída (T5Gemma, adaptado de *decoder-only*). Difusão em blocos: blocos gerados em sequência, com remoção de ruído paralela dos *tokens* mascarados dentro de cada bloco (BD3LM).
>
> - Yang et al. (2025); Zhang et al. (2025); Nie et al. (2024); Arriola et al. (2025).

**Apoio:** slide 5

### 4.3 As diferenças poderão ser atribuídas ao paradigma gerativo?

> [!tip]- Pontos-chave
> **Resposta direta:** Não de forma causal isolada: os modelos diferem também em corpus de pré-treinamento, tokenizador e pós-treinamento. Compara-se o desempenho efetivo de representantes.
>
> - Mitigação: *zero-shot*, *prompt-only*, precisão numérica padronizada e sem decodificação restrita.

**Apoio:** slide 21 · A16 (slide 42)

### 4.4 ⚠️ Por que 0,6B, e não 1B a 4B?

> [!tip]- Pontos-chave
> **Resposta direta:** É a escala em que os três paradigmas têm representantes públicos comparáveis e que roda no *hardware* local.
>
> > [!warning] Preparar
> > O artigo justifica pela escala comum e pela execução local, mas não discute escalas maiores; tenha o argumento pronto (disponibilidade de representantes e memória da GPU).

**Apoio:** A16 (slide 42) · slide 14

### 4.5 ⚠️ De onde vem o Qwen3-0.6B BD3LM?

> [!tip]- Pontos-chave
> **Resposta direta:** É o representante de difusão em blocos; o nome indica derivação do Qwen3-0.6B, adaptando pesos autoregressivos para difusão (Gong et al., 2024; Arriola et al., 2025).
>
> > [!warning] Preparar
> > Diferentemente do Qwen3 e do T5Gemma, o artigo não traz nota de rodapé com o *checkpoint* do BD3LM; tenha em mãos o identificador exato, quem o publicou, a licença e a confirmação de que deriva do Qwen3-0.6B.

**Apoio:** A16 (slide 42) · slide 5

### 4.6 ⚠️ O T5Gemma B-B tem mesmo ~0,6B? Por que a variante PrefixLM-IT?

> [!tip]- Pontos-chave
> **Resposta direta:** O artigo o coloca na faixa de 0,6B (codificador e decodificador de tamanho *base*); a variante IT é ajustada por instruções, necessária para seguir o *prompt* *zero-shot* como os demais.
>
> > [!warning] Preparar
> > Confira no *model card* (google/t5gemma-b-b-prefixlm-it) o número exato de parâmetros e o que significa o objetivo de adaptação PrefixLM.

**Apoio:** A16 (slide 42)

### 4.7 Por que desativar o modo *thinking* do Qwen3?

> [!tip]- Pontos-chave
> **Resposta direta:** Para que o orçamento de 1.200 *tokens* seja consumido só pelo objeto JSON.

**Apoio:** A16 (slide 42) · slide 14

### 4.8 Por que não usar decodificação restrita por gramática?

> [!tip]- Pontos-chave
> **Resposta direta:** Para observar a capacidade intrínseca de cada modelo: os motores de decodificação restrita atuam de modo distinto sobre a geração sequencial e sobre o refinamento por difusão, o que confundiria a comparação.
>
> - Geng et al. (2023; 2025); Mündler; Dekoninck; Vechev (2025); Khanal et al. (2026).

**Apoio:** slide 5 · slide 11

### 4.9 Por que não fazer ajuste fino (*fine-tuning*)?

> [!tip]- Pontos-chave
> **Resposta direta:** O desenho é *zero-shot* e *prompt-only* para comparar os representantes sem introduzir variáveis de treinamento; vários estudos do núcleo treinam gestores (GRPO, LoRA, SFT), mas aqui se mede o comportamento instrucional.

**Apoio:** slide 11 · A1 (slide 27)

### 4.10 ⚠️ Os modelos cabem na GTX 1650?

> [!tip]- Pontos-chave
> **Resposta direta:** A Fase 0 valida o carregamento dos três escritores e do juiz; a precisão numérica (FP16 ou BF16) será uniforme entre os modelos.
>
> > [!warning] Preparar
> > A GTX 1650 tem 4 GB de VRAM e não tem suporte nativo a BF16 (arquitetura Turing); na prática a precisão uniforme tende a ser FP16 ou FP32. Tenha um plano B (por exemplo, CPU com os 24 GB de RAM) e meça o uso de memória.

**Apoio:** slide 14 · slide 16

## 5. GU-JSON, esquema e prompt

### 5.1 O que é o GU-JSON e por que ele, e não o CoK-JSON ou o GO/GM?

> [!tip]- Pontos-chave
> **Resposta direta:** *Generate-Update* em JSON: o escritor recebe o esquema, o estado anterior e a nova observação e regenera o JSON completo, $M_t = G(S, M_{t-1}, O_t)$. Toda a manutenção do estado fica em uma única chamada, sem algoritmos auxiliares de mesclagem.
>
> - Sob limite de *tokens*, o GU-JSON superou o GU-Text (Hwang et al., 2024).
> - O CoK-JSON seleciona chaves antes de atualizar, o que acrescenta uma etapa auxiliar e dilui o efeito do escritor.

**Apoio:** slide 3 · A4 (slide 30)

### 5.2 Por que reescrever o objeto inteiro em vez de aplicar operações parciais?

> [!tip]- Pontos-chave
> **Resposta direta:** A reescrita integral exige que o próprio modelo preserve, integre e mantenha a sintaxe ao mesmo tempo, e é exatamente essa capacidade que se quer medir. Operações aplicadas por código, como no PRISM (Jayalath et al., 2025), transferem parte do trabalho a um controlador externo.
>
> **Limite:** O trabalho não compara GU-JSON com operações parciais.

**Apoio:** slide 3 · A4 (slide 30)

### 5.3 Por que um esquema plano e mínimo?

> [!tip]- Pontos-chave
> **Resposta direta:** `{"state": {"chave": "valor"}}` é idêntico para todos os escritores e instâncias e isola a reescrita do estado.
>
> **Limite:** A validade externa fica restrita a esquemas planos de pares chave-valor.

**Apoio:** A14 (slide 40) · slide 21

### 5.4 Por que o *prompt* está em inglês?

> [!tip]- Pontos-chave
> **Resposta direta:** É o idioma nativo do SUMIE e dos modelos avaliados; o texto é idêntico para os três escritores.

**Apoio:** A14 (slide 40)

### 5.5 Quais são as seis regras do *prompt-base*?

> [!tip]- Pontos-chave
> **Resposta direta:** Preservar o que continua válido; aplicar o que a observação introduz explicitamente; substituir só quando a observação estabelecer invalidade, mantendo perspectivas divergentes; não inventar fatos; respeitar o esquema; retornar só o JSON completo.

**Apoio:** A14 (slide 40)

### 5.6 Por que limitar a saída a 1.200 *tokens*?

> [!tip]- Pontos-chave
> **Resposta direta:** Para seguir o regime de memória limitada de Hwang et al. (2024), com orçamento fixo para todos os escritores.
>
> - O piloto verifica se os estados esperados $M^*_t$ cabem inteiros no orçamento; assim, omissões são atribuídas ao escritor, e não a truncamento.

**Apoio:** slide 11 · slide 12

### 5.7 ⚠️ E se algum estado esperado passar de 1.200 *tokens*?

> [!tip]- Pontos-chave
> **Resposta direta:** O protocolo exige que os estados esperados caibam inteiros no orçamento, e o piloto (Fase 1) verifica isso antes de fixar as regras.
>
> > [!warning] Preparar
> > O artigo não diz o que fazer com transições acima do limite; decida (por exemplo, excluí-las e reportá-las à parte) e leve a decisão pronta.

**Apoio:** slide 12 · slide 16

### 5.8 ⚠️ O orçamento de 1.200 *tokens* é justo entre tokenizadores diferentes?

> [!tip]- Pontos-chave
> **Resposta direta:** O limite vale na contagem de cada modelo; as diferenças de tokenizador são admitidas como parte do desempenho de cada representante.
>
> > [!warning] Preparar
> > O mesmo JSON pode ocupar números diferentes de *tokens* no Qwen3 e no T5Gemma; proponha medir no piloto o comprimento de $M^*_t$ com cada tokenizador.

**Apoio:** slide 14 · A15 (slide 41)

### 5.9 Como se evita que a resposta esperada vaze para o escritor?

> [!tip]- Pontos-chave
> **Resposta direta:** Só o esquema, $M^*_{t-1}$ e $O_t$ entram no *prompt*; $M^*_t$, as anotações e os rótulos seguem por um caminho separado, usado apenas na avaliação.

**Apoio:** slide 14 · slide 13

### 5.10 Por que a entrada é o estado de referência, e não a saída do escritor no turno anterior?

> [!tip]- Pontos-chave
> **Resposta direta:** Para avaliar cada transição isoladamente: os erros de uma transição não se propagam para a seguinte.
>
> **Limite:** Não mede o acúmulo de erros que ocorreria em uso real.

**Apoio:** slide 12 · slide 21

## 6. SUMIE e preparação dos dados

### 6.1 O que é o SUMIE?

> [!tip]- Pontos-chave
> **Resposta direta:** *Benchmark* de sumarização incremental de entidades (Hwang et al., 2025): sequências de parágrafos com fatos novos, repetições, distratores e pontos de vista divergentes; cada parágrafo tem anotações de atributos e valores. Licença Apache-2.0.

**Apoio:** slide 12

### 6.2 Por que o SUMIE, e não LongMemEval, LoCoMo ou MemoryAgentBench?

> [!tip]- Pontos-chave
> **Resposta direta:** Esses *benchmarks* avaliam a memória pela resposta a perguntas no fim da sequência; o SUMIE anota atributos e valores por parágrafo, o que permite inspecionar o estado em cada transição.
>
> - Hu; Wang; McAuley (2025); Wu et al. (2024); Maharana et al. (2024).

**Apoio:** A4 (slide 30) · slide 12

### 6.3 O que é a política de acumulação do SUMIE?

> [!tip]- Pontos-chave
> **Resposta direta:** Perspectivas distintas sobre um atributo são integradas: uma nova opinião não invalida automaticamente a anterior.
>
> - Está na regra 3 do *prompt*, na definição de UPDATE e no critério do juiz, que só aceita equivalências compatíveis com essa política.

**Apoio:** slide 12 · A14 (slide 40)

### 6.4 Como as transições são construídas?

> [!tip]- Pontos-chave
> **Resposta direta:** Cada etapa $t$ vira a tupla $(M^*_{t-1}, O_t, M^*_t)$: o estado acumulado de referência até $t-1$, o parágrafo do turno $t$ e o estado esperado depois de incorporá-lo.

**Apoio:** slide 12

### 6.5 Como são definidos PRESERVE, ADD e UPDATE?

> [!tip]- Pontos-chave
> **Resposta direta:** Por comparação determinística entre $M^*_{t-1}$ e $M^*_t$, atributo a atributo: PRESERVE já existia e não muda; ADD aparece pela primeira vez em $O_t$; UPDATE já existia e recebe complemento ou nova perspectiva.

**Apoio:** slide 12 · A19 (slide 45)

### 6.6 ⚠️ Quantas entidades e transições serão avaliadas?

> [!tip]- Pontos-chave
> **Resposta direta:** Na Fase 2, toda a partição de avaliação do SUMIE; antes disso, 25 entidades separadas no piloto e 15 transições sintéticas na Fase 0.
>
> > [!warning] Preparar
> > O artigo não informa o tamanho da partição de avaliação; levante o número de entidades e de transições no repositório do SUMIE.

**Apoio:** slide 16 · slide 12

### 6.7 Os dados sintéticos não limitam as conclusões?

> [!tip]- Pontos-chave
> **Resposta direta:** Limitam o alcance: os resultados valem para sumarização incremental de entidades. Em troca, os dados são públicos, sem dados pessoais, e as entidades são mascaradas (por exemplo, ENTITY0).
>
> **Limite:** Validade externa: esquema plano e transições com estado de referência.

**Apoio:** slide 13 · slide 21

### 6.8 Como funciona a normalização textual?

> [!tip]- Pontos-chave
> **Resposta direta:** Espaços, caixa e pontuação são normalizados antes da correspondência direta; as regras são fixadas no piloto (Fase 1).

**Apoio:** slide 15 · slide 16

## 7. Métricas e juiz semântico

### 7.1 Quais métricas são primárias e por quê?

> [!tip]- Pontos-chave
> **Resposta direta:** State F1, Preservation Accuracy e Update Accuracy (agregada e separada em ADD e UPDATE): são as métricas das hipóteses. As estruturais e a taxa de alucinação completam o diagnóstico.

**Apoio:** slide 15 · A18 (slide 44) · slide 11

### 7.2 Qual a diferença entre JSON Validity e Schema Validity?

> [!tip]- Pontos-chave
> **Resposta direta:** JSON Validity: a saída bruta é lida por `json.loads` sem reparo. Schema Validity: a saída contém exclusivamente o objeto raiz `state`, que mapeia chaves textuais a valores.

**Apoio:** A18 (slide 44) · slide 15

### 7.3 Como se calculam a precisão, a revocação e o F1 do estado?

> [!tip]- Pontos-chave
> **Resposta direta:** O JSON vira pares caminho-valor (`state.<atributo>`, valor normalizado), sem ordem de chaves. TP: pares correspondentes diretamente ou aceitos pelo juiz; FP: pares gerados não correspondentes ou não sustentados; FN: fatos esperados ausentes. $P = TP/(TP+FP)$, $R = TP/(TP+FN)$, $F_1 = 2PR/(P+R)$.
>
> - As correspondências são um-para-um.

**Apoio:** A19 (slide 45) · slide 15

### 7.4 ⚠️ Qual a diferença entre falso positivo e alucinação?

> [!tip]- Pontos-chave
> **Resposta direta:** Alucinação é o par gerado sem correspondência esperada e sem suporte nas anotações, em $M^*_{t-1}$ ou em $O_t$; FP inclui todo par gerado não correspondente ou não sustentado.
>
> > [!warning] Preparar
> > O artigo não explicita a relação; leia-a como "alucinação ⊆ FP": um FP com apoio na entrada (por exemplo, um detalhe não anotado) não é alucinação.

**Apoio:** A18 (slide 44) · A19 (slide 45)

### 7.5 O que são as visões condicional e global?

> [!tip]- Pontos-chave
> **Resposta direta:** Condicional: só as transições com JSON válido e aderente ao esquema, isolando a qualidade do conteúdo. Global (*end-to-end*): falhas estruturais recebem zero, refletindo a confiabilidade efetiva do escritor.

**Apoio:** slide 15

### 7.6 O que são os resultados estritos e os híbridos?

> [!tip]- Pontos-chave
> **Resposta direta:** Estritos: só correspondência direta após normalização. Híbridos: incluem as equivalências aceitas pelo juiz. Os dois são reportados; as métricas primárias usam o híbrido.

**Apoio:** slide 15 · A17 (slide 43)

### 7.7 Por que usar um modelo de linguagem como juiz?

> [!tip]- Pontos-chave
> **Resposta direta:** A avaliação original do SUMIE já usa um juiz para o alinhamento semântico; aqui ele só é chamado para as divergências que a correspondência direta não resolve.
>
> - Recebe $M^*_{t-1}$, $O_t$, $M^*_t$, as anotações e o estado gerado; decide entre equivalente, ausente/contradito ou incerto.
> - Não pode inferir suporte por plausibilidade geral.

**Apoio:** A17 (slide 43) · slide 15

### 7.8 Como se controla o viés do juiz?

> [!tip]- Pontos-chave
> **Resposta direta:** Versão, quantização e *prompt* congelados antes da Fase 2; julgamento cego à identidade do escritor; incertos reportados à parte, sem contar como acerto; amostra auditada manualmente; resultados estritos e proporção enviada ao juiz divulgados.

**Apoio:** A17 (slide 43) · slide 21

### 7.9 ⚠️ O juiz Gemma 3 1B não favorece o T5Gemma, da mesma família?

> [!tip]- Pontos-chave
> **Resposta direta:** O juiz é independente dos três escritores e não sabe qual deles gerou a saída; os resultados estritos permitem verificar se o juiz muda a ordem dos escritores.
>
> > [!warning] Preparar
> > O T5Gemma é adaptado de modelos Gemma e o artigo não discute esse risco de afinidade; prepare a resposta e proponha comparar estrito × híbrido por escritor.

**Apoio:** A17 (slide 43) · A16 (slide 42)

### 7.10 ⚠️ Um juiz de 1B quantizado em Q4_K_M é confiável?

> [!tip]- Pontos-chave
> **Resposta direta:** Foi escolhido por ser aberto, local e caber no limite de 4 GiB de memória residente; ele só decide divergências e é verificado no piloto por auditoria manual.
>
> > [!warning] Preparar
> > Q4_K_M é uma quantização GGUF de cerca de 4 bits por peso; o artigo não define o tamanho da amostra auditada nem o critério de aceite. Defina-os.

**Apoio:** A17 (slide 43) · slide 16

### 7.11 Como se calculam a Preservation Accuracy e a Update Accuracy?

> [!tip]- Pontos-chave
> **Resposta direta:** PA: atributos PRESERVE mantidos corretamente sobre o total de PRESERVE esperados. UA: atributos ADD ou UPDATE registrados corretamente sobre o total esperado, também separada por operação.
>
> - Correto = correspondência direta ou equivalência confirmada pelo juiz; incertos ficam à parte.

**Apoio:** A19 (slide 45)

## 8. Hipóteses e análise estatística

### 8.1 Quais são as hipóteses?

> [!tip]- Pontos-chave
> **Resposta direta:** H0: não há diferença estatisticamente significativa nas métricas primárias (State F1, Preservation Accuracy e Update Accuracy) entre os três escritores. H1: há diferenças significativas na preservação do estado e na incorporação de novas informações, refletindo perfis de erro distintos.

**Apoio:** slide 11 · A20 (slide 46)

### 8.2 Você espera que algum paradigma vença?

> [!tip]- Pontos-chave
> **Resposta direta:** Não há hipótese direcional: H1 afirma que há diferença, não qual escritor é melhor. O desenho permite verificar se a codificação bidirecional ou a difusão em blocos são mais ou menos estáveis que a geração autoregressiva.

**Apoio:** slide 20 · slide 11

### 8.3 Por que Friedman e Wilcoxon, e não ANOVA ou teste t?

> [!tip]- Pontos-chave
> **Resposta direta:** São testes não paramétricos pareados: os três escritores são avaliados nas mesmas unidades e não se supõe normalidade. Friedman compara os três pelos postos médios; Wilcoxon pareado compara dois a dois (Demšar, 2006).
>
> - Wilcoxon interpretado como diferença de localização pressupõe diferenças aproximadamente simétricas.

**Apoio:** A20 (slide 46)

### 8.4 Por que a correção de Holm-Bonferroni?

> [!tip]- Pontos-chave
> **Resposta direta:** São três comparações dois a dois por métrica; Holm ordena os valores p e os compara com limites ajustados, controlando a probabilidade de pelo menos uma rejeição indevida (Holm, 1979), com menos perda de poder que o Bonferroni simples.
>
> - α = 0,05.

**Apoio:** A20 (slide 46)

### 8.5 ⚠️ Qual é a unidade de análise?

> [!tip]- Pontos-chave
> **Resposta direta:** A entidade: as diferenças pareadas são calculadas no nível de entidade, porque as transições de uma mesma entidade não são independentes e os testes exigem unidades independentes.
>
> > [!warning] Preparar
> > O artigo não diz como a métrica por entidade é agregada (média das transições ou contagem conjunta dos pares); defina isso e leve pronto.

**Apoio:** A20 (slide 46)

### 8.6 ⚠️ E se o teste de Friedman não for significativo?

> [!tip]- Pontos-chave
> **Resposta direta:** H0 não é rejeitada para aquela métrica; os resultados descritivos (média, mediana, curvas por turno e perfil por operação) continuam informativos.
>
> > [!warning] Preparar
> > O artigo não diz se os Wilcoxon serão feitos mesmo sem rejeição global; seguindo Demšar (2006), o *post-hoc* vem depois da rejeição no Friedman. Deixe isso explícito.

**Apoio:** A20 (slide 46)

### 8.7 ⚠️ Você vai reportar tamanho de efeito ou intervalo de confiança?

> [!tip]- Pontos-chave
> **Resposta direta:** O plano prevê média, mediana, testes pareados e curvas por turno.
>
> > [!warning] Preparar
> > A sigla IC (Intervalo de Confiança) está na lista de siglas, mas não é usada no texto; retire a sigla ou inclua IC (por exemplo, *bootstrap* por entidade) e um tamanho de efeito no plano de análise.

**Apoio:** A20 (slide 46)

### 8.8 ⚠️ Uma única execução é suficiente?

> [!tip]- Pontos-chave
> **Resposta direta:** A decodificação é determinística (sem amostragem e com semente fixa), então repetir a execução daria a mesma saída; a variabilidade analisada vem das entidades.
>
> > [!warning] Preparar
> > Pequenas diferenças numéricas de *hardware* ou de precisão podem alterar saídas; garanta que versões, *hashes* e configuração fiquem no manifesto.

**Apoio:** slide 14 · A20 (slide 46)

### 8.9 Como será a análise longitudinal?

> [!tip]- Pontos-chave
> **Resposta direta:** Curvas de State F1, Preservation Accuracy e JSON Validity em função do índice do turno $t$, para ver como a qualidade se degrada à medida que o estado cresce e se aproxima dos 1.200 *tokens*.

**Apoio:** A20 (slide 46) · slide 20

## 9. Limitações, ética e reprodutibilidade

### 9.1 Quais são as principais ameaças à validade?

> [!tip]- Pontos-chave
> **Resposta direta:** Interna: os modelos diferem além da arquitetura. De construção: possível viés do juiz. Externa: sumarização de entidades, esquema plano e transições com estado de referência, sem medir o impacto nas tarefas do agente.

**Apoio:** slide 21

### 9.2 Há questões éticas envolvidas?

> [!tip]- Pontos-chave
> **Resposta direta:** Não há participantes humanos nem coleta de dados pessoais: os dados são sintéticos e públicos (SUMIE, Apache-2.0) e os modelos têm pesos abertos (Qwen3 sob Apache-2.0; juiz sob a licença Gemma).

**Apoio:** slide 14 · slide 12

### 9.3 Como se garante a reprodutibilidade do experimento?

> [!tip]- Pontos-chave
> **Resposta direta:** Manifesto com os *commit hashes* dos pesos e a configuração de inferência; decodificação determinística; saídas brutas gravadas antes de qualquer validação e sem reparo; registros JSON com proveniência; versão, *hash* e contexto do juiz registrados.

**Apoio:** slide 14 · A15 (slide 41)

### 9.4 Por que não reparar o JSON inválido?

> [!tip]- Pontos-chave
> **Resposta direta:** Porque o reparo esconderia justamente a falha que o Objetivo a mede; a saída original é preservada e, na visão global, a falha estrutural recebe zero.

**Apoio:** slide 14 · slide 15

### 9.5 Quais são as nove etapas do *harness*?

> [!tip]- Pontos-chave
> **Resposta direta:** (i) ler a transição; (ii) montar o *prompt*; (iii) invocar o adaptador com limite de 1.200 *tokens*; (iv) gravar a saída bruta; (v) validar a sintaxe; (vi) validar o esquema; (vii) correspondência direta; (viii) juiz só para divergências; (ix) registrar.

**Apoio:** slide 14 · A15 (slide 41)

### 9.6 O que o adaptador de cada modelo pode mudar?

> [!tip]- Pontos-chave
> **Resposta direta:** Só o que é específico do modelo: o *template* de conversa e os *tokens* especiais, sem alterar o *prompt-base*. A decodificação também é fixada: *thinking* desativado no Qwen3 e, no BD3LM, tamanho de bloco, passos de remoção de ruído e critério de desmascaramento.

**Apoio:** slide 13 · slide 14

### 9.7 ⚠️ O que fica como trabalho futuro?

> [!tip]- Pontos-chave
> **Resposta direta:** Extensões que o recorte exclui: propagar a saída do escritor entre turnos, esquemas aninhados, decodificação restrita, outras escalas e o impacto do *checkpoint* nas tarefas do agente.
>
> > [!warning] Preparar
> > O artigo não tem seção de trabalhos futuros; essas extensões derivam das limitações (Seções 2.5 e 3.11). Apresente-as como possibilidades, não como compromisso.

**Apoio:** slide 21 · slide 23

## 10. Resultados esperados e cronograma

### 10.1 Que resultados o trabalho vai entregar?

> [!tip]- Pontos-chave
> **Resposta direta:** Quatro conjuntos de evidências — robustez estrutural com categorias de falha; fidelidade global e longitudinal; perfil de erro por operação; relação entre validade sintática e fidelidade semântica — além de um protocolo e um *harness* reutilizáveis.

**Apoio:** slide 20

### 10.2 O que seria um escritor "conservador" e um que sobrescreve?

> [!tip]- Pontos-chave
> **Resposta direta:** Conservador: preserva bem o estado anterior (PA alta), mas falha em incorporar novos atributos (UA baixa). O outro integra a informação nova, mas esquece ou sobrescreve campos válidos (PA baixa).

**Apoio:** slide 20 · A19 (slide 45)

### 10.3 ⚠️ E se nenhum modelo gerar JSON válido com frequência?

> [!tip]- Pontos-chave
> **Resposta direta:** Isso já é resultado do Objetivo a: a visão global atribui zero e a classificação das falhas (truncamento, chaves malformadas, texto fora do objeto) caracteriza os modos de falha de cada escritor.
>
> > [!warning] Preparar
> > A visão condicional pode ficar com poucas transições; diga como reportará (por exemplo, o número de transições válidas por escritor).

**Apoio:** slide 20 · slide 15

### 10.4 Quais são as fases do experimento?

> [!tip]- Pontos-chave
> **Resposta direta:** Fase 0: 15 transições sintéticas, verificação funcional e pico de memória do juiz até 4 GiB. Fase 1: piloto em 25 entidades separadas, para normalização, comprimento em *tokens*, ausência de truncamento, auditoria e congelamento do juiz. Fase 2: os três escritores em toda a partição de avaliação.

**Apoio:** slide 16

### 10.5 Como está organizado o cronograma?

> [!tip]- Pontos-chave
> **Resposta direta:** São 15 atividades em 20 quinzenas. TCC I (ago.–dez./2026, Q1–Q10): tema, revisão, protocolo, verificação dos modelos, texto e apresentação. TCC II (fev.–jun./2027, Q11–Q20): preparação do SUMIE, *harness*, Fases 0 a 2, estatística, redação e defesa.

**Apoio:** slide 22 · A21 (slide 47)

### 10.6 ⚠️ Quais são os riscos do cronograma e o plano B?

> [!tip]- Pontos-chave
> **Resposta direta:** A Fase 0 detecta cedo problemas de carregamento e memória, e a Fase 1 fixa as regras antes do experimento principal.
>
> > [!warning] Preparar
> > O artigo não lista riscos nem contingências; prepare dois ou três (modelo que não cabe na GPU, tempo de inferência do BD3LM, juiz reprovado na auditoria).

**Apoio:** slide 22 · slide 16

### 10.7 Como os objetivos se ligam às evidências?

> [!tip]- Pontos-chave
> **Resposta direta:** Pelos Quadros 6 a 8: a) analisador e validador → JSON e Schema Validity; b) estados de referência, correspondência e juiz → precisão, revocação, F1 e alucinação; c) rotulador de operações → PA e UA; todos com comparações pareadas.

**Apoio:** slide 17 · slide 18 · slide 19

## Números para ter na ponta da língua

| Tema | Valor |
| --- | --- |
| Escritores | 3 representantes de ~0,6B: Qwen3-0.6B, T5Gemma B-B PrefixLM-IT e Qwen3-0.6B BD3LM |
| Juiz | Gemma 3 1B Instruct, GGUF Q4_K_M, local, pico de memória residente ≤ 4 GiB |
| Orçamentos | saída ≤ 1.200 *tokens* por transição; contexto de entrada ≤ 8.192 *tokens* |
| Protocolo | 6 regras no *prompt-base*; 9 etapas no *harness*; 3 métricas primárias; α = 0,05 |
| Fases | Fase 0: 15 transições sintéticas; Fase 1: 25 entidades; Fase 2: partição de avaliação completa |
| Busca | arXiv (título e resumo), 01/07/2025 a 19/11/2026; 8 consultas (905 registros somados); 12 estudos de controle |
| Funil | 738 únicos → 696 após termos → 189 na elegibilidade → 12 no núcleo |
| Triagem | claude-haiku-5.5 via GitHub Copilot SDK 1.0.31; lotes de 20; 36 requisições, 38 créditos (teto 150) |
| Elegibilidade | 189 requisições, ~191 créditos (teto 400); 185 HTML + 4 PDF; até 100 mil caracteres; trechos de 20 a 400 caracteres; corte de 4,5B |
| Artefatos | repositório público da revisão v2.1.0; *scripts* em C# (.NET 10); *hashes* SHA-256 |
| *Hardware* | Intel Core i5 de 10ª geração, 24 GB de RAM, NVIDIA GeForce GTX 1650 |
| Cronograma | 15 atividades em 20 quinzenas: TCC I Q1–Q10 (ago.–dez./2026); TCC II Q11–Q20 (fev.–jun./2027) |

## Definições rápidas

| Termo | Definição |
| --- | --- |
| *Checkpoint* JSON | estado persistente da entidade, `{"state": {"chave": "valor"}}`, regenerado a cada turno |
| GU-JSON | *Generate-Update* em JSON: $M_t = G(S, M_{t-1}, O_t)$, com reescrita integral |
| Escritor de memória | modelo $G$ que produz o novo *checkpoint* (*memory writer*) |
| $M^*_{t-1}$, $O_t$, $M^*_t$ | estado de referência anterior, parágrafo do turno e estado esperado |
| PRESERVE / ADD / UPDATE | manter atributo inalterado / incluir atributo novo / integrar complemento ou nova perspectiva |
| JSON Validity / Schema Validity | saída lida por `json.loads` sem reparo / só o objeto raiz `state` com chaves e valores textuais |
| State P, R e F1 | precisão, revocação e média harmônica sobre pares caminho-valor |
| Hallucination Rate | pares gerados sem correspondência esperada e sem suporte na entrada ou nas anotações |
| PA / UA | acurácia de preservação (PRESERVE) / de atualização (ADD e UPDATE) |
| Condicional / global | só transições válidas / falha estrutural conta como zero |
| Estrito / híbrido | só correspondência normalizada / inclui equivalências aceitas pelo juiz |
| *Zero-shot*, *prompt-only* | sem exemplos no *prompt* e sem decodificação restrita |
| Decodificação restrita | filtra *tokens* inválidos por gramática durante a geração |
| BD3LM | difusão em blocos: blocos em sequência, remoção de ruído paralela dentro do bloco |
| GGUF / Q4_K_M | formato de pesos para execução local / quantização de ~4 bits por peso |
| Friedman | compara 3+ modelos nas mesmas unidades pelos postos médios |
| Wilcoxon pareado | compara 2 modelos pelos postos das diferenças pareadas |
| Holm-Bonferroni | ajuste sequencial dos valores p para comparações múltiplas |

## ⚠️ Pontos a preparar ou corrigir antes da banca

- **1.6** Qual é a relação do trabalho com Sistemas de Informação? — O artigo não explicita esse vínculo; prepare 2 ou 3 frases próprias ligando o trabalho a disciplinas do curso.
- **3.2** Por que buscar só no arXiv? — O artigo declara a limitação, mas não justifica a escolha; prepare o argumento e diga se pretende ampliar as fontes no TCC II.
- **3.3** Por que a janela de 1º/07/2025 a 19/11/2026? — O artigo não justifica o início em julho de 2025; tenha essa justificativa pronta.
- **3.6** Por que o núcleo não exige C7? — O artigo não explica isso no texto; a resposta é uma inferência sua, então formule-a com segurança.
- **3.7** Por que o limite de ~4 bilhões de parâmetros? — O artigo não justifica o corte em 4B; argumento possível: é a faixa em que a literatura já usa gestores compactos e que ainda roda localmente.
- **3.11** Que diretriz metodológica orientou a revisão? — Petersen, Vakkalanka e Kuzniarz (2015) está nas referências, mas não é citado no texto; cite-o na Seção 3.1 (ou retire-o) e saiba dizer o que adotou dele.
- **4.4** Por que 0,6B, e não 1B a 4B? — O artigo justifica pela escala comum e pela execução local, mas não discute escalas maiores; tenha o argumento pronto (disponibilidade de representantes e memória da GPU).
- **4.5** De onde vem o Qwen3-0.6B BD3LM? — Diferentemente do Qwen3 e do T5Gemma, o artigo não traz nota de rodapé com o *checkpoint* do BD3LM; tenha em mãos o identificador exato, quem o publicou, a licença e a confirmação de que deriva do Qwen3-0.6B.
- **4.6** O T5Gemma B-B tem mesmo ~0,6B? Por que a variante PrefixLM-IT? — Confira no *model card* (google/t5gemma-b-b-prefixlm-it) o número exato de parâmetros e o que significa o objetivo de adaptação PrefixLM.
- **4.10** Os modelos cabem na GTX 1650? — A GTX 1650 tem 4 GB de VRAM e não tem suporte nativo a BF16 (arquitetura Turing); na prática a precisão uniforme tende a ser FP16 ou FP32. Tenha um plano B (por exemplo, CPU com os 24 GB de RAM) e meça o uso de memória.
- **5.7** E se algum estado esperado passar de 1.200 *tokens*? — O artigo não diz o que fazer com transições acima do limite; decida (por exemplo, excluí-las e reportá-las à parte) e leve a decisão pronta.
- **5.8** O orçamento de 1.200 *tokens* é justo entre tokenizadores diferentes? — O mesmo JSON pode ocupar números diferentes de *tokens* no Qwen3 e no T5Gemma; proponha medir no piloto o comprimento de $M^*_t$ com cada tokenizador.
- **6.6** Quantas entidades e transições serão avaliadas? — O artigo não informa o tamanho da partição de avaliação; levante o número de entidades e de transições no repositório do SUMIE.
- **7.4** Qual a diferença entre falso positivo e alucinação? — O artigo não explicita a relação; leia-a como "alucinação ⊆ FP": um FP com apoio na entrada (por exemplo, um detalhe não anotado) não é alucinação.
- **7.9** O juiz Gemma 3 1B não favorece o T5Gemma, da mesma família? — O T5Gemma é adaptado de modelos Gemma e o artigo não discute esse risco de afinidade; prepare a resposta e proponha comparar estrito × híbrido por escritor.
- **7.10** Um juiz de 1B quantizado em Q4_K_M é confiável? — Q4_K_M é uma quantização GGUF de cerca de 4 bits por peso; o artigo não define o tamanho da amostra auditada nem o critério de aceite. Defina-os.
- **8.5** Qual é a unidade de análise? — O artigo não diz como a métrica por entidade é agregada (média das transições ou contagem conjunta dos pares); defina isso e leve pronto.
- **8.6** E se o teste de Friedman não for significativo? — O artigo não diz se os Wilcoxon serão feitos mesmo sem rejeição global; seguindo Demšar (2006), o *post-hoc* vem depois da rejeição no Friedman. Deixe isso explícito.
- **8.7** Você vai reportar tamanho de efeito ou intervalo de confiança? — A sigla IC (Intervalo de Confiança) está na lista de siglas, mas não é usada no texto; retire a sigla ou inclua IC (por exemplo, *bootstrap* por entidade) e um tamanho de efeito no plano de análise.
- **8.8** Uma única execução é suficiente? — Pequenas diferenças numéricas de *hardware* ou de precisão podem alterar saídas; garanta que versões, *hashes* e configuração fiquem no manifesto.
- **9.7** O que fica como trabalho futuro? — O artigo não tem seção de trabalhos futuros; essas extensões derivam das limitações (Seções 2.5 e 3.11). Apresente-as como possibilidades, não como compromisso.
- **10.3** E se nenhum modelo gerar JSON válido com frequência? — A visão condicional pode ficar com poucas transições; diga como reportará (por exemplo, o número de transições válidas por escritor).
- **10.6** Quais são os riscos do cronograma e o plano B? — O artigo não lista riscos nem contingências; prepare dois ou três (modelo que não cabe na GPU, tempo de inferência do BD3LM, juiz reprovado na auditoria).
