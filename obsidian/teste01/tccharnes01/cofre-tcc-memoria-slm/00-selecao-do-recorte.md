---
aliases:
  - Seleção de granularidade
tags:
  - tcc
  - delimitacao
  - granularidade
status: preliminar
---

# Seleção do recorte

Foram mantidas 13 opções. Os níveis 0 e 1 definem a base do tema; os níveis 2 e 3 apresentam escolhas experimentais; o nível 4 contém três formulações finais alternativas.

| Nível | Opção escolhida | Descrição expandida | Pergunta correspondente |
| --- | --- | --- | --- |
| 0 — Área ampla | [[01-base-conceitual#0B — Gerenciamento de contexto\|0B · Gerenciamento de contexto]] | Examina como o conteúdo disponível ao modelo é selecionado, reduzido e organizado dentro de uma janela limitada. Inclui histórico, recuperação, sumarização e estruturas externas de contexto. | Como o gerenciamento de contexto influencia o desempenho de agentes baseados em modelos de linguagem? |
| 1 — Fenômeno | [[01-base-conceitual#1A — Persistência de estado\|1A · Persistência de estado]] | Focaliza a conservação explícita do estado operacional entre as etapas de uma tarefa, incluindo fatos coletados, decisões tomadas, restrições vigentes e ações já executadas. | Em que medida diferentes estratégias de persistência de estado afetam a confiabilidade e a eficiência de um agente baseado em SLM? |
| 2 — Comparação | [[02-comparacoes#2A — Quatro estratégias\|2A · Quatro estratégias]] | Usa o histórico completo como referência e compara três formas de compactação ou externalização: janela recente, resumo em linguagem natural e estado estruturado em JSON. | Como essas quatro estratégias diferem quanto à confiabilidade e à eficiência de agentes baseados em SLMs? |
| 2 — Comparação | [[02-comparacoes#2B — Resumo versus checkpoint JSON\|2B · Resumo × checkpoint JSON]] | Isola o efeito da representação do estado: texto livre produzido por sumarização versus campos explícitos e verificáveis em uma estrutura JSON. | Checkpoints JSON preservam melhor o estado da tarefa do que resumos textuais? |
| 2 — Comparação | [[02-comparacoes#2D — Origem do checkpoint JSON\|2D · Origem do checkpoint JSON]] | Separa checkpoints JSON atualizados por regras do harness de checkpoints JSON extraídos pelo próprio modelo. Isso permite medir se erros surgem da estratégia de memória ou da geração do estado. | Como a forma de criação do checkpoint JSON afeta a correção e a consistência do estado persistido? |
| 2 — Comparação | [[02-comparacoes#2E — Execução contínua versus interrompida\|2E · Contínua × interrompida]] | Compara a execução sem interrupção com a retomada a partir de estado persistido. A condição contínua funciona como referência para estimar o custo específico da interrupção. | Qual é o impacto da interrupção e da restauração do estado sobre o sucesso final da tarefa? |
| 3 — Contexto | [[03-contextos-de-avaliacao#3A — Tarefas sintéticas e determinísticas\|3A · Tarefas determinísticas]] | Emprega tarefas artificiais com estados finais, restrições e pontos de interrupção definidos previamente. Essa escolha permite avaliação automática, repetição controlada e análise causal. | Como as estratégias se comportam em tarefas cujo estado final e restrições podem ser verificados automaticamente? |
| 3 — Contexto | [[03-contextos-de-avaliacao#3C — Fluxos transacionais\|3C · Fluxos transacionais]] | Modela processos como cadastro, reserva ou solicitação, nos quais informações são coletadas progressivamente. O estado correto pode ser comparado campo a campo depois da retomada. | Qual estratégia reduz a perda de campos e restrições em fluxos transacionais interrompidos? |
| 3 — Contexto | [[03-contextos-de-avaliacao#3D — Conversações longas\|3D · Conversações longas]] | Distribui fatos e preferências por uma conversa extensa para avaliar recuperação temporal e manutenção de coerência. Aproxima o estudo de benchmarks de memória conversacional. | Qual estratégia recupera melhor informações relevantes distribuídas ao longo de uma interação extensa? |
| 3 — Contexto | [[03-contextos-de-avaliacao#3E — Execução local com SLM de 1–4B\|3E · Execução local 1–4B]] | Restringe o experimento a um modelo aberto de 1–4B, quantizado e executado em hardware de consumo. A limitação torna tokens, latência, RAM e VRAM parte relevante da análise. | Qual estratégia oferece melhor equilíbrio entre confiabilidade e custo computacional em um SLM executado localmente? |
| 4 — Candidato final | [[04-candidatos-finais#4A — Comparação ampla\|4A · Comparação ampla]] | Recorte abrangente que mede quatro estratégias durante interrupções controladas. Compara sucesso final, retenção de restrições, ações inconsistentes, tokens e latência usando o mesmo modelo e as mesmas tarefas. | Em que medida histórico completo, janela deslizante, sumarização textual e checkpoint JSON afetam a confiabilidade e a eficiência de um SLM local na retomada de tarefas interrompidas? |
| 4 — Candidato final | [[04-candidatos-finais#4B — Preservação de restrições\|4B · Preservação de restrições]] | Recorte reduzido centrado em estratégias compactas e na preservação de restrições. É indicado se quatro condições tornarem o experimento excessivo para o calendário do TCC. | Em SLMs locais, checkpoints JSON reduzem a perda de restrições quando comparados à sumarização textual e à janela deslizante? |
| 4 — Candidato final | [[04-candidatos-finais#4D — Validação do checkpoint JSON\|4D · Validação do checkpoint JSON]] | Recorte metodológico que investiga a procedência do checkpoint JSON. Compara atualização determinística e geração pelo SLM para separar falhas de armazenamento de falhas de extração do estado. | Checkpoints JSON atualizados deterministicamente são mais confiáveis do que checkpoints JSON gerados pelo próprio SLM na retomada de tarefas interrompidas? |

## Síntese do tema atual

O tema investiga como mecanismos externos de gerenciamento de contexto preservam o [[05-glossario#Estado operacional|estado operacional]] de agentes baseados em [[05-glossario#SLM|SLMs]] locais. A avaliação deverá observar interrupção e retomada de tarefas, correção do estado, preservação de restrições e custo computacional.

## Decisão que ainda falta

É necessário escolher **um candidato final principal**:

- 4A para uma comparação abrangente;
- 4B para um TCC mais estreito e viável;
- 4D para estudar especificamente a produção e validação do checkpoint JSON.

Consulte [[04-candidatos-finais#Comparação dos candidatos]].

