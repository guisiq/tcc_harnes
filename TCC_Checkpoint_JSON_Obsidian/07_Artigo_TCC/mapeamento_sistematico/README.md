# Mapeamento sistemático reprodutível (2025-07-01 a 2026-11-12)

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

Usa o GitHub Copilot SDK (`GitHub.Copilot.SDK` 1.0.31). Cada requisição abre uma sessão nova, sem ferramentas,
com o [roteiro](protocolo/roteiro_triagem.md) como mensagem de sistema, e recebe 20 registros. A resposta é
validada (chave, decisão, códigos e relevância) e gravada em `decisoes/llm_<lote>.jsonl`. Registros já decididos
em qualquer arquivo de `decisoes/` são ignorados, o que permite retomar a execução.

**Controle de custo (obrigatório):**

- somente os modelos de **menor preço por token** (entrada + saída) listados por `ListModelsAsync`; `--modelo`
  só aceita um modelo desse nível (em 2026-11-12: `claude-haiku-5.5` e `gpt-6-luna`);
- **teto de 1.000 créditos** acumulado entre execuções em `custo_llm.jsonl` (o script nunca aceita valor maior;
  `--limite-creditos` só pode reduzi-lo). Cada requisição reserva sua estimativa antes do envio e contabiliza o
  maior valor entre o custo por tokens e o `Cost` informado pelo SDK;
- o crédito restante é repassado ao servidor em `SessionLimits.MaxAiCredits`;
- `--estimar` mostra o custo previsto sem chamar o modelo. Triar do zero os 2.787 registros (lotes + auditoria)
  foi estimado em cerca de 154 créditos.

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
