using System.Text;
using System.Text.Json;
using RevisorArtigoTcc;

Console.OutputEncoding = Encoding.UTF8;
using var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => { e.Cancel = true; cts.Cancel(); };

var pdfPath = @"D:\repos\tcc_harnes\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins_corrigido (1).pdf";
var outputPath = @"D:\repos\tcc_harnes\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\observacoes_artigo_tcc.md";
var model = "mai-code-2-flash";
var batchSize = 10;
var concurrency = 4;
int? maxPages = null;
var deterministicOnly = false;
var docxPath = @"D:\repos\tcc_harnes\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins_corrigido (1).docx";
var commentedDocxPath = @"D:\repos\tcc_harnes\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins_corrigido (1)_comentado.docx";
var visualModel = "mai-code-2-flash";
var skipVisual = false;
var visualPagesPerBatch = 10;
var visualDpi = 150;
var diagramImage = @"c:\Users\lopes\AppData\Roaming\Code\agentSessionData\462f97c7-24f3-473a-bc50-e7d1b899960d\attachments\93d9ef48-f242-4494-8818-377182308e78\Pasted Image.png";

for (var i = 0; i < args.Length; i++)
{
    switch (args[i])
    {
        case "--pdf":
        case "-i":
            pdfPath = Path.GetFullPath(args[++i]);
            break;
        case "--output":
        case "-o":
            outputPath = Path.GetFullPath(args[++i]);
            break;
        case "--model":
        case "-m":
            model = args[++i];
            break;
        case "--batch-size":
            batchSize = int.Parse(args[++i]);
            break;
        case "--concurrency":
            concurrency = int.Parse(args[++i]);
            break;
        case "--max-pages":
            maxPages = int.Parse(args[++i]);
            break;
        case "--deterministic-only":
            deterministicOnly = true;
            break;
        case "--docx":
            docxPath = Path.GetFullPath(args[++i]);
            break;
        case "--comments-output":
            commentedDocxPath = Path.GetFullPath(args[++i]);
            break;
        case "--visual-model":
            visualModel = args[++i];
            break;
        case "--skip-visual":
            skipVisual = true;
            break;
        case "--visual-batch-size":
            visualPagesPerBatch = int.Parse(args[++i]);
            break;
        case "--visual-dpi":
            visualDpi = int.Parse(args[++i]);
            break;
        case "--diagram-image":
            diagramImage = Path.GetFullPath(args[++i]);
            break;
        case "--models":
        {
            await using var client = new GitHub.Copilot.CopilotClient();
            var models = await client.ListModelsAsync();
            Console.WriteLine(JsonSerializer.Serialize(models.Select(m => new { m.Id, m.Name }), new JsonSerializerOptions { WriteIndented = true }));
            return 0;
        }
        case "--help":
        case "-h":
            Console.WriteLine("""
                Uso: RevisorArtigoTcc [opções]
                  --pdf, -i <arquivo.pdf>       PDF do artigo TCC a analisar
                  --output, -o <arquivo.md>     Arquivo Markdown de observações de saída
                  --model, -m <modelo>          Modelo econômico do Copilot SDK (padrão: mai-code-2-flash; suporta mai-code-2)
                  --batch-size <N>              Itens por lote enviado ao modelo (padrão: 10)
                  --concurrency <N>             Sessões paralelas no Copilot SDK (padrão: 4)
                  --max-pages <N>               Limita às N primeiras páginas (opcional)
                  --deterministic-only          Executa apenas a auditoria determinística sem chamar LLM
                  --docx <arquivo.docx>         DOCX original usado para criar a cópia comentada
                  --comments-output <arquivo>   Caminho da cópia DOCX com comentários críticos
                  --visual-model <modelo>       Modelo com visão (padrão: mai-code-2-flash)
                  --visual-batch-size <N>       Páginas por lote visual (padrão: 10)
                  --visual-dpi <N>              Resolução do render (padrão: 150)
                  --diagram-image <arquivo.png> Diagrama de referência para comparar no lote visual
                  --skip-visual                 Não executar auditoria visual das páginas
                  --models                      Lista modelos disponíveis no Copilot SDK
                """);
            return 0;
    }
}

Console.Error.WriteLine($"[1/4] Extraindo parágrafos e estrutura de: {pdfPath}");
var extraction = PdfParagraphExtractor.Extract(pdfPath, maxPages);
Console.Error.WriteLine($"      Extraídos {extraction.Items.Count} itens em {extraction.PageCount} páginas ({extraction.Images.Count} imagens embutidas).");

Console.Error.WriteLine("[2/4] Executando auditoria determinística (Diagrama + Metodologia + Checklist TCC1)...");
var (itemAudits, citationAudit, visualAudits) = DeterministicAuditor.AuditDocument(extraction);
var detIssuesCount = itemAudits.Values.Sum(x => x.Issues.Count);
Console.Error.WriteLine($"      {detIssuesCount} apontamentos determinísticos detectados; {citationAudit.CitedInText.Count} citações cruzadas com {citationAudit.ListedInReferences.Count} referências.");

Dictionary<int, LlmParagraphObservation> llmResults = new();
var apiCalls = 0;
var cacheHits = 0;

if (!deterministicOnly)
{
    var cacheDir = Path.Combine(Path.GetDirectoryName(outputPath)!, ".revisor-cache");
    Console.Error.WriteLine($"[3/4] Executando análise parágrafo por parágrafo via GitHub Copilot SDK (modelo: {model}, lote: {batchSize}, concorrência: {concurrency})...");
    var analyzer = new CopilotParagraphAnalyzer(model, batchSize, concurrency);
    (llmResults, apiCalls, cacheHits) = await analyzer.AnalyzeAllAsync(
        extraction.Items,
        itemAudits,
        cacheDir,
        Console.Error.WriteLine,
        cts.Token);
}
else
{
    Console.Error.WriteLine("[3/4] Modo --deterministic-only ativo; pulando chamadas ao LLM.");
}

