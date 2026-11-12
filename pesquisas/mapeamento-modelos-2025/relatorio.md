# Mapeamento de modelos candidatos ao GU-JSON

> Atualizacao: a [busca abrangente](relatorio-busca-abrangente.md) amplia esta
> triagem historica e corrige a omissao de T5Gemma 2. Ela tambem identificou
> PrahokBART e novos modelos de difusao; a triagem ampliada ainda e parcial.

**Data de corte:** 12/11/2026. **Natureza:** mapeamento sistematico
exploratorio documental, nao benchmark nem revisao bibliografica exaustiva.

## 1. Resultado executivo

Com as restricoes simultaneas de **base/pretrained, publicacao desde 2025,
ate 1 bilhao de parametros totais, licenca admitida, um unico motor nativo
e 4 GB de VRAM**, nao foi possivel preencher os tres grupos de geracao.

- Ha **seis candidatos/reservas autoregressivos com caminho nativo
  documentado em llama.cpp**, ainda sem teste de carregamento ou VRAM.
- T5Gemma pequeno existe e possui checkpoints pretrained, mas seu suporte
  nativo nao foi confirmado nos dois motores nas revisoes consultadas.
- Difusao pequena existe. BD3LM-OWT encontra obstaculos de runtime e contexto;
  os Qwen3 diffusion localizados usam linhagem pos-treinada/SFT e arquitetura
  propria, nao satisfazendo o criterio de base puro.
- Recomenda-se **llama.cpp** para o piloto local. Mudar para RunPod pode
  resolver capacidade/ambiente, mas nao transforma um checkpoint instruct
  em base nem acrescenta suporte nativo ausente.

**Nao ha candidato aprovado em execucao E1/E2.** As confirmacoes abaixo
sao documentais D1/D2, conforme o [protocolo](protocolo.md).

## 2. Cobertura e rastreabilidade

Foram inspecionados **36 checkpoints na triagem tecnica**: 34 da coleta
principal e dois Sarashina adicionais. Incluindo popularidade e seus
falsos positivos, foram obtidos metadados de **46 IDs unicos**.

| Conjunto utilizado | Horario UTC de inicio/fim das requisicoes | Respostas | Publicas / restritas |
|---|---|---:|---:|
| [Coleta principal](dados/coleta-final-20261112/evidencias.json) | 12/11/2026 11:49:45 a 11:51:15 | 171 | 143 / 28 |
| [Complementos](dados/complementos-20261112/evidencias.json) | 12/11/2026 11:59:38 a 12:00:16 | 74 | 62 / 12 |

As respostas restritas sao HTTP 401 de arquivos gated; nao foram tratadas
como configs validos nem houve tentativa de contornar autenticacao.
As paginas publicas dos modelos Gemma/T5Gemma foram consultadas no
complemento. A primeira coleta de 30 IDs foi preservada como historico,
mas nao fundamenta as contagens finais.

Fontes/consultas exatas: [manifesto principal](fontes.json) e
[manifesto complementar](fontes-complementares.json).
Cada indice de evidencias registra URL, UTC, HTTP e SHA-256. Os CSVs
[principal](dados/coleta-final-20261112/modelos.csv) e
[complementar](dados/complementos-20261112/modelos.csv) identificam SHA,
arquitetura, arquivos de tokenizer e licenca de cada repositorio.

As consultas por familia tem limites de resultados. Nao houve varredura
exaustiva/paginada de todo o Hub, dupla triagem independente ou busca
completa em bases bibliograficas. Ausencia nesta lista nao prova ausencia
de outro candidato. A conclusao de inviabilidade refere-se aos candidatos
e revisoes efetivamente examinados.

## 3. Motor e evidencias de suporte

Revisoes fixadas:

- llama.cpp: `827466b9efa0574806bad7732bcd78bfb6d9311d`.
- vLLM: `b6f417fcd1c291b0cbb013579e7c697ace4e4e0a`.

