from typing import List
from openai import OpenAI
from shared.utils import load_config, get_env_var

class EmbeddingHandler:
    """
    Handles interactions with OpenAI Embeddings API.
    """
    def __init__(self):
        config = load_config()
        self.model = config.get("embedding_model", "text-embedding-3-small")
        self.client = OpenAI(api_key=get_env_var("OPENAI_API_KEY"))

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return []

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """
        return self.get_embeddings([text])[0]

# Singleton helper
_embedding_handler = None

def get_embedding(text: str) -> List[float]:
    global _embedding_handler
    if _embedding_handler is None:
        _embedding_handler = EmbeddingHandler()
    return _embedding_handler.get_embedding(text)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    global _embedding_handler
    if _embedding_handler is None:
        _embedding_handler = EmbeddingHandler()
    return _embedding_handler.get_embeddings(texts)
