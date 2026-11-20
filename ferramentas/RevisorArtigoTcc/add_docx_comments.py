import json
import shutil
import sys
from difflib import SequenceMatcher
from pathlib import Path

from docx import Document


CRITICAL_ANCHORS = {
    12: ["2.7 Comparação estatística de modelos"],
    16: ["Como o acúmulo irrestrito"],
    25: ["analisar o perfil de erro dos escritores"],
    55: ["[GS1]", "teste de Friedman"],
    57: ["O valor p expressa"],
    60: ["Quadro 1 – Comparação entre trabalhos relacionados"],
    61: ["Quadro 1 – Comparação entre trabalhos relacionados", "Trabalho", "Vantagens"],
    66: ["Este estudo segue um delineamento experimental"],
    71: ["c) Estudos de controle"],
    76: ["g) 7. Extração", "Extração e síntese"],
    80: ["Os artefatos da revisão"],
    105: ["Qwen3-0.6B Diffusion BD3LM"],
    139: ["Quadro 5 – Métricas de avaliação"],
    163: ["Relação entre validade sintática e fidelidade semântica"],
    183: ["Tabela 1 – Cronograma"],
    201: ["HWANG, Tao; DIAO", "AMU:Admission"],
    232: ["Quadro 7 – Artefatos da revisão"],
}


def normalized(value: str) -> str:
    return " ".join(value.replace("\u00a0", " ").split()).lower()


def find_paragraph(document: Document, anchors: list[str]):
    for paragraph in document.paragraphs:
        text = normalized(paragraph.text)
        if any(normalized(anchor) in text for anchor in anchors):
            return paragraph
    return None


def document_paragraphs(document: Document):
    seen = set()

    def add(paragraph):
        key = id(paragraph._p)
        if key not in seen:
            seen.add(key)
            return paragraph
        return None

    for paragraph in document.paragraphs:
        result = add(paragraph)
        if result is not None:
            yield result

    def table_paragraphs(table):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    result = add(paragraph)
                    if result is not None:
                        yield result
                for nested_table in cell.tables:
                    yield from table_paragraphs(nested_table)

    for table in document.tables:
        yield from table_paragraphs(table)


def find_paragraph_by_text(document: Document, text: str):
    target = normalized(text)
    if not target:
        return None

    candidates = [
        (SequenceMatcher(None, target, normalized(paragraph.text)).ratio(), paragraph)
        for paragraph in document_paragraphs(document)
        if normalized(paragraph.text)
    ]
    candidates.sort(key=lambda candidate: candidate[0], reverse=True)

    if not candidates or candidates[0][0] < 0.90:
        return None
    if len(candidates) > 1 and candidates[0][0] - candidates[1][0] < 0.05:
        return None
    return candidates[0][1]


def find_table(document: Document, anchors: list[str]):
    for table in document.tables:
        text = normalized("\n".join(
            cell.text
            for row in table.rows
            for cell in row.cells
        ))
        if any(normalized(anchor) in text for anchor in anchors):
            return table
    return None


def mark_first_available(document: Document, anchors: list[str]) -> int:
    paragraph = find_paragraph(document, anchors)
    if paragraph is not None:
        return 1 if paragraph.runs else 0

    table = find_table(document, anchors)
    if table is not None:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.runs:
                        return 1
    return 0


def add_comment_to_paragraph(
    document: Document,
    paragraph,
    text: str,
    author: str,
    initials: str,
) -> bool:
    runs = [run for run in paragraph.runs if run.text]
    if not runs:
        return False
    document.add_comment(runs=runs[:1], text=text, author=author, initials=initials)
    return True


def add_comments(
    source_docx: str,
    output_docx: str,
    observations_json: str,
    author: str = "Copilot — Revisão do TCC",
    initials: str = "CP",
) -> dict:
    source = Path(source_docx).resolve()
    output = Path(output_docx).resolve()
    observations = json.loads(Path(observations_json).read_text(encoding="utf-8"))

    if source == output:
        raise ValueError("Source and output DOCX paths must be different.")

    document = Document(str(source))
    existing_comments_preserved = len(document.comments)
    critical_items = {
        int(item["id"]): item
        for item in observations["items"]
        if item["status"] == "CRITICO"
    }

    comments_added = 0
    missed = []

    for item_id, item in sorted(critical_items.items()):
        anchors = CRITICAL_ANCHORS.get(item_id, [])
        paragraph = find_paragraph_by_text(document, item["text"])
        if paragraph is None and anchors:
            paragraph = find_paragraph(document, anchors)
        matched = False

        if paragraph is not None:
            matched = add_comment_to_paragraph(
                document,
                paragraph,
                (
                    f"CRÍTICO #{item_id:03d} — páginas {item['pageStart']}"
                    f"{'-' + str(item['pageEnd']) if item['pageEnd'] != item['pageStart'] else ''}\n"
                    f"Códigos: {', '.join(item['codes'])}\n"
                    f"Observação: {item['observation']}\n"
                    f"Sugestão: {item['suggestion'] or 'Revisar o trecho e corrigir o problema identificado.'}"
                ),
                author,
                initials,
            )

        if not matched:
            table = find_table(document, anchors)
            if table is not None:
                for row in table.rows:
                    for cell in row.cells:
                        for cell_paragraph in cell.paragraphs:
                            if add_comment_to_paragraph(
                                document,
                                cell_paragraph,
                                (
                                    f"CRÍTICO #{item_id:03d} — páginas {item['pageStart']}"
                                    f"{'-' + str(item['pageEnd']) if item['pageEnd'] != item['pageStart'] else ''}\n"
                                    f"Códigos: {', '.join(item['codes'])}\n"
                                    f"Observação: {item['observation']}\n"
                                    f"Sugestão: {item['suggestion'] or 'Revisar o bloco e corrigir o problema identificado.'}"
                                ),
                                author,
                                initials,
                            ):
                                matched = True
                                break
                        if matched:
                            break
                    if matched:
                        break

        if matched:
            comments_added += 1
        else:
            missed.append({
                "id": item_id,
                "reason": "Trecho crítico não localizado com correspondência segura no DOCX",
            })

    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output))

    return {
        "source": str(source),
        "output": str(output),
        "commentsAdded": comments_added,
        "existingCommentsPreserved": existing_comments_preserved,
        "missed": missed,
    }


if __name__ == "__main__":
    if len(sys.argv) not in (4, 6):
        raise SystemExit(
            "Uso: add_docx_comments.py <source.docx> <output.docx> <observacoes.json> "
            "[<autor> <iniciais>]"
        )
    author = sys.argv[4] if len(sys.argv) == 6 else "Copilot — Revisão do TCC"
    initials = sys.argv[5] if len(sys.argv) == 6 else "CP"
    result = add_comments(sys.argv[1], sys.argv[2], sys.argv[3], author, initials)
    print(json.dumps(result, ensure_ascii=False))
