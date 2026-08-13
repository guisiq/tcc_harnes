# 🚀 Guia de Início Rápido - Harness Bibliográfico

## Instalação Rápida (5 minutos)

### Opção 1: PowerShell (Recomendado)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-tools.ps1
```

### Opção 2: Command Prompt
```cmd
setup-tools.bat
```

### Opção 3: Instalação Manual
Veja **SETUP_README.md** para instruções detalhadas

---

## ✅ Verificar Instalação

```powershell
python verify-installation.py
```

Isso verifica se todas as ferramentas foram instaladas corretamente.

---

## 📦 O Que Será Instalado

| Ferramenta | Versão | Propósito |
|-----------|--------|----------|
| **Zotero** | 7+ | Gerenciar referências bibliográficas |
| **Docling** | Latest | Converter/processar PDFs |
| **Obsidian** | Latest | Aplicativo de notas |
| **REST API Plugin** | Latest | Acesso via HTTP ao Obsidian |

---

## 🎯 Próximas Etapas

### 1️⃣ Configurar Zotero
```
1. Abra Zotero
2. Crie uma conta em https://www.zotero.org
3. Configure sincronização automática
4. Crie grupos por tema de pesquisa
```

### 2️⃣ Configurar Obsidian
```
1. Abra Obsidian
2. Crie um novo vault chamado "Pesquisa"
3. Vá para Configurações > Plugins Instalados
4. Ative "Local REST API"
```

### 3️⃣ Testar Integração
```powershell
# Testar API do Obsidian
curl http://localhost:27124/

# Testar Docling
docling seu-arquivo.pdf
```

---

## 🔗 Integrações Opcionais

### Zotero + Obsidian
Instale o plugin **Zotero Integration**:
- Em Obsidian: Community Plugins > "Zotero Integration"
- Configure a pasta de dados do Zotero
- Use `@cite` em suas notas para adicionar referências

### Docling + Obsidian
Use Docling para extrair texto de PDFs:
```powershell
docling seu-arquivo.pdf --output-dir ./exports
```

---

## 📚 Recursos Importantes

### Documentação Oficial
- 🔗 [Zotero Help](https://www.zotero.org/support/)
- 🔗 [Docling GitHub](https://github.com/IBM-Research/docling)
- 🔗 [Obsidian Help](https://help.obsidian.md/)
- 🔗 [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)

### Tutoriais
- [Como usar Zotero para pesquisa](https://www.zotero.org/support/getting_stuff_into_your_library)
- [Obsidian para escritores acadêmicos](https://obsidian.md/)
- [Docling para PDFs complexos](https://github.com/IBM-Research/docling/blob/main/README.md)

### Comunidades
- Zotero: https://forums.zotero.org/
- Obsidian: https://discord.gg/obsidianmd
- Docling: https://github.com/IBM-Research/docling/discussions

---

## 🐛 Problemas Comuns

### ❌ Script não executa
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Python não encontrado
1. Instale Python 3.8+: https://www.python.org/downloads/
2. **Importante**: Marque "Add Python to PATH"
3. Reinicie o terminal

### ❌ Plugin não aparece em Obsidian
1. Feche o Obsidian completamente
2. Verifique: `%APPDATA%\Obsidian\plugins\obsidian-local-rest-api`
3. Se não existir, execute novamente: `.\setup-tools.ps1 -SkipZotero -SkipDocling -SkipObsidian`
4. Reabra o Obsidian

### ❌ Erro de permissão (Access Denied)
- Execute o PowerShell como **Administrador**
- Ou use `setup-tools.bat` como administrador

---

## 💡 Dicas

✨ **Dica 1**: Use templates no Obsidian para notas de pesquisa
```markdown
---
tags: pesquisa, bibliográfico
zotero-key: ABC123
source: Zotero
---

# Título do Artigo

## Resumo
[Resumir artigo aqui]

## Citação
@cite

## Notas Pessoais
[Suas anotações]
```

✨ **Dica 2**: Crie um workflow de importação
1. Adicione PDF ao Zotero
2. Use Local REST API para sincronizar
3. Processe com Docling
4. Anote no Obsidian

✨ **Dica 3**: Automação com Python
```python
import requests

# Consultar API Local do Obsidian
response = requests.get('http://localhost:27124/')
print(response.json())
```

---

## 📋 Checklist de Configuração

- [ ] PowerShell/CMD com permissões de Admin
- [ ] Python 3.8+ instalado com PATH configurado
- [ ] Zotero 7+ instalado e funcionando
- [ ] Docling instalado (`pip install docling`)
- [ ] Obsidian instalado e vault criado
- [ ] Local REST API plugin ativado em Obsidian
- [ ] Verificação de instalação passou (`python verify-installation.py`)
- [ ] Zotero account sincronizado (opcional)
- [ ] Plugin Zotero Integration instalado (opcional)

---

## 🆘 Suporte

Caso encontre problemas:

1. Execute o verificador: `python verify-installation.py`
2. Consulte **SETUP_README.md** para troubleshooting
3. Verifique a documentação oficial das ferramentas
4. Abra uma issue no repositório do projeto

---

**Status**: Pronto para começar! 🎉

Para instruções mais detalhadas, veja [SETUP_README.md](SETUP_README.md)
