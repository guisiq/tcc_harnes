@echo off
REM Script batch para configurar ferramentas - Harness Bibliográfico
REM Alternativa ao PowerShell para usuários que preferem cmd

setlocal enabledelayedexpansion

title Configuracao - Harness Bibliografico
color 0B

echo.
echo ==========================================
echo Configuracao de Ferramentas
echo Harness Bibliografico
echo ==========================================
echo.

REM Verificar se está rodando como Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERRO] Este script requer privilegios de Administrator!
    echo Clique com botao direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

REM ==================== ZOTERO ====================
echo [1/4] Baixando e instalando Zotero 7+...
echo.

if exist "%TEMP%\Zotero-Setup.exe" del "%TEMP%\Zotero-Setup.exe"

echo Baixando Zotero...
powershell -Command "Invoke-WebRequest -Uri 'https://www.zotero.org/download/client/dl?channel=release&platform=win32' -OutFile '%TEMP%\Zotero-Setup.exe' -UseBasicParsing"

if exist "%TEMP%\Zotero-Setup.exe" (
    echo Instalando Zotero...
    "%TEMP%\Zotero-Setup.exe" /S
    echo [OK] Zotero instalado com sucesso!
    del "%TEMP%\Zotero-Setup.exe"
) else (
    echo [ERRO] Nao foi possivel baixar Zotero
)

echo.

REM ==================== DOCLING ====================
echo [2/4] Instalando Docling (IBM)...
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorLevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Baixe Python 3.8+ em: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH"
) else (
    echo Instalando Docling via pip...
    python -m pip install --upgrade pip
    pip install docling
    echo [OK] Docling instalado com sucesso!
)

echo.

REM ==================== OBSIDIAN ====================
echo [3/4] Baixando e instalando Obsidian...
echo.

if exist "%TEMP%\Obsidian-Installer.exe" del "%TEMP%\Obsidian-Installer.exe"

echo Baixando Obsidian...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/obsidianmd/obsidian-releases/releases/download/latest/Obsidian.exe' -OutFile '%TEMP%\Obsidian-Installer.exe' -UseBasicParsing"

if exist "%TEMP%\Obsidian-Installer.exe" (
    echo Instalando Obsidian...
    "%TEMP%\Obsidian-Installer.exe"
    echo [OK] Obsidian instalado com sucesso!
    del "%TEMP%\Obsidian-Installer.exe"
) else (
    echo [ERRO] Nao foi possivel baixar Obsidian
)

echo.

REM ==================== OBSIDIAN PLUGIN ====================
echo [4/4] Configurando Obsidian Local REST API Plugin...
echo.

set PLUGIN_DIR=%APPDATA%\Obsidian\plugins\obsidian-local-rest-api

if not exist "%PLUGIN_DIR%" mkdir "%PLUGIN_DIR%"

if exist "%TEMP%\obsidian-local-rest-api.zip" del "%TEMP%\obsidian-local-rest-api.zip"

echo Baixando plugin...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/coddingtonbear/obsidian-local-rest-api/releases/latest/download/obsidian-local-rest-api.zip' -OutFile '%TEMP%\obsidian-local-rest-api.zip' -UseBasicParsing"

if exist "%TEMP%\obsidian-local-rest-api.zip" (
    echo Extraindo plugin...
    powershell -Command "Expand-Archive -Path '%TEMP%\obsidian-local-rest-api.zip' -DestinationPath '%PLUGIN_DIR%' -Force"
    echo [OK] Plugin configurado com sucesso!
    echo.
    echo Plugin instalado em: %PLUGIN_DIR%
    echo.
    echo Proximas etapas:
    echo 1. Abra Obsidian
    echo 2. Va para Configuracoes ^> Plugins Instalados
    echo 3. Ative "Local REST API"
    del "%TEMP%\obsidian-local-rest-api.zip"
) else (
    echo [ERRO] Nao foi possivel baixar o plugin
    echo Instalacao manual: https://github.com/coddingtonbear/obsidian-local-rest-api
)

echo.
echo ==========================================
echo Configuracao Completa!
echo ==========================================
echo.
echo Documentacao:
echo - Zotero: https://www.zotero.org/support/
echo - Docling: https://github.com/IBM-Research/docling
echo - Obsidian: https://help.obsidian.md/
echo - Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api
echo.

pause
