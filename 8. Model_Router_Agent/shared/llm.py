import os
from  typing import Optional, Dict, Any
from openai import OpenAI
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(
    prompt: str, 
    model: str, 
    temperature: float = 0.7, 
    max_tokens: int = 500,
    retries: int = 3,
    timeout_seconds: int = 10,
    system_prompt: Optional[str] = None
) -> str:
    """
    Generic LLM caller.
    Supports model selection, retries, and timeout handling.
    """
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})

    attempt = 0
    while attempt < retries:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout_seconds
            )
            val = response.choices[0].message.content
            return val if val else ""
            
        except Exception as e:
            attempt += 1
            if attempt >= retries:
                raise Exception(f"Failed to call LLM after {retries} attempts. Last error: {str(e)}")
            time.sleep(1) # Simple static backoff
