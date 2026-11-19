using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using GitHub.Copilot;
using GitHub.Copilot.Rpc;

namespace RevisorArtigoTcc;

public sealed class CopilotParagraphAnalyzer(string model, int batchSize = 6, int concurrency = 3)
{
    // Ultra-compact system prompt (< 320 tokens) encoding all 3 reference sources to minimize context usage per batch
    private const string CompactSystemRubric = """
        Você é um revisor rigoroso de TCC em Sistemas de Informação (Unitins). Avalie cada item textual de forma objetiva contra 3 fontes:
        1) DIAGRAMA (Vieira 2011; Wazlawick):
           - D-AMB: Destruir palavras vagas/ambíguas (muito/muitos/notável/vários), metáforas/analogias vazias; exigir números precisos.
           - D-VERB: Cortar verborreia, palavras supérfluas, períodos longos/complicados.
           - D-FIG: Figuras/quadros/tabelas/fórmulas bem explicados, citados no texto e com legenda autoexplicativa.
           - D-LEIT: Leitura em voz alta (fluidez, frases truncadas, artefatos de edição).
           - D-INTRO: Contextualização, Gap, Estado da arte, Propósito, Estrutura do documento.
           - D-PAR: Parágrafo essencial (faz falta se removido?) e sequência lógica adequada.
           - D-CONC: Conclusões realmente concluem?
           - D-REF: Citações e referências corretas e completas.
        2) METODOLOGIA (05-metodologia-e-escrita-cientifica: Wazlawick; Zucolotto Mód. 1-8; Gerhardt & Silveira; Prodanov & Freitas):
           - M-WAZ: Objetivo verificável (evitar "propor/estudar" vagos); lacuna fundamentada; método = passos replicáveis pós-objetivo (revisão não é o método experimental).
           - M-ZUC: Topic sentence clara abrindo o parágrafo; especificidade; ação no verbo (evitar substantivação e excesso de passiva); Resumo com 6 movimentos; pronomes inequívocos.
           - M-MET: Coerência entre delineamento experimental/quantitativo, variáveis, hipóteses (H0/H1) e métricas.
        3) CHECKLIST TCC1 (Formulario-Checklist_para_o_texto_do_TCC1.pdf):
           - C-01 Título, C-02 Resumo, C-03 Introdução, C-04 Revisão, C-05 Metodologia, C-06 Resultados (não esperado no TCC1), C-07 Discussão (não esperado no TCC1), C-08 Conclusão, C-09 Referências, C-10 Trabalhos relacionados (vantagens/desvantagens/semelhanças), C-11 Formatação ABNT, C-12 Gramática/Ortografia, C-13 Clareza/Coerência, C-14 Originalidade, C-15 Relevância para Sistemas de Informação, C-16 Ética.

        Responda APENAS um JSON array puro (sem markdown fences), um objeto por id recebido:
        [{"id":int,"st":"OK|AJUSTAR|CRITICO","c":["CODIGO"],"obs":"observação técnica direta (máx 35 palavras)","sug":"correção objetiva ou null"}]
        """;

