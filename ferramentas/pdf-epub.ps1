$ErrorActionPreference = 'Stop'
$executable = Join-Path $PSScriptRoot '.tools\pdf-epub\PdfParaEpubBilingue.exe'
if (-not (Test-Path $executable)) {
    throw 'Execute ferramentas/setup-pdf-epub.ps1 antes de usar esta ferramenta.'
}
$previousJar = $env:EPUBCHECK_JAR
$previousPython = $env:PDF_EPUB_PYTHON
$previousConverter = $env:EBOOK_CONVERT
try {
    if (-not $env:EBOOK_CONVERT) {
        $portableConverter = Join-Path $PSScriptRoot '.tools\calibre-portable\Calibre\ebook-convert.exe'
        if (Test-Path $portableConverter) { $env:EBOOK_CONVERT = $portableConverter }
    }
    if (-not $env:EPUBCHECK_JAR) {
        $env:EPUBCHECK_JAR = Join-Path $PSScriptRoot '.tools\epubcheck-5.3.0\epubcheck.jar'
    }
    if (-not $env:PDF_EPUB_PYTHON) {
        $localPython = Join-Path $PSScriptRoot '.tools\python\Scripts\python.exe'
        if (Test-Path $localPython) { $env:PDF_EPUB_PYTHON = $localPython }
    }
    & $executable @args
    $result = $LASTEXITCODE
}
finally {
    $env:EPUBCHECK_JAR = $previousJar
    $env:PDF_EPUB_PYTHON = $previousPython
    $env:EBOOK_CONVERT = $previousConverter
}
exit $result