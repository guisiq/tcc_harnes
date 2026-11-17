"""Compara o DOCX final com o Markdown e com o corpo gerado pelo Pandoc."""

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Cm, Twips
from lxml import etree

from gerar_artigo_unitins import CAPTION, MONTHS, front_matter, inline_text, pandoc_ast, schedule_header


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def article_paragraphs(document):
    paragraphs = document.paragraphs
    for index, paragraph in enumerate(paragraphs):
        if paragraph.style.name == "Heading 1" and paragraph.text.casefold() == "1 introdução":
            return paragraphs[index:]
    raise ValueError("Não foi encontrada a introdução no documento.")


def citation_groups(node):
    groups = []

    def visit(value):
        if isinstance(value, dict):
            if value.get("t") == "Cite":
                groups.append([
                    (item["citationId"], item["citationMode"]["t"])
                    for item in value["c"][0]
                ])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(node)
    return groups


def note_elements(archive):
    if "word/footnotes.xml" not in archive.namelist():
        return {}
    root = etree.fromstring(archive.read("word/footnotes.xml"))
    return {
        element.get(qn("w:id")): element
        for element in root.xpath("/w:footnotes/w:footnote", namespaces=NS)
    }


def field_payloads(root, notes):
    fields = []
    marker = " ADDIN ZOTERO_ITEM CSL_CITATION "

    def read_elements(element):
        stack = []
        for child in element.iter():
            if child.tag == qn("w:footnoteReference"):
                identifier = child.get(qn("w:id"))
                if identifier not in notes:
                    raise ValueError(f"Nota de rodapé ausente: {identifier}")
                read_elements(notes[identifier])
            elif child.tag == qn("w:fldChar"):
                kind = child.get(qn("w:fldCharType"))
                if kind == "begin":
                    stack.append([])
                elif kind == "end" and stack:
                    instruction = "".join(stack.pop())
                    if instruction.startswith(marker):
                        fields.append(json.loads(instruction[len(marker):].strip()))
            elif child.tag == qn("w:instrText") and stack:
                stack[-1].append(child.text or "")

    read_elements(root)
    return fields


def footnote_texts(root, notes):
    result = []
    for identifier in root.xpath("//w:footnoteReference/@w:id", namespaces=NS):
        if identifier not in notes:
            raise ValueError(f"Nota de rodapé ausente: {identifier}")
        result.append("".join(notes[identifier].xpath(".//w:t/text()", namespaces=NS)))
    return result


def math_texts(root):
    return [
        "".join(element.xpath(".//m:t/text()", namespaces=NS)).replace("\u2212", "-")
        for element in root.xpath("//m:oMath", namespaces=NS)
    ]


def media_hashes(archive):
    return Counter(
        hashlib.sha256(archive.read(name)).hexdigest()
        for name in archive.namelist()
        if name.startswith("word/media/") and not name.endswith("/")
    )


def verify_tables(base, final):
    if len(base.tables) != len(final.tables):
        raise ValueError("A quantidade de tabelas mudou durante a formatação.")
    selected = 0
    for table_number, (old, new) in enumerate(zip(base.tables, final.tables), 1):
        periods = schedule_header(old)
        expected_rows = len(old.rows) + (1 if periods is not None else 0)
        if len(new.rows) != expected_rows or len(new.columns) != len(old.columns):
            raise ValueError(f"As dimensões da tabela {table_number} mudaram inesperadamente.")
        if periods is None:
            for old_row, new_row in zip(old.rows, new.rows):
                for old_cell, new_cell in zip(old_row.cells, new_row.cells):
                    if old_cell.text != new_cell.text:
                        raise ValueError(f"O conteúdo da tabela {table_number} foi alterado.")
            continue

        if new.rows[1].cells[0].text.strip() != old.rows[0].cells[0].text.strip():
            raise ValueError("A primeira coluna do cronograma mudou.")
        for index, (month, period) in enumerate(periods, 1):
            if new.rows[1].cells[index].text.strip() != period:
                raise ValueError(f"A quinzena {period} não corresponde à fonte.")
            if new.rows[0].cells[index].text.strip() != MONTHS[month]:
                raise ValueError(f"O mês da quinzena {period} não corresponde à fonte.")
        for old_row, new_row in zip(old.rows[1:], new.rows[2:]):
            if old_row.cells[0].text != new_row.cells[0].text:
                raise ValueError("Uma atividade do cronograma foi alterada.")
            for old_cell, new_cell in zip(old_row.cells[1:], new_row.cells[1:]):
                is_selected = old_cell.text.strip().upper() == "X"
                shading = new_cell._tc.tcPr.find(qn("w:shd"))
                is_blue = shading is not None and shading.get(qn("w:fill"), "").upper() == "5B9BD5"
                if is_selected:
                    if not is_blue or new_cell.text.strip():
                        raise ValueError("Uma seleção do cronograma não foi preservada.")
                    selected += 1
                elif is_blue or old_cell.text != new_cell.text:
                    raise ValueError("Uma célula não selecionada do cronograma foi alterada.")
    return selected


