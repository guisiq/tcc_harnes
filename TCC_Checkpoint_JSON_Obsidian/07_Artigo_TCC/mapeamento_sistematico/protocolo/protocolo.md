# Protocolo do mapeamento sistemático (v2)

Versão legível do [`protocolo.json`](protocolo.json), que é a fonte usada pelos scripts. Alterações de critério
devem ser feitas no JSON e no [roteiro de triagem](roteiro_triagem.md), com nova pasta em `dados/`.

## 1. Objetivo e questões

Mapear estudos publicados entre **2025-07-01 e 2026-11-12** sobre escrita e atualização de memória por modelos de
linguagem, com foco em modelos compactos, estado estruturado (JSON) e geração por difusão.

- **QP1 — Representação e atualização:** como a memória é representada e como informações são incorporadas,
  preservadas, substituídas ou removidas?
- **QP2 — Modelos:** quais estudos usam modelos compactos para escrever/gerir memória e quais comparam geração
  autoregressiva e por difusão?
- **QP3 — Avaliação:** quais trabalhos inspecionam o estado após as atualizações e quais avaliam só a tarefa final?
- **QP4 — Posicionamento:** onde os estudos se aproximam ou se afastam do protocolo do TCC?

## 2. Calibração (QGS)

- 29 estudos conhecidos e relevantes (positivos), 213 exclusões da versão anterior (negativos) e 4 fundamentos.
- As strings foram ajustadas até recuperar o QGS na união das bases; `sensibilidade` registra, por string, o total
  na base e os acertos do QGS.

## 3. Fontes e strings

| Fonte | Acesso | Campo |
|---|---|---|
| OpenAlex | API `/works`, `title_and_abstract.search`, paginação integral | título + resumo, filtro de data |
| Semantic Scholar | API `paper/search/bulk` com *token* | título + resumo, filtro de data |
| *Snowballing* | Semantic Scholar: citações e referências de 13 sementes | janela de datas |

Facetas: S1 atualização de memória; S2 modelos compactos; S3 estado estruturado incremental; S4 geração estruturada;
S5 difusão em tarefas agênticas; S6 avaliação de memória. As strings completas estão em `strings_openalex` e
`strings_semantic_scholar` do JSON.

## 4. Seleção

1. **Deduplicação** por DOI e título normalizado; descarte fora da janela (E1).
2. **Pré-triagem por regras** (`Criterios` em `mapeamento.cs`): faixas *núcleo provável*, *contexto* e *excluído*.
3. **Leitura** de título e resumo de todo o núcleo, de todo o contexto e dos excluídos sem resumo cujo título casa
   `memor|forget|state|json|schema|diffusion|small language|slm`.
4. **Auditoria** de 200 excluídos por regra (amostra determinística), com intervalo de Wilson.

Inclusão (CORE): IC1 atualização de memória; IC2 escritor compacto (≤ ~4B); IC3 estado estruturado incremental;
IC4 geração estruturada por compactos ou difusão. Exclusão: E1–E9 (ver roteiro). Relevância 1–3 para CORE.

## 5. Triagem por LLM e custo

- Lotes embaralhados por SHA-256 com sementes fixas; QGS distribuído sem marcação (controles ocultos).
- 20 registros por bloco por padrão; uma sessão sem ferramentas por bloco, reutilizada por até três tentativas
  para completar as decisões. A saída é validada por esquema JSON; pendências fazem o comando retornar erro.
- Política de custo: somente modelos de menor preço por token; o teto de **1.000 créditos por pasta** acumula
  retomadas em `custo_llm.jsonl`. O script reserva pelo menos 30 créditos por sessão e repassa essa reserva ao
  servidor (`SessionLimits.MaxAiCredits`). Para várias pastas, somar os gastos e reduzir os limites das novas
  execuções para respeitar o teto global escolhido.

## 6. Extração e relatório

`relatorio` preenche [`../modelos/relatorio.md`](../modelos/relatorio.md): fluxo PRISMA, recuperação do QGS,
concordância regras × leitura, auditoria, Quadros 3–4 (CORE relevância 3 por interseção) e Apêndice A.
Os Quadros 1–2 (Nível 1, verificação integral) e a síntese crítica são texto curado no template.

## 7. Versionamento

- Snapshots das APIs e decisões são versionados por execução (`dados/execucao_<data>/`).
- Correções manuais de notas ficam em `relatorio.notas_revisadas` do JSON, nunca nos arquivos de decisão.
