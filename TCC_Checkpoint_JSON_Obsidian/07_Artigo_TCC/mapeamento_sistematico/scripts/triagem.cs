#!/usr/bin/env dotnet
// Triagem por LLM (Copilot SDK) dos lotes gerados por `mapeamento.cs lotes`.
// Uso: dotnet run scripts/triagem.cs -- [--dados <pasta>] [--alvo principal|auditoria|ambos] [--modelo <id>]
//        [--limite-creditos <n>] [--paralelo <n>] [--max-requisicoes <n>] [--estimar]
// Política de custo (protocolo.json > triagem.llm):
//   * apenas os modelos de menor preço por token (entrada + saída) listados pelo SDK;
//   * teto acumulado entre execuções na mesma pasta (custo_llm.jsonl), nunca acima de 1000;
//   * cada bloco reserva um teto próprio e o repassa ao servidor via SessionLimits.MaxAiCredits.
#:package GitHub.Copilot.SDK@1.0.31
#:property Nullable=enable
#:property PublishAot=false
#:property NoWarn=GHCP001

using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;
using GitHub.Copilot;

Console.OutputEncoding = Encoding.UTF8;
const double TETO_ABSOLUTO = 1000;
const double LIMITE_MINIMO_SESSAO = 30;
const int MAX_TENTATIVAS = 3;

var a = Args.Ler(args);
var dados = Path.GetFullPath(a.Get("dados", "dados/execucao_2026-11-12"));
var protocolo = JsonNode.Parse(File.ReadAllText(a.Get("protocolo", "protocolo/protocolo.json")))!;
var roteiroPath = a.Get("roteiro", "protocolo/roteiro_triagem.md");
var roteiro = File.ReadAllText(roteiroPath);
var llm = protocolo["triagem"]!["llm"]!;
var porRequisicao = int.Parse(a.Get("por-requisicao", (string)protocolo["triagem"]!["registros_por_requisicao"]!.ToString()));
var limite = Math.Min(TETO_ABSOLUTO, Math.Min((double)llm["limite_creditos"]!, double.Parse(a.Get("limite-creditos", "1000"), System.Globalization.CultureInfo.InvariantCulture)));
var saidaPorRegistro = (int)llm["tokens_saida_estimados_por_registro"]!;
var reserva = (double)llm["reserva_por_requisicao"]!;
// O SDK reporta custo mínimo por requisição (AssistantUsageData.Cost), que pode superar o custo por tokens.
var custoMinimo = (double)llm["custo_minimo_por_requisicao"]!;
var paralelo = Math.Clamp(int.Parse(a.Get("paralelo", "1")), 1, 4);
var maxReq = int.Parse(a.Get("max-requisicoes", int.MaxValue.ToString()));
var alvo = a.Get("alvo", "ambos");
if (porRequisicao < 1 || limite <= 0 || maxReq < 1 || alvo is not ("principal" or "auditoria" or "ambos"))
    throw new ArgumentException("Verifique --por-requisicao, --limite-creditos, --max-requisicoes e --alvo.");

var alvos = new List<(string nome, string lotes, string decisoes)>();
if (alvo is "principal" or "ambos") alvos.Add(("principal", Path.Combine(dados, "lotes"), Path.Combine(dados, "decisoes")));
if (alvo is "auditoria" or "ambos") alvos.Add(("auditoria", Path.Combine(dados, "auditoria", "lotes"), Path.Combine(dados, "auditoria", "decisoes")));

