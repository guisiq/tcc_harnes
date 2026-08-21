# Ficha preliminar do tema de TCC

## 1. Identificação

| Campo | Preenchimento |
| --- | --- |
| Aluno(a) | guilherme Henrique Siqueira Lopes |
| Curso / Semestre | Sistemas de Informação /7° periodo |
| Orientador(a) | Alex coelho A Confirma |
| Área | Inteligência Artificial; agentes baseados em modelos de linguagem; avaliação experimental |

## 2. Granularidade progressiva do tema

Cada nível acrescenta somente uma faceta principal. Assim, é possível visualizar como o tema e a pergunta são delimitados sem saltos grandes entre os recortes.

|  |  |  |  |
| --- | --- | --- | --- |
| Nível | Faceta acrescentada | Recorte resultante | Pergunta de pesquisa resultante |
| 0 — área | Área de interesse | Memória em sistemas de inteligência artificial. | Como a memória influencia sistemas de inteligência artificial? |
| 1 — objeto | Agentes baseados em modelos de linguagem | Memória em agentes baseados em modelos de linguagem. | Como a memória influencia o funcionamento de agentes baseados em modelos de linguagem? |
| 2 — fenômeno | Persistência de estado | Persistência de estado em agentes baseados em modelos de linguagem. | Em que medida a persistência de estado afeta o desempenho de agentes baseados em modelos de linguagem? |
| 3 — população | Pequenos modelos de linguagem | Persistência de estado em agentes baseados em pequenos modelos de linguagem. | Em que medida diferentes estratégias de persistência de estado afetam a confiabilidade e a eficiência de um agente baseado em SLM? |
|  |  |  |  |
| 5 — intervenções | Estratégias comparadas | Comparação entre histórico completo, janela deslizante, sumarização textual e checkpoint estruturado em JSON. | Como histórico completo, janela deslizante, sumarização textual e checkpoint estruturado afetam a confiabilidade e a eficiência de agentes baseados em SLMs locais? |
| 6 — situação de uso | Tarefas de múltiplas etapas | Estratégias de persistência em agentes locais que executam tarefas de múltiplas etapas. | Como essas estratégias afetam agentes baseados em SLMs locais durante tarefas de múltiplas etapas? |
| 7 — evento observado | Interrupção e retomada | Estratégias de persistência durante a retomada de tarefas de múltiplas etapas após interrupções controladas. | Em que medida essas estratégias afetam a retomada correta de tarefas interrompidas por agentes baseados em SLMs locais? |
| 8 — método | Experimento quantitativo controlado | Comparação experimental das estratégias, mantendo modelo, tarefas e pontos de interrupção constantes. | Qual é o efeito de cada estratégia sobre a retomada de tarefas quando as demais condições experimentais são mantidas constantes? |
| 9 — confiabilidade | Métricas de correção | Avaliação por sucesso final, retenção de restrições e ações duplicadas ou contraditórias. | Em que medida as estratégias diferem quanto ao sucesso final, à retenção de restrições e à ocorrência de ações inconsistentes após a retomada? |
| 10 — eficiência | Métricas de custo | Avaliação conjunta da confiabilidade, do consumo de tokens e da latência. | Qual estratégia apresenta a melhor relação entre confiabilidade, consumo de tokens e latência na retomada das tarefas? |
| 11 — viabilidade | SLM de 1–4B e hardware de consumo | Experimento com um SLM aberto de 1–4B, quantizado e executado em hardware local de consumo. | Em um SLM aberto de 1–4B executado localmente, qual estratégia de persistência oferece a melhor relação entre sucesso na retomada, preservação de restrições e custo computacional? |

## 3. Tema em uma frase

> **Avaliar estratégias de persistência de estado em agentes locais baseados em SLMs de 1–4B, durante a retomada de tarefas interrompidas, visando comparar sucesso final, retenção de restrições, consumo de tokens e latência.**

### Título provisório

**Persistência de estado em agentes baseados em pequenos modelos de linguagem: comparação entre histórico textual, sumarização e checkpoints estruturados**

Uma versão mais específica, caso o experimento confirme sua viabilidade, seria:

**Retomada de tarefas interrompidas por agentes locais baseados em SLMs: uma avaliação de histórico, sumarização e checkpoints em JSON**

## 4. Facetas selecionadas

| Faceta | Delimitação atual | Estado |
| --- | --- | --- |
| Objeto/Fenômeno | Efeito de estratégias externas de persistência de estado sobre agentes baseados em SLMs. | Definido |
| Contexto/Setor | Agentes locais que executam tarefas determinísticas de múltiplas etapas e precisam retomá-las depois de interrupções controladas. | Parcialmente definido |
| Público/População | Um SLM aberto, ajustado para instruções, entre 1B e 4B parâmetros, executado localmente. | Faixa definida; modelo pendente |
| Tempo | Literatura publicada principalmente entre 2023 e 2026; experimento durante o período do TCC. | Preliminar |
| Geografia | Não se aplica como população geográfica; o contexto técnico é hardware local de consumo. | Justificado |
| Dados/Fontes | Tarefas sintéticas e reproduzíveis, estados finais esperados, registros de execução e corpus bibliográfico. | Estrutura definida; tarefas pendentes |
| Método/Abordagem | Experimento quantitativo controlado, com ablação da estratégia de persistência e demais condições mantidas constantes. | Definido |
| Métricas/Variáveis | Sucesso final, sucesso após retomada, retenção de restrições, ações repetidas ou contraditórias, tokens e latência. | Definido |
| Restrições/Viabilidade | GPU com 6 GB de VRAM, 16 GB de RAM, sem treinamento completo, um modelo principal e conjunto limitado de tarefas. | Definido |

