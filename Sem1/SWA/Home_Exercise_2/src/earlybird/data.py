"""Small, explicit file formats shared by the pipeline and the dashboard."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RESULTS = ROOT / "experiments"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def load_sources():
    return read_json(DATA / "source_requirements.json")


def load_clauses():
    return read_json(DATA / "clauses.json")


def dataset(name="reviewed"):
    if name == "reviewed":
        return load_clauses()
    if name == "source":
        # These records deliberately retain the original channels and granularity.
        return [{"id": r["id"], "source": r["id"], "text": r["text"]}
                for r in load_sources()["requirements"] if r["baseline_eligible"]]
    raise ValueError(f"Unknown dataset: {name}")


def validate_inventory():
    source = load_sources()
    rows = source["requirements"]
    clauses = load_clauses()
    assert [r["number"] for r in rows] == list(range(1, 45)), "Expected all 44 statements"
    assert len({r["id"] for r in clauses}) == len(clauses), "Duplicate clause identifiers"
    sources = {r["id"]: r for r in rows}
    for row in rows:
        assert row["disposition"] and row["rationale"]
    for clause in clauses:
        assert clause["source"] in sources
        assert clause["source_quote"] in sources[clause["source"]]["text"], clause["id"]
        assert clause["text"].strip() and clause["review_note"]
    represented = {c["source"] for c in clauses}
    for row in rows:
        assert row["id"] in represented or row["disposition"] in {
            "quality constraint", "superseded", "physical process", "platform constraint", "actor context"
        }, f"Unaccounted source {row['id']}"
    return {"source_statements": len(rows), "reviewed_clauses": len(clauses),
            "source_baseline": len(dataset("source")), "source_sha256": source["sha256"]}
