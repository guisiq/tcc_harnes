# Protocolo do mapeamento de modelos candidatos

Para a ampliacao paginada e reproduzivel da descoberta, veja o
[protocolo da busca abrangente](protocolo-busca-abrangente.md).

## 1. Objetivo e delimitacao

Mapeamento sistematico exploratorio de checkpoints de geracao textual para
reescrita integral de checkpoints JSON (GU-JSON), sem alterar o prompt para
favorecer modelos. Pesquisa iniciada em 12/11/2026, com janela de publicacao
de 01/01/2025 a 12/11/2026.

Esta pasta e independente do artigo e de sua bibliografia atual. Nenhuma
decisao experimental do artigo e alterada automaticamente pelo levantamento.

Requisitos confirmados com o solicitante:

- Ate 1.000.000.000 de parametros TOTAIS, incluindo embeddings; em MoE, nao
  considerar somente parametros ativos.
- Checkpoint pretrained/base, sem ajuste instruct/chat. Um nome com "Base"
  nao dispensa a leitura do model card.
- Pesos publicamente disponibilizados. Licencas permissivas como conjunto
  principal; as excecoes autorizadas sao Gemma e modelos do top 10 com
  licencas proprias que permitam o uso pretendido, identificadas separadamente,
  sem chama-las de Apache/MIT. Outras licencas proprias nao entram
  automaticamente no conjunto principal.
- Um UNICO motor, a escolher entre llama.cpp e vLLM; sem port de arquitetura,
  plugin proprio ou sampler implementado pelo pesquisador.
- Notebook com 4 GB de VRAM. A viabilidade total de memoria precisa ser
  medida; tamanho dos pesos nao equivale ao pico de VRAM.
- Ate tres representantes de cada grupo: autoregressivo decoder-only,
  encoder-decoder e difusao textual. Os grupos nao sao categorias
  arquiteturais perfeitamente simetricas: encoder-decoder normalmente
  tambem gera autoregressivamente. Hibridos SSM/Transformer sao identificados.
- Ranking de popularidade separado da selecao tecnica.

## 2. Fontes, buscas e reprodutibilidade

Fontes primarias: model cards, configs, metadados e tokenizers dos repositorios
originais no Hugging Face; artigos/relatorios dos autores; codigo e
documentacao oficial dos motores. Resultados de busca web servem apenas para
descoberta e nao comprovam parametros, licenca ou compatibilidade.

Buscas exploratorias registradas:

1. `2025 2026 base pretrained language models under 1B Qwen3 Gemma Granite`
2. `google t5gemma s-s b-b l-l prefixlm pretrained parameters July 2025`
3. `diffusion language model 0.6B Base 2025`
4. `small pretrained base models Falcon H1 Tiny Pleias 2025`
5. Inspecao das familias Qwen, Google/Gemma/T5Gemma, IBM Granite, TII/Falcon,
   LiquidAI, SmolLM e BD3LM a partir das fontes encontradas.

As consultas HTTP exatas, a lista de checkpoints e as revisoes dos motores
estao em [fontes.json](fontes.json). Consultas ao Hub sao limitadas aos
resultados indicados por `limit`; nao se afirma cobertura de todo o Hub.
Repositorios derivados/quantizados nao contam como novos modelos base.
A familia Pleias e consultada como verificacao adicional da descoberta.
O complemento inclui Sarashina2.2, por busca de modelos bilingues pequenos,
e a triagem do ranking de pequenos. Suas consultas e exclusoes auditadas
estao em [fontes-complementares.json](fontes-complementares.json).

O coletor preserva respostas originais, URL, horario UTC, status HTTP, SHA-256,
revisao do modelo, arquivos de tokenizer, parametros e licenca declarados.
Os dados dinamicos do Hub representam o momento da coleta, nao um retrato
historico de 2025. `createdAt` e criacao do repositorio, NAO comprovacao de
data de lancamento publico; verificar anuncio/model card para casos limiares.
Revisoes da branch principal dos motores sao evidencia de implementacao
naquela revisao, nao promessa de suporte em toda versao estavel.

```powershell
& .\pesquisas\mapeamento-modelos-2025\scripts\coletar-fontes.ps1

& .\pesquisas\mapeamento-modelos-2025\scripts\coletar-fontes.ps1 `
  -Manifesto .\pesquisas\mapeamento-modelos-2025\fontes-complementares.json `
  -Saida .\pesquisas\mapeamento-modelos-2025\dados\nova-coleta-complementar

& .\pesquisas\mapeamento-modelos-2025\scripts\analisar-coleta.ps1 `
  -Pasta .\pesquisas\mapeamento-modelos-2025\dados\coleta-final-20261112

& .\pesquisas\mapeamento-modelos-2025\scripts\analisar-coleta.ps1 `
  -Pasta .\pesquisas\mapeamento-modelos-2025\dados\complementos-20261112 `
  -RankingPequenos
