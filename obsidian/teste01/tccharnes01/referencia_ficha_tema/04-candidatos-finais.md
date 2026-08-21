---
tags:
  - tcc
  - tema
  - decisao
status: em-selecao
---

# Candidatos finais

## 4B — Preservação de restrições

### Pergunta

> Em SLMs locais, checkpoints JSON reduzem a perda de restrições quando comparados à sumarização textual?

### Escopo

- duas estratégias de persistência: sumarização textual e checkpoint JSON;
- foco em interrupção e retomada;
- tarefas com restrições explícitas;
- compatibilidade obrigatória com a execução local definida em 3E;
- avaliação de retenção e sucesso final.

### Principal vantagem

É o candidato mais delimitado e mais fácil de executar como TCC. A variável dependente principal — retenção de restrições — pode ser calculada automaticamente.

### Principal risco

Um schema mal projetado pode favorecer artificialmente o checkpoint JSON. As restrições avaliadas devem ser representáveis de maneira justa por todas as estratégias.

## Decisão adotada

Adotar 4B como recorte principal do TCC. O experimento compara sumarização textual e checkpoint JSON, com foco na preservação de restrições em tarefas sintéticas e determinísticas executadas por um SLM local.

