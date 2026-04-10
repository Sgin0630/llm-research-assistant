import chromadb
import numpy as np


class VectorStore:
    """Chroma-backed vector store for dense retrieval."""

    def __init__(self, persist_directory: str = "data/chroma", collection_name: str = "hep-arxiv"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, chunks: list[dict], embeddings: np.ndarray) -> None:
        """Store chunks with their embeddings. Each chunk must have 'id' and 'text'.
        Optional metadata keys: arxiv_id, chunk_id."""
        ids = [c["id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [
            {k: v for k, v in c.items() if k not in ("id", "text")}
            for c in chunks
        ]
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

    def query(self, embedding: np.ndarray, n_results: int = 10) -> list[dict]:
        """Return top n_results chunks by cosine similarity to embedding."""
        results = self.collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )
        chunks = []
        for i, doc_id in enumerate(results["ids"][0]):
            chunks.append({
                "id": doc_id,
                "text": results["documents"][0][i],
                **results["metadatas"][0][i],
            })
        return chunks
