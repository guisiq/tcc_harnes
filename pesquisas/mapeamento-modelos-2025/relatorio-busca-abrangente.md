# Busca abrangente de modelos e literatura

**Corte:** 12/11/2026. **Resultado:** descoberta reproduzivel nas fontes e
consultas declaradas, com triagem humana parcial. Isto nao e um censo de
todos os modelos, benchmark, teste de carregamento ou medicao de memoria.
Os criterios permanecem os do [protocolo](protocolo-busca-abrangente.md).

## 1. Resultado executivo

- **Nao, os encoder-decoder encontrados nao se limitam a Gemma.**
  PrahokBART tem duas versoes pretrained, de aproximadamente 62M e 211M,
  com licenca MIT. Ambas documentam limite de 1.024 posicoes, abaixo da
  entrada de ate 8.192 tokens do protocolo comum; sua arquitetura mBART
  tambem nao teve suporte nativo confirmado nas revisoes consultadas.
- O **T5Gemma 2 270M-270M** foi indevidamente omitido da triagem anterior.
  Ele e pretrained e consta agora no inventario. O Hub informa 786.029.296
  elementos safetensors, incluindo os componentes do checkpoint; nao se deve
  presumir que o total seja simplesmente 270M + 270M. Acesso e condicionado
  ao aceite Gemma; tokenizer completo, motor nativo e memoria estao pendentes.
- Tambem foram encontrados modelos de **difusao pequenos** alem de BD3LM.
  dQwen3.5-0.8B-Base declara nao ter instruction tuning e e promissor para
  verificacao, mas nao teve sampler nativo ou VRAM confirmados. Os tres
  checkpoints CoBit e os modelos E-MoE/MDLM sao outros exemplos, ainda
  pendentes ou incompativeis com a configuracao comum.
- A triagem anterior documenta seis candidatos ou reservas autoregressivos
  com caminho arquitetural em llama.cpp. **Nenhum modelo foi aprovado por
  execucao ou por medicao em 4 GB.** Os tres paradigmas ainda nao estao
  preenchidos sob todos os criterios.

## 2. Cobertura e contagens

| Etapa | Resultado |
|---|---:|
| Consultas Hugging Face / arXiv | 25 / 7 |
| Paginas Hub / arXiv verificadas | 169 / 10 |
| Ocorrencias nas paginas Hub, antes da deduplicacao | 162.573 |
| Ocorrencias nas paginas arXiv, antes da deduplicacao | 1.146 |
| Repositorios de modelos distintos, incluindo fontes adicionais | 116.717 |
| Artigos arXiv distintos | 1.073 |
| Modelos revisados manualmente nesta consolidacao | 42 |
| Artigos com revisao bibliografica explicita | 7 |

A coleta paginada ocorreu entre **12:40:14 e 12:48:42 UTC** de 12/11/2026;
as quatro coletas de fontes adicionais terminaram ate 13:06:10 UTC.
As respostas sao dinamicas e sobrepostas: o total de repositorios **nao**
significa 116.717 modelos base elegiveis. Inclui derivados, tarefas nao
relacionadas, datas fora da janela e registros sem dados suficientes.
CoBit, por exemplo, foi localizado pela literatura e incorporado de uma
fonte adicional porque nao apareceu nas 25 consultas paginadas.

| Decisao no inventario de modelos | Repositorios |
|---|---:|
| Candidato documental ou reserva, sem teste E1/E2 | 6 |
| Excluido | 8.261 |
| Pendente | 108.450 |

Das exclusoes, **8.236** sao repositorios marcados pelo Hub como
`base_model:quantized:*`, tratados como derivados e nao como novos modelos
base distintos; 25 decorrem das revisoes manuais. Onze modelos revisados
manualmente permanecem pendentes. Os demais pendentes **nao foram excluidos**:
nao e possivel concluir que nao existam outros candidatos adequados.
Os 1.066 artigos sem revisao bibliografica explicita tambem permanecem
pendentes.

O [inventario de modelos](dados/busca-abrangente-20261112/triagem-modelos.csv)
conserva uma linha por ID e todas as origens; o
[inventario de artigos](dados/busca-abrangente-20261112/triagem-artigos.csv)
conserva uma linha por ID arXiv. As
[estatisticas](dados/busca-abrangente-20261112/estatisticas.json),
[paginas e hashes](dados/busca-abrangente-20261112/paginas.jsonl),
[matriz de consultas](fontes-busca-abrangente.json),
[revisoes de modelos](revisoes-busca-abrangente.csv) e
[revisoes de artigos](revisoes-artigos.csv) permitem reconciliar as etapas.
A prioridade heuristica nao e uma decisao de elegibilidade.
Os dados arquivados estao ignorados pelo Git e devem ser preservados
separadamente para reproduzir esta coleta em outra maquina.

