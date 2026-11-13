#!/usr/bin/env dotnet
// Pipeline reprodutível do mapeamento sistemático (v2).
// Uso: dotnet run scripts/mapeamento.cs -- <comando> [--dados <pasta>] [--protocolo <json>] [--saida <pasta>]
// Comandos: calibrar | sensibilidade | coletar-openalex | coletar-s2 | pretriar | lotes | consolidar | relatorio | offline
#:property Nullable=enable
#:property PublishAot=false
#:property InvariantGlobalization=false

using System.Globalization;
using System.IO.Compression;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;

Console.OutputEncoding = Encoding.UTF8;
var opt = Opcoes.Ler(args);
var ctx = new Contexto(opt);
switch (opt.Comando)
{
    case "calibrar": await Coleta.Calibrar(ctx); break;
    case "sensibilidade": await Coleta.Sensibilidade(ctx); break;
    case "coletar-openalex": await Coleta.OpenAlex(ctx); break;
    case "coletar-s2": await Coleta.SemanticScholar(ctx); break;
    case "pretriar": Pretriagem.Executar(ctx); break;
    case "lotes": Lotes.Executar(ctx); break;
    case "consolidar": Consolidacao.Executar(ctx, opt.Tem("permitir-pendentes")); break;
    case "relatorio": Relatorio.Executar(ctx); break;
    case "offline":
        Pretriagem.Executar(ctx);
        Consolidacao.Executar(ctx, false);
        Relatorio.Executar(ctx);
        break;
    default:
        Console.Error.WriteLine("Comandos: calibrar | sensibilidade | coletar-openalex | coletar-s2 | pretriar | lotes | consolidar | relatorio | offline");
        return 2;
}
return 0;

// ---------------------------------------------------------------- infraestrutura

sealed class Opcoes
{
    public string Comando = "";
    readonly Dictionary<string, string?> _v = new();
    public static Opcoes Ler(string[] a)
    {
        var o = new Opcoes { Comando = a.Length > 0 ? a[0] : "" };
        for (int i = 1; i < a.Length; i++)
            if (a[i].StartsWith("--"))
                o._v[a[i][2..]] = i + 1 < a.Length && !a[i + 1].StartsWith("--") ? a[++i] : null;
        return o;
    }
    public string? this[string k] => _v.TryGetValue(k, out var v) ? v : null;
    public bool Tem(string k) => _v.ContainsKey(k);
}

sealed class Contexto
{
    public readonly string Raiz, Dados, Saida, ProtocoloPath, Modelo;
    public readonly JsonObject P;
    public readonly string Inicio, Fim;
    public Contexto(Opcoes o)
    {
        var dir = AppContext.GetData("EntryPointFileDirectoryPath") as string;
        Raiz = Path.GetFullPath(dir is null ? Directory.GetCurrentDirectory() : Path.Combine(dir, ".."));
        ProtocoloPath = Path.GetFullPath(o["protocolo"] ?? Path.Combine(Raiz, "protocolo", "protocolo.json"));
        Dados = Path.GetFullPath(o["dados"] ?? Path.Combine(Raiz, "dados", "execucao_2026-11-12"));
        Saida = Path.GetFullPath(o["saida"] ?? Path.Combine(Raiz, ".."));
        Modelo = Path.GetFullPath(o["modelo"] ?? Path.Combine(Raiz, "modelos", "relatorio.md"));
        P = JsonNode.Parse(File.ReadAllText(ProtocoloPath))!.AsObject();
        Inicio = (string)P["janela"]!["inicio"]!;
        Fim = (string)P["janela"]!["fim"]!;
        Directory.CreateDirectory(Dados);
    }
    public string D(params string[] p) => Path.Combine([Dados, .. p]);
    public IEnumerable<(string k, string v)> Strings(string fonte) =>
        P[fonte]!.AsObject().Select(kv => (kv.Key, (string)kv.Value!));
}

static class Io
{
    public static readonly JsonSerializerOptions J = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
    };

    static Stream Abrir(string path)
    {
        if (!File.Exists(path) && File.Exists(path + ".gz")) path += ".gz";
        if (!File.Exists(path)) throw new FileNotFoundException("Arquivo não encontrado (execute a etapa anterior)", path);
        Stream s = File.OpenRead(path);
        return path.EndsWith(".gz") ? new GZipStream(s, CompressionMode.Decompress) : s;
    }
    public static bool Existe(string path) => File.Exists(path) || File.Exists(path + ".gz");
    public static JsonNode LerNode(string path) { using var s = Abrir(path); return JsonNode.Parse(s)!; }
    public static T Ler<T>(string path) { using var s = Abrir(path); return JsonSerializer.Deserialize<T>(s, J)!; }

    public static void Gravar(string path, object valor)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        var bytes = valor is JsonNode n
            ? Encoding.UTF8.GetBytes(n.ToJsonString(J))
            : JsonSerializer.SerializeToUtf8Bytes(valor, valor.GetType(), J);
        var tmp = path + ".tmp";
        using (var f = File.Create(tmp))
        {
            if (path.EndsWith(".gz")) { using var g = new GZipStream(f, CompressionLevel.SmallestSize); g.Write(bytes); }
            else f.Write(bytes);
        }
        File.Move(tmp, path, true);
    }

    public static IEnumerable<JsonObject> Jsonl(string path) =>
        File.ReadLines(path).Where(l => l.Trim().Length > 0).Select(l => JsonNode.Parse(l)!.AsObject());

    public static string Norm(string? s)
    {
        var sb = new StringBuilder();
        foreach (var c in (s ?? "").ToLowerInvariant())
            if (c is >= 'a' and <= 'z' or >= '0' and <= '9') sb.Append(c);
        return sb.ToString();
    }

    public static string Hash(string s) => Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(s)));
}

static class Http
{
    static readonly HttpClient C = new() { Timeout = TimeSpan.FromSeconds(120) };
    public static string UserAgent = "tcc-mapping/1.0";

    public static async Task<(JsonNode? json, HttpResponseMessage? resp)> Get(string url, int tentativas = 6, string? s2Key = null)
    {
        Exception? erro = null;
        for (int i = 0; i < tentativas; i++)
        {
            try
            {
                using var req = new HttpRequestMessage(HttpMethod.Get, url);
                req.Headers.UserAgent.ParseAdd(UserAgent);
                if (s2Key is not null) req.Headers.Add("x-api-key", s2Key);
                var r = await C.SendAsync(req);
                if (r.StatusCode == System.Net.HttpStatusCode.NotFound) return (null, r);
                if ((int)r.StatusCode == 429) { await Task.Delay(TimeSpan.FromSeconds(Math.Min(60, 3 * Math.Pow(2, i)))); continue; }
                if (!r.IsSuccessStatusCode) { erro = new HttpRequestException($"{(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}"); await Task.Delay(3000); continue; }
                return (JsonNode.Parse(await r.Content.ReadAsStringAsync()), r);
            }
            catch (Exception e) when (e is HttpRequestException or TaskCanceledException) { erro = e; await Task.Delay(5000); }
        }
        throw new InvalidOperationException("Falha ao obter " + url, erro);
    }

    // Equivalente a urllib.parse.quote(s, safe=":,")
    public static string Quote(string s, string seguros = "") =>
        seguros.Aggregate(Uri.EscapeDataString(s), (acc, c) => acc.Replace(Uri.EscapeDataString(c.ToString()), c.ToString()));
}

// ---------------------------------------------------------------- critérios de pré-triagem (regras léxicas)

static class Criterios
{
    static Regex R(string p) => new(p, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant | RegexOptions.Compiled);

