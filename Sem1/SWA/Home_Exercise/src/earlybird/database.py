"""Neo4j owns the vector store and executes every recorded clustering run.

The GDS projection deliberately has no semantic edges: K-Means clusters the
embedding properties directly. Architecture dependencies are reviewed separately.
"""
from __future__ import annotations

import os
from uuid import uuid4

from neo4j import GraphDatabase

from .data import ROOT


class Database:
    def __init__(self):
        password = os.getenv("NEO4J_PASSWORD")
        auth = (os.getenv("NEO4J_USER", "neo4j"), password) if password else None
        self.driver = GraphDatabase.driver(os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687"),
                                           auth=auth, connection_timeout=5,
                                           connection_acquisition_timeout=10,
                                           max_transaction_retry_time=5)
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def query(self, text, **params):
        records, _, _ = self.driver.execute_query(text, parameters_=params, database_="neo4j")
        return [dict(r) for r in records]

    def status(self):
        version = self.query("CALL dbms.components() YIELD versions RETURN versions[0] AS neo4j")[0]
        version.update(self.query("RETURN gds.version() AS gds")[0])
        return version

    def ingest(self, records, vectors, fingerprint):
        self.query("CREATE CONSTRAINT eb_requirement_key IF NOT EXISTS FOR (r:EBRequirement) REQUIRE r.key IS UNIQUE")
        self.query("CREATE CONSTRAINT eb_run_key IF NOT EXISTS FOR (r:EBRun) REQUIRE r.id IS UNIQUE")
        self.query("""UNWIND $rows AS row
          MERGE (r:EBRequirement {key: row.key})
          SET r.item_id=row.id, r.text=row.text, r.source=row.source,
              r.embedding=row.embedding, r.embedding_set=$fingerprint""",
          rows=[{"key": f"{fingerprint}:{r['id']}", "id": r["id"], "text": r["text"],
                 "source": r["source"], "embedding": v.tolist()} for r, v in zip(records, vectors)],
          fingerprint=fingerprint)
        # One model per index; fail clearly on a dimension change instead of corrupting data.
        index = f"eb_vectors_{vectors.shape[1]}"
        self.query(f"""CREATE VECTOR INDEX {index} IF NOT EXISTS
          FOR (r:EBRequirement) ON (r.embedding)
          OPTIONS {{indexConfig: {{`vector.dimensions`: {vectors.shape[1]},
                   `vector.similarity_function`: 'cosine'}}}}""")
        self.query("CALL db.awaitIndexes(120)")
        return index

    def project(self, fingerprint):
        name = "eb_" + uuid4().hex
        self.query("""MATCH (n:EBRequirement) WHERE n.embedding_set=$fingerprint
          WITH n ORDER BY n.item_id
          WITH gds.graph.project($name, n, null,
            {sourceNodeProperties: n { .embedding }, targetNodeProperties: null}) AS graph
          RETURN graph.graphName AS name, graph.nodeCount AS nodes""",
          fingerprint=fingerprint, name=name)
        return name

    def cluster(self, graph, ids, k, seed):
        query = (ROOT / "db" / "cluster.cypher").read_text(encoding="utf-8")
        rows = self.query(query, graph=graph, k=k, seed=seed)
        by_id = {row["id"]: int(row["cluster"]) for row in rows}
        if set(by_id) != set(ids):
            raise ValueError("Database returned an incomplete or unexpected set of requirements")
        return [by_id[item_id] for item_id in ids]

    def save_run(self, run, fingerprint):
        self.query("""MERGE (run:EBRun {id:$id})
          SET run.k=$k, run.seed=$seed, run.dataset=$dataset, run.variant=$variant,
              run.silhouette=$silhouette, run.embedding_set=$fingerprint,
              run.procedure='gds.kmeans.stream'
          WITH run UNWIND $assignments AS assignment
          MATCH (r:EBRequirement {key:assignment.key})
          MERGE (run)-[a:ASSIGNS]->(r) SET a.cluster=assignment.cluster""",
          id=run["id"], k=run["k"], seed=run["seed"], dataset=run["dataset"],
          variant=run["variant"], silhouette=run["silhouette"], fingerprint=fingerprint,
          assignments=[{"key": f"{fingerprint}:{i}", "cluster": label}
                       for i, label in zip(run["ids"], run["labels"])])

    def drop(self, graph):
        self.query("CALL gds.graph.drop($name, false) YIELD graphName RETURN graphName", name=graph)

    def verify_run(self, run):
        rows = self.query("""MATCH (:EBRun {id:$id})-[a:ASSIGNS]->(r:EBRequirement)
          RETURN r.item_id AS id, a.cluster AS cluster ORDER BY id""", id=run["id"])
        return {r["id"]: r["cluster"] for r in rows} == dict(zip(run["ids"], run["labels"]))

    def nearest(self, fingerprint, item_id, limit=6):
        # Exact similarity on this tiny corpus also avoids ANN filtering losses.
        # The populated vector index is independently exposed for inspection.
        # Neo4j returns (1 + cosine) / 2. Convert to raw cosine [-1, 1]
        # so live and saved NumPy neighbors use the same displayed scale.
        return self.query("""MATCH (q:EBRequirement {embedding_set:$fingerprint, item_id:$id})
          MATCH (r:EBRequirement {embedding_set:$fingerprint}) WHERE r <> q
          RETURN r.item_id AS id, 2.0 * vector.similarity.cosine(q.embedding,r.embedding) - 1.0 AS cosine
          ORDER BY cosine DESC LIMIT $limit""", fingerprint=fingerprint, id=item_id, limit=limit)
