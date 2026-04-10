from rank_bm25 import BM25Okapi


class BM25Index:
    """BM25 keyword index over a list of text chunks."""

    def __init__(self):
        self.chunks = []
        self.bm25 = None

    def build(self, chunks: list[dict]) -> None:
        """Build BM25 index from chunks (each must have 'id' and 'text')."""
        self.chunks = chunks
        corpus = [c["text"].split() for c in chunks]
        self.bm25 = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 10) -> list[str]:
        """Return top_k chunk IDs ranked by BM25 score."""
        if self.bm25 is None:
            raise RuntimeError("Index not built. Call build() first.")
        scores = self.bm25.get_scores(query.split())
        import numpy as np
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.chunks[i]["id"] for i in top_indices]
