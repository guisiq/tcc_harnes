[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Pasta,
    [string]$Revisoes,
    [string]$RevisoesArtigos,
    [string[]]$FontesAdicionais = @()
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $Pasta).Path
$config = Get-Content -LiteralPath (Join-Path $root 'manifesto-usado.json') -Raw | ConvertFrom-Json
$inicio = [DateTimeOffset]$config.inicio
$end = [DateTimeOffset]$config.fim
$indice = @{}
foreach ($line in Get-Content -LiteralPath (Join-Path $root 'paginas.jsonl')) {
    $e = $line | ConvertFrom-Json
    if ($e.estado -ne 'coletado') { continue }
    $key = "$($e.consulta):$($e.pagina)"
    if ($indice.ContainsKey($key)) { throw "Pagina duplicada no indice: $key" }
    $indice[$key] = $e
}
$manual = @{}
$manualArtigos = @{}
if ($Revisoes) {
    foreach ($r in Import-Csv -LiteralPath $Revisoes) {
        if (-not $r.id -or $r.sha -notmatch '^[0-9a-f]{40}$' -or -not $r.motivo -or -not $r.evidencia -or
            $r.decisao -notin @('candidato_documental', 'excluido', 'pendente')) {
            throw "Revisao manual incompleta ou invalida: $($r.id)"
        }
        if ($manual.ContainsKey($r.id)) { throw "Revisao manual duplicada: $($r.id)" }
        $manual[$r.id] = $r
    }
}
if ($RevisoesArtigos) {
    foreach ($r in Import-Csv -LiteralPath $RevisoesArtigos) {
        if (-not $r.id -or -not $r.atualizado -or -not $r.motivo -or -not $r.evidencia -or
            $r.decisao -notin @('modelo_identificado', 'sem_modelo_confirmado', 'excluido', 'pendente')) {
            throw "Revisao bibliografica incompleta ou invalida: $($r.id)"
        }
        if ($manualArtigos.ContainsKey($r.id)) { throw "Revisao bibliografica duplicada: $($r.id)" }
        $manualArtigos[$r.id] = $r
    }
}
$modelos = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::Ordinal)
$artigos = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::Ordinal)
$pagesUsed = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
$rawOccurrences = 0L
$paperOccurrences = 0L
$extraOccurrences = 0L
$fields = @('createdAt', 'lastModified', 'sha', 'tags', 'safetensors', 'config',
    'cardData', 'pipeline_tag', 'likes', 'downloads', 'gated')
$expand = ($fields | ForEach-Object { '&expand%5B%5D=' + $_ }) -join ''

