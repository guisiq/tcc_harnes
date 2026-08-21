---
tags:
  - tcc
  - metricas
  - protocolo
status: preliminar
---

# Métricas e protocolo experimental preliminar

## Variável independente

Depende do candidato final:

- 4A: estratégia de persistência com quatro níveis;
- 4B: estratégia compacta com três níveis;
- 4D: mecanismo de atualização do checkpoint JSON com dois níveis.

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

Registrar separadamente:

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

- tempo total por tarefa;
- tempo de preparação do contexto;
- tempo de inferência;
- tempo específico da retomada;
- percentis p50 e p95.

### Recursos locais

Quando possível, registrar pico de RAM e VRAM. Essas métricas ajudam a caracterizar a viabilidade, mas não precisam ser a contribuição principal.

## Variáveis de controle

- mesmo SLM e quantização;
- mesmas tarefas e pontos de interrupção;
- mesma configuração de geração;
- mesmo limite de passos;
- mesmo hardware;
- mesmas ferramentas;
- mesma ordem ou ordem aleatorizada de forma documentada;
- número igual de repetições por condição.

## Unidade experimental

Uma unidade pode ser definida como:

> Uma execução completa de uma instância de tarefa, sob uma estratégia de persistência e uma condição de interrupção.

## Protocolo mínimo recomendado

1. Definir duas famílias pequenas de tarefas transacionais.
2. Criar estados esperados e restrições verificáveis.
3. Fixar um ponto de interrupção por instância.
4. Executar primeiro a condição contínua.
5. Executar as condições de persistência com interrupção.
6. Repetir cada condição o mesmo número de vezes.
7. Validar automaticamente estado, restrições e ações.
8. Registrar tokens, latência e falhas.
9. Comparar proporções com intervalos de confiança.
10. Analisar qualitativamente as trajetórias de falha.

## Matriz mínima por candidato

| Candidato | Condições principais | Contexto recomendado | Métrica principal |
|---|---|---|---|
| 4A | Histórico, janela, resumo e checkpoint JSON | 3A + 3E | Sucesso final e custo |
| 4B | Janela, resumo e checkpoint JSON | 3A + 3C + 3E | Retenção de restrições |
| 4D | Checkpoint JSON por regras e por SLM | 3A + 3C + 3E | Correção do checkpoint JSON |

## Decisões pendentes para o piloto

- modelo e quantização;
- schema do checkpoint JSON;
- frequência de atualização do resumo e do checkpoint JSON;
- orçamento de contexto;
- quantidade de tarefas e repetições;
- ponto ou pontos de interrupção;
- temperatura e estratégia de amostragem;
- teste estatístico final.

## Critério de viabilidade

O piloto deve demonstrar que o modelo consegue concluir uma parcela razoável das tarefas na condição contínua. Se ele falhar quase sempre sem interrupção, não será possível atribuir as falhas à persistência de estado.

