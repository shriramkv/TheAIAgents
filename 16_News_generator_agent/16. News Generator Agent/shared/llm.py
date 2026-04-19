import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
from shared.logger import logger

# Load environment variables
load_dotenv()

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def call_llm(prompt: str, system_prompt: str = "You are a helpful news assistant.") -> str:
    """
    Standardized LLM call with retries and error handling.
    """
    config = load_config()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model=config.get("model", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=config.get("temperature", 0.4),
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return f"Error: {e}"
