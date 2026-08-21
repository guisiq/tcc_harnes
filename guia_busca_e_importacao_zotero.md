# Guia Passo a Passo — Busca Bibliográfica e Importação no Zotero

> Como executar a **Fase 0 (Busca de estudos)** do pipeline canônico (Petersen/Kitchenham), de forma sistemática e rastreável, usando o Zotero como fonte de verdade do corpus (ver [planejamento_mini_harness_completo.md](planejamento_mini_harness_completo.md), seção 6.0).
>
> Ordem de execução: **1º os artigos de inspiração e fundamentos** (surveys do tema e referências metodológicas) e **2º os artigos da pesquisa em questão** (o domínio harness/SLM, usando a lista de termos da seção "Strings de busca" em [arquitetura_mini_harness_bibliografico.md](arquitetura_mini_harness_bibliografico.md)).

---

## 0. Pré-requisitos (fazer uma única vez)

1. **Zotero 7+** instalado e aberto (já feito via `setup-harness/setup-tools.ps1`).
2. **Zotero Connector** (extensão do navegador) — instale em https://www.zotero.org/download/connectors para o seu navegador principal. Ele permite salvar itens direto de páginas de busca (arXiv, Google Scholar etc.) com um clique.
3. **Plugin Better BibTeX** (citation keys estáveis, usado como `id` no contrato JSON):
   - Baixe o `.xpi` mais recente em https://github.com/retorquere/zotero-better-bibtex/releases
   - No Zotero: `Ferramentas > Extras (Add-ons) > engrenagem > Install Add-on From File...`
   - Selecione o `.xpi` baixado e reinicie o Zotero.
4. **Habilitar a Local API** (para o harness ler a coleção depois): `Editar > Configurações > Avançado > "Permitir que outros aplicativos neste computador se comuniquem com o Zotero"`.
5. Criar a estrutura de coleções no Zotero (painel esquerdo, botão direito &gt; New Collection):

   ```
   TCC-Harness-SLM                (coleção raiz)
   ├── 01-Metodologicos           (Petersen, Kitchenham, Wohlin)
   ├── 03-Inspiracao              (surveys para leitura inicial)
   └── 02-Dominio                 (harness/SLM/avaliação — a pesquisa em questão)
   ```

### Como salvar os PDFs de uma coleção em uma pasta específica

O Zotero não configura uma pasta de anexos diferente para cada coleção. A forma
mais simples de copiar os PDFs de uma coleção para uma pasta do projeto é:

1. No Zotero, clique com o botão direito na coleção desejada, por exemplo
   `03-Inspiracao`, e escolha `Export Collection...`.
2. Escolha um formato de exportação que preserve os anexos, marque **Export Files**
   e confirme.
