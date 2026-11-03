"""The complete experiment: model -> database -> saved evidence -> report."""
from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import version

import numpy as np
from sklearn.metrics import adjusted_rand_score

from .analysis import cluster_cards, display_evidence, score, summarize
from .data import DATA, RESULTS, ROOT, dataset, digest, read_json, validate_inventory, write_json
from .database import Database
from .embeddings import DEFAULT_MODEL, Encoder


def run_experiment(k_min=2, k_max=10, seeds=10, paraphrases=True, model=DEFAULT_MODEL):
    if not 2 <= k_min <= k_max < min(len(dataset("source")), len(dataset("reviewed"))):
        raise ValueError("k must be between 2 and the smaller dataset size minus one")
    if seeds < 1:
        raise ValueError("At least one seed is required")
    coverage = validate_inventory()
    db = Database()
    try:
        database_version = db.status()
        print(f"Database ready: {database_version}", flush=True)
        encoder = Encoder(model)
        bundle = {"format": 1, "created_utc": datetime.now(timezone.utc).isoformat(),
                  "engine": "Neo4j GDS K-Means", "model": encoder.info,
                  "database": database_version, "coverage": coverage,
                  "parameters": {"k_min": k_min, "k_max": k_max, "seeds": list(range(seeds)),
                                 "initialSampler": "kmeans++", "maxIterations": 100,
                                 "deltaThreshold": 0.00001, "concurrency": 1, "numberOfRestarts": 1},
                  "versions": {p: version(p) for p in ["numpy", "scikit-learn", "neo4j"]},
                  "cluster_query": (ROOT / "db" / "cluster.cypher").read_text(encoding="utf-8"),
                  "datasets": {}, "paraphrases": []}

        def cluster_set(records, vectors, fingerprint, name, variant, ks, seed_values):
            index = db.ingest(records, vectors, fingerprint)
            graph = db.project(fingerprint)
            runs = []
            ids = [r["id"] for r in records]
            try:
                for k in ks:
                    for seed in seed_values:
                        labels = db.cluster(graph, ids, k, seed)
                        run = {"id": digest({"set": fingerprint, "k": k, "seed": seed,
                                             "parameters": bundle["parameters"], "query": bundle["cluster_query"]})[:24],
                               "dataset": name, "variant": variant, "k": k, "seed": seed,
                               "ids": ids, "labels": labels, **score(vectors, labels)}
                        db.save_run(run, fingerprint)
                        if not db.verify_run(run):
                            raise ValueError("Persisted database membership differs from the returned run")
                        runs.append(run)
                    print(f"  {name}/{variant}: k={k}, {len(seed_values)} seeds", flush=True)
            finally:
                db.drop(graph)
            return runs, index

        for name in ["source", "reviewed"]:
            records = dataset(name)
            vectors, fingerprint = encoder.encode(records)
            runs, index = cluster_set(records, vectors, fingerprint, name, "original",
                                      range(k_min, k_max+1), range(seeds))
            summary = summarize(runs)
            # This is a geometric reference, not a declaration of architectural optimality.
            suggested_k = max(summary, key=lambda row: row["mean_silhouette"])["k"]
            best = max([r for r in runs if r["k"] == suggested_k], key=lambda r: r["silhouette"])
            for run in runs:
                run["cards"] = cluster_cards(records, vectors, run["labels"])
            bundle["datasets"][name] = {"records": records, "fingerprint": fingerprint,
                "index": index, "runs": runs, "summary": summary, "suggested_k": suggested_k,
                "reference_run": best["id"], **display_evidence(records, vectors)}
            write_json(RESULTS / "checkpoint.json", bundle)
            if name == "reviewed":
                reviewed_records, reviewed_vectors = records, vectors

        if paraphrases:
            reviewed = bundle["datasets"]["reviewed"]
            top_ks = [s["k"] for s in sorted(reviewed["summary"], key=lambda r: -r["mean_silhouette"])[:3]]
            for variant in read_json(DATA / "paraphrases.json"):
                records = [dict(r) for r in reviewed_records]
                item = next(r for r in records if r["id"] == variant["clause"])
                item["text"] = variant["text"]
                vectors, fingerprint = encoder.encode(records)
                runs, _ = cluster_set(records, vectors, fingerprint, "reviewed", variant["id"],
                                      top_ks, range(seeds))
                for run in runs:
                    base = next(r for r in reviewed["runs"] if r["k"] == run["k"] and r["seed"] == run["seed"])
                    run["baseline_run"] = base["id"]
                    run["ari_to_same_seed"] = float(adjusted_rand_score(base["labels"], run["labels"]))
                bundle["paraphrases"].append({**variant, "fingerprint": fingerprint, "runs": runs})
                write_json(RESULTS / "checkpoint.json", bundle)

        # Exercise both a populated index and exact tiny-corpus vector inspection.
        reviewed = bundle["datasets"]["reviewed"]
        indexes = db.query("SHOW VECTOR INDEXES YIELD name, state, populationPercent RETURN name, state, populationPercent")
        nearest = db.nearest(reviewed["fingerprint"], "R29.a")
        bundle["verification"] = {"vector_indexes": indexes, "example_query": "R29.a",
            "example_neighbors": nearest, "persisted_memberships_verified": True,
            "neighbor_score_convention": "raw cosine [-1,1]; Neo4j values converted via 2*score-1",
            "base_runs": sum(len(d["runs"]) for d in bundle["datasets"].values()),
            "paraphrase_runs": sum(len(v["runs"]) for v in bundle["paraphrases"])}
        temporary = RESULTS / "latest.tmp.json"
        write_json(temporary, bundle)
        temporary.replace(RESULTS / "latest.json")
        render_report(bundle)
        print(f"Saved genuine experiment evidence to {RESULTS / 'latest.json'}", flush=True)
        return bundle
    finally:
        db.close()


