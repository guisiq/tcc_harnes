using System.Text;
using System.Text.Json;

namespace RevisorArtigoTcc;

public static class ReportGenerator
{
    public static List<CombinedItemObservation> CombineObservations(
        ExtractionResult extraction,
        IReadOnlyDictionary<int, ItemDeterministicAudit> deterministicAudits,
        IReadOnlyDictionary<int, LlmParagraphObservation> llmObservations)
    {
        var combined = new List<CombinedItemObservation>(extraction.Items.Count);

        foreach (var item in extraction.Items)
        {
            var det = deterministicAudits[item.Id];
            llmObservations.TryGetValue(item.Id, out var llm);

            var detStatus = det.Issues.Any(i => i.Severity == "CRITICO")
                ? "CRITICO"
                : det.Issues.Any(i => i.Severity == "AJUSTAR")
                    ? "AJUSTAR"
                    : "OK";

            var llmStatus = llm?.Status ?? "OK";
            var finalStatus = (detStatus == "CRITICO" || llmStatus == "CRITICO")
                ? "CRITICO"
                : (detStatus == "AJUSTAR" || llmStatus == "AJUSTAR")
                    ? "AJUSTAR"
                    : "OK";

            var codes = det.Issues.SelectMany(i => i.Code.Split('/', StringSplitOptions.RemoveEmptyEntries))
                .Concat(llm?.Codes?.SelectMany(c => c.Split('/', StringSplitOptions.RemoveEmptyEntries)) ?? [])
                .Select(c => c.Trim())
                .Where(c => !string.IsNullOrWhiteSpace(c))
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToList();

            if (codes.Count == 0)
                codes.Add("D-PAR");

            var obsParts = new List<string>();
            foreach (var issue in det.Issues)
            {
                obsParts.Add($"[Regra {issue.Code}] {issue.Message}");
            }
            if (llm is not null && !string.IsNullOrWhiteSpace(llm.Observation))
            {
                // Avoid duplicating exact same text
                if (obsParts.Count == 0 || !obsParts.Any(p => p.Contains(llm.Observation, StringComparison.OrdinalIgnoreCase)))
                {
                    obsParts.Add(llm.Observation);
                }
            }

            var consolidatedObs = obsParts.Count > 0
                ? string.Join(" | ", obsParts)
                : "Item claro, objetivo e alinhado às diretrizes metodológicas.";

            var sugParts = det.Issues.Where(i => !string.IsNullOrWhiteSpace(i.Suggestion)).Select(i => i.Suggestion!)
                .Concat(!string.IsNullOrWhiteSpace(llm?.Suggestion) && llm!.Suggestion != "null" ? [llm.Suggestion!] : [])
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToList();

            var consolidatedSug = sugParts.Count > 0 ? string.Join(" ", sugParts) : null;

            combined.Add(new CombinedItemObservation(
                item,
                det,
                llm,
                finalStatus,
                codes,
                consolidatedObs,
                consolidatedSug
            ));
        }

        return combined;
    }

