from shared.base_agent import BaseAgent
from shared.llm import call_llm
from typing import Dict, Any

class PrimaryAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("PrimaryAgent")
        self.model_name = model_name

    def run(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Full quality responses using high-end model
        """
        system_prompt = (
            "You are a high-end AI agent capable of deep reasoning and detailed analysis. "
            "Provide comprehensive, thorough, and well-structured responses."
        )
        return call_llm(prompt, self.model_name, system_prompt)
