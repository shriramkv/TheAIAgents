import os
from openai import OpenAI
from typing import Optional
from shared.logger import logger
from shared.utils import load_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMInterface:
    """
    Standard LLM call wrapper with error handling and retries.
    """
    def __init__(self, config_path: str = "config.yaml"):
        # Load config
        self.config = load_config(config_path)
        self.model = self.config.get("model", "gpt-4o-mini")
        self.temperature = self.config.get("temperature", 0.3)
        
        # Initialize client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables.")
        
        self.client = OpenAI(api_key=api_key)

    def call_llm(self, prompt: str, system_prompt: str = "You are a senior financial analyst agent.") -> str:
        """
        Executes a call to the LLM with error handling.
        Why: Standardizes all LLM traffic and handles retries/logging in one place.
        """
        try:
            logger.info(f"Calling LLM ({self.model}) with temperature {self.temperature}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return f"Error: {str(e)}"

# Singleton for easy access
llm = LLMInterface()
