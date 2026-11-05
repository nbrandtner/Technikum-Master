# EarlyBird Boundary Lab: experiment report

Generated from actual Neo4j GDS K-Means runs at 2026-11-03T17:24:55.047440+00:00.

Model: `sentence-transformers/all-mpnet-base-v2` at revision `e8c3b32edf5434bc2275fc9bab85f82640a19130`.
Database: Neo4j 2026.10.1; GDS 2026.10.1.

The source baseline and reviewed clauses have different granularity and scope; their scores are not a controlled before/after comparison.

## Source dataset

40 records.

| k | Mean Euclidean silhouette | Seed agreement (ARI) | Mean singletons |
|---|---:|---:|---:|
| 2 | 0.0748 | 0.0872 | 0.00 |
| 3 | 0.0635 | 0.1611 | 0.00 |
| 4 | 0.0464 | 0.1222 | 0.10 |
| 5 | 0.0572 | 0.2007 | 0.10 |
| 6 | 0.0626 | 0.2278 | 0.20 |
| 7 | 0.0582 | 0.2307 | 0.40 |
| 8 | 0.0575 | 0.2458 | 0.50 |
| 9 | 0.0527 | 0.2259 | 1.20 |
| 10 | 0.0531 | 0.2183 | 1.40 |

Geometric reference: k=2, seed=7, run `ef9198b43fbe7ac93a8cbe10`.
This reference maximizes mean silhouette across k and then silhouette within that k; it is not an architectural quality verdict.

### Cluster 0: Order / Customer / Clerk

Each customer can inquire into the status of her order over the phone using the order number. The phone clerk then tells the customer whether the delivery clerk is already on his way or not.

Members: R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44

Name is a keyword suggestion. Inspect the source clauses and the reviewed architecture before adopting it.

### Cluster 1: Breakfast / Croissant / Coffee

We offer a number of prepackaged breakfasts like the mini-breakfast (one croissant, one coffee), the luxury breakfast (one croissant, one glass of orange juice, two kinds of jam, ham and eggs, one cup of coffee) and many more.

Members: R02, R03

Name is a keyword suggestion. Inspect the source clauses and the reviewed architecture before adopting it.

## Reviewed dataset

43 records.

| k | Mean Euclidean silhouette | Seed agreement (ARI) | Mean singletons |
|---|---:|---:|---:|
| 2 | 0.0698 | 0.1355 | 0.00 |
| 3 | 0.0581 | 0.1733 | 0.00 |
| 4 | 0.0551 | 0.1743 | 0.00 |
| 5 | 0.0618 | 0.2407 | 0.30 |
| 6 | 0.0604 | 0.2489 | 0.40 |
| 7 | 0.0620 | 0.2686 | 0.50 |
| 8 | 0.0616 | 0.2708 | 0.60 |
| 9 | 0.0597 | 0.2598 | 0.60 |
| 10 | 0.0601 | 0.2722 | 0.80 |

Geometric reference: k=2, seed=2, run `472b8055ee0b6b256da1b160`.
This reference maximizes mean silhouette across k and then silhouette within that k; it is not an architectural quality verdict.

### Cluster 0: Order / Customer / Clerk

A customer can use one of her previous orders as a blueprint for a new order.

Members: R02.a, R03.a, R04.a, R05.a, R06.a, R09.a, R10.a, R11.a, R11.b, R11.c, R13.a, R14.a, R15.a, R16.a, R17.a, R17.b, R18.a, R19.a, R19.b, R21.a, R22.a, R23.a, R24.a, R25.a, R27.a, R28.a, R29.a, R30.a, R31.a, R31.b, R32.a, R35.a, R37.a, R38.a, R39.a, R40.a, R41.a, R42.a, R43.a, R44.a, R44.b

Name is a keyword suggestion. Inspect the source clauses and the reviewed architecture before adopting it.

### Cluster 1: Search / Limit / Requiring

Search for suitable products by requested characteristics, including a calorie limit and a price limit.

Members: R12.a, R36.a

Name is a keyword suggestion. Inspect the source clauses and the reviewed architecture before adopting it.

## Meaning-preserving wording probes

Each probe changes one clause and compares identical clause IDs at the same k and seed.

- R13.a: mean agreement 0.9746; range 0.7343-1.0000 across 30 runs.
- R29.a: mean agreement 0.9634; range 0.5391-1.0000 across 30 runs.
- R43.a: mean agreement 0.9645; range 0.6016-1.0000 across 30 runs.
- R44.a: mean agreement 0.9722; range 0.7343-1.0000 across 30 runs.

## Architectural inspection candidate

The highest average silhouette selects k=2; its best run places 41 clauses together and isolates two product-search clauses. A seven-cluster candidate exposes more useful responsibilities and several mixed groups. The reviewed proposal assigns six application-core components and one channel boundary using source obligations, state ownership, and the three scenario walkthroughs. Its boundaries are human decisions, not a claim that the embedding model discovered this exact architecture.

Inspect k=7 because it is the second-highest mean-silhouette candidate and separates recognizable cancellation, fulfillment, product, and reporting groups. Seed 0 has the highest silhouette within k=7. This is an explicit human selection for architectural inspection.

Run `a983874ded32c47593dd23c6`.

### C0: Order Eligibility and Cancellation

R10.a, R28.a, R29.a, R30.a, R31.a, R31.b, R41.a

### C1: Packing and Delivery Coordination

R05.a, R18.a, R19.a, R19.b, R21.a, R22.a, R24.a, R25.a, R27.a, R43.a

### C2: Breakfast Composition and Discovery

R02.a, R03.a, R04.a, R12.a

### C3: Daily Business Reporting

R44.a, R44.b

### C4: Identifiers and Channel Contracts

R09.a, R17.a, R17.b, R32.a, R37.a, R38.a, R40.a, R42.a

### C5: Blueprint Reuse and Mixed Constraints

R06.a, R13.a, R14.a, R15.a, R16.a, R23.a, R39.a

### C6: Customer Access and Interaction

R11.a, R11.b, R11.c, R35.a, R36.a


## Limits

This is a small corpus without a ground-truth component partition. Silhouette measures separation, and ARI measures agreement. Neither proves correctness. PCA is a display aid. Dependency direction and primary ownership require explicit architectural judgment. Paraphrase sensitivity includes the effect of changed K-Means initialization geometry, even with the same seed.