## 5. Variáveis do estudo

### Variável independente

Estratégia de persistência de estado:

1. histórico completo;
2. janela deslizante;
3. sumarização textual;
4. checkpoint estruturado em JSON.

O histórico completo funciona como linha de base. Se o orçamento do TCC precisar ser reduzido, a comparação principal poderá se concentrar em janela deslizante, sumarização e checkpoint JSON.

### Variáveis dependentes

- taxa de conclusão correta da tarefa;
- taxa de conclusão correta após interrupção e retomada;
- proporção de restrições preservadas;
- quantidade de ações duplicadas ou contraditórias;
- tokens processados por tarefa;
- latência total e latência de retomada;
- opcionalmente, uso máximo de RAM e VRAM.

### Variáveis de controle

- mesmo modelo e quantização;
- mesmo conjunto e ordem de tarefas;
- mesmos pontos de interrupção;
- mesmo limite de passos e chamadas;
- mesma configuração de geração;
- mesmo orçamento de contexto, quando metodologicamente aplicável;
- mesmo hardware e versão do ambiente.

## 6. Matriz de verificação objetiva

| Critério | Nota | Justificativa |
| --- | --- | --- |
| Relevância | 2 | Persistência de estado é necessária para agentes confiáveis e eficientes em tarefas com várias etapas. |
| Alinhamento | 2 | O estudo se relaciona a Sistemas de Informação, IA aplicada, Machine Learning e Modelagem Computacional do Conhecimento. |
| Viabilidade temporal | 2 | É factível se limitado a um modelo principal, três ou quatro estratégias e poucas famílias de tarefas. |
| Acesso a dados | 2 | As tarefas, interrupções, estados esperados e logs podem ser produzidos localmente de forma determinística. |
| Delimitação/Escopo | 1 | O fenômeno e as métricas estão delimitados, mas ainda faltam modelo, domínio e quantidade de tarefas. |
| Originalidade | 1 | O recorte em SLMs locais e retomada de tarefas é justificável, mas a lacuna precisa ser confirmada pela revisão focal. |
| **Total** | **10/12** | Atende provisoriamente à meta de pelo menos 9/12, sem notas zero. |

### Interpretação

O tema já tem granularidade suficiente para ser apresentado ao orientador como proposta. Ainda não deve ser tratado como formulação definitiva porque as notas de delimitação e originalidade dependem da revisão bibliográfica focal e do piloto.

## 7. Problema de pesquisa

Apesar de agentes baseados em modelos de linguagem precisarem manter um estado consistente para concluir tarefas de múltiplas etapas, estudos sobre memória de agentes frequentemente se concentram em memória conversacional, modelos maiores ou arquiteturas complexas. Ainda há evidência limitada — lacuna a ser confirmada pela revisão bibliográfica focal — sobre como estratégias simples de histórico textual, sumarização e checkpoints estruturados afetam a retomada de tarefas por SLMs de 1–4B executados localmente. Essa incerteza dificulta escolher mecanismos de persistência que conciliem confiabilidade e custo computacional em hardware de consumo.

### Evidências bibliográficas iniciais

- **MemGPT** demonstra o gerenciamento de diferentes camadas de memória e contexto para agentes.
- **LongMemEval** avalia capacidades de memória em interações longas e evidencia diferentes tipos de falha.
- **LoCoMo** aborda memória de longo prazo em conversações extensas.
- **MemoryAgentBench** e trabalhos sobre memória estrutural de agentes oferecem dimensões de avaliação e arquiteturas relacionadas.

Esses trabalhos fundamentam a relevância do fenômeno. Entretanto, não bastam, isoladamente, para provar a originalidade do recorte específico; isso será verificado na segunda passagem da revisão.

## 8. Pergunta de pesquisa

**Em que medida a estratégia de persistência de estado — histórico completo, janela deslizante, sumarização textual ou checkpoint estruturado em JSON — afeta a confiabilidade e a eficiência de agentes baseados em SLMs de 1–4B executados localmente na retomada de tarefas interrompidas?**

### Pergunta alternativa mais estreita

**Em agentes baseados em SLMs de 1–4B executados localmente, checkpoints estruturados em JSON reduzem a perda de restrições e o custo de contexto, quando comparados à sumarização textual e à janela deslizante, na retomada de tarefas interrompidas?**

