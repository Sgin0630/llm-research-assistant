from sentence_transformers import SentenceTransformer
import numpy as np


def load_model(name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """Load a sentence-transformer embedding model."""
    return SentenceTransformer(name)


def embed(model: SentenceTransformer, texts: list[str]) -> np.ndarray:
    """Generate embeddings for a list of texts."""
    return model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
