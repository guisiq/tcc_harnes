# Script para configurar e baixar ferramentas para Harness Bibliográfico
# Zotero 7+, Docling (IBM), Obsidian, Obsidian Local REST API

param(
    [switch]$SkipZotero,
    [switch]$SkipDocling,
    [switch]$SkipObsidian,
    [switch]$SkipPlugin
)
$ErrorActionPreference = "Continue"

# Força TLS 1.2 (evita "conexão fechada inesperadamente" em downloads do GitHub)
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

# Função para obter a URL de um asset da última release de um repositório no GitHub
function Get-LatestGitHubAssetUrl {
    param(
        [string]$Repo,        # ex: "obsidianmd/obsidian-releases"
        [string]$NamePattern  # regex para casar o nome do asset, ex: '^Obsidian-.*-x64\.exe$'
    )
    $headers = @{ "User-Agent" = "tcc-harness-setup-script" }
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -Headers $headers -UseBasicParsing
    $asset = $release.assets | Where-Object { $_.name -match $NamePattern } | Select-Object -First 1
    if (-not $asset) {
        throw "Nenhum asset encontrado em $Repo casando com '$NamePattern' (release: $($release.tag_name))"
    }
    return $asset.browser_download_url
}

# Variáveis de rastreamento
$script:installStatus = @{}
$script:errors = @()
$script:warnings = @()
$script:envVariables = @{}

Write-Host "=== Configuração de Ferramentas para Harness Bibliográfico ===" -ForegroundColor Cyan
Write-Host "Data/Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Gray
Write-Host "Plataforma: $([System.Environment]::OSVersion.VersionString)" -ForegroundColor Gray

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

# Função para registrar status
function Set-InstallStatus {
    param(
        [string]$Tool,
        [string]$Status,  # "Success", "Failed", "Skipped", "Warning"
        [string]$Message
    )
    $script:installStatus[$Tool] = @{
        Status = $Status
        Message = $Message
        Time = Get-Date
    }
}

# Função para adicionar erro
function Add-Error {
    param(
        [string]$Tool,
        [string]$ErrorMessage
    )
    $script:errors += @{
        Tool = $Tool
        Message = $ErrorMessage
        Time = Get-Date
    }
}

# Função para adicionar aviso
function Add-Warning {
    param(
        [string]$Tool,
        [string]$WarningMessage
    )
    $script:warnings += @{
        Tool = $Tool
        Message = $WarningMessage
        Time = Get-Date
    }
}

# Função para registrar variável de ambiente
function Register-EnvVariable {
    param(
        [string]$Name,
        [string]$Value
    )
    $script:envVariables[$Name] = $Value
}

# ==================== ZOTERO ====================
if (-not $SkipZotero) {
    Write-Host "`n[1/4] Instalando Zotero 7+" -ForegroundColor Yellow
    
    try {
        $zoteroUrl = 'https://www.zotero.org/download/client/dl?channel=release&platform=win32'
        $zoteroPath = "$env:TEMP\Zotero-Setup.exe"
        
        Register-EnvVariable "TEMP" "$env:TEMP"
        Register-EnvVariable "ProgramFiles" "$env:ProgramFiles"
        
        Write-Host "Baixando Zotero..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $zoteroUrl -OutFile $zoteroPath -UseBasicParsing -ErrorAction Stop
        
        if (Test-Path $zoteroPath) {
            Write-Host "Instalando Zotero..." -ForegroundColor Cyan
            Start-Process -FilePath $zoteroPath -ArgumentList "/S" -Wait
            
            Write-Host "✓ Zotero instalado com sucesso!" -ForegroundColor Green
            Set-InstallStatus "Zotero" "Success" "Zotero 7+ instalado corretamente"
            Remove-Item $zoteroPath -Force -ErrorAction SilentlyContinue
        } else {
            Add-Error "Zotero" "Arquivo de instalação não foi baixado"
            Write-Host "✗ Erro: Arquivo não foi salvo em $zoteroPath" -ForegroundColor Red
            Set-InstallStatus "Zotero" "Failed" "Arquivo de download não foi criado"
        }
    } catch {
        Add-Error "Zotero" "$($_.Exception.Message)"
        Write-Host "✗ Erro ao instalar Zotero: $($_.Exception.Message)" -ForegroundColor Red
        Set-InstallStatus "Zotero" "Failed" "Erro: $($_.Exception.Message)"
    }
} else {
    Write-Host "`n[1/4] Zotero - PULADO" -ForegroundColor Gray
    Set-InstallStatus "Zotero" "Skipped" "Instalação pulada por opção do usuário"
}

