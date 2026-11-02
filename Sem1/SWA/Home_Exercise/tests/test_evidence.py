"""Checks protect provenance and scientific claims, not implementation details."""
import numpy as np
import pytest
from sklearn.metrics import adjusted_rand_score

from earlybird.analysis import agreement, consensus
from earlybird.data import DATA, dataset, load_clauses, load_sources, read_json, validate_inventory


def test_all_source_statements_and_quotes_are_accounted_for():
    coverage = validate_inventory()
    assert coverage["source_statements"] == 44
    assert coverage["reviewed_clauses"] > 30
    sources = {r["id"]: r for r in load_sources()["requirements"]}
    assert "Business Reporting" not in sources["R43"]["text"]
    assert sources["R44"]["text"].endswith("order number.")


def test_retired_phone_behavior_and_physical_tasks_remain_traceable():
    source_ids = {r["id"] for r in dataset("source")}
    reviewed_sources = {r["source"] for r in dataset("reviewed")}
    assert "R07" in source_ids and "R07" not in reviewed_sources
    assert "R20" not in source_ids
    assert {"R32", "R35", "R37", "R41", "R43", "R44"} <= reviewed_sources


def test_agreement_is_independent_of_cluster_numbers():
    runs = [{"ids": ["a", "b", "c"], "labels": [0, 0, 1]},
            {"ids": ["a", "b", "c"], "labels": [7, 7, 2]}]
    assert agreement(runs) == 1
    np.testing.assert_array_equal(consensus(runs), [[1,1,0], [1,1,0], [0,0,1]])


def test_misaligned_comparisons_are_rejected():
    runs = [{"ids": ["a", "b", "c"], "labels": [0, 0, 1]},
            {"ids": ["b", "a", "c"], "labels": [0, 0, 1]}]
    with pytest.raises(ValueError, match="align"):
        agreement(runs)
    with pytest.raises(ValueError, match="align"):
        consensus(runs)


def test_paraphrases_change_one_known_clause_each():
    ids = {r["id"] for r in load_clauses()}
    for variant in read_json(DATA / "paraphrases.json"):
        assert variant["clause"] in ids
        assert variant["review"]


def test_reviewed_architecture_has_one_primary_owner_per_clause():
    path = DATA / "architecture.json"
    if not path.exists():
        pytest.skip("Review is not yet written")
    architecture = read_json(path)
    owned = [c for component in architecture["components"] for c in component["clauses"]]
    assert len(owned) == len(set(owned)), "Duplicate primary ownership"
    assert set(owned) == {r["id"] for r in load_clauses()}
    components = {c["id"] for c in architecture["components"]}
    for dep in architecture["dependencies"]:
        assert {dep["from"], dep["to"]} <= components


def test_saved_results_have_complete_aligned_memberships_and_finite_metrics():
    from earlybird.pipeline import load_bundle
    bundle = load_bundle()
    if bundle is None:
        pytest.skip("Run the actual database experiment first")
    assert bundle["engine"] == "Neo4j GDS K-Means"
    assert bundle["verification"]["persisted_memberships_verified"]
    assert bundle["coverage"] == validate_inventory(), "Saved results no longer match the inventory"
    for data in bundle["datasets"].values():
        ids = [r["id"] for r in data["records"]]
        for run in data["runs"]:
            assert run["ids"] == ids
            assert len(run["labels"]) == len(ids)
            assert len(run["point_silhouettes"]) == len(ids)
            assert np.isfinite(run["silhouette"])
            assert sum(run["sizes"].values()) == len(ids)
            assert sorted(c for card in run["cards"] for c in card["ids"]) == sorted(ids)
    for variant in bundle["paraphrases"]:
        for run in variant["runs"]:
            base = next(r for r in bundle["datasets"]["reviewed"]["runs"] if r["id"] == run["baseline_run"])
            assert run["ids"] == base["ids"]
            assert run["ari_to_same_seed"] == pytest.approx(adjusted_rand_score(base["labels"], run["labels"]))
