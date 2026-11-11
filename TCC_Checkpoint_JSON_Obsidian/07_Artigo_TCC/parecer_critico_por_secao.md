# Parecer crítico de orientação — por seção

**Base da leitura:** versão mais recente do artigo, `artigo_tcc_unitins_atualizado.docx`, e as mensagens recebidas sobre falta do projeto e de diagramas. Este é um parecer simulado, deliberadamente exigente; não representa uma avaliação oficial do orientador.

## Síntese do parecer

O tema e a pergunta de pesquisa são promissores, e o texto já apresenta uma proposta experimental relativamente detalhada. Ainda assim, na forma atual, o trabalho demonstra principalmente **planejamento**, não um projeto de software concluído nem resultados de pesquisa. O artigo descreve um *harness* em prosa e promete implementá-lo; não apresenta diagramas, repositório executável, teste piloto comprovado ou resultados. Para uma qualificação de projeto isso pode ser uma base; para defender o TCC final, é insuficiente.

A crítica “não tem projeto, não tem os diagramas” é procedente quanto ao artigo. Há quatro notas técnicas de apoio em `04_Implementacao`, mas estão em rascunho e não substituem artefatos implementados ou diagramas apresentados no trabalho. Também há questões científicas que precisam ser resolvidas antes da coleta: o checkpoint exato do modelo de difusão, a construção dos estados de referência e a validade da correspondência textual usada como métrica.

## Observações por seção

### Elementos pré-textuais

**Crítica:** resumo e abstract descrevem um experimento futuro. Isso é coerente com um projeto de TCC I, mas não com um artigo final que anuncie resultados. O título também precisa ser compatível com o estágio real do trabalho: proposta, protocolo ou estudo concluído.

**Perguntas:** O documento será entregue como projeto de TCC I ou como artigo final? Qual é a versão e a data oficial do título? A formatação e a paginação foram conferidas no DOCX final, e não apenas na extração Markdown?

**Ajuste exigido:** declarar claramente o estágio do trabalho e, depois da execução, substituir promessas por resultados observados. Conferir resumo, abstract, palavras-chave e listas de quadros/tabelas após a revisão final.

### 1. Introdução

**Crítica:** a motivação é clara, mas a lacuna depende da afirmação de que não foi identificada uma comparação controlada. A contribuição ainda pode soar como “comparar três modelos” sem explicar por que essa comparação é útil para um sistema de informação ou qual artefato concreto será entregue. Além disso, diferenças entre esses modelos não isolam o efeito causal da arquitetura: treinamento, dados, tokenizador e ajuste por instruções também variam.

**Perguntas:** Qual decisão prática o resultado permitirá tomar? O que será construído além do texto acadêmico? A pergunta compara paradigmas em geral ou somente três implementações específicas?

**Ajuste exigido:** apresentar como contribuição um protocolo reproduzível e um *harness* executável; formular a inferência como comparação entre os três modelos escolhidos, sem generalizar causalmente para todos os paradigmas.

### 2. Memória persistente em agentes

**Crítica geral:** a fundamentação cobre assuntos relevantes, mas predomina a descrição de trabalhos. É necessário fazer a literatura sustentar decisões do experimento, não apenas introduzir termos. A tabela comparativa ajuda, mas não substitui uma síntese crítica das limitações e do espaço exato que o estudo ocupa.

**Perguntas:** Que decisão metodológica cada trabalho relacionado justifica? Que evidência sustenta a escolha de GU-JSON, SUMIE e do schema plano?

#### 2.1 Representação estruturada da memória

**Crítica:** são citadas representações diversas, mas falta mostrar por que um objeto plano de pares chave-valor representa adequadamente as anotações do SUMIE. A representação pode comprimir ou combinar perspectivas e, assim, alterar o que será considerado correto.

**Ajuste exigido:** incluir um exemplo concreto de anotação do conjunto, estado anterior, observação e estado esperado; explicar como preservar perspectivas sem perder rastreabilidade para a fonte.

#### 2.2 Atualização incremental e GU-JSON

**Crítica:** o método está definido matematicamente, mas ainda não está materializado como fluxo observável. A equação não deixa claro o que entra e sai de cada chamada na implementação real.

**Perguntas:** Qual é exatamente o contrato do escritor? O modelo recebe o estado-ouro anterior em todos os turnos? Como a saída bruta e uma falha de parse são tratadas?

**Ajuste exigido:** incluir um diagrama de sequência de uma transição e um exemplo de entrada/saída. Distinguir explicitamente o experimento com estado-ouro do uso encadeado em que a saída do turno anterior alimenta o próximo.

