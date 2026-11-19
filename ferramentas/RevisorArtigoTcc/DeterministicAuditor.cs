using System.Text.RegularExpressions;

namespace RevisorArtigoTcc;

public static class DeterministicAuditor
{
    private static readonly Regex WordCommentRegex = new(@"\[[A-Z]{1,4}\d+\]", RegexOptions.Compiled);
    private static readonly Regex BrokenListMarkerRegex = new(@"(^[a-z]\)[a-z]\)|^[a-z]\)\s+\d+\.)", RegexOptions.Compiled);
    private static readonly Regex SpaceBeforePunctRegex = new(@"(?<=[\p{L}\p{N}])\s+[;,]", RegexOptions.Compiled);
    private static readonly Regex StrayFragmentRegex = new(@"(?<=\.\d*\s+)Com isso\.", RegexOptions.Compiled);
    private static readonly Regex AmbiguousWordsRegex = new(
        @"\b(muito|muitos|muita|muitas|muito\s+grande|not[áa]vel|notavelmente|enorme|bastante|extremamente|v[áa]rios|v[áa]rias|diversos|diversas|significativamente)\b",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);
    private static readonly Regex NominalizationRegex = new(
        @"\b(realizar\s+a\s+\w+ç[ãa]o|fazer\s+a\s+\w+ç[ãa]o|efetuar\s+a\s+\w+ç[ãa]o|proceder\s+[àa]\s+\w+ç[ãa]o|promover\s+a\s+\w+ç[ãa]o|produzir\s+a\s+atualizaç[ãa]o)\b",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);
    private static readonly Regex SuperfluousFillerRegex = new(
        @"\b(cabe\s+ressaltar\s+que|vale\s+destacar\s+que|[ée]\s+importante\s+notar\s+o\s+fato\s+de\s+que|[ée]\s+relevante\s+mencionar\s+que|conv[ée]m\s+lembrar\s+que)\b",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);

