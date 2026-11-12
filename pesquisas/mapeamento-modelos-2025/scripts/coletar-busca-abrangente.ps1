[CmdletBinding()]
param(
    [string]$Manifesto = (Join-Path $PSScriptRoot '..\fontes-busca-abrangente.json'),
    [Parameter(Mandatory)][string]$Saida,
    [switch]$Retomar
)

$ErrorActionPreference = 'Stop'
$curl = (Get-Command curl.exe -ErrorAction Stop).Source
$config = Get-Content -LiteralPath $Manifesto -Raw | ConvertFrom-Json
$inicio = [DateTimeOffset]$config.inicio
$fim = [DateTimeOffset]$config.fim
if ($inicio -gt $fim) { throw 'A data inicial e posterior a data final.' }
if (Test-Path -LiteralPath $Saida) {
    if (-not $Retomar) { throw "A pasta ja existe; use -Retomar: $Saida" }
    $root = (Resolve-Path -LiteralPath $Saida).Path
    $savedManifest = Join-Path $root 'manifesto-usado.json'
    if (-not (Test-Path -LiteralPath $savedManifest) -or
        (Get-FileHash -LiteralPath $savedManifest).Hash -ne (Get-FileHash -LiteralPath $Manifesto).Hash) {
        throw 'Nao e possivel retomar: manifesto ausente ou diferente.'
    }
} else {
    if ($Retomar) { throw "Nao existe coleta para retomar: $Saida" }
    $root = (New-Item -ItemType Directory -Path $Saida).FullName
    Copy-Item -LiteralPath $Manifesto -Destination (Join-Path $root 'manifesto-usado.json')
}
$indice = Join-Path $root 'paginas.jsonl'
$anteriores = @{}
if (Test-Path -LiteralPath $indice) {
    foreach ($line in Get-Content -LiteralPath $indice) {
        $e = $line | ConvertFrom-Json
        if ($e.estado -eq 'coletado') { $anteriores["$($e.consulta):$($e.pagina)"] = $e }
    }
}
$fields = @('createdAt', 'lastModified', 'sha', 'tags', 'safetensors', 'config',
    'cardData', 'pipeline_tag', 'likes', 'downloads', 'gated')
$expand = ($fields | ForEach-Object { '&expand%5B%5D=' + $_ }) -join ''
$falhas = [System.Collections.Generic.List[string]]::new()

function Read-Gzip {
    param([string]$Path)
    $file = [IO.File]::OpenRead($Path)
    $zip = [IO.Compression.GZipStream]::new($file, [IO.Compression.CompressionMode]::Decompress)
    $reader = [IO.StreamReader]::new($zip, [Text.Encoding]::UTF8)
    try { return $reader.ReadToEnd() } finally { $reader.Dispose(); $zip.Dispose(); $file.Dispose() }
}

