from abc import ABC, abstractmethod
from typing import Any, Dict
from shared.logger import get_logger
from shared.utils import load_prompt

class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(name)
        self.system_prompt = load_prompt(name.lower())

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Main execution logic for the agent.
        """
        pass