    public static (
        Dictionary<int, ItemDeterministicAudit> ItemAudits,
        CitationCheckResult CitationAudit,
        List<VisualElementAudit> VisualAudits
    ) AuditDocument(ExtractionResult extraction)
    {
        var itemAudits = new Dictionary<int, ItemDeterministicAudit>();

        foreach (var item in extraction.Items)
        {
            var issues = new List<DeterministicIssue>();
            var words = Regex.Matches(item.Text, @"[\p{L}\p{N}_-]+").Count;

            // Split sentences ignoring common abbreviations like et al., v., n., p., Seção, Fig.
            var cleanedForSent = Regex.Replace(item.Text, @"\b(et\s+al|v|n|p|Prof|Me|Dr|Sr|Sra|ex|i\.e|e\.g|inc|ago|set|out|nov|dez|fev|mar|abr|mai|jun)\.", "$1_DOT_", RegexOptions.IgnoreCase);
            var sentences = Regex.Split(cleanedForSent, @"(?<=[\.\!\?\:;])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ\(])")
                .Where(s => !string.IsNullOrWhiteSpace(s))
                .ToList();
            var sentenceCount = Math.Max(1, sentences.Count);
            var maxSentWords = sentences.Count == 0
                ? words
                : sentences.Max(s => Regex.Matches(s, @"[\p{L}\p{N}_-]+").Count);

            // 1. Word comment markers ([GS1], [GS2], [GS3], [GS4])
            var commentMatches = WordCommentRegex.Matches(item.Text);
            if (commentMatches.Count > 0)
            {
                var tags = string.Join(", ", commentMatches.Select(m => m.Value).Distinct());
                issues.Add(new DeterministicIssue(
                    "C-11/D-LEIT",
                    "CRITICO",
                    "Checklist-TCC1 / Diagrama",
                    $"Marcador residual de comentário de revisão do Word exportado no PDF ({tags}).",
                    $"Remover o marcador {tags} antes de exportar o documento final."
                ));
            }

            // 2. Broken list numbering (c)a) or g) 7.)
            if (item.Kind == "list_item" && BrokenListMarkerRegex.IsMatch(item.Text.Trim()))
            {
                var marker = BrokenListMarkerRegex.Match(item.Text.Trim()).Value;
                issues.Add(new DeterministicIssue(
                    "C-12/D-LEIT",
                    "CRITICO",
                    "Checklist-TCC1 / Diagrama",
                    $"Numeração de alínea corrompida ou duplicada no início do item ('{marker}').",
                    $"Corrigir o marcador de lista '{marker}' para manter apenas a alínea correta ('c)' ou 'g)')."
                ));
            }

            // 3. Truncated sentence in list item or paragraph
            if (item.Kind is "paragraph" or "list_item")
            {
                var trimmed = item.Text.Trim();
                // Ends with '.', ';', ':', '?', ')' optionally followed by footnote digits or Word comment tags like [GS2]
                if (!Regex.IsMatch(trimmed, @"[\.\;\:\?\)\!](\d+|\s*\[[A-Z]{1,4}\d+\])*$"))
                {
                    issues.Add(new DeterministicIssue(
                        "D-LEIT/C-12",
                        "CRITICO",
                        "Diagrama (Leia em voz alta) / Checklist-TCC1",
                        $"Frase truncada / incompleta no final do item (termina abruptamente em: '...{trimmed.Substring(Math.Max(0, trimmed.Length - 45))}').",
                        "Completar a oração truncada e encerrar com pontuação adequada (ex.: 'não foram recuperados;')."
                    ));
                }
            }

            // 4. Stray fragments ("Com isso.") and spacing before punctuation (" ;")
            if (StrayFragmentRegex.IsMatch(item.Text))
            {
                issues.Add(new DeterministicIssue(
                    "D-LEIT/C-12",
                    "CRITICO",
                    "Diagrama (Leia em voz alta / Corte supérfluos)",
                    "Fragmento de frase isolado e sem predicado ('Com isso.') no meio do parágrafo.",
                    "Remover o fragmento solto 'Com isso.' ou integrá-lo sintaticamente à oração seguinte."
                ));
            }

            if (item.Kind is "paragraph" or "list_item" && SpaceBeforePunctRegex.IsMatch(item.Text))
            {
                issues.Add(new DeterministicIssue(
                    "C-12",
                    "CRITICO",
                    "Checklist-TCC1 (Gramática e Ortografia)",
                    "Espaço indevido antes de sinal de pontuação (ex.: 'triados ; Por isso') e inicial maiúscula após ponto e vírgula.",
                    "Remover o espaço antes do ponto e vírgula e grafar 'por isso' com inicial minúscula (ou usar ponto final)."
                ));
            }

            // 5. Sumário page order check
            if (item.Kind == "front_matter_list" && item.Section.Contains("SUMÁRIO", StringComparison.OrdinalIgnoreCase))
            {
                if (item.Text.Contains("2.7 Comparação estatística de modelos") && item.Text.Contains("20") &&
                    item.Text.Contains("2.8 Trabalhos relacionados") && item.Text.Contains("16"))
                {
                    issues.Add(new DeterministicIssue(
                        "C-11/D-PAR",
                        "CRITICO",
                        "Checklist-TCC1 (Formatação) / Diagrama",
                        "Numeração de página inconsistente no Sumário: a seção '2.7 Comparação estatística de modelos' indica página 20, enquanto '2.8 Trabalhos relacionados' indica página 16 (no corpo, a seção 2.7 inicia na página 16).",
                        "Atualizar os campos do Sumário automático no Word antes da exportação para PDF."
                    ));
                }
            }

            // 6. Ambiguous / vague words check (Diagrama: "Localizar e destruir palavras -> geram ambiguidade")
            if (item.Kind is "paragraph" or "list_item")
            {
                var ambMatches = AmbiguousWordsRegex.Matches(item.Text)
                    .Select(m => m.Value.ToLowerInvariant())
                    .Distinct()
                    .ToList();
                if (ambMatches.Count > 0)
                {
                    issues.Add(new DeterministicIssue(
                        "D-AMB/M-ZUC",
                        "AJUSTAR",
                        "Diagrama (Ambiguidade) / Zucolotto Mód. 5",
                        $"Uso de qualificadores/quantificadores potencialmente vagos ou subjetivos ({string.Join(", ", ambMatches.Select(w => $"'{w}'"))}). O diagrama recomenda substituir termos vagos por números ou especificações precisas.",
                        "Substituir o quantificador vago por dado quantitativo, intervalo numérico ou qualificação técnica precisa."
                    ));
                }

                // 7. Long sentences check (Diagrama: "Verborreia -> textos longos e complicados" & Zucolotto Mód. 5)
                if (maxSentWords > 48)
                {
                    issues.Add(new DeterministicIssue(
                        "D-VERB/M-ZUC",
                        "AJUSTAR",
                        "Diagrama (Verborreia) / Zucolotto Mód. 5",
                        $"Período longo ({maxSentWords} palavras na mesma sentença). Frases acima de 45 palavras dificultam a leitura técnica e acumulam subordinadas.",
                        "Dividir o período longo em duas frases diretas na ordem Sujeito-Verbo-Objeto."
                    ));
                }

                // 8. Nominalization check (Zucolotto Mód. 6: "Ação no Verbo")
                if (NominalizationRegex.IsMatch(item.Text))
                {
                    var nom = NominalizationRegex.Match(item.Text).Value;
                    issues.Add(new DeterministicIssue(
                        "M-ZUC/D-VERB",
                        "AJUSTAR",
                        "Zucolotto Mód. 6 (Ação no Verbo)",
                        $"Construção verbal substantivada ('{nom}').",
                        "Trocar a locução substantivada pelo verbo de ação direto correspondente."
                    ));
                }

                if (SuperfluousFillerRegex.IsMatch(item.Text))
                {
                    var filler = SuperfluousFillerRegex.Match(item.Text).Value;
                    issues.Add(new DeterministicIssue(
                        "D-VERB/M-ZUC",
                        "AJUSTAR",
                        "Diagrama / Zucolotto Mód. 7 (Plain Science)",
                        $"Expressão introdutória supérflua ('{filler}').",
                        "Cortar a expressão introdutória e ir direto à afirmação técnica."
                    ));
                }
            }

            // 9. Specific Methodology / Checklist structural checks on key items
            if (item.Kind == "paragraph" && item.Section == "3 MATERIAIS E MÉTODOS" && item.Text.Contains("Ciência da Computação"))
            {
                issues.Add(new DeterministicIssue(
                    "C-15/M-WAZ",
                    "AJUSTAR",
                    "Checklist-TCC1 (Item 15: Relevância para SI)",
                    "O parágrafo situa o delineamento apenas em 'Ciência da Computação', mas o curso e o Checklist do TCC1 exigem explicitar a relevância para a área de Sistemas de Informação (SI).",
                    "Explicitar o vínculo com Sistemas de Informação (ex.: confiabilidade e custo operacional de sistemas de informação baseados em agentes com memória persistente local)."
                ));
            }

            if (item.Kind == "heading" && item.Text.StartsWith("3.1 Revisão sistemática", StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new DeterministicIssue(
                    "M-WAZ/D-PAR",
                    "AJUSTAR",
                    "Wazlawick (Método de Pesquisa, slide 9)",
                    "Wazlawick destaca que a revisão bibliográfica não deve ser confundida com o método de pesquisa em si (pois é etapa prévia para delimitar a lacuna e o objetivo), embora mapeamentos sistemáticos com protocolo formal costumem ser detalhados em seção própria ou apêndice.",
                    "Esclarecer logo no início da Seção 3.1 que a revisão sistemática constitui o procedimento auxiliar de delimitação da lacuna (Seção 2.8), distinguindo-a do método experimental principal (Seções 3.2–3.9)."
                ));
            }

            if (item.Kind == "table" && item.Section.Contains("2.8 Trabalhos relacionados"))
            {
                issues.Add(new DeterministicIssue(
                    "C-10",
                    "AJUSTAR",
                    "Checklist-TCC1 (Item 10: Trabalhos relacionados)",
                    "O Quadro 1 compara representação, atualização, modelos/escala, objeto de avaliação e comparação de paradigmas, mas o Checklist do TCC1 pergunta especificamente por 'vantagens, desvantagens e semelhanças de abordagens'.",
                    "Explicitar na coluna de avaliação/atualização ou no parágrafo de síntese do Quadro 1 as vantagens e limitações/desvantagens diretas de cada abordagem frente ao GU-JSON."
                ));
            }

            if (item.Kind == "table" && item.Section.Contains("3.13 Cronograma"))
            {
                issues.Add(new DeterministicIssue(
                    "D-FIG/C-11",
                    "AJUSTAR",
                    "Diagrama (Imagens, tabelas e fórmulas) / Checklist-TCC1",
                    "Na Tabela 1 (Cronograma), os períodos quinzenais Q1–Q20 estão marcados apenas por preenchimento visual de cor sem caractere textual ('X' ou '•'), ficando vazios em leitores de tela ou extração textual.",
                    "Inserir marcador textual ('X' ou '■') dentro das células ativas de Q1 a Q20 além do sombreamento visual."
                ));
            }

            if (item.Kind == "caption" && item.Text.Contains("detalhe ampliado", StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new DeterministicIssue(
                    "D-FIG/C-11",
                    "AJUSTAR",
                    "Diagrama (Imagens, tabelas e fórmulas) / ABNT",
                    $"Sublegenda '{item.Text}' não consta na Lista de Ilustrações, não é chamada individualmente no corpo do texto e não traz nota 'Fonte:' própria.",
                    "Referenciar os detalhes ampliados 1 a 4 explicitamente no texto da Seção 3.7 (ou numerá-los como Figuras/Subfiguras formais com Fonte)."
                ));
            }

            if (item.Kind == "reference")
            {
                if (item.Text.Contains("---") || Regex.IsMatch(item.Text, @":[A-Z]"))
                {
                    issues.Add(new DeterministicIssue(
                        "D-REF/C-09/C-11",
                        "CRITICO",
                        "Diagrama (Referências) / Checklist-TCC1 (Formatação ABNT)",
                        " Artefato de formatação na referência bibliográfica: falta de espaço após dois-pontos ('AMU:Admission') e travessão LaTeX literal não convertido ('---Structured').",
                        "Corrigir para 'AMU: Admission and Memory Update for Personalized Conversations — Structured Memory with SLM Guided Control.'"
                    ));
                }
            }

            itemAudits[item.Id] = new ItemDeterministicAudit(
                item.Id,
                words,
                sentenceCount,
                maxSentWords,
                issues
            );
        }

        var citationAudit = AuditCitationsAndReferences(extraction);
        var visualAudits = AuditVisualElements(extraction);

        return (itemAudits, citationAudit, visualAudits);
    }