def verify_front(document, front):
    paragraphs = document.paragraphs

    def after(heading, offset):
        for index, paragraph in enumerate(paragraphs):
            if paragraph.text == heading:
                return paragraphs[index + offset].text
        raise ValueError(f"A seção {heading} não foi encontrada no DOCX.")

    sections = front["sections"]
    expected = [
        ("RESUMO", 1, inline_text(sections["Resumo"])),
        ("RESUMO", 2, "Palavras-chave: " + inline_text(sections["Palavras-chave"])),
        ("ABSTRACT", 1, inline_text(sections["Title"])),
        ("ABSTRACT", 2, inline_text(sections["Abstract"])),
        ("ABSTRACT", 3, "Keywords: " + inline_text(sections["Keywords"])),
    ]
    for heading, offset, text in expected:
        if after(heading, offset) != text:
            raise ValueError(f"O conteúdo preliminar {heading}, item {offset}, difere da fonte.")


def verify_references(paragraphs, keys):
    start = None
    for index, paragraph in enumerate(paragraphs):
        if paragraph.style.name == "Heading 1" and paragraph.text.casefold() == "referências":
            start = index + 1
            break
    if start is None:
        raise ValueError("A seção de referências não foi encontrada no corpo.")
    end = len(paragraphs)
    for index in range(start, len(paragraphs)):
        if paragraphs[index].style.name == "Heading 1":
            end = index
            break
    references = [paragraph for paragraph in paragraphs[start:end] if paragraph.text.strip()]
    if len(references) != len(keys):
        raise ValueError(
            f"Foram geradas {len(references)} referências para {len(keys)} chaves citadas."
        )


