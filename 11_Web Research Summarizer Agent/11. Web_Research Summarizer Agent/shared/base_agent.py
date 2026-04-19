from abc import ABC, abstractmethod
from typing import Any
from shared.llm import LLMHandler
from shared.logger import AgentLogger

class BaseAgent(ABC):
    """
    Abstract base class for agents.
    """
    def __init__(self):
        self.llm = LLMHandler()
        self.logger = AgentLogger()

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Main execution method for the agent.
        """
        pass