    static readonly Regex LM = R(@"\b(llms?|slms?|(?:large|small|compact|diffusion)?\s?language models?|agentic|agents?|chatbots?|assistants?|dllms?)\b");
    static readonly Regex MEM = R(@"\b(memory|memories|memory bank|knowledge base|state|states|checkpoints?|blackboard|profile|records?|notes?)\b");
    static readonly Regex OPW = R(@"\b(updat\w*|writ(?:e|es|ing|ten)|consolidat\w*|forget\w*|admission|admit\w*|overwrit\w*|supersed\w*|revis\w*|edit(?:s|ing)?|insert\w*|delet\w*|merg\w*|stale|outdated|obsolete|conflict\w*|maintain\w*|maintenance|evolv\w*|evolution)\b");
    static readonly Regex STRUCT_STATE = R(@"\b(json|schema|structured (?:memory|state|representation|records?)|key-value|tables?|entity|entities|slots?|attributes?|knowledge graph|graph memory|typed)\b");
    static readonly Regex INCR = R(@"\b(incremental\w*|multi-turn|multi-session|long-term|longitudinal|across sessions|over time|sequential\w*|streaming|continual\w*|persistent)\b");
    static readonly Regex SLM = R(@"\b(small language models?|slms?|sub-billion|compact (?:language )?models?|lightweight (?:language )?models?|small models?|(?:0\.\d|[1-4](?:\.\d)?)\s?b\b|qwen[\d.]*-(?:0\.5|0\.6|1\.5|1\.7|3|4)b|llama-3\.2-[13]b|phi-\d|smollm|gemma[\w-]*-(?:2|1|4)b)\b");
    static readonly Regex SGEN = R(@"\b(json|json schema|structured outputs?|structured generation|structured data generation|constrained decoding|grammar-constrained|function calling|tool calling)\b");
    static readonly Regex DIFF = R(@"\b(diffusion language models?|dllms?|masked diffusion|block diffusion|discrete diffusion|diffusion llms?|bd3-?lm|llada|dream-7b|autoregressive (?:and|vs\.?|versus) diffusion)\b");
    static readonly Regex BENCH = R(@"\b(benchmark\w*|evaluat\w*|testbed|dataset)\b");
    static readonly Regex AGENT = R(@"\bagent");

    static readonly Regex E_HW = R(@"\b(kv[- ]?cache|gpu memory|hbm|dram|sram|memory (?:footprint|bandwidth|wall|efficien\w*|consumption|usage|access|hierarch\w*|controller|cells?|overhead|budget|constrain\w*)|memory-(?:efficient|constrained|bound)|in-memory computing|processing-in-memory|quantiz\w*|offload\w*|nand|flash memory|memristor\w*|activation memory|optimizer states?)\b");
    static readonly Regex E_SEC_T = R(@"\b(survey|literature review|systematic review|scoping review|a review|position paper|tutorial|overview|roadmap|taxonomy|vision paper|systematic literature|a perspective on)\b");
    static readonly Regex E_MOD_T = R(@"\b(video|visual|vision|image|images|gui|robot\w*|embodied|driving|speech|audio|multimodal|vlm|mllm|3d|navigation|game)\b");
    static readonly Regex E_ADV = R(@"\b(poison\w*|attack\w*|jailbreak\w*|adversarial|backdoor\w*|privacy|unlearning|injection|sycophan\w*|security)\b");
    static readonly Regex E_DOMAIN = R(@"\b(clinical|patients?|medical|hospital|alzheimer\w*|dementia|students?|classroom|financ\w*|trading|legal|chemistry|materials?|protein|molecul\w*|biolog\w*|manufactur\w*|supply chain|power grid|traffic|satellite|iot)\b");
    static readonly Regex MEM_OK = R(@"\b(agent memory|memory (?:update|management|system|module|bank|agent|writ\w+)s?|long-term memory|conversational memory|persistent memory|structured memory|memory state)\b");

    static readonly Regex MEMS = R(@"\b(memory|memories|memory bank|entity states?|memory states?|checkpoints?|blackboard)\b");
    static readonly Regex UPD = R(@"\b(memory updat\w*|updat\w* (?:the |its |their )?memor\w*|memory (?:writ\w*|edit\w*|revision|maintenance|consolidation|admission|conflicts?|overwrit\w*)|writ\w* (?:to |into )?memory|stale|outdated|obsolete|supersed\w*|overwrit\w*|conflicting (?:facts|information|memories)|knowledge updates?|fact updates?|selective forgetting|forgetting)\b");
    static readonly Regex STRUCT_STRICT = R(@"\b(json|schemas?|structured (?:memory|memories|state|states|records?|representations?)|key-value|entity[- ]state|entity summar\w*|tables?|slots?|attribute-value|typed (?:memory|state|records?))\b");
    static readonly Regex SLM_STRICT = R(@"\b(small language models?|slms?|sub-billion|(?:0\.\d|[1-4](?:\.\d)?)\s?b(?:-parameter)?\b|qwen[\d.]*-(?:0\.5|0\.6|1\.5|1\.7|2|3|4)b|llama-3\.2-[13]b|smollm\w*|phi-[1-4]\b)");
    static readonly Regex FRASE = new(@"(?<=[.!?;])\s+", RegexOptions.Compiled);

    // Coocorrência de todos os padrões dentro de uma mesma frase.
    static bool Co(string t, params Regex[] rs) => FRASE.Split(t).Any(s => rs.All(r => r.IsMatch(s)));

    public static (bool candidato, List<string> tematicos, List<string> exclusoes) Triar(string? titulo, string? resumo)
    {
        titulo ??= "";
        var t = $"{titulo}. {resumo ?? ""}";
        var th = new List<string>();
        if (Co(t, MEM, OPW) && LM.IsMatch(t)) th.Add("T1");
        if (Co(t, STRUCT_STATE, MEM) && INCR.IsMatch(t) && LM.IsMatch(t)) th.Add("T2");
        if (Co(t, SLM, MEM) || (SLM.IsMatch(titulo) && MEM.IsMatch(t))) th.Add("T3");
        if ((SGEN.IsMatch(t) && (SLM.IsMatch(t) || DIFF.IsMatch(t))) || (DIFF.IsMatch(t) && AGENT.IsMatch(t))) th.Add("T4");
        if (Co(t, BENCH, MEM) && (OPW.IsMatch(t) || INCR.IsMatch(t)) && LM.IsMatch(t)) th.Add("T5");
        var ex = new List<string>();
        if (E_HW.IsMatch(t) && !MEM_OK.IsMatch(t)) ex.Add("E2");
        if (E_SEC_T.IsMatch(titulo)) ex.Add("E3");
        if (E_MOD_T.IsMatch(titulo)) ex.Add("E4");
        if (E_ADV.IsMatch(titulo)) ex.Add("E5");
        if (E_DOMAIN.IsMatch(titulo)) ex.Add("E6");
        if (!LM.IsMatch(t)) ex.Add("G1");
        return (th.Count > 0 && ex.Count == 0, th, ex);
    }

    // Facetas do núcleo (IC1–IC4) usadas para separar núcleo provável de contexto.
    public static List<string> Nucleo(string? titulo, string? resumo)
    {
        var t = $"{titulo ?? ""}. {resumo ?? ""}";
        var ic = new List<string>();
        if (Co(t, MEMS, UPD)) ic.Add("IC1");
        if (Co(t, SLM_STRICT, MEMS) || (SLM_STRICT.IsMatch(titulo ?? "") && MEMS.IsMatch(t))) ic.Add("IC2");
        if (Co(t, STRUCT_STRICT, MEMS) && (INCR.IsMatch(t) || UPD.IsMatch(t))) ic.Add("IC3");
        if ((SGEN.IsMatch(t) && (SLM_STRICT.IsMatch(t) || DIFF.IsMatch(t))) || (DIFF.IsMatch(t) && AGENT.IsMatch(t))) ic.Add("IC4");
        return ic;
    }
}

// ---------------------------------------------------------------- modelo de registro

sealed class Registro
{
    public string Title { get; set; } = "";
    public string Abstract { get; set; } = "";
    public string? Date { get; set; }
    public string? Doi { get; set; }
    public List<string> Authors { get; set; } = [];
    public List<string> Ids { get; set; } = [];
    public List<string> Src { get; set; } = [];
    public string Key { get; set; } = "";
    public string Decision { get; set; } = "";
    public List<string> Themes { get; set; } = [];
    public List<string> Excl { get; set; } = [];
    public List<string> Core { get; set; } = [];
    public string Tier { get; set; } = "";
    public string? Final { get; set; }
    public List<string> Codes { get; set; } = [];
    public int Rel { get; set; }
    public string Note { get; set; } = "";
    public bool ScreenedByReading { get; set; }
}

