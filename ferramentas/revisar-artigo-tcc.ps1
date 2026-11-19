param(
    [string]$Pdf = (Join-Path $PSScriptRoot "..\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins_corrigido (1).pdf"),
    [string]$Output = (Join-Path $PSScriptRoot "..\TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\observacoes_artigo_tcc.md"),
    [string]$Model = "mai-code-2-flash",
    [int]$BatchSize = 10,
    [int]$Concurrency = 4,
    [string]$Docx,
    [string]$CommentsOutput,
    [string]$VisualModel = "mai-code-2-flash",
    [int]$VisualBatchSize = 10,
    [int]$VisualDpi = 150,
    [string]$DiagramImage,
    [switch]$SkipVisual,
    [switch]$DeterministicOnly
)

$ErrorActionPreference = 'Stop'
$project = Join-Path $PSScriptRoot "RevisorArtigoTcc\RevisorArtigoTcc.csproj"

$cliArgs = @(
    "--pdf", (Resolve-Path $Pdf).Path,
    "--output", $Output,
    "--model", $Model,
    "--batch-size", $BatchSize.ToString(),
    "--concurrency", $Concurrency.ToString()
)

if ($DeterministicOnly) {
    $cliArgs += "--deterministic-only"
}
if ($Docx) {
    $cliArgs += @("--docx", (Resolve-Path $Docx).Path)
}
if ($CommentsOutput) {
    $cliArgs += @("--comments-output", $CommentsOutput)
}
if ($DiagramImage) {
    $cliArgs += @("--diagram-image", (Resolve-Path $DiagramImage).Path)
}
$cliArgs += @(
    "--visual-model", $VisualModel,
    "--visual-batch-size", $VisualBatchSize.ToString(),
    "--visual-dpi", $VisualDpi.ToString()
)
if ($SkipVisual) {
    $cliArgs += "--skip-visual"
}

& dotnet run --project $project -- @cliArgs
exit $LASTEXITCODE
