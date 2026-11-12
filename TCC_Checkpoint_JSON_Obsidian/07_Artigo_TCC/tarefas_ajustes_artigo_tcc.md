# Checklist dos ajustes pedidos pelo orientador

Esta lista foi refeita a partir da reuniao de 11/11/2026 e dos comentarios e
sugestoes identificados no Google Docs. Ela nao inclui recomendacoes gerais do
parecer critico nem tarefas de implementacao que o orientador nao pediu nessa
reuniao.

Legenda:
- **Feito no artigo:** a mudanca aparece em `artigo_tcc_unitins.md`.
- **Pendente:** ainda precisa ser feita, confirmada ou decidida.
- **Opcional:** o orientador sugeriu apenas se houver tempo.

## Ajustes principais

### 1. Capitulo 2 — comentario C1

- [x] Renomear o capitulo 2 para **Revisao Bibliografica**. O titulo atual do
  artigo atende ao comentario “Isso deve estar dentro do Item 2. Revisao
  Bibliografica”.
- [ ] Se o comentario ainda estiver aberto no Google Docs, responder/resolver
  depois de conferir a versao final. A mudanca no Markdown nao resolve o
  comentario no documento online.

### 2. Mapeamento sistematico — sugestoes S1, S2 e S3

- [ ] Escrever o metodo do mapeamento sistematico, incluindo **bases
  consultadas, string de busca utilizada e periodo consultado**. O orientador
  pediu que se descrevesse como a pesquisa foi feita; nao inventar esses dados.
- [ ] Inserir a descricao como secao **3.10 Mapeamento Sistematico**, depois da
  3.9, e aplicar ao titulo o estilo de secao correspondente no DOCX.
- [ ] Apresentar os **resultados do mapeamento** no capitulo 4, em vez de
  deixar somente uma secao de trabalhos relacionados.
- [ ] Aplicar S1 e S3 de forma coordenada: S1 exclui a secao 2.6 atual e S3
  inclui esse conteudo na nova secao de resultados 4.3. Aceitar apenas S1
  removeria tambem o Quadro 1; aceitar apenas S3 duplicaria o conteudo.
- [ ] Retirar do texto a nota/instrucao em vermelho “Levaria esses resultados
  para os resultados neste momento...” ao transferir o material; ela nao deve
  permanecer como texto do artigo.
- [ ] Completar a nova secao 4.3 com os resultados reais do mapeamento. A copia
  da antiga 2.6, por si so, nao documenta bases, busca, selecao nem resultados
  de um mapeamento.
- [ ] Manter a estrutura acordada: 4.1 Resultados e contribuicoes esperadas;
  4.2 Arquitetura proposta; 4.3 Resultados do Mapeamento Sistematico de
  Literatura; 4.4 Cronograma.
- [ ] Depois de concluir o mapeamento e mover o conteudo, renumerar os quadros
  pela ordem de aparicao e atualizar suas citacoes e a lista de quadros. O
  orientador pediu para conferir o numero do quadro.
- [ ] Atualizar sumario, listas e roteiro da Introducao para refletir a
  estrutura final. No Markdown, o roteiro da Introducao ja foi atualizado; o
  sumario e as listas do DOCX ainda precisam ser conferidos.

**Estado atual do artigo:** o conteudo continua em `2.6 Trabalhos relacionados`,
e o cronograma e `4.3`. A secao de metodo do mapeamento e seus resultados ainda
nao foram incluidos. Portanto, este conjunto de ajustes nao esta concluido.

### 3. Arquitetura proposta — sugestao S3 e orientacao verbal

- [x] Incluir a secao **4.2 Arquitetura proposta** e uma figura com titulo e
  fonte.
- [x] Substituir a frase provisoria e remover o marcador “Explique figura”.
- [ ] Conferir e melhorar a explicacao da figura: descrever como as tecnologias
  interagem e como o fluxo se relaciona aos parametros que serao medidos.
