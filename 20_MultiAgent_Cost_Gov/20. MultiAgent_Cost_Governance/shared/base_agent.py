from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Execute agent logic and return response + metadata
        """
        pass
