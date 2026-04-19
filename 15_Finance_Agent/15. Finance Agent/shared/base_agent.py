from abc import ABC, abstractmethod
from typing import Any, Dict
from shared.logger import logger

class BaseAgent(ABC):
    """
    Abstract Base Class for all Agents.
    Why: Ensures every agent has a consistent run() interface and access to logging.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logger
        self.logger.info(f"Initialized Agent: {self.name}")

    @abstractmethod
    def run(self, input_data: Any) -> Dict[str, Any]:
        """
        The main entry point for the agent logic.
        """
        pass
