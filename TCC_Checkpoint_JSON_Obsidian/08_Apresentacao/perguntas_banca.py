"""Gera o .md de perguntas prováveis da banca, para treinar as respostas.

As perguntas ficam em perguntas_dados_a/b/c.py; aqui elas são numeradas, os slides de apoio
são resolvidos a partir de Deck.refs e os pontos de atenção (⚠️) são reunidos no final.
"""

from __future__ import annotations

from pathlib import Path

from perguntas_dados_a import GRUPOS_A
from perguntas_dados_b import GRUPOS_B
from perguntas_dados_c import GRUPOS_C
from referencias import REFS

GRUPOS = GRUPOS_A + GRUPOS_B + GRUPOS_C
REFS_POR_SLIDE = 13  # deve acompanhar referencias.slides_apendice

NUMEROS = [
    ("Escritores", "3 representantes de ~0,6B: Qwen3-0.6B, T5Gemma B-B PrefixLM-IT e "
                   "Qwen3-0.6B BD3LM"),
    ("Juiz", "Gemma 3 1B Instruct, GGUF Q4_K_M, local, pico de memória residente ≤ 4 GiB"),
    ("Orçamentos", "saída ≤ 1.200 *tokens* por transição; contexto de entrada ≤ 8.192 *tokens*"),
    ("Protocolo", "6 regras no *prompt-base*; 9 etapas no *harness*; 3 métricas primárias; "
                  "α = 0,05"),
    ("Fases", "Fase 0: 15 transições sintéticas; Fase 1: 25 entidades; Fase 2: partição de "
              "avaliação completa"),
    ("Busca", "arXiv (título e resumo), 01/07/2025 a 19/11/2026; 8 consultas (905 registros "
              "somados); 12 estudos de controle"),
    ("Funil", "738 únicos → 696 após termos → 189 na elegibilidade → 12 no núcleo"),
    ("Triagem", "claude-haiku-5.5 via GitHub Copilot SDK 1.0.31; lotes de 20; 36 requisições, "
                "38 créditos (teto 150)"),
    ("Elegibilidade", "189 requisições, ~191 créditos (teto 400); 185 HTML + 4 PDF; até 100 mil "
                      "caracteres; trechos de 20 a 400 caracteres; corte de 4,5B"),
    ("Artefatos", "repositório público da revisão v2.1.0; *scripts* em C# (.NET 10); "
                  "*hashes* SHA-256"),
    ("*Hardware*", "Intel Core i5 de 10ª geração, 24 GB de RAM, NVIDIA GeForce GTX 1650"),
    ("Cronograma", "15 atividades em 20 quinzenas: TCC I Q1–Q10 (ago.–dez./2026); TCC II "
                   "Q11–Q20 (fev.–jun./2027)"),
]

DEFINICOES = [
    ("*Checkpoint* JSON", "estado persistente da entidade, `{\"state\": {\"chave\": \"valor\"}}`, "
                          "regenerado a cada turno"),
    ("GU-JSON", "*Generate-Update* em JSON: $M_t = G(S, M_{t-1}, O_t)$, com reescrita integral"),
    ("Escritor de memória", "modelo $G$ que produz o novo *checkpoint* (*memory writer*)"),
    ("$M^*_{t-1}$, $O_t$, $M^*_t$", "estado de referência anterior, parágrafo do turno e estado "
                                    "esperado"),
    ("PRESERVE / ADD / UPDATE", "manter atributo inalterado / incluir atributo novo / integrar "
                                "complemento ou nova perspectiva"),
    ("JSON Validity / Schema Validity", "saída lida por `json.loads` sem reparo / só o objeto "
                                        "raiz `state` com chaves e valores textuais"),
    ("State P, R e F1", "precisão, revocação e média harmônica sobre pares caminho-valor"),
    ("Hallucination Rate", "pares gerados sem correspondência esperada e sem suporte na entrada "
                           "ou nas anotações"),
    ("PA / UA", "acurácia de preservação (PRESERVE) / de atualização (ADD e UPDATE)"),
    ("Condicional / global", "só transições válidas / falha estrutural conta como zero"),
    ("Estrito / híbrido", "só correspondência normalizada / inclui equivalências aceitas pelo "
                          "juiz"),
    ("*Zero-shot*, *prompt-only*", "sem exemplos no *prompt* e sem decodificação restrita"),
    ("Decodificação restrita", "filtra *tokens* inválidos por gramática durante a geração"),
    ("BD3LM", "difusão em blocos: blocos em sequência, remoção de ruído paralela dentro do bloco"),
    ("GGUF / Q4_K_M", "formato de pesos para execução local / quantização de ~4 bits por peso"),
    ("Friedman", "compara 3+ modelos nas mesmas unidades pelos postos médios"),
    ("Wilcoxon pareado", "compara 2 modelos pelos postos das diferenças pareadas"),
    ("Holm-Bonferroni", "ajuste sequencial dos valores p para comparações múltiplas"),
]


