using System.IO.Compression;
using System.Text;
using System.Text.RegularExpressions;

namespace PdfParaEpubBilingue;

/// <summary>Monta um EPUB (formato ZIP/OPF/NCX/XHTML) bilíngue (EN + PT) com imagens incorporadas.</summary>
public static class EpubBuilder
{
    public static void Build(
        string outputPath,
        string title,
        string author,
        PdfExtractionResult extraction,
        IReadOnlyDictionary<(int Page, int Order), string> translations,
        bool originalOnly = false)
    {
        if (extraction.Paragraphs.Count == 0)
          throw new InvalidDataException("PDF sem texto extraivel; OCR necessario.");
        if (extraction.Images.Any(image => image.ExcludedOrders is not null && extraction.Paragraphs.Any(paragraph =>
            paragraph.PageNumber == image.PageNumber && image.ExcludedOrders.Contains(paragraph.Order))))
            throw new InvalidDataException("Rotulos ou celulas de um visual ainda presentes no texto de leitura.");
        if (!originalOnly && extraction.Paragraphs.Any(paragraph =>
          !translations.TryGetValue((paragraph.PageNumber, paragraph.Order), out var translated) || string.IsNullOrWhiteSpace(translated)))
          throw new InvalidDataException("Traducao incompleta: EPUB nao sera gerado.");
        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(outputPath))!);

        var paragraphsByPage = extraction.Paragraphs
            .GroupBy(p => p.PageNumber)
            .OrderBy(g => g.Key)
            .ToDictionary(g => g.Key, g => g.OrderBy(p => p.Order).ToList());

        var imagesByPage = extraction.Images
            .GroupBy(i => i.PageNumber)
            .ToDictionary(g => g.Key, g => g.OrderBy(i => i.Order).ToList());

        var bodyBuilder = new StringBuilder();
        bodyBuilder.Append($"<h1>{Escape(title)}</h1>\n");
        bodyBuilder.Append($"<p class=\"author\">{Escape(author)}</p>\n");
        bodyBuilder.Append(originalOnly
          ? "<p>Original English text. / Texto original em ingles, sem traducao.</p>"
          : "<p>English original followed by Brazilian Portuguese. / Original em ingles seguido de traducao automatica para portugues, sem revisao humana integral.</p>");

        foreach (var pageNumber in Enumerable.Range(1, extraction.PageCount))
        {
            var hasText = paragraphsByPage.TryGetValue(pageNumber, out var paragraphs) && paragraphs.Count > 0;
            var hasImages = imagesByPage.TryGetValue(pageNumber, out var images) && images.Count > 0;
            if (!hasText && !hasImages)
            {
                continue;
            }

            bodyBuilder.Append($"<h2 id=\"page-{pageNumber}\" class=\"page-heading\">Página {pageNumber} / Page {pageNumber}</h2>\n");

            var inlineImages = (images ?? []).Where(image => image.Kind != "original-page").ToDictionary(image => image.Order);
            var pageParagraphs = (paragraphs ?? []).ToDictionary(paragraph => paragraph.Order);
            if (inlineImages.Keys.Intersect(pageParagraphs.Keys).Any())
              throw new InvalidDataException("Texto visual nao pode aparecer tambem como paragrafo.");
            if (hasText || inlineImages.Count > 0)
            {
              foreach (var order in pageParagraphs.Keys.Concat(inlineImages.Keys).Order())
                {
                if (inlineImages.TryGetValue(order, out var visual))
                {
                        bodyBuilder.Append($"<div class=\"figure\" id=\"visual-{pageNumber}-{order}\"><img src=\"images/{visual.FileName}\" alt=\"{Escape(visual.Caption ?? visual.Kind)}\" /></div>\n");
                  continue;
                }
                var paragraph = pageParagraphs[order];
                    var pt = translations.TryGetValue((paragraph.PageNumber, paragraph.Order), out var t)
                        ? t
                        : "";
                    var enText = Escape(paragraph.Text);
                    // Some extracted "paragraphs" are entirely corrupted glyphs (control characters with no
                    // valid XML representation); once Escape() strips those out nothing readable remains, and
                    // rendering an empty <p> fails structural validation ("Par de idiomas vazio ou incompleto").
                    // Since there is no meaningful content to show either language, omit the pair entirely.
                    if (string.IsNullOrWhiteSpace(enText))
                      continue;
                    bodyBuilder.Append("<div class=\"bilingual\">\n");
                      bodyBuilder.Append($"<p class=\"en\" xml:lang=\"en\">{enText}</p>\n");
                      if (!originalOnly)
                        bodyBuilder.Append($"<p class=\"pt\" xml:lang=\"pt-BR\">{Escape(pt)}</p>\n");
                    bodyBuilder.Append("</div>\n");
                }
            }

            if (hasImages)
            {
                foreach (var image in images!.Where(image => image.Kind == "original-page"))
                {
                    bodyBuilder.Append(
                        $"<div class=\"figure\"><p>Página original {pageNumber} / Original page {pageNumber}</p><img src=\"images/{image.FileName}\" alt=\"Página original {pageNumber}, incluindo figuras e tabelas\" /></div>\n");
                }
            }
        }

        var chapterXhtml = BuildXhtml(title, bodyBuilder.ToString());
        var allImages = extraction.Images;
        var bookId = Guid.NewGuid().ToString();
        var opf = BuildOpf(title, author, bookId, allImages);
        var ncx = BuildNcx(title, bookId, paragraphsByPage.Keys.Union(imagesByPage.Keys).Order());

        using var fileStream = new FileStream(outputPath, FileMode.Create);
        using var archive = new ZipArchive(fileStream, ZipArchiveMode.Create);

        WriteStoredEntry(archive, "mimetype", "application/epub+zip");
        WriteEntry(archive, "META-INF/container.xml", ContainerXml);
        WriteEntry(archive, "OEBPS/content.opf", opf);
        WriteEntry(archive, "OEBPS/toc.ncx", ncx);
        WriteEntry(archive, "OEBPS/chapter.xhtml", chapterXhtml);

        foreach (var image in allImages)
        {
            var entry = archive.CreateEntry($"OEBPS/images/{image.FileName}", CompressionLevel.Optimal);
            using var entryStream = entry.Open();
            entryStream.Write(image.PngBytes, 0, image.PngBytes.Length);
        }
    }

    private const string ContainerXml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
          </rootfiles>
        </container>
        """;

    // PDF extraction occasionally yields raw control characters (e.g. corrupted font glyph mappings) that XML 1.0 forbids.
    private static readonly Regex InvalidXmlChars = new("[\u0000-\u0008\u000B\u000C\u000E-\u001F\uFFFE\uFFFF]", RegexOptions.Compiled);

    private static string Escape(string value) =>
        InvalidXmlChars.Replace(value, "").Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;").Replace("\"", "&quot;").Replace("'", "&apos;");

    private static string BuildXhtml(string title, string body) => $$"""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="pt-BR">
          <head>
            <title>{{Escape(title)}}</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <style type="text/css">
              body { font-family: Georgia, "Times New Roman", serif; line-height: 1.55; margin: 1em auto; padding: 0 0.8em; max-width: 42em; color: #111; background: #fff; letter-spacing: 0; overflow-wrap: anywhere; }
              h1 { font-size: 1.6em; }
              h2.page-heading { font-size: 1.1em; color: #666; border-bottom: 1px solid #ccc; margin-top: 2em; }
              p.author { color: #555; font-style: italic; }
              .bilingual { margin: 0.9em 0; }
              p { orphans: 2; widows: 2; }
              p.en { text-align: left; margin: 0.4em 0; }
              p.pt { text-align: left; margin: 0.4em 0 1.3em 0; border-left: 2px solid #666; padding-left: 0.6em; }
              .figure { margin: 1.2em 0; text-align: center; }
              .figure img { display: block; width: 100%; max-width: 100%; height: auto; }
            </style>
          </head>
          <body>
            {{body}}
          </body>
        </html>
        """;

    private static string BuildOpf(string title, string author, string bookId, List<PdfImage> images)
    {
        var manifestImages = new StringBuilder();
        foreach (var image in images)
        {
            manifestImages.Append(
                $"    <item id=\"img_{Path.GetFileNameWithoutExtension(image.FileName)}\" href=\"images/{image.FileName}\" media-type=\"image/png\"/>\n");
        }

        return $"""
        <?xml version="1.0" encoding="UTF-8"?>
        <package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="BookId">
          <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
            <dc:title>{Escape(title)}</dc:title>
            <dc:creator>{Escape(author)}</dc:creator>
            <dc:language>pt-BR</dc:language>
            <dc:language>en</dc:language>
            <dc:identifier id="BookId">urn:uuid:{bookId}</dc:identifier>
          </metadata>
          <manifest>
            <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
            <item id="content" href="chapter.xhtml" media-type="application/xhtml+xml"/>
        {manifestImages}  </manifest>
          <spine toc="ncx">
            <itemref idref="content"/>
          </spine>
        </package>
        """;
    }

    private static string BuildNcx(string title, string bookId, IEnumerable<int> pages) => $"""
        <?xml version="1.0" encoding="UTF-8"?>
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
          <head>
            <meta name="dtb:uid" content="urn:uuid:{bookId}"/>
            <meta name="dtb:depth" content="1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
          </head>
          <docTitle><text>{Escape(title)}</text></docTitle>
          <navMap>
            {string.Join("\n", pages.Select((page, index) => $"<navPoint id=\"nav-{page}\" playOrder=\"{index + 1}\"><navLabel><text>Pagina {page} / Page {page}</text></navLabel><content src=\"chapter.xhtml#page-{page}\"/></navPoint>"))}
          </navMap>
        </ncx>
        """;

    private static void WriteEntry(ZipArchive archive, string entryName, string content)
    {
        var entry = archive.CreateEntry(entryName, CompressionLevel.Optimal);
        using var stream = entry.Open();
        using var writer = new StreamWriter(stream, new UTF8Encoding(false));
        writer.Write(content);
    }

    private static void WriteStoredEntry(ZipArchive archive, string entryName, string content)
    {
        var entry = archive.CreateEntry(entryName, CompressionLevel.NoCompression);
        using var stream = entry.Open();
        using var writer = new StreamWriter(stream, new UTF8Encoding(false));
        writer.Write(content);
    }
}
