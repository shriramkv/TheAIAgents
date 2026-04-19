from shared.base_agent import BaseAgent
from shared.llm import call_llm
from typing import Dict, Any

class LightweightAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("LightweightAgent")
        self.model_name = model_name

    def run(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Fast and cheap responses using gpt-4o-mini
        """
        system_prompt = (
            "You are a lightweight, efficient AI agent. "
            "Keep your responses very concise and direct and avoid verbosity."
        )
        return call_llm(prompt, self.model_name, system_prompt)