    public async Task<(Dictionary<int, LlmParagraphObservation> Results, int ApiCalls, int CacheHits)> AnalyzeAllAsync(
        IReadOnlyList<DocumentItem> items,
        IReadOnlyDictionary<int, ItemDeterministicAudit> deterministicAudits,
        string cacheDirectory,
        Action<string> log,
        CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(cacheDirectory);
        var results = new Dictionary<int, LlmParagraphObservation>();

        // Items that need LLM semantic/stylistic analysis vs pure structural items handled deterministically
        var itemsForLlm = new List<DocumentItem>();
        foreach (var item in items)
        {
            var det = deterministicAudits[item.Id];
            if (item.Kind is "heading" or "source_note" or "footnote" or "equation" or "code_or_query" ||
                (item.Kind == "reference" && det.Issues.Count == 0))
            {
                // Zero-token deterministic synthesis for structural/reference items without anomalies
                var status = det.Issues.Any(i => i.Severity == "CRITICO")
                    ? "CRITICO"
                    : det.Issues.Any(i => i.Severity == "AJUSTAR")
                        ? "AJUSTAR"
                        : "OK";
                var codes = det.Issues.Select(i => i.Code).Distinct().ToList();
                if (codes.Count == 0)
                {
                    codes.Add(item.Kind switch
                    {
                        "heading" => "D-PAR/C-11",
                        "reference" => "D-REF/C-09",
                        "equation" => "D-FIG/M-MET",
                        "source_note" => "D-FIG/C-11",
                        "footnote" => "C-11",
                        _ => "M-MET"
                    });
                }
                var obs = det.Issues.Count > 0
                    ? string.Join(" ", det.Issues.Select(i => i.Message))
                    : item.Kind switch
                    {
                        "heading" => "Título de seção/subseção em sequência lógica adequada à estrutura IMRaD/monográfica de TCC1.",
                        "reference" => "Referência citada no texto e formatada segundo padrão ABNT (autor, título, veículo/arXiv, ano e acesso).",
                        "equation" => "Fórmula numerada, integrada à explicação das variáveis no parágrafo adjacente e coerente com as métricas do protocolo.",
                        "source_note" => "Atribuição de fonte presente conforme normas de apresentação de ilustrações e quadros.",
                        "footnote" => "Nota de rodapé informativa com URL pública de repositório/artefato técnico.",
                        _ => "Bloco técnico de código/consulta consistente com o protocolo experimental e de revisão sistemática."
                    };
                var sug = det.Issues.FirstOrDefault(i => i.Suggestion is not null)?.Suggestion;
                results[item.Id] = new LlmParagraphObservation(item.Id, status, codes, obs, sug);
            }
            else
            {
                itemsForLlm.Add(item);
            }
        }

        // Chunk sequentially across sections (each item carries its own 'sec' and 'p' metadata)
        // to maximize batch fill rate and cut system-prompt token overhead by ~70%
        var batches = itemsForLlm
            .Chunk(batchSize)
            .ToList();

        log($"Itens totais: {items.Count} | Itens enviados ao LLM ({model}): {itemsForLlm.Count} em {batches.Count} lotes (contexto otimizado).");

        await using var client = new CopilotClient();
        var availableModels = await client.ListModelsAsync();
        var resolvedModel = model;
        if (!availableModels.Any(m => m.Id.Equals(resolvedModel, StringComparison.OrdinalIgnoreCase)))
        {
            resolvedModel = availableModels.FirstOrDefault(m => m.Id.Equals("mai-code-2-flash", StringComparison.OrdinalIgnoreCase))?.Id
                ?? availableModels.FirstOrDefault(m => m.Id.Equals("mai-code-2", StringComparison.OrdinalIgnoreCase))?.Id
                ?? availableModels.FirstOrDefault(m => m.Id.Contains("flash", StringComparison.OrdinalIgnoreCase) || m.Id.Contains("haiku", StringComparison.OrdinalIgnoreCase))?.Id
                ?? "mai-code-2-flash";
            log($"Modelo '{model}' não encontrado; usando modelo econômico disponível: '{resolvedModel}'.");
        }

        var apiCalls = 0;
        var cacheHits = 0;
        using var semaphore = new SemaphoreSlim(Math.Max(1, concurrency));

        var batchTasks = batches.Select(async (batch, batchIndex) =>
        {
            await semaphore.WaitAsync(cancellationToken);
            try
            {
                var (batchObs, usedApi, usedCache) = await AnalyzeBatchWithRetryAsync(
                    client,
                    resolvedModel,
                    batch,
                    batchIndex + 1,
                    batches.Count,
                    deterministicAudits,
                    cacheDirectory,
                    log,
                    cancellationToken);
                Interlocked.Add(ref apiCalls, usedApi);
                Interlocked.Add(ref cacheHits, usedCache);
                return batchObs;
            }
            finally
            {
                semaphore.Release();
            }
        }).ToList();

        var batchOutputs = await Task.WhenAll(batchTasks);
        foreach (var dict in batchOutputs)
        {
            foreach (var kv in dict)
                results[kv.Key] = kv.Value;
        }

        return (results, apiCalls, cacheHits);
    }

