import faiss
import numpy as np
from typing import List, Tuple
from shared.embeddings import get_embedding
from shared.logger import setup_logger

logger = setup_logger(__name__)

class VectorStore:
    """
    In-memory vector store using FAISS.
    Maintains the index and maps back integer IDs to text chunks.
    """
    def __init__(self, embedding_dim: int = 1536):
        # L2 distance index
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents: List[str] = []

    def add_documents(self, texts: List[str], embedding_model: str = "text-embedding-3-small") -> None:
        """
        Embeds texts and adds them to the FAISS index.

        Args:
            texts (List[str]): List of string chunks to embed and store.
            embedding_model (str): The OpenAI embedding model to use.
        """
        if not texts:
            return

        logger.info(f"Adding {len(texts)} documents to vector store.")
        embeddings = []
        for text in texts:
            emb = get_embedding(text, model=embedding_model)
            embeddings.append(emb)

        # Convert to float32 numpy array for FAISS
        embeddings_np = np.array(embeddings).astype("float32")
        self.index.add(embeddings_np)
        
        # Keep track of textual documents corresponding to the vectors
        self.documents.extend(texts)
        logger.info(f"Vector store now contains {len(self.documents)} items.")

    def similarity_search(self, query: str, k: int = 3, embedding_model: str = "text-embedding-3-small") -> List[str]:
        """
        Retrieves the top-k most similar text chunks for a query.

        Args:
            query (str): The search query.
            k (int): Number of top documents to return.
            embedding_model (str): The OpenAI embedding model to use.

        Returns:
            List[str]: The top-k most relevant text chunks.
        """
        if self.index.ntotal == 0:
            logger.warning("Vector store is empty. Returning no chunks.")
            return []

        # Ensure k isn't larger than total docs
        k = min(k, self.index.ntotal)

        # 1. Embed query
        query_emb = get_embedding(query, model=embedding_model)
        query_np = np.array([query_emb]).astype("float32")

        # 2. Search index
        distances, indices = self.index.search(query_np, k)

        # 3. Retrieve texts based on matching IDs
        results = [self.documents[idx] for idx in indices[0]]
        return results

# Singleton instance across the application
vector_db = VectorStore()
