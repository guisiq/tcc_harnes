using System.Diagnostics;
using System.Globalization;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using UglyToad.PdfPig;

namespace RevisorArtigoTcc;

public static class PdfParagraphExtractor
{
    public static ExtractionResult Extract(string pdfPath, int? maxPages = null)
    {
        if (!File.Exists(pdfPath))
            throw new FileNotFoundException("PDF não encontrado.", pdfPath);

        var scriptPath = Path.Combine(AppContext.BaseDirectory, "extract_paragraphs.py");
        if (!File.Exists(scriptPath))
        {
            var repoCandidate = Path.Combine(Path.GetDirectoryName(typeof(PdfParagraphExtractor).Assembly.Location) ?? "", "..", "..", "..", "extract_paragraphs.py");
            if (File.Exists(repoCandidate))
                scriptPath = Path.GetFullPath(repoCandidate);
        }

        if (File.Exists(scriptPath))
        {
            var start = new ProcessStartInfo(Environment.GetEnvironmentVariable("PDF_EPUB_PYTHON") ?? "python")
            {
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8
            };
            start.ArgumentList.Add(scriptPath);
            start.ArgumentList.Add(Path.GetFullPath(pdfPath));
            start.ArgumentList.Add((maxPages ?? 0).ToString(CultureInfo.InvariantCulture));

            using var process = Process.Start(start);
            if (process is not null)
            {
                var stdoutTask = process.StandardOutput.ReadToEndAsync();
                var stderrTask = process.StandardError.ReadToEndAsync();
                if (process.WaitForExit(90_000) && process.ExitCode == 0)
                {
                    var json = stdoutTask.GetAwaiter().GetResult();
                    var firstBrace = json.IndexOf('{');
                    if (firstBrace > 0)
                        json = json[firstBrace..];
                    var parsed = JsonSerializer.Deserialize<ExtractionResult>(json);
                    if (parsed is not null && parsed.Items.Count > 0)
                        return parsed;
                }
            }
        }

        // Pure .NET PdfPig fallback if Python/PyMuPDF is unavailable
        return ExtractWithPdfPigFallback(pdfPath, maxPages);
    }

    private static ExtractionResult ExtractWithPdfPigFallback(string pdfPath, int? maxPages)
    {
        using var document = PdfDocument.Open(pdfPath);
        var limit = maxPages.HasValue ? Math.Min(maxPages.Value, document.NumberOfPages) : document.NumberOfPages;
        var items = new List<DocumentItem>();
        var currentSection = "Elementos Pré-Textuais";
        var id = 1;

        for (var p = 1; p <= limit; p++)
        {
            var page = document.GetPage(p);
            var text = Regex.Replace(page.Text, @"\s+", " ").Trim();
            if (!string.IsNullOrWhiteSpace(text))
            {
                items.Add(new DocumentItem(id++, p, p, p, currentSection, "paragraph", text));
            }
        }

        return new ExtractionResult(limit, items, []);
    }
}
