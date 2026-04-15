from typing import List
from shared.vector_store import vector_db
from shared.logger import setup_logger
from shared.utils import load_config

logger = setup_logger(__name__)
config = load_config()

def retrieve_context(query: str, k: int = None) -> List[str]:
    """
    Retrieve top-k relevant chunks from the vector store based on the semantic similarity to the query.

    Args:
        query (str): The search query of the user.
        k (int, optional): The number of top chunks to return. Defaults to value from config or 3.

    Returns:
        List[str]: A list of text chunks representing the retrieved context.
    """
    top_k = k or config.get('top_k', 3)
    embedding_model = config.get('embedding_model', 'text-embedding-3-small')
    
    logger.info(f"Retrieving top {top_k} chunks for query: '{query}'")
    context_chunks = vector_db.similarity_search(query, k=top_k, embedding_model=embedding_model)
    
    logger.info(f"Retrieved {len(context_chunks)} reasoning context chunks.")
    return context_chunks
