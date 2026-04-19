from openai import OpenAI
from app.core.config import settings

class SampleAgent:
    """
    A minimal AI agent that uses LLM to process user queries.
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS

    def run(self, user_input: str) -> str:
        """
        Executes the agent logic using GPT-4o-mini.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful and concise AI assistant."},
                    {"role": "user", "content": user_input}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
