"""Gera as Figuras 1 e 2 da Seção 3.7 (SVG editável + PNG).

Uso: python gerar_figuras_harness.py
O PNG é renderizado com Chrome/Edge headless, se encontrado.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent

FONT = "Arial, Helvetica, sans-serif"
MONO = "Consolas, 'Courier New', monospace"
INK = "#172533"
LINE = "#263544"
STROKE = "#33495a"
BLUE = "#edf3f8"
GRAY = "#f3f4f6"
GREEN = "#edf5ef"
ACCENT_FILL = "#fff4e5"
ACCENT = "#b45309"
REGION = "#f7fafc"


def var(base: str, sub: str = "", star: bool = False) -> tuple:
    return ("var", base, sub, star)


def rich(parts, size: int) -> str:
    """Monta tspans com sobrescrito '*' e subscrito, voltando à linha de base."""
    out, offset = [], 0.0
    small = round(size * 0.68)
    for part in parts:
        if isinstance(part, str):
            dy = -offset
            offset = 0.0
            attr = f' dy="{dy:.1f}"' if dy else ""
            out.append(f"<tspan{attr}>{escape(part)}</tspan>")
            continue
        _, base, sub, star = part
        dy = -offset
        offset = 0.0
        attr = f' dy="{dy:.1f}"' if dy else ""
        out.append(f'<tspan font-style="italic"{attr}>{escape(base)}</tspan>')
        if star:
            up = -0.38 * size
            out.append(f'<tspan font-size="{small}" dy="{up:.1f}">*</tspan>')
            offset += up
        if sub:
            down = 0.25 * size - offset
            dx = -0.28 * small if star else 0
            dx_attr = f' dx="{dx:.1f}"' if dx else ""
            out.append(f'<tspan font-size="{small}" font-style="italic" dy="{down:.1f}"{dx_attr}>{escape(sub)}</tspan>')
            offset += down
    if offset:
        out.append(f'<tspan dy="{-offset:.1f}"> </tspan>')
    return "".join(out)


class Svg:
    def __init__(self, width: int, height: int, title: str, desc: str):
        self.w, self.h = width, height
        self.body: list[str] = []
        self.head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'  <title id="title">{escape(title)}</title>\n'
            f'  <desc id="desc">{escape(desc)}</desc>\n'
            '  <defs>\n'
            f'    <marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 L12 6 L0 12 Z" fill="{LINE}"/></marker>\n'
            '  </defs>\n'
            f'  <rect width="{width}" height="{height}" fill="#ffffff"/>\n'
        )

    def add(self, s: str) -> None:
        self.body.append("  " + s)

    def rect(self, x, y, w, h, fill=GRAY, stroke=STROKE, dash=False, sw=2, rx=8):
        d = ' stroke-dasharray="10 7"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def diamond(self, cx, cy, hw, hh, fill=GRAY):
        pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
        self.add(f'<polygon points="{pts}" fill="{fill}" stroke="{STROKE}" stroke-width="2"/>')

    def cylinder(self, x, y, w, h, fill=BLUE):
        ry = 16
        self.add(
            f'<path d="M{x} {y + ry} A{w / 2} {ry} 0 0 1 {x + w} {y + ry} V{y + h - ry} '
            f'A{w / 2} {ry} 0 0 1 {x} {y + h - ry} Z" fill="{fill}" stroke="{STROKE}" stroke-width="2"/>'
        )
        self.add(f'<path d="M{x} {y + ry} A{w / 2} {ry} 0 0 0 {x + w} {y + ry}" fill="none" stroke="{STROKE}" stroke-width="2"/>')

    def text(self, x, y, content, size=22, bold=False, anchor="start", mono=False, italic=False, color=INK):
        weight = ' font-weight="700"' if bold else ""
        style = ' font-style="italic"' if italic else ""
        family = MONO if mono else FONT
        body = rich(content, size) if isinstance(content, list) else escape(content)
        self.add(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}"{weight}{style} '
            f'text-anchor="{anchor}" fill="{color}" xml:space="preserve">{body}</text>'
        )

    def arrow(self, points, dash=False, head=True):
        d = "M" + " L".join(f"{px} {py}" for px, py in points)
        extra = ' stroke-dasharray="10 7"' if dash else ""
        marker = ' marker-end="url(#arrow)"' if head else ""
        self.add(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="3"{extra}{marker}/>')

    def save(self, name: str) -> Path:
        path = HERE / f"{name}.svg"
        path.write_text(self.head + "\n".join(self.body) + "\n</svg>\n", encoding="utf-8")
        return path


M_prev = var("M", "t−1", True)
M_ref = var("M", "t", True)
M_gen = var("M", "t")
O_t = var("O", "t")
S_ = var("S")


def figura_visao_geral() -> Svg:
    s = Svg(
        1900, 1620,
        "Figura 1: visão geral do harness experimental para uma transição do SUMIE",
        "Execução nas etapas i a iv: o SUMIE fornece a transição; apenas o estado anterior de referência e a "
        "observação seguem para o prompt fixo e para o escritor, única variável do experimento; a saída bruta é "
        "gravada sem reparo. Avaliação nas etapas v a ix: validação do JSON e do esquema, correspondência direta "
        "com a referência, juiz semântico local apenas para divergências e registro em JSON Lines, que alimenta "
        "as métricas de estrutura, estado e operação e a análise estatística.",
    )
    # Faixa de execução
    s.text(30, 52, "Execução — etapas (i) a (iv)", 24, bold=True, color="#4b5b68")
    s.cylinder(30, 95, 200, 180, BLUE)
    s.text(130, 182, "SUMIE", 26, bold=True, anchor="middle")
    s.text(130, 214, "conjunto público", 20, anchor="middle")

    s.rect(270, 80, 290, 210, GRAY)
    s.text(290, 118, "(i) Preparar transição", 22, bold=True)
    s.text(290, 158, ["(", M_prev, ", ", O_t, ", ", M_ref, ")"], 22)
    s.text(290, 194, "rótulos PRESERVE,", 20)
    s.text(290, 222, "ADD e UPDATE", 20)

    s.rect(600, 80, 280, 210, GRAY)
    s.text(620, 118, "(ii) Montar prompt", 22, bold=True)
    s.text(620, 158, "prompt-base fixo", 22)
    s.text(620, 192, "(Apêndice A)", 22)
    s.text(620, 236, [S_, " + ", M_prev, " + ", O_t], 22)

    s.rect(920, 80, 320, 210, ACCENT_FILL, ACCENT, sw=3)
    s.text(940, 118, ["(iii) Escritor ", var("G")], 22, bold=True)
    s.text(940, 150, "única variável · ≤ 1.200 tokens", 19, color=ACCENT)
    s.text(940, 190, "Qwen3-0.6B", 22)
    s.text(940, 224, "T5Gemma B-B", 22)
    s.text(940, 258, "Qwen3-0.6B BD3LM", 22)

    s.rect(1300, 80, 340, 210, GREEN)
    s.text(1320, 118, "(iv) Gravar saída bruta", 22, bold=True)
    s.text(1320, 158, ["texto produzido (", M_gen, ")"], 22)
    s.text(1320, 192, "em disco, sem reparo", 22)

    s.arrow([(230, 185), (268, 185)])
    s.arrow([(560, 185), (598, 185)])
    s.arrow([(880, 185), (918, 185)])
    s.arrow([(1240, 185), (1298, 185)])

    # Coluna de avaliação
    cx = 1470
    s.text(1490, 334, "Avaliação — etapas (v) a (ix)", 24, bold=True, color="#4b5b68")
    s.arrow([(cx, 290), (cx, 353)])

    s.diamond(cx, 430, 170, 75)
    s.text(cx, 425, "(v) JSON válido?", 22, bold=True, anchor="middle")
    s.text(cx, 455, "json.loads", 19, anchor="middle", mono=True)
    s.arrow([(cx, 505), (cx, 548)])
    s.text(cx + 12, 534, "sim", 19)

    s.diamond(cx, 625, 170, 75)
    s.text(cx, 620, "(vi) Esquema", 22, bold=True, anchor="middle")
    s.text(cx, 648, "válido?", 22, bold=True, anchor="middle")
    s.arrow([(cx, 700), (cx, 748)])
    s.text(cx + 12, 730, "sim", 19)

    s.rect(1300, 750, 340, 130, GRAY)
    s.text(1320, 786, "(vii) Correspondência direta", 22, bold=True)
    s.text(1320, 822, "pares normalizados", 22)
    s.text(1320, 856, "→ métricas estritas", 22)

    s.arrow([(cx, 880), (cx, 918)])
    s.diamond(cx, 990, 170, 70)
    s.text(cx, 998, "Há divergência?", 22, bold=True, anchor="middle")

    # Falhas estruturais
    s.arrow([(1640, 430), (1790, 430), (1790, 1190), (1734, 1190)])
    s.arrow([(1640, 625), (1790, 625)], head=False)
    s.text(1655, 418, "não", 19)
    s.text(1655, 613, "não", 19)
    s.text(1775, 1092, "falha estrutural:", 18, anchor="end")
    s.text(1775, 1114, "zero na visão global", 18, anchor="end")

    # Região de referência (nunca enviada ao escritor)
    s.rect(900, 715, 360, 385, "#eef4fa", STROKE, dash=True, sw=2, rx=12)
    s.text(915, 745, "Somente avaliação", 20, bold=True, color="#4b5b68")
    s.text(915, 770, "(não enviada ao escritor)", 18, color="#4b5b68")
    s.rect(930, 785, 300, 120, BLUE)
    s.text(948, 818, "Referência", 22, bold=True)
    s.text(948, 852, [M_ref, " e anotações SUMIE"], 20)
    s.text(948, 884, "rótulos de operação", 20)
    s.arrow([(1230, 815), (1298, 815)])

    s.rect(930, 935, 300, 150, "#ffffff", STROKE, dash=True)
    s.text(948, 968, "(viii) Juiz semântico", 22, bold=True)
    s.text(948, 1000, "Gemma 3 1B · Q4_K_M", 19)
    s.text(948, 1030, ["recebe ", M_prev, ", ", O_t, ", ", M_ref, ", ", M_gen], 19)
    s.text(948, 1060, "sem a identidade do escritor", 19)
    s.arrow([(1080, 905), (1080, 933)])
    s.arrow([(1300, 990), (1232, 990)], dash=True)
    s.text(1268, 1020, "sim", 19)
    s.arrow([(1080, 1085), (1080, 1190), (1208, 1190)], dash=True)
    s.text(cx + 12, 1098, "não", 19)
    s.arrow([(cx, 1060), (cx, 1128)])

    # Referência vem da preparação (i)
    s.arrow([(520, 290), (520, 845), (928, 845)])
    s.text(540, 832, ["envia ", M_ref, ", anotações e rótulos"], 19, color="#4b5b68")

    s.cylinder(1210, 1130, 520, 125, GREEN)
    s.text(cx, 1196, "(ix) Registros JSON Lines", 22, bold=True, anchor="middle")
    s.text(cx, 1228, "saídas, decisões do juiz, métricas e proveniência", 19, anchor="middle")

    # Métricas e análise
    s.arrow([(cx, 1255), (cx, 1290)], head=False)
    s.arrow([(320, 1290), (1580, 1290)], head=False)
    for x in (320, 950, 1580):
        s.arrow([(x, 1290), (x, 1318)])
    boxes = [
        (30, "Estrutural · objetivo a", "validade do JSON e do esquema"),
        (660, "Estado · objetivo b", "precisão, revocação, F1, alucinação"),
        (1290, "Operação · objetivo c", "preservação, adição e atualização"),
    ]
    for x, title, line in boxes:
        s.rect(x, 1320, 580, 110, "#ffffff")
        s.text(x + 20, 1360, title, 22, bold=True)
        s.text(x + 20, 1396, line, 21)
        s.arrow([(x + 290, 1430), (x + 290, 1478)])
    s.rect(30, 1480, 1840, 110, GRAY)
    s.text(50, 1520, "Análise estatística (Seção 3.9)", 22, bold=True)
    s.text(50, 1556, "IC de 95% por bootstrap · Friedman e Wilcoxon com Holm-Bonferroni · curvas por turno · "
                     "visões condicional e global · resultados estritos e híbridos", 19)

    # Legenda
    s.text(30, 360, "Legenda", 22, bold=True)
    legend = [
        ("cyl", BLUE, "conjunto de dados ou registros"),
        ("rect", BLUE, "entrada ou referência"),
        ("rect", GRAY, "processamento"),
        ("rect", GREEN, "artefato gravado"),
        ("accent", ACCENT_FILL, "variável do experimento"),
        ("dia", GRAY, "decisão"),
        ("dash", "#ffffff", "caminho condicional (juiz)"),
    ]
    y = 385
    for kind, fill, label in legend:
        if kind == "cyl":
            s.cylinder(30, y, 50, 36, fill)
        elif kind == "dia":
            s.diamond(55, y + 18, 25, 18, fill)
        elif kind == "accent":
            s.rect(30, y, 50, 36, fill, ACCENT, sw=3, rx=5)
        elif kind == "dash":
            s.rect(30, y, 50, 36, fill, STROKE, dash=True, rx=5)
        else:
            s.rect(30, y, 50, 36, fill, rx=5)
        s.text(95, y + 26, label, 19)
        y += 48
    return s


def figura_escrita() -> Svg:
    s = Svg(
        1900, 780,
        "Figura 2: etapa de escrita do checkpoint (etapas ii e iii)",
        "A entrada do escritor é o prompt-base do Apêndice A já preenchido, isto é, a tripla (S, M*_{t-1}, O_t). "
        "O texto de instrução e o esquema S são fixos para todas as transições; o estado anterior "
        "de referência e a observação vêm do SUMIE a cada transição. Um dos três escritores gera o checkpoint completo M_t, "
        "conforme a Equação 1. O exemplo usa a frase P9 do primeiro parágrafo da entidade ENTITY0 do SUMIE; o JSON "
        "mostrado é o par anotado Replayability: Multiple endings, não uma saída de modelo.",
    )
    muted = "#4b5b68"

    # Origem dos campos
    s.rect(30, 100, 300, 180, BLUE)
    s.text(50, 136, "Fixo", 22, bold=True)
    s.text(50, 166, "igual em todas as", 19)
    s.text(50, 190, "transições e escritores", 19)
    s.text(50, 226, "instruções e regras 1–6", 19)
    s.text(50, 254, ["esquema ", S_, " (Seção 3.3)"], 19)

    s.cylinder(30, 300, 300, 270, BLUE)
    s.text(50, 354, "SUMIE", 22, bold=True)
    s.text(50, 382, "conjunto de dados", 19)
    s.text(50, 430, ["estado anterior ", M_prev], 19)
    s.text(50, 526, ["observação ", O_t], 19)

    # Prompt preenchido = entrada do escritor
    px, pw = 390, 680
    fx, fw = px + 20, pw - 40
    s.text(px, 62, "(ii) Entrada do escritor: prompt-base preenchido (Apêndice A)", 22, bold=True)
    s.rect(px, 80, pw, 660, GRAY, sw=2.5)

    def field(y, h, label, parts=None):
        s.rect(fx, y, fw, h, "#ffffff", rx=6)
        s.text(fx + 18, y + 32, label, 19, mono=True, bold=True)
        if parts:
            s.text(fx + 18 + 11 * len(label) + 30, y + 32, parts, 19, color=muted)

    field(100, 60, "You are the memory-state updater…", None)
    s.text(fx + fw - 18, 132, "regras 1–6", 18, anchor="end", color=muted)

    field(180, 100, "SCHEMA:", [S_])
    s.text(fx + 18, 264, '{"state": {"chave": "valor"}}', 19, mono=True)

    field(300, 100, "CURRENT STATE:", [M_prev])
    s.text(fx + 18, 384, '{"state": {}}', 19, mono=True)
    s.text(fx + fw - 18, 384, "primeiro parágrafo: vazio", 17, anchor="end", color=muted)

    field(420, 200, "NEW OBSERVATION:", [O_t])
    s.text(fx + fw - 18, 452, "SUMIE · ENTITY0 · frase P9", 17, anchor="end", color=muted)
    sentence = [
        "“The game's replayability is further enhanced by its",
        "multiple endings, encouraging players to revisit",
        "ENTITY0 and explore different narrative paths.”",
    ]
    for i, line in enumerate(sentence):
        s.text(fx + 18, 500 + i * 32, line, 19, italic=True)

    field(640, 80, "UPDATED STATE:", None)
    s.text(fx + 18, 702, ["o escritor gera ", M_gen, " a partir deste ponto"], 18, color=ACCENT)

    s.arrow([(330, 130), (408, 130)])
    s.arrow([(330, 230), (408, 230)])
    s.arrow([(330, 410), (408, 410)])
    s.arrow([(330, 520), (408, 520)])

    # Escritor
    gx, gw = 1230, 330
    s.text(gx + gw / 2, 175, [M_gen, " = ", var("G"), "(", S_, ", ", M_prev, ", ", O_t, ")"], 24, anchor="middle")
    s.text(gx + gw / 2, 203, "Equação 1, com o estado de referência", 17, anchor="middle", color=muted)
    s.rect(gx, 225, gw, 360, ACCENT_FILL, ACCENT, sw=3)
    s.text(gx + 20, 263, ["(iii) Escritor ", var("G")], 22, bold=True)
    s.text(gx + 20, 295, "um por execução · ≤ 1.200 tokens", 18, color=ACCENT)
    models = [("Qwen3-0.6B", "autoregressivo decoder-only"),
              ("T5Gemma B-B", "encoder-decoder"),
              ("Qwen3-0.6B BD3LM", "difusão em blocos")]
    y = 343
    for name, paradigm in models:
        s.text(gx + 20, y, name, 22)
        s.text(gx + 40, y + 30, paradigm, 19, italic=True)
        y += 80
    s.arrow([(px + pw, 405), (gx - 2, 405)])
    s.text((px + pw + gx) / 2, 390, ["(", S_, ", ", M_prev, ", ", O_t, ")"], 18, anchor="middle")

    # Saída
    ox = 1610
    s.rect(ox, 240, 270, 330, GREEN)
    s.text(ox + 18, 277, [M_gen, ": saída bruta"], 22, bold=True)
    s.text(ox + 18, 321, '{"state": {', 19, mono=True)
    s.text(ox + 18, 351, ' "Replayability":', 19, mono=True)
    s.text(ox + 18, 381, ' "Multiple endings"', 19, mono=True)
    s.text(ox + 18, 411, "}}", 19, mono=True)
    for i, line in enumerate(["forma esperada para", "o excerto: par anotado", "no SUMIE, não saída", "de modelo"]):
        s.text(ox + 18, 457 + i * 24, line, 18)
    s.arrow([(gx + gw, 405), (ox - 2, 405)])
    return s

def find_browser() -> str | None:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        shutil.which("chrome") or "",
        shutil.which("google-chrome") or "",
        shutil.which("chromium") or "",
    ]
    return next((c for c in candidates if c and Path(c).exists()), None)


def render_png(svg_path: Path, width: int, height: int, scale: float = 1.5) -> None:
    browser = find_browser()
    if not browser:
        print(f"Navegador não encontrado; PNG de {svg_path.name} não gerado.")
        return
    png = svg_path.with_suffix(".png")
    subprocess.run(
        [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--force-device-scale-factor={scale}", f"--window-size={width},{height}",
         "--default-background-color=ffffffff", f"--screenshot={png}", svg_path.as_uri()],
        check=True, capture_output=True,
    )
    print(f"{png.name} gerado")


if __name__ == "__main__":
    for name, fig in (("fig1_harness_visao_geral", figura_visao_geral()),
                      ("fig2_harness_escrita", figura_escrita())):
        path = fig.save(name)
        print(f"{path.name} gerado")
        render_png(path, fig.w, fig.h)
