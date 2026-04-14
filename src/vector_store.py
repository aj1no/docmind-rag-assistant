import faiss
import numpy as np
import os
import json
from typing import List, Dict, Any

from .config import settings

INDEX_FILE = os.path.join(settings.base_dir, "faiss_index.bin")
METADATA_FILE = os.path.join(settings.base_dir, "metadata.json")

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        # all-MiniLM-L6-v2 produces exactly 384 dimensional embeddings.
        self.dimension = 384 

    def init_index(self):
        """Initializes a new empty L2 distance FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

    def load_if_exists(self) -> bool:
        """Loads index and metadata from disk if available."""
        if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            return True
        return False

    def add_embeddings(self, embeddings: List[List[float]], metadata: List[Dict[str, Any]]):
        """Adds vectorized chunks to the active FAISS index."""
        if self.index is None:
            self.init_index()
            
        vectors = np.array(embeddings).astype('float32')
        self.index.add(vectors)
        self.metadata.extend(metadata)
        
    def save(self):
        """Persists the FAISS index and local metadata flatfile."""
        if self.index is not None:
            faiss.write_index(self.index, INDEX_FILE)
            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f)
                
    def search(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        """
        Executes a semantic similarity K-Nearest Neighbors search.
        Returns a list of matching context dictionaries.
        """
        if self.index is None or self.index.ntotal == 0:
            return []
            
        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1 and idx < len(self.metadata):
                dist = float(distances[0][i])
                meta = self.metadata[idx]
                results.append({
                    "score": dist,
                    "document": meta.get("document", "Unknown"),
                    "text": meta.get("text", "")
                })
        return results

# Expose a singleton pattern
vector_store = VectorStore()