// ---------------------------------------------------------------- coleta

static class Coleta
{
    const string SEL = "id,doi,title,abstract_inverted_index,publication_date,type,referenced_works,cited_by_count";
    const string S2 = "https://api.semanticscholar.org/graph/v1";
    const string S2_FIELDS = "title,abstract,externalIds,publicationDate,year,venue,publicationTypes,citationCount,authors";

    static string OaKey => Environment.GetEnvironmentVariable("OPENALEX_API_KEY") is { Length: > 0 } k ? "&api_key=" + k : "";
    static string? S2Key => Environment.GetEnvironmentVariable("S2_API_KEY") is { Length: > 0 } k ? k : null;

    static string Janela(Contexto c) => $"from_publication_date:{c.Inicio},to_publication_date:{c.Fim}";
    static string OaUrl(Contexto c, string q, string extra = "") =>
        "https://api.openalex.org/works?filter=" + Http.Quote($"title_and_abstract.search:{q},{Janela(c)}{extra}", ":,") + OaKey;

    static string Resumo(JsonNode? inv)
    {
        if (inv is not JsonObject o) return "";
        var pos = new List<(int p, string w)>();
        foreach (var (w, ps) in o) foreach (var p in ps!.AsArray()) pos.Add(((int)p!, w));
        return string.Join(" ", pos.OrderBy(x => x.p).ThenBy(x => x.w, StringComparer.Ordinal).Select(x => x.w));
    }

    public static JsonObject Slim(JsonNode w) => new()
    {
        ["id"] = ((string)w["id"]!).Split('/')[^1],
        ["doi"] = w["doi"]?.DeepClone(),
        ["title"] = (string?)w["title"] ?? "",
        ["abstract"] = Resumo(w["abstract_inverted_index"]),
        ["date"] = w["publication_date"]?.DeepClone(),
        ["type"] = w["type"]?.DeepClone(),
        ["referenced_works"] = new JsonArray((w["referenced_works"]?.AsArray() ?? []).Select(r => (JsonNode)((string)r!).Split('/')[^1]).ToArray()),
        ["cited_by_count"] = w["cited_by_count"]?.DeepClone(),
    };

    public static async Task Calibrar(Contexto c)
    {
        var q = c.P["qgs"]!;
        var grupos = new (string nome, List<(string id, string rotulo)> itens)[]
        {
            ("positives", q["positivos"]!.AsArray().Select(x => ((string)x!["openalex"]!, (string)x["rotulo"]!)).ToList()),
            ("negatives", q["negativos"]!.AsArray().Select(x => ((string)x!, (string)x!)).ToList()),
            ("foundations", q["fundamentos"]!.AsArray().Select(x => ((string)x!["openalex"]!, (string)x["rotulo"]!)).ToList()),
        };
        var saida = new JsonObject();
        var naoResolvidos = new JsonArray();
        foreach (var (nome, itens) in grupos)
        {
            var obtidos = new Dictionary<string, JsonNode>();
            foreach (var bloco in itens.Chunk(50))
            {
                var url = "https://api.openalex.org/works?filter=openalex:" + string.Join("|", bloco.Select(b => b.id)) + $"&per-page=50&select={SEL}{OaKey}";
                var (j, _) = await Http.Get(url);
                foreach (var w in j!["results"]!.AsArray()) obtidos[((string)w!["id"]!).Split('/')[^1]] = w;
                await Task.Delay(150);
            }
            var arr = new JsonArray();
            foreach (var (id, rotulo) in itens)
            {
                if (!obtidos.TryGetValue(id, out var w)) { naoResolvidos.Add(new JsonObject { ["bucket"] = nome, ["id"] = id }); continue; }
                var d = Slim(w);
                d["label"] = rotulo;
                arr.Add(d);
            }
            saida[nome] = arr;
            Console.WriteLine($"{nome}: {arr.Count}/{itens.Count}");
        }
        saida["unresolved"] = naoResolvidos;
        Io.Gravar(c.D("calibracao.json.gz"), saida);
    }

    public static async Task Sensibilidade(Contexto c)
    {
        var cal = Io.LerNode(c.D("calibracao.json.gz"));
        var qgs = cal["positives"]!.AsArray().Select(d => (string)d!["id"]!).ToList();
        var rotulo = cal["positives"]!.AsArray().ToDictionary(d => (string)d!["id"]!, d => (string)d!["title"]!);
        var uniao = new HashSet<string>();
        var rel = new JsonObject();
        foreach (var (k, q) in c.Strings("strings_openalex"))
        {
            var (j, _) = await Http.Get(OaUrl(c, q) + "&per-page=1");
            var total = (int)j!["meta"]!["count"]!;
            var (h, _) = await Http.Get(OaUrl(c, q, ",openalex:" + string.Join("|", qgs)) + "&per-page=50&select=id");
            var hits = h!["results"]!.AsArray().Select(r => ((string)r!["id"]!).Split('/')[^1]).ToHashSet();
            uniao.UnionWith(hits);
            rel[k] = new JsonObject { ["total"] = total, ["qgs"] = hits.Count };
            Console.WriteLine($"{k} total={total} QGS={hits.Count}/{qgs.Count}");
        }
        rel["uniao_qgs"] = uniao.Count;
        rel["faltantes"] = new JsonArray(qgs.Where(i => !uniao.Contains(i)).Select(i => (JsonNode)rotulo[i]).ToArray());
        Console.WriteLine($"União: {uniao.Count}/{qgs.Count}");
        Io.Gravar(c.D("sensibilidade.json"), rel);
    }

    // Coleta integral (sem corte por ranking), retomável: o estado é salvo a cada página.
    public static async Task OpenAlex(Contexto c)
    {
        var path = c.D("openalex.json.gz");
        var st = Io.Existe(path) ? Io.LerNode(path).AsObject()
            : new JsonObject { ["records"] = new JsonObject(), ["sources"] = new JsonObject(), ["pages"] = new JsonObject(), ["meta"] = new JsonObject() };
        var rec = st["records"]!.AsObject(); var src = st["sources"]!.AsObject();
        var pages = st["pages"]!.AsObject(); var meta = st["meta"]!.AsObject();
        foreach (var (k, q) in c.Strings("strings_openalex"))
        {
            int p = ((int?)pages[k] ?? 0) + 1;
            if (meta[k] is not null && (p - 1) * 200 >= (int)meta[k]!) continue;
            while (true)
            {
                var (j, resp) = await Http.Get(OaUrl(c, q) + $"&per-page=200&page={p}&select={SEL}", 4);
                var n = (int)j!["meta"]!["count"]!;
                meta[k] = n;
                var res = j["results"]!.AsArray();
                foreach (var w in res)
                {
                    var d = Slim(w!);
                    var id = (string)d["id"]!;
                    if (!rec.ContainsKey(id)) rec[id] = d;
                    if (src[id] is not JsonArray a) src[id] = a = new JsonArray();
                    if (!a.Any(x => (string)x! == k)) a.Add(k);
                }
                pages[k] = p;
                Io.Gravar(path, st);
                Console.WriteLine($"{k} página {p}: {res.Count} (total {n})");
                if (res.Count < 200 || p * 200 >= n) break;
                p++;
                await Task.Delay(200);
            }
        }
        Console.WriteLine($"OpenAlex: {rec.Count} registros únicos");
    }

    static bool NaJanela(Contexto c, JsonNode p) =>
        (string?)p["publicationDate"] is { Length: > 0 } d && string.CompareOrdinal(c.Inicio, d) <= 0 && string.CompareOrdinal(d, c.Fim) <= 0;