| Familia / arquitetura | Evidencia nativa no llama.cpp | Interpretacao |
|---|---|---|
| Qwen3 / `Qwen3ForCausalLM` | [Conversor Qwen](dados/coleta-final-20261112/llama-conversion-qwen.py), registro na linha 173; `qwen3.cpp` no inventario | D2 para Qwen3 AR; nao abrange A2DQwen3 |
| Qwen3.5 / `Qwen3_5ForConditionalGeneration` | Mesmo modulo, registro na linha 694; `qwen35.cpp` | D2 arquitetural; reserva multimodal, uso apenas textual |
| Gemma3 / `Gemma3ForCausalLM` | [Conversor Gemma](dados/coleta-final-20261112/llama-conversion-gemma.py), linha 125; `gemma3.cpp` | D2 arquitetural; arquivos gated continuam pendentes de aceite |
| Granite / `GraniteMoeHybridForCausalLM` | [Conversor Granite](dados/coleta-final-20261112/llama-conversion-granite.py), linha 434 | D2; o conversor reconhece modelos sem camadas SSM e os converte para Granite denso |
| Llama / `LlamaForCausalLM` | [Registro completo](dados/coleta-final-20261112/llama-conversion-init.py) e [conversor Llama](dados/complementos-20261112/llama-conversion-llama.py) | D2 arquitetural para Sarashina; contexto impede o protocolo comum |
| T5Gemma / `T5GemmaForConditionalGeneration` | Ausente do registro consultado; [modulo T5](dados/coleta-final-20261112/llama-conversion-t5.py) registra T5/MT5/UMT5, nao T5Gemma | Nao confirmar D2 por analogia com T5 |
| BD3LM / `BD3LM`; dLLM / `A2DQwen3LMHeadModel` | Nao identificados no registro/conversores consultados | Sem D2 confirmado; codigo proprio nao e suporte nativo |

O [inventario de implementacoes](dados/coleta-final-20261112/llama-model-list.json)
complementa os conversores. Registro de classe nao prova conversao bem-sucedida
de cada checkpoint: o teste E1 continua necessario.

A [documentacao do vLLM](dados/coleta-final-20261112/vllm-gpu.md)
nao oferece Windows nativo; indica Linux/WSL. A GTX 1650 nao deve ser
descartada simplesmente por compute capability: o minimo CUDA documentado
e 7.5. Ainda faltariam validar build, kernels, precisao e memoria dessa GPU.
Para o notebook Windows e batch de uma sequencia, llama.cpp e a escolha
operacional mais simples, nao uma conclusao de desempenho superior.

A [lista de modelos vLLM](dados/coleta-final-20261112/vllm-supported-models.md)
recomenda plugins para encoder-decoder nao nativos; o fallback Transformers
nao comprova suporte generico a T5Gemma. A lista inclui DiffusionGemma
26B-A4B-it: portanto nao seria correto afirmar que vLLM nao suporta
qualquer difusao; esse exemplo excede o teto total e e instruct.

## 4. Triagem tecnica completa

`Data repo` abaixo e **createdAt**, nao dia comprovado de lancamento.
Os candidatos principais pertencem a familias publicadas em 2025/2026,
conforme seus model cards/anuncios; datas exatas de lancamento nao sao
inferidas do Hub. Por exemplo, Granite declara lancamento em 28/10/2025,
embora seus repositorios tenham sido criados em 07/10.

`N` e a contagem `safetensors.total` observada. Para os checkpoints
convencionais ela e uma evidencia quantitativa de tamanho, mas nao
substitui conferencia de pesos compartilhados/quantizados/empacotados.
Os exemplos BitNet/Ornith da secao 8 mostram por que nao confiar cegamente
nesse campo. As exclusoes por tamanho tambem consideram os cards/configs.

