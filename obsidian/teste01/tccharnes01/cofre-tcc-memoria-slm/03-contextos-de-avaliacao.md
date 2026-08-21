---
tags:
  - tcc
  - tarefas
  - avaliacao
---

# Contextos de avaliação selecionados

## 3A — Tarefas sintéticas e determinísticas

São tarefas criadas especificamente para o experimento, com entrada, regras, restrições, pontos de interrupção e estado final esperado definidos previamente.

### Exemplo

Um agente deve montar uma solicitação com campos obrigatórios, respeitar um limite de orçamento e executar uma sequência de ferramentas. O avaliador conhece o estado correto em cada etapa.

### Vantagens

- avaliação automática;
- repetibilidade;
- controle sobre dificuldade e tamanho;
- injeção de interrupções idênticas;
- possibilidade de atribuir cada falha a um campo ou regra.

### Limitação

Resultados em tarefas sintéticas não garantem o mesmo comportamento em situações reais. Essa ameaça deve ser reconhecida como limitação de validade externa.

## 3C — Fluxos transacionais

São processos nos quais o agente coleta dados e modifica um estado estruturado, como:

- cadastro de usuário;
- reserva de horário;
- solicitação de serviço;
- pedido com itens e limites;
- abertura de chamado.

Esses fluxos são adequados porque possuem campos, restrições e estados finais verificáveis. Também permitem detectar repetição de ações, perda de confirmações e alteração indevida de valores.

### Exemplo de estado

```json
{
  "cliente": "Pessoa A",
  "servico": "atendimento técnico",
  "data": "2026-09-14",
  "orcamento_maximo": 300,
  "status": "aguardando confirmação"
}
```

## 3D — Conversações longas

Distribuem fatos, preferências e decisões ao longo de muitas mensagens. O agente precisa recuperar informações antigas quando elas voltam a ser relevantes.

### O que esse contexto mede

- recuperação temporal;
- manutenção de preferências;
- consistência entre informações antigas e recentes;
- resistência a fatos irrelevantes ou contraditórios.

### Diferença em relação aos fluxos transacionais

Fluxos transacionais têm schema e estado final bem definidos. Conversações longas contêm informação aberta e são mais difíceis de avaliar deterministicamente.

Para um TCC simples, 3D deve ser tratado como **domínio alternativo ou extensão**, não necessariamente combinado com 3C no experimento principal.

## 3E — Execução local com SLM de 1–4B

O estudo será realizado com um modelo pequeno, aberto e quantizado, executado em hardware de consumo.

### Consequências metodológicas

- usar um modelo principal para evitar uma matriz experimental excessiva;
- registrar versão, quantização, contexto máximo e parâmetros de geração;
- evitar treinamento completo;
- medir latência, tokens, RAM e VRAM;
- manter temperatura e limites de geração constantes entre condições.

### Justificativa do recorte

Modelos pequenos apresentam limitações diferentes das observadas em modelos maiores. Um mecanismo externo de estado pode compensar parte dessas limitações, mas também pode aumentar custo e introduzir novos erros.

Termos relacionados: [[05-glossario#SLM]], [[05-glossario#Quantização]], [[05-glossario#Hardware de consumo]].

## Escolha de domínio recomendada

Para o experimento mínimo, usar **3A + 3C + 3E**:

- tarefas sintéticas;
- formato transacional;
- um SLM local.

Manter 3D como extensão ou como segunda família pequena de tarefas, caso haja tempo.

