# EarlyBird Boundary Lab

Original planning proposal, 2 November 2026. Implementation was subsequently authorized; see README.md for the implemented project and docs/ for its measured results and reviewed architecture.

The proposed deliverable is a local Python analysis tool with a polished interactive dashboard and a traceable architecture proposal. All required software and models should run without paid APIs. The distinctive question is: **Which component boundaries are supported by semantic similarity, remain stable under harmless wording changes, and respect the business rules?**

## 1. What the exercise requires

The home exercise is ArchitectureDevelopment02, on PDF page 74 / printed slide 136 of `C:/Users/nbran/Downloads/Architecture_Development_V702.pdf`. It asks for embeddings of EarlyBird's functional requirements, storage in a vector database, clustering by the database, and meaningful component names for the resulting clusters. Its stated output is an architecture proposal for the application core.

The following example slides, PDF pages 75-78, already demonstrate embedding arrays, a t-SNE cluster plot, requirement membership lists, and LLM-generated names. Those are useful baseline deliverables. Our additions are explicit scope decisions, experiments on boundary stability, and evaluation against concrete business scenarios. These additions are our proposal, rather than extra mandatory instructions from the exercise.

The 4-6 building-block instruction elsewhere in the deck belongs to the hospital exercise. It does not set the cluster count for this homework. The number of components should emerge from the experiment and architectural review.

The business source is `C:/Users/nbran/Downloads/EarlyBird-Requirements.pdf`, version 1.50, containing 44 numbered statements. A numbered statement is not necessarily one atomic functional requirement. Some statements combine several obligations, describe a manual action, specify a constraint, or describe a process superseded later in the document.

## 2. The central idea

Give the professor a short, reproducible investigation with three linked views:

1. **Discover:** See which requirements the embedding model and database group together.
2. **Inspect:** Open a component and follow its membership back to the exact source clauses, including ambiguous and unstable assignments.
3. **Challenge:** Walk through business scenarios that reveal whether those groups can become a coherent application core.

The presentation should make our architectural judgment visible. Database results remain available alongside the reviewed proposal, with a reason for every merge, split, reassignment, or excluded clause. We can report an inconclusive boundary honestly; finding instability is itself a useful result.

## 3. Establish the input before clustering

Preserve all 44 source statements verbatim in an inventory. Give every statement a disposition and rationale, including statements that will not become clustering input. Record the source page and requirement number.

Build a reviewed set of atomic clauses with stable identifiers such as R17.a and R17.b. Each clause carries its exact source span, any necessary contextual restatement, target-system status, and classification. Resolve references such as 'those three methods' using the source, and show that expansion in the audit view. Keep headings, source identifiers, proposed component names, and manually assigned responsibilities out of the embedded text.

Examples that deserve particular care:

| Source | Treatment to investigate |
| --- | --- |
| R7-8, R27-28 versus R32 and R34 | Phone-clerk interactions are retired. Preserve the enduring ordering, status, and cancellation behavior while recording the supersession of the phone channel. |
| R17 | Separate the single predefined customer address from assignment and communication of an order number. |
| R19, R21, R24 versus R32 | Preserve label, invoice, and itinerary capabilities while documenting replacement of the old tools. |
| R20 and parts of R25 | Physical bag handling and driving remain process context; identify the actual software responsibilities separately. |
| R26 versus R35 | Record replacement of the handwritten delivery confirmation with browser-based confirmation. |
| R1 | Treat the 25-minute delivery promise as a business quality constraint to evaluate, rather than inventing a component from it. |
| R33 | Retain as an incomplete browser/platform constraint; the actual browser list is absent. |
| R34 | Retain actor and access context; do not infer unsupported manager administration functions. |
| R37-41 | Separate SMS syntax and transport obligations from the shared order and cancellation behavior. |
| R42-43 | Preserve the existing external payment system, the record fields, and the assembly-completion trigger. |
| R44 | Preserve automatic nightly printing and the required report contents. |

Use two datasets for clearly different purposes:

- A source-level exploratory baseline, using the eligible functional source statements without architectural cleanup. This exposes what a simple reading of the document produces.
- The reviewed target-system clauses, used for the actual architecture proposal and controlled experiments.

Do not claim a directly comparable clustering score between these datasets: their records and granularity differ. Within the reviewed dataset, wording experiments use the same clause identifiers and change only the reviewed meaning-preserving wording.

Keep an assumptions register. Examples include the unspecified checksum algorithm, how an expected payment date is determined, and how the sender of an SMS cancellation is authenticated. Record uncertainties without silently adding business requirements. The order-number examples are compatible with eight base digits plus a checksum; do not label this a contradiction without resolving that interpretation.

## 4. Technology and the database's role

