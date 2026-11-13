#!/usr/bin/env dotnet
// Busca focada: snapshots Atom do arXiv, lotes, inventário, RIS e quadro comparativo.
// dotnet run scripts/busca_focada.cs -- coletar|preparar|relatorio|offline [--dados pasta] [--protocolo json] [--saida pasta]
#:property Nullable=enable
#:property PublishAot=false
#:property InvariantGlobalization=false

using System.Globalization;
using System.Security.Cryptography;
using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Xml.Linq;

Console.OutputEncoding = Encoding.UTF8;
var opcoes = Opcoes.Ler(args);
if (opcoes.Comando is not ("coletar" or "preparar" or "relatorio" or "offline"))
{
    Console.Error.WriteLine("Uso: busca_focada.cs coletar|preparar|relatorio|offline [--dados pasta] [--protocolo json] [--saida pasta]");
    return 2;
}

var diretorioScript = AppContext.GetData("EntryPointFileDirectoryPath") as string
    ?? throw new InvalidOperationException("Não foi possível localizar o diretório do script.");
var raiz = Path.GetFullPath(Path.Combine(diretorioScript, ".."));
var protocoloPath = Path.GetFullPath(opcoes.Valor("protocolo") ?? Path.Combine(raiz, "protocolo", "protocolo_focado_estrito.json"));
var dados = Path.GetFullPath(opcoes.Valor("dados") ?? Path.Combine(raiz, "dados", "execucao_focada_estrita_2026-11-12"));
var saida = Path.GetFullPath(opcoes.Valor("saida") ?? Path.Combine(raiz, ".."));
var processo = new Busca(raiz, dados, saida, protocoloPath);

switch (opcoes.Comando)
{
    case "coletar":
        await processo.Coletar();
        processo.Preparar();
        break;
    case "preparar": processo.Preparar(); break;
    case "relatorio": processo.Relatorio(); break;
    case "offline":
        processo.Preparar();
        processo.Relatorio();
        break;
}
return 0;

sealed class Opcoes
{
    public string Comando { get; private init; } = "";
    readonly Dictionary<string, string> valores = new(StringComparer.Ordinal);

    public static Opcoes Ler(string[] args)
    {
        var opcoes = new Opcoes { Comando = args.FirstOrDefault() ?? "" };
        for (int i = 1; i < args.Length; i++)
        {
            if (!args[i].StartsWith("--", StringComparison.Ordinal) || i + 1 >= args.Length ||
                args[i + 1].StartsWith("--", StringComparison.Ordinal))
                throw new ArgumentException($"Opção ou valor inválido: {args[i]}");
            string chave = args[i][2..];
            if (chave is not ("dados" or "protocolo" or "saida") || !opcoes.valores.TryAdd(chave, args[++i]))
                throw new ArgumentException($"Opção desconhecida ou repetida: --{chave}");
        }
        return opcoes;
    }

    public string? Valor(string chave) => valores.GetValueOrDefault(chave);
}

