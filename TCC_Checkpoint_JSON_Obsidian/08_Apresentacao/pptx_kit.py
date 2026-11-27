"""Utilitários de layout (python-pptx) usados por gerar_apresentacao.py."""

from __future__ import annotations

import datetime as _dt
import io
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

NAVY = RGBColor(0x1B, 0x3A, 0x6B)
ACCENT = RGBColor(0xC0, 0x58, 0x0E)
INK = RGBColor(0x1F, 0x29, 0x33)
MUTED = RGBColor(0x5B, 0x67, 0x75)
LIGHT = RGBColor(0xEE, 0xF2, 0xF8)
LIGHT2 = RGBColor(0xF2, 0xF4, 0xF7)
ACCENT_LIGHT = RGBColor(0xFF, 0xF4, 0xE5)
GREEN_LIGHT = RGBColor(0xED, 0xF5, 0xEF)
GREEN = RGBColor(0x2E, 0x7D, 0x4F)
LINE = RGBColor(0xC9, 0xD3, 0xE0)
GANTT = RGBColor(0x5B, 0x9B, 0xD5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

MX = 0.6
CW = 12.133
SLIDE_W = 13.333
SLIDE_H = 7.5
FOOTER_TEXT = "Guilherme H. S. Lopes · Projeto de TCC · Sistemas de Informação — UNITINS"
WPM = 130
LIMIT_S = 18 * 60

_ANCHOR = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}
_ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT, None: None}
_TOKEN = re.compile(r"\*\*|~~|_\{([^}]*)\}|\^\{([^}]*)\}")


class P:
    """Parágrafo com opções próprias (sobrepõem os padrões do bloco)."""

    def __init__(self, text: str, **kw):
        self.text = text
        self.kw = kw


def _segments(s: str, markup: bool = True):
    if not markup:
        return [(s, False, False, 0)]
    out, bold, ital, pos = [], False, False, 0
    for m in _TOKEN.finditer(s):
        if m.start() > pos:
            out.append((s[pos:m.start()], bold, ital, 0))
        tok = m.group(0)
        if tok == "**":
            bold = not bold
        elif tok == "~~":
            ital = not ital
        elif m.group(1) is not None:
            out.append((m.group(1), bold, ital, -25000))
        else:
            out.append((m.group(2), bold, ital, 30000))
        pos = m.end()
    if pos < len(s):
        out.append((s[pos:], bold, ital, 0))
    return out


def _para(p, text, *, size=16, color=INK, font="Calibri", bold=False, italic=False,
          align=None, space_after=6, space_before=0, line_spacing=None, bullet=False,
          level=0, bullet_color=ACCENT, markup=True, lang="pt-BR"):
    if isinstance(align, str) or align is None:
        align = _ALIGN[align]
    if align is not None:
        p.alignment = align
    if line_spacing:
        p.line_spacing = line_spacing
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if bullet:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(int(Inches(0.28 + 0.3 * level))))
        pPr.set("indent", str(int(-Inches(0.22))))
        bu_clr = etree.SubElement(pPr, qn("a:buClr"))
        etree.SubElement(bu_clr, qn("a:srgbClr")).set("val", str(bullet_color))
        bu_font = etree.SubElement(pPr, qn("a:buFont"))
        bu_font.set("typeface", "Arial")
        etree.SubElement(pPr, qn("a:buChar")).set("char", "•" if level == 0 else "–")
    for seg, b, i, base in _segments(text, markup):
        for k, part in enumerate(seg.split("\n")):
            if k:
                p.add_line_break()
            if not part:
                continue
            r = p.add_run()
            r.text = part
            f = r.font
            f.size = Pt(size)
            f.name = font
            f.bold = bold or b
            f.italic = italic or i
            f.color.rgb = color
            rPr = r._r.get_or_add_rPr()
            rPr.set("lang", lang)
            if base:
                rPr.set("baseline", str(base))
    # Sem isto, parágrafos vazios (ex.: células do Gantt) herdam 18 pt e aumentam a linha.
    p._p.get_or_add_endParaRPr().set("sz", str(int(size * 100)))