- [ ] Confirmar que a figura mantem o nucleo **“Arquitetura Experimental”**,
  sem repetir blocos de contexto, desafios, motivacao ou avaliacao que ja
  estejam explicados em outras partes.
- [ ] Explicar no texto os elementos do fluxo relevantes: entrada no turno,
  escritor de memoria/GU-JSON, modelos comparados, checkpoint e relacao entre
  turnos. Ajustar a explicacao ao protocolo que sera realmente usado.
- [ ] Na versao DOCX, conferir os estilos dos elementos inseridos: o titulo da
  secao 3.10 deve ser titulo de secao; texto explicativo e imagem nao devem
  aparecer como titulos no sumario.

**Estado atual do artigo:** a secao e a Figura 1 foram acrescentadas, mas a
explicacao ainda deve ser revisada contra todos os pontos verbais do orientador.

### 4. Resultados esperados e sua apresentacao

- [x] Manter a secao de resultados esperados e listar as evidencias/metricas
  previstas.
- [ ] Deixar explicito como os resultados do TCC II poderao ser apresentados,
  por exemplo, em graficos comparando os modelos.
- [ ] Se forem incluidos graficos antes de haver resultados, identifica-los
  claramente como **ilustrativos, com dados sinteticos**, para nao serem
  confundidos com resultados experimentais.

### 5. Linguagem de projeto — comentario C2 e sugestao S4

- [x] Trocar na secao 5 a formulacao “este projeto delineou” por linguagem de
  proposta (“este projeto propoe”).
- [x] Reescrever a frase sobre resultados para o futuro e ajustar a lista de
  desdobramentos, que terminava com pontuacao incompleta.
- [x] Corrigir o ponto e virgula final da lista de desdobramentos futuros,
  encerrando a enumeracao com pontuacao adequada.
- [ ] Revisar o restante das consideracoes finais para nao dar a entender que
  experimento ou resultados futuros ja foram concluidos.
- [ ] Se C2 e S4 ainda estiverem ativos no Google Docs, aplicar/rejeitar as
  sugestoes conforme a versao final (incluindo rejeitar a sugestao de cor
  depois de corrigir o texto) e resolver C2. A edicao do Markdown nao altera o
  estado das sugestoes nem do comentario no documento online.

### 6. Formatacao e identificacao institucional

- [ ] Conferir o cabecalho segundo o manual do TCC.
- [ ] Obter/substituir o logotipo de baixa resolucao pela versao adequada,
  conforme orientacao para consultar o professor indicado.
- [ ] Remover todas as ocorrencias da marca “Internal Use” e conferir o PDF
  final; a marca pode reaparecer se o arquivo mantiver o rotulo de
  sensibilidade.
- [ ] Conferir sumario, listas e numeracao no DOCX/PDF final depois de fechar a
  estrutura das secoes e dos quadros.

## Sugestao opcional

- [ ] Se houver tempo depois dos ajustes principais, avaliar uma descricao da
  organizacao do desenvolvimento em camadas, dados, testes e persistencia para
  evidenciar engenharia de software. O orientador ficou de enviar a referencia
  ou o nome da abordagem; aguardar essa informacao antes de escolher uma.

## Para fechar com o orientador

- [ ] Conferir o comentario possivelmente resolvido na imagem da arquitetura
  (filtrar comentarios resolvidos no Google Docs); seu conteudo nao foi
  recuperado na leitura anterior.
- [ ] Depois dos ajustes principais, enviar a versao revisada ao orientador
  para a ultima revisao.

## Itens que nao sao requisitos confirmados

- A estimativa de 42-43 paginas foi uma previsao, nao uma exigencia.
- Os detalhes de bases, termos de busca, periodo e resultados do mapeamento
  devem vir da pesquisa realmente realizada; nao podem ser preenchidos por
  suposicao.
- A sugestao sobre desenvolvimento em camadas e opcional, nao condicao para
  concluir os ajustes principais.
