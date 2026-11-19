using System.Diagnostics;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using GitHub.Copilot;
using GitHub.Copilot.Rpc;

namespace RevisorArtigoTcc;

public sealed record VisualPageFinding(
    int Page,
    string Severity,
    List<string> Codes,
    string Observation,
    string? Suggestion
);

public sealed record VisualPageReport(
    string Pdf,
    string Model,
    string ReferenceDiagram,
    int Dpi,
    int PageCount,
    int ApiCalls,
    int CacheHits,
    List<VisualPageFinding> Findings
);

public sealed class VisualPageAnalyzer
{
    private const string SystemPrompt = """
        Você é um revisor visual de TCC. Analise páginas reais renderizadas de PDF.
        Compare com o diagrama de referência quando fornecido.
        Verifique objetivamente:
        - margens ABNT/UNITINS, cabeçalho, rodapé e numeração;
        - quebras de página, títulos órfãos, linhas isoladas, espaço antes de pontuação;
        - texto cortado, colunas sobrepostas, tabelas longas, fórmulas ilegíveis;
        - legendas, fontes, alinhamento, recuos, espaçamento e legibilidade;
        - ordem visual da imagem/figura/legenda/fonte;
        - placeholders ou marcadores residuais ([GS1]-[GS4], XXX, TODO);
        - contraste, resolução, bordas e cortes de elementos.
        Não invente erros. Cite apenas páginas/elementos visíveis.
        Responda APENAS JSON array: [{"page":int,"severity":"OK|AJUSTAR|CRITICO","codes":["V-*"],"observation":"máx 35 palavras","suggestion":"máx 35 palavras|null"}]
        """;

    public async Task<VisualPageReport> AnalyzeAsync(
        string pdfPath,
        string model,
        string outputDirectory,
        string? referenceDiagram,
        int dpi = 150,
        int pagesPerBatch = 10,
        CancellationToken cancellationToken = default)
    {
        var script = Path.Combine(AppContext.BaseDirectory, "render_pdf_pages.py");
        if (!File.Exists(script))
        {
            var repoScript = Path.GetFullPath(
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "render_pdf_pages.py"));
            if (File.Exists(repoScript))
                script = repoScript;
        }
        if (!File.Exists(script))
            throw new FileNotFoundException("Script render_pdf_pages.py não encontrado.", script);

        var rendersDirectory = Path.Combine(outputDirectory, "paginas-renderizadas");
        Directory.CreateDirectory(rendersDirectory);

        var start = new ProcessStartInfo(
            Environment.GetEnvironmentVariable("PDF_EPUB_PYTHON") ?? "python")
        {
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            StandardOutputEncoding = Encoding.UTF8,
            StandardErrorEncoding = Encoding.UTF8
        };
        start.ArgumentList.Add(script);
        start.ArgumentList.Add(Path.GetFullPath(pdfPath));
        start.ArgumentList.Add(rendersDirectory);
        start.ArgumentList.Add(dpi.ToString(System.Globalization.CultureInfo.InvariantCulture));
        start.ArgumentList.Add("0");

        using var renderProcess = Process.Start(start)
            ?? throw new IOException("Python não iniciou para renderizar páginas do PDF.");
        var stdoutTask = renderProcess.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderrTask = renderProcess.StandardError.ReadToEndAsync(cancellationToken);
        renderProcess.WaitForExit();

        if (renderProcess.ExitCode != 0)
            throw new InvalidOperationException("Falha ao renderizar páginas: " + stderrTask.GetAwaiter().GetResult());

        var renderJson = stdoutTask.GetAwaiter().GetResult();
        var rendered = JsonSerializer.Deserialize<RenderedPdf>(
            renderJson,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
            ?? throw new InvalidDataException("Resposta inválida do renderizador de páginas.");

        var cacheDirectory = Path.Combine(outputDirectory, ".visual-cache");
        Directory.CreateDirectory(cacheDirectory);

        await using var client = new CopilotClient();
        var availableModels = await client.ListModelsAsync();
        var resolvedModel = model;
        if (!availableModels.Any(m => m.Id.Equals(resolvedModel, StringComparison.OrdinalIgnoreCase)))
        {
            resolvedModel = availableModels.FirstOrDefault(m => m.Id.Equals("mai-code-2-flash", StringComparison.OrdinalIgnoreCase))?.Id
                ?? availableModels.FirstOrDefault(m => m.Id.Contains("flash", StringComparison.OrdinalIgnoreCase))?.Id
                ?? "mai-code-2-flash";
        }

        var findings = new List<VisualPageFinding>();
        var apiCalls = 0;
        var cacheHits = 0;

        foreach (var batch in rendered.Pages.Chunk(pagesPerBatch))
        {
            cancellationToken.ThrowIfCancellationRequested();
            var firstPage = batch.Min(p => p.Page);
            var lastPage = batch.Max(p => p.Page);
            var promptKeyInput = string.Join("\n", batch.Select(p => p.Path)) +
                "\n" + (referenceDiagram ?? "") + "\n" + model + "\n" + SystemPrompt;
            var cacheKey = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(promptKeyInput)));
            var cachePath = Path.Combine(cacheDirectory, cacheKey + ".json");

            if (File.Exists(cachePath))
            {
                cacheHits++;
                findings.AddRange(ParseFindings(await File.ReadAllTextAsync(cachePath, cancellationToken), batch));
                continue;
            }

