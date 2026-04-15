from abc import ABC, abstractmethod
from typing import Tuple

class BaseAgent(ABC):
    """
    Abstract base class for agents.
    Enforces the run method implementation.
    """
    @abstractmethod
    def run(self, user_input: str) -> Tuple[str, str]:
        """
        Executes the agent logic.
        Returns:
            final_answer (str): The final generated answer
            full_trace (str): Formatting string of agent's reasoning trace
        """
        pass