    public static async Task SemanticScholar(Contexto c)
    {
        var rec = new JsonObject(); var src = new JsonObject();
        var rep = new JsonObject { ["queries"] = new JsonObject(), ["seeds"] = new JsonObject() };
        void Put(JsonNode p, string tag)
        {
            var id = (string)p["paperId"]!;
            if (!rec.ContainsKey(id)) rec[id] = p.DeepClone();
            if (src[id] is not JsonArray a) src[id] = a = new JsonArray();
            a.Add(tag);
        }
        foreach (var (k, q) in c.Strings("strings_semantic_scholar"))
        {
            string? token = null; int? total = null; var ps = new List<JsonNode>();
            do
            {
                var u = $"{S2}/paper/search/bulk?query={Uri.EscapeDataString(q)}&publicationDateOrYear={c.Inicio}:{c.Fim}&fields={S2_FIELDS}" + (token is null ? "" : "&token=" + token);
                var (r, _) = await Http.Get(u, 8, S2Key);
                total = (int?)r!["total"] ?? total;
                ps.AddRange(r["data"]!.AsArray().Select(x => x!));
                token = (string?)r["token"];
                await Task.Delay(1100);
            } while (token is not null);
            var kept = ps.Where(p => NaJanela(c, p)).ToList();
            foreach (var p in kept) Put(p, k);
            rep["queries"]![k] = new JsonObject { ["total"] = total, ["retrieved"] = ps.Count, ["in_window_exact_date"] = kept.Count };
            Console.WriteLine($"{k}: total={total} coletados={ps.Count} na janela={kept.Count}");
        }
        foreach (var s in c.P["sementes_snowballing"]!.AsArray())
        {
            string code = (string)s!["codigo"]!, title = (string)s["titulo"]!; var doi = (string?)s["doi"];
            bool Confere(JsonNode? x) => x is not null && Io.Norm((string?)x["title"]).PadRight(30)[..30] == Io.Norm(title).PadRight(30)[..30];
            var (m, _) = await Http.Get($"{S2}/paper/search/match?query={Uri.EscapeDataString(title)}&fields={S2_FIELDS},paperId", 8, S2Key);
            await Task.Delay(1100);
            JsonNode? seed = m?["data"]?.AsArray().FirstOrDefault();
            if (!Confere(seed) && doi is not null)
            {
                (seed, _) = await Http.Get($"{S2}/paper/DOI:{doi}?fields={S2_FIELDS},paperId", 8, S2Key);
                await Task.Delay(1100);
            }
            if (!Confere(seed))
            {
                rep["seeds"]![code] = new JsonObject { ["title"] = title, ["resolved"] = false };
                Console.WriteLine($"Semente não resolvida: {code}");
                continue;
            }
            var pid = (string)seed!["paperId"]!;
            var fw = (await Arestas(pid, "citations")).Where(p => NaJanela(c, p)).ToList();
            var bw = (await Arestas(pid, "references")).Where(p => NaJanela(c, p)).ToList();
            foreach (var p in fw) Put(p, "FW:" + code);
            foreach (var p in bw) Put(p, "BW:" + code);
            rep["seeds"]![code] = new JsonObject { ["title"] = (string)seed["title"]!, ["paperId"] = pid, ["forward_in_window"] = fw.Count, ["backward_in_window"] = bw.Count };
            Console.WriteLine($"{code}: forward={fw.Count} backward={bw.Count}");
        }
        rep["unique"] = rec.Count;
        Io.Gravar(c.D("semanticscholar.json.gz"), new JsonObject { ["report"] = rep, ["records"] = rec, ["sources"] = src });
        Console.WriteLine($"Semantic Scholar: {rec.Count} registros únicos");
    }

    static async Task<List<JsonNode>> Arestas(string pid, string tipo)
    {
        var chave = tipo == "citations" ? "citingPaper" : "citedPaper";
        var outl = new List<JsonNode>(); int off = 0;
        while (true)
        {
            var (r, _) = await Http.Get($"{S2}/paper/{pid}/{tipo}?fields={S2_FIELDS}&limit=1000&offset={off}", 8, S2Key);
            await Task.Delay(1100);
            if (r is null) return outl;
            foreach (var e in r["data"]?.AsArray() ?? [])
                if (e?[chave]?["paperId"] is not null) outl.Add(e[chave]!);
            if (r["next"] is null) return outl;
            off = (int)r["next"]!;
        }
    }
}

// ---------------------------------------------------------------- união, deduplicação e pré-triagem

static class Pretriagem
{
    public static void Executar(Contexto c)
    {
        var oa = Io.LerNode(c.D("openalex.json.gz"));
        var s2 = Io.LerNode(c.D("semanticscholar.json.gz"));
        var cal = Io.LerNode(c.D("calibracao.json.gz"));
        var recs = new Dictionary<string, (Registro r, HashSet<string> src)>();
        var ordem = new List<string>();

        void Add(string? title, string? abs, string? date, string? doi, string id, IEnumerable<string> tags, IEnumerable<string>? autores = null)
        {
            var k = Io.Norm(title);
            if (k.Length == 0) return;
            if (!recs.TryGetValue(k, out var e))
            {
                e = (new Registro { Title = title!, Date = date, Key = k }, new HashSet<string>(StringComparer.Ordinal));
                recs[k] = e; ordem.Add(k);
            }
            var r = e.r;
            if ((abs ?? "").Length > r.Abstract.Length) r.Abstract = abs!;
            if (string.IsNullOrEmpty(r.Doi)) r.Doi = string.IsNullOrEmpty(doi) ? r.Doi : doi;
            if (string.IsNullOrEmpty(r.Date)) r.Date = string.IsNullOrEmpty(date) ? r.Date : date;
            if (r.Authors.Count == 0 && autores is not null) r.Authors = autores.ToList();
            r.Ids.Add(id);
            e.src.UnionWith(tags);
        }

        var oaSrc = oa["sources"]!.AsObject();
        foreach (var (id, d) in oa["records"]!.AsObject())
            Add((string?)d!["title"], (string?)d["abstract"], (string?)d["date"], (string?)d["doi"], "openalex:" + id,
                oaSrc[id]!.AsArray().Select(t => "OA:" + (string)t!));
        var s2Src = s2["sources"]!.AsObject();
        foreach (var (id, d) in s2["records"]!.AsObject())
        {
            var doi = (string?)d!["externalIds"]?["DOI"];
            Add((string?)d["title"], (string?)d["abstract"] ?? "", (string?)d["publicationDate"], doi is null ? null : "https://doi.org/" + doi,
                "s2:" + id, s2Src[id]!.AsArray().Select(t => "S2:" + (string)t!),
                d["authors"]?.AsArray().Select(a => (string?)a?["name"]).Where(n => !string.IsNullOrWhiteSpace(n)).Select(n => n!));
        }
        foreach (var d in cal["positives"]!.AsArray())
            Add((string?)d!["title"], (string?)d["abstract"], (string?)d["date"], (string?)d["doi"], "openalex:" + (string)d["id"]!, ["SEED"]);

        // DOI repetido com títulos distintos: funde no primeiro registro.
        var porDoi = new Dictionary<string, string>();
        foreach (var k in ordem.ToList())
        {
            var (r, src) = recs[k];
            if (string.IsNullOrEmpty(r.Doi)) continue;
            var dk = r.Doi.ToLowerInvariant();
            if (porDoi.TryGetValue(dk, out var k0) && recs.ContainsKey(k0))
            {
                recs[k0].src.UnionWith(src); recs[k0].r.Ids.AddRange(r.Ids);
                recs.Remove(k); ordem.Remove(k);
            }
            else porDoi[dk] = k;
        }

        var saida = new List<Registro>();
        foreach (var k in ordem)
        {
            var (r, src) = recs[k];
            r.Src = src.OrderBy(s => s, StringComparer.Ordinal).ToList();
            var (cand, th, ex) = Criterios.Triar(r.Title, r.Abstract);
            bool naJanela = !string.IsNullOrEmpty(r.Date) && string.CompareOrdinal(c.Inicio, r.Date) <= 0 && string.CompareOrdinal(r.Date, c.Fim) <= 0;
            if (!naJanela) { cand = false; ex.Add("E1"); }
            if (r.Abstract.Length == 0) ex.Add("noabs");
            r.Decision = cand ? "candidate" : "reject";
            r.Themes = th; r.Excl = ex;
            r.Core = cand ? Criterios.Nucleo(r.Title, r.Abstract) : [];
            r.Tier = r.Core.Count > 0 ? "core" : cand ? "context" : "excluded";
            saida.Add(r);
        }
        Io.Gravar(c.D("pretriagem.json.gz"), saida);

        Console.WriteLine($"Registros únicos: {saida.Count}");
        foreach (var g in saida.GroupBy(r => r.Tier)) Console.WriteLine($"  faixa {g.Key}: {g.Count()}");
        foreach (var b in new[] { "positives", "negatives" })
        {
            var arr = cal[b]!.AsArray();
            var k = arr.Count(d => Criterios.Triar((string?)d!["title"], (string?)d["abstract"]).candidato);
            Console.WriteLine($"  calibração {b}: {k}/{arr.Count} candidatos pelas regras");
        }
    }
}

