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

SUMIE relata perfis diferentes entre modelos; Lu et al. mostram resultados dependentes da tarefa em modelos de difusão maiores. Esses antecedentes motivam analisar perfis, não predizem o ranking de writers compactos em GU-json. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al., 2026]].

## Resultado relevante A

Diferenças pequenas no F1 global, mas grandes em `Preservation Accuracy`.

Interpretação possível:
> modelos podem ter qualidade agregada semelhante e perfis distintos de preservação do estado.

## Resultado relevante B

Um writer gera JSON válido com frequência alta, mas mantém fatos obsoletos.

Interpretação:
> correção sintática não implica memória operacional correta.

Contar como obsoleto apenas o que a regra da tarefa invalida, não opiniões divergentes válidas no SUMIE. [[06_Referencias/referencias#JSONSchemaBench|JSONSchemaBench]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

## Resultado relevante C

Writers apresentam F1 agregado semelhante, mas diferem em operações específicas.

Interpretação:
> qualidade global semelhante pode ocultar perfis diferentes de preservação e atualização.

## Resultado relevante D

As diferenças observadas no SUMIE podem não se repetir na amostra FactConsolidation-SH de supersession.

Interpretação:
> os resultados podem depender do tipo de informação e operação presentes no dataset.

O contraste entre datasets não isola o efeito da operação; a H2 permanece exploratória. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].


## Resultado nulo também é relevante

Se não houver diferença estatisticamente/praticamente relevante:

> não foi detectada diferença relevante entre os representantes sob o protocolo e a precisão estatística obtida.

Ausência de diferença detectada não prova equivalência ou substituibilidade; interpretar os intervalos e limites do desenho.

Esse resultado ainda seria útil se o desenho experimental for sólido e os limites forem bem documentados.
