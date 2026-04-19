from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Execute the agent logic.
        """
        pass

    def log_step(self, message: str):
        """
        Utility to log a step in the process.
        """
        print(f"[{self.__class__.__name__}] {message}")