def _ref_part(ref_key: str) -> str:
    keys = [k for k, _ in REFS]
    if ref_key not in keys:
        raise KeyError(f"Referência desconhecida: {ref_key}")
    return f"refs_{keys.index(ref_key) // REFS_POR_SLIDE + 1}"


def _apoio(keys, refs):
    out = []
    for k in keys:
        if k.startswith("@"):
            out.append(f"{refs[_ref_part(k[1:])]} (referência)")
        elif k in refs:
            out.append(refs[k])
        else:
            raise KeyError(f"Chave de slide desconhecida em perguntas: {k}")
    return " · ".join(out)


def _quote(lines):
    return [("> " + ln) if ln else ">" for ln in lines]


def _pergunta(num, item, refs):
    marca = "⚠️ " if item["alerta"] else ""
    corpo = [f"**Resposta direta:** {item['r']}"]
    if item["ev"]:
        corpo += [""] + [f"- {e}" for e in item["ev"]]
    if item["lim"]:
        corpo += ["", f"**Limite:** {item['lim']}"]
    if item["alerta"]:
        corpo += ["", "> [!warning] Preparar", f"> {item['alerta']}"]
    linhas = [f"### {num} {marca}{item['p']}", "", "> [!tip]- Pontos-chave"]
    linhas += _quote(corpo)
    linhas += ["", f"**Apoio:** {_apoio(item['apoio'], refs)}", ""]
    return linhas


def build_md(refs: dict[str, str]) -> str:
    total = sum(len(itens) for _, itens in GRUPOS)
    n_alerta = sum(1 for _, itens in GRUPOS for it in itens if it["alerta"])
    out = [
        "---",
        'title: "Perguntas da banca — treino da arguição"',
        "aliases:",
        '  - "perguntas banca treino"',
        "tags:",
        "  - tcc",
        "  - apresentacao",
        "status: draft",
        "---",
        "",
        "# Perguntas da banca — treino da arguição",
        "",
        f"{total} perguntas prováveis, em {len(GRUPOS)} grupos, com base no artigo do TCC I. "
        "Arquivo gerado por `gerar_apresentacao.py`; edite as perguntas em "
        "`perguntas_dados_*.py`.",
        "",
        "## Como treinar",
        "",
        "1. Leia a pergunta e responda **em voz alta, em até 1 minuto**, nesta ordem: "
        "**resposta direta → evidência do trabalho → limite**.",
        "2. Só então abra **Pontos-chave** e compare.",
        "3. Se a resposta pedir detalhe, abra o slide indicado em **Apoio**: no Modo do "
        "Apresentador, digite o número do slide e tecle Enter; para voltar ao encerramento, "
        f"digite {refs['obrigado'].split()[-1]} e Enter.",
        f"4. Os {n_alerta} itens marcados com ⚠️ são pontos fracos ou informações que o artigo "
        "não traz; a lista no final reúne o que preparar ou corrigir antes da banca.",
        "",
        "## Grupos",
        "",
    ]
    # Títulos de grupo sem itálico, para que os links [[#...]] do Obsidian resolvam.
    nomes = [nome.replace("*", "") for nome, _ in GRUPOS]
    out += [f"{i}. [[#{i}. {nome}|{nome}]] ({len(itens)})"
            for i, (nome, (_, itens)) in enumerate(zip(nomes, GRUPOS), 1)]
    alertas = []
    for i, (nome, (_, itens)) in enumerate(zip(nomes, GRUPOS), 1):
        if out[-1] != "":
            out.append("")
        out += [f"## {i}. {nome}", ""]
        for j, item in enumerate(itens, 1):
            num = f"{i}.{j}"
            out += _pergunta(num, item, refs)
            if item["alerta"]:
                alertas.append((num, item))
    out += ["## Números para ter na ponta da língua", "", "| Tema | Valor |", "| --- | --- |"]
    out += [f"| {a} | {b} |" for a, b in NUMEROS]
    out += ["", "## Definições rápidas", "", "| Termo | Definição |", "| --- | --- |"]
    out += [f"| {a} | {b} |" for a, b in DEFINICOES]
    out += ["", "## ⚠️ Pontos a preparar ou corrigir antes da banca", ""]
    out += [f"- **{num}** {it['p']} — {it['alerta']}" for num, it in alertas]
    out.append("")
    return "\n".join(out)


def write_md(path, refs: dict[str, str]) -> None:
    Path(path).write_text(build_md(refs), encoding="utf-8")
