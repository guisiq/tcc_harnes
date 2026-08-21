---
tags:
  - tcc
  - glossario
---

# Glossário

## Ações inconsistentes

Ações que repetem, contradizem ou desfazem indevidamente uma decisão anterior. Exemplos: registrar duas vezes a mesma reserva ou ignorar uma confirmação já realizada.

## Agente baseado em modelo de linguagem

Sistema no qual um modelo de linguagem participa de um ciclo de observação, decisão e ação. O agente pode consultar memória, chamar ferramentas e atualizar um ambiente.

## Checkpoint JSON

Registro explícito do estado da tarefa em JSON. Seus campos podem representar objetivos, dados coletados, restrições, ações realizadas e próximos passos.

## Confiabilidade

Capacidade de produzir resultados corretos e consistentes em diferentes tarefas e repetições. No estudo, deve ser operacionalizada por métricas específicas, não usada apenas como conceito abstrato.

## Estado final

Situação do ambiente depois da execução da tarefa. É comparado com um estado esperado para determinar se a tarefa foi realmente concluída.

## Estado operacional

Conjunto mínimo de informações necessárias para continuar uma tarefa corretamente: objetivo, campos, decisões, restrições, resultados e progresso.

## Execução contínua

Condição na qual o agente realiza todos os passos sem interrupção artificial. Serve como referência para avaliar a penalidade causada pela retomada.

## Harness

Camada de software ao redor do modelo que prepara contexto, chama o modelo, valida saídas, executa ferramentas, mantém estado e registra trajetórias.

## Hardware de consumo

Computador pessoal sem infraestrutura especializada de datacenter. Neste projeto, envolve GPU com 6 GB de VRAM e 16 GB de RAM.

## Histórico completo

Estratégia que reapresenta ao modelo todas as mensagens e resultados anteriores enquanto couberem na janela disponível.

## Interrupção controlada

Pausa aplicada em um ponto definido previamente e repetido nas mesmas condições experimentais.

## Janela de contexto

Quantidade máxima de tokens que o modelo consegue processar em uma chamada, incluindo instruções, histórico, memória, ferramentas e saída reservada.

## Janela deslizante

Estratégia que conserva somente as mensagens mais recentes e remove as mais antigas quando o contexto cresce.

## Memória externa

Informação armazenada fora dos parâmetros do modelo, como histórico, banco vetorial, arquivo, resumo ou checkpoint JSON.

## Quantização

Redução da precisão numérica dos pesos para diminuir uso de memória e permitir execução local. Pode alterar velocidade e qualidade das respostas.

## Restrição

Condição que deve permanecer verdadeira durante a tarefa, como limite de orçamento, data permitida, preferência do usuário ou proibição de repetir uma ação.

## Retomada

Continuação de uma tarefa depois de interrupção, usando o estado persistido e o contexto disponibilizado pelo harness.

## Schema

Definição dos campos, tipos, valores permitidos e obrigatoriedade de uma estrutura. Em JSON, pode ser validado automaticamente.

## SLM

*Small Language Model* ou pequeno modelo de linguagem. Neste projeto, refere-se operacionalmente a um modelo aberto de aproximadamente 1–4 bilhões de parâmetros, adequado à execução local.

## Sumarização textual

Compactação do histórico em texto livre. Pode reduzir tokens, mas também omitir, reinterpretar ou fundir informações.

## Tarefa de múltiplas etapas

Tarefa que exige uma sequência de decisões, coletas de dados ou chamadas de ferramentas, criando dependência entre passos anteriores e posteriores.

## Tokens

Unidades em que o texto é dividido para processamento pelo modelo. Servem como medida de volume de entrada e saída.

## Validação determinística

Verificação realizada por regras de software, sem depender do julgamento do modelo. Exemplos: validar JSON, comparar campos e verificar o estado final.

## Validade externa

Grau em que os resultados podem ser generalizados para outros modelos, tarefas, usuários ou ambientes.

## Validade interna

Grau em que a diferença observada pode ser atribuída à estratégia estudada, e não a variáveis de confusão.

## VRAM

Memória da GPU usada para carregar pesos, cache de atenção e outros dados durante a inferência.

