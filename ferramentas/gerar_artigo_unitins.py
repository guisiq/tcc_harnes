"""Prepara o DOCX do artigo; a paginação final é feita pelo script PowerShell."""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_SOURCE = ROOT / "TCC_Checkpoint_JSON_Obsidian" / "07_Artigo_TCC" / "artigo_tcc_unitins.md"
DEFAULT_HEADER = ROOT / "anexos" / "Recursos" / "Cabeçalho oficial 2025.docx"
DEFAULT_CONFIG = HERE / "artigo_unitins_config.json"
DEFAULT_CSL_NAME = "associacao-brasileira-de-normas-tecnicas.csl"
INTRODUCTION = re.compile(r"^#\s+1\s+Introdução\s*$", re.IGNORECASE | re.MULTILINE)
CAPTION = re.compile(r"^(?:Quadro|Tabela)\s+\d+\s+[–—-]\s+")
HEADING = re.compile(r"^Heading ([1-9])$")
BLACK = RGBColor(0, 0, 0)
FONT = "Arial"
MONTHS = {
    "jan": "Janeiro",
    "fev": "Fevereiro",
    "mar": "Março",
    "abr": "Abril",
    "mai": "Maio",
    "jun": "Junho",
    "jul": "Julho",
    "ago": "Agosto",
    "set": "Setembro",
    "out": "Outubro",
    "nov": "Novembro",
    "dez": "Dezembro",
}


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--cabecalho", type=Path, default=DEFAULT_HEADER)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--pandoc", type=Path, required=True)
    parser.add_argument("--csl", type=Path, required=True)
    parser.add_argument("--mapa-zotero", type=Path)
    parser.add_argument("--trabalho", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    return parser.parse_args()


def require_file(path, description):
    if not path.is_file():
        raise ValueError(f"{description} não encontrado: {path}")


def pandoc_ast(pandoc, source):
    result = subprocess.run(
        [str(pandoc), str(source), "-f", "markdown", "-t", "json"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def inline_text(inlines, *, ignore_notes=False):
    result = []
    for inline in inlines:
        kind = inline["t"]
        if kind == "Str":
            result.append(inline["c"])
        elif kind in {"Space", "SoftBreak"}:
            result.append(" ")
        elif kind == "LineBreak":
            result.append("\n")
        elif kind in {"Emph", "Strong", "SmallCaps", "Superscript", "Subscript"}:
            result.append(inline_text(inline["c"], ignore_notes=ignore_notes))
        elif kind == "Code":
            result.append(inline["c"][1])
        elif kind == "Note" and ignore_notes:
            continue
        else:
            raise ValueError(f"Formatação não suportada nos dados preliminares: {kind}")
    return "".join(result)


def metadata_text(meta, key, *, required=True):
    value = meta.get(key)
    if value is None:
        if required:
            raise ValueError(f"Metadado obrigatório ausente: {key}")
        return ""
    if value["t"] == "MetaInlines":
        return inline_text(value["c"], ignore_notes=True).strip()
    if value["t"] == "MetaString":
        return value["c"].strip()
    raise ValueError(f"Metadado {key} está em um formato não suportado.")


def personal_name(inlines):
    value = inline_text(inlines, ignore_notes=True).strip()
    if "," in value:
        surname, given = value.split(",", 1)
        value = f"{given.strip()} {surname.strip().title()}"
    if not value:
        raise ValueError("O nome de um autor está vazio.")
    return value


def front_matter(ast):
    meta = ast["meta"]
    title = metadata_text(meta, "title")
    subtitle = metadata_text(meta, "subtitle", required=False)
    date = metadata_text(meta, "date")
    years = re.findall(r"\b\d{4}\b", date)
    authors = meta.get("author", {})
    if not years or authors.get("t") != "MetaList" or len(authors["c"]) != 2:
        raise ValueError("Informe o ano e os dois autores (acadêmico e orientador) nos metadados.")
    if any(item.get("t") != "MetaInlines" for item in authors["c"]):
        raise ValueError("Os nomes dos autores devem usar texto nos metadados.")

    labels = {"Resumo", "Palavras-chave", "Title", "Abstract", "Keywords"}
    sections = {}
    first_heading = None
    for index, block in enumerate(ast["blocks"]):
        if block["t"] == "Header":
            level, _, heading_content = block["c"]
            if level != 1 or inline_text(heading_content).casefold() != "1 introdução":
                raise ValueError("O primeiro título do artigo deve ser '# 1 Introdução'.")
            first_heading = index
            break
        if block["t"] == "RawBlock" and block["c"][0] == "html" and block["c"][1].lstrip().startswith("<!--"):
            continue
        if block["t"] not in {"Para", "Plain"} or not block["c"]:
            raise ValueError(f"Elemento preliminar não suportado: {block['t']}")
        first = block["c"][0]
        label = inline_text(first["c"]).rstrip(":").strip() if first["t"] == "Strong" else ""
        if label not in labels:
            raise ValueError(
                "Cada elemento preliminar deve estar em um único parágrafo com rótulo "
                "(Resumo, Palavras-chave, Title, Abstract ou Keywords)."
            )
        if label in sections:
            raise ValueError(f"Seção preliminar duplicada: {label}")
        content = list(block["c"][1:])
        while content and content[0]["t"] == "Space":
            content.pop(0)
        if not content:
            raise ValueError(f"A seção preliminar está vazia: {label}")
        inline_text(content)
        sections[label] = content
    missing = labels - sections.keys()
    if missing:
        raise ValueError(f"Seções preliminares ausentes: {', '.join(sorted(missing))}")
    if first_heading is None:
        raise ValueError("Não foi encontrado o início do corpo do artigo.")
    return {
        "title": f"{title}: {subtitle}".upper() if subtitle else title.upper(),
        "year": years[-1],
        "author": personal_name(authors["c"][0]["c"]),
        "advisor": personal_name(authors["c"][1]["c"]),
        "sections": sections,
        "body_blocks": ast["blocks"][first_heading:],
    }


def collect_citation_groups(node):
    groups = []

    def visit(value):
        if isinstance(value, dict):
            if value.get("t") == "Cite":
                citations = value["c"][0]
                for citation in citations:
                    if citation["citationPrefix"] or citation["citationSuffix"]:
                        raise ValueError(
                            "Citações com prefixo, sufixo ou indicação de página ainda não "
                            f"são suportadas: {citation['citationId']}."
                        )
                if len(citations) != 1 and any(
                    item["citationMode"]["t"] == "AuthorInText" for item in citations
                ):
                    raise ValueError("Uma citação narrativa não pode compartilhar o mesmo grupo.")
                groups.append([item["citationId"] for item in citations])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(node)
    return groups


def zotero_items(keys, cache_path, adjustments):
    if not keys:
        raise ValueError("Nenhuma citação foi encontrada no corpo do artigo.")
    if cache_path is not None:
        require_file(cache_path, "Mapa CSL do Zotero")
        raw_items = json.loads(cache_path.read_text(encoding="utf-8"))
        if not isinstance(raw_items, list):
            raise ValueError("O mapa Zotero deve conter uma lista CSL JSON.")
        items = {}
        for item in raw_items:
            key = item.get("id")
            if not isinstance(key, str) or key in items:
                raise ValueError(f"Identificador ausente ou duplicado no mapa Zotero: {key!r}")
            items[key] = item
    else:
        payload = {
            "jsonrpc": "2.0",
            "method": "item.pandoc_filter",
            "params": {"citekeys": sorted(keys), "asCSL": True, "style": "apa"},
            "id": 1,
        }
        request = urllib.request.Request(
            "http://127.0.0.1:23119/better-bibtex/json-rpc",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with opener.open(request, timeout=30) as response:
                reply = json.load(response)
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            raise ValueError(
                "Não foi possível consultar o Better BibTeX no Zotero local. "
                "Abra o Zotero ou informe um mapa CSL com -MapaZotero. "
                f"Detalhe: {error}"
            ) from error
        if reply.get("error"):
            raise ValueError(f"Erro do Better BibTeX: {reply['error']}")
        result = reply.get("result")
        if not isinstance(result, dict) or not isinstance(result.get("items"), dict):
            raise ValueError("O Better BibTeX retornou uma resposta sem metadados CSL.")
        if result.get("errors"):
            raise ValueError(f"Erro ao consultar referências no Zotero: {result['errors']}")
        items = result["items"]

    missing = sorted(keys - items.keys())
    if missing:
        raise ValueError("Citações não encontradas no Zotero: " + ", ".join(missing))

    output = []
    for key in sorted(keys):
        item = dict(items[key])
        correction = adjustments.get(key, {})
        if not isinstance(correction, dict) or {"id", "custom"} & correction.keys():
            raise ValueError(f"Ajuste bibliográfico inválido para {key}.")
        item.update(correction)
        item["id"] = key
        custom = item.get("custom")
        if (
            not isinstance(custom, dict)
            or not isinstance(custom.get("itemID"), int)
            or isinstance(custom["itemID"], bool)
            or custom["itemID"] < 1
        ):
            raise ValueError(f"A referência {key} não tem o itemID do Zotero.")
        uri = custom.get("uri")
        if not isinstance(uri, str) or not uri.startswith(
            ("http://zotero.org/", "https://zotero.org/", "https://www.zotero.org/")
        ):
            raise ValueError(f"A referência {key} não tem um URI válido do Zotero.")
        output.append(item)
    return output


def format_run(run, *, size=12, bold=None, italic=None, font=FONT):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = BLACK
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic


def add_inlines(paragraph, inlines, *, bold=False, italic=False):
    for inline in inlines:
        kind = inline["t"]
        if kind == "Str":
            run = paragraph.add_run(inline["c"])
            format_run(run, bold=bold, italic=italic)
        elif kind in {"Space", "SoftBreak", "LineBreak"}:
            run = paragraph.add_run(" " if kind != "LineBreak" else "\n")
            format_run(run, bold=bold, italic=italic)
        elif kind in {"Emph", "Strong", "SmallCaps", "Superscript", "Subscript"}:
            if kind in {"Superscript", "Subscript"}:
                start = len(paragraph.runs)
                add_inlines(paragraph, inline["c"], bold=bold, italic=italic)
                for run in paragraph.runs[start:]:
                    run.font.superscript = kind == "Superscript"
                    run.font.subscript = kind == "Subscript"
            else:
                add_inlines(
                    paragraph,
                    inline["c"],
                    bold=bold or kind == "Strong",
                    italic=italic or kind == "Emph",
                )
                if kind == "SmallCaps":
                    raise ValueError("Versalete não é suportado nos elementos preliminares.")
        elif kind == "Code":
            run = paragraph.add_run(inline["c"][1])
            format_run(run, bold=bold, italic=italic, font="Courier New")
        else:
            raise ValueError(f"Formatação não suportada nos elementos preliminares: {kind}")


def shade_cell(cell, color):
    properties = cell._tc.get_or_add_tcPr()
    previous = properties.find(qn("w:shd"))
    if previous is not None:
        properties.remove(previous)
    properties.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>'))


def schedule_header(table):
    headers = [cell.text.strip() for cell in table.rows[0].cells]
    if not headers or headers[0].casefold() not in {"ativ.", "atividade", "atividades"}:
        return None
    if len(headers) < 3 or (len(headers) - 1) % 2:
        raise ValueError("O cronograma precisa ter duas quinzenas para cada mês.")
    periods = []
    for header in headers[1:]:
        match = re.fullmatch(r"([A-Za-zÀ-ÿ]+)\s+(Q\d+)", header, flags=re.IGNORECASE)
        if not match or match.group(1).casefold()[:3] not in MONTHS:
            raise ValueError(f"Cabeçalho de cronograma não reconhecido: {header}")
        periods.append((match.group(1).casefold()[:3], match.group(2).upper()))
    for index in range(0, len(periods), 2):
        if periods[index][0] != periods[index + 1][0]:
            raise ValueError("As quinzenas consecutivas do cronograma devem pertencer ao mesmo mês.")
    if len({period for _, period in periods}) != len(periods):
        raise ValueError("O cronograma contém quinzenas duplicadas.")
    return periods


def format_schedule(table, periods):
    previous = table._tbl.getprevious()
    if previous is None or previous.tag != qn("w:p"):
        raise ValueError("O cronograma deve vir depois de um parágrafo introdutório.")
    introduction = docx.text.paragraph.Paragraph(previous, table._parent)
    introduction.paragraph_format.page_break_before = True
    introduction.paragraph_format.keep_with_next = True
    table.autofit = False
    properties = table._tbl.tblPr
    margins = properties.find(qn("w:tblCellMar"))
    if margins is not None:
        properties.remove(margins)
    properties.append(parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        '<w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
        '<w:left w:w="12" w:type="dxa"/><w:right w:w="12" w:type="dxa"/>'
        '</w:tblCellMar>'
    ))
    for index, (_, period) in enumerate(periods, 1):
        table.rows[0].cells[index].text = period
    top = OxmlElement("w:tr")
    first = OxmlElement("w:tc")
    first.append(parse_xml(f'<w:tcPr {nsdecls("w")}><w:shd w:fill="EAEAEA"/></w:tcPr>'))
    first.append(parse_xml(f'<w:p {nsdecls("w")}><w:pPr><w:jc w:val="center"/></w:pPr></w:p>'))
    top.append(first)
    for month, _ in periods[::2]:
        cell = OxmlElement("w:tc")
        cell.append(parse_xml(
            f'<w:tcPr {nsdecls("w")}><w:gridSpan w:val="2"/>'
            '<w:shd w:fill="EAEAEA"/></w:tcPr>'
        ))
        cell.append(parse_xml(
            f'<w:p {nsdecls("w")}><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="40" w:after="40"/></w:pPr>'
            f'<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>'
            f'<w:b/><w:sz w:val="15"/></w:rPr><w:t>{MONTHS[month]}</w:t></w:r></w:p>'
        ))
        top.append(cell)
    table._tbl.insert(table._tbl.index(table.rows[0]._tr), top)


def format_tables(document):
    schedules = 0
    for table in document.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        properties = table._tbl.tblPr
        old_borders = properties.find(qn("w:tblBorders"))
        if old_borders is not None:
            properties.remove(old_borders)
        properties.append(parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '</w:tblBorders>'
        ))
        periods = schedule_header(table)
        if periods is not None:
            schedules += 1
            format_schedule(table, periods)
        for row_index, row in enumerate(table.rows):
            row_properties = row._tr.get_or_add_trPr()
            if row_properties.find(qn("w:cantSplit")) is None:
                row_properties.append(OxmlElement("w:cantSplit"))
            for column_index, cell in enumerate(row.cells):
                text = cell.text.strip()
                if row_index == 0 or (periods is not None and row_index == 1):
                    shade_cell(cell, "EAEAEA")
                elif periods is not None and text.upper() == "X":
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.text = ""
                    shade_cell(cell, "5B9BD5")
                for paragraph in cell.paragraphs:
                    if periods is not None:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    paragraph.paragraph_format.first_line_indent = Cm(0)
                    paragraph.paragraph_format.line_spacing = 1.0
                    paragraph.paragraph_format.space_before = Pt(1 if periods else 2)
                    paragraph.paragraph_format.space_after = Pt(1 if periods else 2)
                    if row_index == 0 and periods is None:
                        paragraph.paragraph_format.keep_with_next = True
                    for run in paragraph.runs:
                        format_run(
                            run,
                            size=7.5 if periods else 10,
                            bold=(row_index == 0 or (
                                periods is not None and (row_index == 1 or column_index == 0)
                            )),
                        )
    if schedules > 1:
        raise ValueError("Há mais de um cronograma; a paginação precisa ser revisada.")


def format_document(document, front, config):
    headings = []
    captions = []
    for paragraph in document.paragraphs:
        style = HEADING.fullmatch(paragraph.style.name) if paragraph.style else None
        if style:
            headings.append((paragraph.text.strip(), int(style.group(1))))
        if CAPTION.match(paragraph.text.strip()):
            captions.append(paragraph.text.strip())
    if not headings or headings[0][0].casefold() != "1 introdução":
        raise ValueError("O corpo deve começar pelo título '1 Introdução'.")
    if len({text.casefold() for text, _ in headings}) != len(headings):
        raise ValueError("O artigo contém títulos duplicados; o sumário ficaria ambíguo.")
    if len({text.casefold() for text in captions}) != len(captions):
        raise ValueError("O artigo contém legendas duplicadas; a lista ficaria ambígua.")

    for section in document.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(3)
        section.left_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.right_margin = Cm(2)
        section.header_distance = Cm(1)
        section.footer_distance = Cm(1.25)
    first = document.paragraphs[0]
    first.paragraph_format.page_break_before = True

    def insert(text="", *, align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=12,
               before=0, after=0, spacing=1.5, first_indent=0, left_indent=0,
               page_break=False):
        paragraph = first.insert_paragraph_before("")
        paragraph.alignment = align
        paragraph.paragraph_format.space_before = Pt(before)
        paragraph.paragraph_format.space_after = Pt(after)
        paragraph.paragraph_format.line_spacing = spacing
        paragraph.paragraph_format.first_line_indent = Cm(first_indent)
        paragraph.paragraph_format.left_indent = Cm(left_indent)
        if page_break:
            paragraph.paragraph_format.page_break_before = True
        if text:
            format_run(paragraph.add_run(text), size=size, bold=bold)
        return paragraph

    def insert_labeled(label, nodes):
        paragraph = insert(align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing=1.0)
        format_run(paragraph.add_run(label + " "), bold=True)
        add_inlines(paragraph, nodes)

    def insert_list_entry(text, *, bold=False, indent=0, after=3, spacing=1.15):
        paragraph = insert(
            align=WD_ALIGN_PARAGRAPH.LEFT, after=after, spacing=spacing, left_indent=indent
        )
        paragraph._p.get_or_add_pPr().append(parse_xml(
            f'<w:tabs {nsdecls("w")}><w:tab w:val="right" '
            'w:leader="dot" w:pos="9072"/></w:tabs>'
        ))
        format_run(paragraph.add_run(text + "\t0"), bold=bold)

    required = ("instituicao", "campus", "curso", "local", "orientador_titulo", "apresentacao")
    for key in required:
        if not isinstance(config.get(key), str) or not config[key]:
            raise ValueError(f"Configuração obrigatória ausente: {key}")
    siglas = config.get("siglas")
    if not isinstance(siglas, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in siglas.items()
    ):
        raise ValueError("A configuração de siglas deve ser um objeto de textos.")

    insert(config["instituicao"], bold=True, before=6, after=2, spacing=1.15)
    insert(config["campus"], bold=True, after=12, spacing=1.15)
    insert(config["curso"], bold=True, after=64, spacing=1.15)
    insert(front["author"].upper(), after=84, spacing=1.15)
    insert(front["title"], bold=True, after=140, spacing=1.3)
    insert(config["local"], after=2, spacing=1.15)
    insert(front["year"], spacing=1.15)

    insert(config["instituicao"], before=6, after=2, spacing=1.15, page_break=True)
    insert(config["curso"], after=50, spacing=1.15)
    insert(front["author"].upper(), after=60, spacing=1.15)
    insert(front["title"], bold=True, after=50, spacing=1.3)
    insert(
        config["apresentacao"].format(orientador=front["advisor"]),
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        size=11,
        after=12,
        spacing=1.0,
        left_indent=8,
    )
    advisor = insert(
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=95, spacing=1.0, left_indent=8
    )
    format_run(advisor.add_run("Orientador: "), size=11, bold=True)
    format_run(
        advisor.add_run(f'{config["orientador_titulo"]} {front["advisor"]}'),
        size=11,
        bold=False,
    )
    insert(config["local"], after=2, spacing=1.15)
    insert(front["year"], spacing=1.15)

    sections = front["sections"]
    insert("RESUMO", bold=True, before=6, after=24, page_break=True)
    resumo = insert(align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=18, spacing=1.0)
    add_inlines(resumo, sections["Resumo"])
    insert_labeled("Palavras-chave:", sections["Palavras-chave"])

    insert("ABSTRACT", bold=True, before=6, after=18, page_break=True)
    english_title = insert(after=12, spacing=1.15)
    add_inlines(english_title, sections["Title"])
    abstract = insert(align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=18, spacing=1.0)
    add_inlines(abstract, sections["Abstract"])
    insert_labeled("Keywords:", sections["Keywords"])

    if captions:
        insert("LISTA DE QUADROS E TABELAS", bold=True, before=6, after=24, page_break=True)
        for caption in captions:
            insert_list_entry(caption, after=6, spacing=1.5)

    if siglas:
        insert("LISTA DE ABREVIATURAS E SIGLAS", bold=True, before=6, after=24, page_break=True)
        for abbreviation, description in siglas.items():
            paragraph = insert(align=WD_ALIGN_PARAGRAPH.LEFT, after=4)
            format_run(paragraph.add_run(f"{abbreviation} – "), bold=True)
            format_run(paragraph.add_run(description), bold=False)

    insert("SUMÁRIO", bold=True, before=6, after=18, page_break=True)
    for text, level in headings:
        insert_list_entry(text.upper() if level == 1 else text, bold=level == 1, indent=(level - 1) * 0.75)

    in_body = False
    in_references = False
    for paragraph in document.paragraphs:
        style_name = paragraph.style.name if paragraph.style else ""
        text = paragraph.text.strip()
        if text.casefold() == "1 introdução":
            in_body = True
        if not in_body:
            continue
        heading = HEADING.fullmatch(style_name)
        if heading:
            level = int(heading.group(1))
            if re.search(r"referências", text, re.IGNORECASE):
                in_references = True
                paragraph.paragraph_format.page_break_before = True
            elif re.search(r"apêndice", text, re.IGNORECASE):
                in_references = False
                paragraph.paragraph_format.page_break_before = True
            elif re.match(r"^\d+\s+considerações", text, re.IGNORECASE):
                paragraph.paragraph_format.page_break_before = True
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.left_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.5
            paragraph.paragraph_format.space_before = Pt(18 if level == 1 else 12)
            paragraph.paragraph_format.space_after = Pt(6)
            for run in paragraph.runs:
                if level == 1:
                    run.text = run.text.upper()
                format_run(run, bold=True)
            continue
        if paragraph._p.find(qn("m:oMathPara")) is not None:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.5
            paragraph.paragraph_format.space_before = Pt(6)
            paragraph.paragraph_format.space_after = Pt(6)
            continue
        if style_name == "Source Code" or "You are the memory-state updater" in text:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.left_indent = Cm(0.5)
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_before = Pt(6)
            paragraph.paragraph_format.space_after = Pt(6)
            for run in paragraph.runs:
                format_run(run, size=9.5, font="Courier New")
            continue
        if style_name == "Bibliography" or (in_references and text):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.left_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_before = Pt(0)
            paragraph.paragraph_format.space_after = Pt(12)
            for run in paragraph.runs:
                format_run(run)
            continue
        if CAPTION.match(text):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_before = Pt(12)
            paragraph.paragraph_format.space_after = Pt(4)
            paragraph.paragraph_format.keep_with_next = text.startswith("Quadro ")
            for run in paragraph.runs:
                format_run(run, size=10, bold=True)
            continue
        if text.startswith("Fonte:"):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_before = Pt(4)
            paragraph.paragraph_format.space_after = Pt(12)
            for run in paragraph.runs:
                format_run(run, size=10, bold=False)
            continue
        if (text.startswith("(") and text.endswith(")") and len(text) < 80) or (
            "=" in text and re.search(r"\([1-6]\)", text)
        ):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.5
            paragraph.paragraph_format.space_before = Pt(6)
            paragraph.paragraph_format.space_after = Pt(6)
            for run in paragraph.runs:
                format_run(run)
            continue
        if re.match(r"^([a-d]\)|\d+\.)", text) or "List" in style_name or "Compact" in style_name:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.left_indent = Cm(1.25)
            paragraph.paragraph_format.line_spacing = 1.5
            paragraph.paragraph_format.space_before = Pt(0)
            paragraph.paragraph_format.space_after = Pt(2)
            for run in paragraph.runs:
                format_run(run)
            continue
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.first_line_indent = Cm(0 if text.startswith("em que ") else 1.25)
        paragraph.paragraph_format.line_spacing = 1.5
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        for run in paragraph.runs:
            format_run(run)

    format_tables(document)
    return len(headings), len(captions)


def generate(args):
    for path, description in (
        (args.entrada, "Markdown do artigo"),
        (args.cabecalho, "Modelo de cabeçalho"),
        (args.config, "Configuração"),
        (args.pandoc, "Pandoc"),
        (args.csl, "Estilo CSL"),
        (HERE / "zotero_abnt_unitins.lua", "Filtro Zotero"),
    ):
        require_file(path, description)
    if not args.trabalho.is_dir():
        raise ValueError(f"Diretório de trabalho não encontrado: {args.trabalho}")
    if args.saida.exists():
        raise ValueError(f"O arquivo de saída já existe: {args.saida}")

    source = args.entrada.read_text(encoding="utf-8-sig")
    introduction = INTRODUCTION.search(source)
    if introduction is None:
        raise ValueError("O Markdown precisa conter o título '# 1 Introdução'.")
    snapshot = args.trabalho / "fonte.md"
    snapshot.write_text(source, encoding="utf-8")
    ast = pandoc_ast(args.pandoc, snapshot)
    front = front_matter(ast)
    groups = collect_citation_groups(front["body_blocks"])
    keys = {key for group in groups for key in group}
    config = json.loads(args.config.read_text(encoding="utf-8"))
    adjustments = config.get("ajustes_zotero", {})
    if not isinstance(adjustments, dict):
        raise ValueError("A configuração de ajustes Zotero deve ser um objeto.")
    items = zotero_items(keys, args.mapa_zotero, adjustments)
    item_path = args.trabalho / "zotero_items.json"
    item_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    body = "---\nlang: pt-BR\n---\n\n" + source[introduction.start():]
    body = re.sub(
        r"^((?:Tabela|Quadro)\s+\d+\s+[–—-]\s+[^\n]+)\n(Fonte:)",
        r"\1\n\n\2",
        body,
        flags=re.MULTILINE,
    )
    body_path = args.trabalho / "corpo.md"
    body_path.write_text(body, encoding="utf-8")
    base_path = args.trabalho / "corpo.docx"
    environment = os.environ.copy()
    environment["UNITINS_ZOTERO_ITEMS"] = str(item_path)
    resource_path = os.pathsep.join((str(args.entrada.parent.resolve()), str(args.trabalho)))
    subprocess.run(
        [
            str(args.pandoc),
            str(body_path),
            f"--reference-doc={args.cabecalho}",
            f"--csl={args.csl}",
            f"--bibliography={item_path}",
            f"--lua-filter={HERE / 'zotero_abnt_unitins.lua'}",
            f"--resource-path={resource_path}",
            "-o",
            str(base_path),
        ],
        check=True,
        env=environment,
    )
    document = docx.Document(base_path)
    headings, captions = format_document(document, front, config)
    document.save(args.saida)
    print(
        f"Preparado: {len(groups)} grupos de citação, {len(keys)} referências, "
        f"{headings} títulos e {captions} legendas."
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        generate(parse_arguments())
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Erro ao gerar o artigo: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
