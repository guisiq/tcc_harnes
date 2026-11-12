# Protocolo da busca abrangente

Este protocolo amplia a descoberta anterior; nao altera os requisitos
experimentais do [protocolo original](protocolo.md). O recorte e de modelos
base/pretrained publicados entre 01/01/2025 e 12/11/2026, com ate
1.000.000.000 de parametros totais, licenca e tokenizer identificados,
um unico motor nativo entre llama.cpp e vLLM e teste posterior em 4 GB.
Os tres grupos sao decoder autoregressivo, encoder-decoder e difusao textual.

## Fontes e estrategia

A matriz executavel [fontes-busca-abrangente.json](fontes-busca-abrangente.json)
define 25 consultas ao Hugging Face Hub e sete ao arXiv. Inclui:

- geracao textual e multimodal com tamanho indexado ate 1B;
- `text2text-generation`, familias encoder-decoder e nomes de pretreinamento,
  inclusive buscas sem filtro de tamanho;
- termos e familias de difusao textual e de modelos base;
- tres consultas ordenadas por ultima modificacao, para ampliar parcialmente
  a descoberta de repositorios antigos; e
- titulos/resumos e outros metadados de literatura do arXiv, sem baixar PDFs.

No Hub, cada consulta usa paginas de ate 1.000 resultados, ordem decrescente
pela data especificada, e segue `Link: rel="next"` ate nao haver proxima
pagina ou a ultima data da pagina atingir o limite inferior da janela.
A pagina de fronteira e mantida integralmente. Nao ha exclusao por nome,
ausencia de tamanho indexado, data de criacao do repositorio ou popularidade.
O campo `createdAt` e a data do repositorio, nao a publicacao do modelo;
registros fora da janela sao mantidos para verificacao. Uma consulta por
`lastModified` nao recupera todos os repositorios antigos relevantes.

As consultas arXiv usam `submittedDate`, paginas de ate 250 e verificam
`startIndex`, `totalResults` e identificadores. As versoes de um mesmo artigo
sao reunidas pelo ID arXiv. Referencias em artigos sao pistas de descoberta,
nao prova da existencia de pesos publicos ou de compatibilidade.
Os metadados sao os observados na coleta, nao um retrato historico congelado
na data inicial do artigo. Buscas seletivas adicionais de RedLLM e fontes
primarias de T5Gemma 2 estao em
[fontes-complemento-busca.json](fontes-complemento-busca.json).
O exame de artigos e dos resultados do Hub gerou uma segunda coleta
[fontes-literatura-modelos.json](fontes-literatura-modelos.json). Seus IDs
entram no mesmo inventario, mesmo quando nenhum filtro paginado os encontrou.
A revisao adicional de modelos encontrados no inventario usa
[fontes-triagem-adicional.json](fontes-triagem-adicional.json). A escolha dos
17 registros foi humana, apoiada nos grupos, tamanho e popularidade
observados; nao representa triagem exaustiva da fila.

## Integridade, inventario e triagem

O coletor grava o manifesto, cada resposta compactada, headers, URL, horario
UTC, status, contagem, proxima pagina e SHA-256 do corpo e do arquivo gzip.
Arquivos `conclusao.json` registram por que cada consulta terminou. Em caso
de erro, a coleta falha explicitamente; `-Retomar` reaproveita somente paginas
cujo URL e hash comprimido coincidem com o indice e conserva as tentativas.

O consolidador exige que todas as consultas tenham terminado, verifica os
dois hashes, URLs iniciais, links nos headers, contagens, ordenacao, cadeia
de paginas e totais arXiv. Reune
IDs identicos, preservando todas as origens `consulta:pagina`, e gera uma
linha por modelo e uma por artigo. Repositorios/versoes diferentes nao sao
automaticamente considerados modelos independentes. Divergencia de SHA
entre paginas e sinalizada; uma revisao manual precisa indicar o SHA.
Fontes complementares opcionais sao verificadas por SHA-256 e suas origens
aparecem como `complemento/pasta/arquivo`. Um repositorio com varios pesos
e uma linha no inventario do Hub; seus checkpoints precisam ser discriminados
separadamente na analise.