# ==================== DOCLING ====================
if (-not $SkipDocling) {
    Write-Host "`n[2/4] Instalando Docling (IBM)" -ForegroundColor Yellow
    
    try {
        # Verificar se pip está disponível
        if (Test-Command "pip") {
            Register-EnvVariable "PythonHome" "$([System.Environment]::GetEnvironmentVariable('PYTHONHOME', 'User'))"
            Register-EnvVariable "PATH_Contains_Python" (Get-Command "python" -ErrorAction SilentlyContinue)
            
            Write-Host "Atualizando pip..." -ForegroundColor Cyan
            python -m pip install --upgrade pip 2>&1 | Out-Null
            
            Write-Host "Instalando Docling..." -ForegroundColor Cyan
            pip install docling 2>&1 | Out-Null
            
            Write-Host "✓ Docling instalado com sucesso!" -ForegroundColor Green
            Set-InstallStatus "Docling" "Success" "Docling instalado via pip"
        } else {
            Add-Error "Docling" "Python/pip não encontrado no PATH"
            Write-Host "✗ Python/pip não encontrado. Instale Python 3.8+ antes de continuar." -ForegroundColor Red
            Write-Host "   Baixe em: https://www.python.org/downloads/" -ForegroundColor Gray
            Write-Host "   IMPORTANTE: Marque 'Add Python to PATH' durante instalação" -ForegroundColor Yellow
            Set-InstallStatus "Docling" "Failed" "Python/pip não encontrado"
        }
    } catch {
        Add-Error "Docling" "$($_.Exception.Message)"
        Write-Host "✗ Erro ao instalar Docling: $($_.Exception.Message)" -ForegroundColor Red
        Set-InstallStatus "Docling" "Failed" "Erro: $($_.Exception.Message)"
    }
} else {
    Write-Host "`n[2/4] Docling - PULADO" -ForegroundColor Gray
    Set-InstallStatus "Docling" "Skipped" "Instalação pulada por opção do usuário"
}

# ==================== OBSIDIAN ====================
if (-not $SkipObsidian) {
    Write-Host "`n[3/4] Instalando Obsidian" -ForegroundColor Yellow
    
    try {
        Write-Host "Consultando última versão do Obsidian..." -ForegroundColor Cyan
        $obsidianUrl = Get-LatestGitHubAssetUrl -Repo "obsidianmd/obsidian-releases" -NamePattern '^Obsidian-.*\.exe$'
        $obsidianPath = "$env:TEMP\Obsidian-Installer.exe"
        
        Write-Host "Baixando Obsidian..." -ForegroundColor Cyan
        Write-Host "URL: $obsidianUrl" -ForegroundColor Gray
        Invoke-WebRequest -Uri $obsidianUrl -OutFile $obsidianPath -UseBasicParsing -ErrorAction Stop
        
        if (Test-Path $obsidianPath) {
            Write-Host "Instalando Obsidian..." -ForegroundColor Cyan
            Start-Process -FilePath $obsidianPath -Wait
            
            Write-Host "✓ Obsidian instalado com sucesso!" -ForegroundColor Green
            Set-InstallStatus "Obsidian" "Success" "Obsidian instalado corretamente"
            Remove-Item $obsidianPath -Force -ErrorAction SilentlyContinue
        } else {
            Add-Error "Obsidian" "Arquivo de instalação não foi baixado"
            Write-Host "✗ Erro: Arquivo não foi salvo" -ForegroundColor Red
            Set-InstallStatus "Obsidian" "Failed" "Arquivo de download não foi criado"
        }
    } catch {
        Add-Error "Obsidian" "$($_.Exception.Message)"
        Write-Host "✗ Erro ao instalar Obsidian: $($_.Exception.Message)" -ForegroundColor Red
        Set-InstallStatus "Obsidian" "Failed" "Erro: $($_.Exception.Message)"
    }
} else {
    Write-Host "`n[3/4] Obsidian - PULADO" -ForegroundColor Gray
    Set-InstallStatus "Obsidian" "Skipped" "Instalação pulada por opção do usuário"
}

