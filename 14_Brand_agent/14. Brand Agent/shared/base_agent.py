from abc import ABC, abstractmethod
from shared.logger import logger

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents in the Brand Monitoring System.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logger

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Main execution method for the agent.
        """
        pass

    def log_step(self, message: str):
        """
        Logs a specific step in the agent's reasoning or execution.
        """
        self.logger.info(f"[{self.name}] {message}")
