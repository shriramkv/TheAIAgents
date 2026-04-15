from abc import ABC, abstractmethod
from typing import Tuple

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Provides the core interface every agent must implement.
    """
    
    @abstractmethod
    def run(self, user_input: str) -> Tuple[str, str]:
        """
        Runs the agent logic.
        
        Args:
            user_input: The string query provided by the user.
            
        Returns:
            Tuple[str, str]: (Final Answer, Reasoning Trace Log)
        """
        pass