A pergunta principal é mais adequada enquanto a revisão ainda está em andamento. A alternativa deve ser adotada somente se a literatura e o piloto indicarem que o checkpoint JSON é a comparação central mais promissora.

## 9. Objetivos

### Objetivo geral

**Avaliar** o efeito de estratégias de persistência de estado na confiabilidade e na eficiência de agentes baseados em SLMs locais durante a retomada de tarefas interrompidas.

### Objetivos específicos

1. **Selecionar** um SLM aberto de 1–4B compatível com o hardware disponível.
2. **Implementar** as estratégias de histórico completo, janela deslizante, sumarização textual e checkpoint estruturado em um harness experimental comum.
3. **Construir** um conjunto reproduzível de tarefas com estados esperados e pontos controlados de interrupção.
4. **Medir** conclusão, retomada, retenção de restrições, ações inconsistentes, tokens e latência.
5. **Comparar** o desempenho e o custo das estratégias sob condições equivalentes.
6. **Analisar** os padrões de falha e as ameaças à validade do experimento.
7. **Documentar** o protocolo, as configurações e os artefatos necessários à reprodução do estudo.

## 10. Hipóteses preliminares

As hipóteses servem para orientar o desenho, não como conclusões antecipadas:

- **H1:** checkpoints estruturados preservam mais restrições e estado operacional do que janela deslizante e sumarização textual.
- **H2:** sumarização textual reduz o consumo de contexto, mas introduz maior risco de omissão ou alteração de restrições.
- **H3:** janela deslizante apresenta baixo custo operacional, porém perde informações antigas quando a tarefa ultrapassa a janela disponível.
- **H4:** o benefício do checkpoint depende de como ele é produzido e validado; um checkpoint gerado pelo próprio SLM pode introduzir erros diferentes de um checkpoint atualizado deterministicamente pelo harness.

## 11. Desenho experimental mínimo viável

| Elemento | Proposta preliminar |
| --- | --- |
| Modelo | Um SLM aberto de 1–4B, quantizado, ajustado para instruções |
| Estratégias | Três ou quatro condições de persistência |
| Tarefas | Duas ou três famílias de tarefas determinísticas de múltiplas etapas |
| Interrupções | Pontos fixos, definidos previamente em cada tarefa |
| Referência correta | Estado final esperado e conjunto explícito de restrições |
| Repetições | A definir no piloto; usar o mesmo número por condição |
| Avaliação | Regras determinísticas e análise dos registros de execução |
| Análise | Diferenças de proporções, intervalos de confiança e comparação de custo |

## 12. Decisões ainda pendentes

Antes de fechar a ficha definitiva, é necessário decidir:

1. o modelo e a quantização exatos;
2. os domínios e a quantidade de tarefas;
3. se o checkpoint será atualizado por regras, pelo SLM ou por ambas as alternativas;
4. o orçamento de contexto comum às estratégias;
5. o número de repetições e os testes estatísticos;
6. o semestre e o cronograma oficial do TCC;
7. se o histórico completo permanecerá como condição experimental ou apenas como referência.

### Recomendação para o piloto

Começar com checkpoint atualizado deterministicamente pelo harness. Isso isola melhor o efeito do formato de persistência. A geração do checkpoint pelo próprio SLM pode ser uma condição adicional, caso haja tempo, porque mistura dois efeitos: persistência e qualidade da extração do estado.

## 13. Critérios para validar ou reformular o tema

O tema deve ser mantido se a revisão focal e o piloto confirmarem que:

- há poucos estudos que comparem diretamente essas estratégias em SLMs locais de 1–4B;
- as tarefas permitem medir estado e restrições de forma objetiva;
- o modelo escolhido executa as tarefas básicas com frequência suficiente para permitir comparação;
- as quatro condições cabem no cronograma e no hardware.

O tema deve ser estreitado se:

- houver estudos quase idênticos com o mesmo porte de modelo e protocolo;
- o número de condições tornar o experimento excessivo;
- a sumarização ou o histórico completo não forem comparáveis sob um orçamento justo.

Nesse caso, o recorte recomendado será comparar apenas **janela deslizante, sumarização textual e checkpoint estruturado**, com foco em **retenção de restrições após retomada**.

## 14. Papel do harness bibliográfico

O harness bibliográfico será um **instrumento de apoio** para buscar estudos, registrar evidências, validar a lacuna, escolher métricas e revisar decisões durante o projeto. Ele não integra o objeto experimental do TCC, a menos que o projeto seja posteriormente redirecionado para Harness Engineering.

## 15. Síntese para apresentação ao orientador

Pretende-se avaliar como diferentes estratégias de persistência de estado afetam agentes baseados em pequenos modelos de linguagem executados localmente. O experimento comparará histórico textual, janela deslizante, sumarização e checkpoints em JSON durante a retomada de tarefas interrompidas. A avaliação considerará sucesso final, retenção de restrições, ações inconsistentes, tokens e latência. A contribuição pretendida é produzir evidência controlada sobre alternativas simples de memória para agentes pequenos em hardware de consumo, recorte cuja originalidade ainda será confirmada por revisão focal da literatura.