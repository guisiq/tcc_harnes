# RevisorArtigoTcc — Harness .NET com GitHub Copilot SDK

Harness em C# (.NET 9 + `GitHub.Copilot.SDK`) para revisão técnica parágrafo por parágrafo do artigo de TCC contra três referenciais:

1. **Diagrama de Revisão do Texto / Cuidados Finais** (*Vieira, 2011; Wazlawick*)
2. **Acervo `artigos/05-metodologia-e-escrita-cientifica/`** (*Wazlawick UFOP/UFU, Zucolotto Módulos 1–8, Gerhardt & Silveira 2009, Prodanov & Freitas 2013*)
3. **Checklist do TCC 1** (`Formulario-Checklist_para_o_texto_do_TCC1.pdf`)

## Modelo

Não existe um modelo chamado `GPTLua` no catálogo do GitHub Copilot SDK disponível nesta máquina. A integração visual usa o modelo econômico com visão `mai-code-2-flash` por padrão; o parâmetro `-VisualModel "mai-code-2"` permite trocar para o modelo principal da mesma família.

## Otimização de Contexto e Custo

- **Modelo padrão econômico (50% off):** `mai-code-2-flash` (também compatível com `mai-code-2` via `-Model "mai-code-2"`).
- **Pré-auditoria determinística (0 tokens):** extrai os 248 itens lógicos do PDF reconstruindo parágrafos quebrados entre linhas/páginas, expressões matemáticas inline (`$M_{t-1}^*$`), cruzando 100% das citações × referências e validando figuras/quadros/tabelas, pontuação, marcadores residuais do Word (`[GS1]`–`[GS4]`), alíneas quebradas (`c)a)`, `g) 7.`), frases truncadas e extensão de períodos.
- **Rubrica compacta + sessões sem ferramentas (`AvailableTools = []`):** elimina o custo de esquemas de ferramentas por chamada e agrupa os parágrafos em lotes de 10 itens (~16 requisições no total), com cache SHA-256 em `.revisor-cache/`.

## Uso

A partir da raiz do repositório:

```powershell
# Execução padrão com mai-code-2-flash
.\ferramentas\revisar-artigo-tcc.ps1

# Usando mai-code-2
.\ferramentas\revisar-artigo-tcc.ps1 -Model "mai-code-2"

# Apenas auditoria determinística (instantânea, sem chamadas ao LLM)
.\ferramentas\revisar-artigo-tcc.ps1 -DeterministicOnly

# Auditoria textual + cópia DOCX comentada + auditoria visual das páginas
.\ferramentas\revisar-artigo-tcc.ps1 `
  -Model "mai-code-2-flash" `
  -VisualModel "mai-code-2-flash" `
  -VisualDpi 150 `
  -VisualBatchSize 10 `
  -CommentAuthor "Nome do autor" `
  -CommentInitials "NA"
```

Os comentários usam o autor `Copilot — Revisão do TCC` e as iniciais `CP` por padrão. Use
`--comment-author` e `--comment-initials` para atribuí-los a outro autor.

## Saídas Geradas

- `TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\observacoes_artigo_tcc.md`: relatório completo com estatísticas, avaliação dos 16 itens do Checklist do TCC1, matriz do Diagrama de Revisão, matriz de Metodologia Científica, cruzamento de citações × referências e tabela parágrafo por parágrafo (`#001` a `#248`).
- `TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\observacoes_artigo_tcc.json`: dados estruturados item por item.
- `TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\artigo_tcc_unitins_corrigido (1)_comentado.docx`: cópia do DOCX original com comentários críticos anexados aos trechos correspondentes e comentários anteriores preservados.
- `TCC_Checkpoint_JSON_Obsidian\07_Artigo_TCC\observacoes_visuais_artigo_tcc.md` e `.json`: auditoria visual de todas as páginas, usando o modelo com visão configurado.
