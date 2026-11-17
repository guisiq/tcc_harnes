import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.shared import Cm, Pt


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import gerar_artigo_unitins as generator
import validar_artigo_unitins as validator


def text(value):
    return [{"t": "Str", "c": value}]


def labeled(label, value):
    return {
        "t": "Para",
        "c": [
            {"t": "Strong", "c": text(label + ":")},
            {"t": "Space"},
            {"t": "Str", "c": value},
        ],
    }


def article_ast():
    return {
        "meta": {
            "title": {"t": "MetaInlines", "c": text("Um título")},
            "subtitle": {"t": "MetaInlines", "c": text("um subtítulo")},
            "date": {"t": "MetaInlines", "c": text("Palmas, 2027")},
            "author": {
                "t": "MetaList",
                "c": [
                    {"t": "MetaInlines", "c": text("LOPES, Guilherme")},
                    {"t": "MetaInlines", "c": text("COELHO, Alex")},
                ],
            },
        },
        "blocks": [
            labeled("Resumo", "Texto do resumo."),
            labeled("Palavras-chave", "Memória."),
            labeled("Title", "A title"),
            labeled("Abstract", "Abstract text."),
            labeled("Keywords", "Memory."),
            {
                "t": "Header",
                "c": [1, ["introducao", [], []], text("1 Introdução")],
            },
        ],
    }


def citation(key, *, prefix=None, suffix=None):
    return {
        "citationId": key,
        "citationMode": {"t": "NormalCitation"},
        "citationPrefix": prefix or [],
        "citationSuffix": suffix or [],
    }


def document_with_schedule():
    document = Document()
    document.add_paragraph("O cronograma segue.")
    document.add_paragraph("Tabela 1 – Cronograma de atividades")
    table = document.add_table(rows=2, cols=5)
    for cell, label in zip(table.rows[0].cells, ["Ativ.", "Set Q1", "Set Q2", "Out Q3", "Out Q4"]):
        cell.text = label
    for cell, value in zip(table.rows[1].cells, ["1-", "X", "", "", "X"]):
        cell.text = value
    return document


class FrontMatterTests(unittest.TestCase):
    def test_metadata_and_sections_are_taken_from_source(self):
        result = generator.front_matter(article_ast())
        self.assertEqual(result["title"], "UM TÍTULO: UM SUBTÍTULO")
        self.assertEqual(result["year"], "2027")
        self.assertEqual(result["author"], "Guilherme Lopes")
        self.assertEqual(result["advisor"], "Alex Coelho")
        self.assertEqual(generator.inline_text(result["sections"]["Title"]), "A title")

    def test_unlabeled_extra_paragraph_is_not_silently_discarded(self):
        ast = article_ast()
        ast["blocks"].insert(1, {"t": "Para", "c": text("Outro parágrafo.")})
        with self.assertRaisesRegex(ValueError, "único parágrafo"):
            generator.front_matter(ast)

    def test_wrong_first_heading_is_rejected(self):
        ast = article_ast()
        ast["blocks"][-1]["c"][2] = text("1 Contexto")
        with self.assertRaisesRegex(ValueError, "primeiro título"):
            generator.front_matter(ast)