// ---------------------------------------------------------------- lotes de leitura e amostra de auditoria

static class Lotes
{
    public static bool PrecisaLeitura(Registro r, Regex semResumo) =>
        r.Tier is "core" or "context" || (r.Tier == "excluded" && r.Excl.Contains("noabs") && semResumo.IsMatch(r.Title));

    public static Regex RegexSemResumo(Contexto c) =>
        new((string)c.P["triagem"]!["regex_titulo_sem_resumo"]!, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);

    // Embaralhamento determinístico: ordena pelo SHA-256 de "semente:chave".
    static List<Registro> Embaralhar(IEnumerable<Registro> rs, string semente) =>
        rs.OrderBy(r => Io.Hash(semente + ":" + r.Key), StringComparer.Ordinal).ToList();

    static string Linha(Registro r, int max) => new JsonObject
    {
        ["key"] = r.Key, ["title"] = r.Title,
        ["abstract"] = r.Abstract.Length > max ? r.Abstract[..max] : r.Abstract,
    }.ToJsonString(Io.J);

    public static void Executar(Contexto c)
    {
        var t = c.P["triagem"]!;
        int nNucleo = (int)t["lotes_nucleo"]!, nContexto = (int)t["lotes_contexto"]!, max = (int)t["max_caracteres_resumo"]!;
        var rs = Io.Ler<List<Registro>>(c.D("pretriagem.json.gz"));
        var semResumo = RegexSemResumo(c);
        var nucleo = Embaralhar(rs.Where(r => r.Tier == "core"), "nucleo");
        var extra = Embaralhar(rs.Where(r => r.Tier != "core" && PrecisaLeitura(r, semResumo)), "contexto");
        var dir = c.D("lotes");
        if (Directory.Exists(dir)) Directory.Delete(dir, true);
        Directory.CreateDirectory(dir);
        void Grava(List<Registro> lista, int n, int desloc)
        {
            for (int i = 0; i < n; i++)
            {
                var parte = lista.Where((_, j) => j % n == i).ToList();
                File.WriteAllLines(Path.Combine(dir, $"lote_{desloc + i:00}.jsonl"), parte.Select(r => Linha(r, max)));
                Console.WriteLine($"lote_{desloc + i:00}: {parte.Count}");
            }
        }
        Grava(nucleo, nNucleo, 0);
        Grava(extra, nContexto, nNucleo);

        // Amostra de auditoria dos excluídos sem leitura (reaproveita amostra.txt se já existir).
        var amostraPath = c.D("auditoria", "amostra.txt");
        var excluidos = rs.Where(r => r.Tier == "excluded" && !PrecisaLeitura(r, semResumo)).ToDictionary(r => r.Key);
        List<string> chaves;
        if (File.Exists(amostraPath)) chaves = File.ReadAllLines(amostraPath).Where(l => l.Length > 0).ToList();
        else
        {
            chaves = Embaralhar(excluidos.Values, "auditoria").Take((int)c.P["auditoria"]!["tamanho"]!).Select(r => r.Key).ToList();
            Directory.CreateDirectory(Path.GetDirectoryName(amostraPath)!);
            File.WriteAllLines(amostraPath, chaves);
        }
        var audDir = c.D("auditoria", "lotes");
        Directory.CreateDirectory(audDir);
        File.WriteAllLines(Path.Combine(audDir, "auditoria.jsonl"), chaves.Where(excluidos.ContainsKey).Select(k => Linha(excluidos[k], max)));
        Console.WriteLine($"auditoria: {chaves.Count} de {excluidos.Count} excluídos sem leitura");
    }
}

// ---------------------------------------------------------------- consolidação

static class Consolidacao
{
    public static Dictionary<string, JsonObject> Decisoes(string dir)
    {
        var d = new Dictionary<string, JsonObject>();
        if (!Directory.Exists(dir)) return d;
        foreach (var f in Directory.GetFiles(dir, "*.jsonl").OrderBy(f => f, StringComparer.Ordinal))
            foreach (var o in Io.Jsonl(f)) d[(string)o["key"]!] = o;
        return d;
    }

    public static void Executar(Contexto c, bool permitirPendentes)
    {
        var rs = Io.Ler<List<Registro>>(c.D("pretriagem.json.gz"));
        var cal = Io.LerNode(c.D("calibracao.json.gz"));
        var dec = Decisoes(c.D("decisoes"));
        var semResumo = Lotes.RegexSemResumo(c);
        var esperadas = rs.Where(r => Lotes.PrecisaLeitura(r, semResumo)).Select(r => r.Key).ToHashSet();
        var pendentes = esperadas.Where(k => !dec.ContainsKey(k)).ToList();
        var sobrando = dec.Keys.Where(k => !esperadas.Contains(k)).ToList();
        Console.WriteLine($"Decisões: {dec.Count}; esperadas: {esperadas.Count}; pendentes: {pendentes.Count}; fora da lista de leitura: {sobrando.Count}");
        if (pendentes.Count > 0 && !permitirPendentes)
            throw new InvalidOperationException($"{pendentes.Count} registros ainda sem decisão. Execute scripts/triagem.cs ou use --permitir-pendentes.");

        foreach (var r in rs)
        {
            if (dec.TryGetValue(r.Key, out var d))
            {
                r.Final = (string)d["decision"]!;
                r.Codes = d["codes"]!.AsArray().Select(x => (string)x!).ToList();
                r.Rel = (int?)d["relevance"] ?? 0;
                r.Note = (string?)d["note"] ?? "";
                r.ScreenedByReading = true;
            }
            else
            {
                r.Final = r.Tier == "excluded" ? "EXCLUDE" : null;
                r.Codes = r.Excl; r.Rel = 0; r.Note = "pré-triagem automática"; r.ScreenedByReading = false;
            }
        }
        Io.Gravar(c.D("consolidado.json.gz"), rs);

        foreach (var g in rs.GroupBy(r => r.Final ?? "PENDENTE").OrderBy(g => g.Key)) Console.WriteLine($"  {g.Key}: {g.Count()}");
        var idx = rs.ToDictionary(r => r.Key);
        Console.WriteLine("Controles do QGS:");
        foreach (var d in cal["positives"]!.AsArray())
        {
            var o = idx.GetValueOrDefault(Io.Norm((string?)d!["title"]));
            Console.WriteLine($"  {o?.Final ?? "AUSENTE",-8} R{o?.Rel ?? 0} {Trunc((string)d["title"]!, 85)}");
        }
    }

    static string Trunc(string s, int n) => s.Length > n ? s[..n] : s;
}

// ---------------------------------------------------------------- relatório (quadros, CSV, RIS, Markdown)

static class Relatorio
{
    static readonly CultureInfo BR = CultureInfo.GetCultureInfo("pt-BR");
    static string N(int n) => n.ToString("N0", BR);
    static string Pct(int a, int b) => b == 0 ? "NR" : $"{Math.Round(100.0 * a / b, MidpointRounding.AwayFromZero):0}%";
    static string P1(double x) => (100 * x).ToString("0.0", BR) + "%";

    static (double lo, double hi) Wilson(int k, int n, double z = 1.96)
    {
        double p = (double)k / n, z2 = z * z, den = 1 + z2 / n;
        double centro = (p + z2 / (2 * n)) / den, meia = z * Math.Sqrt(p * (1 - p) / n + z2 / (4.0 * n * n)) / den;
        return (Math.Max(0, centro - meia), Math.Min(1, centro + meia));
    }

