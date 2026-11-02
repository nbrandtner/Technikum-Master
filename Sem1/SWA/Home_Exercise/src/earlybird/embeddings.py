"""Local model inference with content-addressed caching and revision provenance."""
from __future__ import annotations

import os
from importlib.metadata import version

import numpy as np

from .data import DATA, ROOT, digest, read_json, write_json

DEFAULT_MODEL = "sentence-transformers/all-mpnet-base-v2"


class Encoder:
    def __init__(self, model_name=DEFAULT_MODEL):
        # Keep downloaded model files inside the project, not a global user cache.
        os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
        os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
        from huggingface_hub import HfApi
        from sentence_transformers import SentenceTransformer
        import torch

        torch.set_num_threads(4)
        model_lock = DATA / "model-lock.json"
        if model_lock.exists() and read_json(model_lock)["model"] == model_name:
            self.info = read_json(model_lock)
        else:
            revision = HfApi().model_info(model_name).sha
            self.info = {"model": model_name, "revision": revision,
                         "sentence_transformers": version("sentence-transformers"),
                         "torch": version("torch"), "device": "cpu", "normalized": True}
            write_json(model_lock, self.info)
        self.model = SentenceTransformer(model_name, revision=self.info["revision"], device="cpu",
                                         cache_folder=str(ROOT / ".cache" / "models"))

    def encode(self, records):
        fingerprint = digest({"records": [{"id": r["id"], "text": r["text"]} for r in records],
                              "model": self.info})
        path = ROOT / ".cache" / "embeddings" / f"{fingerprint}.npy"
        if path.exists():
            vectors = np.load(path, allow_pickle=False)
        else:
            vectors = self.model.encode([r["text"] for r in records], normalize_embeddings=True,
                                        show_progress_bar=True, batch_size=16)
            path.parent.mkdir(parents=True, exist_ok=True)
            np.save(path, vectors, allow_pickle=False)
        vectors = np.asarray(vectors, dtype=np.float32)
        if vectors.shape[0] != len(records) or not np.isfinite(vectors).all():
            raise ValueError("Embeddings are missing, misaligned, or non-finite")
        if not np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-5):
            raise ValueError("Expected unit-normalized embeddings")
        return vectors, fingerprint
