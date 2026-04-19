from abc import ABC, abstractmethod
from typing import Any, Dict
from shared.logger import logger

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logger

    @abstractmethod
    def run(self, user_input: str) -> str:
        """
        Main execution loop for the agent.
        """
        pass

    def log_input(self, user_input: str):
        self.logger.log_input(user_input)

    def log_result(self, result: str):
        self.logger.log_result(result)
