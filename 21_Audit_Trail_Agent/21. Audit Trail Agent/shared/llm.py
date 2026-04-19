import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, List

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(messages: List[Dict[str, str]], model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """
    Calls the OpenAI LLM and returns the response along with usage metadata.
    
    Args:
        messages: List of message dictionaries (role/content)
        model: Model name to use
        
    Returns:
        Dictionary containing 'response' and 'tokens_used'
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    
    return {
        "response": response.choices[0].message.content,
        "tokens_used": response.usage.total_tokens,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens
    }
