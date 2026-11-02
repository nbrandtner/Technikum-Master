"""One-time, auditable import of the supplied PDF; no network or LLM rewriting.

Whitespace is collapsed. Wording and punctuation remain as extracted by pypdf.
The explicit clause curation lives in data/curation.json and is reviewable separately.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pypdf import PdfReader
from earlybird.data import DATA, read_json, write_json, validate_inventory

HEADINGS = ["Placing an Order on the Phone", "Packaging an Order", "Delivering an Order",
            "Status Inquiry", "Canceling an Order", "Placing and Canceling an Order by Text Message",
            "Payment", "Business Reporting"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pdf", type=Path)
    args = p.parse_args()
    reader = PdfReader(args.pdf)
    rows = []
    for page_no, (page, first, last) in enumerate(zip(reader.pages, [1, 14, 32], [13, 31, 44]), 1):
        text = re.sub(r"\s+", " ", page.extract_text()).strip()
        positions = []
        cursor = 0
        for number in range(first, last + 1):
            m = re.search(rf"(?<!\S){number}\.\s+", text[cursor:])
            if m is None:
                raise ValueError(f"Missing R{number}")
            start = cursor + m.start()
            end = cursor + m.end()
            positions.append((number, start, end))
            cursor = end
        for i, (number, _, start) in enumerate(positions):
            end = positions[i+1][1] if i+1 < len(positions) else len(text)
            body = text[start:end].strip()
            for heading in HEADINGS:
                if body.endswith(heading):
                    body = body[:-len(heading)].strip()
            rows.append({"id": f"R{number:02d}", "number": number, "page": page_no, "text": body})
    curation = read_json(DATA / "curation.json")
    for row in rows:
        row.update(curation["dispositions"].get(row["id"], {
            "disposition": "retained", "rationale": "Business obligation remains applicable under R32.",
            "baseline_eligible": True
        }))
    source = {"title": "Early Bird Management System Requirements", "version": "1.50",
              "filename": args.pdf.name, "sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
              "extraction": "pypdf; whitespace collapsed; inter-paragraph headings removed",
              "requirements": rows}
    write_json(DATA / "source_requirements.json", source)
    clauses = []
    source_map = {r["id"]: r for r in rows}
    for c in curation["clauses"]:
        row = dict(c)
        row["source"] = c["id"].split(".")[0]
        row["page"] = source_map[row["source"]]["page"]
        row["source_quote"] = c.get("source_quote", source_map[row["source"]]["text"])
        clauses.append(row)
    write_json(DATA / "clauses.json", clauses)
    print(validate_inventory())


if __name__ == "__main__":
    main()
