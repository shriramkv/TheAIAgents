from openai import OpenAI
from typing import List, Dict, Any, Optional
import os
import sys

from config.settings import OPENAI_API_KEY, LLM_MODEL, EMBEDDING_MODEL

class LLMClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            print("WARNING: OPENAI_API_KEY is not set. API calls will fail.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_chat_completion(self, messages: List[Dict[str, str]], model: str = LLM_MODEL, temperature: float = 0.7) -> str:
        """
        Generates a chat completion using the OpenAI API.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"Error: {e}"

    def generate_embedding(self, text: str, model: str = EMBEDDING_MODEL) -> List[float]:
        """
        Generates a vector embedding for the given text.
        """
        try:
            if not text or not isinstance(text, str) or not text.strip():
                return []
                
            response = self.client.embeddings.create(
                input=[text],
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
