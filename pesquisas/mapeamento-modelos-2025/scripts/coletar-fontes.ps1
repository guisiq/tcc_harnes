[CmdletBinding()]
param(
    [string]$Manifesto = (Join-Path $PSScriptRoot '..\fontes.json'),
    [string]$Saida = (Join-Path $PSScriptRoot ("..\dados\" + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')))
)

$ErrorActionPreference = 'Stop'
$curl = (Get-Command curl.exe -ErrorAction Stop).Source
$config = Get-Content -LiteralPath $Manifesto -Raw | ConvertFrom-Json
if (Test-Path -LiteralPath $Saida) {
    throw "A pasta de saida ja existe: $Saida. Use outra pasta para preservar a coleta anterior."
}
$root = (New-Item -ItemType Directory -Path $Saida).FullName
$evidencias = [System.Collections.Generic.List[object]]::new()
$falhas = [System.Collections.Generic.List[string]]::new()

function Save-Fonte {
    param([string]$Url, [string]$Arquivo, [switch]$PodeSerRestrito)
    $destino = Join-Path $root $Arquivo
    $parent = Split-Path -Parent $destino
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
    $inicio = [DateTime]::UtcNow.ToString('o')
    $status = & $curl --location --silent --show-error --connect-timeout 10 --max-time 45 `
        --retry 1 --retry-delay 1 --user-agent 'TCC-model-mapping/1.0' `
        --output $destino --write-out '%{http_code}' $Url
    $codigo = $LASTEXITCODE
    $http = "$status".Trim()
    $ok = $codigo -eq 0 -and $http -eq '200'
    $restrito = $codigo -eq 0 -and $PodeSerRestrito -and $http -in @('401', '403')
    $hash = if (Test-Path -LiteralPath $destino) {
        (Get-FileHash -LiteralPath $destino -Algorithm SHA256).Hash.ToLowerInvariant()
    } else { $null }
    $evidencias.Add([pscustomobject]@{
        url = $Url; arquivo = $Arquivo; consultado_em_utc = $inicio
        http_status = $http; curl_exit = $codigo; sha256 = $hash
        estado = $(if ($ok) { 'coletado' } elseif ($restrito) { 'acesso_restrito' } else { 'erro' })
    })
    if ($restrito) {
        Write-Warning "Acesso restrito, sem tentativa de contornar autenticacao: $Url (HTTP $http)."
    } elseif (-not $ok) {
        $mensagem = "$Url (HTTP $http; curl $codigo)"
        $falhas.Add($mensagem)
        Write-Warning "Falha de coleta: $mensagem"
    }
    return $ok
}

$resumo = [System.Collections.Generic.List[object]]::new()
foreach ($id in $config.modelos) {
    $nome = $id.Replace('/', '__')
    $arquivo = "modelos\$nome.json"
    if (-not (Save-Fonte "https://huggingface.co/api/models/$id" $arquivo)) { continue }
    $m = Get-Content -LiteralPath (Join-Path $root $arquivo) -Raw | ConvertFrom-Json
    $resumo.Add([pscustomobject]@{
        id = $m.id; created_at = ([DateTimeOffset]$m.createdAt).ToUniversalTime().ToString('o'); revision = $m.sha
        parametros_safetensors = $m.safetensors.total
        arquiteturas = ($m.config.architectures -join ';')
        model_type = $m.config.model_type; licenca = ($m.cardData.license -join ';')
        gated = $m.gated; likes = $m.likes; downloads = $m.downloads
        arquivos_tokenizer = (($m.siblings.rfilename | Where-Object { $_ -match 'tokenizer|vocab|merges|spiece' }) -join ';')
    })
    foreach ($item in @('README.md', 'config.json', 'tokenizer_config.json', 'LICENSE', 'LICENSE.txt', 'LICENSE.md')) {
        if ($m.siblings.rfilename -contains $item) {
            $null = Save-Fonte "https://huggingface.co/$id/raw/$($m.sha)/$item" `
                "modelos\$nome.$item" -PodeSerRestrito
        }
    }
    Write-Output "Modelo: $id; parametros=$($m.safetensors.total)"
}
foreach ($fonte in @($config.buscas) + @($config.fontes_runtime)) {
    $null = Save-Fonte $fonte.url $fonte.arquivo -PodeSerRestrito:([bool]$fonte.pode_ser_restrito)
}
$resumo | Export-Csv -LiteralPath (Join-Path $root 'modelos.csv') -NoTypeInformation -Encoding utf8
$evidencias | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $root 'evidencias.json') -Encoding utf8
$config | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $root 'manifesto-usado.json') -Encoding utf8
$rankingPath = Join-Path $root 'ranking-likes.json'
$rankingColetado = @($evidencias | Where-Object { $_.arquivo -eq 'ranking-likes.json' -and $_.estado -eq 'coletado' })
if ($rankingColetado.Count -eq 1) {
    $ranking = @(Get-Content -LiteralPath $rankingPath -Raw | ConvertFrom-Json)
    $posicao = 0
    $ranking | ForEach-Object {
        $posicao++
        [pscustomobject]@{
            posicao = $posicao; id = $_.id; likes = $_.likes
            downloads = $_.downloads; created_at = ([DateTimeOffset]$_.createdAt).ToUniversalTime().ToString('o')
            licenca = (@($_.tags | Where-Object { $_ -like 'license:*' }) -join ';')
        }
    } | Export-Csv -LiteralPath (Join-Path $root 'ranking-likes.csv') -NoTypeInformation -Encoding utf8
}
if ($falhas.Count -gt 0) {
    $falhas | Set-Content -LiteralPath (Join-Path $root 'erros.txt') -Encoding utf8
    throw "$($falhas.Count) fontes falharam. Coleta INCOMPLETA, consulte erros.txt e evidencias.json em $root."
}
Write-Output "Coleta concluida: $root"