    static string Link(Registro o)
    {
        if (!string.IsNullOrEmpty(o.Doi)) return o.Doi.StartsWith("http") ? o.Doi : "https://doi.org/" + o.Doi;
        foreach (var i in o.Ids) if (i.StartsWith("openalex:")) return "https://openalex.org/" + i[9..];
        foreach (var i in o.Ids) if (i.StartsWith("s2:")) return "https://www.semanticscholar.org/paper/" + i[3..];
        return "";
    }
    static string Data(Registro o) { var x = o.Date ?? "NR"; return x.EndsWith("-01-01") ? x[..4] + "†" : x[..Math.Min(7, x.Length)]; }
    static string Esc(string? s) => (s ?? "").Replace("|", "\\|").Replace("\n", " ").Trim();
    static string Origem(Registro o)
    {
        bool oa = o.Src.Any(x => x.StartsWith("OA:")), s2q = o.Src.Any(x => x.StartsWith("S2:S")), sb = o.Src.Any(x => x.StartsWith("S2:FW") || x.StartsWith("S2:BW"));
        var s = (oa ? "OA" : "") + (s2q ? "+S2" : "") + (sb ? "+SB" : "");
        return s.Length == 0 ? "SEED" : s;
    }
    static string Curto(string t) => t.Split(':')[0].Trim();
    static string Csv(string? v) => v is null ? "" : v.IndexOfAny([',', '"', '\r', '\n']) >= 0 ? "\"" + v.Replace("\"", "\"\"") + "\"" : v;
    static Dictionary<string, int> Conta(IEnumerable<string> xs) => xs.GroupBy(x => x).ToDictionary(g => g.Key, g => g.Count());
    static int G(Dictionary<string, int> d, string k) => d.GetValueOrDefault(k);
    static string Lista(Dictionary<string, int> d, Func<string, string>? rot = null) =>
        string.Join(" | ", d.OrderByDescending(kv => kv.Value).ThenBy(kv => kv.Key, StringComparer.Ordinal).Select(kv => $"{(rot ?? (x => x))(kv.Key)}: {N(kv.Value)}"));