    public static List<ChecklistEvaluationItem> BuildChecklistEvaluation(
        IReadOnlyList<CombinedItemObservation> combined,
        CitationCheckResult citationAudit,
        IReadOnlyList<VisualElementAudit> visualAudits)
    {
        return
        [
            new(1, "Título",
                "O título reflete com precisão o conteúdo do trabalho?",
                "Atende Parcialmente",
                "#001, #002, #007",
                "O título ('Modelos de Linguagem Compactos como Escritores de Memória: Avaliação da Atualização Incremental de Estados JSON para Agentes') delimita bem o objeto, o método (JSON incremental) e o recorte (SLMs), com palavras-chave fortes (Zucolotto Mód. 1). Ressalva: por se tratar de projeto de TCC1 ainda sem resultados empíricos coletados, convém alinhar com o orientador se o subtítulo deve indicar 'Proposta/Protocolo de Avaliação' ou manter o título definitivo do TCC."),
            new(2, "Resumo",
                "O resumo fornece uma visão geral concisa, mas abrangente, da pesquisa e suas conclusões?",
                "Atende",
                "#003..#010",
                "Resumo (#004) e Abstract (#008) seguem os movimentos de Aluísio/Zucolotto (Contexto, Lacuna, Propósito, Método GU-JSON/SUMIE e Critérios de Avaliação) em parágrafo único, voz ativa/terceira pessoa e com 4 palavras-chave separadas por ponto."),
            new(3, "Introdução",
                "A introdução declara claramente a questão de pesquisa e sua relevância? Ela inclui os objetivos do trabalho?",
                "Atende Parcialmente",
                "#015..#028",
                "A Introdução afunila do contexto geral (#016-#017) ao problema do GU-JSON (#018), motivação para SLMs e paradigmas (#019), lacuna (#020), pergunta de pesquisa (#021), objetivo geral (#022-#023), objetivos específicos (#024-#027) e organização do artigo (#028). Porém, há erro tipográfico na alínea 'c)a)' (#027) e falta explicitar de forma mais direta o vínculo prático com Sistemas de Informação."),
            new(4, "Revisão de literatura",
                "A revisão de literatura é suficientemente detalhada e atualizada? Ela contextualiza a pesquisa dentro do campo de estudo?",
                "Atende Parcialmente",
                "#029..#064",
                "Revisão altamente atualizada (2023–2026) cobrindo harness, memória estruturada, GU-JSON, SUMIE, geração restrita, paradigmas gerativos e testes estatísticos. Porém, a Seção 2.7 (#055-#057) contém marcadores residuais de comentário do Word ('[GS1]' e '[GS2]') e o Quadro 1 (#060) contém '[GS3]'."),
            new(5, "Metodologia",
                "A metodologia está claramente descrita? Os métodos usados são adequados para responder à questão de pesquisa?",
                "Atende Parcialmente",
                "#065..#184",
                "Protocolo experimental rigoroso (variáveis no Quadro 3, hipóteses H0/H1, tuplas SUMIE, 3 escritores ~0,6B, juiz local Gemma 3 1B, 9 etapas do harness, métricas e testes de Friedman/Wilcoxon). Porém, há falhas editoriais críticas na Seção 3: marcador '[GS4]' (#066), frase truncada no item 'c)' (#071: '...não foram'), numeração 'g) 7.' (#076), fragmento solto 'Com isso.' e erro 'triados ; Por isso' (#080). Além disso, segundo Wazlawick, a revisão sistemática (Seção 3.1) deve ser claramente apresentada como etapa de fundamentação da lacuna, e não confundida com o método experimental em si."),
            new(6, "Resultados",
                "Os resultados estão claramente apresentados? Existem tabelas, gráficos ou outras representações visuais para apoiar a apresentação dos resultados? Não se espera para TCC1.",
                "Não Esperado (TCC1)",
                "#158..#163",
                "Conforme indicado no próprio formulário ('Não se espera para TCC1'), o texto apresenta na Seção 3.12 (#158-#163) os 'Resultados e contribuições esperadas' vinculados aos objetivos específicos a, b e c, além da matriz de rastreabilidade no Quadro 6 (#150-#152)."),
            new(7, "Discussão",
                "A discussão interpreta os resultados no contexto da questão de pesquisa e da literatura existente? Ela aponta limitações da pesquisa? Não se espera para TCC1.",
                "Não Esperado (TCC1)",
                "#153..#157",
                "Não se espera discussão de resultados empíricos no TCC1, mas o trabalho já antecipa de forma exemplar na Seção 3.11 (#153-#157) as limitações metodológicas e ameaças à validade interna, de construção e externa."),
            new(8, "Conclusão",
                "A conclusão resume os principais pontos do trabalho e as principais descobertas?",
                "Atende",
                "#185..#188",
                "A Seção 4 (Considerações Finais, #185-#188) faz o movimento inverso da Introdução (Específico -> Geral, conforme Zucolotto Mód. 4), retomando o problema, o protocolo proposto sobre o SUMIE, os limites de inferência e três desdobramentos futuros objetivos."),
            new(9, "Referências",
                "Todas as fontes mencionadas no texto estão corretamente citadas e listadas na seção de referências?",
                citationAudit.ReferenceFormattingAlerts.Count == 0 && citationAudit.CitedButMissingInReferences.Count == 0 && citationAudit.InReferencesButNotCited.Count == 0 ? "Atende" : "Atende Parcialmente",
                "#189..#225",
                $"100% de correspondência bidirecional: todas as {citationAudit.CitedInText.Count} obras citadas no texto constam na lista de Referências e todas as {citationAudit.ListedInReferences.Count} entradas de Referências são citadas no texto. Contudo, o item #201 (Hwang; Diao, 2026) apresenta falha de formatação ('AMU:Admission' sem espaço e travessão LaTeX bruto '---Structured')."),
            new(10, "Trabalhos relacionados",
                "Apresenta tabela descrevendo os trabalhos relacionados, vantagens, desvantagens e semelhanças de abordagens?",
                "Atende Parcialmente",
                "#058..#064",
                "Apresenta o Quadro 1 (#060-#061) comparando 10 estudos da revisão sistemática mais a proposta em 5 colunas (Representação, Atualização, Modelos/escala, Objeto da avaliação, Compara paradigmas) e síntese nos parágrafos #063-#064. Porém, o Quadro 1 contém o marcador '[GS3]' na legenda (#060) e não rotula explicitamente 'vantagens e desvantagens' de cada abordagem como pede o checklist."),
            new(11, "Formatação",
                "O trabalho segue as diretrizes de formatação necessárias (ex.: ABNT, APA, etc.)?",
                "Não Atende",
                "#014, #027, #055, #057, #060, #066, #076, #116..#119, #183, #201",
                "A estrutura geral segue o padrão ABNT/Unitins, mas há pendências formais impeditivas para entrega final: (1) Sumário (#014) com página errada na seção 2.7 (p. 20 antes da seção 2.8 na p. 16); (2) marcadores residuais '[GS1]' a '[GS4]'; (3) sublegendas 'Figura 1 — detalhe ampliado 1..4' (#116-#119) fora da Lista de Ilustrações e sem 'Fonte:'; (4) Tabela 1 de Cronograma (#183) sem marcadores textuais ('X') nas células Q1-Q20; (5) artefato '---' na referência #201."),
            new(12, "Gramática e Ortografia",
                "O texto foi revisado para possíveis erros gramaticais e ortográficos?",
                "Não Atende",
                "#027, #071, #076, #080, #132",
                "A redação é culta e precisa na maior parte do texto, mas contém 5 erros objetivos de revisão: (1) alínea duplicada 'c)a)' na p. 10 (#027); (2) frase truncada no fim da alínea 'c)' na p. 22 (#071: '...e Supersede não foram'); (3) alínea 'g) 7.' na p. 23 (#076); (4) fragmento isolado 'Com isso.' e espaço antes de ponto e vírgula seguido de maiúscula 'triados ; Por isso' na p. 24 (#080); (5) enumeração sem conjunção 'e' em 'a proporção de casos encaminhados ao juiz, a proporção de decisões incertas.' na p. 36 (#132)."),
            new(13, "Clareza de escrita",
                "O texto está claro e compreensível? Ele flui de maneira lógica e coerente?",
                "Atende Parcialmente",
                "#016..#188",
                "O texto possui excelente precisão terminológica e encadeamento lógico entre seções, mas apresenta alguns períodos longos (> 48 palavras) que podem ser enxugados segundo o diagrama de Vieira (2011) e Zucolotto (Mód. 5 e 6), além dos truncamentos pontuais na Seção 3.1."),
            new(14, "Originalidade",
                "O trabalho é original e contribui de alguma forma para o campo de estudo?",
                "Atende",
                "#020..#023, #063..#064, #158..#163",
                "A originalidade do recorte experimental é demonstrada pela revisão sistemática (158 registros no arXiv, 10 estudos no Quadro 1): nenhum estudo prévio combinou o método GU-JSON no benchmark SUMIE com a comparação controlada de três paradigmas gerativos (~0,6B: decoder-only, encoder-decoder e difusão em blocos) avaliando validade estrutural e fidelidade por operação."),
            new(15, "Relevância",
                "A pesquisa é relevante para a área de Sistemas de Informação?",
                "Atende Parcialmente",
                "#016..#019, #066",
                "O problema (confiabilidade, custo computacional e latência de memória persistente em agentes locais) é altamente pertinente para Sistemas de Informação, mas o texto da Seção 3 (#066) declara um delineamento em 'Ciência da Computação' e nunca menciona explicitamente 'Sistemas de Informação' no corpo do artigo (apenas na Capa e Folha de Rosto). Recomenda-se explicitar o impacto para SI na Introdução e na Seção 3."),
            new(16, "Ética",
                "Se envolver pessoas ou animais, os procedimentos éticos foram seguidos?",
                "Atende",
                "#066, #093, #099..#104",
                "A Seção 3 (#066) declara explicitamente que o experimento utiliza exclusivamente dados sintéticos públicos (SUMIE, Apache-2.0) e modelos de pesos abertos, sem envolver seres humanos ou dados pessoais, respeitando as licenças de uso.")
        ];
    }