# ==================== OBSIDIAN LOCAL REST API PLUGIN ====================
if (-not $SkipPlugin) {
    Write-Host "`n[4/4] Configurando Obsidian Local REST API Plugin" -ForegroundColor Yellow
    
    try {
        # Localizar pasta de plugins do Obsidian
        $obsidianVault = "$env:APPDATA\Obsidian\plugins"
        
        Register-EnvVariable "APPDATA" "$env:APPDATA"
        Register-EnvVariable "OBSIDIAN_PLUGINS_DIR" "$obsidianVault"
        
        # Aguardar o Obsidian ser aberto (se não estiver)
        Write-Host "Aguardando Obsidian inicializar (5 segundos)..." -ForegroundColor Cyan
        Start-Sleep -Seconds 5
        
        # Criar diretório de plugins se não existir
        New-FolderIfNotExists $obsidianVault
        
        $pluginDir = "$obsidianVault\obsidian-local-rest-api"
        
        Write-Host "Consultando última versão do plugin..." -ForegroundColor Cyan
        
        # A release atual publica os arquivos do plugin soltos (main.js, manifest.json,
        # styles.css), sem um .zip. Baixamos cada arquivo diretamente.
        $headers = @{ "User-Agent" = "tcc-harness-setup-script" }
        $release = Invoke-RestMethod -Uri "https://api.github.com/repos/coddingtonbear/obsidian-local-rest-api/releases/latest" -Headers $headers -UseBasicParsing
        $requiredFiles = @("main.js", "manifest.json", "styles.css")
        
        New-FolderIfNotExists $pluginDir
        $downloaded = @()
        foreach ($fileName in $requiredFiles) {
            $asset = $release.assets | Where-Object { $_.name -eq $fileName } | Select-Object -First 1
            if ($asset) {
                Write-Host "Baixando $fileName..." -ForegroundColor Cyan
                Invoke-WebRequest -Uri $asset.browser_download_url -OutFile "$pluginDir\$fileName" -UseBasicParsing -ErrorAction Stop
                $downloaded += $fileName
            } elseif ($fileName -ne "styles.css") {
                # styles.css é opcional em algumas versões do plugin
                throw "Asset '$fileName' não encontrado na release $($release.tag_name)"
            }
        }
        
        if ($downloaded -contains "main.js" -and $downloaded -contains "manifest.json") {
            Write-Host "✓ Obsidian Local REST API Plugin configurado!" -ForegroundColor Green
            Write-Host "  Local: $pluginDir" -ForegroundColor Gray
            Write-Host "  Próximas etapas:" -ForegroundColor Gray
            Write-Host "  1. Abra Obsidian" -ForegroundColor Gray
            Write-Host "  2. Vá para Configurações > Plugins Instalados" -ForegroundColor Gray
            Write-Host "  3. Ative 'Local REST API'" -ForegroundColor Gray
            
            Set-InstallStatus "Obsidian Local REST API Plugin" "Success" "Plugin baixado corretamente"
        } else {
            Add-Error "Obsidian Local REST API Plugin" "Arquivos do plugin não foram criados"
            Write-Host "✗ Erro: Arquivos essenciais do plugin não foram salvos" -ForegroundColor Red
            Set-InstallStatus "Obsidian Local REST API Plugin" "Failed" "Arquivos não foram baixados"
        }
    } catch {
        Add-Error "Obsidian Local REST API Plugin" "$($_.Exception.Message)"
        Write-Host "✗ Erro ao configurar plugin: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Instalação manual: https://github.com/coddingtonbear/obsidian-local-rest-api" -ForegroundColor Gray
        Set-InstallStatus "Obsidian Local REST API Plugin" "Failed" "Erro: $($_.Exception.Message)"
    }
} else {
    Write-Host "`n[4/4] Obsidian Local REST API Plugin - PULADO" -ForegroundColor Gray
    Set-InstallStatus "Obsidian Local REST API Plugin" "Skipped" "Instalação pulada por opção do usuário"
}

# ==================== RESUMO FINAL ====================
Write-Host "`n$('='*70)" -ForegroundColor Cyan
Write-Host "RESUMO FINAL DA INSTALAÇÃO" -ForegroundColor Cyan
Write-Host "$('='*70)" -ForegroundColor Cyan

Write-Host "`n[STATUS DOS COMPONENTES]" -ForegroundColor Yellow
Write-Host "$('-'*70)" -ForegroundColor Yellow