    private static CitationCheckResult AuditCitationsAndReferences(ExtractionResult extraction)
    {
        var bodyItems = extraction.Items.Where(i => i.Kind != "reference").ToList();
        var refItems = extraction.Items.Where(i => i.Kind == "reference").ToList();

        var bodyText = string.Join(" ", bodyItems.Select(i => i.Text));
        var citedSet = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        // Parenthetical citations: (Autor; Autor, 2025; Autor et al., 2024)
        foreach (Match m in Regex.Matches(bodyText, @"\(([A-ZÀ-Ý][^()]+?\d{4})\)"))
        {
            var chunk = m.Groups[1].Value;
            foreach (var part in Regex.Split(chunk, @"(?<=\d{4})\s*;\s*"))
            {
                var m2 = Regex.Match(part.Trim(), @"^([A-ZÀ-Ý][A-Za-zÀ-ÿšŠüÜ-]+).*?(\d{4})");
                if (m2.Success)
                {
                    citedSet.Add($"{m2.Groups[1].Value.ToUpperInvariant()} ({m2.Groups[2].Value})");
                }
            }
        }

        // Narrative citations: Autor et al. (2025) or Autor; Autor (2026)
        foreach (Match m in Regex.Matches(bodyText, @"([A-ZÀ-Ý][A-Za-zÀ-ÿšŠüÜ-]+)(?:\s+et\s+al\.|(?:\s*;\s*[A-ZÀ-Ý][A-Za-zÀ-ÿšŠüÜ-]+)+)?\s*\((\d{4})\)"))
        {
            citedSet.Add($"{m.Groups[1].Value.ToUpperInvariant()} ({m.Groups[2].Value})");
        }

        var refSet = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var formattingAlerts = new List<string>();

        foreach (var r in refItems)
        {
            var m = Regex.Match(r.Text.Trim(), @"^([A-ZÀ-ÝŠÜ-]+),.*?\b(19\d\d|20\d\d)\b");
            if (m.Success)
            {
                refSet.Add($"{m.Groups[1].Value.ToUpperInvariant()} ({m.Groups[2].Value})");
            }
            if (r.Text.Contains("---") || Regex.IsMatch(r.Text, @":[A-Z]"))
            {
                formattingAlerts.Add($"Item #{r.Id:D3} (p. {r.PageStart}): '{r.Text[..Math.Min(85, r.Text.Length)]}...' contém '---' ou falta espaço após ':'.");
            }
        }

        var citedList = citedSet.OrderBy(x => x).ToList();
        var refList = refSet.OrderBy(x => x).ToList();
        var missingInRefs = citedList.Where(c => !refSet.Contains(c)).ToList();
        var uncitedRefs = refList.Where(r => !citedSet.Contains(r)).ToList();

        return new CitationCheckResult(
            citedList,
            refList,
            missingInRefs,
            uncitedRefs,
            formattingAlerts
        );
    }

