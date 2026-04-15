import os
from openai import OpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm_with_tools(
    messages: List[Dict[str, Any]], 
    tools: List[Dict[str, Any]], 
    model: str = "gpt-4o-mini", 
    temperature: float = 0.2, 
    max_tokens: int = 500
) -> Any:
    """
    Calls the OpenAI API with an array of messages and available tools.
    
    Args:
        messages: The chat history and system prompt.
        tools: The JSON schema definitions of the tools available.
        model: The LLM model to use.
        temperature: Controls randomness in the output.
        max_tokens: Max generated tokens.
        
    Returns:
        The response message object from OpenAI.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message