function Save-Page {
    param([string]$Consulta, [int]$Numero, [string]$Url, [string]$Tipo, [int]$Intervalo)
    $key = "${Consulta}:$Numero"
    if ($anteriores.ContainsKey($key)) {
        $e = $anteriores[$key]
        $gz = Join-Path $root $e.arquivo
        if ($e.url -ne $Url -or -not (Test-Path -LiteralPath $gz) -or
            (Get-FileHash -LiteralPath $gz -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256_gzip) {
            throw "Pagina salva divergente, nao retomada: $key"
        }
        return [pscustomobject]@{ evidencia = $e; conteudo = (Read-Gzip $gz) }
    }

    $dir = Join-Path $root ("paginas\" + $Consulta)
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    $stem = Join-Path $dir ('{0:d5}' -f $Numero)
    $raw = "$stem.tmp"
    $headers = "$stem.headers.txt"
    $gz = "$stem.gz"
    Start-Sleep -Milliseconds $Intervalo
    $when = [DateTimeOffset]::UtcNow.ToString('o')
    $http = & $curl --globoff --location --silent --show-error --connect-timeout 15 --max-time 90 `
        --retry 3 --retry-delay 4 --retry-max-time 240 --user-agent 'TCC-model-mapping/2.0' `
        --dump-header $headers --output $raw --write-out '%{http_code}' $Url
    $exitCode = $LASTEXITCODE
    $http = "$http".Trim()
    if ($exitCode -ne 0 -or $http -ne '200' -or -not (Test-Path -LiteralPath $raw)) {
        $e = [pscustomobject]@{ consulta=$Consulta; pagina=$Numero; url=$Url; tipo=$Tipo
            consultado_em_utc=$when; estado='erro'; http_status=$http; curl_exit=$exitCode }
        $e | ConvertTo-Json -Compress | Add-Content -LiteralPath $indice -Encoding utf8
        throw "Falha HTTP na consulta $key (HTTP $http; curl $exitCode)."
    }
    $body = Get-Content -LiteralPath $raw -Raw
    if ($Tipo -eq 'hub') {
        $parsed = @(ConvertFrom-Json -InputObject $body -AsHashtable)
        $count = $parsed.Count
        $headerText = Get-Content -LiteralPath $headers -Raw
        $matches = [regex]::Matches($headerText, '(?im)^link:\s*<([^>]+)>;\s*rel="next"\s*$')
        $next = if ($matches.Count) { $matches[$matches.Count - 1].Groups[1].Value } else { $null }
        if ($next) {
            $nextUri = [Uri]$next
            if ($nextUri.Scheme -ne 'https' -or $nextUri.Host -ne 'huggingface.co') {
                throw "Link de paginacao inesperado: $next"
            }
        }
        $total = $null
    } else {
        [xml]$doc = $body
        $totalNode = $doc.SelectSingleNode('//*[local-name()="totalResults"]')
        $startNode = $doc.SelectSingleNode('//*[local-name()="startIndex"]')
        if (-not $totalNode -or -not $startNode) { throw "Resposta arXiv invalida: $key" }
        $total = [int]$totalNode.InnerText
        $count = @($doc.SelectNodes('//*[local-name()="feed"]/*[local-name()="entry"]')).Count
        $next = $null
    }
    $rawHash = (Get-FileHash -LiteralPath $raw -Algorithm SHA256).Hash.ToLowerInvariant()
    $input = [IO.File]::OpenRead($raw)
    $output = [IO.File]::Create($gz)
    $zip = [IO.Compression.GZipStream]::new($output, [IO.Compression.CompressionMode]::Compress)
    try { $input.CopyTo($zip) } finally { $zip.Dispose(); $output.Dispose(); $input.Dispose() }
    Remove-Item -LiteralPath $raw
    $relative = "paginas\$Consulta\$('{0:d5}' -f $Numero).gz"
    $e = [pscustomobject]@{
        consulta=$Consulta; pagina=$Numero; tipo=$Tipo; url=$Url; consultado_em_utc=$when
        estado='coletado'; http_status=$http; curl_exit=$exitCode; arquivo=$relative
        headers="paginas\$Consulta\$('{0:d5}' -f $Numero).headers.txt"
        sha256_resposta=$rawHash; sha256_gzip=(Get-FileHash -LiteralPath $gz -Algorithm SHA256).Hash.ToLowerInvariant()
        registros=$count; total_servico=$total; proxima_url=$next
    }
    $e | ConvertTo-Json -Compress -Depth 5 | Add-Content -LiteralPath $indice -Encoding utf8
    $anteriores[$key] = $e
    return [pscustomobject]@{ evidencia = $e; conteudo = $body }
}

function Save-Completion {
    param([string]$Id, [string]$Tipo, [int]$Paginas, [long]$Registros, [string]$Motivo, $Total)
    $result = [pscustomobject]@{ consulta=$Id; tipo=$Tipo; estado='concluida'
        paginas=$Paginas; registros=$Registros; encerramento=$Motivo; total_servico=$Total }
    $result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $root "paginas\$Id\conclusao.json") -Encoding utf8
    Write-Output "$Id : $Paginas paginas, $Registros registros, $Motivo"
}

foreach ($q in $config.hub) {
    if ($q.id -notmatch '^[a-z0-9][a-z0-9-]*$' -or $q.ordenacao -notin @('createdAt', 'lastModified')) {
        throw "Consulta Hub invalida: $($q.id)"
    }
    try {
        $url = "https://huggingface.co/api/models?$($q.parametros)&limit=$($config.hub_pagina)&sort=$($q.ordenacao)&direction=-1$expand"
        $page = 0
        $records = 0L
        $lastDate = [DateTimeOffset]::MaxValue
        do {
            $page++
            $result = Save-Page $q.id $page $url 'hub' $config.hub_intervalo_ms
            $items = @(ConvertFrom-Json -InputObject $result.conteudo -AsHashtable)
            $records += $items.Count
            foreach ($m in $items) {
                if (-not $m.id -or -not $m.($q.ordenacao)) { throw "ID/data ausente: $($q.id), pagina $page." }
                $date = [DateTimeOffset]$m.($q.ordenacao)
                if ($date -gt $lastDate) { throw "Ordenacao nao monotona: $($q.id), pagina $page." }
                $lastDate = $date
            }
            $url = $result.evidencia.proxima_url
            $stop = if ($items.Count -eq 0) { 'pagina_vazia' }
                elseif ($lastDate -lt $inicio) { 'atingiu_limite_inferior' }
                elseif (-not $url) { 'sem_proxima_pagina' }
                else { $null }
        } while (-not $stop)
        Save-Completion $q.id 'hub' $page $records $stop $null
    } catch {
        $falhas.Add("$($q.id): $($_.Exception.Message)")
        Write-Warning $falhas[$falhas.Count - 1]
    }
}

foreach ($q in $config.arxiv) {
    $id = 'arxiv-' + $q.id
    if ($id -notmatch '^[a-z0-9][a-z0-9-]*$') { throw "Consulta arXiv invalida: $id" }
    try {
        $dateRange = 'submittedDate:[' + $inicio.UtcDateTime.ToString('yyyyMMddHHmm') +
            ' TO ' + $fim.UtcDateTime.ToString('yyyyMMddHHmm') + ']'
        $expression = '(' + $q.expressao + ') AND ' + $dateRange
        $encoded = [Uri]::EscapeDataString($expression)
        $offset = 0
        $page = 0
        $total = $null
        do {
            $page++
            $url = "https://export.arxiv.org/api/query?search_query=$encoded&start=$offset&max_results=$($config.arxiv_pagina)&sortBy=submittedDate&sortOrder=descending"
            $result = Save-Page $id $page $url 'arxiv' $config.arxiv_intervalo_ms
            [xml]$doc = $result.conteudo
            $reportedStart = [int]$doc.SelectSingleNode('//*[local-name()="startIndex"]').InnerText
            $reportedTotal = [int]$doc.SelectSingleNode('//*[local-name()="totalResults"]').InnerText
            if ($reportedStart -ne $offset) { throw "Offset arXiv inesperado: $id, pagina $page." }
            if ($null -ne $total -and $reportedTotal -ne $total) { throw "Total arXiv mudou durante a paginacao: $id." }
            $total = $reportedTotal
            $entries = @($doc.SelectNodes('//*[local-name()="feed"]/*[local-name()="entry"]'))
            foreach ($entry in $entries) {
                if ($entry.id -notmatch '^https?://arxiv\.org/abs/') { throw "Entrada arXiv invalida: $id, pagina $page." }
            }
            if ($entries.Count -eq 0 -and $offset -lt $total) { throw "Pagina vazia antes do total arXiv: $id." }
            $offset += $entries.Count
        } while ($offset -lt $total)
        Save-Completion $id 'arxiv' $page $offset 'total_alcancado' $total
    } catch {
        $falhas.Add("${id}: $($_.Exception.Message)")
        Write-Warning $falhas[$falhas.Count - 1]
    }
}
if ($falhas.Count) {
    $falhas | Set-Content -LiteralPath (Join-Path $root 'falhas.txt') -Encoding utf8
    throw "Coleta incompleta: $($falhas.Count) consultas falharam. Consulte falhas.txt e use -Retomar."
}
Write-Output "Coleta paginada concluida: $root"
