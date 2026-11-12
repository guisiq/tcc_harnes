# Gerar o DOCX do artigo

O comando abaixo lê a versão salva de
[`artigo_tcc_unitins.md`](../TCC_Checkpoint_JSON_Obsidian/07_Artigo_TCC/artigo_tcc_unitins.md),
usa o [cabeçalho oficial](../anexos/Recursos/Cabeçalho%20oficial%202025.docx)
e cria outro arquivo DOCX na mesma pasta, com data e hora no nome:

```powershell
pwsh -NoLogo -NoProfile -File .\ferramentas\gerar-artigo-unitins.ps1
```

Execute o comando na raiz do repositório, após salvar as alterações no Markdown.
Para escolher outro destino:

```powershell
pwsh -NoLogo -NoProfile -File .\ferramentas\gerar-artigo-unitins.ps1 `
    -Saida 'D:\caminho\artigo-formatado.docx'
```

O destino não é sobrescrito por padrão. Para substituí-lo intencionalmente,
acrescente `-Force`. Um erro de geração ou validação não substitui o arquivo
existente. Os parâmetros `-Entrada`, `-Cabecalho` e `-Config` permitem escolher
outros arquivos de entrada.

## Pré-requisitos

- Windows com Microsoft Word para área de trabalho e PowerShell 7 (`pwsh`).
  O Word é usado para numerar páginas e verificar sumário e legendas.
- Python 3.9 ou posterior e `python-docx`:

  ```powershell
  python -m pip install -r .\ferramentas\requirements-artigo-unitins.txt
  ```

- Pandoc com suporte a filtros Lua e citeproc. A geração foi testada com a
  versão 3.6.3. O script procura primeiro
  `ferramentas\.tools\pandoc\pandoc.exe`, depois o executável no `PATH`.
- O estilo CSL da Associação Brasileira de Normas Técnicas em
  `ferramentas\.tools\pandoc\associacao-brasileira-de-normas-tecnicas.csl`
  ou `Zotero\styles\associacao-brasileira-de-normas-tecnicas.csl`, dentro do
  perfil do usuário.
- Zotero aberto com a extensão Better BibTeX e as chaves de citação do
  Markdown presentes na biblioteca local. Os metadados são consultados no
  serviço local `127.0.0.1:23119`, não em um servidor externo.

Se necessário, informe `-Python`, `-Pandoc` ou `-Csl` com o caminho completo
do respectivo arquivo. A pasta `ferramentas\.tools` é ignorada pelo Git e
não acompanha o repositório.

Como alternativa explícita ao Zotero aberto, `-MapaZotero` aceita um arquivo
CSL JSON com `id` igual à chave de cada citação e `custom.itemID` e
`custom.uri` correspondentes aos itens da biblioteca. Por exemplo, se o mapa
local anterior ainda existir:

```powershell
pwsh -NoLogo -NoProfile -File .\ferramentas\gerar-artigo-unitins.ps1 `
    -MapaZotero .\ferramentas\.tools\pandoc\zotero_items.json
```

Esse mapa é um retrato dos dados, não uma consulta atualizada. Se faltar uma
chave ou identificação Zotero, a geração termina com erro.

## Manutenção do artigo e da configuração

- O título, o subtítulo, os dois autores e o ano vêm dos metadados do
  Markdown. Mantenha os autores na ordem acadêmico e orientador, e o início
  do corpo como `# 1 Introdução`.
- Mantenha `**Resumo:**`, `**Palavras-chave:**`, `**Title:**`, `**Abstract:**`
  e `**Keywords:**` em parágrafos identificados individualmente. O título em
  inglês é incluído na página do abstract.
- A lista de siglas e os dados institucionais ficam em
  [`artigo_unitins_config.json`](./artigo_unitins_config.json). Atualize-os
  quando o texto ou a identificação institucional mudar.
- O mesmo arquivo contém ajustes bibliográficos explícitos que foram usados
  na versão atual, inclusive os dados publicados do artigo de Hwang de 2024.
  Eles prevalecem sobre os campos correspondentes exportados do Zotero;
  revise ou remova os ajustes se corrigir os dados diretamente na biblioteca.
- A lista de quadros/tabelas e o sumário são derivados das legendas e dos
  títulos do corpo. O cronograma reconhece cabeçalho `Ativ.` e pares como
  `Ago Q1`, `Ago Q2`; as células `X` são representadas em azul. Se ele não
  couber em uma página, o script avisa em vez de salvar um resultado parcial.
- As citações são campos do Zotero; a lista de referências é formatada na
  geração pelo Pandoc/citeproc. Em citações narrativas, o nome do autor é
  texto separado do campo que contém o ano. Após alterar autores ou
  referências no Zotero, regenere o documento para atualizar ambos. Prefixos,
  sufixos e localizadores como `[@chave, p. 12]` ainda não são suportados:
  o script interrompe a geração em vez de descartá-los.

O Word pode aplicar um rótulo de confidencialidade durante a gravação. O
script remove somente caixas de texto do cabeçalho/rodapé cujo conteúdo é
exatamente `---Internal Use---` e confere que o rótulo aplicado continua
inalterado. Se uma política reaplicar a marca, a geração é interrompida e
deve-se verificar a política com o responsável.

## Verificação

A geração confere o texto preliminar, os parágrafos do corpo, os campos de
citação, a quantidade de referências, tabelas, seleções do cronograma,
fórmulas, notas de rodapé, imagens e paginação do sumário e da lista. Para
executar os testes locais dos scripts:

```powershell
python -m unittest discover -s .\ferramentas\tests -p test_artigo_unitins.py -v
```
