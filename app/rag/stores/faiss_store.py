"""FAISS vector store adapter — optional (`pip install -e ".[faiss]"`), local-only, no server.

Verified against faiss-cpu==1.10.0 in this repo's dev environment (if pip attempts to build a
newer faiss-cpu from source and fails, install with `pip install --only-binary=:all: faiss-cpu`).

FAISS's flat indexes have no native delete, so this adapter keeps chunk content/metadata *and*
their embeddings in a companion JSON file and rebuilds the index on `delete_by_document_id`. This
is simple and correct at this repo's demo scale; it is not an optimization for large corpora.
"""

import json
from pathlib import Path

from app.models.rag import Chunk, RetrievedChunk
from app.rag.stores.base import VectorStore


class FAISSVectorStore(VectorStore):
    name = "faiss"

    def __init__(self, persist_dir: str, collection_name: str, dimension: int) -> None:
        try:
            import faiss
        except ImportError as exc:
            raise ImportError(
                'FAISS requires the "faiss" extra: pip install -e ".[faiss]"'
            ) from exc

        self._faiss = faiss
        self._dimension = dimension
        directory = Path(persist_dir)
        directory.mkdir(parents=True, exist_ok=True)
        self._index_path = directory / f"{collection_name}.faiss"
        self._meta_path = directory / f"{collection_name}.meta.json"

        self._chunks_by_id: dict[int, Chunk] = {}
        self._vectors_by_id: dict[int, list[float]] = {}
        self._next_id = 0

        if self._index_path.exists() and self._meta_path.exists():
            self._index = faiss.read_index(str(self._index_path))
            payload = json.loads(self._meta_path.read_text(encoding="utf-8"))
            self._next_id = payload["next_id"]
            self._chunks_by_id = {
                int(k): Chunk.model_validate(v) for k, v in payload["chunks"].items()
            }
            self._vectors_by_id = {int(k): v for k, v in payload["vectors"].items()}
        else:
            self._index = faiss.IndexIDMap(faiss.IndexFlatIP(dimension))

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        import numpy as np

        ids: list[int] = []
        for chunk, vector in zip(chunks, embeddings, strict=True):
            int_id = self._next_id
            self._next_id += 1
            self._chunks_by_id[int_id] = chunk
            self._vectors_by_id[int_id] = vector
            ids.append(int_id)

        vectors = np.array(embeddings, dtype="float32")
        self._index.add_with_ids(vectors, np.array(ids, dtype="int64"))
        self._persist()

    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        total = self.count()
        if total == 0:
            return []
        import numpy as np

        query_vector = np.array([embedding], dtype="float32")
        scores, ids = self._index.search(query_vector, min(top_k, total))
        results: list[RetrievedChunk] = []
        for score, int_id in zip(scores[0], ids[0], strict=True):
            if int_id == -1:
                continue
            chunk = self._chunks_by_id.get(int(int_id))
            if chunk is not None:
                results.append(
                    RetrievedChunk(chunk=chunk, score=float(score), retrieval_method="vector")
                )
        return results

    def delete_by_document_id(self, document_id: str) -> None:
        keep_ids = [i for i, c in self._chunks_by_id.items() if c.document_id != document_id]
        self._rebuild(keep_ids)

    def count(self) -> int:
        return self._index.ntotal

    def _rebuild(self, keep_ids: list[int]) -> None:
        import numpy as np

        self._index = self._faiss.IndexIDMap(self._faiss.IndexFlatIP(self._dimension))
        self._chunks_by_id = {i: self._chunks_by_id[i] for i in keep_ids}
        self._vectors_by_id = {i: self._vectors_by_id[i] for i in keep_ids}
        if keep_ids:
            vectors = np.array([self._vectors_by_id[i] for i in keep_ids], dtype="float32")
            self._index.add_with_ids(vectors, np.array(keep_ids, dtype="int64"))
        self._persist()

    def _persist(self) -> None:
        self._faiss.write_index(self._index, str(self._index_path))
        payload = {
            "next_id": self._next_id,
            "chunks": {str(k): v.model_dump(mode="json") for k, v in self._chunks_by_id.items()},
            "vectors": {str(k): v for k, v in self._vectors_by_id.items()},
        }
        self._meta_path.write_text(json.dumps(payload), encoding="utf-8")
