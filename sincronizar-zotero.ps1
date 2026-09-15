param(
    [string]$ZoteroApiBase = "http://localhost:23119/api/users/0",
    [string]$ZoteroStorageRoot = (Join-Path $env:USERPROFILE "Zotero\storage"),
    [string]$Destination = (Join-Path $PSScriptRoot "artigos"),
    [switch]$NoReadmeUpdate
)

$ErrorActionPreference = "Stop"

function Get-SafeFileName {
    param([string]$Name)

    $safeName = [IO.Path]::GetFileName($Name)
    $safeName = [regex]::Replace($safeName, '[\x00-\x1F<>:"/\\|?*]', '_')
    $safeName = $safeName.Trim().TrimEnd('.', ' ')
    if ([string]::IsNullOrWhiteSpace($safeName)) {
        $safeName = "anexo.pdf"
    }
    if ($safeName -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$') {
        $safeName = "_$safeName"
    }
    return $safeName
}

function ConvertTo-MarkdownTarget {
    param([string]$Name)

    return [Uri]::EscapeDataString($Name).Replace('%2F', '/')
}

function Get-PdfContext {
    param([string]$Name)

    $lower = $Name.ToLowerInvariant()

    if ($lower -match 'systematic|mapping|snowballing|literature review|literature reviews|vosviewer') {
        return 'Metodologia e revisão sistemática'
    }
    if ($lower -match 'memory|conversational|incremental|structural memory|contextual memory|chain-of-memory') {
        return 'Memória de agentes'
    }
    if ($lower -match 'harness|agent|eval|benchmark|judge|tool-use|tool calling|llm-as-judge') {
        return 'Harness e avaliação de agentes'
    }
    if ($lower -match 'small language model|phi-3|recurrentgemma|parameter-efficient|efficientllm|quantization|slm|gemma|llama|qwen') {
        return 'SLM e modelos pequenos'
    }

    return 'Outros'
}

function Update-ReadmeLinks {
    param(
        [string]$ReadmePath,
        [System.IO.FileInfo[]]$PdfFiles
    )

    $startMarker = '<!-- ZOTERO-PDFS-START -->'
    $endMarker = '<!-- ZOTERO-PDFS-END -->'
    $contextOrder = @(
        'Metodologia e revisão sistemática',
        'SLM e modelos pequenos',
        'Memória de agentes',
        'Harness e avaliação de agentes',
        'Outros'
    )

    $groups = @{}
    foreach ($pdf in $PdfFiles) {
        $context = Get-PdfContext -Name $pdf.Name
        if (-not $groups.ContainsKey($context)) {
            $groups[$context] = New-Object System.Collections.Generic.List[string]
        }
        $groups[$context].Add($pdf.Name)
    }

    $lines = @(
        $startMarker
        '## PDFs sincronizados do Zotero'
        ''
        'Links por contexto:'
        ''
    )

    foreach ($context in $contextOrder) {
        if (-not $groups.ContainsKey($context)) {
            continue
        }

        $lines += "### $context"
        $lines += ''
        foreach ($name in ($groups[$context] | Sort-Object)) {
            $target = ConvertTo-MarkdownTarget $name
            $lines += "- [$name]($target)"
        }
        $lines += ''
    }

    $lines += $endMarker
    $generated = $lines -join "`r`n"

    $content = if (Test-Path -LiteralPath $ReadmePath) {
        [IO.File]::ReadAllText($ReadmePath)
    } else {
        "# Artigos`r`n"
    }

    $pattern = '(?s)<!-- ZOTERO-PDFS-START -->.*?<!-- ZOTERO-PDFS-END -->'
    if ($content -match $pattern) {
        $content = [regex]::Replace($content, $pattern, $generated)
    } else {
        $content = $content.TrimEnd() + "`r`n`r`n" + $generated + "`r`n"
    }

    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllText($ReadmePath, $content, $utf8)
}

if (-not (Test-Path -LiteralPath $Destination -PathType Container)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}

$handler = New-Object System.Net.Http.HttpClientHandler
$handler.UseProxy = $false
$httpClient = New-Object System.Net.Http.HttpClient($handler)
$httpClient.DefaultRequestHeaders.Accept.ParseAdd('application/json')
try {
    $itemsJson = $httpClient.GetStringAsync("$ZoteroApiBase/items?format=json&limit=100").GetAwaiter().GetResult()
    $items = @($itemsJson | ConvertFrom-Json)
} finally {
    $httpClient.Dispose()
    $handler.Dispose()
}
$attachments = @($items | Where-Object {
    $_.data.itemType -eq 'attachment' -and
    (([string]$_.data.contentType -ieq 'application/pdf') -or ([string]$_.data.filename -match '(?i)\.pdf$'))
})

$copied = 0
$existing = 0
$missing = 0
$errors = 0

foreach ($attachment in $attachments) {
    try {
        $storageFolder = Join-Path $ZoteroStorageRoot $attachment.key
        if (-not (Test-Path -LiteralPath $storageFolder -PathType Container)) {
            $missing++
            continue
        }

        $source = Get-ChildItem -LiteralPath $storageFolder -File -Recurse |
            Where-Object { $_.Extension -ieq '.pdf' } |
            Select-Object -First 1
        if (-not $source) {
            $missing++
            continue
        }

        $fileName = Get-SafeFileName $attachment.data.filename
        if ([IO.Path]::GetExtension($fileName) -ine '.pdf') {
            $fileName = Get-SafeFileName $source.Name
        }
        $target = Join-Path $Destination $fileName

        if (Test-Path -LiteralPath $target -PathType Leaf) {
            $existing++
            continue
        }
        if (Test-Path -LiteralPath $target) {
            $base = [IO.Path]::GetFileNameWithoutExtension($fileName)
            $extension = [IO.Path]::GetExtension($fileName)
            $target = Join-Path $Destination ("{0}_{1}{2}" -f $base, $attachment.key, $extension)
        }

        Copy-Item -LiteralPath $source.FullName -Destination $target
        $copied++
    } catch {
        $errors++
        Write-Warning "Falha no anexo $($attachment.key): $($_.Exception.Message)"
    }
}

$pdfFiles = @(Get-ChildItem -LiteralPath $Destination -File -Filter '*.pdf' | Sort-Object Name)
if (-not $NoReadmeUpdate) {
    Update-ReadmeLinks -ReadmePath (Join-Path $Destination 'README.md') -PdfFiles $pdfFiles
}

Write-Host "Anexos PDF encontrados: $($attachments.Count)"
Write-Host "Copiados: $copied"
Write-Host "Ja existentes/ignorados: $existing"
Write-Host "Sem arquivo no armazenamento: $missing"
Write-Host "Erros: $errors"
Write-Host "PDFs no destino: $($pdfFiles.Count)"