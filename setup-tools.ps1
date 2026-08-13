# Script para configurar e baixar ferramentas para Harness Bibliográfico
# Zotero 7+, Docling (IBM), Obsidian, Obsidian Local REST API

param(
    [switch]$SkipZotero,
    [switch]$SkipDocling,
    [switch]$SkipObsidian,
    [switch]$SkipPlugin
)

$ErrorActionPreference = "Stop"

Write-Host "=== Configuração de Ferramentas para Harness Bibliográfico ===" -ForegroundColor Cyan

# Função para verificar se um comando existe
function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Função para criar pasta se não existir
function New-FolderIfNotExists {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "✓ Pasta criada: $Path" -ForegroundColor Green
    }
}

# ==================== ZOTERO ====================
if (-not $SkipZotero) {
    Write-Host "`n[1/4] Instalando Zotero 7+" -ForegroundColor Yellow
    
    try {
        $zoteroUrl = "https://www.zotero.org/download/client/dl?channel=release&platform=win32"
        $zoteroPath = "$env:TEMP\Zotero-Setup.exe"
        
        Write-Host "Baixando Zotero..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $zoteroUrl -OutFile $zoteroPath -UseBasicParsing
        
        Write-Host "Instalando Zotero..." -ForegroundColor Cyan
        Start-Process -FilePath $zoteroPath -ArgumentList "/S" -Wait
        
        Write-Host "✓ Zotero instalado com sucesso!" -ForegroundColor Green
        Remove-Item $zoteroPath -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "✗ Erro ao instalar Zotero: $_" -ForegroundColor Red
    }
}

# ==================== DOCLING ====================
if (-not $SkipDocling) {
    Write-Host "`n[2/4] Instalando Docling (IBM)" -ForegroundColor Yellow
    
    try {
        # Verificar se pip está disponível
        if (Test-Command "pip") {
            Write-Host "Instalando Docling via pip..." -ForegroundColor Cyan
            python -m pip install --upgrade pip
            pip install docling
            
            Write-Host "✓ Docling instalado com sucesso!" -ForegroundColor Green
        } else {
            Write-Host "✗ Python/pip não encontrado. Instale Python 3.8+ antes de continuar." -ForegroundColor Red
            Write-Host "   Baixe em: https://www.python.org/downloads/" -ForegroundColor Gray
        }
    } catch {
        Write-Host "✗ Erro ao instalar Docling: $_" -ForegroundColor Red
    }
}

# ==================== OBSIDIAN ====================
if (-not $SkipObsidian) {
    Write-Host "`n[3/4] Instalando Obsidian" -ForegroundColor Yellow
    
    try {
        $obsidianUrl = "https://github.com/obsidianmd/obsidian-releases/releases/download/latest/Obsidian.exe"
        $obsidianPath = "$env:TEMP\Obsidian-Installer.exe"
        
        Write-Host "Baixando Obsidian..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $obsidianUrl -OutFile $obsidianPath -UseBasicParsing
        
        Write-Host "Instalando Obsidian..." -ForegroundColor Cyan
        Start-Process -FilePath $obsidianPath -Wait
        
        Write-Host "✓ Obsidian instalado com sucesso!" -ForegroundColor Green
        Remove-Item $obsidianPath -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "✗ Erro ao instalar Obsidian: $_" -ForegroundColor Red
    }
}

# ==================== OBSIDIAN LOCAL REST API PLUGIN ====================
if (-not $SkipPlugin) {
    Write-Host "`n[4/4] Configurando Obsidian Local REST API Plugin" -ForegroundColor Yellow
    
    try {
        # Localizar pasta de plugins do Obsidian
        $obsidianVault = "$env:APPDATA\Obsidian\plugins"
        
        # Aguardar o Obsidian ser aberto (se não estiver)
        Write-Host "Aguardando Obsidian inicializar (5 segundos)..." -ForegroundColor Cyan
        Start-Sleep -Seconds 5
        
        # Criar diretório de plugins se não existir
        New-FolderIfNotExists $obsidianVault
        
        # URL do plugin
        $pluginUrl = "https://github.com/coddingtonbear/obsidian-local-rest-api/releases/latest/download/obsidian-local-rest-api.zip"
        $pluginZip = "$env:TEMP\obsidian-local-rest-api.zip"
        $pluginDir = "$obsidianVault\obsidian-local-rest-api"
        
        Write-Host "Baixando Obsidian Local REST API Plugin..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $pluginUrl -OutFile $pluginZip -UseBasicParsing
        
        # Criar diretório do plugin
        New-FolderIfNotExists $pluginDir
        
        Write-Host "Extraindo plugin..." -ForegroundColor Cyan
        Expand-Archive -Path $pluginZip -DestinationPath $pluginDir -Force
        
        Write-Host "✓ Obsidian Local REST API Plugin configurado!" -ForegroundColor Green
        Write-Host "  Local: $pluginDir" -ForegroundColor Gray
        Write-Host "  Próximas etapas:" -ForegroundColor Gray
        Write-Host "  1. Abra Obsidian" -ForegroundColor Gray
        Write-Host "  2. Vá para Configurações > Plugins Instalados" -ForegroundColor Gray
        Write-Host "  3. Ative 'Local REST API'" -ForegroundColor Gray
        
        Remove-Item $pluginZip -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "✗ Erro ao configurar plugin: $_" -ForegroundColor Red
        Write-Host "  Instalação manual: https://github.com/coddingtonbear/obsidian-local-rest-api" -ForegroundColor Gray
    }
}

# ==================== RESUMO FINAL ====================
Write-Host "`n=== Configuração Completa ===" -ForegroundColor Cyan
Write-Host "`nPróximas etapas recomendadas:" -ForegroundColor Yellow
Write-Host "1. Abra Zotero e configure sua biblioteca" -ForegroundColor Gray
Write-Host "2. Configure Obsidian com seu vault pessoal" -ForegroundColor Gray
Write-Host "3. Ative o plugin Local REST API em Obsidian" -ForegroundColor Gray
Write-Host "4. Teste a integração entre as ferramentas" -ForegroundColor Gray

Write-Host "`nDocumentação:" -ForegroundColor Yellow
Write-Host "• Zotero: https://www.zotero.org/support/" -ForegroundColor Gray
Write-Host "• Docling: https://github.com/IBM-Research/docling" -ForegroundColor Gray
Write-Host "• Obsidian: https://help.obsidian.md/" -ForegroundColor Gray
Write-Host "• Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api" -ForegroundColor Gray
