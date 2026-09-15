import json
import re
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
paragraphs = []
with pymupdf.open(sys.argv[1]) as document:
    limit = min(int(sys.argv[2]), len(document))
    for page_index in range(limit):
        order = 0
        for block in document[page_index].get_text("blocks", sort=False):
            if block[6] != 0:
                continue
            text = re.sub(
                r"([A-Za-z]+)-\r?\n(?=[a-z])",
                lambda match: match[1] + ("-" if match[1].isupper() or match[1].lower() in
                    {"single", "multi", "long", "short", "self", "cross", "task", "state", "real", "well", "fine"} else ""),
                block[4],
            )
            text = " ".join(text.split())
            if text:
                paragraphs.append({"PageNumber": page_index + 1, "Order": order, "Text": text,
                                   "Bounds": [round(value, 2) for value in block[:4]]})
                order += 1
print(json.dumps(paragraphs, ensure_ascii=False))