// Run in Neo4j Browser at http://localhost:7474
SHOW VECTOR INDEXES;

// Every membership below came from an executed database clustering procedure.
MATCH (run:EBRun)-[a:ASSIGNS]->(r:EBRequirement)
RETURN run.id, run.dataset, run.k, run.seed, r.item_id, a.cluster
ORDER BY run.dataset, run.k, run.seed, r.item_id;

// Replace the example id with one from experiments/latest.json.
// MATCH (run:EBRun {id: '...'})-[a:ASSIGNS]->(r:EBRequirement)
// RETURN run, a, r;
