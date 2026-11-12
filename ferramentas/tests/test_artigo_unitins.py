import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document


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
        self.assertEqual(table.rows[0].cells[1].text, "Setembro")
        self.assertEqual(table.rows[0].cells[3].text, "Outubro")
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
