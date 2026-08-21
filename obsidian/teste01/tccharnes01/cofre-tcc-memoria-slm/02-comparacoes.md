---
tags:
  - tcc
  - experimento
  - comparacoes
---

# Comparações experimentais selecionadas

## 2A — Quatro estratégias

### Estratégias

1. **Histórico completo:** todas as mensagens e resultados anteriores são mantidos na entrada enquanto couberem na janela de contexto.
2. **Janela deslizante:** apenas as interações mais recentes são mantidas; conteúdos antigos são descartados.
3. **Sumarização textual:** interações antigas são substituídas por um resumo em linguagem natural.
4. **Checkpoint JSON:** o estado necessário à continuação é registrado em campos estruturados.

### O que essa comparação isola

Com o mesmo modelo, tarefas e configuração de geração, a comparação estima quanto o formato de memória externa altera a confiabilidade e o custo.

### Cuidados metodológicos

- O histórico completo não é ilimitado; é preciso definir o que acontece quando ele ultrapassa a janela.
- A sumarização introduz uma chamada adicional ou um processo periódico.
- O checkpoint JSON precisa ter um schema fixo e regras claras de atualização.
- As condições devem receber informações semanticamente equivalentes sempre que possível.

### Métricas centrais

[[06-metricas-e-protocolo#Taxa de sucesso final]], [[06-metricas-e-protocolo#Retenção de restrições]], [[06-metricas-e-protocolo#Ações inconsistentes]], tokens e latência.

## 2B — Resumo versus checkpoint JSON

Esta comparação reduz o experimento a duas representações compactas:

- **resumo textual:** flexível, legível e capaz de conservar nuances, porém sujeito a omissões e reformulações;
- **checkpoint JSON:** explícito, validável e fácil de comparar, porém limitado pelo schema escolhido.

### Hipótese possível

O checkpoint JSON pode preservar melhor campos e restrições explicitamente modelados, enquanto o resumo pode preservar melhor informações abertas que não foram previstas no schema.

### Variável que precisa ser controlada

As duas estratégias devem usar um orçamento de contexto comparável. Caso o JSON seja muito menor do que o resumo, o efeito observado misturará **formato** e **quantidade de informação**.

### Resultado esperado do estudo

Não é necessário provar que uma estratégia é universalmente superior. É suficiente identificar em quais tipos de tarefa cada representação falha e qual custo apresenta.

## 2D — Origem do checkpoint JSON

Há duas formas principais de produzir e atualizar o checkpoint JSON:

### Atualização determinística

O harness atualiza o estado a partir de eventos confirmados. Por exemplo, depois de uma ferramenta registrar uma reserva, o programa grava `status: confirmado`.

Vantagens:

- maior rastreabilidade;
- validação direta;
- menor risco de invenção do estado;
- melhor isolamento experimental.

Limitação: exige regras específicas para cada tipo de tarefa.

### Atualização pelo SLM

O modelo recebe o histórico e gera uma nova representação do estado.

Vantagens:

- maior flexibilidade;
- menor necessidade de regras específicas;
- possibilidade de extrair informação de texto livre.

Riscos:

- omissão de campos;
- alteração de valores;
- inferência não autorizada;
- JSON inválido;
- acúmulo de erros entre checkpoints JSON.

### O que essa comparação mede

Separa a confiabilidade do **formato do checkpoint JSON** da confiabilidade do **processo que extrai ou atualiza o estado**.

Para o experimento principal, recomenda-se começar com atualização determinística. A geração pelo SLM pode ser uma extensão.

## 2E — Execução contínua versus interrompida

A execução contínua funciona como linha de base: o agente conclui a tarefa sem precisar restaurar o estado. Na condição interrompida, a execução é pausada em um ponto definido e retomada apenas com a memória permitida pela estratégia.

### Por que essa linha de base é necessária

Um fracasso após a retomada pode ter duas causas:

1. o modelo não consegue realizar a tarefa, mesmo sem interrupção;
2. a restauração perdeu ou alterou informações necessárias.

Comparar as duas condições ajuda a estimar a **penalidade de retomada**.

### Pontos de interrupção

Os pontos devem ser definidos previamente, por exemplo:

- depois da coleta de metade dos campos;
- depois de uma decisão confirmada;
- antes de uma chamada crítica de ferramenta;
- depois de receber um resultado intermediário.

Termos relacionados: [[05-glossario#Interrupção controlada]], [[05-glossario#Retomada]], [[06-metricas-e-protocolo#Penalidade de retomada]].

