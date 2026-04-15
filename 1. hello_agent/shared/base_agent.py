"""
Base Agent definition.
"""
from abc import ABC, abstractmethod
from typing import Tuple
from shared.logger import AgentLogger

class BaseAgent(ABC):
    """
    Base class for agent implementations.
    """
    def __init__(self):
        self.logger = AgentLogger()

    @abstractmethod
    def run(self, user_input: str) -> Tuple[str, str]:
        """
        Runs the agent loop.
        
        Args:
            user_input (str): The query from the user.
            
        Returns:
            Tuple[str, str]: (Final Answer, Log Trace String)
        """
        pass
