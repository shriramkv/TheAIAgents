import time
from typing import Optional, List, Dict, Any
from openai import OpenAI
from shared.utils import load_config, get_env_var
from shared.logger import logger

class LLMService:
    def __init__(self):
        self.config = load_config()
        self.api_key = get_env_var("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=self.api_key)

    def call_llm(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """
        Executes a call to the LLM with retry logic.
        """
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.get("model", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.config.get("temperature", 0.3)
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"Error calling LLM (Attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    return f"Failed to get response after {max_retries} attempts."
        
        return "Unknown error in LLM call."

llm_service = LLMService()

def call_llm(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    """Standard LLM call with retries as requested in requirements."""
    return llm_service.call_llm(prompt, system_prompt)