Console.Error.WriteLine($"[4/4] Consolidando observações e gerando relatório em: {outputPath}");
var combined = ReportGenerator.CombineObservations(extraction, itemAudits, llmResults);
var checklistEval = ReportGenerator.BuildChecklistEvaluation(combined, citationAudit, visualAudits);
var markdown = ReportGenerator.GenerateMarkdownReport(
    pdfPath,
    deterministicOnly ? "deterministic-only" : model,
    apiCalls,
    cacheHits,
    extraction,
    combined,
    citationAudit,
    visualAudits,
    checklistEval);

Directory.CreateDirectory(Path.GetDirectoryName(outputPath)!);
await File.WriteAllTextAsync(outputPath, markdown, new UTF8Encoding(false), cts.Token);

var jsonOutputPath = Path.ChangeExtension(outputPath, ".json");
var jsonPayload = new
{
    sourcePdf = pdfPath,
    model = deterministicOnly ? "deterministic-only" : model,
    apiCalls,
    cacheHits,
    pageCount = extraction.PageCount,
    totalItems = combined.Count,
    counts = new
    {
        ok = combined.Count(c => c.FinalStatus == "OK"),
        ajustar = combined.Count(c => c.FinalStatus == "AJUSTAR"),
        critico = combined.Count(c => c.FinalStatus == "CRITICO")
    },
    citationAudit,
    visualAudits,
    checklist = checklistEval,
    items = combined.Select(c => new
    {
        id = c.Item.Id,
        pageStart = c.Item.PageStart,
        pageEnd = c.Item.PageEnd,
        printedPage = c.Item.PrintedPage,
        section = c.Item.Section,
        kind = c.Item.Kind,
        wordCount = c.Deterministic.WordCount,
        maxSentenceWords = c.Deterministic.MaxSentenceWords,
        status = c.FinalStatus,
        codes = c.AllCodes,
        observation = c.ConsolidatedObservation,
        suggestion = c.ConsolidatedSuggestion,
        text = c.Item.Text
    })
};
await File.WriteAllTextAsync(
    jsonOutputPath,
    JsonSerializer.Serialize(jsonPayload, new JsonSerializerOptions { WriteIndented = true, Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping }),
    new UTF8Encoding(false),
    cts.Token);

CommentInsertionResult? commentInsertion = null;
if (File.Exists(docxPath))
{
    Console.Error.WriteLine($"[5/5] Criando cópia DOCX comentada: {commentedDocxPath}");
    commentInsertion = DocxCommentAdder.AddComments(
        docxPath,
        commentedDocxPath,
        jsonOutputPath,
        cts.Token);
    Console.Error.WriteLine(
        $"      Comentários críticos inseridos: {commentInsertion.CommentsAdded}; comentários já existentes preservados: {commentInsertion.ExistingCommentsPreserved}; ancoragens perdidas: {commentInsertion.Missed.Count}.");
}
else
{
    Console.Error.WriteLine($"DOCX não encontrado para comentários: {docxPath}");
}

VisualPageReport? visualReport = null;
if (!skipVisual)
{
    Console.Error.WriteLine(
        $"[Visual] Renderizando e analisando páginas com visão via modelo: {visualModel} ({visualDpi} dpi, {visualPagesPerBatch} páginas por lote)...");
    var visualAnalyzer = new VisualPageAnalyzer();
    visualReport = await visualAnalyzer.AnalyzeAsync(
        pdfPath,
        visualModel,
        Path.GetDirectoryName(outputPath)!,
        File.Exists(diagramImage) ? diagramImage : null,
        visualDpi,
        visualPagesPerBatch,
        cts.Token);
    var visualMarkdownPath = Path.Combine(Path.GetDirectoryName(outputPath)!,
        "observacoes_visuais_artigo_tcc.md");
    var visualMarkdown = await File.ReadAllTextAsync(visualMarkdownPath, cts.Token);
    markdown += "\n\n---\n\n## Auditoria Visual das Páginas Renderizadas\n\n" +
                visualMarkdown;
    await File.WriteAllTextAsync(outputPath, markdown, new UTF8Encoding(false), cts.Token);
    Console.Error.WriteLine(
        $"      Auditoria visual concluída: {visualReport.PageCount} páginas; {visualReport.ApiCalls} chamadas; {visualReport.CacheHits} cache hits.");
}

Console.WriteLine(JsonSerializer.Serialize(new
{
    status = "completed",
    outputMarkdown = outputPath,
    outputJson = jsonOutputPath,
    commentedDocx = commentInsertion?.Output,
    commentsAdded = commentInsertion?.CommentsAdded,
    missedCommentAnchors = commentInsertion?.Missed.Count,
    visualReport = visualReport is null ? null : Path.Combine(Path.GetDirectoryName(outputPath)!, "observacoes_visuais_artigo_tcc.json"),
    visualModel = visualReport?.Model,
    visualApiCalls = visualReport?.ApiCalls,
    visualCacheHits = visualReport?.CacheHits,
    model = deterministicOnly ? "deterministic-only" : model,
    apiCalls,
    cacheHits,
    totalItems = combined.Count,
    ok = combined.Count(c => c.FinalStatus == "OK"),
    ajustar = combined.Count(c => c.FinalStatus == "AJUSTAR"),
    critico = combined.Count(c => c.FinalStatus == "CRITICO")
}, new JsonSerializerOptions { WriteIndented = true }));

return 0;
