---
title: "Ameaças à validade"
aliases:
  - "08 ameacas validade"
tags:
  - tcc
  - metodologia
status: draft
---

# Ameaças à validade

## Validade interna

### Modelos não são perfeitamente pareados
Qwen3, T5Gemma e Qwen-diffusion possuem treinamentos e tokenizadores diferentes.

A documentação do candidato diffusion ainda precisa confirmar origem e escala. Não deduzir equivalência de treinamento apenas do nome Qwen3. [[06_Referencias/referencias#Qwen3 Technical Report|Qwen3]]; [[06_Referencias/referencias#T5Gemma|T5Gemma]]; [[06_Referencias/referencias#Block Diffusion|Block Diffusion]].

Mitigação:
- aproximar escala;
- usar instruction-tuned quando possível;
- manter todas as demais condições fixas;
- evitar linguagem causal absoluta.

### Decoding diferente
Diffusion não possui exatamente o mesmo processo de geração que AR/seq2seq.

Mitigação:
- fixar budgets equivalentes;
- documentar parâmetros;
- evitar constrained decoding no experimento principal;

### Schema favorece um paradigma
A escolha de schema pode interagir com o modelo; a direção dessa interação não está demonstrada para os representantes do TCC. Resultados de templates em sistemas multiagente não provam superioridade de JSON fixo. [[06_Referencias/referencias#Yuen et al. — Intrinsic Memory Agents|Yuen et al.]]; [[06_Referencias/referencias#PRISM|PRISM]].

Mitigação:
- schema simples;
- justificar pelo problema de estado;
- mesma estrutura para todos.

---

## Validade de construção

### JSON válido não significa memória correta
Mitigação:
- usar F1, preservation, update, supersession e stale facts.

Conformidade estrutural e avaliação do conteúdo têm bases distintas. [[06_Referencias/referencias#JSONSchemaBench|JSONSchemaBench]]; [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]].

### Adaptação de anotações e políticas de conflito
SUMIE fornece anotações por parágrafo e preserva perspectivas conflitantes; FactConsolidation define invalidação temporal explícita. Construir estados acumulados e rótulos sem confundir essas políticas. O F1 original do SUMIE inclui avaliação semântica de evidências, enquanto o State F1 local depende de canonicalização validada. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

### Capacidade do estado de referência
Verificar a viabilidade dos estados esperados sob o teto fixo de 300 tokens e registrar a política de representação. Falta de capacidade não deve ser confundida automaticamente com falha de preservação; não haverá ablação de orçamento.

---

## Validade externa

SUMIE é sintético e representa sumarização incremental de entidades. A amostra de FactConsolidation-SH cobre apenas um contraste de supersession.

Mitigação:
- declarar que os resultados não demonstram generalização para diálogo longo, tarefas multi-hop ou todos os tipos de memória.

---

## Validade de conclusão

### Operação confundida com dataset
SUMIE e FactConsolidation-SH diferem em domínio e política de atualização. Sem casos comparáveis dentro de um mesmo cenário, diferenças entre eles não isolam o efeito de supersession. Manter H2 e a amostra SH como exploratórias. [[06_Referencias/referencias#Hwang et al. — SUMIE|SUMIE]]; [[06_Referencias/referencias#Hu et al. — MemoryAgentBench|MemoryAgentBench]].

### Extrapolação de resultados sobre difusão
Resultados em ferramentas ou memória textual com modelos maiores não predizem fidelidade de JSON compacto; resultados com gramáticas não equivalem ao protocolo prompt-only. [[06_Referencias/referencias#Diffusion em workflows de agentes|Lu et al., 2026]]; [[06_Referencias/referencias#Constrained diffusion decoding|Mündler et al., 2025]].

### Uma única execução determinística
Se geração for determinística, repetições idênticas não acrescentam variância.

Mitigação:
- usar ampla quantidade de amostras;
- bootstrap por amostras para intervalos de confiança;
- quando houver estocasticidade inevitável, rodar seeds adicionais em subconjunto.

### Muitas métricas
Risco de cherry-picking.

Mitigação:
- declarar métricas primárias antes:
  1. State F1
  2. Preservation Accuracy
  3. Supersession Accuracy

---

## Validade de implementação

- testes unitários para parser;
- validação automática do schema;
- armazenar output bruto antes de qualquer reparo;
- não corrigir JSON silenciosamente;
- diferenciar `raw_valid_json` de `repaired_json`.
