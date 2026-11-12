[CmdletBinding()]
param(
    [string]$Entrada = (Join-Path $PSScriptRoot '..\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins.md'),
    [string]$Saida,
    [string]$Cabecalho = (Join-Path $PSScriptRoot '..\anexos\Recursos\Cabeçalho oficial 2025.docx'),
    [string]$Config = (Join-Path $PSScriptRoot 'artigo_unitins_config.json'),
    [string]$Python,
    [string]$Pandoc,
    [string]$Csl,
    [string]$MapaZotero,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Get-AbsolutePath {
    param([string]$Path)
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
}

function Get-LabelState {
    param($Document)
    $label = $Document.SensitivityLabel.GetLabel()
    return [pscustomobject]@{
        Enabled = [bool]$label.IsEnabled
        Id = [string]$label.LabelId
        Name = [string]$label.LabelName
    }
}

function Get-MarkingShapes {
    param($Document)
    $shapes = $Document.Sections.Item(1).Footers.Item(1).Shapes
    $matching = [System.Collections.Generic.List[object]]::new()
    for ($index = 1; $index -le $shapes.Count; $index++) {
        $shape = $shapes.Item($index)
        if ($shape.Type -eq 17 -and $shape.TextFrame.HasText -ne 0 -and
            $shape.TextFrame.TextRange.Text.Trim() -ceq '---Internal Use---') {
            $matching.Add($shape)
        }
    }
    return ,$matching
}

function Get-BodyStart {
    param($Document)
    foreach ($paragraph in $Document.Paragraphs) {
        if ([int]$paragraph.OutlineLevel -eq 1) {
            $text = $paragraph.Range.Text.TrimEnd([char]13, [char]7).Trim()
            if (-not $text) {
                continue
            }
            if ($text -ine '1 INTRODUÇÃO') {
                throw "O primeiro título do corpo não é '1 Introdução': $text"
            }
            return $paragraph
        }
    }
    throw 'Não foi encontrado o primeiro título do corpo.'
}

function Set-PageNumbering {
    param($Word, $Document)
    if ($Document.Sections.Count -ne 1) {
        throw 'O documento preparado deve conter uma seção antes da paginação.'
    }
    $introduction = Get-BodyStart $Document
    $introduction.Format.PageBreakBefore = 0
    $boundary = $introduction.Range.Duplicate
    $boundary.Collapse(1)
    $boundary.InsertBreak(2)
    if ($Document.Sections.Count -ne 2) {
        throw 'Não foi possível inserir a quebra de seção antes da introdução.'
    }
    $firstNumbers = $Document.Sections.Item(1).Headers.Item(1).PageNumbers
    $firstNumbers.RestartNumberingAtSection = $true
    $firstNumbers.StartingNumber = 0
    $header = $Document.Sections.Item(2).Headers.Item(1)
    $header.LinkToPrevious = $false
    $header.PageNumbers.RestartNumberingAtSection = $false
    $number = $header.PageNumbers.Add(2, $true)
    $number.Select()
    $Word.Selection.Range.Font.Name = 'Arial'
    $Word.Selection.Range.Font.Size = 10
    if ($header.Range.Frames.Count -ne 1) {
        throw 'O cabeçalho deve conter exatamente um quadro de numeração.'
    }
    $frame = $header.Range.Frames.Item(1)
    $frame.RelativeVerticalPosition = 1
    $frame.VerticalPosition = $Word.CentimetersToPoints(2)
}

function Get-PageReferences {
    param($Document)
    $bodyStart = (Get-BodyStart $Document).Range.Start
    $front = [System.Collections.Generic.List[object]]::new()
    $targets = [System.Collections.Generic.Dictionary[string, int]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )
    foreach ($paragraph in $Document.Paragraphs) {
        $range = $paragraph.Range
        $text = $range.Text.TrimEnd([char]13, [char]7).Trim()
        if ($range.Start -lt $bodyStart) {
            if ($text -match '^(.+)\t(\d+)$') {
                $front.Add([pscustomobject]@{
                    Paragraph = $paragraph
                    Label = $Matches[1]
                    Page = [int]$Matches[2]
                })
            }
            continue
        }
        if ([int]$paragraph.OutlineLevel -le 9 -or
            $text -match '^(Quadro|Tabela)\s+\d+\s+[–—-]\s+') {
            if ($targets.ContainsKey($text)) {
                throw "Título ou legenda duplicado no corpo: $text"
            }
            $position = $range.Duplicate
            $position.SetRange($range.Start + 1, $range.Start + 1)
            $targets.Add($text, [int]$position.Information(1))
        }
    }
    if ($front.Count -ne $targets.Count) {
        throw "O sumário/lista contém $($front.Count) entradas para $($targets.Count) títulos e legendas."
    }
    foreach ($entry in $front) {
        if (-not $targets.ContainsKey($entry.Label)) {
            throw "A entrada não corresponde a um título ou legenda: $($entry.Label)"
        }
        $entry | Add-Member -NotePropertyName Actual -NotePropertyValue $targets[$entry.Label]
    }
    return ,$front
}

function Update-PageReferences {
    param($Document, [bool]$Update)
    $entries = Get-PageReferences $Document
    $changes = 0
    foreach ($entry in $entries) {
        if ($entry.Page -ne $entry.Actual) {
            $changes++
            if ($Update) {
                $number = $entry.Paragraph.Range.Duplicate
                $end = $number.End - 1
                $number.SetRange($end - $entry.Page.ToString().Length, $end)
                $number.Text = $entry.Actual.ToString()
            }
        }
    }
    return [pscustomobject]@{ Count = $entries.Count; Changes = $changes }
}

function Test-SchedulePage {
    param($Document)
    foreach ($table in $Document.Tables) {
        if ($table.Rows.Count -lt 2) {
            continue
        }
        $first = $table.Cell(2, 1).Range.Text.TrimEnd([char]13, [char]7).Trim()
        if ($first -in @('Ativ.', 'Atividade', 'Atividades')) {
            $start = $table.Range.Duplicate
            $start.SetRange($start.Start + 1, $start.Start + 1)
            $end = $table.Range.Duplicate
            $end.SetRange($end.End - 2, $end.End - 2)
            if ([int]$start.Information(3) -ne [int]$end.Information(3)) {
                throw 'O cronograma ultrapassou uma página; revise a tabela antes de gerar o documento.'
            }
        }
    }
}

$Entrada = Get-AbsolutePath $Entrada
$Cabecalho = Get-AbsolutePath $Cabecalho
$Config = Get-AbsolutePath $Config
if (-not $Saida) {
    $Saida = Join-Path (Split-Path -Parent $Entrada) ("artigo_tcc_unitins_{0}.docx" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
}
$Saida = Get-AbsolutePath $Saida
if ([IO.Path]::GetExtension($Saida) -ine '.docx') {
    throw 'A saída precisa ter a extensão .docx.'
}
if ($Saida -ieq $Cabecalho -or $Saida -ieq $Entrada -or $Saida -ieq $Config) {
    throw 'A saída não pode substituir um arquivo de entrada.'
}
if (-not (Test-Path -LiteralPath (Split-Path -Parent $Saida) -PathType Container)) {
    throw "A pasta de saída não existe: $(Split-Path -Parent $Saida)"
}
if ((Test-Path -LiteralPath $Saida) -and -not $Force) {
    throw "A saída já existe: $Saida. Use outro nome ou -Force para substituí-la."
}
foreach ($file in @($Entrada, $Cabecalho, $Config)) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
        throw "Arquivo necessário não encontrado: $file"
    }
}
if (-not $Python) {
    $command = Get-Command python -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -eq $command) {
        throw 'Python não encontrado. Instale o Python ou informe -Python com o caminho do executável.'
    }
    $Python = $command.Source
}
if (-not $Pandoc) {
    $localPandoc = Join-Path $PSScriptRoot '.tools\pandoc\pandoc.exe'
    if (Test-Path -LiteralPath $localPandoc -PathType Leaf) {
        $Pandoc = $localPandoc
    } else {
        $command = Get-Command pandoc -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -eq $command) {
            throw 'Pandoc não encontrado. Instale-o ou informe -Pandoc com o caminho do executável.'
        }
        $Pandoc = $command.Source
    }
}
if (-not $Csl) {
    $localCsl = Join-Path $PSScriptRoot '.tools\pandoc\associacao-brasileira-de-normas-tecnicas.csl'
    $zoteroCsl = Join-Path $env:USERPROFILE 'Zotero\styles\associacao-brasileira-de-normas-tecnicas.csl'
    if (Test-Path -LiteralPath $localCsl -PathType Leaf) {
        $Csl = $localCsl
    } elseif (Test-Path -LiteralPath $zoteroCsl -PathType Leaf) {
        $Csl = $zoteroCsl
    } else {
        throw 'Estilo CSL da ABNT não encontrado. Instale-o no Zotero ou informe -Csl.'
    }
}
$Pandoc = Get-AbsolutePath $Pandoc
$Csl = Get-AbsolutePath $Csl
if ($MapaZotero) {
    $MapaZotero = Get-AbsolutePath $MapaZotero
}

