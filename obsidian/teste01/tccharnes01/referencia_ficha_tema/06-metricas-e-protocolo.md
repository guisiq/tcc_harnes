---
tags:
  - tcc
  - metricas
  - protocolo
status: preliminar
---
# Métricas e protocolo experimental preliminar

## Delimitação experimental

O experimento corresponde ao candidato 4B e deve respeitar obrigatoriamente o contexto 3E. 

## Variável independente

A variável independente é a estratégia de persistência, com dois níveis:

1. **Sumarização textual:** substitui parte do histórico por um resumo em linguagem natural.
2. **Checkpoint JSON:** persiste o estado operacional em campos estruturados.

A condição de execução contínua e a interrupção controlada são condições do protocolo, não níveis adicionais da variável independente.

## Modelos e compatibilidade

O conjunto preliminar de modelos para o piloto é:

| Modelo | Arquitetura | Função preliminar |
| --- | --- | --- |
| Qwen2.5-3B-Instruct | Transformer decoder-only | Baseline Transformer A |
| Phi-3.5-mini-Instruct ou Gemma pequeno equivalente | Transformer decoder-only | Baseline Transformer B |
| RecurrentGemma 2B-IT | Griffin, com atenção local e recorrência | Arquitetura híbrida recorrente |
| Mamba aproximadamente 2.8B instruction-tuned | State Space Model (SSM) | Arquitetura baseada em estado |

O piloto deve selecionar um modelo principal, registrando o motivo da escolha. A seleção deve considerar capacidade de concluir as tarefas sem interrupção, compatibilidade com as ferramentas, memória disponível, latência e estabilidade da geração. Comparar todos os modelos entre si não faz parte do experimento principal, pois isso misturaria arquitetura do SLM com estratégia de persistência.

## Variáveis dependentes

### Taxa de sucesso final

Proporção de execuções cujo estado final corresponde aos critérios de conclusão.

`sucesso final = execuções corretas / total de execuções`

### Sucesso após retomada

Proporção de execuções interrompidas que concluem corretamente a tarefa depois da restauração.

### Retenção de restrições

Proporção das restrições originalmente válidas que permanecem corretas depois da retomada.

`retenção = restrições preservadas / restrições esperadas`

É recomendável registrar também violações críticas separadamente, porque uma única violação pode invalidar toda a tarefa.

### Correção do checkpoint JSON

Proporção de campos cujo valor corresponde ao estado verdadeiro do ambiente no momento do checkpoint JSON.

`correção = campos corretos / campos avaliáveis`

Essa métrica é específica da condição de checkpoint JSON. Para a sumarização textual, a qualidade da memória deve ser avaliada pelo estado recuperado, pelas restrições preservadas e pelo resultado final.

Registrar separadamente no checkpoint JSON:

- campos ausentes;
- valores alterados;
- campos inventados;
- estrutura inválida.

### Ações inconsistentes

Contagem de ações duplicadas, contraditórias, inválidas ou executadas fora de ordem.

### Penalidade de retomada

Diferença entre o desempenho da execução contínua e o desempenho da execução interrompida.

`penalidade = sucesso contínuo − sucesso após retomada`

### Consumo de tokens

Somar tokens de entrada e saída de todas as chamadas necessárias à tarefa, incluindo chamadas de sumarização ou produção do checkpoint JSON.

### Latência

Registrar:

- ~~<mark data-color="#ff8c0066" style="background-color: rgba(255, 140, 0, 0.4); color: inherit;">tempo total por tarefa;</mark>~~
- ~~<mark data-color="#ff8c0066" style="background-color: rgba(255, 140, 0, 0.4); color: inherit;">tempo de preparação do contexto;</mark>~~
- ~~<mark data-color="#ff8c0066" style="background-color: rgba(255, 140, 0, 0.4); color: inherit;">tempo de inferência;</mark>~~
- ~~<mark data-color="#ff8c0066" style="background-color: rgba(255, 140, 0, 0.4); color: inherit;">tempo específico da retomada;</mark>~~
- ~~<mark data-color="#ff8c0066" style="background-color: rgba(255, 140, 0, 0.4); color: inherit;">percentis p50 e p95.</mark>~~

### Recursos locais

Quando possível, registrar pico de RAM e VRAM. Essas métricas ajudam a caracterizar a viabilidade, mas não precisam ser a contribuição principal.

## Variáveis de controle

- mesmo modelo principal, versão e quantização;
- mesma família de ferramentas e mesmo contrato de saída;
- mesmas tarefas e pontos de interrupção;
- mesma configuração de geração;
- mesmo limite de passos;
- mesmo hardware;
- mesma ordem ou ordem aleatorizada de forma documentada;
- número igual de repetições por condição.

## Unidade experimental

Uma unidade pode ser definida como:

> Uma execução completa de uma instância de tarefa, sob uma estratégia de persistência e uma condição de interrupção.

## Protocolo mínimo recomendado

 1. Definir uma família pequena de tarefas sintéticas e determinísticas, com múltiplas etapas.
 2. Criar estados esperados e restrições verificáveis.
 3. Escolher o modelo principal e a quantização no piloto.
 4. Fixar um ponto de interrupção por instância.
 5. Executar primeiro a condição contínua como referência de viabilidade.
 6. Executar as duas estratégias de persistência com interrupção.
 7. Repetir cada condição o mesmo número de vezes.
 8. Validar automaticamente estado, restrições e ações.
 9. Registrar tokens, latência, memória e falhas.
10. Comparar proporções com intervalos de confiança.
11. Analisar qualitativamente as trajetórias de falha.

## Matriz mínima por candidato

| Candidato | Condições principais | Contexto recomendado | Métrica principal |
| --- | --- | --- | --- |
| 4B | Resumo e checkpoint JSON | 3A + 3E | Retenção de restrições |

## Decisões pendentes para o piloto

- modelo principal entre os candidatos de 3E e sua quantização;
- versão do modelo, contexto máximo e parâmetros de geração;
- schema do checkpoint JSON;
- frequência de atualização do resumo e do checkpoint JSON;
- orçamento de contexto;
- quantidade de tarefas e repetições;
- ponto ou pontos de interrupção;
- temperatura e estratégia de amostragem;
- teste estatístico final.

## Critério de viabilidade

O piloto deve demonstrar que o modelo escolhido consegue concluir uma parcela razoável das tarefas na condição contínua. Se ele falhar quase sempre sem interrupção, não será possível atribuir as falhas à persistência de estado. Também deve verificar que as duas estratégias cabem no orçamento de contexto e que o checkpoint JSON pode ser validado automaticamente.