3. Selecione a pasta de destino, por exemplo `d:\repos\tcc_harnes\artigos\`.
4. Confira se os PDFs foram copiados e renomeie-os conforme a tabela de
   `artigos/README.md`, quando necessário.

Esse procedimento exporta uma cópia dos arquivos e mantém o Zotero como fonte de
verdade. Repita-o para `01-Metodologicos`, `03-Inspiracao` e `02-Dominio` conforme
for acumulando artigos. Para atualizar a pasta depois, exporte novamente a
coleção ou copie apenas os anexos novos.

#### Alternativa: arquivos vinculados

Se você quiser que os PDFs já sejam armazenados fora da biblioteca interna do
Zotero, configure `Editar > Configurações > Avançado > Arquivos e pastas > Diretório
base de anexos vinculados` e escolha uma pasta. Depois, adicione os PDFs como
**arquivos vinculados**. Essa opção não é a recomendada para o mini-harness, pois
o Connector normalmente cria anexos armazenados na biblioteca do Zotero; nesse
caso, prefira a exportação com **Export Files** acima.

## FASE 1 — Artigos de inspiração e fundamentos (ler antes de implementar)

Nesta fase, você reúne e lê os **7 artigos-âncora** que preparam o terreno antes da implementação do mini-harness. Diferente da busca por termos (Fase 2), aqui o processo é **busca dirigida por título/DOI**.

A Fase 1 divide-se em dois blocos complementares com a mesma estrutura de organização:
- **1A. Surveys de inspiração**: conceitos do domínio (SLM, agent harness, avaliação) para definir o escopo do mini-harness.
- **1B. Referências metodológicas**: diretrizes formais de revisão (mapeamento sistemático, SLR, snowballing) para estruturar o processo.

---

### Lista de Artigos da Fase 1

#### 1A. Surveys de inspiração (Coleção Zotero: `03-Inspiracao`)

- **sharma2025** — _Small Language Models for Agentic Systems: A Survey_ (Sharma & Mehta, 2025)
  - **Busca**: `Small Language Models for Agentic Systems Survey Sharma Mehta 2025`
  - **Foco**: Conecta SLMs, agentes e uso de ferramentas; leitura principal do tema.
- **meng2026harness** — _Agent Harness for Large Language Model Agents: A Survey_ (Meng et al., 2026)
  - **Busca**: `Agent Harness for Large Language Model Agents Survey Meng 2026`
  - **Foco**: Arquitetura, componentes e taxonomia de agent harness.
- **lu2025** — _Small Language Models: Survey, Measurements, and Insights_ (Lu et al., 2025)
  - **Busca**: `Small Language Models Survey Measurements Insights Lu 2025`
  - **Foco**: Capacidades, medições e limitações práticas de SLMs.

#### 1B. Referências metodológicas (Coleção Zotero: `01-Metodologicos`)

- **petersen2008** — _Systematic Mapping Studies in Software Engineering_ (Petersen et al., 2008)
  - **Busca**: `Systematic Mapping Studies in Software Engineering Petersen 2008 EASE`
  - **Foco**: Conceito original e as 5 fases do mapeamento sistemático.
- **petersen2015** — _Guidelines for conducting systematic mapping studies in software engineering: An update_ (Petersen et al., 2015)
  - **Busca**: `Guidelines for conducting systematic mapping studies software engineering update Petersen 2015`
  - **Foco**: Guia prático e atualizado para conduzir o mapeamento.
- **kitchenham2007** — _Guidelines for performing Systematic Literature Reviews in Software Engineering_ (Kitchenham & Charters, 2007)
  - **Busca**: `Kitchenham Charters Guidelines performing Systematic Literature Reviews Software Engineering EBSE-2007-01`
  - **Foco**: Protocolo, critérios de inclusão/exclusão, avaliação de qualidade e validade.
- **wohlin2014** — _Guidelines for snowballing in systematic literature studies_ (Wohlin, 2014)
  - **Busca**: `Wohlin Guidelines snowballing systematic literature studies EASE 2014`
  - **Foco**: Procedimento sistemático de busca por referências (*snowballing*).

---

### Passo a Passo de Importação (Fase 1A e 1B)

Para cada um dos 7 artigos acima, execute os passos a seguir:

#### Passo 1.1 — Localizar o artigo
Busque pelo título/autores no Google Scholar ou no portal de periódicos/acesso institucional da sua universidade.

#### Passo 1.2 — Importar no Zotero e organizar na coleção
Importe via **Zotero Connector**, **Adicionar por Identificador (DOI)** ou **Manual**. Em seguida, mova o item para a coleção correspondente:
- Artigos **1A** (Surveys) → Coleção `03-Inspiracao`
- Artigos **1B** (Metodológicos) → Coleção `01-Metodologicos`

#### Passo 1.3 — Salvar o PDF localmente e atualizar o rastreamento
Exporte a coleção ou salve o PDF na pasta `artigos/` com o nome indicado no `artigos/README.md`. Marque o status como `✅ baixado` no README.

#### Passo 1.4 — Checar e fixar o Citation Key (Better BibTeX)
No Zotero, clique com o botão direito no item → `Better BibTeX Key... > Pin key` e garanta que a chave bate com a tabela (`sharma2025`, `meng2026harness`, `petersen2015`, etc.).

---

## FASE 2 — Artigos da pesquisa em questão (domínio harness/SLM)

Diferente da Fase 1, aqui a busca é **sistemática por termos** (as strings de busca da seção final de [arquitetura_mini_harness_bibliografico.md](arquitetura_mini_harness_bibliografico.md)).

### Passo 2.1 — Monte as strings de busca por bloco

Os termos já estão organizados em 4 blocos combináveis:

- **Bloco A (harness/agente):** "harness engineering", "agent harness", "LLM harness", "evaluation harness", "agentic AI", "LLM agent", "tool-use"/"tool calling", "planner generator evaluator", "LLM-as-judge", "agent evaluation"
- **Bloco B (modelos pequenos):** "small language model\*", SLM, "on-device", "edge LLM", "efficient inference", "quantization"/"quantized", "knowledge distillation", "parameter-efficient", LoRA, "sub-billion", "7B"/"3B"/"1B"
- **Bloco C (avaliação simples):** "benchmark", "pass@k", "exact match", "rubric", "automatic evaluation", "reproducib\*", "low-cost evaluation", "lightweight evaluation"
- **Bloco D (revisão/mapeamento):** "systematic literature review", "systematic mapping", "survey", "scoping review", "bibliometric"

String-exemplo combinada (já pronta para colar nos buscadores):

```
("small language model*" OR "SLM" OR "on-device" OR "edge LLM")
AND ("agent*" OR "harness" OR "tool-use" OR "tool calling" OR "LLM-as-judge")
AND ("evaluation" OR "benchmark" OR "reproducib*")
```

### Passo 2.2 — Rode a busca nas fontes gratuitas (nesta ordem)

1. **arXiv** (https://arxiv.org/search) — cole os termos do Bloco A+B, sem chave de API.
2. **Semantic Scholar** (https://www.semanticscholar.org/search) — repita a busca; ótimo para achar citações e "papers similares" (snowballing, Wohlin 2014).
3. **Google Scholar** — para achar artigos fora do arXiv/Semantic Scholar (workshops, revistas menores).

Anote (ex.: numa aba do próprio Zotero ou num rascunho) quantos resultados cada combinação de blocos retornou — isso vira o registro do "search string used" que o Kitchenham & Charters exige no protocolo.

### Passo 2.3 — Triagem título/resumo (critério de inclusão humano)

Antes de importar, leia título + resumo de cada resultado e decida incluir/excluir (é você o "critério humano de seleção" — seção 6.0 do planejamento). Critério mínimo:

- Trata de harness/avaliação de agentes OU de modelos pequenos (SLM) — pelo menos um dos dois.
- Tem relação com viabilidade prática (reprodutibilidade, custo, hardware modesto) OU é uma survey/mapeamento (Bloco D) que ajuda a mapear o campo.
- Exclua: só menciona os termos de passagem, sem contribuição própria ao tema.

### Passo 2.4 — Importar os aprovados no Zotero

Mesmo processo da Fase 1 (Connector é o mais rápido para lotes vindos de arXiv/Semantic Scholar — a maioria das páginas de resultado do arXiv permite selecionar vários itens de uma vez no Connector). Arraste cada item aprovado para a coleção `02-Dominio`.

### Passo 2.5 — Deduplicar

No Zotero: `Minha Biblioteca > Itens duplicados` (painel esquerdo) — revise e mescle duplicatas (o mesmo paper pode aparecer no arXiv e no Semantic Scholar).

### Passo 2.6 — Tags por bloco (prepara o keywording da fase 4 de Petersen)

Para cada item importado, adicione uma tag indicando de qual bloco ele veio (ex.: `bloco-A`, `bloco-B`, `bloco-C`, `bloco-D`) — isso acelera o keywording automático que o mini-harness fará depois (seção 2.1/3.6 do planejamento).

### Passo 2.7 — Salvar PDFs localmente e atualizar rastreamento

1. Exporte a coleção `02-Dominio` para `artigos/` conforme a seção "Como salvar os PDFs de uma coleção em uma pasta específica" e use o padrão de nome `Sobrenome_Ano_Titulo_Curto.pdf` (mesmo padrão da tabela existente).
2. Adicione uma nova linha na tabela "Referências — Domínio" do artigos/README.md para cada novo artigo (chave, autor/ano, título, fonte, arquivo esperado, status).

---

## 3. Organização sistemática no Zotero (resumo de convenções)

| Elemento | Convenção |
| --- | --- |
| Coleção raiz | `TCC-Harness-SLM` — é o "escopo" que o harness lê |
| Subcoleção | `01-Metodologicos` / `03-Inspiracao` / `02-Dominio` — separa método, leitura inicial e busca por termos |
| Citation key | `sobrenomeAno` (ex.: `petersen2008`), fixado via Better BibTeX (`Pin key`) |
| Tags | `bloco-A/B/C/D` (origem da busca) + tags livres que surgirem na leitura |
| Duplicatas | Resolver sempre em `Itens duplicados` antes de rodar o harness |
| PDF anexado | Sempre anexar o PDF ao item (o parser Docling/GROBID lê esse anexo) |

## 4. Checklist final antes de rodar o mini-harness

- [ ] 4 artigos metodológicos importados em `01-Metodologicos`, com PDF anexado.

- [ ] Artigos de domínio (busca por termos) importados em `02-Dominio`, sem duplicatas.

- [ ] Todos os itens têm citation key fixada (Better BibTeX).

- [ ] `artigos/README.md` atualizado (status `✅ baixado` em todas as linhas relevantes).

- [ ] Local API do Zotero habilitada (para o harness ler a coleção depois).

Com isso, a Fase 0 (Preparação do corpus) do plano de implementação (seção 8 do planejamento) está concluída e o corpus está pronto para o Loader do Zotero.