$work = Join-Path ([IO.Path]::GetTempPath()) ("artigo-unitins-{0}" -f [guid]::NewGuid().ToString('N'))
$word = $null
$document = $null
New-Item -ItemType Directory -Path $work | Out-Null
try {
    $inputs = @($Entrada, $Cabecalho, $Config, $Csl)
    if ($MapaZotero) {
        $inputs += $MapaZotero
    }
    $initialHashes = @{}
    foreach ($inputFile in $inputs) {
        $initialHashes[$inputFile] = (Get-FileHash -LiteralPath $inputFile -Algorithm SHA256).Hash
    }
    $prepared = Join-Path $work 'artigo-preparado.docx'
    $arguments = @(
        (Join-Path $PSScriptRoot 'gerar_artigo_unitins.py'),
        '--entrada', $Entrada,
        '--cabecalho', $Cabecalho,
        '--config', $Config,
        '--pandoc', $Pandoc,
        '--csl', $Csl,
        '--trabalho', $work,
        '--saida', $prepared
    )
    if ($MapaZotero) {
        $arguments += @('--mapa-zotero', $MapaZotero)
    }
    & $Python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "A preparação do DOCX falhou (código $LASTEXITCODE)."
    }

    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($prepared, $false, $false)
    Set-PageNumbering $word $document
    $stable = $false
    for ($pass = 1; $pass -le 5; $pass++) {
        $document.Repaginate()
        $result = Update-PageReferences $document $true
        Write-Output "Paginação ${pass}: $($result.Changes) referências atualizadas."
        if ($result.Changes -eq 0) {
            $stable = $true
            break
        }
    }
    if (-not $stable) {
        throw 'As páginas do sumário e da lista não estabilizaram após cinco tentativas.'
    }
    Test-SchedulePage $document
    $document.Save()
    $labelBefore = Get-LabelState $document
    $markings = Get-MarkingShapes $document
    foreach ($shape in $markings) {
        $shape.Delete()
    }
    if ($markings.Count -gt 0) {
        Write-Output "Removidas $($markings.Count) marcas visuais Internal Use, sem alterar o rótulo."
        $document.Save()
    }
    $document.Close(0)
    $document = $word.Documents.Open($prepared, $false, $true)
    $document.Repaginate()
    $result = Update-PageReferences $document $false
    if ($result.Changes -ne 0) {
        throw "O documento salvo contém $($result.Changes) páginas incorretas no sumário ou na lista."
    }
    Test-SchedulePage $document
    $labelAfter = Get-LabelState $document
    if ($labelBefore.Enabled -ne $labelAfter.Enabled -or $labelBefore.Id -ne $labelAfter.Id -or
        $labelBefore.Name -ne $labelAfter.Name) {
        throw 'O rótulo de confidencialidade foi alterado durante a gravação.'
    }
    if ((Get-MarkingShapes $document).Count -gt 0) {
        throw 'O Word reaplicou a marca Internal Use; verifique a política de confidencialidade.'
    }
    $pages = $document.ComputeStatistics(2)
    $document.Close(0)
    $document = $null
    & $Python (Join-Path $PSScriptRoot 'validar_artigo_unitins.py') `
        --fonte (Join-Path $work 'fonte.md') `
        --corpo (Join-Path $work 'corpo.docx') `
        --final $prepared `
        --pandoc $Pandoc
    if ($LASTEXITCODE -ne 0) {
        throw "A validação do conteúdo falhou (código $LASTEXITCODE)."
    }
    foreach ($inputFile in $inputs) {
        if ((Get-FileHash -LiteralPath $inputFile -Algorithm SHA256).Hash -ne $initialHashes[$inputFile]) {
            throw "Um arquivo de entrada mudou durante a geração: $inputFile. Execute o comando novamente."
        }
    }
    [IO.File]::Copy($prepared, $Saida, [bool]$Force)
    Write-Output "DOCX gerado: $Saida"
    Write-Output "Verificado: $pages páginas; $($result.Count) entradas paginadas; sem a marca visual Internal Use."
}
finally {
    if ($null -ne $document) {
        $document.Close(0)
    }
    if ($null -ne $word) {
        $word.Quit()
    }
    if (Test-Path -LiteralPath $work -PathType Container) {
        Remove-Item -LiteralPath $work -Recurse -Force
    }
}