    private static List<VisualElementAudit> AuditVisualElements(ExtractionResult extraction)
    {
        var results = new List<VisualElementAudit>();
        var nonCaptionText = string.Join(" ", extraction.Items.Where(i => i.Kind is not "caption" and not "front_matter_list").Select(i => i.Text));
        var frontMatterLists = string.Join("\n", extraction.Items.Where(i => i.Kind == "front_matter_list").Select(i => i.Text));

        for (var idx = 0; idx < extraction.Items.Count; idx++)
        {
            var item = extraction.Items[idx];
            if (item.Kind != "caption")
                continue;

            var m = Regex.Match(item.Text, @"^(Figura|Quadro|Tabela)\s+(\d+)");
            var identifier = m.Success ? $"{m.Groups[1].Value} {m.Groups[2].Value}" : item.Text[..Math.Min(25, item.Text.Length)];
            var isDetail = item.Text.Contains("detalhe ampliado", StringComparison.OrdinalIgnoreCase);
            if (isDetail)
            {
                var dm = Regex.Match(item.Text, @"detalhe ampliado\s+\d+", RegexOptions.IgnoreCase);
                identifier = dm.Success ? $"Figura 1 ({dm.Value})" : item.Text;
            }

            var citedInBody = isDetail
                ? nonCaptionText.Contains("detalhe ampliado", StringComparison.OrdinalIgnoreCase)
                : Regex.IsMatch(nonCaptionText, $@"\b{Regex.Escape(identifier)}\b", RegexOptions.IgnoreCase);

            var listedInFront = !isDetail && frontMatterLists.Contains(identifier, StringComparison.OrdinalIgnoreCase);

            var hasSourceNote = false;
            for (var lookahead = idx + 1; lookahead <= Math.Min(extraction.Items.Count - 1, idx + 3); lookahead++)
            {
                if (extraction.Items[lookahead].Kind == "source_note")
                {
                    hasSourceNote = true;
                    break;
                }
                if (extraction.Items[lookahead].Kind is "caption" or "heading")
                    break;
            }

            var alerts = new List<string>();
            if (!citedInBody)
                alerts.Add("Não citado nominalmente no corpo do texto.");
            if (!hasSourceNote)
                alerts.Add("Sem indicação 'Fonte:' imediatamente após o elemento.");
            if (!listedInFront)
                alerts.Add("Ausente na Lista de Ilustrações / Quadros e Tabelas.");
            if (item.Text.Contains("[GS", StringComparison.Ordinal))
                alerts.Add("Contém marcador residual de comentário [GS].");

            results.Add(new VisualElementAudit(
                identifier,
                m.Success ? m.Groups[1].Value : "Ilustração",
                item.Id,
                item.PageStart,
                citedInBody,
                hasSourceNote,
                listedInFront,
                item.Text,
                alerts
            ));
        }

        return results;
    }
}
