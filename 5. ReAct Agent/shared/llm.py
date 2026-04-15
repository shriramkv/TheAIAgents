import os
from openai import OpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv

from shared.utils import load_config

# Load env variables
load_dotenv()

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = load_config()
        self.model = self.config.get("model", "gpt-4o-mini")
        self.temperature = self.config.get("temperature", 0.2)
        self.max_tokens = self.config.get("max_tokens", 600)

    def call_llm(self, messages: List[Dict[str, str]]) -> str:
        """
        Calls OpenAI model with current messages and config
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content or ""