// Blocos pendentes (retomada: ignora chaves já decididas em qualquer arquivo do diretório de decisões).
var blocos = new List<Bloco>();
foreach (var (nome, lotesDir, decDir) in alvos)
{
    if (!Directory.Exists(lotesDir)) { Console.WriteLine($"[{nome}] sem lotes em {lotesDir}; execute `mapeamento.cs lotes`."); continue; }
    var feitas = new HashSet<string>();
    if (Directory.Exists(decDir))
        foreach (var f in Directory.GetFiles(decDir, "*.jsonl"))
            foreach (var l in File.ReadLines(f).Where(l => l.Trim().Length > 0))
                feitas.Add((string)JsonNode.Parse(l)!["key"]!);
    foreach (var f in Directory.GetFiles(lotesDir, "*.jsonl").OrderBy(f => f, StringComparer.Ordinal))
    {
        var pend = File.ReadLines(f).Where(l => l.Trim().Length > 0).Select(l => JsonNode.Parse(l)!.AsObject())
            .Where(o => !feitas.Contains((string)o["key"]!)).ToList();
        for (int i = 0; i < pend.Count; i += porRequisicao)
            blocos.Add(new Bloco(nome, Path.GetFileNameWithoutExtension(f), decDir, pend.Skip(i).Take(porRequisicao).ToList()));
    }
}
var pendentes = blocos.Sum(b => b.Registros.Count);
Console.WriteLine($"Pendentes: {pendentes} registros em {blocos.Count} requisições ({porRequisicao}/requisição).");

var razaoCusto = Path.Combine(dados, "custo_llm.jsonl");
double gasto = File.Exists(razaoCusto)
    ? File.ReadLines(razaoCusto).Where(l => l.Trim().Length > 0).Sum(l => (double)JsonNode.Parse(l)!["custo_contabilizado"]!)
    : 0;
Console.WriteLine($"Créditos já consumidos (custo_llm.jsonl): {gasto:F2} de {limite:0.##}.");

await using var client = new CopilotClient();
await client.StartAsync();

// Seleção do modelo: somente o nível de menor preço por token.
var modelos = (await client.ListModelsAsync())
    .Where(m => m.Billing?.TokenPrices?.InputPrice is not null && m.Billing.TokenPrices.OutputPrice is not null)
    .Where(m => m.Policy is null || string.Equals(m.Policy.State.ToString(), "enabled", StringComparison.OrdinalIgnoreCase))
    .Select(m => (m, preco: m.Billing!.TokenPrices!.InputPrice!.Value + m.Billing.TokenPrices.OutputPrice!.Value))
    .ToList();
if (modelos.Count == 0) throw new InvalidOperationException("Nenhum modelo com preço por token disponível.");
var menor = modelos.Min(x => x.preco);
var baratos = modelos.Where(x => x.preco == menor).Select(x => x.m).OrderBy(m => m.Id, StringComparer.Ordinal).ToList();
Console.WriteLine("Modelos de menor preço: " + string.Join(", ", baratos.Select(m => m.Id)));
var pedido = a.Get("modelo", "");
var modelo = pedido.Length == 0 ? baratos[0] : baratos.FirstOrDefault(m => m.Id == pedido)
    ?? throw new InvalidOperationException($"Modelo '{pedido}' não está entre os de menor preço ({string.Join(", ", baratos.Select(m => m.Id))}).");
var tp = modelo.Billing!.TokenPrices!;
double lote = tp.BatchSize is > 0 ? tp.BatchSize.Value : 1_000_000;
double CustoTokens(long entrada, long saida, long cacheLeitura, long cacheEscrita) =>
    ((entrada - cacheLeitura) * tp.InputPrice!.Value + cacheLeitura * (tp.CacheReadPrice ?? tp.InputPrice!.Value)
     + cacheEscrita * (tp.CacheWritePrice ?? tp.InputPrice!.Value) + saida * tp.OutputPrice!.Value) / lote;
double Estimar(Bloco b)
{
    var chars = roteiro.Length + b.Registros.Sum(r => r.ToJsonString().Length) + 600;
    return Math.Max(CustoTokens(chars / 3, b.Registros.Count * saidaPorRegistro, 0, 0) * reserva, custoMinimo);
}
var estimativa = blocos.Sum(b => MAX_TENTATIVAS * Estimar(b));
Console.WriteLine($"Modelo: {modelo.Id} (entrada {tp.InputPrice}, saída {tp.OutputPrice} por {lote:N0} tokens). Estimativa conservadora com até {MAX_TENTATIVAS} tentativas: {estimativa:F2} créditos.");
if (gasto + estimativa > limite) Console.WriteLine($"Aviso: a estimativa excede o teto restante ({limite - gasto:F2}); a execução parará ao atingi-lo.");
if (a.Has("estimar")) return 0;