Tokenizers: **Q** Qwen2Tokenizer/BPE; **G** arquivos Gemma identificados,
conteudo gated; **I** GPT2Tokenizer/BPE Granite; **F** PreTrainedTokenizerFast;
**L** TokenizersBackend Liquid; **B** familia GPT-2/OWT BD3LM;
**S** LlamaTokenizer/SentencePiece Sarashina; **R** arquivos identificados
no CSV, sem necessidade de aprovar o tokenizer de um modelo ja excluido.
Todos os arquivos identificados ficam vinculados ao SHA do respectivo modelo.

### 4.1 Autoregressivos e hibridos pretrained

| Checkpoint original no Hub | Data repo | N | Licenca | Tok. | Decisao |
|---|---|---:|---|---|---|
| Qwen/Qwen3-0.6B-Base | 2025-04-28 | 596049920 | Apache-2.0 | Q | Candidato D2; shortlist |
| Qwen/Qwen3.5-0.8B-Base | 2026-02-28 | 873438784 | Apache-2.0 | Q | Reserva D2; multimodal e hibrido, nao equivalente a decoder denso |
| google/gemma-3-270m | 2025-08-05 | 268098176 | Gemma | G | Candidato D2, condicional ao aceite; shortlist |
| google/gemma-3-1b-pt | 2025-02-20 | 999885952 | Gemma | G | Reserva D2; maior pressao de memoria |
| ibm-granite/granite-4.0-350m-base | 2025-10-07 | 352379904 | Apache-2.0 | I | Candidato D2; shortlist; todas as 28 camadas sao attention |
| ibm-granite/granite-4.0-h-350m-base | 2025-10-07 | 340332224 | Apache-2.0 | I | Reserva D2; 4 camadas attention e 28 Mamba |
| ibm-granite/granite-4.0-1b-base | 2025-10-07 | 1631750144 | Apache-2.0 | I | Excluir: >1B total; card declara 1.6B |
| tiiuae/Falcon-H1-0.5B-Base | 2025-05-01 | 521411104 | Falcon-LLM | F | Excluir do recorte de licencas; nao e Apache |
| tiiuae/Falcon-H1-Tiny-90M-Base | 2026-01-12 | 91131072 | Falcon-LLM | F | Excluir do recorte de licencas |
| tiiuae/Falcon-H1-Tiny-Multilingual-100M-Base | 2026-01-12 | 107908288 | Falcon-LLM | F | Excluir do recorte de licencas |
| LiquidAI/LFM2.5-350M-Base | 2026-03-31 | 354483968 | LFM Open License v1.0 | L | Excluir do recorte de licencas, apesar de caminho arquitetural nativo |
| LiquidAI/LFM2.5-230M-Base | 2026-06-16 | 229693184 | LFM Open License v1.0 | L | Excluir do recorte de licencas |
| sbintuitions/sarashina2.2-0.5b | 2025-03-03 | 793048320 | MIT | S | Excluir da configuracao atual: contexto 8192 < 8192+1200 |
| sbintuitions/sarashina2.2-1b | 2025-03-03 | 1407538944 | MIT | S | Excluir: >1B total, apesar de nome 1B |

As exclusoes Falcon/Liquid sao do **criterio autorizado**, nao uma afirmacao
de que pesquisa academica seja proibida. O usuario abriu excecao para Gemma
e modelos do top 10, nao para toda licenca proprietaria.
Hibridos SSM/Transformer continuam gerando autoregressivamente e nao preenchem
por si so o grupo encoder-decoder ou difusao.

### 4.2 Encoder-decoder pretrained

| Checkpoint | Data repo | N | Licenca / tokenizer | Decisao |
|---|---|---:|---|---|
| google/t5gemma-s-s-prefixlm | 2025-06-19 | 312517632 | Gemma / G | Sem suporte nativo confirmado |
| google/t5gemma-b-b-prefixlm | 2025-06-19 | 591490560 | Gemma / G | Sem suporte nativo confirmado |
| google/t5gemma-l-l-prefixlm | 2025-06-19 | 1241761792 | Gemma / G | >1B e suporte nao confirmado |
| google/t5gemma-s-s-ul2 | 2025-06-19 | 312517632 | Gemma / G | Sem suporte nativo confirmado |
| google/t5gemma-b-b-ul2 | 2025-06-19 | 591490560 | Gemma / G | Sem suporte nativo confirmado |

