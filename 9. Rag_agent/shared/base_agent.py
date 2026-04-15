from abc import ABC, abstractmethod
from typing import Tuple

class BaseAgent(ABC):
    """
    Abstract base class defining the standard interface for AI agents.
    """
    @abstractmethod
    def run(self, query: str) -> Tuple[str, str, str]:
        """
        Executes the main logic of the agent.

        Args:
            query (str): The user query to answer.

        Returns:
            Tuple[str, str, str]: Context used, final answer, execution logs.
        """
        pass
