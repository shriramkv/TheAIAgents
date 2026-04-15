"""
LLM Interface using OpenAI SDK.
"""
import os
from openai import OpenAI
import yaml

class LLMInterface:
    """
    Handles interactions with the Large Language Model.
    """
    def __init__(self, config_path: str = "config.yaml"):
        # Load constraints/config
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception:
            self.config = {}
        
        self.client = OpenAI() # Assumes OPENAI_API_KEY is properly loaded from the environment
        self.model = self.config.get("model", "gpt-4o-mini")
        self.temperature = self.config.get("temperature", 0.3)
        self.max_tokens = self.config.get("max_tokens", 300)

    def generate(self, prompt: str) -> str:
        """Generates text from the LLM based on the given prompt."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content.strip()
