from openai import OpenAI
from shared.utils import load_config, get_env_var

class LLMHandler:
    """
    Handles interactions with OpenAI LLM.
    """
    def __init__(self):
        config = load_config()
        self.model = config.get("model", "gpt-4o-mini")
        self.client = OpenAI(api_key=get_env_var("OPENAI_API_KEY"))

    def call_llm(self, prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
        """
        Generate grounded response using the prompt.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"

# Singleton helper
_llm_handler = None

def call_llm(prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
    global _llm_handler
    if _llm_handler is None:
        _llm_handler = LLMHandler()
    return _llm_handler.call_llm(prompt, system_prompt)
