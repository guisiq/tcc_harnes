using System.Text;
using UglyToad.PdfPig.Content;
using UglyToad.PdfPig.Rendering.Skia;
using System.Text.RegularExpressions;
using System.Diagnostics;
using System.Text.Json;

namespace PdfParaEpubBilingue;

/// <summary>Um parágrafo de texto extraído de uma página do PDF.</summary>
public sealed record PdfParagraph(int PageNumber, int Order, string Text, double[]? Bounds = null);

/// <summary>Uma imagem extraída de uma página do PDF, já convertida para PNG.</summary>
public sealed record PdfImage(int PageNumber, int Order, string FileName, byte[] PngBytes,
    string Kind = "original-page", string? Caption = null, int[]? ExcludedOrders = null);

public sealed record PdfExtractionResult(int PageCount, List<PdfParagraph> Paragraphs, List<PdfImage> Images);

/// <summary>Extrai texto (em ordem de leitura) e imagens de um PDF usando PdfPig.</summary>
public static class PdfExtractor
{
    public static PdfExtractionResult Extract(string pdfPath, int? maxPages = null)
    {
        if (maxPages is <= 0)
            throw new ArgumentOutOfRangeException(nameof(maxPages));
        var paragraphs = new List<PdfParagraph>();
        var images = new List<PdfImage>();

        using var document = UglyToad.PdfPig.PdfDocument.Open(pdfPath, SkiaRenderingParsingOptions.Instance);
        document.AddSkiaPageFactory();
        var pageCount = document.NumberOfPages;
        var pagesToRead = maxPages.HasValue ? Math.Min(maxPages.Value, pageCount) : pageCount;

        for (var pageNumber = 1; pageNumber <= pagesToRead; pageNumber++)
        {
            var page = document.GetPage(pageNumber);

            using var rendered = document.GetPageAsPng(pageNumber, 2, 100);
            images.Add(new PdfImage(pageNumber, 0, $"page-{pageNumber:D3}.png", rendered.ToArray()));
        }

        var start = new ProcessStartInfo(Environment.GetEnvironmentVariable("PDF_EPUB_PYTHON") ?? "python")
        {
            UseShellExecute = false, RedirectStandardOutput = true, RedirectStandardError = true,
            StandardOutputEncoding = Encoding.UTF8, StandardErrorEncoding = Encoding.UTF8
        };
        start.ArgumentList.Add(Path.Combine(AppContext.BaseDirectory, "extract_text.py"));
        start.ArgumentList.Add(Path.GetFullPath(pdfPath));
        start.ArgumentList.Add(pagesToRead.ToString(System.Globalization.CultureInfo.InvariantCulture));
        using var process = Process.Start(start) ?? throw new IOException("Python nao iniciou. Instale Python e pymupdf.");
        var stdout = process.StandardOutput.ReadToEndAsync();
        var stderr = process.StandardError.ReadToEndAsync();
        if (!process.WaitForExit(90000))
        {
            process.Kill(true);
            throw new TimeoutException("Extracao PDF excedeu 90 segundos.");
        }
        if (process.ExitCode != 0) throw new InvalidDataException("Extracao falhou: " + stderr.GetAwaiter().GetResult());
        paragraphs = JsonSerializer.Deserialize<List<PdfParagraph>>(stdout.GetAwaiter().GetResult())
            ?? throw new InvalidDataException("Extrator retornou dados invalidos.");
        return new PdfExtractionResult(pagesToRead, paragraphs, images);
    }

    private static string NormalizeWhitespace(string text)
    {
        text = Regex.Replace(text, @"(\p{L})-\r?\n(\p{Ll})", "$1$2");
        var sb = new StringBuilder(text.Length);
        var lastWasSpace = false;
        foreach (var c in text)
        {
            var ch = c is '\n' or '\r' or '\t' ? ' ' : c;
            if (ch == ' ')
            {
                if (lastWasSpace)
                {
                    continue;
                }

                lastWasSpace = true;
            }
            else
            {
                lastWasSpace = false;
            }

            sb.Append(ch);
        }

        return sb.ToString().Trim();
    }
}