foreach ($component in @("Zotero", "Docling", "Obsidian", "Obsidian Local REST API Plugin")) {
    if ($script:installStatus.ContainsKey($component)) {
        $status = $script:installStatus[$component]
        
        switch ($status.Status) {
            "Success" {
                Write-Host "✓ $component - SUCESSO" -ForegroundColor Green
                Write-Host "  └─ $($status.Message)" -ForegroundColor Gray
            }
            "Failed" {
                Write-Host "✗ $component - FALHA" -ForegroundColor Red
                Write-Host "  └─ $($status.Message)" -ForegroundColor Gray
            }
            "Skipped" {
                Write-Host "⊘ $component - PULADO" -ForegroundColor Gray
                Write-Host "  └─ $($status.Message)" -ForegroundColor Gray
            }
            "Warning" {
                Write-Host "⚠ $component - AVISO" -ForegroundColor Yellow
                Write-Host "  └─ $($status.Message)" -ForegroundColor Gray
            }
        }
    }
}

# Contar resultados
$successCount = ($script:installStatus.Values | Where-Object { $_.Status -eq "Success" }).Count
$failureCount = ($script:installStatus.Values | Where-Object { $_.Status -eq "Failed" }).Count
$skippedCount = ($script:installStatus.Values | Where-Object { $_.Status -eq "Skipped" }).Count

Write-Host "`n[ESTATÍSTICAS]" -ForegroundColor Yellow
Write-Host "$('-'*70)" -ForegroundColor Yellow
Write-Host "✓ Sucessos: $successCount" -ForegroundColor Green
Write-Host "✗ Falhas: $failureCount" -ForegroundColor Red
Write-Host "⊘ Pulados: $skippedCount" -ForegroundColor Gray
Write-Host "Total de componentes: $($script:installStatus.Count)" -ForegroundColor Cyan

if ($script:errors.Count -gt 0) {
    Write-Host "`n[ERROS ENCONTRADOS]" -ForegroundColor Red
    Write-Host "$('-'*70)" -ForegroundColor Red
    
    foreach ($err in $script:errors) {
        Write-Host "[$($err.Tool)]" -ForegroundColor Red
        Write-Host "  └─ $($err.Message)" -ForegroundColor Gray
        Write-Host "  └─ Horário: $($err.Time.ToString('HH:mm:ss'))" -ForegroundColor Gray
    }
}

if ($script:warnings.Count -gt 0) {
    Write-Host "`n[AVISOS]" -ForegroundColor Yellow
    Write-Host "$('-'*70)" -ForegroundColor Yellow
    
    foreach ($warning in $script:warnings) {
        Write-Host "[$($warning.Tool)]" -ForegroundColor Yellow
        Write-Host "  └─ $($warning.Message)" -ForegroundColor Gray
    }
}

Write-Host "`n[VARIÁVEIS DE AMBIENTE DETECTADAS]" -ForegroundColor Cyan
Write-Host "$('-'*70)" -ForegroundColor Cyan

foreach ($envVar in $script:envVariables.GetEnumerator()) {
    Write-Host "$($envVar.Key):" -ForegroundColor Cyan
    if ($envVar.Value) {
        Write-Host "  └─ $($envVar.Value)" -ForegroundColor Gray
    } else {
        Write-Host "  └─ [NÃO ENCONTRADA]" -ForegroundColor Red
    }
}

# Variáveis de ambiente do sistema
Write-Host "`n[VARIÁVEIS DE SISTEMA IMPORTANTES]" -ForegroundColor Cyan
Write-Host "$('-'*70)" -ForegroundColor Cyan

$sysEnvVars = @("PATH", "PYTHON_HOME", "PYTHONHOME", "USERPROFILE", "APPDATA", "TEMP")
foreach ($var in $sysEnvVars) {
    $value = [System.Environment]::GetEnvironmentVariable($var, "User")
    if (-not $value) {
        $value = [System.Environment]::GetEnvironmentVariable($var, "Machine")
    }
    
    if ($value) {
        Write-Host "$var = $value" -ForegroundColor Gray
    } else {
        Write-Host "$var = [NÃO ENCONTRADA]" -ForegroundColor Yellow
    }
}

Write-Host "`n[O QUE NÃO FOI ENCONTRADO]" -ForegroundColor Red
Write-Host "$('-'*70)" -ForegroundColor Red

$notFound = @()

if ($failureCount -gt 0) {
    foreach ($err in $script:errors) {
        $notFound += "• $($err.Tool): $($err.Message)"
    }
}