## 3. Encoder-decoder: resultados alem da primeira busca

| Checkpoint | Evidencia de tamanho | Licenca e tokenizer | Decisao para o protocolo |
|---|---:|---|---|
| [PrahokBART base](https://huggingface.co/nict-astrec-att/prahokbart_base) | 61.611.268 elementos | MIT; `AlbertTokenizer` e `spiece.model` | Pretrained Khmer/ingles; [config](dados/literatura-modelos-20261112/modelos/nict-astrec-att__prahokbart_base.config.json) limita posicoes a 1.024; excluido da configuracao comum |
| [PrahokBART big](https://huggingface.co/nict-astrec-att/prahokbart_big) | 211.270.916 elementos | MIT; `AlbertTokenizer` e `spiece.model` | Pretrained Khmer/ingles; [config](dados/prahokbart-big-20261112/modelos/nict-astrec-att__prahokbart_big.config.json) tambem limita a 1.024; excluido |
| [T5Gemma 2 270M-270M](https://huggingface.co/google/t5gemma-2-270m-270m) | 786.029.296 elementos | Gemma; `tokenizer.json` e `tokenizer_config.json` identificados, conteudo restrito | Pretrained multimodal; suporte nativo e memoria pendentes |
| T5Gemma S-S PrefixLM / UL2 | 312.517.632 elementos cada | Gemma; arquivos de tokenizer identificados, gated | Pretrained; arquitetura T5Gemma sem suporte nativo confirmado |
| T5Gemma B-B PrefixLM / UL2 | 591.490.560 elementos cada | Gemma; arquivos de tokenizer identificados, gated | Pretrained; arquitetura T5Gemma sem suporte nativo confirmado |
| [Pretrain-AKK-60m](https://huggingface.co/Thalesian/Pretrain-AKK-60m) | 60.706.304 elementos | Licenca nao declarada no card/indice; SentencePiece identificado | T5, mas o card nao comprova treinamento base nem licenca; pendente |

Os [cards PrahokBART](dados/literatura-modelos-20261112/modelos/nict-astrec-att__prahokbart_base.README.md)
descrevem pretreino desde o inicio e dados em Khmer e ingles; nao se deve
confundir os checkpoints originais com ajustes de terceiros. O card descreve
normalizacao/segmentacao Khmer e codigos de idioma, que tambem precisariam
ser avaliados para preservar a mesma tarefa.

O [card publico do T5Gemma 2](dados/fontes-busca-20261112/t5gemma2-card-publico.html)
e o [artigo](https://arxiv.org/abs/2512.14856) confirmam o checkpoint
pretrained. Os arquivos `config.json` e `tokenizer_config.json` retornaram
HTTP 401 sem aceite; o inventario de arquivos e a arquitetura indexada
estao na [metadata](dados/fontes-busca-20261112/modelos/google__t5gemma-2-270m-270m.json).
Nao se contornou o acesso.

O pedido [ggml-org/llama.cpp#22670](https://github.com/ggml-org/llama.cpp/issues/22670)
foi encerrado por inatividade, nao como prova de implementacao. Um comentario
posterior descreve patches de terceiros para reranking, sem geracao incremental.
Na revisao fixada, nao foi identificado caminho nativo para a arquitetura
exata. A documentacao vLLM menciona BART por plugin externo, o que nao
comprova mBART nativo nem atende ao criterio sem plugins proprios.

O artigo [RedLLM](https://arxiv.org/abs/2510.26622) estudou encoder-decoder
pretrained desde cerca de 150M, mas as
[consultas registradas](dados/fontes-busca-20261112/busca-redllm.json) nao
localizaram um checkpoint publico dos autores. Isso e **pendencia de
disponibilidade**, nao prova de que ele nao exista.

## 4. Difusao textual

| Familia / variacao | Tamanho e licenca | Tokenizer e situacao |
|---|---|---|
| [Dhara-70M](https://huggingface.co/codelion/dhara-70m) | 71.344.512 elementos; Apache-2.0 | GPT-2; [card](dados/literatura-modelos-20261112/modelos/codelion__dhara-70m.README.md) informa contexto 1.024 e codigo proprio; excluido da configuracao comum |
| CoBit-S LM1B | 130M declarados; MIT | [config original](https://raw.githubusercontent.com/GBATZOLIS/BitstreamDiffusion/a6ba2413e3fc70a30a7bd9d1a2d1af13024e3f88/configs/lm1b/continuous/rate_bits_1M.py) indica `bert-base-uncased`, 128 tokens no experimento e geracao incondicional |
| CoBit-S OWT | 130M declarados; MIT | GPT-2 + codec BPE16; [config](dados/literatura-modelos-20261112/cobit-owt-small-config.py) usa 1.024 tokens e geracao incondicional |
| CoBit-M OWT | 462M declarados; MIT | Mesmo esquema OWT; [config](dados/literatura-modelos-20261112/cobit-owt-medium-config.py) usa 1.024 tokens e geracao incondicional |
| BD3LM OWT, blocos 4 / 8 / 16 / 1024-pretrain | 169.627.250 elementos por checkpoint; Apache-2.0 | Configs informam `model_length=1024`; tokenizer e runtime exigem verificacao; excluidos da configuracao comum |
| [dQwen3.5-0.8B-Base](https://huggingface.co/UT-IFML/dQwen3.5-0.8B-Base) | 752.393.024 elementos; Apache-2.0 | Tokenizer Qwen; [card](dados/triagem-adicional-20261112/modelos/UT-IFML__dQwen3.5-0.8B-Base.README.md) declara base sem instruction tuning; suporte nativo e memoria pendentes |
| [Open-dcoder-0.5B](https://huggingface.co/fredzzp/open-dcoder-0.5B) | 630.167.424 elementos; Apache-2.0 | Tokenizer Qwen; [card](dados/triagem-adicional-20261112/modelos/fredzzp__open-dcoder-0.5B.README.md) exige sampler personalizado; linhagem de treinamento e runtime pendentes |
| [HDLM epsilon 0,05](https://huggingface.co/hdlm-group/hdlm-base-epsilon-0.05) | 162.246.514 elementos; Apache-2.0 | GPT-2; [config](dados/triagem-adicional-20261112/modelos/hdlm-group__hdlm-base-epsilon-0.05.config.json) informa comprimento 1.024; excluido da configuracao comum |
| MDLM / MDLM-MoE / E-MoE LM1B | 139.292.986 / 536.051.002 / 536.051.002 elementos; Apache-2.0 | `bert-base-uncased`; [configs](dados/triagem-adicional-20261112/modelos/ArsenyIvanov__emoe-lm1b.config.json) informam `model_length=128`; excluidos |
| [Dual-LM-470M](https://huggingface.co/ltg/dual-lm-470m) | 468.700.160 elementos; Apache-2.0 | BPE; objetivos autoregressivo e masked-diffusion; [config](dados/triagem-adicional-20261112/modelos/ltg__dual-lm-470m.config.json) informa 2.048 posicoes; excluido |
| A2D GPT-NeoX 160M / 400M | 162.322.944 / 405.334.016 elementos | Cards declaram base sem instruction tuning, mas configs limitam posicoes a 2.048 e nao informam licenca do checkpoint; excluidos |
| [Zarya-0.6B](https://huggingface.co/ai-forever/Zarya-0.6B) | 596.049.920 elementos; MIT | Tokenizer Qwen; card informa contexto 2.048 e tag instruct, enquanto config informa 40.960 posicoes; pureza base e capacidade pendentes |

O [card CoBit](dados/literatura-modelos-20261112/modelos/gbatzolis__CoBit.README.md)
lista tres arquivos `.pt` no **mesmo repositorio**: nao sao tres IDs no
inventario. A configuracao de treinamento documentada nao comprova um limite
arquitetural absoluto, mas tambem nao comprova a tarefa condicionada de
8.192 tokens nem a geracao nativa em llama.cpp ou vLLM. Os tres ficam
pendentes, sem baixar pesos.

O dQwen3.5-0.8B-Base parte de um modelo autoregressivo base e o card
explicitamente nega instruction tuning. Sua
[config](dados/triagem-adicional-20261112/modelos/UT-IFML__dQwen3.5-0.8B-Base.config.json)
informa 262.144 posicoes, mas isso nao prova que o sampler aceite 8.192
tokens no mesmo protocolo ou que caiba em 4 GB. Suporte generico a Qwen3.5
nao comprova suporte ao `DiffuQwen35` nem ao procedimento de difusao.

O [card Dual-LM](dados/triagem-adicional-20261112/modelos/ltg__dual-lm-470m.README.md)
lista 50 branches com diferentes pesos dos objetivos, inclusive variantes
puramente autoregressivas e de masked-diffusion. Esta coleta verificou o
checkpoint `main`, nao os SHAs nem a elegibilidade de todas as branches.

O [estudo comparativo AR/MDLM](https://arxiv.org/abs/2603.22075) relata
modelos de 123,6M e 162,7M. Embora o artigo afirme disponibilizar pesos,
a [arvore Git arquivada](dados/literatura-modelos-20261112/arche-tree.json)
nao os lista, a pagina de releases estava vazia e a API do repositorio Hub
informado retornou HTTP 401. Disponibilidade publica, licenca dos pesos e
compatibilidade ficam pendentes.

Os dois checkpoints Qwen3 diffusion **dllm-hub** revisados anteriormente
derivam de um checkpoint pos-treinado e de dados SFT; essa exclusao nao deve
ser generalizada para dQwen3.5-0.8B-Base. O checkpoint PlaidQ revisado
tambem deriva de Qwen3-0.6B pos-treinado.

## 5. Autoregressivos: referencias para um piloto posterior

Os seguintes sao **candidatos documentais**, nao modelos executados:

| Checkpoint | Elementos safetensors | Licenca / tokenizer | Observacao |
|---|---:|---|---|
| Qwen/Qwen3-0.6B-Base | 596.049.920 | Apache-2.0 / Qwen BPE | Caminho Qwen3 documentado em llama.cpp |
| google/gemma-3-270m | 268.098.176 | Gemma / arquivos Gemma identificados, gated | Aceite necessario; caminho Gemma3 documentado |
| ibm-granite/granite-4.0-350m-base | 352.379.904 | Apache-2.0 / GPT-2 BPE | Caminho Granite documentado |

Como reservas: Qwen3.5-0.8B-Base, Gemma-3-1b-pt e
granite-4.0-h-350m-base. A [triagem tecnica anterior](relatorio.md)
contem os SHAs, licencas, tokenizers e conversores correspondentes. Todos
esses exemplos pertencem ao grupo de geracao autoregressiva; eles nao
substituem representantes dos outros dois grupos.

## 6. Reproducao da consolidacao arquivada

Na raiz do repositorio, com PowerShell 7:

```powershell
$base = '.\pesquisas\mapeamento-modelos-2025'
$fontes = @(
  "$base\dados\fontes-busca-20261112",
  "$base\dados\literatura-modelos-20261112",
  "$base\dados\prahokbart-big-20261112",
  "$base\dados\triagem-adicional-20261112"
)
& "$base\scripts\consolidar-busca-abrangente.ps1" `
  -Pasta "$base\dados\busca-abrangente-20261112" `
  -FontesAdicionais $fontes `
  -Revisoes "$base\revisoes-busca-abrangente.csv" `
  -RevisoesArtigos "$base\revisoes-artigos.csv"
```

O consolidador verifica respostas comprimidas e descomprimidas, URLs, links
de paginacao, contagens, conclusoes, SHAs de fontes adicionais e versoes das
revisoes. A primeira tentativa teve duas falhas explicitas ao interpretar
uma chave JSON vazia; apos correcao do parser, a coleta foi retomada. O
arquivo `falhas.txt` preserva esse historico e nao indica falha da retomada.
Os comandos para executar uma coleta nova estao no
[protocolo](protocolo-busca-abrangente.md).

## 7. O que continua sem conclusao

A busca nao cobre toda a literatura fora do arXiv nem todos os repositorios
fora das consultas e fontes complementares. Os 108.450 modelos pendentes
precisam de triagem antes de se afirmar que nao ha outros elegiveis. Modelo
base, licenca, tokenizer, limite de contexto e suporte nativo devem ser
conferidos para cada candidato.

Mesmo para os seis candidatos documentais, ainda faltam conversao,
carregamento, completion, teste com os mesmos dados e prompts, medicao de
pico de VRAM e conciliacao do limite de saida de 300 versus 1.200 tokens.
Nao houve download de pesos, contratacao de RunPod nem execucao do experimento.
