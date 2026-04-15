from abc import ABC, abstractmethod
from typing import Any

class BaseAgent(ABC):
    """
    Base Agent Interface.
    """
    
    @abstractmethod
    def run(self, user_input: str) -> Any:
        """
        Main execution loop for the agent.
        """
        pass