def fill(tf, items, **defaults):
    base = dict(size=16, color=INK, font="Calibri", space_after=6, bullet=False,
                level=0, bullet_color=ACCENT)
    base.update(defaults)
    if isinstance(items, (str, P)):
        items = [items]
    for idx, it in enumerate(items):
        kw = dict(base)
        if isinstance(it, P):
            kw.update(it.kw)
            t = it.text
        else:
            t = it
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        _para(p, t, **kw)


def text(slide, x, y, w, h, items, anchor="top", margin=0.05, **kw):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    m = Inches(margin)
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = m
    tf.vertical_anchor = _ANCHOR[anchor]
    fill(tf, items, **kw)
    return tb


def rect(slide, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def B(*items, **kw):
    """Itens com marcador."""
    return [P(t, bullet=True, **kw) for t in items]


def S(*items, **kw):
    """Subitens (segundo nível de marcador)."""
    return [P(t, bullet=True, level=1, **kw) for t in items]


def bullets(slide, items, y=1.6, h=None, x=MX, w=CW, size=20, space_after=10, **kw):
    """Corpo padrão do slide: lista em coluna única (str vira marcador; P mantém opções)."""
    h = (6.92 - y) if h is None else h
    its = [it if isinstance(it, P) else P(it, bullet=True) for it in items]
    return text(slide, x, y, w, h, its, size=size, space_after=space_after, **kw)


def heading(t, size=18, space_before=0):
    """Subtítulo de texto dentro da lista (sem caixa)."""
    return P(t, bold=True, color=ACCENT, size=size, space_before=space_before, space_after=4)


def caption(slide, y, label, x=MX, w=CW, size=14, h=0.36, align=None):
    """Título de quadro, tabela ou figura, acima do elemento, como no artigo."""
    return text(slide, x, y, w, h, f"**{label}**", size=size, align=align, space_after=0)


def fonte(slide, y, txt="Fonte: elaborado pelo autor (2026).", x=MX, w=CW, size=11):
    return text(slide, x, y, w, 0.3, txt, size=size, color=MUTED, space_after=0)


def equation(slide, y, h, items, size=32, x=MX, w=CW, **kw):
    """Equação como texto centralizado, sem caixa."""
    return text(slide, x, y, w, h, items, size=size, font="Cambria Math", color=NAVY,
                align="center", anchor="middle", space_after=4, **kw)


def _borders(cell, color=LINE, width_pt=0.75):
    tcPr = cell._tc.get_or_add_tcPr()
    for i, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        ln = etree.Element(qn(tag), {"w": str(int(Pt(width_pt))), "cap": "flat",
                                     "cmpd": "sng", "algn": "ctr"})
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr")).set("val", str(color))
        etree.SubElement(ln, qn("a:prstDash")).set("val", "solid")
        tcPr.insert(i, ln)


def add_table(slide, x, y, rows, col_w, header_rows=1, size=12, merges=(),
              row_h=0.3, font="Calibri"):
    """rows: lista de linhas; célula = str | lista | dict(t, fill, color, bold, size,
    align, font, markup)."""
    nr, nc = len(rows), len(col_w)
    heights = row_h if isinstance(row_h, (list, tuple)) else [row_h] * nr
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(col_w)),
                                Inches(sum(heights)))
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    for c, w in enumerate(col_w):
        tbl.columns[c].width = Inches(w)
    for r, h in enumerate(heights):
        tbl.rows[r].height = Inches(h)
    for r1, c1, r2, c2 in merges:
        tbl.cell(r1, c1).merge(tbl.cell(r2, c2))
    for r, row in enumerate(rows):
        for c in range(nc):
            cell = tbl.cell(r, c)
            spec = row[c] if c < len(row) else ""
            if not isinstance(spec, dict):
                spec = {"t": spec}
            hdr = r < header_rows
            zebra = WHITE if (r - header_rows) % 2 == 0 else LIGHT2
            cell.fill.solid()
            cell.fill.fore_color.rgb = spec.get("fill", NAVY if hdr else zebra)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            if cell.is_spanned:
                cell.text_frame.paragraphs[0]._p.get_or_add_endParaRPr().set(
                    "sz", str(int(size * 100)))
            else:
                tf = cell.text_frame
                tf.word_wrap = True
                t = spec.get("t", "")
                fill(tf, t if isinstance(t, list) else [t], size=spec.get("size", size),
                     color=spec.get("color", WHITE if hdr else INK),
                     bold=spec.get("bold", hdr), align=spec.get("align"),
                     font=spec.get("font", font), markup=spec.get("markup", True),
                     space_after=spec.get("space_after", 0))
            _borders(cell)
    return gf


