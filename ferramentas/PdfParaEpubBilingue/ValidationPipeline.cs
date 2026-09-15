using System.Diagnostics;
using System.IO.Compression;
using System.Text.Json;
using System.Xml;
using System.Xml.Linq;
using Microsoft.Playwright;
using SkiaSharp;

namespace PdfParaEpubBilingue;

public sealed record ValidationReport(bool Valid, List<string> Issues, int? EpubCheckExitCode, List<JsonElement> LayoutChecks);

public static class EpubValidator
{
    public static List<string> CheckStructure(string path, bool bilingual = true)
    {
        var issues = new List<string>();
        try
        {
            using var archive = ZipFile.OpenRead(path);
            var mime = archive.Entries.FirstOrDefault();
            if (mime?.FullName != "mimetype" || Read(mime) != "application/epub+zip")
                issues.Add("Primeira entrada deve ser mimetype com application/epub+zip.");
            using (var binary = new BinaryReader(File.OpenRead(path)))
            {
                binary.BaseStream.Position = 8;
                if (binary.ReadUInt16() != 0) issues.Add("mimetype deve estar sem compressao.");
            }
            foreach (var name in new[] { "META-INF/container.xml", "OEBPS/content.opf", "OEBPS/toc.ncx", "OEBPS/chapter.xhtml" })
            {
                var entry = archive.GetEntry(name) ?? throw new InvalidDataException($"Entrada ausente: {name}");
                using var reader = XmlReader.Create(entry.Open(), new XmlReaderSettings { DtdProcessing = DtdProcessing.Ignore, XmlResolver = null });
                var xml = XDocument.Load(reader);
                foreach (var attribute in xml.Descendants().Attributes().Where(attribute => attribute.Name.LocalName is "src" or "href"))
                {
                    var reference = Uri.UnescapeDataString(attribute.Value.Split('#')[0]);
                    if (string.IsNullOrEmpty(reference)) continue;
                    if (Uri.TryCreate(reference, UriKind.Absolute, out _))
                        issues.Add($"Recurso externo nao permitido: {reference}");
                    else if (archive.GetEntry("OEBPS/" + reference) is null)
                        issues.Add($"Recurso ausente: {reference}");
                }
                if (name.EndsWith("chapter.xhtml"))
                {
                    XNamespace html = "http://www.w3.org/1999/xhtml";
                    var pairs = xml.Descendants(html + "div").Where(element => (string?)element.Attribute("class") == "bilingual").ToList();
                    if (pairs.Count == 0) issues.Add("Nenhum trecho de leitura encontrado.");
                    foreach (var pair in pairs)
                    {
                        var text = pair.Elements(html + "p").ToArray();
                        if (text.Length != (bilingual ? 2 : 1) || text.Any(element => string.IsNullOrWhiteSpace(element.Value)))
                            issues.Add("Par de idiomas vazio ou incompleto.");
                        else if ((string?)text[0].Attribute(XNamespace.Xml + "lang") != "en" ||
                            (bilingual && (string?)text[1].Attribute(XNamespace.Xml + "lang") != "pt-BR"))
                            issues.Add("Ordem esperada: en, depois pt-BR.");
                    }
                }
            }
            foreach (var image in archive.Entries.Where(entry => entry.FullName.EndsWith(".png")))
            {
                using var bitmap = SKBitmap.Decode(image.Open());
                if (bitmap is null || bitmap.Width < 10 || bitmap.Height < 10)
                    issues.Add($"Imagem invalida: {image.FullName}");
                else
                {
                    var colors = new HashSet<uint>();
                    for (var row = 0; row < bitmap.Height; row += Math.Max(1, bitmap.Height / 150))
                    for (var column = 0; column < bitmap.Width; column += Math.Max(1, bitmap.Width / 150))
                        colors.Add((uint)bitmap.GetPixel(column, row));
                    if (colors.Count < 2) issues.Add($"Imagem aparentemente em branco: {image.FullName}");
                }
            }
        }
        catch (Exception exception) when (exception is InvalidDataException or XmlException or IOException)
        {
            issues.Add(exception.Message);
        }
        return issues;
    }