sealed class Busca
{
    static readonly JsonSerializerOptions Json = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true,
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    };
    static readonly JsonSerializerOptions JsonFormatado = new(Json) { WriteIndented = true };
    static readonly XNamespace Atom = "http://www.w3.org/2005/Atom";
    static readonly XNamespace OpenSearch = "http://a9.com/-/spec/opensearch/1.1/";
    static readonly UTF8Encoding Utf8 = new(false);
    static readonly CultureInfo PtBr = CultureInfo.GetCultureInfo("pt-BR");

    readonly string raiz, dados, saida, protocoloPath;
    readonly Protocolo protocolo;
    readonly DateOnly inicio, fim;

    public Busca(string raiz, string dados, string saida, string protocoloPath)
    {
        this.raiz = raiz;
        this.dados = dados;
        this.saida = saida;
        this.protocoloPath = protocoloPath;
        protocolo = Ler<Protocolo>(protocoloPath);
        inicio = DateOnly.ParseExact(protocolo.Inicio, "yyyy-MM-dd", CultureInfo.InvariantCulture);
        fim = DateOnly.ParseExact(protocolo.Fim, "yyyy-MM-dd", CultureInfo.InvariantCulture);
        if (fim < inicio || protocolo.Pagina is < 1 or > 2000 || protocolo.IntervaloSegundos < 3 ||
            protocolo.Consultas.Count == 0 || protocolo.Consultas.Any(c =>
                !Regex.IsMatch(c.Id, @"^[A-Za-z0-9_-]+$") || string.IsNullOrWhiteSpace(c.Expressao)) ||
            protocolo.Consultas.Select(c => c.Id).Distinct(StringComparer.Ordinal).Count() != protocolo.Consultas.Count)
            throw new InvalidDataException("Protocolo inválido: verifique janela, página, intervalo e consultas.");
    }

    string Caminho(params string[] partes) => Path.Combine([dados, .. partes]);
    static string Hash(string path) => Convert.ToHexStringLower(SHA256.HashData(File.ReadAllBytes(path)));
    static T Ler<T>(string path) =>
        JsonSerializer.Deserialize<T>(File.ReadAllText(path, Utf8), Json)
        ?? throw new InvalidDataException($"JSON vazio: {path}");
    static void Gravar<T>(string path, T valor) =>
        File.WriteAllText(path, JsonSerializer.Serialize(valor, JsonFormatado) + "\n", Utf8);
    static string Linha<T>(T valor) => JsonSerializer.Serialize(valor, Json);
    static List<T> LerJsonl<T>(string path) => File.ReadLines(path, Utf8)
        .Where(l => !string.IsNullOrWhiteSpace(l))
        .Select(l => JsonSerializer.Deserialize<T>(l, Json) ?? throw new InvalidDataException($"Linha JSON vazia em {path}"))
        .ToList();
    static string Limpar(string? texto) => Regex.Replace(texto ?? "", @"\s+", " ").Trim();
    static string N(int numero) => numero.ToString("N0", PtBr);

    public async Task Coletar()
    {
        string raw = Caminho("arxiv");
        if (Directory.Exists(raw) && Directory.EnumerateFiles(raw).Any())
            throw new InvalidOperationException($"A pasta {raw} já contém snapshots. Use outra pasta --dados para uma nova coleta.");
        Directory.CreateDirectory(raw);
        using var cliente = new HttpClient { Timeout = TimeSpan.FromMinutes(2) };
        cliente.DefaultRequestHeaders.UserAgent.ParseAdd("tcc-mapeamento-focado/1.0");
        var manifesto = new Manifesto
        {
            DataUtc = DateTimeOffset.UtcNow.ToString("O", CultureInfo.InvariantCulture),
            ProtocoloSha256 = Hash(protocoloPath)
        };
        bool primeiraRequisicao = true;
        foreach (var consulta in protocolo.Consultas)
        {
            string janela = $"submittedDate:[{inicio:yyyyMMdd}0000 TO {fim:yyyyMMdd}2359]";
            string query = $"({consulta.Expressao}) AND {janela}";
            var log = new ConsultaManifesto { Id = consulta.Id, Expressao = query };
            int deslocamento = 0;
            int? total = null;
            do
            {
                if (!primeiraRequisicao)
                    await Task.Delay(TimeSpan.FromSeconds(protocolo.IntervaloSegundos));
                primeiraRequisicao = false;
                string url = "https://export.arxiv.org/api/query?search_query=" + Uri.EscapeDataString(query) +
                    $"&start={deslocamento}&max_results={protocolo.Pagina}&sortBy=submittedDate&sortOrder=ascending";
                using var resposta = await cliente.GetAsync(url);
                string xml = await resposta.Content.ReadAsStringAsync();
                if (!resposta.IsSuccessStatusCode)
                    throw new HttpRequestException($"arXiv {consulta.Id}, página {deslocamento}: HTTP {(int)resposta.StatusCode}.");
                var feed = XDocument.Parse(xml).Root ?? throw new InvalidDataException($"Feed vazio em {consulta.Id}.");
                int informado = Total(feed);
                if (total.HasValue && total.Value != informado)
                    throw new InvalidDataException($"O total de {consulta.Id} mudou durante a paginação ({total} para {informado}).");
                total = informado;
                var entradas = feed.Elements(Atom + "entry").ToList();
                foreach (var entrada in entradas) _ = Identificador(entrada);
                if (entradas.Count == 0 && deslocamento < total)
                    throw new InvalidDataException($"arXiv retornou página vazia para {consulta.Id}, faltando resultados.");
                string nome = $"{consulta.Id}_{deslocamento:D5}.xml";
                string path = Path.Combine(raw, nome);
                File.WriteAllText(path, xml, Utf8);
                log.Paginas.Add(new Pagina { Arquivo = nome, Inicio = deslocamento, Retornados = entradas.Count, Sha256 = Hash(path) });
                deslocamento += entradas.Count;
                Console.WriteLine($"{consulta.Id}: {deslocamento}/{total}");
            } while (deslocamento < total);
            if (deslocamento != total)
                throw new InvalidDataException($"A contagem coletada de {consulta.Id} difere do total informado.");
            log.Total = total!.Value;
            manifesto.Consultas.Add(log);
        }
        Gravar(Caminho("manifesto.json"), manifesto);
        Console.WriteLine($"Snapshots e manifesto gravados em {dados}.");
    }

    static int Total(XElement feed)
    {
        var valor = feed.Element(OpenSearch + "totalResults")?.Value;
        return int.TryParse(valor, NumberStyles.None, CultureInfo.InvariantCulture, out int total) && total >= 0
            ? total : throw new InvalidDataException("O feed do arXiv não informou totalResults válido.");
    }

    static string Identificador(XElement entrada)
    {
        string id = entrada.Element(Atom + "id")?.Value ?? "";
        if (!Uri.TryCreate(id, UriKind.Absolute, out var uri) ||
            !uri.Host.EndsWith("arxiv.org", StringComparison.OrdinalIgnoreCase) ||
            !uri.AbsolutePath.StartsWith("/abs/", StringComparison.Ordinal))
            throw new InvalidDataException($"Identificador arXiv inválido no feed: {id}");
        string semVersao = Regex.Replace(uri.Segments.Last(), @"v\d+$", "");
        return Regex.IsMatch(semVersao, @"^\d{4}\.\d{4,5}$")
            ? semVersao : throw new InvalidDataException($"Identificador inesperado: {id}");
    }

    List<Artigo> CarregarSnapshots(out Manifesto manifesto, out int foraJanela)
    {
        manifesto = Ler<Manifesto>(Caminho("manifesto.json"));
        if (!string.Equals(manifesto.ProtocoloSha256, Hash(protocoloPath), StringComparison.Ordinal))
            throw new InvalidDataException("O protocolo não corresponde ao hash registrado no manifesto da coleta.");
        if (!manifesto.Consultas.Select(c => c.Id).SequenceEqual(protocolo.Consultas.Select(c => c.Id)))
            throw new InvalidDataException("As consultas do manifesto não correspondem ao protocolo.");

        var trabalhos = new Dictionary<string, Artigo>(StringComparer.Ordinal);
        var fora = new HashSet<string>(StringComparer.Ordinal);
        foreach (var consulta in manifesto.Consultas)
        {
            var vistosNaConsulta = new HashSet<string>(StringComparer.Ordinal);
            int obtidos = 0;
            foreach (var pagina in consulta.Paginas.OrderBy(p => p.Inicio))
            {
                string path = Caminho("arxiv", pagina.Arquivo);
                if (pagina.Inicio != obtidos || Hash(path) != pagina.Sha256)
                    throw new InvalidDataException($"Página alterada ou sequência inválida: {path}");
                var feed = XDocument.Load(path).Root ?? throw new InvalidDataException($"Feed vazio: {path}");
                var entradas = feed.Elements(Atom + "entry").ToList();
                if (Total(feed) != consulta.Total || entradas.Count != pagina.Retornados)
                    throw new InvalidDataException($"Contagens divergentes em {path}.");
                foreach (var entrada in entradas)
                {
                    string id = Identificador(entrada);
                    string versao = Regex.Match(entrada.Element(Atom + "id")!.Value, @"v\d+$").Value;
                    if (versao.Length == 0)
                        throw new InvalidDataException($"Versão arXiv ausente para {id}.");
                    if (!vistosNaConsulta.Add(id))
                        throw new InvalidDataException($"Registro duplicado entre páginas da consulta {consulta.Id}: {id}");
                    string publicado = entrada.Element(Atom + "published")?.Value
                        ?? throw new InvalidDataException($"Data ausente para {id}.");
                    var data = DateOnly.FromDateTime(DateTimeOffset.Parse(publicado, CultureInfo.InvariantCulture).UtcDateTime);
                    if (data < inicio || data > fim) { fora.Add(id); continue; }
                    string titulo = Limpar(entrada.Element(Atom + "title")?.Value);
                    if (titulo.Length == 0) throw new InvalidDataException($"Título ausente para {id}.");
                    if (!trabalhos.TryGetValue(id, out var trabalho))
                    {
                        trabalho = new Artigo
                        {
                            Key = "arxiv:" + id,
                            Id = id,
                            Versao = versao,
                            Title = titulo,
                            Abstract = Limpar(entrada.Element(Atom + "summary")?.Value),
                            Date = data.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture),
                            Url = "https://arxiv.org/abs/" + id + versao,
                            Authors = entrada.Elements(Atom + "author")
                                .Select(a => Limpar(a.Element(Atom + "name")?.Value))
                                .Where(a => a.Length > 0).ToList()
                        };
                        trabalhos.Add(id, trabalho);
                    }
                    else if (!string.Equals(trabalho.Title, titulo, StringComparison.Ordinal))
                        throw new InvalidDataException($"Títulos divergentes para {id} entre as consultas.");
                    else if (!string.Equals(trabalho.Versao, versao, StringComparison.Ordinal))
                        throw new InvalidDataException($"Versões divergentes para {id} entre as consultas.");
                    trabalho.Consultas.Add(consulta.Id);
                }
                obtidos += entradas.Count;
            }
            if (obtidos != consulta.Total)
                throw new InvalidDataException($"Coleta incompleta de {consulta.Id}: {obtidos}/{consulta.Total}.");
        }
        foraJanela = fora.Count;
        return trabalhos.Values.OrderBy(t => t.Id, StringComparer.Ordinal).ToList();
    }

    public void Preparar()
    {
        var artigos = CarregarSnapshots(out _, out int fora);
        Directory.CreateDirectory(Caminho("lotes"));
        File.WriteAllLines(Caminho("candidatos.jsonl"), artigos.Select(Linha), Utf8);
        File.WriteAllLines(Caminho("lotes", "focado.jsonl"), artigos.Select(a => Linha(new
        {
            key = a.Key, title = a.Title, @abstract = a.Abstract
        })), Utf8);
        Console.WriteLine($"Candidatos únicos na janela: {artigos.Count}; fora da janela pela data do primeiro depósito: {fora}.");
    }

    public void Relatorio()
    {
        var artigos = CarregarSnapshots(out var manifesto, out int fora);
        var porKey = artigos.ToDictionary(a => a.Key, StringComparer.Ordinal);
        string decDir = Caminho("decisoes");
        if (!Directory.Exists(decDir)) throw new DirectoryNotFoundException($"Decisões não encontradas: {decDir}");
        var decisoes = new Dictionary<string, Decisao>(StringComparer.Ordinal);
        foreach (string file in Directory.GetFiles(decDir, "*.jsonl").OrderBy(x => x, StringComparer.Ordinal))
            foreach (var decisao in LerJsonl<Decisao>(file))
                if (!porKey.ContainsKey(decisao.Key) || !decisoes.TryAdd(decisao.Key, decisao) ||
                    decisao.Decision is not ("CORE" or "CONTEXT" or "EXCLUDE"))
                    throw new InvalidDataException($"Decisão desconhecida, inválida ou duplicada para {decisao.Key}.");
        var faltantes = artigos.Where(a => !decisoes.ContainsKey(a.Key)).Select(a => a.Key).ToList();
        if (faltantes.Count > 0)
            throw new InvalidDataException($"Faltam decisões para {faltantes.Count} candidatos; não é possível gerar o relatório final.");

        var revisoes = Ler<List<Revisao>>(Caminho("revisao_final.json"));
        var revisadas = new Dictionary<string, Revisao>(StringComparer.Ordinal);
        foreach (var revisao in revisoes)
        {
            if (!porKey.ContainsKey(revisao.Key) || !revisadas.TryAdd(revisao.Key, revisao) ||
                string.IsNullOrWhiteSpace(revisao.Motivo))
                throw new InvalidDataException($"Revisão final inválida ou duplicada: {revisao.Key}");
            if (revisao.Verificacao is not ("R" or "T"))
                throw new InvalidDataException($"Nível de verificação inválido para {revisao.Key}.");
            if (revisao.Verificacao == "T" &&
                (!Uri.TryCreate(revisao.Fonte, UriKind.Absolute, out var fonte) ||
                 fonte.Scheme != Uri.UriSchemeHttps || fonte.Host != "arxiv.org" ||
                 fonte.AbsolutePath != $"/html/{porKey[revisao.Key].Id}{porKey[revisao.Key].Versao}" &&
                 fonte.AbsolutePath != $"/pdf/{porKey[revisao.Key].Id}{porKey[revisao.Key].Versao}"))
                throw new InvalidDataException($"Fonte integral ausente ou incompatível com o snapshot para {revisao.Key}.");
            if (revisao.Incluir && revisao.Tipo is not ("NUCLEO" or "COMPARADOR"))
                throw new InvalidDataException($"Tipo final inválido para {revisao.Key}.");
            if (revisao.Incluir && new[] { revisao.Representacao, revisao.Atualizacao, revisao.Modelos,
                    revisao.Avaliacao, revisao.Paradigmas }.Any(string.IsNullOrWhiteSpace))
                throw new InvalidDataException($"Faltam campos do quadro para {revisao.Key}.");
        }
        var coreNaoRevisados = decisoes.Values.Where(d => d.Decision == "CORE" && !revisadas.ContainsKey(d.Key)).ToList();
        if (coreNaoRevisados.Count > 0)
            throw new InvalidDataException($"Falta revisão final de {coreNaoRevisados.Count} registros CORE.");
        var selecionados = revisoes.Where(r => r.Incluir)
            .OrderBy(r => porKey[r.Key].Date, StringComparer.Ordinal)
            .ThenBy(r => porKey[r.Key].Title, StringComparer.Ordinal).ToList();
        if (selecionados.Count == 0) throw new InvalidDataException("Nenhum estudo foi selecionado para o quadro.");
        if (selecionados.Any(r => porKey[r.Key].Authors.Count == 0))
            throw new InvalidDataException("Um estudo selecionado não tem autores no snapshot.");

        Directory.CreateDirectory(saida);
        Inventario(artigos, decisoes, revisadas);
        Ris(selecionados, porKey);
        string texto = MontarRelatorio(artigos, decisoes, revisadas, selecionados, manifesto, fora);
        string path = Path.Combine(saida, "mapeamento_focado_trabalhos_relacionados_2025_2026.md");
        File.WriteAllText(path, texto, Utf8);
        Console.WriteLine($"Relatório: {artigos.Count} candidatos, {decisoes.Values.Count(d => d.Decision == "CORE")} CORE, {selecionados.Count} selecionados.");
        Console.WriteLine($"Saída: {path}");
    }

    void Inventario(List<Artigo> artigos, Dictionary<string, Decisao> decisoes, Dictionary<string, Revisao> revisoes)
    {
        static string Csv(string? valor) => "\"" + (valor ?? "").Replace("\"", "\"\"") + "\"";
        var linhas = new List<string> { "id,titulo,data,url,consultas,decisao,codigos,relevancia,justificativa,revisao_final,tipo_final,verificacao,fonte_verificacao,motivo_final" };
        foreach (var a in artigos)
        {
            var d = decisoes[a.Key];
            revisoes.TryGetValue(a.Key, out var r);
            linhas.Add(string.Join(",", new[] { a.Id, a.Title, a.Date, a.Url, string.Join(";", a.Consultas),
                d.Decision, string.Join(";", d.Codes), d.Relevance.ToString(CultureInfo.InvariantCulture), d.Note,
                r is null ? "não revisado" : r.Incluir ? "incluído" : "excluído",
                r?.Tipo ?? "", r?.Verificacao ?? "", r?.Fonte ?? "", r?.Motivo ?? "" }.Select(Csv)));
        }
        File.WriteAllLines(Path.Combine(saida, "mapeamento_focado_inventario_2025_2026.csv"), linhas, new UTF8Encoding(true));
    }

    void Ris(List<Revisao> selecionados, Dictionary<string, Artigo> porKey)
    {
        static string AutorRis(string autor)
        {
            if (autor.Contains(',')) return autor;
            int separador = autor.LastIndexOf(' ');
            return separador < 0 ? autor : $"{autor[(separador + 1)..]}, {autor[..separador]}";
        }
        var linhas = new List<string>();
        foreach (var r in selecionados)
        {
            var a = porKey[r.Key];
            linhas.Add("TY  - GEN");
            linhas.Add("TI  - " + a.Title);
            foreach (var autor in a.Authors) linhas.Add("AU  - " + AutorRis(autor));
            linhas.Add("PY  - " + a.Date[..4]);
            linhas.Add("DA  - " + a.Date.Replace("-", "/"));
            linhas.Add("UR  - " + a.Url);
            linhas.Add("AB  - " + a.Abstract);
            linhas.Add("N1  - " + r.Motivo);
            linhas.Add("ER  - ");
            linhas.Add("");
        }
        File.WriteAllText(Path.Combine(saida, "mapeamento_focado_selecionados_2025_2026.ris"),
            string.Join("\r\n", linhas), Utf8);
    }

    string MontarRelatorio(List<Artigo> artigos, Dictionary<string, Decisao> decisoes,
        Dictionary<string, Revisao> revisoes, List<Revisao> selecionados, Manifesto manifesto, int fora)
    {
        var b = new StringBuilder();
        void L(string texto = "") => b.AppendLine(texto);
        static string Celula(string texto) => Limpar(texto).Replace("|", "\\|");
        var porKey = artigos.ToDictionary(a => a.Key, StringComparer.Ordinal);
        var ids = artigos.Select(a => a.Id).ToHashSet(StringComparer.Ordinal);
        int controles = protocolo.Controles.Count(c => ids.Contains(c.IdArxiv));
        int core = decisoes.Values.Count(d => d.Decision == "CORE");
        int contexto = decisoes.Values.Count(d => d.Decision == "CONTEXT");
        int excluidos = decisoes.Values.Count(d => d.Decision == "EXCLUDE");
        int selecionadosCore = selecionados.Count(r => decisoes[r.Key].Decision == "CORE");
        int selecionadosContexto = selecionados.Count(r => decisoes[r.Key].Decision == "CONTEXT");
        int selecionadosExcluidos = selecionados.Count(r => decisoes[r.Key].Decision == "EXCLUDE");
        int revisadosNaoCore = revisoes.Count(r => decisoes[r.Key].Decision != "CORE");
        int nucleoFinal = selecionados.Count(r => r.Tipo == "NUCLEO");
        int comparadores = selecionados.Count(r => r.Tipo == "COMPARADOR");

        L("# Mapeamento focado de trabalhos relacionados");
        L();
        L($"**Janela:** {inicio:dd/MM/yyyy} a {fim:dd/MM/yyyy}; data do primeiro depósito no arXiv.  ");
        L($"**Coleta:** {manifesto.DataUtc}; fonte: arXiv API. Este documento não altera o artigo do TCC.");
        L();
        L("## Metodologia");
        L();
        L("O procedimento é um mapeamento sistematizado e limitado, inspirado no planejamento, busca, triagem e extração de [Petersen et al. (2015)](https://doi.org/10.1016/j.infsof.2015.03.007). A calibração exploratória com trabalhos conhecidos foi inspirada no uso de estudos de referência por [Zhang et al. (2011)](https://doi.org/10.1016/j.infsof.2010.12.010), sem representar uma validação independente nem uma estimativa geral de cobertura.");
        string referenciaRedacao = Path.GetFullPath(Path.Combine(raiz, "..", "..", "..", "artigos",
            "05-metodologia-e-escrita-cientifica", "Prodanov_Freitas_2013_Metodologia_do_Trabalho_Cientifico",
            "Prodanov_Freitas_2013_Metodologia_do_Trabalho_Cientifico.md"));
        string linkRedacao = Path.GetRelativePath(saida, referenciaRedacao).Replace('\\', '/');
        L($"A exposição de objetivo, procedimentos e limitações também segue a orientação geral de organização do trabalho científico de [Prodanov e Freitas (2013)](<{linkRedacao}>), presente no material metodológico indicado.");
        L("A questão é identificar quais estudos aproximam escrita incremental de memória estruturada, modelos compactos, avaliação do estado e paradigmas gerativos. As consultas combinam essas facetas nos campos título e resumo. O recorte cobre preprints no arXiv, não toda a literatura; trabalhos fora dessa fonte ou com primeiro depósito anterior à janela podem ficar ausentes.");
        L("OpenAlex e Semantic Scholar responderam HTTP 429 às tentativas da busca focada e não integram esta coleta. Seus resultados antigos não foram apresentados como novas buscas.");
        L();
        L("| Consulta | Faceta | Total informado | Registros coletados |");
        L("|---|---|---:|---:|");
        foreach (var c in protocolo.Consultas)
        {
            var m = manifesto.Consultas.Single(x => x.Id == c.Id);
            L($"| {c.Id} | {Celula(c.Objetivo)} | {N(m.Total)} | {N(m.Paginas.Sum(p => p.Retornados))} |");
        }
        L();
        string linkProtocolo = Path.GetRelativePath(saida, protocoloPath).Replace('\\', '/');
        L($"As expressões completas e a janela `submittedDate` estão no [protocolo focado]({linkProtocolo}). Todos os resultados de cada consulta foram paginados; os totais por consulta se sobrepõem.");
        L();
        L($"Após deduplicação por identificador arXiv: **{N(artigos.Count)} candidatos** na janela; {N(fora)} registros fora dela pela data do primeiro depósito. A triagem por IA do título e resumo classificou **{N(core)} CORE**, {N(contexto)} CONTEXT e {N(excluidos)} EXCLUDE.");
        L("CORE exige estudo primário, atualização incremental de memória textual estruturada e, além disso, ao menos uma dimensão: escritor ou gestor compacto de até aproximadamente 4B parâmetros; avaliação direta da fidelidade ou correção do estado; ou comparação pertinente de paradigmas gerativos. CONTEXT indica proximidade parcial ou evidência insuficiente; EXCLUDE abrange estudos secundários, memória de hardware, modalidade não textual principal e outros temas sem contribuição pertinente.");
        L($"A revisão final registrou decisões para todos os {N(core)} CORE e para {N(revisadosNaoCore)} outros candidatos selecionados por proximidade: manteve {N(selecionadosCore)} CORE e excluiu {N(core - selecionadosCore)}. A classificação e a revisão foram assistidas por IA, sem avaliação humana independente.");
        L("Como exceção explícita, a revisão pode incluir comparadores CONTEXT que avaliem paradigmas gerativos em memória de agentes ou estado de planejamento revisável, mesmo sem cumprir o núcleo; também pode corrigir uma decisão inicial mediante justificativa individual. Não se trata de alegar que todos os CONTEXT foram reavaliados integralmente.");
        L();
        L($"Para diagnosticar perdas, as consultas recuperaram **{controles}/{protocolo.Controles.Count}** controles previamente conhecidos; esses controles não foram acrescentados artificialmente aos resultados. São uma amostra dirigida, não uma medida de cobertura geral.");
        foreach (var c in protocolo.Controles)
            L($"- {c.Nome} ([arXiv:{c.IdArxiv}](https://arxiv.org/abs/{c.IdArxiv})): {(ids.Contains(c.IdArxiv) ? "recuperado" : "não recuperado") }.");
        L();
        L($"O quadro inclui **{N(selecionados.Count)} estudos da busca focada**: {N(nucleoFinal)} no núcleo após a revisão e {N(comparadores)} comparadores. Na triagem inicial, eram {N(selecionadosCore)} CORE, {N(selecionadosContexto)} CONTEXT e {N(selecionadosExcluidos)} EXCLUDE. Acrescenta dois fundamentos anteriores ao recorte e a linha da proposta. Não há corte arbitrário por ranking.");
        L();
        L("## Quadro comparativo");
        L();
        L("| Trabalho | Representação da memória | Atualização | Modelos e escala | Objeto da avaliação | Compara paradigmas gerativos |");
        L("|---|---|---|---|---|---|");
        L("| [Hwang et al. (2024), fundamento](https://doi.org/10.18653/v1/2024.findings-emnlp.220) | Texto e JSON | GU-JSON e alternativas; reescrita do estado | Gemini Ultra e Pro | Fidelidade de resumos incrementais | Não identificado como comparação de paradigmas |");
        L("| [SUMIE (2025), fundamento](https://aclanthology.org/2025.coling-main.721/) | Entidades, atributos e valores | Integra informações e preserva perspectivas | Modelos de linguagem de grande porte | Precisão, revocação e F1 do resumo | Não identificado como comparação de paradigmas |");
        foreach (var r in selecionados)
        {
            var a = porKey[r.Key];
            string titulo = Celula(a.Title).Replace("[", "\\[").Replace("]", "\\]");
            string verificacao = r.Verificacao == "T" ? $"[T]({r.Fonte})" : "R";
            string tipo = r.Tipo == "NUCLEO" ? "núcleo" : "comparador";
            L($"| [{titulo}]({a.Url}) ({a.Date[..4]}; {tipo}; IA: {decisoes[r.Key].Decision}; {verificacao}) | {Celula(r.Representacao)} | {Celula(r.Atualizacao)} | {Celula(r.Modelos)} | {Celula(r.Avaliacao)} | {Celula(r.Paradigmas)} |");
        }
        L("| **Proposta do TCC** | Checkpoint JSON de esquema fixo | Reescrita integral GU-JSON | Representantes compactos autoregressivo, encoder-decoder e difusão em blocos | Validade e fidelidade por transição, turno e operação no SUMIE | Sim, sob o mesmo protocolo |");
        L();
        L("A categoria final distingue núcleo e comparador; CORE/CONTEXT/EXCLUDE são os rótulos da triagem inicial por IA, não uma avaliação independente. R indica título e resumo; T aponta para a versão do texto integral da qual também foram conferidos trechos, não necessariamente o artigo completo. Confirme método, modelos e resultados no texto integral antes de citar.");
        L();
        L("## Síntese");
        L();
        var idsSelecionados = selecionados.Select(r => porKey[r.Key].Id).ToHashSet(StringComparer.Ordinal);
        if (idsSelecionados.Contains("2604.07877") && idsSelecionados.Contains("2605.15759") && idsSelecionados.Contains("2609.36976"))
            L("- MemReader, DimMem e AMU já aproximam modelos compactos e escrita ou gestão de memória estruturada. Portanto, essa combinação isoladamente não constitui uma lacuna nova.");
        if (idsSelecionados.Contains("2603.26680"))
            L("- AlpsBench avalia diretamente a memória atualizada, além das respostas. Assim, não é seguro afirmar que todos os benchmarks de memória avaliam apenas respostas finais.");
        if (idsSelecionados.Contains("2608.01708"))
            L("- PGMem mede diretamente a qualidade de uma parte do estado: os rótulos de suas arestas. Isso não equivale à fidelidade de um checkpoint JSON completo.");
        if (idsSelecionados.Contains("2601.12979") && idsSelecionados.Contains("2610.24717"))
            L("- DiffuAgent compara difusão e autoregressão em tarefas agênticas; sua sumarização de memória e suas chamadas JSON são avaliações distintas. DiffuPlan estuda a revisão de um plano textual, não um checkpoint GU-JSON do SUMIE.");
        L("- No escopo examinado, a proposta diferencia-se pela combinação de GU-JSON, esquema e transições do SUMIE, três escritores compactos e avaliação de validade e fidelidade por atualização. A busca limitada não comprova ausência universal de trabalhos similares, e comparar modelos pré-treinados diferentes não isola causalmente o efeito da arquitetura.");
        L();
        L("## Referências dos estudos selecionados");
        L();
        foreach (var r in selecionados)
        {
            var a = porKey[r.Key];
            L($"- {string.Join("; ", a.Authors)}. **{a.Title}**. arXiv, {a.Date[..4]}. [Registro {a.Id}{a.Versao}]({a.Url}). Primeiro depósito: {a.Date}.");
        }
        L();
        L("## Reprodutibilidade e limitações");
        L();
        L("- [Inventário e decisões](./mapeamento_focado_inventario_2025_2026.csv); [RIS dos selecionados](./mapeamento_focado_selecionados_2025_2026.ris). O comando gera o RIS, mas não cria nem importa uma coleção no Zotero.");
        string roteiro = Path.GetRelativePath(saida, Path.Combine(raiz, "protocolo", "roteiro_triagem_focado.md")).Replace('\\', '/');
        string revisaoPath = Path.GetRelativePath(saida, Caminho("revisao_final.json")).Replace('\\', '/');
        L($"- [Roteiro da triagem]({roteiro}), [revisão final]({revisaoPath}), snapshots por consulta, manifesto com hashes e decisões estão em `{Path.GetRelativePath(saida, dados).Replace('\\', '/')}/`.");
        string custoPath = Caminho("custo_llm.jsonl");
        if (File.Exists(custoPath))
        {
            double custo = File.ReadLines(custoPath, Utf8).Where(l => !string.IsNullOrWhiteSpace(l)).Sum(l =>
            {
                using var registro = JsonDocument.Parse(l);
                return registro.RootElement.GetProperty("custo_contabilizado").GetDouble();
            });
            L($"- A triagem desta execução registrou {custo.ToString("N2", PtBr)} créditos contabilizados em `custo_llm.jsonl`; despesas de pilotos anteriores são separadas.");
        }
        else
            L("- Não há registro de custo da triagem nesta pasta; não é possível determinar o consumo desta execução.");
        L("- Para reproduzir sem rede e sem novas chamadas a modelos, execute `dotnet run scripts/busca_focada.cs -- offline` a partir da pasta `mapeamento_sistematico`.");
        L("- As consultas são deliberadamente estreitas: sua precisão tende a melhorar, mas sua sensibilidade pode cair. Os controles não recuperados, os estudos sem palavras explícitas no título/resumo e os trabalhos fora do arXiv exigem verificação adicional.");
        L("- Os nomes de autores no RIS são convertidos do nome completo fornecido pelo arXiv pela última palavra; nomes compostos ou institucionais devem ser conferidos após a importação.");
        return b.ToString();
    }
}