| Part | Proposed choice | Reason |
| --- | --- | --- |
| Analysis and orchestration | Python | Readable scripts and a small number of explicit steps. |
| Embeddings | Sentence Transformers, initially all-mpnet-base-v2 | Local sentence embeddings; no API key or usage charge. Cache the exact model revision. |
| Database | Neo4j Community Edition with vector indexes and the Community Graph Data Science plugin | Stores embeddings and provenance, supports vector search, and performs the clustering inside the database process. |
| Clustering | GDS K-Means on the original embedding dimensions | A documented database procedure with explicit parameters and repeatable seeds. |
| Evaluation | NumPy and scikit-learn metrics | Compare runs independently of arbitrary cluster numbers. |
| Dashboard | Streamlit with Plotly | Python throughout; interactive charts and source inspectors. |
| Architecture output | Markdown, CSV/JSON evidence, and Mermaid diagrams | Easy to review and regenerate. |

Neo4j is a graph database with vector capabilities. We should describe that accurately and demonstrate a real vector index and a real GDS clustering query. The vector index supports similarity inspection; GDS reads the stored embedding properties for clustering. Neither the index itself nor ordinary vector retrieval performs K-Means.

The official documentation supports vector indexes in Community Edition and GDS clustering on float-array node properties. GDS K-Means uses Euclidean distance. Normalize embedding inputs consistently, record the distance choices, and label Euclidean silhouette and cosine-neighbor evidence separately. Do not describe ordinary K-Means as spherical K-Means.

Docker is available on this machine, but the engine and required Python packages have not been validated or installed. The first implementation milestone will verify a compatible Neo4j/GDS pair and pin it. Neo4j Desktop with a local GDS installation is an alternative if Docker setup becomes inconvenient. Initial installation and model downloads need internet access; the prepared demo should run locally afterward.

Official references checked during planning:

