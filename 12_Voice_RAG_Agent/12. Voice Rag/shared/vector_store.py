import os
import faiss
import numpy as np
import pickle
from typing import List, Dict, Any
from shared.utils import load_config

class VectorStore:
    """
    FAISS-based vector store management.
    """
    def __init__(self):
        config = load_config()
        self.index_path = config.get("index_path", "vectorstore.index")
        self.dimension = 1536 # Default for text-embedding-3-small
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

    def add_texts(self, texts: List[str], embeddings: List[List[float]]):
        """
        Add texts and their embeddings to the index.
        """
        embeddings_np = np.array(embeddings).astype('float32')
        self.index.add(embeddings_np)
        self.metadata.extend(texts)

    def search(self, query_embedding: List[float], k: int = 3) -> List[str]:
        """
        Search for the top k most relevant texts.
        """
        query_np = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_np, k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def save(self):
        """
        Save the index and metadata to disk.
        """
        faiss.write_index(self.index, self.index_path)
        with open(f"{self.index_path}.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """
        Load the index and metadata from disk.
        """
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(f"{self.index_path}.pkl", "rb") as f:
                self.metadata = pickle.dump(self.metadata, f)
        else:
            print(f"Index file {self.index_path} not found. Starting with empty store.")

# Singleton instance
vector_store = VectorStore()
