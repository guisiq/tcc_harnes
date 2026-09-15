using System.IO.Compression;
using System.Xml.Linq;
using PdfParaEpubBilingue;
using SkiaSharp;
using Xunit;

namespace PdfParaEpubBilingue.Tests;

public sealed class PipelineTests : IDisposable
{
    private readonly string directory = Path.Combine(Path.GetTempPath(), "pdf-epub-tests-" + Guid.NewGuid());
    private static readonly PdfParagraph[] Source = [new(1, 0, "Memory & <context> \"test\"")];

    [Theory]
    [InlineData("")]
    [InlineData("[]")]
    [InlineData("{}")]
    [InlineData("[{\"id\":1,\"pt\":\"Memoria\"}]")]
    [InlineData("[{\"id\":0,\"pt\":\"\"}]")]
    [InlineData("[{\"id\":0,\"pt\":null}]")]
    [InlineData("[{\"id\":0,\"pt\":\"Um\"},{\"id\":0,\"pt\":\"Dois\"}]")]
    [InlineData("Explanation\n```json\n[{\"id\":0,\"pt\":\"Memoria\"}]\n```")]
    public void RejectsIncompleteOrMalformedTranslation(string json) =>
        Assert.Throws<InvalidDataException>(() => BilingualTranslator.ParseTranslations(json, Source));

    [Fact]
    public void ParsesCompleteTranslation() =>
        Assert.Equal("Memoria", BilingualTranslator.ParseTranslations("[{\"id\":0,\"pt\":\"Memoria\"}]", Source)[0]);

    [Theory]
    [InlineData("\n")]
    [InlineData("\r\n")]
    public void AcceptsExactJsonFence(string newline) =>
        Assert.Equal("Memoria", BilingualTranslator.ParseTranslations("```json" + newline + "[{\"id\":0,\"pt\":\"Memoria\"}]" + newline + "```", Source)[0]);

    [Theory]
    [InlineData("--unknown")]
    [InlineData("--output")]
    [InlineData("--max-pages", "0")]
    [InlineData("--max-pages", "-1")]
    [InlineData("--max-pages", "abc")]
    public void RejectsInvalidArguments(params string[] options) =>
        Assert.Throws<ArgumentException>(() => CliArgs.Parse(["paper.pdf", .. options]));

    [Fact]
    public void MissingTranslationCannotCreateEpub()
    {
        var path = Path.Combine(directory, "missing.epub");
        Assert.Throws<InvalidDataException>(() => EpubBuilder.Build(path, "Title", "Author", Extraction(), new Dictionary<(int, int), string>()));
        Assert.False(File.Exists(path));
    }

    [Fact]
    public void BilingualEpubPreservesTextAndImage()
    {
        var path = Build();
        Assert.Empty(EpubValidator.CheckStructure(path));
        using var archive = ZipFile.OpenRead(path);
        using var stream = archive.GetEntry("OEBPS/chapter.xhtml")!.Open();
        var xml = XDocument.Load(stream);
        XNamespace html = "http://www.w3.org/1999/xhtml";
        var paragraphs = xml.Descendants(html + "div").Single(element => (string?)element.Attribute("class") == "bilingual").Elements(html + "p").ToArray();
        Assert.Equal(Source[0].Text, paragraphs[0].Value);
        Assert.Equal("Memoria & <contexto>", paragraphs[1].Value);
        Assert.Equal("en", (string?)paragraphs[0].Attribute(XNamespace.Xml + "lang"));
        Assert.Equal("pt-BR", (string?)paragraphs[1].Attribute(XNamespace.Xml + "lang"));
    }

    [Fact]
    public void MissingImageFailsValidation()
    {
        var path = Build();
        using (var archive = ZipFile.Open(path, ZipArchiveMode.Update))
            archive.GetEntry("OEBPS/images/page-001.png")!.Delete();
        Assert.Contains(EpubValidator.CheckStructure(path), issue => issue.Contains("Recurso ausente"));
    }

    [Fact]
    public void OriginalOnlyIsNotAcceptedAsBilingual()
    {
        var path = Path.Combine(directory, "original.epub");
        EpubBuilder.Build(path, "Title", "Author", Extraction(), new Dictionary<(int, int), string>(), true);
        Assert.Empty(EpubValidator.CheckStructure(path, false));
        Assert.NotEmpty(EpubValidator.CheckStructure(path));
    }

    [Fact]
    public void BrokenArchiveFailsValidation()
    {
        Directory.CreateDirectory(directory);
        var path = Path.Combine(directory, "broken.epub");
        File.WriteAllText(path, "not a ZIP");
        Assert.NotEmpty(EpubValidator.CheckStructure(path));
    }