def verify_formatting(document):
    for section in document.sections:
        for attribute, centimeters in (
            ("page_width", 21), ("page_height", 29.7),
            ("top_margin", 3), ("left_margin", 3),
            ("bottom_margin", 2), ("right_margin", 2),
        ):
            actual = getattr(section, attribute)
            if actual is None or abs(actual - Cm(centimeters)) > Cm(0.01):
                raise ValueError(f"Formatação Unitins: {attribute} deve medir {centimeters} cm.")

    def inherited(style, group, attribute):
        while style is not None:
            value = getattr(getattr(style, group), attribute)
            if value is not None:
                return value
            style = style.base_style
        return None

    def has_font_size(paragraph, points):
        for run in paragraph.runs:
            size = run.font.size
            if size is None:
                size = inherited(run.style, "font", "size")
            if size is None:
                size = inherited(paragraph.style, "font", "size")
            if size is None or size.pt != points:
                return False
        return True

    styles = {style.style_id: style for style in document.styles}
    for relation in document.part.rels.values():
        if relation.reltype != RT.FOOTNOTES:
            continue
        notes = etree.fromstring(relation.target_part.blob)
        for identifier in set(notes.xpath("//w:pStyle/@w:val", namespaces=NS)):
            style = styles.get(identifier)
            font = inherited(style, "font", "name")
            size = inherited(style, "font", "size")
            spacing = inherited(style, "paragraph_format", "line_spacing")
            alignment = inherited(style, "paragraph_format", "alignment")
            if alignment is None:
                # O Word omite o alinhamento quando coincide com o padrão do documento.
                defaults = document.styles.element.xpath(
                    "w:docDefaults/w:pPrDefault/w:pPr/w:jc/@w:val"
                )
                alignment = WD_ALIGN_PARAGRAPH.from_xml(defaults[0] if defaults else "left")
            if (
                font != "Arial"
                or size is None or size.pt != 10
                or spacing != 1.0
                or alignment != WD_ALIGN_PARAGRAPH.LEFT
            ):
                raise ValueError(
                    "Formatação Unitins: notas devem usar Arial 10, espaço simples e "
                    f"alinhamento à esquerda. Estilo {identifier}: fonte={font}, "
                    f"tamanho={size.pt if size is not None else None}, "
                    f"entrelinha={spacing}, alinhamento={alignment}."
                )

    summary_remaining = 0
    in_body = False
    in_references = False
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if summary_remaining:
            summary_remaining -= 1
            if summary_remaining == 0:
                if paragraph.paragraph_format.line_spacing != 1.0 or not has_font_size(paragraph, 11):
                    raise ValueError("Formatação Unitins: resumo e abstract devem usar fonte 11 e espaço simples.")
        if text in {"RESUMO", "ABSTRACT"}:
            summary_remaining = 1 if text == "RESUMO" else 2
            continue
        if text.casefold() == "1 introdução":
            in_body = True
        if not in_body:
            continue
        if paragraph.style.name == "Heading 1":
            in_references = text.casefold() == "referências"
        if CAPTION.match(text) or text.startswith("Fonte:"):
            if (
                paragraph.paragraph_format.alignment != WD_ALIGN_PARAGRAPH.CENTER
                or paragraph.paragraph_format.line_spacing != 1.0
                or not has_font_size(paragraph, 10)
            ):
                raise ValueError(f"Formatação Unitins: legenda/fonte fora do padrão: {text[:80]}")
            if text.startswith(("Quadro ", "Tabela ")):
                following = paragraph._p.getnext()
                if following is None or following.tag != qn("w:tbl"):
                    raise ValueError("Formatação Unitins: título de quadro ou tabela deve ficar acima do elemento.")
            continue
        if paragraph.style.name == "Heading 1" and not re.match(r"^\d+\s", text):
            if paragraph.paragraph_format.alignment != WD_ALIGN_PARAGRAPH.CENTER:
                raise ValueError(f"Formatação Unitins: título sem número deve ser centralizado: {text}")
        if (
            text and not in_references
            and paragraph.style.name in {"Normal", "Body Text", "First Paragraph"}
            and paragraph._p.find(qn("m:oMathPara")) is None
        ):
            expected_indent = Cm(0) if (
                text.startswith("em que ") or re.match(r"^([a-z]\)|\d+\.)", text)
            ) else Cm(1.25)
            indent = paragraph.paragraph_format.first_line_indent
            if indent is None:
                indent = inherited(paragraph.style, "paragraph_format", "first_line_indent")
            if indent is None:
                defaults = document.styles.element.xpath(
                    "w:docDefaults/w:pPrDefault/w:pPr/w:ind"
                )
                properties = defaults[0].attrib if defaults else {}
                indent = Twips(
                    -int(properties[qn("w:hanging")]) if qn("w:hanging") in properties
                    else int(properties.get(qn("w:firstLine"), "0"))
                )
            if (
                paragraph.paragraph_format.alignment != WD_ALIGN_PARAGRAPH.JUSTIFY
                or paragraph.paragraph_format.line_spacing != 1.5
                or indent is None or abs(indent - expected_indent) > Cm(0.01)
                or not has_font_size(paragraph, 12)
            ):
                raise ValueError(f"Formatação Unitins: corpo fora do padrão: {text[:80]}")

    width = document.sections[0].page_width - document.sections[0].left_margin - document.sections[0].right_margin
    for table in document.tables:
        if abs(sum(column.width for column in table.columns) - width) > Cm(0.02):
            raise ValueError("Formatação Unitins: tabela não ocupa a largura útil da página.")
        header = table.rows[0]._tr.trPr
        if header is None or header.find(qn("w:tblHeader")) is None:
            raise ValueError("Formatação Unitins: cabeçalho da tabela não se repete nas páginas seguintes.")
        previous = table._tbl.getprevious()
        caption = "".join(previous.xpath(".//w:t/text()")) if previous is not None else ""
        if caption.startswith("Tabela "):
            borders = table._tbl.tblPr.find(qn("w:tblBorders"))
            for side in ("left", "right"):
                border = borders.find(qn(f"w:{side}")) if borders is not None else None
                if border is None or border.get(qn("w:val")) not in {"nil", "none"}:
                    raise ValueError("Formatação Unitins: tabelas não devem ter fechamento lateral.")
    for image in document.inline_shapes:
        if image.width > width + Cm(0.01):
            raise ValueError("Formatação Unitins: imagem ultrapassa a largura útil da página.")


