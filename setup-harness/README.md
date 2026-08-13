# 📁 Setup Harness - Ferramentas de Configuração

Esta pasta contém todos os scripts e documentação necessária para configurar as ferramentas do mini harness bibliográfico.

## 📋 Estrutura da Pasta

```
setup-harness/
├── README.md                    # Este arquivo
├── QUICKSTART.md               # Guia rápido de início (👈 COMECE AQUI!)
├── SETUP_README.md             # Documentação completa
├── setup-tools.ps1             # Script PowerShell (Recomendado)
├── setup-tools.bat             # Script CMD (Alternativa)
├── setup-config.json           # Arquivo de configuração
└── verify-installation.py      # Script de verificação
```

---

## 🚀 Como Começar (3 Passos)

### 1️⃣ Abra a Pasta
```powershell
cd setup-harness
```

### 2️⃣ Escolha seu método de instalação

**Opção A - PowerShell (Recomendado)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-tools.ps1
```

**Opção B - Command Prompt**
```cmd
setup-tools.bat
```

### 3️⃣ Verifique a Instalação
```powershell
python verify-installation.py
```

---

## 📚 Arquivos Disponíveis

### 🔵 Scripts de Instalação

| Arquivo | Descrição | Usar Quando |
|---------|-----------|-----------|
| **setup-tools.ps1** | Script PowerShell completo com rastreamento detalhado | Windows com PowerShell, quer mais controle |
| **setup-tools.bat** | Script Batch simples | Windows CMD, preferir simplicidade |

### 📖 Documentação

| Arquivo | Descrição | Ler Quando |
|---------|-----------|-----------|
| **QUICKSTART.md** | Guia de 5 minutos | Primeira vez, quer começar rápido |
| **SETUP_README.md** | Guia completo com troubleshooting | Precisa de detalhes, tem problemas |

### ⚙️ Configuração

| Arquivo | Descrição |
|---------|-----------|
| **setup-config.json** | Configurações centralizadas (URLs, caminhos, etc) |
| **verify-installation.py** | Verifica se tudo foi instalado corretamente |

---

## 🎯 Próximas Etapas

1. **Leia** [QUICKSTART.md](QUICKSTART.md) (5 min)
2. **Execute** um dos scripts de instalação
3. **Verifique** com `python verify-installation.py`
4. **Configure** cada ferramenta conforme as instruções

---

## ⚡ Resumo Rápido

### O que será instalado?

- ✅ **Zotero 7+** - Gerenciador de referências (gratuito)
- ✅ **Docling** - Conversor de PDFs (gratuito)
- ✅ **Obsidian** - Aplicativo de notas (gratuito)
- ✅ **Local REST API Plugin** - Acesso via HTTP (gratuito)

### Requisitos Mínimos

- Windows 10+
- PowerShell 5.0+ ou CMD
- Conexão com internet
- Python 3.8+ (para Docling)

### Tempo Estimado

- Instalação: 10-15 minutos
- Configuração: 5-10 minutos

---

## 🐛 Problemas Rápidos?

Veja [SETUP_README.md](SETUP_README.md) - Seção "Troubleshooting"

Ou execute o verificador:
```powershell
python verify-installation.py
```

---

## 📞 Suporte

1. **Primeiro**, leia [QUICKSTART.md](QUICKSTART.md)
2. **Depois**, consulte [SETUP_README.md](SETUP_README.md)
3. **Depois**, verifique: `python verify-installation.py`
4. **Finalmente**, consulte documentação oficial das ferramentas

---

## 📦 Estrutura Recomendada do Projeto

```
tccHarnes/
├── setup-harness/               # 👈 Você está aqui
│   ├── setup-tools.ps1
│   ├── setup-tools.bat
│   ├── verify-installation.py
│   ├── setup-config.json
│   ├── QUICKSTART.md
│   ├── SETUP_README.md
│   └── README.md
├── artigos/
├── arquitetura_mini_harness_bibliografico.md
├── planejamento_mini_harness_completo.md
└── ... (outros arquivos)
```

---

## ✅ Checklist de Início

- [ ] Leu [QUICKSTART.md](QUICKSTART.md)
- [ ] Tem Python 3.8+ instalado
- [ ] Tem permissões de Admin no Windows
- [ ] Tem conexão com internet
- [ ] Executou o script de instalação
- [ ] Executou `python verify-installation.py`
- [ ] Todas as ferramentas mostram ✓

---

**Status**: Pronto para começar! 🎉

👉 **[Abra QUICKSTART.md](QUICKSTART.md) para começar em 5 minutos**

---

*Última atualização: 2026-08-13*