#### 2.3 Avaliação de memória e atualização de conhecimento

**Crítica:** a política de acumulação do SUMIE é central e precisa permanecer inequívoca. Uma opinião divergente não é automaticamente uma atualização que apaga o valor anterior; regra de precedência temporal é outra tarefa.

**Ajuste exigido:** definir uma tabela de decisão para PRESERVE, ADD e UPDATE, com exemplos positivos e casos-limite. Se FactConsolidation-SH continuar como contraste opcional, não atribuir diferenças entre conjuntos à operação de atualização: conjunto e regra mudam ao mesmo tempo.

#### 2.4 Geração estruturada

**Crítica:** a justificativa para não usar decodificação restrita é válida para medir o regime *prompt-only*, mas o texto precisa explicar por que esse regime representa a condição de uso pretendida. Validade sintática e validade de schema são métricas diferentes e devem permanecer separadas.

**Ajuste exigido:** mostrar exemplos das categorias de falha e explicitar que uma saída estruturalmente válida ainda pode estar semanticamente errada.

#### 2.5 Paradigmas gerativos e modelos compactos

**Crítica:** a seção descreve as arquiteturas, mas a seleção dos modelos não permite atribuir as diferenças observadas exclusivamente a elas. A viabilidade local também é afirmada antes de comprovar que os três checkpoints rodam no hardware planejado.

**Perguntas:** Os três modelos cabem na memória disponível, com qual precisão e tempo por transição? Qual é o identificador exato do modelo BD3LM?

**Ajuste exigido:** fazer um teste técnico de carregamento e inferência nos três modelos antes de fechar o protocolo. Registrar repositório, revisão/hash, tokenizer, runtime, precisão e parâmetros de geração. O checkpoint exato de Qwen3 BD3LM ainda precisa ser confirmado.

#### 2.6 Trabalhos relacionados

**Crítica:** o quadro compara trabalhos, mas não evidencia o raciocínio que leva da literatura ao desenho proposto. A linha “este trabalho” resume a intenção, não uma contribuição já demonstrada.

**Ajuste exigido:** fechar a seção com uma síntese explícita: o que já foi testado, o que permanece em aberto, qual hipótese o estudo pode testar e quais conclusões ele não poderá sustentar.

### 3. Materiais e métodos

**Crítica geral:** é a seção mais detalhada, mas ainda descreve procedimentos futuros. Um método detalhado não prova que o sistema foi implementado, que os dados foram preparados ou que as métricas funcionam.

**Perguntas:** Onde estão o código, os testes, o manifesto dos modelos, uma amostra processada e a saída bruta de uma execução piloto?

#### 3.1 Desenho experimental e variáveis

**Crítica:** a variável independente é apresentada como modelo escritor, mas a pergunta e algumas justificativas falam em paradigmas. Essa diferença precisa ser consistente. Também faltam contagens que permitam avaliar o tamanho real do experimento e a unidade usada nos testes estatísticos.

**Ajuste exigido:** declarar entidade, transição e escritor como unidades de análise quando aplicável; informar número de entidades e transições por partição; esclarecer se os 300 tokens são somente saída e como é verificado o truncamento.

#### 3.2 Método, schema e prompt

**Crítica:** o schema `{ "state": { "chave": "valor" } }` é simples, mas pode não representar adequadamente valores múltiplos, evidências ou perspectivas. A regra de substituir valores precisa corresponder exatamente à política do benchmark.

**Ajuste exigido:** publicar o schema literal, exemplos completos e o prompt versionado. Definir se uma atualização pode combinar vários fatos no mesmo valor e como a avaliação rastreia cada fato esperado.

#### 3.3 Conjunto de dados e transições

**Crítica:** descrever o SUMIE não basta para reproduzir a preparação. O texto não fixa com precisão versão, partição, contagens e procedimento auditável de construção dos estados acumulados. O piloto de 25 entidades precisa ter separação clara da avaliação principal.

**Perguntas:** Como se obtém cada estado-ouro acumulado? Quem conferiu os casos ambíguos? Quantas transições têm PRESERVE, ADD e UPDATE?

**Ajuste exigido:** documentar script de preparação, partição, licença, hashes/versão, exclusões, contagens e exemplos revisados. Validar o piloto antes de usar os estados como referência.

#### 3.4 Modelos avaliados

