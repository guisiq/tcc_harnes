---
tags:
  - tcc
  - experimento
  - comparacoes
---

# Comparações experimentais selecionadas

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


