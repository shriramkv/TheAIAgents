from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all AI Agents.
    Enforces a standard structure where an agent must implement a run method.
    """
    
    @abstractmethod
    def run(self, user_input: str):
        """
        Main entry point for the agent's logic.
        
        Args:
            user_input (str): The query or input provided by the user.
        """
        pass