**Crítica:** as famílias estão nomeadas, mas ainda não são identificadores reproduzíveis. O modelo de difusão exato é uma pendência que ameaça a viabilidade e a comparabilidade do experimento.

**Ajuste exigido:** congelar identificadores e revisões dos três modelos e registrar licença, tokenizer, template de conversa, parâmetros, precisão numérica e limitações conhecidas. Não iniciar a coleta principal com o checkpoint BD3LM indefinido.

#### 3.5 Ambiente de execução e *harness*

**Crítica:** aqui fica mais evidente o ponto levantado pelo orientador. O texto lista oito etapas do pipeline, mas não apresenta o projeto visualmente nem demonstra que os componentes existem e se comunicam. As notas técnicas de arquitetura ajudam a planejar, mas estão em rascunho.

**Ajuste exigido:** incorporar ao artigo ao menos: (1) diagrama de componentes — adaptador SUMIE, construtor de prompt, três adapters, logger, parser, validador, avaliador e armazenamento; (2) diagrama de sequência para uma transição; (3) diagrama do fluxo de dados e dos estados/ operações. Não desenhar uma interface de usuário fictícia: o produto de software deste estudo é o *harness* experimental. Acompanhar os diagramas com implementação, testes e uma execução demonstrável.

#### 3.6 Métricas

**Crítica:** a métrica denominada State F1 é uma adaptação baseada em correspondência canônica e não deve ser apresentada como reprodução direta do F1 semântico original do SUMIE. Igualdade textual pode penalizar paráfrases corretas. Há também casos de denominador zero, estado vazio, JSON inválido e schema inválido que precisam de regra explícita.

**Ajuste exigido:** validar canonicalização manualmente em amostra anotada; fixar regras para divisão por zero e falhas estruturais; reportar métricas condicionais e *end-to-end* separadamente; apresentar micro e/ou macroagregação com justificativa. Documentar limitações da taxa de alucinação, que exige distinguir fato sem suporte de paráfrase.

#### 3.7 Procedimento e análise estatística

**Crítica:** bootstrap por entidade e comparações pareadas são escolhas coerentes, mas falta mostrar como as dependências entre turnos serão preservadas na implementação da reamostragem. Não detectar diferença estatística não demonstra equivalência entre os modelos.

**Ajuste exigido:** especificar o algoritmo de reamostragem, tamanho da amostra efetiva, tratamento de comparações múltiplas e tamanho de efeito. Justificar a geração determinística e registrar seeds/configurações; evitar interpretar ausência de significância como equivalência.

#### 3.8 Rastreabilidade

**Crítica:** o quadro é uma boa matriz de planejamento, mas seus campos descrevem evidências futuras. No estado atual, ele não comprova que objetivos foram atendidos.

**Ajuste exigido:** após cada fase, substituir “será produzido” por referências a artefatos concretos: teste, log, tabela, gráfico ou commit identificável.

#### 3.9 Limitações e ameaças à validade

**Crítica:** a seção reconhece limitações importantes, especialmente o uso de estado-ouro anterior. Isso é metodologicamente honesto, mas significa que o experimento mede erro de transição isolado e não a degradação acumulada de um agente em execução real.

**Ajuste exigido:** manter essa limitação em destaque na discussão e nas conclusões. Incluir risco de inviabilidade de hardware/checkpoint e risco de validade da correspondência textual. Não prometer impacto em decisões finais do agente sem avaliar essa consequência.

### 4. Resultados esperados e cronograma

#### 4.1 Resultados e contribuições esperadas

**Crítica:** esta seção não contém resultados; contém previsões e entregáveis. Isso é aceitável em um projeto de TCC I, mas não atende a uma defesa de trabalho concluído. A frase sobre identificar qual arquitetura será “mais estável” não deve sugerir resultado antecipado.

**Ajuste exigido:** no projeto, apresentar resultados como perguntas e produtos esperados, sem expectativa direcional. No TCC final, substituir esta seção por resultados observados, análise, limitações e comparação com a literatura.

#### 4.2 Cronograma

**Crítica:** há uma sequência de atividades, mas o cronograma não torna visíveis marcos de decisão e contingências. A recomendação recebida de defender no semestre seguinte pode ser razoável se o restante for viável, mas o texto ainda prevê implementação e experimento no TCC II.

**Perguntas:** O que já foi implementado e validado? Quais disciplinas faltam no próximo semestre? A coordenação confirma a possibilidade de cursar TCC I e II ou defender nesse calendário?

