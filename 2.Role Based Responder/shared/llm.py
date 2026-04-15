import os
from openai import OpenAI
import openai

def call_llm(user_input: str, system_prompt: str, config: dict) -> str:
    """
    Calls the LLM using the OpenAI SDK with a role-based system prompt.
    
    Args:
        user_input (str): The specific query from the user.
        system_prompt (str): The role-defining system prompt.
        config (dict): The configuration settings loaded from config.yaml.
        
    Returns:
        str: The generated text response from the LLM.
        
    Raises:
        ValueError: If the API key is not configured or an API error occurs.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please set it before running.")
        
    client = OpenAI(api_key=api_key)
    
    model = config.get("model", "gpt-4o-mini")
    temperature = config.get("temperature", 0.5)
    max_tokens = config.get("max_tokens", 400)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        # Handle fundamental API-related errors
        raise ValueError(f"OpenAI API error occurred: {e}")
    except Exception as e:
        # Catch unexpected errors to avoid crashing the whole agent loop unsafely
        raise ValueError(f"Unexpected error when calling LLM: {e}")