class CitationTests(unittest.TestCase):
    def test_collects_nested_groups_without_comment_placeholders(self):
        ast = [{"t": "Para", "c": [
            {"t": "Cite", "c": [[citation("one"), citation("two")], []]}
        ]}]
        self.assertEqual(generator.collect_citation_groups(ast), [["one", "two"]])

    def test_rejects_unsupported_citation_locator(self):
        ast = {"t": "Cite", "c": [[citation("one", suffix=text(", p. 12"))], []]}
        with self.assertRaisesRegex(ValueError, "indicação de página"):
            generator.collect_citation_groups(ast)

    def test_cache_requires_every_zotero_key_and_preserves_adjustments(self):
        item = {
            "id": "one",
            "title": "Original",
            "custom": {
                "itemID": 3,
                "uri": "http://zotero.org/users/local/example/items/ABC",
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "items.json"
            path.write_text(json.dumps([item]), encoding="utf-8")
            result = generator.zotero_items({"one"}, path, {"one": {"title": "Corrigido"}})
            self.assertEqual(result[0]["title"], "Corrigido")
            self.assertEqual(result[0]["custom"], item["custom"])
            with self.assertRaisesRegex(ValueError, "two"):
                generator.zotero_items({"one", "two"}, path, {})
            with self.assertRaisesRegex(ValueError, "Ajuste bibliográfico inválido"):
                generator.zotero_items({"one"}, path, {"one": {"custom": {}}})

    def test_rejects_invalid_zotero_item_identifier(self):
        item = {
            "id": "one",
            "custom": {"itemID": True, "uri": "http://zotero.org/users/local/example/items/ABC"},
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "items.json"
            path.write_text(json.dumps([item]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "itemID"):
                generator.zotero_items({"one"}, path, {})


class ScheduleTests(unittest.TestCase):
    def test_months_and_selections_come_from_table(self):
        original = document_with_schedule()
        formatted = document_with_schedule()
        generator.format_tables(formatted)
        table = formatted.tables[0]
        self.assertEqual(table.rows[0].cells[1].text, "set.")
        self.assertEqual(table.rows[0].cells[3].text, "out.")
        self.assertTrue(formatted.paragraphs[0].paragraph_format.page_break_before)
        borders = table._tbl.tblPr.find(generator.qn("w:tblBorders"))
        for side in ("left", "right"):
            self.assertEqual(borders.find(generator.qn(f"w:{side}")).get(generator.qn("w:val")), "nil")
        self.assertEqual([cell.text for cell in table.rows[1].cells[1:]], ["Q1", "Q2", "Q3", "Q4"])
        self.assertEqual(validator.verify_tables(original, formatted), 2)

    def test_validator_detects_a_missing_selection(self):
        original = document_with_schedule()
        formatted = document_with_schedule()
        generator.format_tables(formatted)
        generator.shade_cell(formatted.tables[0].rows[2].cells[1], "FFFFFF")
        with self.assertRaisesRegex(ValueError, "seleção"):
            validator.verify_tables(original, formatted)

    def test_rejects_unpaired_months(self):
        document = document_with_schedule()
        document.tables[0].rows[0].cells[2].text = "Out Q2"
        with self.assertRaisesRegex(ValueError, "mesmo mês"):
            generator.format_tables(document)


class FormattingTests(unittest.TestCase):
    def formatted_document(self):
        document = Document()
        document.add_heading("1 Introdução", level=1)
        document.add_paragraph("Texto do artigo.")
        document.add_paragraph("e) Etapa da revisão.")
        document.add_paragraph("em que o estado representa a memória.")
        document.add_paragraph("Figura 1 – Fluxo da pesquisa")
        document.add_heading("Referências", level=1)
        document.add_paragraph("Uma referência.")
        document.add_heading("Apêndice A – Material complementar", level=1)
        notes = Part(
            PackURI("/word/footnotes.xml"), CT.WML_FOOTNOTES,
            b'<w:footnotes xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            b'<w:footnote w:id="1"><w:p><w:pPr><w:pStyle w:val="FootnoteText"/>'
            b'</w:pPr><w:r><w:t>Nota.</w:t></w:r></w:p></w:footnote></w:footnotes>',
            document.part.package,
        )
        document.part.relate_to(notes, RT.FOOTNOTES)
        config = json.loads((TOOLS / "artigo_unitins_config.json").read_text(encoding="utf-8"))
        generator.format_document(document, generator.front_matter(article_ast()), config)
        return document

    def test_detects_margins_and_body_spacing_regressions(self):
        for regression in ("margem", "entrelinha"):
            with self.subTest(regression=regression):
                document = self.formatted_document()
                validator.verify_formatting(document)
                if regression == "margem":
                    document.sections[0].left_margin = Cm(2)
                else:
                    next(p for p in document.paragraphs if p.text == "Texto do artigo.").paragraph_format.line_spacing = 1.0
                with self.assertRaisesRegex(ValueError, "Formatação Unitins"):
                    validator.verify_formatting(document)

    def test_detects_figure_caption_and_footnote_regressions(self):
        for regression in ("legenda", "nota"):
            with self.subTest(regression=regression):
                document = self.formatted_document()
                if regression == "legenda":
                    paragraph = next(p for p in document.paragraphs if p.text == "Figura 1 – Fluxo da pesquisa")
                    paragraph.runs[0].font.size = Pt(12)
                else:
                    document.styles["Footnote Text"].font.size = Pt(12)
                with self.assertRaisesRegex(ValueError, "Formatação Unitins"):
                    validator.verify_formatting(document)

    def test_detects_abstract_and_table_header_regressions(self):
        document = self.formatted_document()
        paragraph = next(p for p in document.paragraphs if p.text == "Abstract text.")
        paragraph.runs[0].font.size = Pt(12)
        with self.assertRaisesRegex(ValueError, "resumo e abstract"):
            validator.verify_formatting(document)
        document = self.formatted_document()
        table = document.add_table(rows=2, cols=2)
        generator.format_tables(document)
        validator.verify_formatting(document)
        properties = table.rows[0]._tr.trPr
        properties.remove(properties.find(generator.qn("w:tblHeader")))
        with self.assertRaisesRegex(ValueError, "cabeçalho da tabela"):
            validator.verify_formatting(document)

    def test_accepts_word_normalizing_the_footnote_style_name(self):
        document = self.formatted_document()
        style = document.styles["Footnote Text"]
        style.name = "Texto de nota de rodapé"
        style.element.set(generator.qn("w:styleId"), "Textodenotaderodape")
        notes = document.part.part_related_by(RT.FOOTNOTES)
        notes._blob = notes.blob.replace(b'"FootnoteText"', b'"Textodenotaderodape"')
        validator.verify_formatting(document)

    def test_resolves_inherited_footnote_font_and_document_alignment(self):
        document = self.formatted_document()
        style = document.styles["Footnote Text"]
        style.font.name = None
        style.paragraph_format.alignment = None
        validator.verify_formatting(document)
        defaults = document.styles.element.xpath("w:docDefaults/w:pPrDefault/w:pPr")[0]
        alignment = generator.OxmlElement("w:jc")
        alignment.set(generator.qn("w:val"), "both")
        defaults.append(alignment)
        with self.assertRaisesRegex(ValueError, "notas devem"):
            validator.verify_formatting(document)

    def test_resolves_body_font_size_inherited_after_word_save(self):
        document = self.formatted_document()
        paragraph = next(p for p in document.paragraphs if p.text == "Texto do artigo.")
        for run in paragraph.runs:
            run.font.size = None
        validator.verify_formatting(document)
        paragraph.style.font.size = Pt(11)
        with self.assertRaisesRegex(ValueError, "corpo fora do padrão"):
            validator.verify_formatting(document)

    def test_resolves_omitted_zero_indent_after_word_save(self):
        document = self.formatted_document()
        paragraph = next(p for p in document.paragraphs if p.text.startswith("em que "))
        paragraph.paragraph_format.first_line_indent = None
        validator.verify_formatting(document)
        paragraph.style.paragraph_format.first_line_indent = Cm(1.25)
        with self.assertRaisesRegex(ValueError, "corpo fora do padrão"):
            validator.verify_formatting(document)

    def test_detects_misplaced_table_caption_and_closed_sides(self):
        document = self.formatted_document()
        caption = document.add_paragraph("Tabela 1 – Dados do experimento")
        table = document.add_table(rows=2, cols=3)
        generator.format_tables(document)
        for run in caption.runs:
            run.font.size = Pt(10)
        caption.alignment = generator.WD_ALIGN_PARAGRAPH.CENTER
        caption.paragraph_format.line_spacing = 1.0
        validator.verify_formatting(document)
        table._tbl.addnext(caption._p)
        with self.assertRaisesRegex(ValueError, "acima do elemento"):
            validator.verify_formatting(document)
        table._tbl.addprevious(caption._p)
        border = table._tbl.tblPr.find(generator.qn("w:tblBorders")).find(generator.qn("w:left"))
        border.set(generator.qn("w:val"), "single")
        with self.assertRaisesRegex(ValueError, "fechamento lateral"):
            validator.verify_formatting(document)


@unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 não encontrado")
class OutputProtectionTests(unittest.TestCase):
    def test_existing_output_is_not_overwritten_without_force(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "existente.docx"
            path.write_bytes(b"conteudo existente")
            result = subprocess.run(
                [
                    "pwsh", "-NoLogo", "-NoProfile", "-File",
                    str(TOOLS / "gerar-artigo-unitins.ps1"), "-Saida", str(path),
                ],
                capture_output=True,
                encoding="utf-8",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(path.read_bytes(), b"conteudo existente")
            self.assertIn("já existe", result.stderr)


if __name__ == "__main__":
    unittest.main()