PrefixLM/UL2 sao variantes de treinamento, nao novos paradigmas independentes.
Selecionar um checkpoint sem `-it` e importante: o T5Gemma IT proposto no
artigo anterior nao satisfaz o novo recorte de base.

### 4.3 Difusao e conversoes para difusao

| Checkpoint | Data repo | N | Licenca / tokenizer | Decisao |
|---|---|---:|---|---|
| kuleshov-group/bd3lm-owt-block_size4 | 2025-02-26 | 169627250 | Apache-2.0 / B | Runtime proprio; contexto 1024 |
| kuleshov-group/bd3lm-owt-block_size8 | 2025-02-26 | 169627250 | Apache-2.0 / B | Mesmo obstaculo; mesma familia |
| kuleshov-group/bd3lm-owt-block_size16 | 2025-02-25 | 169627250 | Apache-2.0 / B | Mesmo obstaculo; mesma familia |
| kuleshov-group/bd3lm-owt-block_size1024-pretrain | 2025-03-18 | 169627250 | Apache-2.0 / B | Mesmo obstaculo; nao equivale a contexto de 8192 |
| GSAI-ML/LLaDA-8B-Base | 2025-02-19 | 8015581184 | MIT / R | >1B total |
| Dream-org/Dream-v0-Base-7B | 2025-04-03 | 7615616512 | Apache-2.0 / R | >1B total |
| dllm-hub/Qwen3-0.6B-diffusion-mdlm-v0.1 | 2025-12-04 | 751632384 | Apache-2.0 / Q | Linhagem pos-treinada/SFT; A2DQwen3 sem D2 confirmado |
| dllm-hub/Qwen3-0.6B-diffusion-bd3lm-v0.1 | 2025-12-04 | 751632384 | Apache-2.0 / Q | Linhagem pos-treinada/SFT; A2DQwen3 sem D2 confirmado |
| LiquidAI/LFM2.5-Encoder-350M-Diffusion | 2026-07-10 | 354483968 | LFM propria / L | Instrucao e licenca fora do recorte |

O [card do Qwen3 BD3LM](dados/coleta-final-20261112/modelos/dllm-hub__Qwen3-0.6B-diffusion-bd3lm-v0.1.README.md)
identifica `Qwen/Qwen3-0.6B` como origem, nao `Qwen3-0.6B-Base`, e lista
dados SFT. Seu exemplo usa AutoModelForMaskedLM, codigo remoto, sampler
especifico e chat template. **O checkpoint existe**, mas nao satisfaz
as novas restricoes; nao deve permanecer descrito apenas como "nao localizado".

O [exemplo nativo de difusao llama.cpp](dados/coleta-final-20261112/llama-diffusion.md)
usa CLI e parametros de passos/blocos proprios. Nao confundir um mesmo motor
com um mesmo algoritmo de geracao. A arquitetura Liquid bidirecional aparece
no conversor atual; sua exclusao aqui nao depende de alegar ausencia de suporte.

### 4.4 Controles e exclusoes adicionais

