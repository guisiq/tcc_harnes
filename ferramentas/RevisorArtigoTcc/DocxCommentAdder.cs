using System.Diagnostics;
using System.Text;
using System.Text.Json;

namespace RevisorArtigoTcc;

public sealed record CommentInsertionResult(
    string Source,
    string Output,
    int CommentsAdded,
    int ExistingCommentsPreserved,
    List<CommentMiss> Missed
);

public sealed record CommentMiss(
    int Id,
    string Reason
);

public static class DocxCommentAdder
{
    public static CommentInsertionResult AddComments(
        string sourceDocx,
        string outputDocx,
        string observationsJson,
        CancellationToken cancellationToken = default)
    {
        var script = Path.Combine(AppContext.BaseDirectory, "add_docx_comments.py");
        if (!File.Exists(script))
        {
            var repoScript = Path.GetFullPath(
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "add_docx_comments.py"));
            if (File.Exists(repoScript))
                script = repoScript;
        }

        if (!File.Exists(script))
            throw new FileNotFoundException("Script add_docx_comments.py não encontrado.", script);

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
        start.ArgumentList.Add(Path.GetFullPath(sourceDocx));
        start.ArgumentList.Add(Path.GetFullPath(outputDocx));
        start.ArgumentList.Add(Path.GetFullPath(observationsJson));

        using var process = Process.Start(start)
            ?? throw new IOException("Python não iniciou para inserir comentários no DOCX.");

        var stdout = process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderr = process.StandardError.ReadToEndAsync(cancellationToken);
        process.WaitForExit();

        cancellationToken.ThrowIfCancellationRequested();
        if (process.ExitCode != 0)
            throw new InvalidOperationException("Falha ao inserir comentários no DOCX: " + stderr.GetAwaiter().GetResult());

        var json = stdout.GetAwaiter().GetResult();
        return JsonSerializer.Deserialize<CommentInsertionResult>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        }) ?? throw new InvalidDataException("Resposta inválida do criador de comentários.");
    }
}
