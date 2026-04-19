import os
import time
from typing import Optional, List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from shared.utils import load_config

load_dotenv()

class LLMHandler:
    """
    Handles interactions with the OpenAI API with retry logic.
    """
    def __init__(self):
        self.config = load_config()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = self.config.get("model", "gpt-4o-mini")
        self.temperature = self.config.get("temperature", 0.3)
        self.max_retries = self.config.get("max_retries", 3)

    def call_llm(self, prompt: str, system_prompt: str = "You are a helpful research assistant.") -> str:
        """
        Calls the LLM with the given prompt and system prompt.
        Includes basic retry logic for robustness.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                retries += 1
                if retries >= self.max_retries:
                    return f"Error calling LLM after {self.max_retries} attempts: {str(e)}"
                time.sleep(2 ** retries)  # Exponential backoff
        return "Unknown error occurred during LLM call."