- [Neo4j vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/)
- [GDS K-Means](https://neo4j.com/docs/graph-data-science/current/algorithms/kmeans/)
- [GDS on Docker](https://neo4j.com/docs/graph-data-science/current/installation/installation-docker/)
- [Community and Enterprise plugin availability](https://neo4j.com/docs/operations-manual/current/configuration/plugins/)
- [Sentence Transformers model documentation](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
- [Adjusted Rand Index](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)
- [Silhouette score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
- [Streamlit interactive Plotly charts](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)

## 5. Run a small, defensible experiment

Start with one embedding model and database K-Means. Predeclare a modest sweep, provisionally k=2 through 10 and ten recorded random seeds per k, adjusted only for dataset size or a documented technical reason. Store every run, rather than retaining only the most attractive chart.

For each run, collect cluster sizes, per-clause and average silhouette, representative requirements nearest the cluster center, and membership. Review degenerate results such as many singleton clusters. Choose a useful candidate using the metrics together with business coherence and the cost of fragmentation. The highest silhouette does not establish the best architecture.

For the strongest two or three candidates, inspect stability across seeds and a small set of manually reviewed paraphrases. Include difficult requirements such as R13, R29, R43, and R44. Preserve negations, quantifiers, actors, triggers, and numeric limits. Compare assignments only on aligned clause identifiers. Use Adjusted Rand Index for overall agreement and a pairwise co-assignment heatmap to show which requirements repeatedly stay together. Report how many runs support a relationship; this is observed stability, not a probability of architectural correctness.

Cluster the full embeddings. Use PCA for an initial two-dimensional display and explicitly label the projection as a display aid. A t-SNE or UMAP view is optional. Do not evaluate architecture quality from the spacing of points in a reduced plot.

Do not use manual component labels as algorithm input. Human review follows the unsupervised result. A local language model may optionally suggest names after clustering, but is unnecessary for the core submission. Names and one-sentence responsibilities can be reviewed directly from the actual cluster contents.

## 6. Turn clusters into an architecture proposal

For each candidate component, produce a small card containing its name, one-sentence responsibility, requirement membership, business knowledge it owns, offered operations, and allowed dependencies. Preserve each atomic clause's primary owner; cross-component participation appears as a collaboration rather than duplicate ownership.

Plausible areas to investigate include Product Catalog and Composition, Customer Eligibility, Order Lifecycle, Fulfillment, Billing Documents and Payment Exchange, and Daily Reporting. These are human hypotheses, not computed results or a required component count. Fulfillment may split into packing and delivery, and other areas may merge if the evidence supports it. Keep these labels out of embedding input.

Model browser and SMS entry points around the application core. The existing payment system is external. These placements are architectural decisions that need an explicit rationale; an occurrence of 'SMS' should not automatically create a separate business subsystem.

Derive dependency directions from required operations and data ownership. Semantic similarity is symmetric and cannot establish caller/callee direction. The lecture's discussion of directional domain knowledge on PDF pages 71-72 is useful supporting context.

Preserve a database-generated cluster proposal as the required primary result, then show a reviewed variant if changes are justified. Log the affected clauses, original grouping, reviewed grouping, rule or scenario evidence, and tradeoff for every change. A modular application core is a sufficient design target; choosing independently deployed services requires additional evidence.

## 7. Make the distinctive part concrete

The dashboard's Challenge view should contain three short walkthroughs tied to actual requirements:

| Scenario | Requirements | Architectural question |
| --- | --- | --- |
| Cancellation arrives as assembly finishes | R18, R29-31, R43 | Who owns the authoritative state transition, and how is an accepted cancellation prevented from racing with assembly completion? |
| An invoice is printed again | R21-23, R42-43 | Can a new numbered invoice copy be produced without confusing document printing with the trigger for an expected payment? |
| The same order is submitted through web and SMS | R32, R37-41 | Do the entry points invoke the same order rules while handling their own input and response formats? |

A fourth optional walkthrough examines whether the nightly report in R44 creates broad read dependencies and whether a reporting projection is justified.

For each scenario, highlight the source clauses, responsible components, required calls or events, and an explanation of any failure in the candidate design. These are architecture walkthroughs, not claims that a production order-processing engine has been implemented. Concurrency control and retry/idempotency choices should be labeled as engineering decisions derived from the business rules.

As a stretch feature, show a proposed change such as changing the SMS syntax. Mark the directly affected responsibilities and explain possible contract effects. Label this as a reasoned change-impact estimate, not a measured prediction of which source files would change.

## 8. Dashboard and presentation

Use a restrained breakfast-inspired palette: warm ivory background, dark ink text, amber accents, and distinct accessible component colors. Keep the same component colors across views. Use stable layout positions when switching experiments so that movement does not exaggerate changes.

The Discover view has run controls, a requirement map, a membership list, and a compact metrics panel. Selecting a requirement opens its exact source text, target-system restatement, nearest neighbors, component membership, and stability evidence. The Inspect view shows the component cards and a dependency diagram. Similarity links and allowed dependencies must have different labels and visual treatments.

The Challenge view uses the three scenarios above. Include a source inventory and assumptions view so every source statement remains accounted for. Use plain labels and a small number of controls; technical run details can live in an expandable panel.

Provide an explicitly labeled replay mode from saved genuine experiment outputs so the presentation survives an unavailable database. Keep the live database path available to demonstrate the exercise. Avoid dependence on a live model download during the presentation.

Suggested presentation sequence: state the exercise, show the source ambiguity, demonstrate one baseline, inspect one unstable boundary, challenge it with the cancellation or invoice scenario, and show the resulting reviewed component proposal with traceability. End with the limitations of semantic clustering on this small corpus.

## 9. Implementation milestones

| Milestone | Concrete result | Completion check |
| --- | --- | --- |
| 1. Source inventory | All 44 statements and reviewed atomic clauses | Every statement has a disposition; every transformation has provenance. |
| 2. Database baseline | Local embeddings, populated vector index, database K-Means, named cluster proposal | A saved run can be traced to its input, model revision, parameters, and executed database procedure. |
| 3. Boundary evidence | Parameter sweep, selected paraphrase runs, stability results | Comparisons use aligned identifiers; all recorded runs remain inspectable. |
| 4. Architecture review | Component cards, ownership, dependencies, decision log | Each selected functional clause has a primary owner; every architectural adjustment is explained. |
| 5. Dashboard | Discover, Inspect, Challenge, source and assumptions views | Requirement selection and all three scenarios work with saved genuine results. |
| 6. Submission | README, concise report, diagrams, reproducibility instructions, demo script | A fresh setup can reproduce the baseline, and the saved replay can present the same evidence. |

Build the required baseline before polishing the UI. The minimum distinctive scope is one model, one database algorithm, a documented sweep, the three scenario walkthroughs, and the dashboard. A second embedding model, graph community detection, arbitrary change simulation, and a full EarlyBird business application are outside this initial scope.

During implementation, use meaningful checks for source coverage, embedding-to-clause alignment, database cluster persistence, reproducibility, and the scenario evidence. UI review should verify readable labels, consistent colors, accurate source links, and a clearly distinguished live/replay state. Numerical scores and claimed findings enter the report only after real runs.

Proposed eventual repository shape: `data/` for reviewed requirements and assumptions, `src/` for the pipeline and dashboard, `db/` for Cypher procedures and queries, `experiments/` for run configurations and genuine results, and `docs/` for architecture decisions and the report. Keep the original PDFs outside the repository unless we decide they should be included.

The user accepted the Python/dashboard direction and authorized implementation using free tools. The implementation and genuine experiment outputs now live alongside this original proposal.