    [Fact]
    public void VisualCellsAndCaptionNeverEnterTranslationAndAppearInline()
    {
        var (blocks, original) = VisualSource();
        var organized = VisualLayoutOrganizer.ApplyRegions(blocks, original, [new("table", 3, [20, 30, 170, 105])]);
        Assert.Equal(new[] { 0, 4 }, organized.Paragraphs.Select(block => block.Order));
        Assert.Equal(new[] { 1, 2, 3 }, organized.Images.Single().ExcludedOrders);
        Assert.Equal(1, organized.Images.Single().Order);
        var path = Path.Combine(directory, "visual.epub");
        EpubBuilder.Build(path, "Title", "Author", organized,
            new Dictionary<(int, int), string> { [(1, 0)] = "Antes", [(1, 4)] = "Depois" });
        Assert.Empty(EpubValidator.CheckStructure(path));
        using var archive = ZipFile.OpenRead(path);
        using var stream = archive.GetEntry("OEBPS/chapter.xhtml")!.Open();
        var xml = XDocument.Load(stream);
        XNamespace html = "http://www.w3.org/1999/xhtml";
        var flow = xml.Descendants(html + "div").Select(element => (string?)element.Attribute("class")).ToArray();
        Assert.Equal(new[] { "bilingual", "figure", "bilingual" }, flow);
        Assert.DoesNotContain("81.25", string.Join(" ", xml.Descendants(html + "p").Select(element => element.Value)));
        using var crop = SKBitmap.Decode(organized.Images.Single().PngBytes);
        Assert.Equal(SKColors.Black, crop.GetPixel(50, 40));
    }

    [Theory]
    [InlineData(20, 30, 170, 45)]
    [InlineData(-10, 30, 170, 105)]
    [InlineData(30, 30, 170, 105)]
    public void RejectsClippedOrOutOfPageVisual(double left, double top, double right, double bottom)
    {
        var (blocks, original) = VisualSource();
        Assert.Throws<InvalidDataException>(() => VisualLayoutOrganizer.ApplyRegions(blocks, original,
            [new("table", 3, [left, top, right, bottom])]));
    }

    [Fact]
    public void MissingCaptionRegionFails()
    {
        var (blocks, original) = VisualSource();
        Assert.Throws<InvalidDataException>(() => VisualLayoutOrganizer.ApplyRegions(blocks, original, []));
    }

    [Fact]
    public void BuilderRejectsVisualTextLeakage()
    {
        var (blocks, original) = VisualSource();
        var organized = VisualLayoutOrganizer.ApplyRegions(blocks, original, [new("table", 3, [20, 30, 170, 105])]);
        organized.Paragraphs.Add(blocks[2]);
        Assert.Throws<InvalidDataException>(() => EpubBuilder.Build(Path.Combine(directory, "leak.epub"), "Title", "Author",
            organized, new Dictionary<(int, int), string>(), true));
    }

    private static (PdfParagraph[] Blocks, PdfImage Original) VisualSource()
    {
        PdfParagraph[] blocks = [new(1, 0, "Prose before", [20, 0, 170, 10]),
            new(1, 1, "Dataset F1", [20, 35, 170, 45]), new(1, 2, "81.25 79.50", [20, 50, 170, 60]),
            new(1, 3, "Table 1: Results.", [20, 90, 170, 100]), new(1, 4, "Prose after", [20, 125, 170, 135])];
        using var bitmap = new SKBitmap(400, 400);
        bitmap.Erase(SKColors.White);
        using var canvas = new SKCanvas(bitmap);
        using var paint = new SKPaint { Color = SKColors.Black };
        canvas.DrawRect(30, 60, 310, 135, paint);
        using var data = bitmap.Encode(SKEncodedImageFormat.Png, 100);
        return (blocks, new(1, 0, "page-001.png", data.ToArray()));
    }

    private string Build()
    {
        var path = Path.Combine(directory, "test.epub");
        EpubBuilder.Build(path, "Title & <test>", "Author", Extraction(),
            new Dictionary<(int, int), string> { [(1, 0)] = "Memoria & <contexto>" });
        return path;
    }

    [Theory]
    [InlineData("kfx")]
    [InlineData("azw")]
    [InlineData("")]
    [InlineData("epub,")]
    public void RejectsUnsupportedExportFormats(string value) =>
        Assert.Throws<ArgumentException>(() => KindleExporter.ParseFormats(value));

    [Fact]
    public void ParsesKindleOptions()
    {
        var args = CliArgs.Parse(["book.epub", "--export-only", "--formats", "EPUB,azw3,mobi,pdf,azw3", "--calibre", "converter.exe"]);
        Assert.True(args!.ExportOnly);
        Assert.Equal(new[] { "epub", "azw3", "mobi", "pdf" }, args.Formats);
        Assert.Equal("converter.exe", args.Calibre);
        Assert.Equal("mai-code-1.1-flash", args.Model);
    }

    [Theory]
    [InlineData("azw3")]
    [InlineData("mobi")]
    [InlineData("pdf")]
    public void RejectsInvalidExportContainer(string format)
    {
        Directory.CreateDirectory(directory);
        var path = Path.Combine(directory, "broken." + format);
        File.WriteAllBytes(path, new byte[100]);
        Assert.Throws<InvalidDataException>(() => KindleExporter.VerifyContainer(path, format));
    }

    private static PdfExtractionResult Extraction()
    {
        using var bitmap = new SKBitmap(32, 32);
        bitmap.Erase(SKColors.White);
        bitmap.SetPixel(16, 16, SKColors.Black);
        using var data = bitmap.Encode(SKEncodedImageFormat.Png, 100);
        return new(1, Source.ToList(), [new(1, 0, "page-001.png", data.ToArray())]);
    }

    public void Dispose()
    {
        if (Directory.Exists(directory)) Directory.Delete(directory, true);
    }
}