if ($notFound.Count -gt 0) {
    foreach ($item in $notFound) {
        Write-Host $item -ForegroundColor Red
    }
} else {
    Write-Host "Nenhum erro crítico encontrado!" -ForegroundColor Green
}

Write-Host "`n[RECOMENDAÇÕES PARA RESOLVER PROBLEMAS]" -ForegroundColor Yellow
Write-Host "$('-'*70)" -ForegroundColor Yellow

if ($script:installStatus["Docling"].Status -eq "Failed") {
    Write-Host "❌ DOCLING NÃO INSTALADO" -ForegroundColor Red
    Write-Host "1. Instale Python 3.8+:" -ForegroundColor Cyan
    Write-Host "   https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "2. IMPORTANTE: Marque 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "3. Reinicie o PowerShell" -ForegroundColor Cyan
    Write-Host "4. Depois execute: pip install docling" -ForegroundColor Cyan
    Write-Host ""
}

if ($script:installStatus["Obsidian Local REST API Plugin"].Status -eq "Failed") {
    Write-Host "❌ PLUGIN LOCAL REST API NÃO INSTALADO" -ForegroundColor Red
    Write-Host "Opção 1 - Instalação Manual:" -ForegroundColor Cyan
    Write-Host "  1. Vá para: https://github.com/coddingtonbear/obsidian-local-rest-api/releases" -ForegroundColor Cyan
    Write-Host "  2. Baixe a versão mais recente (obsidian-local-rest-api.zip)" -ForegroundColor Cyan
    Write-Host "  3. Extraia para: %APPDATA%\Obsidian\plugins\obsidian-local-rest-api" -ForegroundColor Cyan
    Write-Host "  4. Reinicie Obsidian" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Opção 2 - Community Plugins:" -ForegroundColor Cyan
    Write-Host "  1. Abra Obsidian" -ForegroundColor Cyan
    Write-Host "  2. Configurações > Community Plugins > Desabilitar modo restrito" -ForegroundColor Cyan
    Write-Host "  3. Procure por 'Local REST API'" -ForegroundColor Cyan
    Write-Host "  4. Instale e ative" -ForegroundColor Cyan
    Write-Host ""
}

if ($script:installStatus["Zotero"].Status -eq "Failed") {
    Write-Host "❌ ZOTERO NÃO INSTALADO" -ForegroundColor Red
    Write-Host "Instale manualmente em: https://www.zotero.org/download/" -ForegroundColor Cyan
    Write-Host ""
}

if ($script:installStatus["Obsidian"].Status -eq "Failed") {
    Write-Host "❌ OBSIDIAN NÃO INSTALADO" -ForegroundColor Red
    Write-Host "Instale manualmente em: https://obsidian.md/download" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "`n[PRÓXIMAS ETAPAS]" -ForegroundColor Yellow
Write-Host "$('-'*70)" -ForegroundColor Yellow

if ($successCount -eq 4) {
    Write-Host "✓ Todas as ferramentas foram instaladas com sucesso!" -ForegroundColor Green
    Write-Host "Próximas etapas:" -ForegroundColor Yellow
    Write-Host "1. Abra Zotero e configure sua biblioteca" -ForegroundColor Gray
    Write-Host "2. Configure Obsidian com seu vault pessoal" -ForegroundColor Gray
    Write-Host "3. Ative o plugin Local REST API em Obsidian" -ForegroundColor Gray
    Write-Host "4. Teste a integração entre as ferramentas" -ForegroundColor Gray
} else {
    Write-Host "Resolva os problemas acima e execute o script novamente" -ForegroundColor Yellow
    Write-Host "Você pode pular componentes já instalados com as flags -Skip*" -ForegroundColor Gray
}

Write-Host "`n[DOCUMENTAÇÃO E SUPORTE]" -ForegroundColor Yellow
Write-Host "$('-'*70)" -ForegroundColor Yellow
Write-Host "• Zotero: https://www.zotero.org/support/" -ForegroundColor Gray
Write-Host "• Docling: https://github.com/IBM-Research/docling" -ForegroundColor Gray
Write-Host "• Obsidian: https://help.obsidian.md/" -ForegroundColor Gray
Write-Host "• Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api" -ForegroundColor Gray
Write-Host "• Verificação: python verify-installation.py" -ForegroundColor Cyan

Write-Host "`n$('='*70)" -ForegroundColor Cyan
Write-Host "FIM DA INSTALAÇÃO - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "$('='*70)`n" -ForegroundColor Cyan