# ----------------------------------------------------------------- imagens ---

_IMG_RATIOS = (("logo", 5.5), ("fig2", 2.44), ("fig1", 1.34))


def load_images(docx: Path) -> dict:
    found = {}
    with zipfile.ZipFile(docx) as z:
        for name in sorted(z.namelist()):
            if not name.startswith("word/media/"):
                continue
            data = z.read(name)
            try:
                w, h = Image.open(io.BytesIO(data)).size
            except Exception:
                continue
            ratio = w / h
            for key, target in _IMG_RATIOS:
                if key not in found and abs(ratio - target) / target < 0.12:
                    found[key] = (data, w, h)
                    break
    missing = [k for k, _ in _IMG_RATIOS if k not in found]
    if missing:
        raise SystemExit(f"Imagens não encontradas no .docx: {missing}")
    return found


def add_image(slide, imgs, key, x, y, w=None, h=None):
    data, pw, ph = imgs[key]
    if w is not None and h is not None:
        scale = min(w / pw, h / ph)
        w, h = pw * scale, ph * scale
    elif w is not None:
        h = w * ph / pw
    else:
        w = h * pw / ph
    return slide.shapes.add_picture(io.BytesIO(data), Inches(x), Inches(y), Inches(w),
                                    Inches(h))


# ---------------------------------------------------------- deck + roteiro ---

_NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
_RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
_CT = "application/vnd.openxmlformats-officedocument.presentationml."


