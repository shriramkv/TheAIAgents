import os
from openai import OpenAI
from dotenv import load_dotenv
from shared.logger import get_logger
from shared.utils import load_config

# Load environment variables
load_dotenv()

logger = get_logger("LLM")
config = load_config()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt: str, system_prompt: str = "") -> str:
    """
    Standard LLM call with basic error handling and logging.
    """
    try:
        logger.info(f"Calling LLM ({config['model']})...")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=config.get("temperature", 0.3)
        )
        
        content = response.choices[0].message.content
        logger.info("LLM call successful.")
        return content.strip()
        
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return f"Error: {str(e)}"
