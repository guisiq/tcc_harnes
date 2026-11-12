[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Pasta,
    [switch]$RankingPequenos
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $Pasta).Path
$manifesto = Get-Content -LiteralPath (Join-Path $root 'manifesto-usado.json') -Raw | ConvertFrom-Json
$evidencias = @(Get-Content -LiteralPath (Join-Path $root 'evidencias.json') -Raw | ConvertFrom-Json)
$metadados = @(Import-Csv -LiteralPath (Join-Path $root 'modelos.csv'))
if ($metadados.Count -ne $manifesto.modelos.Count) {
    throw "Contagem de modelos divergente: $($metadados.Count) registros para $($manifesto.modelos.Count) IDs."
}
foreach ($e in $evidencias) {
    if ($e.estado -notin @('coletado', 'acesso_restrito')) {
        throw "Coleta incompleta: $($e.url) ($($e.estado))."
    }
    $arquivo = Join-Path $root $e.arquivo
    $hash = (Get-FileHash -LiteralPath $arquivo -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $e.sha256) { throw "SHA-256 divergente: $arquivo" }
}
$memoria = foreach ($m in $metadados) {
    $original = Get-Content -LiteralPath (Join-Path $root ("modelos\" + $m.id.Replace('/', '__') + '.json')) -Raw | ConvertFrom-Json
    if ($original.sha -ne $m.revision -or "$($original.safetensors.total)" -ne "$($m.parametros_safetensors)") {
        throw "Resumo divergente dos metadados originais: $($m.id)."
    }
    $parametros = $original.safetensors.total
    $contagemRejeitada = $m.id -in @($manifesto.exclusoes_ranking.id)
    $kv = $null
    $contexto = $null
    $configNome = "modelos\" + $m.id.Replace('/', '__') + '.config.json'
    $configPublico = @($evidencias | Where-Object { $_.arquivo -eq $configNome -and $_.estado -eq 'coletado' })
    if ($configPublico.Count -eq 1) {
        $c = Get-Content -LiteralPath (Join-Path $root $configNome) -Raw | ConvertFrom-Json
        $contexto = $c.max_position_embeddings
        $dense = @($c.architectures | Where-Object { $_ -in @('Qwen3ForCausalLM', 'LlamaForCausalLM', 'Olmo2ForCausalLM') }).Count -gt 0
        if ($c.architectures -contains 'GraniteMoeHybridForCausalLM') {
            $dense = $c.layer_types.Count -gt 0 -and @($c.layer_types | Where-Object { $_ -ne 'attention' }).Count -eq 0
        }
        if ($dense -and $contexto -ge 10240) {
            $head = if ($c.head_dim) { $c.head_dim } else { $c.hidden_size / $c.num_attention_heads }
            if (-not $c.num_hidden_layers -or -not $c.num_key_value_heads -or -not $head) {
                throw "Dimensoes insuficientes para estimar KV: $($m.id)."
            }
            $kv = (4.0 * $c.num_hidden_layers * $c.num_key_value_heads * $head * 10240 / 1GB).ToString('0.000', [Globalization.CultureInfo]::InvariantCulture)
        }
    }
    [pscustomobject]@{
        id = $m.id
        elementos_serializados = $parametros
        pesos_f16_gib = $(if ($null -ne $parametros -and -not $contagemRejeitada) { (2.0 * $parametros / 1GB).ToString('0.000', [Globalization.CultureInfo]::InvariantCulture) } else { $null })
        contexto_config_publico = $contexto
        kv_f16_10240_gib = $kv
        observacao = $(if ($contagemRejeitada) { 'Estimativa omitida: indice nao representa os parametros logicos do modelo.' } else { 'Somente pesos; nao e pico de VRAM. Contagem serializada requer revisao para pesos packed/tied.' })
    }
}
$memoria | Export-Csv -LiteralPath (Join-Path $root 'estimativa-pesos.csv') -NoTypeInformation -Encoding utf8

if ($RankingPequenos) {
    $lista = @(Get-Content -LiteralPath (Join-Path $root 'ranking-pequenos-bruto.json') -Raw | ConvertFrom-Json)
    if ($lista.Count -ne 20) { throw 'A consulta de popularidade nao retornou os 20 registros esperados.' }
    $excluidos = @($manifesto.exclusoes_ranking.id)
    $selecionados = @($lista | Where-Object { $_.id -notin $excluidos } | Select-Object -First 10)
    if ($selecionados.Count -ne 10) { throw 'Nao ha dez registros apos as exclusoes verificadas.' }
    $posicao = 0
    $anterior = [long]::MaxValue
    $tabela = foreach ($m in $selecionados) {
        $original = Get-Content -LiteralPath (Join-Path $root ("modelos\" + $m.id.Replace('/', '__') + '.json')) -Raw | ConvertFrom-Json
        if ($null -eq $original.safetensors.total -or $original.safetensors.total -gt 1000000000) {
            throw "Tamanho nao confirmado para o ranking: $($m.id)."
        }
        if ($m.likes -gt $anterior) { throw 'A ordem por likes nao e decrescente.' }
        $anterior = $m.likes
        $posicao++
        [pscustomobject]@{
            posicao = $posicao; id = $m.id; likes = $m.likes
            parametros_safetensors = $original.safetensors.total
            licenca = ($original.cardData.license -join ';')
            created_at = ([DateTimeOffset]$m.createdAt).ToUniversalTime().ToString('o')
        }
    }
    $tabela | Export-Csv -LiteralPath (Join-Path $root 'top10-pequenos-verificado.csv') -NoTypeInformation -Encoding utf8
}
Write-Output "Integridade validada: $($metadados.Count) modelos; $($evidencias.Count) respostas; $root"