def render_report(bundle):
    lines = ["# EarlyBird Boundary Lab: experiment report", "",
             f"Generated from actual {bundle['engine']} runs at {bundle['created_utc']}.", "",
             f"Model: `{bundle['model']['model']}` at revision `{bundle['model']['revision']}`.",
             f"Database: Neo4j {bundle['database']['neo4j']}; GDS {bundle['database']['gds']}.", "",
             "The source baseline and reviewed clauses have different granularity and scope; their scores are not a controlled before/after comparison.", ""]
    for name, data in bundle["datasets"].items():
        lines += [f"## {name.title()} dataset", "", f"{len(data['records'])} records.", "",
                  "| k | Mean Euclidean silhouette | Seed agreement (ARI) | Mean singletons |",
                  "|---|---:|---:|---:|"]
        for row in data["summary"]:
            lines.append(f"| {row['k']} | {row['mean_silhouette']:.4f} | {row['seed_agreement']:.4f} | {row['mean_singletons']:.2f} |")
        run = next(r for r in data["runs"] if r["id"] == data["reference_run"])
        lines += ["", f"Geometric reference: k={run['k']}, seed={run['seed']}, run `{run['id']}`.",
                  "This reference maximizes mean silhouette across k and then silhouette within that k; it is not an architectural quality verdict.", ""]
        for card in run["cards"]:
            lines += [f"### Cluster {card['cluster']}: {card['name']}", "", card["responsibility"], "",
                      "Members: " + ", ".join(card["ids"]), "",
                      "Name is a keyword suggestion. Inspect the source clauses and the reviewed architecture before adopting it.", ""]
    if bundle["paraphrases"]:
        lines += ["## Meaning-preserving wording probes", "",
                  "Each probe changes one clause and compares identical clause IDs at the same k and seed.", ""]
        for variant in bundle["paraphrases"]:
            values = [r["ari_to_same_seed"] for r in variant["runs"]]
            lines += [f"- {variant['clause']}: mean agreement {np.mean(values):.4f}; range {min(values):.4f}-{max(values):.4f} across {len(values)} runs."]
    review_path = DATA / "architecture.json"
    if review_path.exists():
        review = read_json(review_path)
        candidate = next((r for r in bundle["datasets"]["reviewed"]["runs"]
                          if r["id"] == review["basis"]["candidate_run"]), None)
        lines += ["", "## Architectural inspection candidate", "", review["rationale"], ""]
        if candidate:
            lines += [review["basis"]["selection"], "", f"Run `{candidate['id']}`.", ""]
            for card in candidate["cards"]:
                lines += [f"### C{card['cluster']}: {review['candidate_names'][str(card['cluster'])]}",
                          "", ", ".join(card["ids"]), ""]
        else:
            lines += ["The review refers to a previous experiment. Update it before presenting it as a review of these runs.", ""]
        render_architecture(review, candidate)
    lines += ["", "## Limits", "", "This is a small corpus without a ground-truth component partition. "
              "Silhouette measures separation, and ARI measures agreement. Neither proves correctness. "
              "PCA is a display aid. Dependency direction and primary ownership require explicit architectural judgment. "
              "Paraphrase sensitivity includes the effect of changed K-Means initialization geometry, even with the same seed.", ""]
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "EXPERIMENT_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def render_architecture(review, candidate):
    lines = ["# EarlyBird: reviewed architecture proposal", "", review["rationale"], "",
             "This is a human-reviewed application-core design. The source-linked clauses remain the authority; numerical clustering metrics do not establish these ownership decisions.", ""]
    if candidate:
        lines += [f"Reviewed database run: `{candidate['id']}`, k={candidate['k']}, seed={candidate['seed']}.",
                  "", review["basis"]["selection"], ""]
    else:
        lines += ["Review basis does not match the current experiment; preserve this as a historical proposal until reviewed again.", ""]
    lines += ["## Components and allowed use", "", "```mermaid", "flowchart LR"]
    for component in review["components"]:
        lines.append(f'  {component["id"]}["{component["name"]}"]')
    for dep in review["dependencies"]:
        lines.append(f'  {dep["from"]} -->|"{dep["label"]}"| {dep["to"]}')
    lines += ["```", "", "Arrows identify allowed use or dependency on a producer's data contract. Event/data flow can run in the opposite direction. The existing payment processor, printers, and SMS gateway are external adapters; this is not a deployment diagram.", ""]
    for component in review["components"]:
        lines += [f"### {component['name']}", "", f"Scope: {component['scope']}.", "",
                  component["responsibility"], "", "Owns: " + component["owns"], "",
                  "Offers: " + "; ".join(component["operations"]), "",
                  "Primary clauses: " + ", ".join(component["clauses"]), ""]
    lines += ["## Decision log", ""]
    for decision in review["decisions"]:
        lines += ["### " + decision["title"], "", decision["reason"], "",
                  "Evidence: " + ", ".join(decision["clauses"]), ""]
    if candidate:
        owners = {clause: c["name"] for c in review["components"] for clause in c["clauses"]}
        lines += ["## Complete ownership trail", "", "| Clause | Database cluster | Reviewed primary owner |",
                  "|---|---|---|"]
        lines += [f"| {item} | C{label} | {owners[item]} |" for item, label in zip(candidate["ids"], candidate["labels"])]
    lines += ["", "## Engineering decisions and unresolved policies", "",
              "Order state changes need atomic transition control. A committed assembly transition drives expected-payment transfer; retries need an explicit delivery/deduplication strategy. Immutable order snapshots, reliable events, and a reporting projection are design choices rather than additional numbered requirements. Browser compatibility, checksum computation, SMS cancellation authorization, payment due dates, route objectives, and the business-day cutoff remain unresolved where the PDF is incomplete.", ""]
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "ARCHITECTURE.md").write_text("\n".join(lines), encoding="utf-8")


def load_bundle():
    path = RESULTS / "latest.json"
    return read_json(path) if path.exists() else None