| Checkpoint | Data repo | N | Licenca / tokenizer | Motivo |
|---|---|---:|---|---|
| Qwen/Qwen3-0.6B | 2025-04-27 | 751632384 | Apache-2.0 / Q | Pos-treinado; usar o checkpoint `-Base` |
| google/gemma-3-1b-it | 2025-03-10 | 999885952 | Gemma / G | Instruction-tuned |
| LiquidAI/LFM2-350M | 2025-07-10 | 354483968 | LFM propria / L | Instruction-tuned; licenca fora do recorte |
| HuggingFaceTB/SmolLM2-360M | 2024-10-31 | 361821120 | Apache-2.0 / R | Lancamento anterior a 2025 |
| HuggingFaceTB/SmolLM3-3B | 2025-07-08 | 3075098624 | Apache-2.0 / R | >1B total |
| meta-llama/Llama-3.2-1B | 2024-09-18 | 1235814400 | Llama 3.2 / R | >1B total e anterior a 2025 |
| allenai/OLMo-2-0425-1B | 2025-04-17 | 1484916736 | Apache-2.0 / R | >1B total |
| PleIAs/Baguettotron | 2025-11-10 | 320956992 | Apache-2.0 / R | Card declara treinamento nativo para instrucoes com thinking traces |

Treinado do zero nao significa automaticamente "base sem instrucao".
Tampouco um modelo derivado de Stable Diffusion no nome do ranking e
necessariamente um gerador textual por difusao: MagicPrompt e GPT-2.

## 5. Shortlist, tokenizer e licencas

Sugestao de **ate tres familias**, priorizando margem de memoria:

1. [Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base):
   Apache-2.0; Qwen2Tokenizer/BPE, vocabulario configurado 151936;
   contexto do modelo 32768.
