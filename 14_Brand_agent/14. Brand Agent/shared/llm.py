import time
from openai import OpenAI
from typing import Any, Dict, List
from shared.logger import logger
from shared.utils import load_config, get_env_var

class LLMInterface:
    def __init__(self):
        self.api_key = get_env_var("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.config = load_config()
        self.model = self.config.get("model", "gpt-4o-mini")
        self.temperature = self.config.get("temperature", 0.3)

    def call_llm(self, prompt: str, system_prompt: str = "You are a helpful assistant.", max_retries: int = 3) -> str:
        """
        Calls the OpenAI LLM with retry logic.
        """
        for attempt in range(max_retries):
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
                logger.error(f"LLM call failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e
        return ""

llm = LLMInterface()

def call_llm(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    return llm.call_llm(prompt, system_prompt)
