"""Gera a apresentação do projeto de TCC I e o arquivo de perguntas para treino.

Uso: python gerar_apresentacao.py [caminho/do/artigo.docx]

As figuras 1 e 2 e o logotipo são lidos do próprio .docx do artigo. Saídas, nesta pasta:
- Apresentacao_TCC_I_Guilherme_Lopes.pptx (roteiro nas anotações e nos comentários);
- perguntas_banca_treino.md (perguntas para treinar a arguição).
"""

from __future__ import annotations

import sys
from pathlib import Path

from perguntas_banca import write_md
from pptx_kit import LIMIT_S, Deck, _mmss, load_images
from slides_apendice_b import build_apendice
from slides_principais_a import build_a
from slides_principais_b import build_b
from slides_principais_c import build_c

HERE = Path(__file__).resolve().parent
OUT_PPTX = HERE / "Apresentacao_TCC_I_Guilherme_Lopes.pptx"
OUT_MD = HERE / "perguntas_banca_treino.md"


def find_docx() -> Path:
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.exists():
            raise SystemExit(f"Arquivo não encontrado: {p}")
        return p
    default = HERE.parent / "artigo_tcc_unitins_corrigido (1).docx"
    if default.exists():
        return default
    cands = sorted(HERE.parent.glob("artigo_tcc_unitins*.docx"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not cands:
        raise SystemExit("Nenhum artigo_tcc_unitins*.docx encontrado; informe o caminho.")
    return cands[0]


CHECKPOINTS = (("pergunta", "Pergunta de pesquisa"), ("revisao", "Revisão sistemática"),
               ("quadro6", "Quadro 6"), ("resultados", "Resultados esperados"),
               ("consideracoes", "Considerações finais"))


def extras(main):
    total = main[-1]["acc"]
    mapa = [f"MAPA DE TEMPO (fala a 130 palavras/min + 3 s por slide) — total {_mmss(total)} "
            f"de {_mmss(LIMIT_S)}:"]
    mapa += [f"  slide {m['n']:>2}: {_mmss(m['t'])} (acumulado {_mmss(m['acc'])})"
             for m in main]
    by_key = {m["key"]: m for m in main}
    nav = ("NAVEGAÇÃO: no Modo do Apresentador, digite o número do slide e tecle Enter para "
           "abrir um apêndice durante a arguição; digite "
           f"{by_key['obrigado']['n']} e Enter para voltar ao encerramento.")
    marcos = "; ".join(f"{lab} (slide {by_key[k]['n']}) até {_mmss(by_key[k]['acc'] - by_key[k]['t'])}"
                       for k, lab in CHECKPOINTS if k in by_key)
    return {"capa": ["\n".join(mapa), nav,
                     f"MARCOS DE TEMPO — comece cada slide até: {marcos}. Se estiver mais de "
                     "1 min atrasado, use as dicas 'SE O TEMPO APERTAR'."]}


def main():
    docx = find_docx()
    deck = Deck(load_images(docx))
    build_a(deck)
    build_b(deck)
    build_c(deck)
    build_apendice(deck)
    main_slides, total = deck.finalize(extras)
    deck.save(OUT_PPTX)
    write_md(OUT_MD, deck.refs)
    print(f"Artigo: {docx.name}")
    print("\n".join(deck.time_map(main_slides)))
    print(f"Total previsto: {_mmss(total)} (limite {_mmss(LIMIT_S)}) · "
          f"{len(deck.prs.slides)} slides ({len(main_slides)} principais)")
    print(f"PPTX: {OUT_PPTX}\nMD:   {OUT_MD}")


if __name__ == "__main__":
    main()
