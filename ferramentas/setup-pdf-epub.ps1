$ErrorActionPreference = 'Stop'
$tools = Join-Path $PSScriptRoot '.tools'
$project = Join-Path $PSScriptRoot 'PdfParaEpubBilingue'
$dotnet = Join-Path $env:ProgramFiles 'dotnet\dotnet.exe'
if (-not (Test-Path $dotnet)) { $dotnet = (Get-Command dotnet -ErrorAction Stop).Source }
$python = (Get-Command python -ErrorAction Stop).Source
& java -version
if ($LASTEXITCODE -ne 0) { throw 'Java e necessario para EPUBCheck.' }
New-Item -ItemType Directory -Force -Path $tools | Out-Null
$environment = Join-Path $tools 'python'
& $python -m venv $environment
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente Python.' }
$localPython = Join-Path $environment 'Scripts\python.exe'
& $localPython -m pip install -r (Join-Path $project 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar PyMuPDF.' }
$jar = Join-Path $tools 'epubcheck-5.3.0\epubcheck.jar'
if (-not (Test-Path $jar)) {
    $download = Join-Path $tools 'epubcheck-5.3.0.zip'
    Invoke-WebRequest 'https://github.com/w3c/epubcheck/releases/download/v5.3.0/epubcheck-5.3.0.zip' -OutFile $download
    Expand-Archive -Path $download -DestinationPath $tools -Force
}
& java -jar $jar --version
if ($LASTEXITCODE -ne 0) { throw 'EPUBCheck nao iniciou.' }
$publish = Join-Path $tools 'pdf-epub'
& $dotnet publish $project -c Release -r win-x64 --self-contained false -o $publish
if ($LASTEXITCODE -ne 0) { throw 'Falha ao publicar a CLI.' }
& (Join-Path $publish 'PdfParaEpubBilingue.exe') --install-browser
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar Chromium.' }
Write-Host 'Pronto. Execute ferramentas/pdf-epub.ps1 --help. A traducao requer autenticacao Copilot e pode consumir cota.'
Write-Host 'AZW3/MOBI/PDF requerem Calibre: https://calibre-ebook.com/download_portable'
Write-Host 'Use EBOOK_CONVERT ou --calibre para indicar ebook-convert.exe. EPUB nao requer Calibre.'