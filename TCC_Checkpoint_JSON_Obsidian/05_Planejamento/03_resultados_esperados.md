---
title: "Resultados esperados — sem antecipar resultados"
aliases:
  - "03 resultados esperados"
tags:
  - tcc
  - planejamento
status: draft
---

# Resultados esperados — sem antecipar resultados

Este documento serve para planejar **que tipos de evidência serão úteis**, não para supor qual modelo vencerá.

## Resultado relevante A

Diferenças pequenas no F1 global, mas grandes em `Preservation Accuracy`.

Interpretação possível:
> modelos podem ter qualidade agregada semelhante e perfis distintos de preservação do estado.

## Resultado relevante B

Um writer gera JSON válido com frequência alta, mas mantém fatos obsoletos.

Interpretação:
> correção sintática não implica memória operacional correta.

## Resultado relevante C

Writers apresentam F1 agregado semelhante, mas diferem em operações específicas.

Interpretação:
> qualidade global semelhante pode ocultar perfis diferentes de preservação e atualização.

## Resultado relevante D

As diferenças observadas no SUMIE podem não se repetir na amostra FactConsolidation-SH de supersession.

Interpretação:
> os resultados podem depender do tipo de informação e operação presentes no dataset.


## Resultado nulo também é relevante

Se não houver diferença estatisticamente/praticamente relevante:

> modelos compactos dos três paradigmas podem ser substituíveis nesta tarefa sob o protocolo testado.

Esse resultado ainda seria útil se o desenho experimental for sólido e os limites forem bem documentados.