def _mmss(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def _words(s: str) -> int:
    return len(re.findall(r"\S+", s))


class Deck:
    def __init__(self, imgs):
        self.prs = Presentation()
        self.prs.slide_width = Inches(SLIDE_W)
        self.prs.slide_height = Inches(SLIDE_H)
        self.imgs = imgs
        self.refs: dict[str, str] = {}
        self.slides: list[dict] = []
        self.appendix: list[tuple[str, str, int]] = []

    # ---- criação -------------------------------------------------------
    def new(self, key, tag=None, title=None, code=None, footer=True, title_size=28):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        n = len(self.prs.slides)
        self.refs[key] = f"{code} (slide {n})" if code else f"slide {n}"
        if code:
            self.appendix.append((code, title or "", n))
        if tag:
            text(s, MX, 0.25, CW, 0.32, (f"{code} · " if code else "") + tag.upper(),
                 size=12, bold=True, color=ACCENT, space_after=0)
        if title:
            text(s, MX, 0.55, CW, 0.85, title, size=title_size, bold=True, color=NAVY,
                 anchor="middle", space_after=0)
        if footer:
            rect(s, MX, 7.02, CW, 0.012, LINE)
            text(s, MX, 7.06, 9.5, 0.3, FOOTER_TEXT, size=10, color=MUTED, space_after=0)
            num = f"{code} · {n}" if code else str(n)
            text(s, MX + CW - 2.0, 7.06, 2.0, 0.3, num, size=10, color=MUTED,
                 align="right", space_after=0)
        self.slides.append({"slide": s, "n": n, "key": key, "code": code})
        return s

    def img(self, slide, key, x, y, w=None, h=None):
        return add_image(slide, self.imgs, key, x, y, w, h)

    def _meta(self, slide):
        return next(m for m in self.slides if m["slide"] is slide)

    def script(self, slide, objetivo, fala, transicao="", corte="", pontos=(), extra=()):
        self._meta(slide).update(kind="main", objetivo=objetivo, fala=fala,
                                 transicao=transicao, corte=corte, pontos=list(pontos),
                                 extra=list(extra))

    def apoio(self, slide, pontos):
        self._meta(slide).update(kind="apoio", pontos=list(pontos))

    # ---- comentários legados --------------------------------------------
    def _comment_parts(self, items):
        pkg = self.prs.part.package
        authors = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   f'<p:cmAuthorLst xmlns:p="{_NS_P}"><p:cmAuthor id="1" '
                   f'name="Roteiro de apresentação" initials="RA" lastIdx="{len(items)}" '
                   f'clrIdx="0"/></p:cmAuthorLst>')
        part = Part(PackURI("/ppt/commentAuthors.xml"), _CT + "commentAuthors+xml", pkg,
                    authors.encode("utf-8"))
        self.prs.part.relate_to(part, _RT + "commentAuthors")
        now = _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000")
        for idx, (slide, body) in enumerate(items, start=1):
            xml = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   f'<p:cmLst xmlns:p="{_NS_P}"><p:cm authorId="1" dt="{now}" idx="{idx}">'
                   f'<p:pos x="10" y="10"/><p:text>{escape(body)}</p:text></p:cm></p:cmLst>')
            cpart = Part(PackURI(f"/ppt/comments/comment{idx}.xml"), _CT + "comments+xml",
                         pkg, xml.encode("utf-8"))
            slide.part.relate_to(cpart, _RT + "comments")

    # ---- finalização ------------------------------------------------------
    def finalize(self, extra_fn=None):
        """extra_fn(main) -> {chave_do_slide: [linhas extras das anotações]}."""
        main = [m for m in self.slides if m.get("kind") == "main"]
        acc = 0.0
        for m in main:
            m["t"] = (_words(m["fala"]) + _words(m["transicao"])) / WPM * 60 + 3
            acc += m["t"]
            m["acc"] = acc
        total = acc
        extra_by_key = extra_fn(main) if extra_fn else {}
        comments = []
        for m in self.slides:
            kind = m.get("kind")
            notes = m["slide"].notes_slide.notes_text_frame
            if kind == "main":
                lines = [f"⏱ TEMPO PREVISTO {_mmss(m['t'])} | ACUMULADO {_mmss(m['acc'])} "
                         f"/ 18:00",
                         f"OBJETIVO: {m['objetivo']}", "", "FALA SUGERIDA:", m["fala"]]
                if m["transicao"]:
                    lines += ["", f"TRANSIÇÃO → {m['transicao']}"]
                if m["corte"]:
                    lines += ["", f"SE O TEMPO APERTAR: {m['corte']}"]
                for e in m["extra"] + list(extra_by_key.get(m["key"], [])):
                    lines += ["", e]
                notes.text = "\n".join(lines)
                body = [f"Roteiro · {_mmss(m['t'])} (acumulado {_mmss(m['acc'])})"]
                body += [f"• {p}" for p in m["pontos"]]
                if m["transicao"]:
                    body.append(f"→ {m['transicao']}")
                comments.append((m["slide"], "\n".join(body)))
            elif kind == "apoio":
                code = m["code"] or ""
                lines = [f"APÊNDICE {code} — conteúdo de apoio (fora dos 18 min).",
                         "Use apenas se a banca pedir detalhes sobre este ponto.", "",
                         "Pontos para explicar:"] + [f"• {p}" for p in m["pontos"]]
                notes.text = "\n".join(lines)
                comments.append((m["slide"], "\n".join(
                    [f"Apoio {code} · fora dos 18 min"] + [f"• {p}" for p in m["pontos"]])))
        self._comment_parts(comments)
        return main, total

    def time_map(self, main) -> list[str]:
        return [f"{m['n']:>2}  {_mmss(m['t']):>5}  acum. {_mmss(m['acc']):>5}" for m in main]

    def save(self, path: Path):
        self.prs.save(str(path))


__all__ = [n for n in dir() if not n.startswith("_") or n in ("_mmss", "_words")]