```

Requisitos do coletor: PowerShell e `curl.exe`; sem pacotes adicionais,
credenciais, download de pesos ou execucao de codigo remoto. Cada execucao
gera uma nova subpasta em `dados`. O manifesto usado e copiado para a coleta.
HTTP 401/403 de arquivos gated e registrado como acesso restrito, sem tentar
contornar o aceite da licenca. Demais erros tornam a coleta incompleta e
encerram o script com falha explicita. A coleta nao pode aprovar licencas
automaticamente.

## 3. Triagem e extracoes

Para cada checkpoint, registrar:

1. ID original e SHA; familia e grupo de geracao.
2. Evidencia de pretrained/base e data de disponibilidade.
3. Parametros totais expostos pelo Hub (`safetensors.total`) ou outra
   contagem primaria documentada; nao inferir tamanho apenas de "1B".
   O indice do Hub tambem pode contar elementos empacotados ou apenas
   tensores auxiliares. Conferir model card/config antes de tratar essa
   contagem como parametros logicos, especialmente em modelos quantizados.
4. Licenca e suas restricoes: acesso, uso, redistribuicao e derivados.
5. Tokenizer: arquivos na mesma revisao, classe/algoritmo quando publicos,
   vocabulario e tokens especiais quando acessiveis.
6. Arquitetura exata do config; conversor e implementacao nativos no motor.
7. Contexto, suporte a completions e parametros de geracao necessarios.
8. Memoria teorica dos pesos e, em etapa posterior, pico medido.
9. Decisao: candidato documental, reserva, excluido, ou pendente de evidencia.

Ausencia de uma arquitetura no conversor e no registro inspecionados impede
confirma-la como suportada; isso nao prova que ninguem possua um fork externo.
Ter GGUF ou implementacao de T5 nao prova suporte a T5Gemma.
Ter Qwen3 autoregressivo nao prova um checkpoint Qwen3 diffusion.

## 4. Niveis de confirmacao

- **D1:** model card, licenca e metadados identificados.
- **D2:** implementacao e caminho de conversao nativos identificados no motor.
- **E1:** conversao/carregamento e completion realmente executados.
- **E2:** tarefa GU-JSON validada sob o teto de memoria no hardware-alvo.

Este levantamento e documental: nao alegar E1/E2 sem executar esses testes.
Um candidato D2 nao e automaticamente "cabe em 4 GB confirmado".

## 5. Protocolo comum proposto para o piloto posterior

Preservar o protocolo atual de prompt-only, schema e mesma sequencia SUMIE:

- mesmo texto do prompt, sem exemplos individuais, fine-tuning, ferramentas,
  grammar/JSON constrained decoding, reparo ou tentativas extras por modelo;
- interface de completion para modelos base, nao chat template instruct;
- pesos e KV cache em F16 como primeira configuracao comum, batch de sequencias
  igual a 1, um escritor carregado por vez; fixar tambem microbatch no manifesto;
- contexto de entrada ate 8.192 tokens e saida de ate 1.200 tokens, conforme o
  artigo atual; em decoder-only o contexto alocado precisa acomodar a SOMA;
- mesmos documentos textuais; usar os tokenizers nativos, registrar contagens
  por tokenizer e checar que nenhum prompt/estado-ouro exceda o limite;
- greedy quando implementado nativamente, seed registrada, sem confundir
  mesmos parametros nominais com mesmo algoritmo para difusao;
- registrar versao/build, SHA dos pesos e GGUF, runtime/backend, GPU, CUDA,
  tokens de entrada/saida, tempo, falhas e pico de VRAM/RAM.

O indice antigo de 300 tokens e o artigo com 1.200 precisam ser conciliados
ANTES de rodar. O levantamento nao altera essa decisao.

Se F16 nao couber, nao quantizar apenas o modelo que falhou: definir e
justificar outra condicao comum e repetir o piloto em todos. Nao aceitar
CPU offload como prova de que a execucao integral cabe em 4 GB de VRAM.
Mesmo formato/precisao nao significa igualdade de treinamento, dados,
tokenizacao, computacao ou capacidade.

Teste de aceitacao E2: executar todas as transicoes selecionadas para o
piloto, incluir os maiores prompts e estados validos, medir memoria total
da placa e processo, verificar ausencia de offload nao declarado e margem
para o sistema grafico. Nao reduzir o prompt/contexto so para um candidato.

## 6. Popularidade e limites

Ranking apartado de pequenos: consultar os 20 primeiros repositorios com
`pipeline_tag=text-generation`, filtro `num_parameters=min:0,max:1B`, likes
decrescentes, via API publica do Hugging Face, na data/hora da coleta.
Inspecionar falsos positivos de tamanho, registrar exclusoes no manifesto
e selecionar os dez primeiros restantes. Conferir os metadados dos dez.
Nao filtrar data ou tipo base nessa lista contextual; esses filtros
continuam obrigatorios na selecao experimental. O ranking global sem
filtro de tamanho da primeira etapa e preservado apenas como historico,
nao substitui o ranking de pequenos solicitado.

Os likes medem popularidade, nao qualidade em GU-JSON; downloads nao
equivalem a uso em inferencia. Nao usar ambos como evidencia de
superioridade ou como criterio para ignorar a licenca. Modelos sem
pipeline_tag ou sem tamanho indexado podem ficar fora desta consulta:
trata-se de um ranking operacional do Hub, nao de todos os modelos existentes.

Nao sera contratado Pod, gasto credito ou baixado peso neste mapeamento.
A execucao em RunPod e uma etapa posterior, dependente de autorizacao.
