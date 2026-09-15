using System.Diagnostics;
using System.Text;

namespace PdfParaEpubBilingue;

public sealed record KindleExport(string Format, string Path, long Bytes, string Validation);

public static class KindleExporter
{
    public static string[] ParseFormats(string value)
    {
        var formats = value.Split(',').Select(format => format.Trim().ToLowerInvariant()).Distinct().ToArray();
        if (formats.Length == 0 || formats.Any(format => format is not ("epub" or "azw3" or "mobi" or "pdf")))
            throw new ArgumentException("Formatos suportados: epub,azw3,mobi,pdf. KFX nao e gerado.");
        return formats;
    }

    public static string ResolveConverter(string? configured)
    {
        if (!string.IsNullOrWhiteSpace(configured))
            return File.Exists(configured) ? Path.GetFullPath(configured) : throw new FileNotFoundException("ebook-convert nao encontrado.", configured);
        var paths = new[]
        {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Calibre2", "ebook-convert.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Calibre2", "ebook-convert.exe")
        }.Concat((Environment.GetEnvironmentVariable("PATH") ?? "").Split(Path.PathSeparator)
            .Select(directory => Path.Combine(directory, OperatingSystem.IsWindows() ? "ebook-convert.exe" : "ebook-convert")));
        return paths.FirstOrDefault(File.Exists) ?? throw new FileNotFoundException("Instale Calibre ou informe --calibre <ebook-convert.exe> / EBOOK_CONVERT.");
    }

    public static async Task<List<KindleExport>> ExportAsync(string epub, IEnumerable<string> formats,
        string converter, bool force, Action<string> log, CancellationToken cancellationToken = default)
    {
        var requested = ParseFormats(string.Join(',', formats)).Where(format => format != "epub").ToArray();
        foreach (var format in requested)
            if (File.Exists(Path.ChangeExtension(epub, format)) && !force)
                throw new IOException($"Saida {format} ja existe. Use --force.");
        var exports = new List<KindleExport>();
        foreach (var format in requested)
        {
            var output = Path.ChangeExtension(epub, format);
            var work = Path.Combine(epub + ".work", "exports", Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(work);
            var candidate = Path.Combine(work, "book." + format);
            log($"Exportando {format.ToUpperInvariant()} via Calibre...");
            var arguments = new List<string> { Path.GetFullPath(epub), candidate, "--output-profile", "tablet", "--chapter", "/", "--page-breaks-before", "/" };
            if (format == "mobi") arguments.AddRange(["--mobi-file-type", "old", "--mobi-keep-original-images"]);
            if (format == "pdf") arguments.AddRange(["--paper-size", "a5", "--pdf-default-font-size", "16", "--pdf-page-margin-left", "20", "--pdf-page-margin-right", "20"]);
            await RunConverterAsync(converter, arguments, Path.Combine(work, "conversion.log"), cancellationToken);
            VerifyContainer(candidate, format);
            if (format is "azw3" or "mobi")
            {
                var roundtrip = Path.Combine(work, "reopened.epub");
                await RunConverterAsync(converter, [candidate, roundtrip, "--output-profile", "tablet"], Path.Combine(work, "reopen.log"), cancellationToken);
                using var archive = System.IO.Compression.ZipFile.OpenRead(roundtrip);
                if (!archive.Entries.Any(entry => entry.FullName.EndsWith(".opf")) || !archive.Entries.Any(entry => entry.FullName.EndsWith(".html") || entry.FullName.EndsWith(".xhtml")))
                    throw new InvalidDataException("Calibre nao conseguiu reabrir o livro exportado.");
            }
            File.Move(candidate, output, force);
            exports.Add(new(format, output, new FileInfo(output).Length,
                format == "pdf" ? "PDF aberto pelo PdfPig; sem teste em Kindle fisico" : "Reaberto pelo Calibre; sem teste em Kindle fisico"));
        }
        return exports;
    }

    public static void VerifyContainer(string path, string format)
    {
        using var stream = File.OpenRead(path);
        var header = new byte[80];
        if (stream.Read(header) < header.Length) throw new InvalidDataException("Arquivo exportado vazio ou truncado.");
        if (format == "pdf")
        {
            if (Encoding.ASCII.GetString(header, 0, 5) != "%PDF-") throw new InvalidDataException("Assinatura PDF invalida.");
            using var document = UglyToad.PdfPig.PdfDocument.Open(path);
            if (document.NumberOfPages == 0) throw new InvalidDataException("PDF sem paginas.");
        }
        else if (format is "azw3" or "mobi")
        {
            if (Encoding.ASCII.GetString(header, 60, 8) != "BOOKMOBI") throw new InvalidDataException("Container Kindle invalido.");
        }
        else throw new ArgumentException("Formato de exportacao nao suportado.");
    }

    private static async Task RunConverterAsync(string converter, IEnumerable<string> arguments, string logPath, CancellationToken cancellationToken)
    {
        var start = new ProcessStartInfo(converter) { UseShellExecute = false, RedirectStandardOutput = true, RedirectStandardError = true };
        foreach (var argument in arguments) start.ArgumentList.Add(argument);
        using var process = Process.Start(start) ?? throw new IOException("Calibre nao iniciou.");
        var stdout = process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderr = process.StandardError.ReadToEndAsync(cancellationToken);
        using var timeout = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeout.CancelAfter(TimeSpan.FromMinutes(5));
        try { await process.WaitForExitAsync(timeout.Token); }
        catch { if (!process.HasExited) process.Kill(true); throw; }
        await File.WriteAllTextAsync(logPath, await stdout + "\n" + await stderr, cancellationToken);
        if (process.ExitCode != 0) throw new IOException($"Calibre falhou ({process.ExitCode}). Consulte {logPath}");
    }
}