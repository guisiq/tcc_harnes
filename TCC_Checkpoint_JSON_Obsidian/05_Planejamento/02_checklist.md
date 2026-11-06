---
title: "Checklist"
aliases:
  - "02 checklist"
tags:
  - tcc
  - planejamento
status: draft
---

# Checklist

## Revisão
- [ ] Ler Hwang integralmente
- [ ] Ler SUMIE
- [ ] Ler MemoryAgentBench
- [ ] Ler Yuen
- [ ] Ler PRISM na versão publicada EMNLP 2025
- [ ] Ler Zeng como contexto de representação/recuperação
- [ ] Ler Qwen3 Technical Report
- [ ] Ler T5Gemma report
- [ ] Ler Block Diffusion
- [ ] Ler paper do diffusion selecionado
- [ ] Fichar os contrapontos de Lu et al. e Mündler et al.
- [ ] Executar backward snowballing
- [ ] Executar forward snowballing

Seguir [[06_Referencias/artigos_prioridade|Prioridades auditadas]] e [[06_Referencias/referencias|Bibliografia]]. As caixas representam atividades do projeto, não são concluídas automaticamente pela auditoria bibliográfica.

## Modelos
- [ ] Confirmar Qwen3-0.6B
- [ ] Aceitar licença/acesso T5Gemma
- [ ] Confirmar repositório exato Qwen diffusion BD3LM
- [ ] Testar FP16 na GTX 1650
- [ ] Registrar versões

## Dados
- [ ] Baixar SUMIE
- [ ] Baixar MemoryAgentBench
- [ ] Criar transition format
- [ ] Validar ground truth
- [ ] Validar canonicalização e viabilidade dos estados sob 300 tokens fixos
- [ ] Rotular operações sem transformar opiniões divergentes do SUMIE em supersession
- [ ] Documentar a regra temporal de FactConsolidation-SH
- [ ] Confirmar licença e revisão dos dados MemoryAgentBench diante da divergência cartão/artigo
- [ ] Fixar critérios e tamanho da amostra FactCon-SH antes da comparação

## Harness
- [ ] Adapter AR
- [ ] Adapter encoder-decoder
- [ ] Adapter diffusion
- [ ] Logger
- [ ] JSON parser
- [ ] Schema validator
- [ ] Metric calculator
- [ ] Tests

## Experimentos
- [ ] sanity check
- [ ] validar os três writers em uma amostra curta de transições
- [ ] piloto SUMIE
- [ ] SUMIE completo
- [ ] amostra de supersession FactCon-SH, após SUMIE

## Escrita
- [ ] Problema
- [ ] Objetivo geral
- [ ] Objetivos específicos
- [ ] RQs
- [ ] Trabalhos relacionados
- [ ] Método
- [ ] Ameaças
- [ ] Resultados
- [ ] Discussão
- [ ] Conclusão