2. [Granite-4.0-350m-base](https://huggingface.co/ibm-granite/granite-4.0-350m-base):
   Apache-2.0; GPT2Tokenizer/BPE, vocabulario 100352; contexto 32768.
3. [Gemma-3-270m](https://huggingface.co/google/gemma-3-270m):
   termos Gemma; tokenizer.json, tokenizer.model e tokenizer_config.json
   identificados no mesmo SHA; contexto 32768 segundo o card publico.
   Aceite dos termos e inspecao dos arquivos completos pendentes.

Reservas: Gemma-3-1b-pt, Granite-4.0-h-350m-base e Qwen3.5-0.8B-Base.
As duas ultimas mudam tambem a composicao arquitetural; Qwen3.5 e multimodal.
Nao tratar variantes da mesma familia como tres evidencias independentes
de um efeito causal de paradigma.

SHAs da shortlist:

| Modelo | SHA dos arquivos originais |
|---|---|
| Qwen3-0.6B-Base | `da87bfb608c14b7cf20ba1ce41287e8de496c0cd` |
| Granite-4.0-350m-base | `a50b46cef21c8a86b15f0496cb794487a78a910b` |
| Gemma-3-270m | `9b0cfec892e2bc2afd938c98eabe4e4a7b1e0ca1` |

Os tokenizers nativos sao parte do tratamento experimental, nao algo a ser
substituido por um tokenizer comum. A mesma entrada textual pode consumir
numeros distintos de tokens. `model_max_length` do tokenizer, inclusive
valores sentinela enormes, nao substitui o contexto do config/model card.

**Licencas:** Apache-2.0/MIT admitem uso e redistribuicao sob suas condicoes
de avisos/licenca; nao dispensam atribuicao. Os
[termos Gemma](https://ai.google.dev/gemma/terms) nao sao Apache/MIT:
exigem cumprimento das restricoes de uso e condicoes de redistribuicao
(termos, avisos e politicas aplicaveis). A excecao autoriza avaliar a
possibilidade de uso, nao ignorar aceite ou chamar a licenca de permissiva.

O [card Falcon](dados/coleta-final-20261112/modelos/tiiuae__Falcon-H1-0.5B-Base.README.md)
aponta a [Falcon-LLM License](https://falconllm.tii.ae/falcon-terms-and-conditions.html);
nao houve parecer juridico nem aprovacao dessa excecao.
A [licenca Liquid coletada](dados/coleta-final-20261112/modelos/LiquidAI__LFM2.5-350M-Base.LICENSE)
estabelece limitacao comercial por receita de US$10 milhoes e disposicoes
para pesquisa/organizacoes qualificadas. Portanto nao e uma permissiva
irrestrita. Nenhuma dessas familias aparece no top 10 operacional abaixo.

## 6. Memoria: estimativa, nao medicao

Condicao proposta: pesos/KV F16, uma sequencia, um escritor por vez,
entrada ate 8192 tokens e saida ate 1200. Reservar **10240 tokens de
contexto total** acomoda a soma 9392 sem reduzir so um dos modelos.

Piso de pesos em GiB = `2 * N / 2^30`. Para attention densa com GQA:
KV F16 = `2(K,V) * 2 bytes * camadas * KV_heads * head_dim * contexto`.
O [analisador](scripts/analisar-coleta.ps1) reproduz os valores em
[estimativa-pesos.csv](dados/coleta-final-20261112/estimativa-pesos.csv).
Ele deixa KV vazio quando nao aplica/nao ha config publico suficiente.

| Modelo | Pesos F16 (GiB) | KV F16 a 10240 (GiB) | Leitura |
|---|---:|---:|---|
| Qwen3-0.6B-Base | 1.110 | 1.094 | Cerca de 2.204 GiB antes dos demais custos |
| Granite-4.0-350m-base | 0.656 | 0.273 | Cerca de 0.930 GiB antes dos demais custos |
| Gemma-3-270m | 0.499 | Nao calculado aqui | Config gated; nao presumir formula global para attention local |
| Gemma-3-1b-pt | 1.862 | Nao calculado aqui | Maior risco de pressao em 4 GB |
| Granite-4.0-h-350m-base | 0.634 | Nao usar formula densa global | Somar estados SSM e attention no piloto |

Esses numeros **nao incluem** buffers, ativacoes, CUDA, workspace, logits,
alocador, estados SSM, overhead do motor ou memoria do desktop. Nao sao
comprovacao de que qualquer configuracao cabe integralmente em 4 GB.
A GTX 1650 tambem nao deve ser tomada como equivalente a uma GPU moderna
com o mesmo tamanho de VRAM. Medir tempo e memoria no hardware real.

## 7. Mesma tarefa/configuracao: criterio de aceitacao

Antes de aceitar um candidato:

1. Converter pelo caminho nativo, carregar em llama.cpp na revisao fixada e
   registrar SHA do GGUF produzido, build, CUDA/backend e tokenizer.
2. Executar completion base com o mesmo prompt, schema, documentos SUMIE,
   greedy, limite 1200, contexto 10240, uma sequencia e microbatch fixado.
3. Medir o piloto completo, incluindo maiores entradas/estados, memoria
   total/processo, latencia, falhas e tokens; nao inferir VRAM de peso em disco.
4. Nao usar chat template instruct, grammar, reparo, truncamento adicional,
   offload ou quantizacao especifica so no candidato que falhou.
5. Se o limite nao couber em todos, revisar uma condicao comum e repetir
   o piloto inteiro; nao mudar silenciosamente o protocolo.

Conferir ainda a divergencia preexistente entre 300 tokens no indice
e 1200 no artigo. Aqui foi adotado 1200 apenas como hipotese de triagem.
Nenhum documento do artigo foi alterado.

Resultado atual por grupo:

| Grupo | Ate tres representantes? | Principal barreira |
|---|---|---|
| Decoder-only AR | Sim, documentalmente, com reservas | Aceite Gemma e verificacao E1/E2 |
| Encoder-decoder | Nao confirmado neste recorte | T5Gemma nao confirmado nativamente |
| Difusao textual | Nao confirmado neste recorte | Runtime/contexto ou linhagem SFT/tamanho/licenca |

Ampliar VRAM em RunPod preservando llama.cpp e uma extensao operacional
possivel. Aceitar Transformers/custom samplers, modelos instruct ou outro
limite de contexto seria **mudanca do recorte**, nao simples instalacao.
Nao foi provisionado Pod, gasto credito ou baixado peso.

## 8. Ranking separado: pequenos por likes do Hub

Fonte: [consulta preservada](dados/complementos-20261112/ranking-pequenos-bruto.json),
API publica Hugging Face, em 12/11/2026, horario por requisicao no indice.
Universo operacional: `text-generation`, tamanho indexado ate 1B, primeiros
20 por likes. Apos verificar falsos positivos, selecionar os dez primeiros.
**Sem filtro de ano ou de base nesta lista contextual.** A elegibilidade
experimental continua exigindo ambos.

| Posicao | Repositorio | Likes | Licenca declarada | Selecao experimental atual |
|---:|---|---:|---|---|
| 1 | openai-community/gpt2 | 3931 | MIT | Fora: anterior a 2025 |
| 2 | Qwen/Qwen3-0.6B | 1893 | Apache-2.0 | Fora: pos-treinado, nao `-Base` |
| 3 | google/gemma-3-1b-it | 1313 | Gemma | Fora: instruct |
| 4 | google/gemma-3-270m | 1146 | Gemma | Shortlist documental, condicional ao aceite |
| 5 | google/functiongemma-270m-it | 1128 | Gemma | Fora: instruct especializado |
| 6 | Qwen/Qwen2.5-0.5B-Instruct | 742 | Apache-2.0 | Fora: anterior a 2025 e instruct |
| 7 | Gustavosta/MagicPrompt-Stable-Diffusion | 740 | MIT | Fora: anterior a 2025 e ajuste especializado |
| 8 | google/gemma-3-270m-it | 715 | Gemma | Fora: instruct |
| 9 | distilbert/distilgpt2 | 667 | Apache-2.0 | Fora: anterior a 2025 |
| 10 | Qwen/Qwen2.5-0.5B | 494 | Apache-2.0 | Fora: anterior a 2025 |

Tabela reproduzida por `-RankingPequenos` em
[top10-pequenos-verificado.csv](dados/complementos-20261112/top10-pequenos-verificado.csv).
As licencas sao as declaradas nos metadados/card; a excecao de licenca
propria nao remove exclusoes por base, ano, tamanho ou runtime.

Tres falsos positivos da consulta foram explicitamente excluidos:

- `microsoft/bitnet-b1.58-2B-4T`: o card declara ~2B parametros; o indice
  conta elementos dos tensores empacotados, nao os parametros logicos.
- `ornith-ai/Ornith-1.0-9B` e `ornith-ai/Ornith-1.0-35B`: os cards descrevem
  modelos 9B/35B; os poucos tensores indexados nao representam o modelo total.

As exclusoes constam no manifesto; nao se alterou o ranking em silencio.
Likes sao popularidade acumulada de repositorios, nao qualidade na tarefa
ou numero de execucoes. O ranking nao substitui a triagem tecnica.

## 9. Artefatos e verificacao

- [Protocolo separado](protocolo.md).
- [Scripts de coleta e analise](scripts).
- [Manifesto principal](fontes.json) e [complementar](fontes-complementares.json).
- [Evidencias principais](dados/coleta-final-20261112/evidencias.json) e
  [complementares](dados/complementos-20261112/evidencias.json).
- [Avisos e licencas dos materiais de terceiros](AVISOS-TERCEIROS.txt).

Verificacoes executadas: sintaxe PowerShell; integridade SHA-256 de todas
as 245 respostas das duas coletas utilizadas; contagem CSV/manifesto;
consistencia de SHA e tamanho contra JSON original; dez entradas de
ranking em ordem decrescente com tamanho conferido; formulas de pesos/KV.
Tambem foram verificadas a recusa de sobrescrita de snapshots, a rejeicao
de contagem/hash inconsistentes e a omissao de estimativa indevida para
pesos empacotados. Links locais e presenca dos 36 IDs na triagem conferidos.
Essas verificacoes validam os artefatos, **nao a execucao dos modelos**.