    public static void Executar(Contexto c)
    {
        var d = Io.Ler<List<Registro>>(c.D("consolidado.json.gz"));
        if (d.Any(o => o.Final is null)) Console.WriteLine("AVISO: há registros sem decisão final; o relatório ficará incompleto.");
        var oa = Io.LerNode(c.D("openalex.json.gz"));
        var s2 = Io.LerNode(c.D("semanticscholar.json.gz"));
        var cal = Io.LerNode(c.D("calibracao.json.gz"));
        var rel = c.P["relatorio"]!;
        var notas = rel["notas_revisadas"]!.AsObject().Select(kv => (kv.Key, (string)kv.Value!)).ToList();
        foreach (var o in d) foreach (var (k, v) in notas) if (o.Title.StartsWith(k)) o.Note = v;

        var V = new Dictionary<string, string>();
        var idx = d.ToDictionary(o => o.Key);

        // Recuperação por string
        var oaMeta = oa["meta"]!.AsObject(); var oaSrc = oa["sources"]!.AsObject();
        var s2Rep = s2["report"]!; var s2Src = s2["sources"]!.AsObject();
        var oaColetados = Conta(oaSrc.SelectMany(kv => kv.Value!.AsArray().Select(x => (string)x!)));
        var s2Coletados = Conta(s2Src.SelectMany(kv => kv.Value!.AsArray().Select(x => (string)x!)));
        string Cel(int total, int col) => total == col ? N(total) : $"{N(total)} (coletados {N(col)})";
        var linhas = new List<string>(); int somaOa = 0, somaS2 = 0;
        foreach (var (k, _) in c.Strings("strings_openalex"))
        {
            int to = (int?)oaMeta[k] ?? 0, ts = (int?)s2Rep["queries"]?[k]?["total"] ?? 0;
            somaOa += G(oaColetados, k); somaS2 += G(s2Coletados, k);
            linhas.Add($"| {k} | {Cel(to, G(oaColetados, k))} | {Cel(ts, G(s2Coletados, k))} |");
        }
        linhas.Add($"| **Soma (com sobreposição entre strings)** | **{N(somaOa)}** | **{N(somaS2)}** |");
        linhas.Add($"| **Registros únicos na base** | **{N(oa["records"]!.AsObject().Count)}** | **{N(s2["records"]!.AsObject().Count)}**, incluindo o *snowballing* |");
        V["TABELA_RECUPERACAO"] = string.Join("\n", linhas);
        V["OA_PAGINAS"] = N(oa["pages"]!.AsObject().Sum(kv => (int)kv.Value!));

        var lm = (string)c.P["strings_openalex"]!["S1"]!; lm = lm[..(lm.IndexOf(" AND ", StringComparison.Ordinal))];
        V["TABELA_STRINGS"] = "| Código | Faceta | String booleana (sintaxe OpenAlex) |\n|---|---|---|\n" + string.Join("\n",
            c.Strings("strings_openalex").Select(kv => $"| {kv.k} | {(string?)c.P["facetas"]?[kv.k] ?? ""} | `{(kv.v.StartsWith(lm + " AND ") ? "LM" + kv.v[lm.Length..] : kv.v)}` |"));

        // Sensibilidade frente ao QGS (a partir dos snapshots)
        var pos = cal["positives"]!.AsArray().Select(x => x!).ToList();
        var oaIds = oa["records"]!.AsObject().Select(kv => kv.Key).ToHashSet();
        var s2Rec = s2["records"]!.AsObject();
        var s2Strings = s2Rec.Where(kv => s2Src[kv.Key]!.AsArray().Any(t => ((string)t!).StartsWith('S'))).Select(kv => Io.Norm((string?)kv.Value!["title"])).ToHashSet();
        var s2Todos = s2Rec.Select(kv => Io.Norm((string?)kv.Value!["title"])).ToHashSet();
        bool HitOa(JsonNode p) => oaIds.Contains((string)p["id"]!);
        V["QGS_N"] = N(pos.Count);
        V["QGS_OA"] = N(pos.Count(HitOa)); V["QGS_OA_PCT"] = Pct(pos.Count(HitOa), pos.Count);
        var falt = pos.Where(p => !HitOa(p)).Select(p => Curto((string)p["title"]!)).ToList();
        V["QGS_OA_FALTANTES"] = falt.Count == 0 ? "nenhum" : string.Join(", ", falt);
        int hs2 = pos.Count(p => s2Strings.Contains(Io.Norm((string?)p["title"])));
        V["QGS_S2"] = N(hs2); V["QGS_S2_PCT"] = Pct(hs2, pos.Count);
        V["QGS_UNIAO"] = N(pos.Count(p => HitOa(p) || s2Todos.Contains(Io.Norm((string?)p["title"]))));

        // Snowballing
        var sementes = c.P["sementes_snowballing"]!.AsArray();
        V["SB_N"] = N(sementes.Count);
        var seeds = s2Rep["seeds"]!.AsObject();
        V["SB_DETALHE"] = string.Join(", ", seeds.Where(kv => (bool?)kv.Value!["resolved"] != false)
            .Select(kv => $"{kv.Key} ({(int)kv.Value!["forward_in_window"]!}/{(int)kv.Value!["backward_in_window"]!})"));
        var naoRes = seeds.Where(kv => (bool?)kv.Value!["resolved"] == false).Select(kv => $"{kv.Key} ({Curto((string)kv.Value!["title"]!)})").ToList();
        V["SB_NAO_RESOLVIDAS"] = naoRes.Count == 0 ? "nenhuma" : string.Join(", ", naoRes);

        // Origem e pré-triagem
        var origem = Conta(d.Select(Origem));
        V["TOTAL"] = N(d.Count);
        V["ORIG_AMBAS"] = N(G(origem, "OA+S2") + G(origem, "OA+S2+SB"));
        V["ORIG_OA"] = N(G(origem, "OA") + G(origem, "OA+SB"));
        V["ORIG_S2"] = N(G(origem, "+S2") + G(origem, "+S2+SB"));
        V["ORIG_SB"] = N(G(origem, "+SB"));
        V["ORIG_SEED"] = N(G(origem, "SEED"));
        var tier = Conta(d.Select(o => o.Tier));
        V["TIER_CORE"] = N(G(tier, "core")); V["TIER_CONTEXT"] = N(G(tier, "context")); V["TIER_EXCL"] = N(G(tier, "excluded"));
        var lidos = d.Where(o => o.ScreenedByReading).ToList();
        var lidosTier = Conta(lidos.Select(o => o.Tier));
        V["LIDOS"] = N(lidos.Count); V["LIDOS_EXCL"] = N(G(lidosTier, "excluded"));
        var tamLotes = Directory.Exists(c.D("decisoes")) ? Directory.GetFiles(c.D("decisoes"), "*.jsonl").Select(f => Io.Jsonl(f).Count()).ToList() : [0];
        V["LOTES_N"] = N(tamLotes.Count); V["LOTE_MIN"] = N(tamLotes.Min()); V["LOTE_MAX"] = N(tamLotes.Max());
        var auto = d.Where(o => o.Tier == "excluded" && !o.ScreenedByReading).ToList();
        V["AUTO_EXCL"] = N(auto.Count);

        // Leitura
        var final = Conta(d.Select(o => o.Final ?? "PENDENTE"));
        var finalLido = Conta(lidos.Select(o => o.Final!));
        var core = d.Where(o => o.Final == "CORE").ToList();
        var coreRel = Conta(core.Select(o => o.Rel.ToString()));
        V["CORE"] = N(core.Count); V["CORE_R3"] = N(G(coreRel, "3"));
        foreach (var ic in new[] { "IC1", "IC2", "IC3", "IC4" })
        {
            V["CORE_" + ic] = N(core.Count(o => o.Codes.Contains(ic)));
            V["R3_" + ic] = N(core.Count(o => o.Rel == 3 && o.Codes.Contains(ic)));
        }
        var ano = Conta(core.Select(o => (o.Date ?? "NR")[..Math.Min(4, (o.Date ?? "NR").Length)]));
        V["CORE_2025"] = N(G(ano, "2025")); V["CORE_2026"] = N(G(ano, "2026"));
        V["SB_CORE"] = N(core.Count(o => Origem(o) == "+SB"));
        foreach (var t in new[] { "core", "context", "excluded" })
            foreach (var f in new[] { "CORE", "CONTEXT", "EXCLUDE" })
                V[$"TX_{t}_{f}"] = N(lidos.Count(o => o.Tier == t && o.Final == f));

        // Controles
        var ctrl = pos.Select(p => idx.GetValueOrDefault(Io.Norm((string?)p["title"]))).ToList();
        int cc = ctrl.Count(o => o?.Final == "CORE"), ccx = ctrl.Count(o => o?.Final is "CORE" or "CONTEXT");
        V["CTRL_CORE"] = N(cc); V["CTRL_CORE_PCT"] = Pct(cc, pos.Count);
        V["CTRL_CORE_CTX"] = N(ccx); V["CTRL_CORE_CTX_PCT"] = Pct(ccx, pos.Count);
        var neg = cal["negatives"]!.AsArray().Select(p => idx.GetValueOrDefault(Io.Norm((string?)p!["title"]))).ToList();
        V["NEG_N"] = N(neg.Count); V["NEG_RECUP"] = N(neg.Count(o => o is not null));
        V["NEG_CORE"] = N(neg.Count(o => o?.Final == "CORE")); V["NEG_CTX"] = N(neg.Count(o => o?.Final == "CONTEXT"));
        V["NEG_EXC"] = N(neg.Count(o => o?.Final == "EXCLUDE")); V["NEG_NAO_RECUP"] = N(neg.Count(o => o is null));

        // Fluxo
        var autoCod = Conta(auto.Select(o => o.Excl.Count > 0 ? o.Excl[0] : "sem faceta"));
        string RotAuto(string k) => k switch { "sem faceta" => "sem faceta temática", "noabs" => "sem resumo e sem termo de memória no título", _ => k };
        var exclLidos = Conta(lidos.Where(o => o.Final == "EXCLUDE").Select(o => o.Codes.Count > 0 ? o.Codes[0] : "NR"));
        var autoItens = Lista(autoCod, RotAuto).Split(" | ");
        var fluxo = new StringBuilder();
        fluxo.AppendLine("Identificação");
        fluxo.AppendLine($"  OpenAlex, S1–S6: {N(somaOa)} ocorrências → {N(oa["records"]!.AsObject().Count)} únicos");
        fluxo.AppendLine($"  Semantic Scholar, S1–S6 e snowballing: {N(somaS2)} ocorrências das strings, mais o snowballing → {N(s2Rec.Count)} únicos");
        fluxo.AppendLine($"  Sementes dirigidas: {V["ORIG_SEED"]}");
        fluxo.AppendLine("        ↓ deduplicação por DOI e título normalizado");
        fluxo.AppendLine($"Registros únicos: {V["TOTAL"]}");
        fluxo.AppendLine("        ↓ pré-triagem por regras, usada para priorização");
        fluxo.AppendLine($"  Núcleo provável: {V["TIER_CORE"]} | Contexto: {V["TIER_CONTEXT"]} | Excluídos: {V["TIER_EXCL"]}");
        fluxo.AppendLine("        ↓");
        fluxo.AppendLine($"  Excluídos automaticamente sem leitura: {V["AUTO_EXCL"]}");
        foreach (var bloco in autoItens.Chunk(5)) fluxo.AppendLine("    " + string.Join(" | ", bloco));
        fluxo.AppendLine($"  Lidos por título e resumo: {V["LIDOS"]} = {N(G(lidosTier, "core"))} + {N(G(lidosTier, "context"))} + {N(G(lidosTier, "excluded"))}");
        fluxo.AppendLine("        ↓");
        fluxo.AppendLine($"  EXCLUDE após leitura: {N(G(finalLido, "EXCLUDE"))}");
        fluxo.AppendLine("    " + Lista(exclLidos));
        fluxo.AppendLine($"  CONTEXT: {N(G(final, "CONTEXT"))}");
        fluxo.AppendLine($"  CORE: {V["CORE"]}");
        fluxo.AppendLine($"    relevância 3: {N(G(coreRel, "3"))} | relevância 2: {N(G(coreRel, "2"))} | relevância 1: {N(G(coreRel, "1"))}");
        fluxo.AppendLine("        ↓");
        fluxo.AppendLine("Síntese");
        fluxo.AppendLine($"  Nível 1, Quadros 1 e 2: {V["QGS_N"]} estudos verificados em metadados ou texto e {N(cal["foundations"]!.AsArray().Count)} fundamentos");

        // Quadros
        var q1 = rel["quadro1_prefixos"]!.AsArray().Select(x => (string)x!).ToArray();
        bool NoQ1(Registro o) => q1.Any(p => o.Title.StartsWith(p, StringComparison.Ordinal));
        var r3 = core.Where(o => o.Rel == 3).ToList();
        var inter = r3.Where(o => !NoQ1(o) && (o.Codes.Contains("IC2") || (o.Codes.Contains("IC4") && o.Codes.Count > 1))).ToList();
        var ic4 = r3.Where(o => !NoQ1(o) && o.Codes.SequenceEqual(["IC4"])).ToList();
        V["Q3_N"] = N(inter.Count); V["Q4_N"] = N(ic4.Count); V["NIVEL2_N"] = N(inter.Count + ic4.Count);
        V["R3_OUTROS"] = N(r3.Count(o => !NoQ1(o) && !inter.Contains(o) && !ic4.Contains(o)));
        fluxo.AppendLine($"  Nível 2, Quadros 3 e 4: {V["NIVEL2_N"]} novos estudos CORE de relevância 3 nas interseções do TCC");
        fluxo.AppendLine($"  Nível 3, Apêndice A: todos os {V["CORE_R3"]} estudos CORE de relevância 3");
        fluxo.Append($"  Inventário: todos os {V["TOTAL"]} registros com decisão e justificativa");
        V["FLUXO"] = fluxo.ToString();

        string Ord(Registro o) => o.Date ?? "";
        string Cods(Registro o) => string.Join(", ", o.Codes.OrderBy(x => x, StringComparer.Ordinal));
        string Row(Registro o) => $"| [{Esc(o.Title)}](<{Link(o)}>) | {Data(o)} | {Cods(o)} | {Esc(o.Note)} |";
        const string HDR = "| Trabalho | Data | Critérios | Contribuição e aproximação com o TCC (título e resumo) |\n|---|---|---|---|";
        V["QUADRO3"] = HDR + "\n" + string.Join("\n", inter.OrderBy(Ord, StringComparer.Ordinal).Select(Row));
        V["QUADRO4"] = HDR + "\n" + string.Join("\n", ic4.OrderBy(Ord, StringComparer.Ordinal).Select(Row));
        V["APENDICE_A"] = HDR + "\n" + string.Join("\n", r3.OrderBy(o => string.Join(",", o.Codes.OrderBy(x => x, StringComparer.Ordinal)), StringComparer.Ordinal).ThenBy(Ord, StringComparer.Ordinal).Select(Row));

        // Auditoria dos excluídos sem leitura
        var aud = Consolidacao.Decisoes(c.D("auditoria", "decisoes")).Values.ToList();
        V["AUDITORIA"] = aud.Count == 0 ? "**Auditoria dos excluídos sem leitura:** não executada nesta rodada." : TextoAuditoria(aud, auto.Count, idx);

        V["DATA_EXECUCAO"] = DateTime.ParseExact((string)c.P["data_execucao"]!, "yyyy-MM-dd", CultureInfo.InvariantCulture).ToString("d 'de' MMMM 'de' yyyy", BR);

        // CSV com todos os registros
        var ordemFinal = new Dictionary<string, int> { ["CORE"] = 0, ["CONTEXT"] = 1, ["EXCLUDE"] = 2 };
        var csv = new StringBuilder("titulo,data,link,origem,pre_triagem,lido,decisao,codigos,relevancia,justificativa\r\n");
        foreach (var o in d.OrderBy(o => ordemFinal.GetValueOrDefault(o.Final ?? "", 3)).ThenBy(o => -o.Rel).ThenBy(o => o.Title.ToLowerInvariant(), StringComparer.Ordinal))
            csv.Append(string.Join(",", new[] { o.Title, o.Date, Link(o), string.Join(";", o.Src), o.Tier, o.ScreenedByReading ? "sim" : "não",
                o.Final, string.Join(";", o.Codes), o.Rel == 0 ? "" : o.Rel.ToString(), o.Note }.Select(Csv))).Append("\r\n");
        File.WriteAllText(Path.Combine(c.Saida, "mapeamento_2025_2026_inventario_triagem.csv"), csv.ToString(), new UTF8Encoding(true));

        // RIS do Nível 2
        var ris = new StringBuilder();
        int comAutores = 0;
        foreach (var o in inter.Concat(ic4).OrderBy(Ord, StringComparer.Ordinal))
        {
            var doi = (o.Doi ?? "").Replace("https://doi.org/", "");
            ris.Append(doi.StartsWith("10.18653") ? "TY  - CPAPER\r\n" : "TY  - GEN\r\n");
            ris.Append($"TI  - {o.Title}\r\n");
            foreach (var a in o.Authors) ris.Append($"AU  - {a}\r\n");
            if (o.Authors.Count > 0) comAutores++;
            if (!string.IsNullOrEmpty(o.Date)) ris.Append($"PY  - {o.Date[..4]}\r\nDA  - {o.Date.Replace('-', '/')}\r\n");
            if (doi.Length > 0) ris.Append($"DO  - {doi}\r\n");
            ris.Append($"UR  - {Link(o)}\r\n");
            if (o.Abstract.Length > 0) ris.Append($"AB  - {o.Abstract.Replace("\r", " ").Replace("\n", " ")}\r\n");
            ris.Append($"KW  - mapeamento_2025_2026\r\nKW  - {string.Join(";", o.Codes.OrderBy(x => x, StringComparer.Ordinal))}\r\n");
            ris.Append($"N1  - Triagem por título/resumo: {o.Note}{(o.Authors.Count > 0 ? "" : " Autores não disponíveis nas bases; completar via DOI no Zotero.")}\r\nER  - \r\n\r\n");
        }
        V["RIS_AUTORES"] = N(comAutores);
        File.WriteAllText(Path.Combine(c.Saida, "mapeamento_gu_json_nivel2_2025_2026.ris"), ris.ToString(), new UTF8Encoding(false));

        // Documento final
        var md = File.ReadAllText(c.Modelo).Replace("\r\n", "\n");
        md = Regex.Replace(md, @"\{\{(\w+)\}\}", m => V.TryGetValue(m.Groups[1].Value, out var v) ? v : m.Value);
        var faltam = Regex.Matches(md, @"\{\{(\w+)\}\}").Select(m => m.Groups[1].Value).Distinct().ToList();
        if (faltam.Count > 0) throw new InvalidOperationException("Placeholders sem valor: " + string.Join(", ", faltam));
        File.WriteAllText(Path.Combine(c.Saida, "mapeamento_sistematico_trabalhos_relacionados_2025_2026.md"), md, new UTF8Encoding(false));

        var est = new JsonObject();
        foreach (var (k, v) in V.Where(kv => !kv.Value.Contains('\n')).OrderBy(kv => kv.Key, StringComparer.Ordinal)) est[k] = v;
        Io.Gravar(c.D("estatisticas.json"), est);
        Console.WriteLine($"Relatório: {V["TOTAL"]} registros; CORE={V["CORE"]} (R3={V["CORE_R3"]}); Quadro 3={V["Q3_N"]}; Quadro 4={V["Q4_N"]}; controles CORE={V["CTRL_CORE"]}/{V["QGS_N"]}");
        Console.WriteLine($"Saída: {c.Saida}");
    }