**Ajuste exigido:** alinhar o cronograma ao calendário institucional e ao orientador; marcar datas de congelamento de protocolo, piloto, coleta, análise, redação e entrega; incluir plano alternativo caso um modelo não rode. Não reduzir o escopo removendo validação essencial só para antecipar a defesa.

### 5. Considerações finais

**Crítica:** o texto resume corretamente uma proposta, mas não conclui uma investigação. A linguagem precisa deixar claro que não há resultados empíricos ainda. Para a versão final, repetir objetivos sem responder à pergunta será insuficiente.

**Ajuste exigido:** após a coleta, responder à pergunta com dados, indicar o alcance da evidência e separar achados de trabalho futuro.

### Referências

**Crítica:** as referências sustentam o tema, mas precisam de uma auditoria bibliográfica final. A precisão dos dados de publicação, versões, autoria, ano e URL é parte da reprodutibilidade, não mero acabamento.

**Ajuste exigido:** conferir cada entrada com a fonte primária e normalizar o estilo institucional; verificar correspondência um-para-um entre citações no texto e lista final; registrar data de acesso quando exigida.

### Apêndice A — Prompt-base

**Crítica:** disponibilizar o prompt é positivo, mas o apêndice sozinho não permite reproduzir a chamada. Faltam os detalhes específicos de template, marcadores de conversa e parâmetros técnicos de cada modelo.

**Ajuste exigido:** manter o texto instrucional comum idêntico, documentar separadamente adaptações de API sem alteração semântica e fornecer um exemplo completo de chamada e resposta bruta anonimizadas ou sintéticas.

## Projeto e diagramas que precisam aparecer

As notas de apoio existentes são úteis, mas estão explicitamente marcadas como rascunho: [arquitetura do harness](../04_Implementacao/01_arquitetura_harness.md), [prompt-base](../04_Implementacao/02_prompt_base.md), [formato dos dados](../04_Implementacao/03_formato_dados.md) e [pipeline de avaliação](../04_Implementacao/04_pipeline_avaliacao.md). Elas não devem ser apresentadas como implementação pronta.

Para responder concretamente à crítica recebida, o artigo/projeto deve mostrar:

1. **Arquitetura do harness:** entradas, módulos, três escritores, validação, métricas e armazenamento dos resultados.
2. **Sequência de uma transição GU-JSON:** estado anterior, observação, prompt, geração bruta, parse/schema, comparação com estado esperado e log.
3. **Modelo de dados e operações:** registro de transição, estrutura JSON e exemplos de PRESERVE, ADD e UPDATE sob a política do SUMIE.
4. **Evidência de execução:** repositório/código, testes automatizados, uma execução piloto rastreável e arquivos de saída.

Não confundir esses diagramas do sistema experimental com diagramas de UML decorativos. Cada figura deve explicar uma decisão, componente ou fluxo que existe no projeto.

## Perguntas que eu faria antes de aprovar a próxima etapa

1. Qual é exatamente o produto de software que será entregue e onde está o código executável?
2. Que parte do pipeline já roda hoje, e qual teste comprova isso?
3. Qual checkpoint BD3LM será usado, com qual revisão e interface?
4. Quantas entidades e transições compõem cada partição do SUMIE?
5. Como os estados-ouro acumulados e os rótulos de operação foram construídos e auditados?
6. Como a avaliação distingue paráfrase correta de alucinação ou erro de valor?
7. O que o resultado permite concluir com estado-ouro por turno, e o que não permite concluir sobre memória acumulada?
8. O plano cabe no hardware, no calendário acadêmico e nas disciplinas restantes?

## Parecer e prioridade de trabalho

**Parecer simulado:** tema aprovado para continuidade, mas trabalho insuficiente para ser tratado como TCC concluído ou defendido sem implementação, diagramas e evidência empírica. A sugestão de defesa no semestre seguinte deve ser decidida com o orientador e a coordenação após confirmar disciplinas, prazos e viabilidade técnica.

**Ordem recomendada:**

1. Confirmar com o orientador se o próximo marco é projeto de TCC I ou defesa final e quais entregáveis a banca exige.
2. Fixar os três checkpoints e fazer prova de execução local antes de ampliar o texto.
3. Construir e testar o fluxo mínimo do *harness*; produzir os três diagramas acima a partir da implementação real.
4. Auditar o SUMIE, as transições, a política de conflito e a métrica de correspondência.
5. Executar piloto, corrigir o protocolo e só então congelar a coleta principal.
6. Rodar o experimento, publicar resultados reproduzíveis e reescrever a discussão e a conclusão com base nos dados.
