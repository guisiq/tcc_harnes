# Script de Configuração - Harness Bibliográfico

Script PowerShell para automatizar a instalação e configuração das ferramentas necessárias para o mini harness bibliográfico.

## 📋 Ferramentas Instaladas

- **Zotero 7+** - Gerenciador de referências bibliográficas
- **Docling (IBM)** - Conversor de PDFs e documentos
- **Obsidian** - Aplicativo de notas baseado em arquivos
- **Obsidian Local REST API** - Plugin para acesso via API REST

## 🚀 Como Usar

### Opção 1: Instalação Completa (Recomendado)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-tools.ps1
```

### Opção 2: Instalação Seletiva

Pule componentes específicos usando flags:

```powershell
# Instala tudo exceto Zotero
.\setup-tools.ps1 -SkipZotero

# Instala apenas Obsidian e seu plugin
.\setup-tools.ps1 -SkipZotero -SkipDocling

# Instala tudo exceto o plugin
.\setup-tools.ps1 -SkipPlugin
```

## ✅ Pré-requisitos

- **Windows 10+**
- **PowerShell 5.0+** (executar como Administrator)
- **Python 3.8+** (para Docling)
  - Baixe em: https://www.python.org/downloads/
  - Marque "Add Python to PATH" durante instalação

## 📝 Após a Instalação

### 1. Zotero
- Abra o Zotero
- Configure sua biblioteca pessoal
- Configure sincronização (opcional)

### 2. Docling
- Teste a instalação:
  ```powershell
  python -c "import docling; print(docling.__version__)"
  ```
- Documentação: https://github.com/IBM-Research/docling

### 3. Obsidian
- Crie seu vault pessoal
- Abra as configurações

### 4. Local REST API Plugin
- Vá para **Configurações > Plugins Instalados**
- Procure por "Local REST API"
- Ative o plugin
- Configure conforme necessário (porta padrão: 27124)

## 🔗 Integrações Recomendadas

### Zotero + Obsidian
- Instale o plugin **Zotero Integration** no Obsidian
- Configure a conexão com Zotero

### Docling + Obsidian
- Use Docling para converter PDFs
- Importe os documentos convertidos no Obsidian

### Local REST API
- Documente sua API em: `http://localhost:27124`
- Use para automações e scripts externos

## 🐛 Troubleshooting

### Erro de Execução de Script
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python/Docling não encontrado
```powershell
# Reinstale Python e adicione ao PATH
pip install --upgrade pip
pip install docling
```

### Plugin não aparece no Obsidian
1. Feche completamente o Obsidian
2. Verifique a pasta: `%APPDATA%\Obsidian\plugins\obsidian-local-rest-api`
3. Reabra o Obsidian
4. Vá para Configurações > Plugins Instalados

## 📚 Documentação Oficial

- Zotero: https://www.zotero.org/support/
- Docling: https://github.com/IBM-Research/docling
- Obsidian: https://help.obsidian.md/
- Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api

## 💡 Dicas

- Execute o script como Administrator para evitar problemas de permissão
- Tenha conexão com internet estável durante a instalação
- Alguns antivírus podem bloquear downloads - adicione exceções se necessário

---

**Última atualização:** 2026-08-13