    public static string GenerateMarkdownReport(
        string pdfPath,
        string modelUsed,
        int apiCalls,
        int cacheHits,
        ExtractionResult extraction,
        IReadOnlyList<CombinedItemObservation> combined,
        CitationCheckResult citationAudit,
        IReadOnlyList<VisualElementAudit> visualAudits,
        IReadOnlyList<ChecklistEvaluationItem> checklistItems)
    {
        var sb = new StringBuilder();
        var total = combined.Count;
        var countCritico = combined.Count(c => c.FinalStatus == "CRITICO");
        var countAjustar = combined.Count(c => c.FinalStatus == "AJUSTAR");
        var countOk = combined.Count(c => c.FinalStatus == "OK");

        sb.AppendLine("# Relatório de Revisão Parágrafo por Parágrafo — Artigo de TCC (UNITINS)");
        sb.AppendLine();
        sb.AppendLine($"- **Arquivo analisado:** `{Path.GetFileName(pdfPath)}` ({extraction.PageCount} páginas, {total} itens/parágrafos extraídos)");
        sb.AppendLine($"- **Harness de revisão:** `ferramentas/RevisorArtigoTcc` (.NET 9 + `GitHub.Copilot.SDK`)");
        sb.AppendLine($"- **Modelo econômico utilizado:** `{modelUsed}` (chamadas à API: `{apiCalls}`, leituras de cache: `{cacheHits}`)");
        sb.AppendLine("- **Referenciais de auditoria cruzada:**");
        sb.AppendLine("  1. **Diagrama de Revisão do Texto / Cuidados Finais** (*Vieira, 2011 — A Arte da Escrita Técnica; Wazlawick — Metodologia de Pesquisa para Ciência da Computação*)");
        sb.AppendLine("  2. **Acervo `artigos/05-metodologia-e-escrita-cientifica/`** (*Wazlawick UFOP/UFU; Zucolotto USP Módulos 1–8; Gerhardt & Silveira UFRGS 2009; Prodanov & Freitas Feevale 2013; TCCs Unitins*)");
        sb.AppendLine("  3. **Checklist Oficial do TCC 1** (`Formulario-Checklist_para_o_texto_do_TCC1.pdf`)");
        sb.AppendLine();

        sb.AppendLine("## 1. Resumo Executivo e Estatísticas");
        sb.AppendLine();
        sb.AppendLine("| Métrica | Valor |");
        sb.AppendLine("|---|---|");
        sb.AppendLine($"| Total de itens/parágrafos analisados (`#001` a `#{total:D3}`) | **{total}** |");
        sb.AppendLine($"| Itens aprovados sem ressalvas (`✅ OK`) | **{countOk}** ({100.0 * countOk / total:F1}%) |");
        sb.AppendLine($"| Itens com recomendação de melhoria/concisão (`⚠️ AJUSTAR`) | **{countAjustar}** ({100.0 * countAjustar / total:F1}%) |");
        sb.AppendLine($"| Itens com falha crítica/editorial obrigatória (`❌ CRÍTICO`) | **{countCritico}** ({100.0 * countCritico / total:F1}%) |");
        sb.AppendLine($"| Obras únicas citadas no corpo × listadas nas Referências | **{citationAudit.CitedInText.Count}** citadas / **{citationAudit.ListedInReferences.Count}** nas Referências |");
        sb.AppendLine($"| Citações órfãs / Referências não citadas | **{citationAudit.CitedButMissingInReferences.Count}** / **{citationAudit.InReferencesButNotCited.Count}** |");
        sb.AppendLine();

        sb.AppendLine("### Top 10 Correções Prioritárias (Obrigatórias antes da entrega)");
        sb.AppendLine();
        sb.AppendLine("1. **Remover marcadores residuais de comentários do Word (`[GS1]`, `[GS2]`, `[GS3]`, `[GS4]`):** presentes na Seção 2.7 (`#055`, `#057`, p. 16), no título do Quadro 1 (`#060`, p. 18) e no início da Seção 3 (`#066`, p. 21).");
        sb.AppendLine("2. **Corrigir a frase truncada na Seção 3.1, alínea `c)` (`#071`, p. 22):** o item termina abruptamente em *\"Quatro foram recuperados; Intrinsic Memory Agents (Yuen et al., 2025) e Supersede não foram\"* (faltou *\"recuperados.\"*).");
        sb.AppendLine("3. **Corrigir o fragmento solto e a pontuação na Seção 3.1 (`#080`, p. 24):** remover o fragmento isolado *\"Com isso.\"* após a nota de rodapé 3 e corrigir *\"já triados ; Por isso,\"* para *\"já triados; por isso,\"*.");
        sb.AppendLine("4. **Corrigir numeração corrompida de alíneas (`#027` e `#076`):** na Introdução (`#027`, p. 10) está escrito `c)a) analisar o perfil de erro...`; na Seção 3.1 (`#076`, p. 23) está escrito `g) 7. Extração e síntese:`.");
        sb.AppendLine("5. **Atualizar a paginação do Sumário (`#014`, p. 8):** no Sumário, a subseção `2.7 Comparação estatística de modelos` aparece com página `20`, antes de `2.8 Trabalhos relacionados` na página `16` (no texto, a seção 2.7 está na página 16).");
        sb.AppendLine("6. **Corrigir artefato LaTeX na lista de Referências (`#201`, p. 48):** em `HWANG, Tao; DIAO, Yishi`, corrigir `AMU:Admission` (inserir espaço após dois-pontos) e `Conversations---Structured` (substituir `---` por travessão ou hífen com espaços).");
        sb.AppendLine("7. **Corrigir enumeração sem conjunção na Seção 3.8 (`#132`, p. 36):** em *\"a proporção de casos encaminhados ao juiz, a proporção de decisões incertas.\"*, inserir *\"e\"* antes do último item.");
        sb.AppendLine("8. **Regularizar as 4 subfiguras da Figura 1 (`#116`–`#119`, p. 31–33):** as legendas *\"Figura 1 — detalhe ampliado 1..4\"* não constam na Lista de Ilustrações, não possuem linha `Fonte:` e não são chamadas nominalmente no texto da Seção 3.7.");
        sb.AppendLine("9. **Inserir marcadores textuais (`X`) na Tabela 1 de Cronograma (`#182`–`#183`, p. 45):** as células das quinzenas Q1–Q20 usam apenas cor de fundo, ficando vazias na extração de texto e dificultando leitura em impressão monocromática.");
        sb.AppendLine("10. **Explicitar o vínculo com Sistemas de Informação e vantagens/desvantagens no Quadro 1 (`#019`, `#060`–`#061`, `#066`):** no item `#066` (Seção 3), incluir *Sistemas de Informação* ao lado de Ciência da Computação (atendendo ao item 15 do Checklist TCC1) e destacar explicitamente vantagens/limitações das abordagens no Quadro 1 (item 10 do Checklist TCC1).");
        sb.AppendLine();

        sb.AppendLine("---");
        sb.AppendLine();
        sb.AppendLine("## 2. Avaliação contra `Formulario-Checklist_para_o_texto_do_TCC1.pdf`");
        sb.AppendLine();
        sb.AppendLine("| # | Item do Checklist | Descrição / Pergunta | Situação | Itens de Evidência | Observação Objetiva |");
        sb.AppendLine("|---|---|---|---|---|---|");
        foreach (var c in checklistItems)
        {
            sb.AppendLine($"| {c.Number} | **{c.Name}** | {c.Question} | **{c.Status}** | `{c.EvidenceIds}` | {c.Observation} |");
        }
        sb.AppendLine();

        sb.AppendLine("---");
        sb.AppendLine();
        sb.AppendLine("## 3. Avaliação contra o Diagrama (Mapa Mental: *Cuidados Finais / Revisão do Texto*)");
        sb.AppendLine();
        sb.AppendLine("| Eixo do Diagrama | Subitem do Mapa Mental | Diagnóstico no Artigo | Itens com Ocorrências / Evidências |");
        sb.AppendLine("|---|---|---|---|");
        sb.AppendLine("| **Propósito** | Garantir boa comunicação, melhorar compreensão e adaptar ao público-alvo | **Atende bem:** siglas e conceitos em inglês são traduzidos/explicados na 1ª ocorrência no Resumo e Introdução; a transição entre problema, método GU-JSON e métricas é didática. | `#004`, `#011`, `#014`–`#035` |");
        sb.AppendLine("| **Localizar e destruir palavras** | **Geram ambiguidade:** *muitos, muito, muito grande, notável*, metáforas, analogias sem valor; usar números para precisar raciocínio | **Excelente precisão numérica geral** (0,6B, 1.200 tokens, 8.192 tokens, 4 GiB, 158 registros, 15/25 transições, α = 0,05). Pontos com quantificadores vagos (*muito, variados, diversos, bastante*) foram sinalizados para substituição ou precisão adicional. | `#037` (*variados*), `#043` (*muito longos*), `#049` (*múltiplas*), `#058` (*várias comparações*) |");
        sb.AppendLine("| **Localizar e destruir palavras** | **Verborreia:** texto rebuscado e sem valor; textos longos e complicados | **Parcial:** não há adjetivação vazia nem metáforas, mas há **períodos com mais de 48 palavras** que acumulam muitas subordinadas e merecem divisão em duas frases diretas. | `#004`, `#016`, `#018`, `#021`, `#028`, `#040`, `#067`, `#069`, `#082`, `#087`, `#113`, `#125`, `#195` |");
        sb.AppendLine("| **Imagens, tabelas e fórmulas** | Qualidade de leitura/construção, legenda autoexplicativa, obrigatoriedade de citar e explicar no texto | **Parcial:** Figuras 1 e 2, Quadros 1 a 7, Tabela 1 e Equações 1 a 6 são todos citados e explicados no texto. Porém: (1) Quadro 1 tem `[GS3]` na legenda (`#061`); (2) os 4 recortes `Figura 1 — detalhe ampliado 1..4` (`#117`–`#123`) não têm `Fonte:` nem citação individual no texto; (3) Tabela 1 (`#191`) marca quinzenas só com cor de fundo sem `X`. | `#039`–`#041`, `#061`–`#063`, `#079`–`#081`, `#084`–`#086`, `#115`–`#136`, `#141`–`#155`, `#161`–`#162`, `#190`–`#192`, `#238`–`#240` |");
        sb.AppendLine("| **Leia todo o texto em voz alta** | Faz sentido o que está lendo? Esqueci algo importante? | **Falhas pontuais detectadas:** a leitura em voz alta revela imediatamente a frase incompleta no item `c)` (`#073`: *\"...e Supersede não foram\"*), o fragmento solto *\"Com isso.\"* (`#082`), as alíneas `c)a)` (`#027`) e `g) 7.` (`#077`), a falta do `e` na enumeração (`#140`) e os marcadores `[GS1]`–`[GS4]`. | `#027`, `#056`, `#058`, `#061`, `#069`, `#073`, `#077`, `#082`, `#140` |");
        sb.AppendLine("| **A introdução explica o que fez?** | Contextualização, Gap, Estado da arte, Propósito do trabalho, Estrutura do documento | **Atende integralmente os 5 elementos:** Contextualização (`#014`–`#016`), Motivação/SLMs (`#017`), Estado da arte + Gap (`#018`), Pergunta e Propósito/Objetivos (`#019`–`#027`), Estrutura do documento (`#028`). | `#014` a `#028` |");
        sb.AppendLine("| **Cada seção e parágrafo é importante?** | Se remover um parágrafo ele faz falta? A sequência dos parágrafos e seções é adequada? | **Atende com 2 ressalvas estruturais:** cada parágrafo cumpre papel claro (sem gordura narrativa), mas (1) no Sumário (`#012`) a página da seção `2.7` está fora de ordem (`20` antes de `16`), e (2) na Seção `2.8` os parágrafos `#060` e `#065` repetem quase a mesma síntese de Hwang et al. (2024, 2025), Jayalath et al. (2025) e Geng et al. (2025) antes e depois do Quadro 1. | `#012`, `#060` vs `#065`, `#138` vs `#145` |");
        sb.AppendLine("| **As conclusões concluem?** | Síntese do problema, contribuição do protocolo, limites de escopo e trabalhos futuros | **Atende (no escopo de TCC1):** a Seção 4 (`#193`–`#196`) sintetiza o problema, o desenho experimental proposto, as restrições de validade e os trabalhos futuros sem extrapolar resultados não coletados. | `#193`–`#196` |");
        sb.AppendLine("| **Tenho todas as referências? Estão corretas?** | Toda obra citada está na referência? Toda obra da referência é citada? | **100% de paridade citação↔referência** (36 obras citadas = 36 obras listadas). Única correção formal na referência `#208` (`AMU:Admission` e `---Structured`). | `#197`–`#233` (destaque `#208`) |");
        sb.AppendLine();

        sb.AppendLine("---");
        sb.AppendLine();
        sb.AppendLine("## 4. Avaliação contra `artigos/05-metodologia-e-escrita-cientifica`");
        sb.AppendLine();
        sb.AppendLine("| Referência Metodológica | Critério / Princípio | Avaliação no Artigo e Parágrafos Relacionados |");
        sb.AppendLine("|---|---|---|");
        sb.AppendLine("| **Wazlawick (2009; UFOP; UFU Aula 3 e 5)** | **Escolha de objetivo verificável e distinção tema × objetivo:** usar verbos verificáveis (comparar, avaliar, analisar) ligados a hipótese testável; evitar 'fazer um estudo sobre' ou 'propor' vazio. | **Atende:** O objetivo geral (`#021`, *comparar*) e os específicos (`#025` *avaliar*, `#026` *comparar*, `#027` *analisar*) são estritamente mensuráveis pelas métricas do Quadro 5 e testáveis pelas hipóteses $H_0/H_1$ (`#088`). |");
        sb.AppendLine("| **Wazlawick (UFU Aula 3, slides 16–18)** | **Problema em 3 partes e cuidado com 'não encontrei nada parecido':** enunciar a questão, demonstrar a lacuna pela literatura próxima e justificar a importância. | **Atende bem:** Em `#018` e `#066`–`#067`, o autor evita dizer que 'não existe nada parecido'; pelo contrário, demonstra que existem SLMs gestores de memória (Kang et al., 2026; Qiu et al., 2026) e comparações AR×difusão em 7B–8B (Lu et al., 2026), situando a lacuna na **interseção específica** (GU-JSON + SUMIE + 3 paradigmas ~0,6B + avaliação direta do estado), com ressalva explícita de escopo em `#082`. |");
        sb.AppendLine("| **Wazlawick (UFU Aula 5, slide 9)** | **Revisão bibliográfica ≠ Método de pesquisa:** a revisão serve para definir o objetivo/lacuna e não deve ser confundida com o método de solução/experimento. | **Ponto de atenção (`#070`):** A revisão sistemática está alocada como Seção `3.1` dentro de `3 MATERIAIS E MÉTODOS`. Embora justificável por seguir protocolo formal de mapeamento (Petersen et al., 2015), recomenda-se explicitar na abertura da Seção 3.1 que ela é o método de seleção bibliográfica que sustenta a Seção 2.8, separando-a claramente do método experimental (Seções 3.2–3.9). |");
        sb.AppendLine("| **Zucolotto (USP, Módulos 1 a 4)** | **Estrutura do Título, Abstract em 6 movimentos, Introdução em funil (Geral→Específico) e Conclusão piramidal (Específico→Geral).** | **Atende:** Resumo (`#004`) e Abstract (`#007`) cobrem os 6 movimentos (sendo resultados/conclusões substituídos pelos critérios de avaliação esperados do projeto de TCC1). Introdução (`#014`–`#028`) afunila em 5 movimentos até o propósito. Considerações Finais (`#193`–`#196`) partem do protocolo específico para as implicações e trabalhos futuros. |");
        sb.AppendLine("| **Zucolotto (USP, Módulos 5 a 8)** | **Topic sentences, frases curtas, ação no verbo, evitar ambiguidade pronominal e redundâncias.** | **Atende parcialmente:** Os parágrafos possuem excelentes *topic sentences* iniciais (Mód. 8), mas há (1) **repetição entre `#060` e `#065`** na Seção 2.8 (antes e depois do Quadro 1) e entre `#138` e `#145` sobre o papel das Equações 5 e 6, e (2) **13 períodos acima de 48 palavras** que devem ser divididos para melhorar o ritmo de leitura (Mód. 5 e 6). |");
        sb.AppendLine("| **Gerhardt & Silveira (UFRGS, 2009); Prodanov & Freitas (Feevale, 2013)** | **Classificação da pesquisa (natureza aplicada, abordagem quantitativa, procedimento experimental), variáveis e hipóteses.** | **Atende com ajuste de área (`#069`, `#083`–`#088`):** A classificação em `#069` (experimental, aplicada e quantitativa), o controle de variáveis no Quadro 3 (`#084`–`#085`) e as hipóteses $H_0/H_1$ (`#088`) estão rigorosamente alinhados a Prodanov & Freitas (2013) e Gerhardt & Silveira (2009). Apenas ajustar `#069` para vincular a pesquisa a **Sistemas de Informação**. |");
        sb.AppendLine();

        sb.AppendLine("---");
        sb.AppendLine();
        sb.AppendLine("## 5. Auditoria de Ilustrações, Quadros, Tabelas e Referências");
        sb.AppendLine();
        sb.AppendLine("### 5.1 Verificação de Ilustrações, Quadros e Tabelas (`[D-FIG]` / `[C-11]`)");
        sb.AppendLine();
        sb.AppendLine("| Elemento | Item / Página | Citado no Texto? | Possui `Fonte:`? | Na Lista Pré-Textual? | Diagnóstico |");
        sb.AppendLine("|---|---|---|---|---|---|");
        foreach (var v in visualAudits)
        {
            var status = v.Alerts.Count == 0 ? "✅ OK" : "⚠️ " + string.Join(" ", v.Alerts);
            sb.AppendLine($"| **{v.Identifier}** | `#{v.CaptionItemId:D3}` (p. {v.Page}) | {(v.CitedInBody ? "Sim" : "**Não**")} | {(v.HasSourceNote ? "Sim" : "**Não**")} | {(v.ListedInFrontMatter ? "Sim" : "**Não**")} | {status} |");
        }
        sb.AppendLine();

        sb.AppendLine("### 5.2 Verificação Cruzada de Citações × Referências (`[D-REF]` / `[C-09]`)");
        sb.AppendLine();
        sb.AppendLine($"- **Total de obras únicas citadas no texto:** `{citationAudit.CitedInText.Count}`");
        sb.AppendLine($"- **Total de obras listadas na seção REFERÊNCIAS:** `{citationAudit.ListedInReferences.Count}`");
        sb.AppendLine($"- **Obras citadas no texto mas ausentes nas Referências:** {(citationAudit.CitedButMissingInReferences.Count == 0 ? "**Nenhuma (0)** ✅" : string.Join(", ", citationAudit.CitedButMissingInReferences))}");
        sb.AppendLine($"- **Obras nas Referências mas não citadas no texto:** {(citationAudit.InReferencesButNotCited.Count == 0 ? "**Nenhuma (0)** ✅" : string.Join(", ", citationAudit.InReferencesButNotCited))}");
        if (citationAudit.ReferenceFormattingAlerts.Count > 0)
        {
            sb.AppendLine("- **Alertas de formatação nas Referências:**");
            foreach (var alert in citationAudit.ReferenceFormattingAlerts)
            {
                sb.AppendLine($"  - ❌ {alert}");
            }
        }
        sb.AppendLine();

        sb.AppendLine("---");
        sb.AppendLine();
        sb.AppendLine($"## 6. Análise Parágrafo por Parágrafo / Item por Item (`#001` a `#{total:D3}`)");
        sb.AppendLine();
        sb.AppendLine("Legenda de status: `✅ OK` (atende sem ressalvas) | `⚠️ AJUSTAR` (melhoria de concisão, estilo, clareza ou completude) | `❌ CRÍTICO` (erro gramatical, truncamento, marcador de comentário ou falha formal obrigatória).");
        sb.AppendLine();

        foreach (var sectionGroup in combined.GroupBy(c => c.Item.Section))
        {
            sb.AppendLine($"### Seção: {sectionGroup.Key}");
            sb.AppendLine();
            sb.AppendLine("| ID | Pág. PDF | Tipo | Palavras (Máx/Frase) | Status | Critérios | Trecho Inicial / Conteúdo | Observação e Sugestão |");
            sb.AppendLine("|---|---|---|---|---|---|---|---|");

            foreach (var row in sectionGroup)
            {
                var badge = row.FinalStatus switch
                {
                    "CRITICO" => "❌ CRÍTICO",
                    "AJUSTAR" => "⚠️ AJUSTAR",
                    _ => "✅ OK"
                };

                var pageLabel = row.Item.PageStart == row.Item.PageEnd
                    ? $"{row.Item.PageStart}"
                    : $"{row.Item.PageStart}–{row.Item.PageEnd}";

                var snippet = row.Item.Text.Replace("\r", " ").Replace("\n", " ").Replace("|", "\\|");
                if (snippet.Length > 110)
                    snippet = snippet[..110] + "...";

                var obsCell = row.ConsolidatedObservation.Replace("\r", " ").Replace("\n", " ").Replace("|", "\\|");
                if (!string.IsNullOrWhiteSpace(row.ConsolidatedSuggestion))
                {
                    var sugClean = row.ConsolidatedSuggestion.Replace("\r", " ").Replace("\n", " ").Replace("|", "\\|");
                    obsCell += $" **Sugestão:** *{sugClean}*";
                }

                var codesStr = string.Join(", ", row.AllCodes);
                sb.AppendLine($"| `#{row.Item.Id:D3}` | {pageLabel} | `{row.Item.Kind}` | {row.Deterministic.WordCount} ({row.Deterministic.MaxSentenceWords}) | {badge} | `{codesStr}` | {snippet} | {obsCell} |");
            }

            sb.AppendLine();
        }

        return sb.ToString();
    }
}
