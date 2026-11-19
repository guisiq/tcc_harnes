import json
import sys
from pathlib import Path

import pymupdf


def render_pages(pdf_path: str, output_dir: str, dpi: int = 150, max_pages: int | None = None) -> dict:
    pdf = Path(pdf_path).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(str(pdf)) as document:
        limit = len(document) if max_pages is None else min(max_pages, len(document))
        pages = []
        for page_index in range(limit):
            page = document[page_index]
            scale = dpi / 72.0
            pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
            path = out / f"page-{page_index + 1:03d}.png"
            pix.save(str(path))
            pages.append({
                "page": page_index + 1,
                "path": str(path),
                "width": pix.width,
                "height": pix.height,
            })
        return {
            "pdf": str(pdf),
            "dpi": dpi,
            "pageCount": limit,
            "pages": pages,
        }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Uso: render_pdf_pages.py <arquivo.pdf> <diretorio> [dpi] [max-pages]")
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    max_pages = int(sys.argv[4]) if len(sys.argv) > 4 and int(sys.argv[4]) > 0 else None
    print(json.dumps(render_pages(sys.argv[1], sys.argv[2], dpi, max_pages), ensure_ascii=False))
