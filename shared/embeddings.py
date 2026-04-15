import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate an embedding using the OpenAI embeddings API.

    Args:
        text (str): The text content to embed.
        model (str): The model identifier to use for embeddings.

    Returns:
        List[float]: The generated embedding vector.
    """
    # Replace newlines which may negatively affect performance
    text = text.replace("\n", " ")
    
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding
