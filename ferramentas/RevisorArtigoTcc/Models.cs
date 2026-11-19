using System.Text.Json.Serialization;

namespace RevisorArtigoTcc;

public sealed record DocumentItem(
    int Id,
    int PageStart,
    int PageEnd,
    int? PrintedPage,
    string Section,
    string Kind,
    string Text
);

public sealed record PdfImageMeta(
    int Page,
    int IndexOnPage,
    int Xref,
    int Width,
    int Height
);

public sealed record ExtractionResult(
    int PageCount,
    List<DocumentItem> Items,
    List<PdfImageMeta> Images
);

public sealed record DeterministicIssue(
    string Code,
    string Severity, // "CRITICO", "AJUSTAR", "INFO"
    string Source,   // "Diagrama", "Metodologia", "Checklist-TCC1"
    string Message,
    string? Suggestion = null
);

public sealed record ItemDeterministicAudit(
    int ItemId,
    int WordCount,
    int SentenceCount,
    int MaxSentenceWords,
    List<DeterministicIssue> Issues
);

public sealed record CitationCheckResult(
    List<string> CitedInText,
    List<string> ListedInReferences,
    List<string> CitedButMissingInReferences,
    List<string> InReferencesButNotCited,
    List<string> ReferenceFormattingAlerts
);

public sealed record VisualElementAudit(
    string Identifier,
    string Kind,
    int CaptionItemId,
    int Page,
    bool CitedInBody,
    bool HasSourceNote,
    bool ListedInFrontMatter,
    string CaptionText,
    List<string> Alerts
);

public sealed record LlmParagraphObservation(
    [property: JsonPropertyName("id")] int Id,
    [property: JsonPropertyName("st")] string Status, // "OK", "AJUSTAR", "CRITICO"
    [property: JsonPropertyName("c")] List<string> Codes,
    [property: JsonPropertyName("obs")] string Observation,
    [property: JsonPropertyName("sug")] string? Suggestion
);

public sealed record CombinedItemObservation(
    DocumentItem Item,
    ItemDeterministicAudit Deterministic,
    LlmParagraphObservation? Llm,
    string FinalStatus,
    List<string> AllCodes,
    string ConsolidatedObservation,
    string? ConsolidatedSuggestion
);

public sealed record ChecklistEvaluationItem(
    int Number,
    string Name,
    string Question,
    string Status, // "Atende", "Atende Parcialmente", "Não Atende", "Não Esperado (TCC1)"
    string EvidenceIds,
    string Observation
);
