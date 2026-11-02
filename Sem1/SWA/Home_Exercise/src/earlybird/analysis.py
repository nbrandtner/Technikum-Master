"""Metrics describe geometry and agreement; they do not certify an architecture."""
from __future__ import annotations

from collections import Counter
from itertools import combinations

import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score, silhouette_samples


def score(vectors, labels):
    count = len(set(labels))
    values = silhouette_samples(vectors, labels, metric="euclidean") if 1 < count < len(labels) else np.zeros(len(labels))
    sizes = dict(Counter(labels))
    return {"silhouette": float(values.mean()), "point_silhouettes": values.tolist(),
            "sizes": {str(k): v for k, v in sizes.items()},
            "singletons": sum(n == 1 for n in sizes.values())}


def agreement(runs):
    if len(runs) < 2:
        return 1.0
    if any(r["ids"] != runs[0]["ids"] for r in runs):
        raise ValueError("Clustering agreement requires identical aligned identifiers")
    return float(np.mean([adjusted_rand_score(a["labels"], b["labels"]) for a, b in combinations(runs, 2)]))


def consensus(runs):
    if not runs:
        raise ValueError("At least one run is needed")
    if any(r["ids"] != runs[0]["ids"] for r in runs):
        raise ValueError("Consensus requires aligned identifiers")
    labels = np.array([r["labels"] for r in runs])
    return (labels[:, :, None] == labels[:, None, :]).mean(axis=0)


def summarize(runs):
    result = []
    for k in sorted({r["k"] for r in runs}):
        group = [r for r in runs if r["k"] == k]
        result.append({"k": k, "mean_silhouette": float(np.mean([r["silhouette"] for r in group])),
                       "min_silhouette": min(r["silhouette"] for r in group),
                       "max_silhouette": max(r["silhouette"] for r in group),
                       "seed_agreement": agreement(group), "runs": len(group),
                       "mean_singletons": float(np.mean([r["singletons"] for r in group]))})
    return result


def display_evidence(records, vectors):
    pca = PCA(n_components=2, svd_solver="full")
    coords = pca.fit_transform(vectors)
    # Anchor signs deterministically; no visual repositioning between seeds/k.
    for axis in range(2):
        anchor = np.argmax(np.abs(coords[:, axis]))
        if coords[anchor, axis] < 0:
            coords[:, axis] *= -1
    cosine = vectors @ vectors.T
    return {"coordinates": coords.tolist(), "pca_variance": pca.explained_variance_ratio_.tolist(),
            "neighbors": {r["id"]: [{"id": records[j]["id"], "cosine": float(cosine[i, j])}
                           for j in np.argsort(-cosine[i]) if j != i][:6] for i, r in enumerate(records)}}


def cluster_cards(records, vectors, labels):
    # Keyword suggestions come from actual text; no hand-written owner labels enter clustering.
    tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    words = tfidf.fit_transform([r["text"] for r in records])
    terms = tfidf.get_feature_names_out()
    cards = []
    for label in sorted(set(labels)):
        indexes = np.flatnonzero(np.array(labels) == label)
        term_scores = np.asarray(words[indexes].mean(axis=0)).ravel()
        keywords = []
        for j in np.argsort(-term_scores):
            term = terms[j]
            if term_scores[j] <= 0:
                break
            if not any(set(term.split()) & set(previous.split()) for previous in keywords):
                keywords.append(term)
            if len(keywords) == 3:
                break
        center = vectors[indexes].mean(axis=0)
        nearest = sorted(indexes, key=lambda i: np.linalg.norm(vectors[i] - center))
        representative = records[nearest[0]]
        cards.append({"cluster": int(label), "name": " / ".join(k.title() for k in keywords),
                      "naming": "TF-IDF keyword suggestion; inspect membership before accepting",
                      "ids": [records[i]["id"] for i in indexes],
                      "representatives": [records[i]["id"] for i in nearest[:3]],
                      "responsibility": representative["text"]})
    return cards