    public static async Task<ValidationReport> ValidateAsync(string epub, string? jar, string reportDirectory,
        bool bilingual = true, CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(reportDirectory);
        var issues = CheckStructure(epub, bilingual);
        int? checkExit = null;
        var layouts = new List<JsonElement>();
        if (jar is null || !File.Exists(jar))
            issues.Add("EPUBCheck nao executado: informe --epubcheck-jar ou EPUBCHECK_JAR.");
        else
        {
            var start = new ProcessStartInfo("java") { UseShellExecute = false, RedirectStandardOutput = true, RedirectStandardError = true };
            foreach (var argument in new[] { "-jar", Path.GetFullPath(jar), Path.GetFullPath(epub), "--json", Path.Combine(reportDirectory, "epubcheck.json") })
                start.ArgumentList.Add(argument);
            try
            {
                using var process = Process.Start(start) ?? throw new IOException("Nao foi possivel iniciar Java.");
                var stdout = process.StandardOutput.ReadToEndAsync(cancellationToken);
                var stderr = process.StandardError.ReadToEndAsync(cancellationToken);
                using var timeout = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
                timeout.CancelAfter(TimeSpan.FromSeconds(90));
                try { await process.WaitForExitAsync(timeout.Token); }
                catch { if (!process.HasExited) process.Kill(true); throw; }
                await File.WriteAllTextAsync(Path.Combine(reportDirectory, "epubcheck.log"), await stdout + "\n" + await stderr, cancellationToken);
                checkExit = process.ExitCode;
                if (checkExit != 0) issues.Add($"EPUBCheck reprovou o arquivo (exit {checkExit}).");
            }
            catch (Exception exception) when (exception is IOException or System.ComponentModel.Win32Exception)
            {
                issues.Add("EPUBCheck nao executado: " + exception.Message);
            }
        }

        if (CheckStructure(epub, bilingual).Count == 0)
        {
            try
            {
                var preview = Path.Combine(reportDirectory, "preview");
                Directory.CreateDirectory(preview);
                ZipFile.ExtractToDirectory(epub, preview, true);
                using var playwright = await Playwright.CreateAsync();
                await using var browser = await playwright.Chromium.LaunchAsync(new() { Headless = true });
                var page = await browser.NewPageAsync();
                foreach (var width in new[] { 390, 600, 1200 })
                foreach (var fontSize in new[] { 16, 24 })
                {
                    cancellationToken.ThrowIfCancellationRequested();
                    await page.SetViewportSizeAsync(width, 900);
                    await page.GotoAsync(new Uri(Path.Combine(preview, "OEBPS", "chapter.xhtml")).AbsoluteUri);
                    await page.AddStyleTagAsync(new() { Content = $"body {{ font-size: {fontSize}px; }}" });
                    var result = await page.EvaluateAsync<JsonElement>("""
                        () => {
                          const issues = [];
                          const elements = [...document.querySelectorAll('p,h1,h2,img')];
                          for (const element of elements) {
                            const rect = element.getBoundingClientRect();
                            if (rect.right > innerWidth + 1 || rect.left < -1) issues.push('overflow: ' + element.tagName);
                            if (!rect.width || !rect.height) issues.push('empty box: ' + element.tagName);
                          }
                          const blocks = [...document.querySelectorAll('.bilingual p')];
                          for (let index = 1; index < blocks.length; index++) {
                            if (blocks[index].getBoundingClientRect().top < blocks[index-1].getBoundingClientRect().bottom - 1)
                              issues.push('overlapping paragraphs');
                          }
                          const images = [...document.images];
                          if (images.some(image => !image.complete || !image.naturalWidth)) issues.push('broken image');
                                                    for (const image of images) {
                                                        const rect = image.getBoundingClientRect();
                                                        if (image.naturalWidth && Math.abs(rect.width / rect.height - image.naturalWidth / image.naturalHeight) > 0.02)
                                                            issues.push('distorted image');
                                                    }
                                                    const flow = [...document.querySelectorAll('.bilingual,.figure')];
                                                    for (let index = 1; index < flow.length; index++) {
                                                        if (flow[index].getBoundingClientRect().top < flow[index-1].getBoundingClientRect().bottom - 1)
                                                            issues.push('overlapping visual or text');
                                                    }
                          return { width: innerWidth, fontSize: getComputedStyle(document.body).fontSize,
                            pairs: document.querySelectorAll('.bilingual').length, images: images.length, issues };
                        }
                        """);
                    layouts.Add(result);
                    foreach (var issue in result.GetProperty("issues").EnumerateArray())
                        issues.Add($"Layout {width}/{fontSize}: {issue.GetString()}");
                    await page.ScreenshotAsync(new() { Path = Path.Combine(reportDirectory, $"layout-{width}-{fontSize}.png") });
                    if (width == 600 && fontSize == 16 && await page.Locator(".figure").CountAsync() > 0)
                    {
                        await page.Locator(".figure").First.ScrollIntoViewIfNeededAsync();
                        await page.ScreenshotAsync(new() { Path = Path.Combine(reportDirectory, "figure-600.png") });
                    }
                    if (fontSize == 16 && width is 390 or 600)
                    {
                        foreach (var visual in await page.Locator(".figure[id]").AllAsync())
                        {
                            var id = await visual.GetAttributeAsync("id");
                            await visual.ScreenshotAsync(new() { Path = Path.Combine(reportDirectory, $"{id}-{width}.png") });
                        }
                    }
                }
            }
            catch (PlaywrightException exception)
            {
                issues.Add("Validacao visual falhou: " + exception.Message);
            }
        }
        var report = new ValidationReport(issues.Count == 0, issues, checkExit, layouts);
        await File.WriteAllTextAsync(Path.Combine(reportDirectory, "validation.json"), JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }), cancellationToken);
        return report;
    }

    private static string Read(ZipArchiveEntry entry)
    {
        using var reader = new StreamReader(entry.Open());
        return reader.ReadToEnd();
    }
}