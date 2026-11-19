import json
import re
import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

HEADING_RE = re.compile(
    r"^(\d+(\.\d+)*\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]|RESUMO$|ABSTRACT$|LISTA DE |SUMÁRIO$|REFERÊNCIAS$|APÊNDICE [A-Z]|Expressões de busca$)"
)
CAPTION_RE = re.compile(r"^(Figura|Quadro|Tabela)\s+\d+\s*[–—-]")
FONTE_RE = re.compile(r"^Fonte:\s*")
FOOTNOTE_RE = re.compile(r"^[1-9]\s+(Disponível em:|Modelo e termos)")


def extract_document(pdf_path: str, max_pages: int | None = None) -> dict:
    doc = pymupdf.open(pdf_path)
    limit = min(max_pages, len(doc)) if max_pages else len(doc)

    items = []
    images_meta = []
    current_section = "Elementos Pré-Textuais"
    current = None

    def flush():
        nonlocal current
        if current and current["Text"].strip():
            current["Id"] = len(items) + 1
            items.append(current)
        current = None

    for pno in range(limit):
        page_num = pno + 1
        page = doc[pno]

        for img_idx, img_info in enumerate(page.get_images(full=True), start=1):
            xref = img_info[0]
            width, height = img_info[2], img_info[3]
            images_meta.append({
                "Page": page_num,
                "IndexOnPage": img_idx,
                "Xref": xref,
                "Width": width,
                "Height": height,
            })

        raw_blocks = [b for b in page.get_text("blocks") if b[6] == 0]
        filtered = []
        printed_page = None
        for b in raw_blocks:
            t = " ".join(b[4].split())
            if not t:
                continue
            if b[1] < 80 and b[0] > 490 and t.isdigit():
                printed_page = int(t)
                continue
            filtered.append([b[0], b[1], b[2], b[3], t])

        filtered.sort(key=lambda x: (round(x[1] / 4.0), x[0]))

        if page_num in (1, 2):
            flush()
            sec = "Capa" if page_num == 1 else "Folha de Rosto"
            items.append({
                "Id": len(items) + 1,
                "PageStart": page_num,
                "PageEnd": page_num,
                "PrintedPage": printed_page,
                "Section": sec,
                "Kind": "front_matter",
                "Text": " | ".join(b[4] for b in filtered),
            })
            continue

        if page_num in (5, 6, 7, 8):
            flush()
            heading = filtered[0][4] if filtered else f"Página {page_num}"
            current_section = heading
            items.append({
                "Id": len(items) + 1,
                "PageStart": page_num,
                "PageEnd": page_num,
                "PrintedPage": printed_page,
                "Section": heading,
                "Kind": "front_matter_list",
                "Text": "\n".join(b[4] for b in filtered),
            })
            continue

        # Group blocks into horizontal lines using a y-center tolerance of 7pt
        filtered.sort(key=lambda x: (x[1], x[0]))
        line_groups = []
        for b in filtered:
            b_yc = 0.5 * (b[1] + b[3])
            placed = False
            if (b[3] - b[1]) < 24:
                for g in line_groups:
                    if g["height"] < 24 and abs(b_yc - g["yc"]) < 7.0:
                        g["blocks"].append(b)
                        g["yc"] = sum(0.5 * (x[1] + x[3]) for x in g["blocks"]) / len(g["blocks"])
                        g["height"] = max(x[3] for x in g["blocks"]) - min(x[1] for x in g["blocks"])
                        placed = True
                        break
            if not placed:
                line_groups.append({"yc": b_yc, "height": b[3] - b[1], "blocks": [b]})

        lines = []
        for g in line_groups:
            sb_list = sorted(g["blocks"], key=lambda x: x[0])
            x0 = sb_list[0][0]
            y0 = min(x[1] for x in sb_list)
            x1 = max(x[2] for x in sb_list)
            y1 = max(x[3] for x in sb_list)
            text_line = " ".join(x[4] for x in sb_list)
            # Clean math spacing artifacts like '𝑀𝑡−1 ∗ ,' -> '𝑀𝑡−1∗,'
            text_line = re.sub(r"\s+∗", "∗", text_line)
            text_line = re.sub(r"(?<=[∗₀₁₂₃₄₅₆₇₈₉𝑡])\s+([,.;:\)])", r"\1", text_line)
            text_line = re.sub(r"\(\s+", "(", text_line)
            lines.append([x0, y0, x1, y1, text_line])

        in_table = current is not None and current["Kind"] == "table"
        for x0, y0, x1, y1, t in lines:
            if FOOTNOTE_RE.match(t) and y0 > 700:
                items.append({
                    "Id": len(items) + 1,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "footnote",
                    "Text": t,
                })
                continue

            if (HEADING_RE.match(t) and x0 < 310) or (
                page_num in (48, 52, 53) and HEADING_RE.match(t)
            ):
                flush()
                current_section = t
                in_table = False
                items.append({
                    "Id": len(items) + 1,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "heading",
                    "Text": t,
                })
                continue

            if CAPTION_RE.match(t):
                flush()
                in_table = t.startswith(("Quadro", "Tabela"))
                current = {
                    "Id": 0,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "caption",
                    "Text": t,
                }
                continue

            if current is not None and current["Kind"] == "caption":
                # Multi-line caption continuation (e.g. Tabela 1 two-line title)
                if not current["Text"].endswith(".") and y0 < 235 and not t.startswith(("Etapa", "Tipo", "Trabalho", "Consulta", "Categoria", "Objetivo", "Ativ.", "ago.")):
                    current["Text"] += " " + t
                    continue
                else:
                    flush()
                    if in_table:
                        current = {
                            "Id": 0,
                            "PageStart": page_num,
                            "PageEnd": page_num,
                            "PrintedPage": printed_page,
                            "Section": current_section,
                            "Kind": "table",
                            "Text": "",
                        }

            if FONTE_RE.match(t):
                flush()
                in_table = False
                items.append({
                    "Id": len(items) + 1,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "source_note",
                    "Text": t,
                })
                continue

            if in_table:
                if current is None or current["Kind"] != "table":
                    flush()
                    current = {
                        "Id": 0,
                        "PageStart": page_num,
                        "PageEnd": page_num,
                        "PrintedPage": printed_page,
                        "Section": current_section,
                        "Kind": "table",
                        "Text": t,
                    }
                else:
                    current["PageEnd"] = page_num
                    current["Text"] += (" | " if current["Text"] else "") + t
                continue

            if current_section == "REFERÊNCIAS":
                flush()
                items.append({
                    "Id": len(items) + 1,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "reference",
                    "Text": t,
                })
                continue

            if 97.0 <= x0 <= 102.0 and page_num >= 52:
                flush()
                items.append({
                    "Id": len(items) + 1,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "code_or_query",
                    "Text": t,
                })
                continue

            if re.match(r"^F[1-6]\s*[–—-]", t):
                flush()
                current = {
                    "Id": 0,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "list_item",
                    "Text": t,
                }
                continue

            is_display_eq = (
                (page_num == 14 and 225 <= y0 <= 260)
                or (page_num == 37 and 420 <= y0 <= 540)
                or (page_num == 38 and 250 <= y0 <= 355)
            )
            if is_display_eq:
                if current and current["Kind"] == "equation":
                    current["PageEnd"] = page_num
                    current["Text"] += " " + t
                else:
                    flush()
                    current = {
                        "Id": 0,
                        "PageStart": page_num,
                        "PageEnd": page_num,
                        "PrintedPage": printed_page,
                        "Section": current_section,
                        "Kind": "equation",
                        "Text": t,
                    }
                continue

            if page_num in (3, 4) and (
                t.startswith("Palavras-chave:")
                or t.startswith("Keywords:")
                or t.startswith("Compact language models")
            ):
                flush()
                current = {
                    "Id": 0,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "paragraph",
                    "Text": t,
                }
                continue

            is_new_list = 145.0 <= x0 <= 170.0
            is_new_para = 119.0 <= x0 <= 120.8

            if is_new_list:
                flush()
                current = {
                    "Id": 0,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "list_item",
                    "Text": t,
                }
            elif is_new_para:
                flush()
                current = {
                    "Id": 0,
                    "PageStart": page_num,
                    "PageEnd": page_num,
                    "PrintedPage": printed_page,
                    "Section": current_section,
                    "Kind": "paragraph",
                    "Text": t,
                }
            else:
                if current is None or current["Kind"] not in ("paragraph", "list_item"):
                    flush()
                    current = {
                        "Id": 0,
                        "PageStart": page_num,
                        "PageEnd": page_num,
                        "PrintedPage": printed_page,
                        "Section": current_section,
                        "Kind": "paragraph",
                        "Text": t,
                    }
                else:
                    current["PageEnd"] = page_num
                    current["Text"] += " " + t

    flush()
    # Re-index sequentially
    for idx, item in enumerate(items, start=1):
        item["Id"] = idx

    return {
        "PageCount": limit,
        "Items": items,
        "Images": images_meta,
    }


if __name__ == "__main__":
    pdf_file = sys.argv[1]
    max_p = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "0" else None
    result = extract_document(pdf_file, max_p)
    print(json.dumps(result, ensure_ascii=False))