def verify(source, body, final, pandoc):
    ast = pandoc_ast(pandoc, source)
    front = front_matter(ast)
    groups = citation_groups(front["body_blocks"])
    keys = {key for group in groups for key, _ in group}
    base = Document(body)
    output = Document(final)
    old_paragraphs = article_paragraphs(base)
    new_paragraphs = article_paragraphs(output)
    if len(old_paragraphs) != len(new_paragraphs):
        raise ValueError("A quantidade de parágrafos do corpo mudou durante a formatação.")
    for index, (old, new) in enumerate(zip(old_paragraphs, new_paragraphs), 1):
        expected = old.text.upper() if old.style.name == "Heading 1" else old.text
        if expected != new.text:
            raise ValueError(f"O parágrafo {index} do corpo mudou durante a formatação.")
    verify_front(output, front)
    verify_references(new_paragraphs, keys)
    verify_formatting(output)
    selected = verify_tables(base, output)

    with ZipFile(body) as base_archive, ZipFile(final) as final_archive:
        base_root = etree.fromstring(base_archive.read("word/document.xml"))
        final_root = etree.fromstring(final_archive.read("word/document.xml"))
        base_notes = note_elements(base_archive)
        final_notes = note_elements(final_archive)
        fields = field_payloads(final_root, final_notes)
        if len(fields) != len(groups):
            raise ValueError(f"Foram gerados {len(fields)} campos para {len(groups)} grupos de citação.")
        for group, field in zip(groups, fields):
            actual = [item["itemData"]["id"] for item in field["citationItems"]]
            if actual != [key for key, _ in group]:
                raise ValueError(f"As chaves de citação foram alteradas: {actual}")
            if len(group) == 1 and group[0][1] == "AuthorInText":
                if not field["citationItems"][0].get("suppress-author"):
                    raise ValueError(f"A citação narrativa não preservou o autor: {group[0][0]}")
                if not re.fullmatch(r"\([^()]+\)", field["properties"]["plainCitation"]):
                    raise ValueError(f"A citação narrativa não preservou o ano: {group[0][0]}")
        if math_texts(base_root) != math_texts(final_root):
            raise ValueError("As expressões matemáticas foram alteradas.")
        if footnote_texts(base_root, base_notes) != footnote_texts(final_root, final_notes):
            raise ValueError("As notas de rodapé foram alteradas.")
        if media_hashes(base_archive) != media_hashes(final_archive):
            raise ValueError("As imagens do cabeçalho ou do artigo foram alteradas.")
        for name in final_archive.namelist():
            if re.fullmatch(r"word/(header|footer)\d+\.xml", name):
                root = etree.fromstring(final_archive.read(name))
                text = "".join(root.xpath("//w:t/text()", namespaces=NS))
                if "---Internal Use---" in text:
                    raise ValueError("A marca Internal Use permanece no cabeçalho ou rodapé.")
        if b"Do Zotero Refresh" in final_archive.read("word/document.xml"):
            raise ValueError("Há campos de citação sem formatação no documento.")
        math_count = len(math_texts(final_root))
        notes_count = len(footnote_texts(final_root, final_notes))

    print(
        f"Conteúdo verificado: {len(new_paragraphs)} parágrafos, {len(groups)} grupos de citação, "
        f"{len(keys)} referências, {len(output.tables)} tabelas, {selected} seleções no cronograma, "
        f"{math_count} expressões matemáticas e {notes_count} notas."
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fonte", type=Path, required=True)
    parser.add_argument("--corpo", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--pandoc", type=Path, required=True)
    args = parser.parse_args()
    try:
        verify(args.fonte, args.corpo, args.final, args.pandoc)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Erro ao validar o artigo: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