Todos os modelos sao inicialmente **pendentes**. A unica exclusao automatica
e de repositorios identificados pelo proprio Hub com a tag
`base_model:quantized:*`: sao derivados, nao modelos base distintos. O motivo
e as paginas de origem permanecem no inventario. Revisoes manuais
documentadas podem confirmar, excluir ou manter qualquer registro pendente.
Uma prioridade e pontuacao heuristicas servem apenas para ordenar leituras;
nao sao decisao de elegibilidade. Nome com `base`, tamanho indexado e tag de
licenca nao substituem model card, pesos originais, verificacao de tokenizer
ou suporte do motor. Artigos nao revisados permanecem pendentes; revisoes
bibliograficas identificam a data da versao e nao aprovam o modelo para uso.

`safetensors.total` e um indice de elementos armazenados; pesos compartilhados,
componentes multimodais, quantizacao e tensores ausentes podem impedir sua
interpretacao direta como parametros logicos. O criterio de 1B e conferido
nas fontes primarias antes da selecao. A regressao obrigatoria e encontrar
`google/t5gemma-2-270m-270m` no inventario com uma decisao explicita.

## Reproducao

Requisitos: PowerShell 7 e `curl.exe`. `ConvertFrom-Json -AsHashtable`
aceita propriedades de metadados com nome vazio ou que diferem por
maiusculas/minusculas. Na primeira tentativa da coleta arquivada, duas
consultas falharam explicitamente por uma propriedade vazia; apos corrigir
o parser, a mesma pasta foi retomada. `falhas.txt`, se presente, e historico
das falhas daquela tentativa; a completude e estabelecida por todas as
conclusoes e pela verificacao do consolidador.

Os arquivos de `dados/`, incluindo respostas arquivadas e inventarios, estao
ignorados pelo Git. Para preservar esta coleta em outra maquina, guarde ou
transfira essa pasta separadamente; refazer consultas dinamicas nao garante
os mesmos resultados. Sem os arquivos arquivados, a consolidacao e os links
locais para evidencias nao funcionam.

Executar na raiz do repositorio, usando uma pasta nova:

```powershell
& .\pesquisas\mapeamento-modelos-2025\scripts\coletar-busca-abrangente.ps1 `
  -Saida .\pesquisas\mapeamento-modelos-2025\dados\nova-busca

# Apenas se a coleta falhar:
& .\pesquisas\mapeamento-modelos-2025\scripts\coletar-busca-abrangente.ps1 `
  -Saida .\pesquisas\mapeamento-modelos-2025\dados\nova-busca -Retomar

& .\pesquisas\mapeamento-modelos-2025\scripts\consolidar-busca-abrangente.ps1 `
  -Pasta .\pesquisas\mapeamento-modelos-2025\dados\nova-busca
```

Uma revisao manual pode ser reaplicada com `-Revisoes arquivo.csv`; os campos
obrigatorios sao `id`, `sha`, `decisao`, `motivo` e `evidencia`. Se o SHA
revisado nao estiver na nova coleta, a execucao falha para impedir a
transferencia silenciosa da decisao a outros pesos. Consolide novamente a
coleta arquivada com `-FontesAdicionais pasta1,pasta2` para incluir as fontes
de modelos revisados e `-RevisoesArtigos arquivo.csv` para aplicar as revisoes
fixadas por ID e data de atualizacao do artigo. Buscas novas podem mudar com
o tempo, inclusive nos totais e nas revisoes do Hub.

## Limites de interpretacao

Esta e uma busca abrangente e auditavel nas fontes e consultas declaradas,
nao um censo de todos os modelos, todos os arquivos do Hub ou toda a
literatura mundial. Um repositorio pode nao conter os termos, tags ou
metadados pesquisados; ha literatura fora do arXiv e modelos fora do Hub.
Uma consulta dinamica tambem pode mudar durante a paginacao. Nao houve
dupla triagem independente. A avaliacao humana e parcial quando houver
registros pendentes, e eles nao podem ser contados como excluidos.

Registro de arquitetura/conversor nao comprova carregamento, tokenizacao,
completion, comparabilidade dos prompts ou consumo de memoria. Nenhum peso
foi baixado e nao houve benchmark, medicao de VRAM ou contratacao de RunPod.
