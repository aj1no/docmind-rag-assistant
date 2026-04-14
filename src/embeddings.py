from sentence_transformers import SentenceTransformer
from typing import List
from .config import settings

# Global cache to avoid reloading model across requests
_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print("Loading embedding model, this may take a moment on first run...")
        _model = SentenceTransformer(settings.embedding_model)
    return _model

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Converts a list of texts into vector embeddings.
    """
    model = get_model()
    embeddings_array = model.encode(texts)
    # FAISS requires lists/numpy arrays; we convert back to python list for type safety boundaries
    return embeddings_array.tolist()

def get_embedding(text: str) -> List[float]:
    """
    Convenience method for a single text embed (useful during queries).
    """
    return get_embeddings([text])[0]