var manifesto = new JsonObject
{
    ["data_utc"] = DateTime.UtcNow.ToString("o"),
    ["modelo"] = modelo.Id,
    ["sdk"] = "GitHub.Copilot.SDK 1.0.31",
    ["roteiro_sha256"] = Convert.ToHexStringLower(SHA256.HashData(Encoding.UTF8.GetBytes(roteiro))),
    ["registros_por_requisicao"] = porRequisicao,
    ["limite_creditos"] = limite,
};
foreach (var (_, _, decDir) in alvos)
{
    Directory.CreateDirectory(decDir);
    File.WriteAllText(Path.Combine(decDir, "_execucao_llm.json"), manifesto.ToJsonString(new JsonSerializerOptions { WriteIndented = true }));
}

var trava = new object();
double reservado = 0;
bool parar = false;
int enviadas = 0, decididos = 0, falhas = 0;
var jsonOpts = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
var saidaJson = new JsonSerializerOptions { Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

async Task Processar(Bloco b)
{
    double est = Math.Max(LIMITE_MINIMO_SESSAO, MAX_TENTATIVAS * Estimar(b));
    lock (trava)
    {
        if (parar || enviadas >= maxReq) return;
        if (gasto + reservado + est > limite)
        {
            parar = true;
            Console.Error.WriteLine($"Saldo insuficiente para reservar {est:F2} créditos para uma sessão (gasto {gasto:F2}, reservado {reservado:F2}, teto {limite:0.##}); interrompendo.");
            return;
        }
        reservado += est; enviadas++;
    }
    long entrada = 0, saida = 0, cacheL = 0, cacheE = 0; double reportado = 0;
    var restantes = b.Registros.ToDictionary(r => (string)r["key"]!);
    var aceitas = new List<Decisao>();
    try
    {
        await using var sessao = await client.CreateSessionAsync(new SessionConfig
        {
            Model = modelo.Id,
            SystemMessage = new SystemMessageConfig { Mode = SystemMessageMode.Replace, Content = roteiro },
            AvailableTools = [],
            SkipCustomInstructions = true,
            OnPermissionRequest = PermissionHandler.ApproveAll,
            SessionLimits = new SessionLimitsConfig { MaxAiCredits = est },
            OnEvent = ev =>
            {
                if (ev is AssistantUsageEvent u)
                {
                    Interlocked.Add(ref entrada, u.Data.InputTokens ?? 0);
                    Interlocked.Add(ref saida, u.Data.OutputTokens ?? 0);
                    Interlocked.Add(ref cacheL, u.Data.CacheReadTokens ?? 0);
                    Interlocked.Add(ref cacheE, u.Data.CacheWriteTokens ?? 0);
                    lock (trava) reportado += u.Data.Cost ?? 0;
                }
                else if (ev is SessionLimitsExhaustedRequestedEvent)
                {
                    lock (trava) parar = true;
                    Console.Error.WriteLine("Limite de créditos da sessão esgotado no servidor; interrompendo.");
                }
            },
        });
        for (int tentativa = 1; tentativa <= MAX_TENTATIVAS && restantes.Count > 0 && !parar; tentativa++)
        {
            var prompt = "Classifique somente os registros abaixo segundo o roteiro. Devolva exatamente um item por chave em `decisoes`. "
                + "Para EXCLUDE, `codes` deve conter pelo menos um código literal E2, E3, E4, E5, E6, E8 ou E9; "
                + "para CONTEXT, use []; para CORE, use os códigos literais IC1 a IC4 aplicáveis. "
                + "Use relevance 0 para CONTEXT ou EXCLUDE e uma justificativa não vazia em `note`.\n\n"
                + string.Join("\n", restantes.Values.Select(r => r.ToJsonString()));
            try
            {
                var resp = await sessao.SendAndWaitAsync<Resposta>(new MessageOptions { Prompt = prompt }, jsonOpts, TimeSpan.FromMinutes(3));
                foreach (var d in resp?.Decisoes ?? [])
                {
                    if (d.Key is not null && restantes.ContainsKey(d.Key) && Valida(d))
                    {
                        aceitas.Add(d);
                        restantes.Remove(d.Key);
                    }
                    else
                        Console.Error.WriteLine($"  [{b.Lote}] resposta inválida ou chave desconhecida: {JsonSerializer.Serialize(d, saidaJson)}");
                }
            }
            catch (JsonException ex)
            {
                Console.Error.WriteLine($"  [{b.Lote}] JSON inválido na tentativa {tentativa}: {ex.Message.Split('\n')[0]}");
            }
        }
    }
    finally
    {
        var custo = CustoTokens(entrada, saida, cacheL, cacheE);
        var contabilizado = Math.Max(custo, reportado);
        lock (trava)
        {
            reservado -= est; gasto += contabilizado; decididos += aceitas.Count; falhas += restantes.Count;
            Directory.CreateDirectory(b.DirDecisoes);
            File.AppendAllLines(Path.Combine(b.DirDecisoes, $"llm_{b.Lote}.jsonl"), aceitas.Select(d => JsonSerializer.Serialize(d, saidaJson)));
            File.AppendAllText(razaoCusto, new JsonObject
            {
                ["data_utc"] = DateTime.UtcNow.ToString("o"), ["modelo"] = modelo.Id, ["alvo"] = b.Alvo, ["lote"] = b.Lote,
                ["registros"] = b.Registros.Count, ["decididos"] = aceitas.Count,
                ["tokens_entrada"] = entrada, ["tokens_saida"] = saida, ["tokens_cache_leitura"] = cacheL, ["tokens_cache_escrita"] = cacheE,
                ["custo_tokens"] = Math.Round(custo, 4), ["custo_reportado"] = Math.Round(reportado, 4), ["custo_contabilizado"] = Math.Round(contabilizado, 4),
            }.ToJsonString() + "\n");
            Console.WriteLine($"  [{b.Alvo}/{b.Lote}] {aceitas.Count}/{b.Registros.Count} decididos; custo {contabilizado:F3}; acumulado {gasto:F2}/{limite:0.##}");
        }
    }
}

static bool Valida(Decisao d)
{
    var codes = d.Codes ?? [];
    return d.Decision switch
    {
        "CORE" => d.Relevance is >= 1 and <= 3 && codes.Count > 0 && codes.All(c => c is "IC1" or "IC2" or "IC3" or "IC4"),
        "CONTEXT" => d.Relevance == 0,
        "EXCLUDE" => d.Relevance == 0 && codes.Count > 0 && codes.All(c => c.Length == 2 && c[0] == 'E' && char.IsDigit(c[1])),
        _ => false,
    } && !string.IsNullOrWhiteSpace(d.Note) && d.Note.Length <= 200;
}

using (var sem = new SemaphoreSlim(paralelo))
    await Task.WhenAll(blocos.Select(async b =>
    {
        await sem.WaitAsync();
        try { await Processar(b); } finally { sem.Release(); }
    }));

int aindaPendentes = pendentes - decididos;
Console.WriteLine($"Concluído: {decididos} decididos, {aindaPendentes} pendentes ({falhas} em blocos iniciados), {gasto:F2}/{limite:0.##} créditos.");
await client.StopAsync();
if (aindaPendentes > 0) return 2;
return 0;

record Bloco(string Alvo, string Lote, string DirDecisoes, List<JsonObject> Registros);

class Resposta
{
    [JsonPropertyName("decisoes")] public List<Decisao> Decisoes { get; set; } = [];
}

class Decisao
{
    [JsonPropertyName("key")] public string? Key { get; set; }
    [JsonPropertyName("decision")] public string? Decision { get; set; }
    [JsonPropertyName("codes")] public List<string>? Codes { get; set; }
    [JsonPropertyName("relevance")] public int Relevance { get; set; }
    [JsonPropertyName("note")] public string? Note { get; set; }
}

class Args
{
    readonly Dictionary<string, string> v = new();
    public static Args Ler(string[] a)
    {
        var r = new Args();
        for (int i = 0; i < a.Length; i++)
            if (a[i].StartsWith("--"))
                r.v[a[i][2..]] = i + 1 < a.Length && !a[i + 1].StartsWith("--") ? a[++i] : "true";
        return r;
    }
    public string Get(string k, string padrao) => v.TryGetValue(k, out var s) ? s : padrao;
    public bool Has(string k) => v.ContainsKey(k);
}
