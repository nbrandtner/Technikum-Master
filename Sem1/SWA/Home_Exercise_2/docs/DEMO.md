# A short presentation of EarlyBird Boundary Lab

Open the dashboard with `.\run.ps1` from the project root. Saved genuine outputs support every view without downloading a model or starting a database. To demonstrate database persistence too, start Docker Desktop and run `docker compose up -d --wait`, then `.\run.ps1 verify`.

## 1. Establish the question

"The exercise asks whether embeddings can group functional requirements into components. My investigation asks which of those boundaries we can defend once we inspect scope, wording sensitivity, and the business rules."

Show **Sources**. Search for R07, then R32. Explain that the document describes both today's phone process and a future web/SMS system. Every statement is preserved, including retired interactions and incomplete constraints. A cluster of phone vocabulary is not automatically a future business component.

## 2. Show what the database actually computed

Open **Discover**, select the reviewed clauses, and inspect the geometric reference. Change k and seed. Explain that the number of components is a design tradeoff, not fixed by the unrelated hospital exercise in the lecture.

Select a clause, preferably R29.a or R43.a. Open its source and compare its neighbors. The map is a fixed two-dimensional PCA display; the clustering used the complete embeddings. Open Experiment details to show the actual GDS query, pinned model revision, and run identifier.

The original source baseline is available as an exploratory contrast. Its different scope and granularity mean its silhouette cannot serve as a controlled before/after quality claim.

## 3. Find the uncertain boundaries

Open **Stability**. Compare geometric separation with seed agreement. Explain the heatmap: a cell records the fraction of seeds in which two clauses share a cluster at this k. It is not a probability that an architectural decision is correct.

Expand a paraphrase probe. Only one clause's meaning-preserving wording was changed; comparisons use identical clause IDs at the same k and seed. Report the measured agreement shown by the experiment, even if it contradicts an expectation. Same-seed changes can still affect K-Means initialization geometry.

## 4. Expose architectural judgment

Open **Inspect**. Show the named components, primary ownership, offered operations, and allowed dependencies. Explain which decisions differ from the database's clusters and why. A sentence can collaborate across components while retaining one primary owner.

Similarity cannot determine dependency direction. Product Catalog can exist without knowing about an order, whereas ordering must resolve products; the allowed use is derived from the domain and operations.

## 5. Challenge it with the business rules

Open **Challenge** and use the slider to walk through each scenario:

- **Cancellation versus assembly:** The authoritative state transition decides which wins. Assembly completion is the exact cutoff and the payment trigger.
- **Another invoice copy:** A new numbered print must not be confused with the assembly-triggered payment interface.
- **Web and SMS:** Different input formats invoke shared order and cancellation behavior. The unresolved SMS cancellation identity policy stays visible.

These are architecture walkthroughs. The tool does not claim to implement a production breakfast service, concurrent transactions, a payment processor, or an SMS gateway.

## 6. State the practical result and limits

"Embeddings provided a reproducible starting partition. Stability experiments exposed sensitivity, and source-linked scenarios supplied reasons for accepting or changing boundaries. The result is a reviewed application-core proposal with a visible decision trail."

This is one small requirements corpus with no labeled ground-truth architecture. High silhouette and agreement support specific claims about geometry and stability. They do not establish a universally optimal component design.
