import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt: str, model_name: str = "gpt-4o-mini") -> str:
    """
    Generates a response using the OpenAI Chat Completions API based on the retrieved context.

    Args:
        prompt (str): The compiled prompt including context and user query.
        model_name (str): The language model to use for generation.

    Returns:
        str: The LLM's answer.
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful, knowledgeable AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()