function Read-VerifiedPage {
    param($Entry)
    $path = Join-Path $root $Entry.arquivo
    if (-not (Test-Path -LiteralPath $path) -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Entry.sha256_gzip) {
        throw "Arquivo comprimido ausente ou alterado: $($Entry.arquivo)"
    }
    $file = [IO.File]::OpenRead($path)
    $zip = [IO.Compression.GZipStream]::new($file, [IO.Compression.CompressionMode]::Decompress)
    $buffer = [IO.MemoryStream]::new()
    try {
        $zip.CopyTo($buffer)
        $buffer.Position = 0
        $hash = (Get-FileHash -InputStream $buffer -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($hash -ne $Entry.sha256_resposta) { throw "SHA-256 da resposta divergente: $($Entry.arquivo)" }
        $buffer.Position = 0
        $reader = [IO.StreamReader]::new($buffer, [Text.Encoding]::UTF8, $true, 1024, $true)
        try { return $reader.ReadToEnd() } finally { $reader.Dispose() }
    } finally { $buffer.Dispose(); $zip.Dispose(); $file.Dispose() }
}

function Add-Model {
    param($M, [string]$Origin)
    if (-not $M.id) { throw "Modelo sem ID em $Origin" }
    if (-not $modelos.ContainsKey($M.id)) {
        $compact = [pscustomobject]@{
            id=$M.id; createdAt=$M.createdAt; tags=$M.tags; gated=$M.gated
            likes=$M.likes; downloads=$M.downloads; pipeline_tag=$M.pipeline_tag
            config=[pscustomobject]@{ architectures=$M.config.architectures; model_type=$M.config.model_type }
            cardData=[pscustomobject]@{ license=$M.cardData.license }
            safetensors=[pscustomobject]@{ total=$M.safetensors.total }
        }
        $modelos[$M.id] = [pscustomobject]@{
            modelo = $compact
            origens = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
            revisoes = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        }
    }
    $item = $modelos[$M.id]
    [void]$item.origens.Add($Origin)
    if ($M.sha) { [void]$item.revisoes.Add("$($M.sha)") }
}

function Add-Paper {
    param($Entry, [string]$Origin)
    $url = $Entry.SelectSingleNode('./*[local-name()="id"]').InnerText
    if ($url -notmatch '^https?://arxiv\.org/abs/') { throw "Artigo sem ID valido em $Origin" }
    $id = ($url -replace '^https?://arxiv\.org/abs/', '') -replace 'v\d+$', ''
    if (-not $artigos.ContainsKey($id)) {
        $artigos[$id] = [pscustomobject]@{
            id = $id
            titulo = (($Entry.SelectSingleNode('./*[local-name()="title"]').InnerText -replace '\s+', ' ').Trim())
            resumo = (($Entry.SelectSingleNode('./*[local-name()="summary"]').InnerText -replace '\s+', ' ').Trim())
            publicado = $Entry.SelectSingleNode('./*[local-name()="published"]').InnerText
            atualizado = $Entry.SelectSingleNode('./*[local-name()="updated"]').InnerText
            origens = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        }
    } elseif ($artigos[$id].atualizado -cne $Entry.SelectSingleNode('./*[local-name()="updated"]').InnerText) {
        throw "Versoes diferentes do artigo observadas durante a coleta: $id"
    }
    [void]$artigos[$id].origens.Add($Origin)
}

$queries = @()
foreach ($q in $config.hub) { $queries += [pscustomobject]@{ id=$q.id; tipo='hub'; q=$q } }
foreach ($q in $config.arxiv) { $queries += [pscustomobject]@{ id=('arxiv-' + $q.id); tipo='arxiv'; q=$q } }
foreach ($query in $queries) {
    $conclusionPath = Join-Path $root "paginas\$($query.id)\conclusao.json"
    if (-not (Test-Path -LiteralPath $conclusionPath)) { throw "Consulta incompleta: $($query.id)" }
    $completion = Get-Content -LiteralPath $conclusionPath -Raw | ConvertFrom-Json
    if ($completion.estado -ne 'concluida' -or $completion.tipo -ne $query.tipo -or $completion.paginas -lt 1) {
        throw "Conclusao invalida: $($query.id)"
    }
    $total = 0L
    $previous = $null
    $lastDate = [DateTimeOffset]::MaxValue
    for ($i = 1; $i -le $completion.paginas; $i++) {
        $key = "$($query.id):$i"
        if (-not $indice.ContainsKey($key)) { throw "Pagina ausente no indice: $key" }
        [void]$pagesUsed.Add($key)
        $e = $indice[$key]
        if ($e.tipo -ne $query.tipo -or $e.http_status -ne '200') { throw "Estado HTTP invalido: $key" }
        if ($query.tipo -eq 'hub') {
            $expectedUrl = if ($i -eq 1) {
                "https://huggingface.co/api/models?$($query.q.parametros)&limit=$($config.hub_pagina)&sort=$($query.q.ordenacao)&direction=-1$expand"
            } else { $previous.proxima_url }
            if ($e.url -cne $expectedUrl) { throw "Cadeia de paginacao interrompida: $key" }
            $headerPath = Join-Path $root $e.headers
            if (-not (Test-Path -LiteralPath $headerPath)) { throw "Headers ausentes: $key" }
            $headerText = Get-Content -LiteralPath $headerPath -Raw
            $links = [regex]::Matches($headerText, '(?im)^link:\s*<([^>]+)>;\s*rel="next"\s*$')
            $next = if ($links.Count) { $links[$links.Count - 1].Groups[1].Value } else { $null }
            if ("$($e.proxima_url)" -cne "$next") { throw "Link de paginacao divergente: $key" }
        } else {
            $dateRange = 'submittedDate:[' + $inicio.UtcDateTime.ToString('yyyyMMddHHmm') +
                ' TO ' + $end.UtcDateTime.ToString('yyyyMMddHHmm') + ']'
            $expression = '(' + $query.q.expressao + ') AND ' + $dateRange
            $encoded = [Uri]::EscapeDataString($expression)
            $expectedUrl = "https://export.arxiv.org/api/query?search_query=$encoded&start=$total&max_results=$($config.arxiv_pagina)&sortBy=submittedDate&sortOrder=descending"
            if ($e.url -cne $expectedUrl) { throw "URL arXiv divergente: $key" }
        }
        $body = Read-VerifiedPage $e
        if ($query.tipo -eq 'hub') {
            $items = @(ConvertFrom-Json -InputObject $body -AsHashtable)
            if ($items.Count -ne $e.registros) { throw "Contagem divergente: $key" }
            foreach ($m in $items) {
                if (-not $m.($query.q.ordenacao)) { throw "Data de ordenacao ausente: $key" }
                $date = [DateTimeOffset]$m.($query.q.ordenacao)
                if ($date -gt $lastDate) { throw "Ordenacao nao monotona: $key" }
                $lastDate = $date
                Add-Model $m $key
            }
            $total += $items.Count
            $rawOccurrences += $items.Count
        } else {
            [xml]$doc = $body
            $offset = [int]$doc.SelectSingleNode('//*[local-name()="startIndex"]').InnerText
            $reportedTotal = [int]$doc.SelectSingleNode('//*[local-name()="totalResults"]').InnerText
            $items = @($doc.SelectNodes('//*[local-name()="feed"]/*[local-name()="entry"]'))
            if ($offset -ne $total -or $items.Count -ne $e.registros -or
                $reportedTotal -ne $completion.total_servico) { throw "Pagina arXiv inconsistente: $key" }
            foreach ($paper in $items) { Add-Paper $paper $key }
            $total += $items.Count
            $paperOccurrences += $items.Count
        }
        $previous = $e
    }
    if ($total -ne $completion.registros) { throw "Contagem da consulta divergente: $($query.id)" }
    if ($query.tipo -eq 'hub') {
        if ($completion.encerramento -eq 'atingiu_limite_inferior' -and $lastDate -ge $inicio) {
            throw "Limite inferior nao atingido: $($query.id)"
        }
        if ($completion.encerramento -eq 'sem_proxima_pagina' -and $previous.proxima_url) {
            throw "Consulta terminou com proxima pagina nao coletada: $($query.id)"
        }
        if ($completion.encerramento -eq 'pagina_vazia' -and $previous.registros -ne 0) {
            throw "Encerramento por pagina vazia inconsistente: $($query.id)"
        }
        if ($completion.encerramento -notin @('atingiu_limite_inferior', 'sem_proxima_pagina', 'pagina_vazia')) {
            throw "Encerramento desconhecido: $($query.id)"
        }
    } elseif ($total -ne $completion.total_servico -or $completion.encerramento -ne 'total_alcancado') {
        throw "Literatura incompleta: $($query.id)"
    }
}
if ($pagesUsed.Count -ne $indice.Count) { throw 'Existem paginas coletadas fora das consultas concluidas.' }
foreach ($directory in $FontesAdicionais) {
    $extraRoot = (Resolve-Path -LiteralPath $directory).Path
    $extraName = Split-Path -Leaf $extraRoot
    $extraConfig = Get-Content -LiteralPath (Join-Path $extraRoot 'manifesto-usado.json') -Raw | ConvertFrom-Json
    $evidence = @(Get-Content -LiteralPath (Join-Path $extraRoot 'evidencias.json') -Raw | ConvertFrom-Json)
    foreach ($entry in $evidence) {
        $file = Join-Path $extraRoot $entry.arquivo
        if ($entry.estado -notin @('coletado', 'acesso_restrito') -or
            -not (Test-Path -LiteralPath $file) -or
            (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) {
            throw "Evidencia complementar ausente ou divergente: $extraName/$($entry.arquivo)"
        }
    }
    foreach ($id in $extraConfig.modelos) {
        $relative = 'modelos\' + $id.Replace('/', '__') + '.json'
        $entries = @($evidence | Where-Object { $_.arquivo -eq $relative -and $_.estado -eq 'coletado' })
        if ($entries.Count -ne 1 -or $entries[0].url -ne "https://huggingface.co/api/models/$id") {
            throw "Metadados complementares ausentes ou ambiguos: $id"
        }
        $m = Get-Content -LiteralPath (Join-Path $extraRoot $relative) -Raw | ConvertFrom-Json -AsHashtable
        if ($m.id -cne $id) { throw "ID complementar divergente: $id" }
        Add-Model $m "complemento/$extraName/$relative"
        $extraOccurrences++
    }
}
if (@($config.hub | Where-Object { $_.id -eq 't5gemma' }).Count -gt 0 -and
    -not $modelos.ContainsKey('google/t5gemma-2-270m-270m')) {
    throw 'Regressao: T5Gemma 2 nao apareceu na consulta de descoberta.'
}
foreach ($id in $manual.Keys) {
    if (-not $modelos.ContainsKey($id)) { throw "Revisao manual sem modelo descoberto: $id" }
    if (-not $modelos[$id].revisoes.Contains($manual[$id].sha)) {
        throw "SHA da revisao manual nao consta na coleta: $id"
    }
}
foreach ($id in $manualArtigos.Keys) {
    if (-not $artigos.ContainsKey($id) -or $artigos[$id].atualizado -cne $manualArtigos[$id].atualizado) {
        throw "Artigo ou versao da revisao bibliografica ausente: $id"
    }
}

$stats = [ordered]@{
    consultas_hub = @($config.hub).Count
    consultas_arxiv = @($config.arxiv).Count
    paginas = $pagesUsed.Count
    ocorrencias_hub = $rawOccurrences
    fontes_complementares = $FontesAdicionais.Count
    ocorrencias_complementares = $extraOccurrences
    modelos_distintos = $modelos.Count
    ocorrencias_arxiv = $paperOccurrences
    artigos_distintos = $artigos.Count
    artigos_revisados = $manualArtigos.Count
    candidatos_documentais = 0
    excluidos = 0
    pendentes = 0
    prioridade_alta = 0
    revisoes_divergentes = 0
}
$modelRows = foreach ($id in $modelos.Keys) {
    $item = $modelos[$id]
    $m = $item.modelo
    $tags = @($m.tags)
    $arch = @($m.config.architectures) -join ';'
    $license = if ($m.cardData.license) { @($m.cardData.license) -join ';' }
        else { ($tags | Where-Object { $_ -like 'license:*' } | ForEach-Object { $_ -replace '^license:', '' }) -join ';' }
    $size = $m.safetensors.total
    $date = [DateTimeOffset]$m.createdAt
    $combined = "$id $arch $($m.config.model_type) $($tags -join ' ')"
    $groups = [Collections.Generic.List[string]]::new()
    if ($combined -match '(?i)t5gemma|(^|[ /;:_-])(t5|mt5|bart|mbart|pegasus|longt5|seq2seq)([ /;:_-]|$)|encoder.?decoder') {
        $groups.Add('encoder-decoder-possivel')
    }
    if ($combined -match '(?i)diffusion|bd3lm|mdlm|llada|dreammodel|a2dqwen') { $groups.Add('difusao-possivel') }
    if ($tags -contains 'text-generation') { $groups.Add('geracao-textual') }
    if ($tags -contains 'image-text-to-text') { $groups.Add('multimodal') }
    if (-not $groups.Count) { $groups.Add('verificar-tarefa') }
    $alerts = [Collections.Generic.List[string]]::new()
    $likelyTuned = $id -match '(?i)(^|[/_.-])(it|instruct|instruction|chat|flan|sft|finetun|finetuned|dpo|adapter|lora)([_.-]|$)'
    $likelyQuantized = $id -match '(?i)(^|[/_.-])(gguf|ggml|gptq|awq|onnx|mlx|quantized)([_.-]|$)'
    $baseHint = $id -match '(?i)(^|[/_.-])(base|pretrain|pretrained|pretraining|pt)([_.-]|$)'
    if ($likelyTuned) { $alerts.Add('nome_sugere_ajuste') }
    if ($likelyQuantized) { $alerts.Add('nome_sugere_derivado') }
    if ($null -eq $size) { $alerts.Add('parametros_nao_indexados') }
    elseif ([long]$size -gt 1000000000) { $alerts.Add('indice_acima_1b') }
    if ($date -lt $inicio -or $date -gt $end) { $alerts.Add('data_repo_fora_da_janela') }
    if ($item.revisoes.Count -gt 1) { $alerts.Add('revisoes_divergentes'); $stats.revisoes_divergentes++ }
    $score = 0
    if ($groups -contains 'encoder-decoder-possivel' -or $groups -contains 'difusao-possivel') { $score += 8 }
    if ($baseHint) { $score += 15 }
    if ($null -ne $size -and [long]$size -le 1000000000) { $score += 10 }
    if ($license -match 'apache-2.0|mit|gemma|bsd|cc-by-4.0') { $score += 3 }
    if ($tags -contains 'text-generation' -or $tags -contains 'text2text-generation') { $score += 4 }
    if ($likelyTuned -or $likelyQuantized) { $score -= 30 }
    if ($null -ne $size -and [long]$size -gt 1000000000) { $score -= 15 }
    if ($date -lt $inicio -or $date -gt $end) { $score -= 12 }
    $priority = if ($score -ge 25) { 'alta' } elseif ($score -ge 10) { 'normal' } else { 'baixa' }
    if ($priority -eq 'alta') { $stats.prioridade_alta++ }
    $decision = 'pendente'
    $reason = 'Metadados de descoberta; treinamento, licenca, runtime e memoria exigem verificacao.'
    $evidence = ''
    if (@($tags | Where-Object { $_ -like 'base_model:quantized:*' }).Count -gt 0) {
        $decision = 'excluido'
        $reason = 'O Hub identifica este repositorio como quantizacao derivada; nao e contado como modelo base distinto.'
        $evidence = 'https://huggingface.co/' + $id
    }
    if ($manual.ContainsKey($id)) {
        $review = $manual[$id]
        $decision = $review.decisao
        $reason = $review.motivo
        $evidence = $review.evidencia
    }
    if ($item.revisoes.Count -gt 1 -and $decision -eq 'candidato_documental') {
        $decision = 'pendente'
        $reason = 'Revisoes distintas observadas; confirmar qual SHA foi avaliado.'
    }
    switch ($decision) {
        'candidato_documental' { $stats.candidatos_documentais++ }
        'excluido' { $stats.excluidos++ }
        default { $stats.pendentes++ }
    }
    [pscustomobject]@{
        id=$id; created_at=$date.ToUniversalTime().ToString('o')
        revisoes=(@($item.revisoes | Sort-Object) -join ';')
        parametros_safetensors=$size; arquitetura=$arch; model_type=$m.config.model_type
        licenca_declarada=$license; gated=$m.gated; likes=$m.likes; downloads=$m.downloads
        pipeline=$m.pipeline_tag; grupos=($groups -join ';'); alertas=($alerts -join ';')
        prioridade=$priority; pontuacao=$score; decisao=$decision; motivo=$reason
        evidencia=$evidence; origens=(@($item.origens | Sort-Object) -join ';')
    }
}
$modelRows | Export-Csv -LiteralPath (Join-Path $root 'triagem-modelos.csv') -NoTypeInformation -Encoding utf8
$paperRows = foreach ($id in $artigos.Keys) {
    $p = $artigos[$id]
    $decision = 'pendente'
    $reason = 'Verificar checkpoint base, licenca e runtime no trabalho e nas fontes originais.'
    $evidence = ''
    if ($manualArtigos.ContainsKey($id)) {
        $review = $manualArtigos[$id]
        $decision = $review.decisao
        $reason = $review.motivo
        $evidence = $review.evidencia
    }
    [pscustomobject]@{
        id=$id; titulo=$p.titulo; publicado=$p.publicado; atualizado=$p.atualizado
        resumo=$p.resumo; decisao=$decision; motivo=$reason; evidencia=$evidence
        url=('https://arxiv.org/abs/' + $id); origens=(@($p.origens | Sort-Object) -join ';')
    }
}
$paperRows | Export-Csv -LiteralPath (Join-Path $root 'triagem-artigos.csv') -NoTypeInformation -Encoding utf8
if (@($modelRows).Count -ne $stats.modelos_distintos -or @($paperRows).Count -ne $stats.artigos_distintos) {
    throw 'A consolidacao perdeu registros distintos.'
}
$stats | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $root 'estatisticas.json') -Encoding utf8
Write-Output "Integridade OK: $($stats.paginas) paginas; $($stats.modelos_distintos) modelos; $($stats.artigos_distintos) artigos."
