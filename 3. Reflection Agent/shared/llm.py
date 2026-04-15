import os
from openai import OpenAI
from dotenv import load_dotenv

from .utils import load_config

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI client conditionally
client = OpenAI(api_key=api_key) if api_key else None

# Load config settings like model and temperature
config = load_config()

def call_llm(user_input: str, system_prompt: str) -> str:
    """
    Generic LLM caller with standard configurations.
    
    Args:
        user_input (str): The actual query/content to send.
        system_prompt (str): The role/instructions for the system.
        
    Returns:
        str: The raw generated text from the LLM.
    """
    if not client:
        return "Error: OPENAI_API_KEY is missing. Please set it in your .env file."
        
    try:
        response = client.chat.completions.create(
            model=config.get("model", "gpt-4o-mini"),
            temperature=config.get("temperature", 0.4),
            max_tokens=config.get("max_tokens", 500),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
