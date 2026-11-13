# Mapeamento sistemático reprodutível (2025-07-01 a 2026-11-12)

**Busca focada para o quadro do TCC:** [relatório e metodologia](../mapeamento_focado_trabalhos_relacionados_2025_2026.md),
[inventário](../mapeamento_focado_inventario_2025_2026.csv) e
[RIS para o Zotero](../mapeamento_focado_selecionados_2025_2026.ris).
O procedimento de reprodução está na seção [Busca focada](#busca-focada-para-o-quadro-de-trabalhos-relacionados).

## Versão ampla anterior

Pipeline que coleta, pré-tria, tria por LLM e gera o relatório
[`../mapeamento_sistematico_trabalhos_relacionados_2025_2026.md`](../mapeamento_sistematico_trabalhos_relacionados_2025_2026.md),
o inventário CSV e o RIS do Nível 2.

## Pré-requisitos

- .NET SDK 10 ou superior (scripts são *file-based apps*: `dotnet run arquivo.cs`).
- Somente para a triagem por LLM: GitHub Copilot CLI instalado e autenticado (`copilot --version`).
- Opcional: `OPENALEX_API_KEY` e `S2_API_KEY` para aumentar as cotas das APIs.

## Uso rápido

```powershell
# Reproduz a execução registrada sem rede nem LLM (pré-triagem, consolidação e relatório)
./executar.ps1 -Offline

# Nova execução completa em outra pasta de dados
./executar.ps1 -Dados dados/execucao_AAAA-MM-DD

# Apenas estimar o custo da triagem por LLM
./executar.ps1 -Dados dados/execucao_AAAA-MM-DD -SomenteEstimar
```

Para uma nova execução, atualize `data_execucao` e `janela.fim` em [`protocolo/protocolo.json`](protocolo/protocolo.json).

## Etapas (`scripts/mapeamento.cs`)

| Comando | Entrada | Saída |
|---|---|---|
| `calibrar` | QGS do protocolo | `calibracao.json.gz` |
| `sensibilidade` | strings S1–S6 | `sensibilidade.json` (totais e acertos do QGS por string) |
| `coletar-openalex` | strings OpenAlex | `openalex.json.gz` (paginação integral, retomável) |
| `coletar-s2` | strings S2 + sementes | `semanticscholar.json.gz` (busca *bulk* + *snowballing*) |
| `pretriar` | snapshots | `pretriagem.json.gz` (deduplicação, janela, regras) |
| `lotes` | pré-triagem | `lotes/*.jsonl`, `auditoria/lotes/auditoria.jsonl` |
| `consolidar` | `decisoes/*.jsonl` | `consolidado.json.gz` + controles do QGS |
| `relatorio` | consolidado + `modelos/relatorio.md` | Markdown, CSV, RIS e `estatisticas.json` |
| `offline` | — | `pretriar` + `consolidar` + `relatorio` |

Opções comuns: `--dados <pasta>`, `--protocolo <json>`, `--saida <pasta>` (padrão `..`), `--modelo <template>`.

## Triagem por LLM (`scripts/triagem.cs`)

Usa o GitHub Copilot SDK (`GitHub.Copilot.SDK` 1.0.31). Cada bloco abre uma sessão sem ferramentas,
com o [roteiro](protocolo/roteiro_triagem.md) como mensagem de sistema, e recebe 20 registros por padrão.
Até três chamadas na mesma sessão tentam completar as decisões faltantes do bloco. A resposta é validada
(chave, decisão, códigos e relevância) e gravada em `decisoes/llm_<lote>.jsonl`. Registros já decididos
em qualquer arquivo de `decisoes/` são ignorados, o que permite retomar a execução; pendências retornam erro.

**Controle de custo (obrigatório):**

- somente os modelos de **menor preço por token** (entrada + saída) listados por `ListModelsAsync`; `--modelo`
  só aceita um modelo desse nível (em 2026-11-12: `claude-haiku-5.5` e `gpt-6-luna`);
- **teto de 1.000 créditos por pasta de dados**, acumulado entre retomadas em `custo_llm.jsonl`; o script nunca
  aceita valor maior e `--limite-creditos` só pode reduzi-lo. Para várias pastas, some os gastos e reduza os
  limites das demais execuções para respeitar o teto global;
- antes de cada bloco são reservados pelo menos 30 créditos (mínimo aceito pelo servidor), ou três vezes a
  estimativa por requisição se maior. Esse limite por sessão é repassado em `SessionLimits.MaxAiCredits`;
  o gasto registrado é o maior entre o custo estimado por tokens e o `Cost` informado pelo SDK;
- `--estimar` apresenta uma estimativa com até três tentativas por bloco, sem chamar o modelo.

Outras opções: `--alvo principal|auditoria|ambos`, `--paralelo 1..4`, `--max-requisicoes N`.

## Estrutura

```
protocolo/       protocolo.json (máquina), protocolo.md (humano), roteiro_triagem.md (prompt de triagem)
modelos/         relatorio.md (template com placeholders {{NOME}})
scripts/         mapeamento.cs, triagem.cs
dados/execucao_2026-11-12/
  calibracao.json.gz, openalex.json.gz, semanticscholar.json.gz   snapshots das APIs (versionados)
  decisoes/lote_XX.jsonl                                           decisões da triagem por leitura
  auditoria/amostra.txt, auditoria/decisoes/auditoria.jsonl        amostra de 200 excluídos e decisões
  estatisticas.json                                                números usados no relatório
```

Arquivos derivados (`pretriagem.json.gz`, `consolidado.json.gz`, `lotes/`) não são versionados.

## Reprodutibilidade e limitações

- A coleta depende do estado das bases na data; por isso os snapshots são versionados e a reprodução oficial é o
  modo `-Offline`, que gera saídas idênticas byte a byte às da execução registrada.
- A triagem por LLM não é determinística; as decisões salvas são o registro auditável. Na execução de
  2026-11-12 a triagem foi feita por agentes do GitHub Copilot (modelo não registrado), sem avaliador humano;
  os controles ocultos do QGS e a auditoria de 200 excluídos medem sua confiabilidade.
- Apenas duas bases (OpenAlex e Semantic Scholar), complementadas por *snowballing*.

## Busca focada para o quadro de trabalhos relacionados

A execução focada é independente da v2 e produz uma tabela com as mesmas colunas
do Quadro 1 do artigo. Ela combina facetas já nas consultas e requer, na triagem,
atualização incremental de memória textual estruturada e ao menos uma dimensão
adicional de proximidade. Consulte o [protocolo focado](protocolo/protocolo_focado_estrito.json)
e o [roteiro de triagem](protocolo/roteiro_triagem_focado.md).

Em 12/11/2026, OpenAlex e Semantic Scholar retornaram HTTP 429 nas tentativas
de busca focada. A coleta efetiva desta execução foi realizada **somente na API
do arXiv**, e seus resultados não devem ser interpretados como cobertura de
todos os periódicos, anais ou preprints. A data usada é a do primeiro depósito
no arXiv, que pode ser diferente da publicação em anais.
Um piloto com a primeira versão das consultas está preservado separadamente em
`dados/execucao_focada_2026-11-12/`; sua consulta F3 era mais ampla. A execução
intermediária com F3 mais restrita, anterior à inclusão da consulta F6, está em
`dados/execucao_focada_ensaio_2026-11-12/`, com
[seu protocolo](protocolo/protocolo_focado_ensaio.json). A F6 foi acrescentada
para procurar estado tipado e modelos pequenos após inspecionar um estudo de
referência não recuperado; este refinamento é exploratório. A execução final está
em `dados/execucao_focada_estrita_2026-11-12/`.

Na revisão final, todos os CORE são examinados. Podem ser acrescentados
comparadores CONTEXT que avaliem paradigmas gerativos em memória de agentes ou
estado de planejamento revisável, desde que identificados e justificados
individualmente; também são permitidas correções justificadas da triagem inicial.
Esses comparadores não são apresentados como se satisfizessem os critérios CORE.

Na execução final, foram triados 158 títulos e resumos: 13 CORE, 91 CONTEXT
e 54 EXCLUDE. A revisão adicional cobre os 13 CORE e seis CONTEXT escolhidos
por proximidade, não todos os CONTEXT. Foram selecionados dez estudos:
oito do núcleo final (três eram CONTEXT corrigidos após consulta ao texto) e
dois comparadores. A verificação de textos integrais foi parcial e não houve
avaliador humano independente.

```powershell
# Reproduz a tabela, o CSV e o RIS salvos, sem rede e sem chamadas ao modelo.
dotnet run scripts\busca_focada.cs -- offline

# Para nova janela, copie o protocolo e edite a cópia, sem alterar o original.
Copy-Item protocolo\protocolo_focado_estrito.json protocolo\protocolo_focado_nova_execucao.json
# Edite inicio e fim em protocolo\protocolo_focado_nova_execucao.json.
dotnet run scripts\busca_focada.cs -- coletar --dados dados\nova_execucao --protocolo protocolo\protocolo_focado_nova_execucao.json

# Prévia de custo e triagem dos candidatos com o roteiro focado.
dotnet run scripts\triagem.cs -- --dados dados\nova_execucao --alvo principal --roteiro protocolo\roteiro_triagem_focado.md --por-requisicao 10 --paralelo 1 --limite-creditos 160 --estimar
dotnet run scripts\triagem.cs -- --dados dados\nova_execucao --alvo principal --roteiro protocolo\roteiro_triagem_focado.md --por-requisicao 10 --paralelo 1 --limite-creditos 160

# Após registrar a revisão de cada CORE em dados\nova_execucao\revisao_final.json:
dotnet run scripts\busca_focada.cs -- relatorio --dados dados\nova_execucao --protocolo protocolo\protocolo_focado_nova_execucao.json
```

O manifesto guarda o hash do protocolo, o total, a paginação e o hash de cada
resposta Atom; a reprodução falha se algum snapshot ou protocolo for alterado.
As decisões do modelo, o registro de custo e `revisao_final.json` são mantidos
com a execução. A revisão final registra inclusões e exclusões sem corte por
posição no ranking; os campos do quadro devem ser confirmados no texto integral.
Cada item da revisão tem `key`, `incluir` (booleano), `motivo` e `verificacao`
(`R` para título/resumo; `T` para trechos do texto integral). Para `T`, `fonte`
deve apontar ao HTML ou PDF da mesma versão do arXiv registrada no snapshot.
Para um estudo incluído, preencha `tipo` (`NUCLEO` ou `COMPARADOR`) e os campos
`representacao`, `atualizacao`, `modelos`, `avaliacao` e `paradigmas`.
Use a [revisão registrada](dados/execucao_focada_estrita_2026-11-12/revisao_final.json)
como exemplo. O script falha se uma decisão CORE, campo obrigatório ou
referência à versão verificada estiver faltando.

No piloto com a primeira versão das consultas, a triagem foi interrompida
após contabilizar 33 créditos e não alimenta a classificação final. O custo da
execução final foi de 16 créditos contabilizados em seu próprio
`custo_llm.jsonl`: total registrado entre as duas pastas, **49 créditos**.
Essa contabilização não substitui a consulta à fatura do serviço.

O RIS contém apenas os dez estudos selecionados, sem anexos de texto integral.
Sua geração não cria uma coleção no Zotero; o arquivo pode ser importado
manualmente. Confira nomes compostos ou institucionais após a importação.
