from typing import List
from shared.vector_store import vector_db
from shared.logger import setup_logger
from shared.utils import load_config

logger = setup_logger(__name__)
config = load_config()

def index_documents(chunks: List[str]) -> None:
    """
    Embeds chunks and stores them in the vector database.

    Args:
        chunks (List[str]): List of textual chunks to index.
    """
    if not chunks:
        logger.warning("No chunks provided to index.")
        return

    embedding_model = config.get('embedding_model', 'text-embedding-3-small')
    logger.info(f"Indexing {len(chunks)} chunks with model: {embedding_model}")
    
    vector_db.add_documents(chunks, embedding_model=embedding_model)
    logger.info("Indexing complete.")