    static string TextoAuditoria(List<JsonObject> aud, int universo, Dictionary<string, Registro> idx)
    {
        int n = aud.Count;
        int core = aud.Count(a => (string?)a["decision"] == "CORE"), ctx = aud.Count(a => (string?)a["decision"] == "CONTEXT");
        var r3 = aud.Where(a => (string?)a["decision"] == "CORE" && ((int?)a["relevance"] ?? 0) == 3).ToList();
        var (lo, hi) = Wilson(core, n);
        var (lo3, hi3) = Wilson(r3.Count, n);
        string Ext(double x) => N((int)Math.Round(universo * x, MidpointRounding.AwayFromZero));
        var sb = new StringBuilder("**Auditoria dos excluídos sem leitura.** ");
        sb.Append($"Uma amostra aleatória de {N(n)} dos {N(universo)} registros excluídos por regra foi lida com o mesmo roteiro. ");
        sb.Append($"O resultado foi {N(n - core - ctx)} EXCLUDE, {N(ctx)} CONTEXT e **{N(core)} CORE** ({P1((double)core / n)}; IC 95% de Wilson: {P1(lo)}–{P1(hi)}). ");
        if (r3.Count > 0)
        {
            var titulos = string.Join("; ", r3.Select(a => idx.TryGetValue((string)a["key"]!, out var o) ? $"*{o.Title}*" : (string)a["key"]!));
            sb.Append($"{(r3.Count == 1 ? "Apenas **1** desses registros tem" : $"**{N(r3.Count)}** desses registros têm")} relevância 3 ({P1((double)r3.Count / n)}; IC 95%: {P1(lo3)}–{P1(hi3)}): {titulos}. ");
        }
        sb.Append($"Extrapolando a amostra, as regras podem ter deixado de fora entre {Ext(lo)} e {Ext(hi)} estudos CORE");
        sb.Append(r3.Count * 2 < core ? ", em sua maioria de relevância 1 ou 2. " : ". ");
        sb.Append($"Para relevância 3, a estimativa fica entre {Ext(lo3)} e {Ext(hi3)} estudos. ");
        sb.Append("Por isso, as contagens de CORE devem ser lidas como **limite inferior**, e os quadros de Nível 2 não esgotam todos os estudos de relevância 3. ");
        sb.Append("As decisões da auditoria estão em `mapeamento_sistematico/dados/<execução>/auditoria/` e não foram somadas às contagens do fluxo.");
        return sb.ToString();
    }
}