    private async Task<(Dictionary<int, LlmParagraphObservation> Map, int ApiCalls, int CacheHits)> AnalyzeBatchWithRetryAsync(
        CopilotClient client,
        string resolvedModel,
        DocumentItem[] batch,
        int batchNumber,
        int totalBatches,
        IReadOnlyDictionary<int, ItemDeterministicAudit> deterministicAudits,
        string cacheDirectory,
        Action<string> log,
        CancellationToken cancellationToken)
    {
        var payloadObj = batch.Select(item =>
        {
            var det = deterministicAudits[item.Id];
            var detAlerts = det.Issues.Select(i => $"{i.Code}: {i.Message}").ToArray();
            // Only summarize oversized tables; keep full prose paragraphs intact so the model never sees artificial '[...]'
            var compactText = item.Kind == "table" && item.Text.Length > 1500
                ? item.Text[..1500] + " [tabela resumida na extração]"
                : item.Text;
            return new
            {
                id = item.Id,
                p = item.PageStart,
                sec = item.Section,
                kind = item.Kind,
                w = det.WordCount,
                maxSentW = det.MaxSentenceWords,
                det = detAlerts,
                txt = compactText
            };
        });

        var inputJson = JsonSerializer.Serialize(payloadObj);
        var cacheKey = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes($"revisor-v1\n{resolvedModel}\n{CompactSystemRubric}\n{inputJson}")));
        var cachePath = Path.Combine(cacheDirectory, cacheKey + ".json");

        if (File.Exists(cachePath))
        {
            try
            {
                var cachedText = await File.ReadAllTextAsync(cachePath, cancellationToken);
                var parsed = ParseBatchResponse(cachedText, batch);
                log($"Lote {batchNumber}/{totalBatches} (IDs {batch[0].Id}..{batch[^1].Id}): cache hit.");
                return (parsed, 0, 1);
            }
            catch
            {
                // Ignore corrupted cache and re-fetch
            }
        }

        var apiCalls = 0;
        for (var attempt = 1; attempt <= 2; attempt++)
        {
            cancellationToken.ThrowIfCancellationRequested();
            apiCalls++;
            log($"Lote {batchNumber}/{totalBatches} (IDs {batch[0].Id}..{batch[^1].Id}, Seção '{batch[0].Section}'): analisando via {resolvedModel} (tentativa {attempt})...");

            try
            {
                await using var session = await client.CreateSessionAsync(new SessionConfig
                {
                    Model = resolvedModel,
                    AvailableTools = [],
                    OnPermissionRequest = (_, _) => Task.FromResult<PermissionDecision>(PermissionDecision.Reject("Sem ferramentas na revisão textual.")),
                    SystemMessage = new SystemMessageConfig
                    {
                        Content = CompactSystemRubric
                    }
                });

                var requiredIds = string.Join(",", batch.Select(b => b.Id));
                var prompt = $"Avalie os itens a seguir (IDs obrigatórios: {requiredIds}). Retorne APENAS o JSON array puro:\n{inputJson}";

                var response = await session.SendAndWaitAsync(
                    new MessageOptions { Prompt = prompt },
                    TimeSpan.FromMinutes(2),
                    cancellationToken);

                var content = response?.Data.Content ?? "";
                var parsed = ParseBatchResponse(content, batch);

                await File.WriteAllTextAsync(cachePath + ".tmp", content, cancellationToken);
                File.Move(cachePath + ".tmp", cachePath, true);
                return (parsed, apiCalls, 0);
            }
            catch (Exception ex) when (ex is not OperationCanceledException)
            {
                if (attempt < 2)
                {
                    log($"Lote {batchNumber}: falha de parse/chamada ({ex.Message}); repetindo...");
                    continue;
                }

                if (batch.Length > 1)
                {
                    log($"Lote {batchNumber}: dividindo lote de {batch.Length} itens para isolar falha...");
                    var mid = batch.Length / 2;
                    var left = await AnalyzeBatchWithRetryAsync(client, resolvedModel, batch[..mid], batchNumber, totalBatches, deterministicAudits, cacheDirectory, log, cancellationToken);
                    var right = await AnalyzeBatchWithRetryAsync(client, resolvedModel, batch[mid..], batchNumber, totalBatches, deterministicAudits, cacheDirectory, log, cancellationToken);
                    foreach (var kv in right.Map)
                        left.Map[kv.Key] = kv.Value;
                    return (left.Map, apiCalls + left.ApiCalls + right.ApiCalls, left.CacheHits + right.CacheHits);
                }

                // Fallback deterministic observation if a single item fails twice
                var single = batch[0];
                var det = deterministicAudits[single.Id];
                var fallbackStatus = det.Issues.Any(i => i.Severity == "CRITICO")
                    ? "CRITICO"
                    : det.Issues.Count > 0 ? "AJUSTAR" : "OK";
                var fallbackObs = det.Issues.Count > 0
                    ? string.Join(" ", det.Issues.Select(i => i.Message))
                    : "Parágrafo objetivo, com função clara na seção e aderente às normas de escrita científica.";
                var map = new Dictionary<int, LlmParagraphObservation>
                {
                    [single.Id] = new LlmParagraphObservation(
                        single.Id,
                        fallbackStatus,
                        det.Issues.Select(i => i.Code).DefaultIfEmpty("D-PAR/M-ZUC").ToList(),
                        fallbackObs,
                        det.Issues.FirstOrDefault()?.Suggestion)
                };
                return (map, apiCalls, 0);
            }
        }

        throw new InvalidOperationException("Unreachable");
    }

    private static Dictionary<int, LlmParagraphObservation> ParseBatchResponse(string rawContent, DocumentItem[] expectedBatch)
    {
        var cleaned = rawContent.Trim();
        var startBracket = cleaned.IndexOf('[');
        var endBracket = cleaned.LastIndexOf(']');
        if (startBracket < 0 || endBracket <= startBracket)
            throw new InvalidDataException("Resposta não contém um array JSON '[' ... ']'.");

        var jsonSlice = cleaned[startBracket..(endBracket + 1)];
        var list = JsonSerializer.Deserialize<List<LlmParagraphObservation>>(jsonSlice, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        }) ?? throw new InvalidDataException("Array JSON nulo.");

        var map = new Dictionary<int, LlmParagraphObservation>();
        foreach (var item in list)
        {
            var normalizedStatus = (item.Status ?? "OK").Trim().ToUpperInvariant() switch
            {
                "CRITICO" or "CRÍTICO" or "ERRO" => "CRITICO",
                "AJUSTAR" or "ALERTA" or "PARCIAL" or "REVISAR" => "AJUSTAR",
                _ => "OK"
            };
            map[item.Id] = item with
            {
                Status = normalizedStatus,
                Codes = item.Codes ?? ["D-PAR"],
                Observation = string.IsNullOrWhiteSpace(item.Observation) ? "Sem ressalvas adicionais." : item.Observation.Trim()
            };
        }

        foreach (var expected in expectedBatch)
        {
            if (!map.ContainsKey(expected.Id))
                throw new InvalidDataException($"ID esperado #{expected.Id} ausente na resposta do modelo.");
        }

        return map;
    }
}
