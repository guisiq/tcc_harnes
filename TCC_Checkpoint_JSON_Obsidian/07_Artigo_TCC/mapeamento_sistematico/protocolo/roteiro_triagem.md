# Roteiro de triagem por título e resumo (v2)

Decida cada registro com base SOMENTE no título e no resumo fornecidos.

## Critérios gerais (todos obrigatórios para CORE ou CONTEXT)
- G1: estudo baseado em modelos de linguagem (LLM, SLM, dLLM) ou agentes baseados neles.
- G2: estudo primário (propõe método/sistema, benchmark ou avaliação empírica). Surveys, revisões, posições, tutoriais e visões → EXCLUDE (E3).
- G3: o objeto é memória/estado TEXTUAL de LMs ou geração estruturada textual.

## Critérios do núcleo (CORE exige ≥1)
- IC1 Atualização de memória: propõe, analisa ou avalia como a memória/estado persistente de um LM/agente é ESCRITO, ATUALIZADO, REVISADO, CONSOLIDADO, SUBSTITUÍDO, RESOLVE CONFLITOS ou ESQUECE (não basta armazenar e recuperar).
- IC2 Escritor compacto: modelo de até ~4B parâmetros (SLM) escreve, extrai, atualiza ou gerencia memória.
- IC3 Estado estruturado incremental: memória/estado com estrutura explícita (JSON, esquema, entidades/atributos, tabela, registros tipados, grafo de entidades/fatos) mantida ao longo de múltiplas entradas, turnos ou sessões; inclui sumarização incremental de entidades.
- IC4 Geração estruturada por compactos ou difusão: geração JSON/esquema/chamadas de ferramenta por SLMs ou modelos de difusão de linguagem, ou comparação autoregressivo × difusão em tarefas agênticas/estruturadas.

## CONTEXT (memória de agentes LM, mas sem satisfazer IC1–IC4)
Ex.: foco em recuperação/RAG/uso da memória; arquitetura geral sem foco na escrita/atualização; memória procedural/de experiências/habilidades; benchmarks de recordação/QA de longo prazo sem medir atualização.

## Exclusão (EXCLUDE)
- E2 memória no sentido computacional (KV cache, GPU/VRAM, quantização, eficiência de memória de treino/inferência, hardware).
- E3 estudo secundário (survey, revisão, posição, tutorial, visão).
- E4 modalidade não textual como objeto principal (vídeo, imagem, GUI, robótica, condução, áudio, embodied).
- E5 foco principal em segurança, privacidade, ataques, envenenamento, unlearning.
- E6 aplicação de domínio em que LM/memória é apenas ferramenta, sem contribuição para as questões acima.
- E8 informação insuficiente para decidir (sem resumo e título não decisivo).
- E9 fora do tema (não trata de memória/estado de LMs nem de geração estruturada).

## Relevância (somente CORE)
- 3: diretamente comparável ao TCC — avalia a fidelidade/correção do estado após atualizações, OU usa SLM como escritor/gestor de memória com avaliação, OU estado estruturado (JSON/entidades) atualizado incrementalmente, OU compara paradigmas gerativos (difusão × autoregressivo) em geração estruturada.
- 2: responde diretamente a uma questão (IC) mas com tarefa/medida distante.
- 1: tangencial (atende o IC apenas de modo secundário).

Em caso de dúvida entre CORE e CONTEXT, prefira CORE com relevância 1 (inclusão conservadora).

## Saída
Para CADA registro recebido, devolva exatamente um item com:
- `key`: a chave do registro, copiada sem alteração;
- `decision`: `CORE`, `CONTEXT` ou `EXCLUDE`;
- `codes`: códigos IC1–IC4 atendidos (CORE) ou o código de exclusão principal (EXCLUDE); lista vazia para CONTEXT;
- `relevance`: 1, 2 ou 3 para CORE; 0 nos demais casos;
- `note`: justificativa em português, com no máximo 160 caracteres, descrevendo a contribuição e a aproximação com o TCC.

Não invente informações ausentes do título ou do resumo.
