import os
import time
from typing import Optional
from openai import OpenAI
from shared.utils import load_config

# Initialize configuration
config = load_config()

# OpenAI client instantiated globally (ensure load_environment is called before using call_llm)
client = None

def call_llm(prompt: str, system_prompt: str = "", logger=None) -> str:
    """
    Generic LLM caller using OpenAI SDK.
    Includes retries and basic timeout handling.
    
    Args:
        prompt (str): The user query/prompt.
        system_prompt (str): Optional system instructions.
        logger: Optional logger instance to capture call metrics.
        
    Returns:
        str: The LLM response.
    """
    global client
    if client is None:
        if logger:
            logger.log("SYSTEM", "Initializing OpenAI client...", level="DEBUG")
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    model = config.get("model", "gpt-4o-mini")
    temperature = config.get("temperature", 0.3)
    max_tokens = config.get("max_tokens", 700)
    max_retries = config.get("max_retries", 3)

    if logger:
        logger.log("LLM_CALL", f"Requesting model: {model} (Temp: {temperature}, Max Tokens: {max_tokens})", level="DEBUG")
        logger.log("LLM_CALL", f"Prompt length: {len(prompt)} characters", level="DEBUG")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    for attempt in range(max_retries):
        try:
            if logger and attempt > 0:
                logger.log("LLM_RETRY", f"Retry attempt {attempt} of {max_retries - 1}...", level="WARNING")
            
            start_time = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=30.0
            )
            duration = time.time() - start_time
            
            content = response.choices[0].message.content.strip()
            if logger:
                logger.log("LLM_RESPONSE", f"Received response in {duration:.2f}s. Content length: {len(content)} characters.", level="DEBUG")
            
            return content
        except Exception as e:
            if logger:
                logger.log("LLM_ERROR", f"Attempt {attempt} failed: {str(e)}", level="ERROR")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                error_msg = f"Error interacting with LLM after {max_retries} attempts: {str(e)}"
                if logger:
                    logger.log("LLM_CRITICAL", error_msg, level="CRITICAL")
                return error_msg
    
    return ""
