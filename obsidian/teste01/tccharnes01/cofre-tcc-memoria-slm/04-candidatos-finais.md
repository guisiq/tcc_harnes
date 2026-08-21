---
tags:
  - tcc
  - tema
  - decisao
status: em-selecao
---

# Candidatos finais

## 4A — Comparação ampla

### Pergunta

> Em que medida histórico completo, janela deslizante, sumarização textual e checkpoint JSON afetam a confiabilidade e a eficiência de um SLM local na retomada de tarefas interrompidas?

### Escopo

- quatro estratégias;
- execução contínua e interrompida;
- um SLM local;
- tarefas determinísticas;
- métricas de qualidade e custo.

### Principal vantagem

Produz uma visão abrangente e permite observar diferentes compromissos entre retenção de informação e custo.

### Principal risco

O número de condições cresce rapidamente. Quatro estratégias em dois modos de execução já formam oito condições antes de considerar tarefas e repetições.

## 4B — Preservação de restrições

### Pergunta

> Em SLMs locais, checkpoints JSON reduzem a perda de restrições quando comparados à sumarização textual e à janela deslizante?

### Escopo

- três estratégias compactas;
- foco em interrupção e retomada;
- tarefas com restrições explícitas;
- avaliação de retenção e sucesso final.

### Principal vantagem

É o candidato mais delimitado e mais fácil de executar como TCC. A variável dependente principal — retenção de restrições — pode ser calculada automaticamente.

### Principal risco

Um schema mal projetado pode favorecer artificialmente o checkpoint JSON. As restrições avaliadas devem ser representáveis de maneira justa por todas as estratégias.

## 4D — Validação do checkpoint JSON

### Pergunta

> Checkpoints JSON atualizados deterministicamente são mais confiáveis do que checkpoints JSON gerados pelo próprio SLM na retomada de tarefas interrompidas?

### Escopo

- um formato de checkpoint JSON;
- dois mecanismos de atualização;
- tarefas interrompidas;
- correção do estado e propagação de erros.

### Principal vantagem

Tem uma pergunta causal clara e separa a representação do estado do processo de criação do estado.

### Principal risco

A comparação pode ser previsível se a atualização determinística tiver acesso direto ao estado correto do ambiente. É necessário definir quais eventos e informações cada método pode observar.

## Comparação dos candidatos

| Critério | 4A — Amplo | 4B — Restrições | 4D — Origem do checkpoint JSON |
|---|---|---|---|
| Número de estratégias | 4 | 3 | 2 mecanismos |
| Pergunta principal | Qual estratégia funciona melhor? | O checkpoint JSON reduz perda de restrições? | Quem deve produzir o checkpoint JSON? |
| Complexidade | Alta | Média-baixa | Média |
| Métrica central | Sucesso e custo | Retenção de restrições | Correção do checkpoint JSON |
| Risco de escopo | Alto | Baixo | Médio |
| Recomendação | Revisão ampla ou experimento com poucas tarefas | Melhor candidato para o TCC principal | Boa extensão ou alternativa metodológica |

## Rotas coerentes

### Rota abrangente

`0B → 1A → 2A + 2E → 3A + 3E → 4A`

### Rota recomendada para o TCC

`0B → 1A → 2B + 2E → 3A + 3C + 3E → 4B`

### Rota metodológica

`0B → 1A → 2D + 2E → 3A + 3C + 3E → 4D`

## Decisão preliminar sugerida

Adotar 4B como tema principal e manter 4D como extensão opcional. Usar 4A para organizar a revisão bibliográfica, sem assumir que todas as quatro estratégias precisarão integrar o experimento final.

