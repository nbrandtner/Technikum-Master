# Validation of the implemented project

Validated on 2 November 2026, using Python 3.12 on Windows.

| Check | Observed result |
| --- | --- |
| Source coverage and quote provenance | All 44 numbered statements accounted for; 43 reviewed clauses; 40 source-baseline records. |
| Database | Neo4j Community 2026.10.1, GDS 2026.10.1, healthy local container. |
| Vector store | 768-dimensional cosine index `eb_vectors_768`, ONLINE, 100% populated. A real index query returned stored requirement matches. |
| Base clustering sweep | 180 executed GDS runs: two datasets, k=2..10, ten seeds each. |
| Wording probes | 120 executed GDS runs: four single-clause paraphrases, three selected k values, ten seeds each. |
| Persistence audit | All 300 saved memberships read back from Neo4j matched the saved experiment. |
| Selected-run reproduction | Re-executed reviewed k=7, seed=0: identical memberships, ARI=1.0. Projection uses explicit clause-ID ordering. |
| Automated tests | Eight tests passed, including every dashboard view, k changes, and all three scenario walkthroughs. |
| Browser review | Checked the actual local Streamlit page, discovery controls, source inspector, component cards, and dependency diagram. |

The discovery preview is saved in `docs/screenshots/discover.png`. Test commands and reproduction steps are in the README. The code, configuration, model revision, generated report, and saved genuine results are included in the project.

The source PDF SHA-256 is `a48fb03c232777c7db22d76b0f5f0f63cecf4868acdb29014987978e8c1b54eb`. The selected architecture inspection run is `a983874ded32c47593dd23c6`.

These checks validate the analysis tool and its evidence trail. The business scenarios are architecture walkthroughs; a production ordering service, payment processor, SMS gateway, and route optimizer have not been implemented.

## Presentation preparation, 3 November 2026

All six read-only statements in `db/presentation.cypher` were executed against the local database. The vector index was ONLINE with 768 dimensions and COSINE similarity, the sample requirement had 768 stored values, and the seven candidate groups had the expected sizes: 7, 10, 4, 2, 8, 7, 5.

The live-neighbor display was corrected to convert Neo4j's rescaled similarity to the raw cosine convention used by the saved NumPy results. The verification example was refreshed from the live database; clustering memberships and metrics were not changed. Nine tests passed with `EARLYBIRD_TEST_DATABASE=1`, including comparisons of live and saved neighbor IDs and scores for two requirements.
