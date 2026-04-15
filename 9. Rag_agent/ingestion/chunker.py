import tiktoken
from typing import List
from shared.logger import setup_logger
from shared.utils import load_config

logger = setup_logger(__name__)
config = load_config()

def chunk_text(text: str, chunk_size: int = None, overlap: int = 50) -> List[str]:
    """
    Splits text into smaller token-aware chunks.

    Args:
        text (str): The document text to chunk.
        chunk_size (int): Max number of tokens per chunk. Defaults to config value or 400.
        overlap (int): Number of overlapping tokens between chunks. Defaults to 50.

    Returns:
        List[str]: A list of chunks.
    """
    if not text.strip():
        return []

    c_size = chunk_size or config.get('chunk_size', 400)
    
    # We use tiktoken to split by actual token count.
    # We use 'cl100k_base' which is used by gpt-4o-mini and text-embedding-3-small
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    
    chunks = []
    start = 0
    while start < len(tokens):
        # Determine end of chunk
        end = start + c_size
        chunk_tokens = tokens[start:end]
        
        # Decode back to text
        chunk_str = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_str)
        
        # Move the pointer, accounting for overlap
        start += (c_size - overlap)

    logger.info(f"Split document into {len(chunks)} chunks using size {c_size} and overlap {overlap}.")
    return chunks
