<#
.SYNOPSIS
  Executa o mapeamento sistemático de ponta a ponta (ou apenas a parte offline).

.EXAMPLE
  ./executar.ps1 -Offline
  Regera CSV, RIS e Markdown a partir dos snapshots e das decisões versionados (sem rede, sem LLM).

.EXAMPLE
  ./executar.ps1 -Dados dados/execucao_2027-01-15
  Nova execução completa: coleta nas APIs, pré-triagem, lotes, triagem por LLM (teto de créditos), consolidação e relatório.
#>
param(
    [string]$Dados = 'dados/execucao_2026-11-12',
    [string]$Saida = '..',
    [string]$Modelo = '',
    [double]$LimiteCreditos = 1000,
    [switch]$Offline,
    [switch]$SomenteEstimar
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

function Etapa([string]$script, [string[]]$argumentos) {
    Write-Host "`n>> dotnet run scripts/$script -- $($argumentos -join ' ')" -ForegroundColor Cyan
    dotnet run "scripts/$script" -- @argumentos
    if ($LASTEXITCODE -ne 0) { throw "Falha em $script $($argumentos[0]) (código $LASTEXITCODE)." }
}

$comum = @('--dados', $Dados)
if ($Offline) {
    Etapa mapeamento.cs (@('offline') + $comum + @('--saida', $Saida))
    return
}

foreach ($cmd in 'calibrar', 'sensibilidade', 'coletar-openalex', 'coletar-s2', 'pretriar', 'lotes') {
    Etapa mapeamento.cs (@($cmd) + $comum)
}

$triagem = $comum + @('--limite-creditos', $LimiteCreditos)
if ($Modelo) { $triagem += @('--modelo', $Modelo) }
Etapa triagem.cs ($triagem + @('--estimar'))
if ($SomenteEstimar) { return }
Etapa triagem.cs $triagem

Etapa mapeamento.cs (@('consolidar') + $comum)
Etapa mapeamento.cs (@('relatorio') + $comum + @('--saida', $Saida))
