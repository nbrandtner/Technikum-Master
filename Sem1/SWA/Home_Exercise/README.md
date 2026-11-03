# EarlyBird Boundary Lab

A local, free architecture investigation for the EarlyBird home exercise. Python generates sentence embeddings; Neo4j stores and indexes them and runs GDS K-Means; Streamlit presents the evidence and the reviewed architecture.

**Moving to a laptop?** Follow the [Windows laptop setup guide](docs/LAPTOP_SETUP.md). It explains what to copy, how to create a fresh Python environment, and how saved dashboard results differ from the Docker database stored on the home PC.

## Open the dashboard

On this machine, the project environment is already prepared. From PowerShell in this folder:

```powershell
.\run.ps1
```

Open http://127.0.0.1:8501. The dashboard replays genuine saved experiment outputs and does not need a running database or a model download. The optional **Query live neighbors** switch reads from Neo4j; the banner continues to identify the displayed clusters as saved experiment results.

Start with [the reviewed architecture](docs/ARCHITECTURE.md), [measured experiment results](docs/EXPERIMENT_REPORT.md), [the presentation guide](docs/DEMO.md), or [validation evidence](docs/VALIDATION.md).

## Reproduce the analysis

Prerequisites on another computer: Python 3.12 or 3.13, Docker Desktop with Linux containers, and internet for initial package/model/image downloads. No API key, paid service, GPU, or account is needed.

```powershell
.\run.ps1 setup
.\run.ps1 experiment
.\run.ps1 verify
.\run.ps1 test
.\run.ps1 dashboard
```

If a new database is still starting, wait until `docker compose ps` reports healthy and retry the experiment. Stop only the project's database with `.\run.ps1 stop`; this preserves its named data volume. Close the dashboard's terminal with Ctrl+C.

For a shorter exploratory run:

```powershell
.\run.ps1 experiment --k-min 2 --k-max 5 --seeds 3 --no-paraphrases
```

An experiment replaces `experiments/latest.json` and the generated report. Preserve those files first if you want to keep an earlier result. The model revision is pinned in `data/model-lock.json`; cached model and embedding files live in `.cache/`. Exact installed package versions are recorded in `requirements-lock.txt` (Windows / Python 3.12). A fresh environment can install that lock with `python -m pip install -r requirements-lock.txt` followed by `python -m pip install -e . --no-deps`.

## What to explore

- **Discover:** original versus reviewed inputs, k/seed controls, fixed PCA map, exact source wording, nearest clauses, and database-produced component membership.
- **Stability:** silhouette and seed agreement across k, co-assignment heatmaps, and one-clause paraphrase experiments.
- **Inspect:** human-reviewed responsibilities, knowledge ownership, allowed dependencies, and the decision log.
- **Challenge:** cancellation versus assembly, invoice reprinting versus payment registration, and shared web/SMS business rules. These are architecture walkthroughs, not a simulated production system.
- **Sources:** all 44 source statements, every reviewed clause, exclusions/supersessions, and unresolved questions.

## How the experiment works

1. `data/source_requirements.json` preserves all numbered statements with normalized whitespace, source pages, and a SHA-256 of the supplied PDF. `data/curation.json` documents each target-system transformation; `data/clauses.json` is the generated reviewed input.
2. Local Sentence Transformers creates unit-normalized embeddings. IDs, section headings, architectural owner labels, and proposed component names are excluded from model input.
3. Neo4j stores those vectors and creates a real cosine vector index. GDS projects the selected records and clusters their full-dimensional embedding properties using the query in `db/cluster.cypher`.
4. The default sweep uses k=2..10 and seeds=0..9 on both datasets. GDS executes every clustering run. Python computes Euclidean silhouettes and label-invariant agreement. Every run's membership is persisted and read back for verification.
5. Four reviewed paraphrases each change one clause. They are evaluated at the three k values with highest reviewed-dataset mean silhouette, using all ten seeds. Same-k, same-seed comparisons use exactly aligned clause IDs.
6. Genuine outputs, provenance, query text, component suggestions, and verification evidence are saved for presentation. `docs/EXPERIMENT_REPORT.md` is generated from those results.

The vector index enables similarity inspection; it does not itself execute K-Means. GDS is the database-side clustering engine. Exact cosine comparisons are appropriate for this small corpus and are used for nearest-clause inspection to avoid approximate-index filtering losses.

The source baseline retains eligible original functional statements, including superseded channel wording. The reviewed set resolves target-system scope and splits mixed obligations. Because their records differ, comparing their silhouette scores is exploratory, not a controlled proof that preprocessing improved the architecture.

## Scope and interpretation

The assignment is on PDF page 74 / printed slide 136 of the architecture lecture. Embeddings, database clustering, and meaningful cluster names meet its central requirements. The stability investigation and scenario review are explicit additions.

Neo4j is a graph database with vector capabilities. Component names initially use keywords from actual cluster contents; the reviewed architecture uses explicit human judgment. The display distinguishes these outputs. Similarity is symmetric and cannot determine caller/callee direction. A high silhouette, a stable cluster, or an attractive PCA map is not proof of architectural correctness.

All 44 statements remain accounted for. Browser compatibility, checksum algorithms, cancellation authorization by SMS, itinerary optimality, and payment-date policy remain open where the source is incomplete. The project sends no SMS and makes no payments.

## Project map

```text
app.py                  Streamlit entry point
src/earlybird/          data, embeddings, database, metrics, pipeline, dashboard, CLI
data/                   source inventory, reviewed clauses, assumptions, scenarios, architecture
db/                     executed clustering query and inspection queries
experiments/latest.json genuine saved experiment output
docs/                   report, architecture explanation, and presentation guide
scripts/                one-time PDF importer
tests/                  provenance, experiment integrity, and dashboard interaction checks
compose.yaml            local Neo4j with GDS
run.ps1                 convenience commands
```

To regenerate the inventory from the original PDF:

```powershell
.venv\Scripts\python.exe scripts\import_requirements.py "C:\Users\nbran\Downloads\EarlyBird-Requirements.pdf"
```

The PDF remains outside this repository. The inventory records its verified checksum. No external content is treated as permission to operate services.

## References

- [Neo4j vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/)
- [GDS K-Means](https://neo4j.com/docs/graph-data-science/current/algorithms/kmeans/)
- [GDS Docker installation](https://neo4j.com/docs/graph-data-science/current/installation/installation-docker/)
- [Sentence Transformers models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
- [Adjusted Rand Index](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)
