---
title: "Hardware e viabilidade de execução local"
aliases:
  - "07 hardware local"
tags:
  - tcc
  - metodologia
status: draft
---

# Hardware e viabilidade de execução local

## PC 1 — principal

- Lenovo IdeaPad Gaming 3i;
- Intel Core i5 de 10ª geração;
- 24 GB RAM;
- GeForce GTX 1650;
- ambiente principal de inferência local.

Confirmar a capacidade de VRAM disponível e a compatibilidade das dependências antes de iniciar a coleta.

## PC 2 — auxiliar

Informado como:

- Intel Core i5 de "1°/11° geração";
- 16 GB RAM;
- vídeo integrado.

**Ação:** confirmar a geração exata do processador.

## Divisão de trabalho

### PC 1

Executar os três writers, desde que os modelos possam ser carregados no ambiente local.

### PC 2

Preparar datasets, fazer parsing, validar o schema, calcular métricas e produzir tabelas e análises.

## Critério de viabilidade

Antes da coleta principal, verificar no piloto que cada modelo consegue carregar e concluir as transições previstas. Se algum modelo não for compatível com o ambiente local, revisar a seleção de modelos ou o escopo experimental.
