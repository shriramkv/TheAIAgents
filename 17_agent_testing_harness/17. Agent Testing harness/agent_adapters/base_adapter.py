from abc import ABC, abstractmethod
from typing import Any, Dict, List

class AgentAdapter(ABC):
    """
    Abstract base class for agent adapters.
    Standardizes the interface for interacting with different agent frameworks.
    """

    @abstractmethod
    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Executes the agent with the given prompt.
        
        Must return a dictionary containing:
        - "output": str (Final response)
        - "steps": List[Dict[str, Any]] (Trace of actions taken)
        - "metadata": Dict[str, Any] (Token usage, latency, etc.)
        """
        pass

    def _format_step(self, action: str, input: Any, output: Any, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper to format a step consistently.
        """
        return {
            "action": action,
            "input": input,
            "output": output,
            "metadata": metadata or {}
        }
