from shared.embeddings import get_embedding
from shared.vector_store import vector_store
from shared.utils import load_config
from typing import List

def retrieve_context(query: str, k: int = 3) -> List[str]:
    """
    Retrieve relevant chunks for a given query.
    """
    if not query:
        return []

    config = load_config()
    top_k = config.get("top_k", k)
    
    # 1. Generate query embedding
    query_embedding = get_embedding(query)
    
    # 2. Search in vector store
    results = vector_store.search(query_embedding, k=top_k)
    
    return results
