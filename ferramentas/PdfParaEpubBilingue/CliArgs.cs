namespace PdfParaEpubBilingue;

public sealed class CliArgs
{
    public required string InputPdf { get; init; }
    public string? Output { get; init; }
    public string? Title { get; init; }
    public string? Author { get; init; }
    public string Model { get; init; } = "mai-code-1.1-flash";
    public string[] Formats { get; init; } = ["epub"];
    public string? Calibre { get; init; }
    public bool ExportOnly { get; init; }
    public string? EpubCheckJar { get; init; }
    public bool Force { get; init; }
    public bool ExtractOnly { get; init; }
    public bool SkipTranslation { get; init; }
    public int? MaxPages { get; init; }

    public static CliArgs? Parse(string[] args)
    {
        if (args.Length == 0)
        {
            return null;
        }

        string? input = null;
        string? output = null;
        string? title = null;
        string? author = null;
        var model = "mai-code-1.1-flash";
        var formats = new[] { "epub" };
        var calibre = Environment.GetEnvironmentVariable("EBOOK_CONVERT");
        var exportOnly = false;
        string? epubCheckJar = Environment.GetEnvironmentVariable("EPUBCHECK_JAR");
        var force = false;
        var extractOnly = false;
        var skipTranslation = false;
        int? maxPages = null;

        for (var i = 0; i < args.Length; i++)
        {
            string Value()
            {
                if (i + 1 >= args.Length || args[i + 1].StartsWith("--"))
                    throw new ArgumentException($"Valor ausente para {args[i]}.");
                return args[++i];
            }
            switch (args[i])
            {
                case "--formats":
                    formats = KindleExporter.ParseFormats(Value());
                    break;
                case "--calibre":
                    calibre = Value();
                    break;
                case "--export-only":
                    exportOnly = true;
                    break;
                case "--output":
                case "-o":
                    output = Value();
                    break;
                case "--title":
                    title = Value();
                    break;
                case "--author":
                    author = Value();
                    break;
                case "--model":
                    model = Value();
                    break;
                case "--epubcheck-jar":
                    epubCheckJar = Value();
                    break;
                case "--force":
                    force = true;
                    break;
                case "--extract-only":
                    extractOnly = true;
                    break;
                case "--no-translate":
                    skipTranslation = true;
                    break;
                case "--max-pages":
                    if (!int.TryParse(Value(), out var pageLimit) || pageLimit <= 0)
                        throw new ArgumentException("--max-pages deve ser um inteiro positivo.");
                    maxPages = pageLimit;
                    break;
                case "--help":
                case "-h":
                    return null;
                default:
                    if (args[i].StartsWith('-') || input is not null)
                        throw new ArgumentException($"Argumento desconhecido: {args[i]}.");
                    input = args[i];
                    break;
            }
        }

        if (input is null)
        {
            return null;
        }

        return new CliArgs
        {
            InputPdf = input,
            Output = output,
            Title = title,
            Author = author,
            Model = model,
            SkipTranslation = skipTranslation,
            MaxPages = maxPages,
            EpubCheckJar = epubCheckJar,
            Force = force,
            ExtractOnly = extractOnly,
            Formats = formats,
            Calibre = calibre,
            ExportOnly = exportOnly,
        };
    }

    public static void PrintUsage()
    {
        Console.WriteLine("""
            Uso: PdfParaEpubBilingue <arquivo.pdf> [opções]

            Converte um PDF acadêmico em EPUB bilíngue (inglês original + tradução em
            português), incluindo recortes originais de tabelas e figuras no fluxo. A tradução
            usa o GitHub Copilot SDK e envia texto ao provedor (pode consumir cota).
            Requer .NET 9, Python com PyMuPDF, Java, EPUBCheck e Chromium Playwright.
            Execute ferramentas/setup-pdf-epub.ps1 para preparar dependencias locais.
            PDF digital somente: sem OCR. A ordem e hifenizacao de PDFs complexos
            podem exigir revisao; imagens e formulas originais nao sao redesenhadas.
            PyMuPDF tem licenca AGPL/comercial; revise antes de redistribuir a ferramenta.

            Opções:
              --output, -o <arquivo.epub>   Caminho do EPUB de saída (padrão: mesmo nome do PDF)
              --title <texto>               Título a usar no EPUB (padrão: nome do arquivo)
              --author <texto>              Autor a usar no EPUB
              --model <nome>                 Modelo de layout/traducao (padrao: mai-code-1.1-flash)
              --formats <lista>              epub,azw3,mobi,pdf (padrao: epub; EPUB base sempre mantido)
              --export-only                  Entrada EPUB existente: exporta sem chamar IA
              --calibre <ebook-convert.exe>   Conversor Calibre; alternativa: EBOOK_CONVERT
              --models                       Lista modelos disponiveis na conta
              --epubcheck-jar <arquivo.jar>   EPUBCheck oficial; alternativa: variavel EPUBCHECK_JAR
              --extract-only                 Salva texto extraido e paginas PNG, sem chamar IA
              --force                        Autoriza substituir a saida existente
              --install-browser              Instala Chromium para validacao Playwright
              --validate <arquivo.epub>       Valida EPUB existente (usa EPUBCHECK_JAR)
              --no-translate                 Nao traduz prosa; recortes ainda usam IA de layout
              --max-pages <N>                Processa só as N primeiras páginas (útil para testes rápidos)

                        Exemplo a partir da raiz do repositorio:
                            ./ferramentas/pdf-epub.ps1 "artigos/paper.pdf" --output "artigos/epub/paper.epub"

                        stdout: resultado JSON; stderr: progresso/erros. Cache: <saida>.work/cache.
                        Saida somente publicada apos validacao. Codigos: 0 sucesso, 1 argumentos,
                        2 falha de execucao, 3 validacao reprovada, 130 cancelamento.
                        EPUB: envie pelo Send to Kindle para conversao; copiar EPUB por USB nao basta.
                        AZW3: recomendado para USB. MOBI: legado, nao aceito pelo Send to Kindle.
                        PDF: pagina fixa A5. KFX: nao suportado por este exportador.
                        Elementos sem legenda numerada exigem revisao manual dos recortes.
            """);
    }
}
