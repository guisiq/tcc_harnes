using PdfParaEpubBilingue;
using System.Text.Json;

using var cancellation = new CancellationTokenSource();
Console.CancelKeyPress += (_, eventArgs) => { eventArgs.Cancel = true; cancellation.Cancel(); };
try
{
    if (args.Length == 0 || args.Contains("--help") || args.Contains("-h"))
    {
        CliArgs.PrintUsage();
        return args.Length == 0 ? 1 : 0;
    }
    if (args.SequenceEqual(new[] { "--install-browser" }))
        return Microsoft.Playwright.Program.Main(new[] { "install", "chromium" });
    if (args.SequenceEqual(new[] { "--models" }))
    {
        await using var client = new GitHub.Copilot.CopilotClient();
        var models = await client.ListModelsAsync();
        Console.WriteLine(JsonSerializer.Serialize(models));
        return 0;
    }
    if (args.Length == 2 && args[0] == "--validate")
    {
        var existing = Path.GetFullPath(args[1]);
        var validation = await EpubValidator.ValidateAsync(existing, Environment.GetEnvironmentVariable("EPUBCHECK_JAR"), existing + ".validation", cancellationToken: cancellation.Token);
        Console.WriteLine(JsonSerializer.Serialize(validation));
        return validation.Valid ? 0 : 3;
    }
    var cli = CliArgs.Parse(args) ?? throw new ArgumentException("Informe o PDF de entrada.");
    var source = Path.GetFullPath(cli.InputPdf);
    if (!File.Exists(source)) throw new FileNotFoundException("PDF nao encontrado.", source);
    var converter = cli.Formats.Any(format => format != "epub") ? KindleExporter.ResolveConverter(cli.Calibre) : null;
    if (cli.ExportOnly)
    {
        if (!source.EndsWith(".epub", StringComparison.OrdinalIgnoreCase) || cli.Output is not null || cli.ExtractOnly || cli.MaxPages.HasValue)
            throw new ArgumentException("--export-only requer um EPUB, sem --output, --extract-only ou --max-pages.");
        var checkedSource = await EpubValidator.ValidateAsync(source, cli.EpubCheckJar, source + ".validation", !cli.SkipTranslation, cancellation.Token);
        if (!checkedSource.Valid)
        {
            Console.WriteLine(JsonSerializer.Serialize(new { status = "validation_failed", report = checkedSource }));
            return 3;
        }
        var exported = converter is null ? [] : await KindleExporter.ExportAsync(source, cli.Formats, converter, cli.Force, Console.Error.WriteLine, cancellation.Token);
        Console.WriteLine(JsonSerializer.Serialize(new { status = "exported", source, exports = exported }));
        return 0;
    }
    if (!source.EndsWith(".pdf", StringComparison.OrdinalIgnoreCase)) throw new ArgumentException("A entrada deve ser PDF.");
    var suffix = cli.SkipTranslation ? "-original" : "-bilingue";
    if (cli.MaxPages.HasValue) suffix += "-amostra";
    var output = Path.GetFullPath(cli.Output ?? Path.Combine(Path.GetDirectoryName(source)!, Path.GetFileNameWithoutExtension(source) + suffix + ".epub"));
    if (!output.EndsWith(".epub", StringComparison.OrdinalIgnoreCase)) throw new ArgumentException("A saida deve terminar em .epub.");
    if (File.Exists(output) && !cli.Force) throw new IOException("Saida ja existe. Use --force para substituir.");
    if (!cli.Force && cli.Formats.Where(format => format != "epub").Any(format => File.Exists(Path.ChangeExtension(output, format))))
        throw new IOException("Uma exportacao solicitada ja existe. Use --force para substituir.");
    if (!cli.ExtractOnly && (cli.EpubCheckJar is null || !File.Exists(cli.EpubCheckJar)))
        throw new ArgumentException("Informe o EPUBCheck oficial via --epubcheck-jar ou EPUBCHECK_JAR antes da traducao.");
    var work = output + ".work";
    Directory.CreateDirectory(work);
    Console.Error.WriteLine($"Extraindo: {source}");
    var extraction = PdfExtractor.Extract(source, cli.MaxPages);
    if (extraction.Paragraphs.Count == 0) throw new InvalidDataException("PDF sem texto. OCR necessario; conversao interrompida.");
    await File.WriteAllTextAsync(Path.Combine(work, "source.json"), JsonSerializer.Serialize(extraction.Paragraphs, new JsonSerializerOptions { WriteIndented = true }), cancellation.Token);
    foreach (var image in extraction.Images)
        await File.WriteAllBytesAsync(Path.Combine(work, image.FileName), image.PngBytes, cancellation.Token);
    Console.Error.WriteLine($"{extraction.PageCount} paginas; {extraction.Paragraphs.Count} trechos; {extraction.Images.Count} paginas renderizadas.");
    if (cli.ExtractOnly)
    {
        Console.WriteLine(JsonSerializer.Serialize(new { status = "extracted", work, extraction.PageCount }));
        return 0;
    }
    Dictionary<(int Page, int Order), string> translations = new();
    Console.Error.WriteLine($"Organizando tabelas e figuras via {cli.Model}; texto e coordenadas serao enviados ao provedor.");
    extraction = await VisualLayoutOrganizer.OrganizeAsync(extraction, cli.Model, Path.Combine(work, "layout-cache"), Console.Error.WriteLine, cancellation.Token);
    await File.WriteAllTextAsync(Path.Combine(work, "reading-source.json"), JsonSerializer.Serialize(extraction.Paragraphs, new JsonSerializerOptions { WriteIndented = true }), cancellation.Token);
    await File.WriteAllTextAsync(Path.Combine(work, "visuals.json"), JsonSerializer.Serialize(extraction.Images.Select(image => new
    {
        image.PageNumber, image.Order, image.FileName, image.Kind, image.Caption, image.ExcludedOrders
    }), new JsonSerializerOptions { WriteIndented = true }), cancellation.Token);
    foreach (var image in extraction.Images)
        await File.WriteAllBytesAsync(Path.Combine(work, image.FileName), image.PngBytes, cancellation.Token);
    if (!cli.SkipTranslation)
    {
        Console.Error.WriteLine($"Tradução via Copilot/{cli.Model}; o texto sera enviado ao provedor e pode consumir cota.");
        translations = await new BilingualTranslator(cli.Model).TranslateAsync(extraction.Paragraphs,
            Console.Error.WriteLine, Path.Combine(work, "cache"), cancellation.Token);
    }
    await File.WriteAllTextAsync(Path.Combine(work, "bilingual.json"), JsonSerializer.Serialize(extraction.Paragraphs.Select(paragraph => new
    {
        page = paragraph.PageNumber, order = paragraph.Order, en = paragraph.Text,
        pt = translations.GetValueOrDefault((paragraph.PageNumber, paragraph.Order))
    }), new JsonSerializerOptions { WriteIndented = true }), cancellation.Token);
    var title = cli.Title ?? Path.GetFileNameWithoutExtension(source);
    if (cli.MaxPages.HasValue) title += $" (amostra: {extraction.PageCount} paginas)";
    var candidate = Path.Combine(work, "candidate.epub");
    EpubBuilder.Build(candidate, title, cli.Author ?? "Autor nao informado", extraction, translations, cli.SkipTranslation);
    Console.Error.WriteLine("Validando estrutura, EPUBCheck e layout em 6 combinacoes de tela/fonte...");
    var report = await EpubValidator.ValidateAsync(candidate, cli.EpubCheckJar, output + ".validation", !cli.SkipTranslation, cancellation.Token);
    if (!report.Valid)
    {
        Console.WriteLine(JsonSerializer.Serialize(new { status = "validation_failed", candidate, report }));
        return 3;
    }
    File.Move(candidate, output, cli.Force);
    var exports = converter is null ? [] : await KindleExporter.ExportAsync(output, cli.Formats, converter, cli.Force, Console.Error.WriteLine, cancellation.Token);
    Console.WriteLine(JsonSerializer.Serialize(new { status = "validated", output, model = cli.SkipTranslation ? null : cli.Model,
        layoutModel = cli.Model, pages = extraction.PageCount, pairs = translations.Count, images = extraction.Images.Count, exports, report = output + ".validation/validation.json" }));
    return 0;
}
catch (OperationCanceledException)
{
    Console.Error.WriteLine("Operacao cancelada ou timeout. Cache preservado; saida final nao publicada.");
    return 130;
}
catch (Exception exception)
{
    Console.Error.WriteLine(exception.Message);
    return exception is ArgumentException or FileNotFoundException ? 1 : 2;
}
