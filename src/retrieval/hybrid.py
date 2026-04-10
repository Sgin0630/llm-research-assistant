from src.retrieval.bm25_index import BM25Index
from src.retrieval.vector_store import VectorStore
from src.retrieval.embeddings import embed


def reciprocal_rank_fusion(
    dense_ids: list[str],
    bm25_ids: list[str],
    k: int = 60,
) -> list[str]:
    """Merge dense and sparse results using Reciprocal Rank Fusion."""
    scores: dict[str, float] = {}
    for rank, doc_id in enumerate(dense_ids):
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    for rank, doc_id in enumerate(bm25_ids):
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=lambda d: scores[d], reverse=True)


class HybridRetriever:
    """Retrieve physics paper chunks using BM25 + dense embeddings fused with RRF."""

    def __init__(self, chunks: list[dict], embed_model, vector_store: VectorStore):
        self.chunks = chunks
        self.chunk_map = {c["id"]: c for c in chunks}
        self.embed_model = embed_model
        self.vector_store = vector_store
        self.bm25 = BM25Index()
        self.bm25.build(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """Return top_k chunks fused from BM25 and dense retrieval."""
        # BM25
        bm25_ids = self.bm25.search(query, top_k=top_k * 2)

        # Dense
        query_embedding = embed(self.embed_model, [query])[0]
        dense_chunks = self.vector_store.query(query_embedding, n_results=top_k * 2)
        dense_ids = [c["id"] for c in dense_chunks]

        # Fuse
        fused_ids = reciprocal_rank_fusion(dense_ids, bm25_ids)
        return [self.chunk_map[cid] for cid in fused_ids[:top_k] if cid in self.chunk_map]