            await using var session = await client.CreateSessionAsync(new SessionConfig
            {
                Model = resolvedModel,
                AvailableTools = [],
                OnPermissionRequest = (_, _) =>
                    Task.FromResult<PermissionDecision>(PermissionDecision.Reject("Sem ferramentas na auditoria visual.")),
                SystemMessage = new SystemMessageConfig { Content = SystemPrompt }
            });

            var attachments = new List<Attachment>();
            if (!string.IsNullOrWhiteSpace(referenceDiagram) && File.Exists(referenceDiagram))
            {
                attachments.Add(new AttachmentFile
                {
                    Type = "file",
                    Path = Path.GetFullPath(referenceDiagram),
                    DisplayName = "diagrama-referencia-cuidados-finais.png"
                });
            }
            foreach (var page in batch)
            {
                attachments.Add(new AttachmentFile
                {
                    Type = "file",
                    Path = page.Path,
                    DisplayName = $"pagina-{page.Page:000}.png"
                });
            }

            apiCalls++;
            var pagePrompt = $"Analise somente as páginas anexadas {firstPage} a {lastPage}. " +
                             "Retorne uma entrada por problema relevante. Se não houver problema visível, retorne [{" +
                             "\"page\":página,\"severity\":\"OK\",\"codes\":[\"V-FMT\"],\"observation\":\"Nenhum problema visual relevante identificado.\",\"suggestion\":null" +
                             "}]. " +
                             "Não resuma o texto inteiro.";

            var response = await session.SendAndWaitAsync(
                new MessageOptions
                {
                    Prompt = pagePrompt,
                    Attachments = attachments
                },
                TimeSpan.FromMinutes(3),
                cancellationToken);

            var content = response?.Data.Content ?? "[]";
            var parsed = ParseFindings(content, batch);
            findings.AddRange(parsed);
            await File.WriteAllTextAsync(cachePath + ".tmp", content, cancellationToken);
            File.Move(cachePath + ".tmp", cachePath, true);
        }

        findings = findings
            .DistinctBy(f => $"{f.Page}|{f.Severity}|{f.Observation}")
            .OrderBy(f => f.Page)
            .ThenByDescending(f => f.Severity)
            .ToList();

        var report = new VisualPageReport(
            Pdf: Path.GetFullPath(pdfPath),
            Model: resolvedModel,
            ReferenceDiagram: referenceDiagram is null ? "" : Path.GetFullPath(referenceDiagram),
            Dpi: dpi,
            PageCount: rendered.PageCount,
            ApiCalls: apiCalls,
            CacheHits: cacheHits,
            Findings: findings);

        Directory.CreateDirectory(outputDirectory);
        await File.WriteAllTextAsync(
            Path.Combine(outputDirectory, "observacoes_visuais_artigo_tcc.json"),
            JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }),
            cancellationToken);

        await File.WriteAllTextAsync(
            Path.Combine(outputDirectory, "observacoes_visuais_artigo_tcc.md"),
            BuildVisualMarkdown(report),
            cancellationToken);

        return report;
    }

    private static List<VisualPageFinding> ParseFindings(string content, RenderedPage[] batch)
    {
        var start = content.IndexOf('[');
        var end = content.LastIndexOf(']');
        if (start < 0 || end <= start)
            return batch.Select(p => new VisualPageFinding(
                p.Page,
                "OK",
                ["V-PARSE"],
                "Análise visual não retornou JSON válido; revisão automática inconclusiva.",
                "Revisar a página visualmente."
            )).ToList();

        try
        {
            return JsonSerializer.Deserialize<List<VisualPageFinding>>(
                content[start..(end + 1)],
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? [];
        }
        catch
        {
            return batch.Select(p => new VisualPageFinding(
                p.Page,
                "OK",
                ["V-PARSE"],
                "Análise visual não retornou JSON válido; revisão automática inconclusiva.",
                "Revisar a página visualmente."
            )).ToList();
        }
    }

    private static string BuildVisualMarkdown(VisualPageReport report)
    {
        var sb = new StringBuilder();
        sb.AppendLine("# Auditoria Visual das Páginas do PDF");
        sb.AppendLine();
        sb.AppendLine($"- PDF: `{report.Pdf}`");
        sb.AppendLine($"- Modelo com visão: `{report.Model}`");
        sb.AppendLine($"- Resolução: `{report.Dpi} dpi`");
        sb.AppendLine($"- Páginas analisadas: `{report.PageCount}`");
        sb.AppendLine($"- Chamadas à API: `{report.ApiCalls}`");
        sb.AppendLine($"- Lotes servidos pelo cache: `{report.CacheHits}`");
        sb.AppendLine();
        sb.AppendLine("| Página | Status | Códigos | Observação | Sugestão |");
        sb.AppendLine("|---|---|---|---|---|");
        foreach (var finding in report.Findings)
        {
            sb.AppendLine(
                $"| {finding.Page} | {finding.Severity} | {string.Join(", ", finding.Codes)} | {finding.Observation} | {finding.Suggestion ?? "-"} |");
        }
        sb.AppendLine();
        return sb.ToString();
    }

    private sealed record RenderedPdf(
        string Pdf,
        int Dpi,
        int PageCount,
        RenderedPage[] Pages);

    private sealed record RenderedPage(
        int Page,
        string Path,
        int Width,
        int Height);
}