sealed class Protocolo
{
    public string Inicio { get; set; } = "";
    public string Fim { get; set; } = "";
    public int Pagina { get; set; }
    public double IntervaloSegundos { get; set; }
    public List<Consulta> Consultas { get; set; } = [];
    public List<Controle> Controles { get; set; } = [];
}
sealed class Consulta
{
    public string Id { get; set; } = "";
    public string Objetivo { get; set; } = "";
    public string Expressao { get; set; } = "";
}
sealed class Controle
{
    public string Nome { get; set; } = "";
    public string IdArxiv { get; set; } = "";
}
sealed class Manifesto
{
    public string DataUtc { get; set; } = "";
    public string ProtocoloSha256 { get; set; } = "";
    public List<ConsultaManifesto> Consultas { get; set; } = [];
}
sealed class ConsultaManifesto
{
    public string Id { get; set; } = "";
    public string Expressao { get; set; } = "";
    public int Total { get; set; }
    public List<Pagina> Paginas { get; set; } = [];
}
sealed class Pagina
{
    public string Arquivo { get; set; } = "";
    public int Inicio { get; set; }
    public int Retornados { get; set; }
    public string Sha256 { get; set; } = "";
}
sealed class Artigo
{
    public string Key { get; set; } = "";
    public string Id { get; set; } = "";
    public string Versao { get; set; } = "";
    public string Title { get; set; } = "";
    public string Abstract { get; set; } = "";
    public string Date { get; set; } = "";
    public string Url { get; set; } = "";
    public List<string> Authors { get; set; } = [];
    public List<string> Consultas { get; set; } = [];
}
sealed class Decisao
{
    public string Key { get; set; } = "";
    public string Decision { get; set; } = "";
    public List<string> Codes { get; set; } = [];
    public int Relevance { get; set; }
    public string Note { get; set; } = "";
}
sealed class Revisao
{
    public string Key { get; set; } = "";
    public required bool Incluir { get; set; }
    public string Tipo { get; set; } = "";
    public string Motivo { get; set; } = "";
    public string Representacao { get; set; } = "";
    public string Atualizacao { get; set; } = "";
    public string Modelos { get; set; } = "";
    public string Avaliacao { get; set; } = "";
    public string Paradigmas { get; set; } = "";
    public string Verificacao { get; set; } = "";
    public string Fonte { get; set; } = "";
}
