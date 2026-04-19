import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any
from .logger import logger

load_dotenv()

class LLMInterface:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=self.api_key)

    def call_llm(self, prompt: str, model: str, system_prompt: str = "You are a helpful assistant.") -> Dict[str, Any]:
        """
        Call OpenAI API and return response with token usage
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            usage = response.usage
            content = response.choices[0].message.content
            
            return {
                "response": content,
                "input_tokens": usage.prompt_tokens,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "model": model
            }
        except Exception as e:
            logger.error(f"Error calling LLM ({model}): {str(e)}")
            raise

llm_interface = LLMInterface()

def call_llm(prompt: str, model: str, system_prompt: str = "You are a helpful assistant.") -> Dict[str, Any]:
    return llm_interface.call_llm(prompt, model, system_prompt)
