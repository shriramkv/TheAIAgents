from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Defines the standard run method.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, user_query: str) -> Dict[str, Any]:
        """
        Execute the agent's logic for a given query.
        """
        pass
