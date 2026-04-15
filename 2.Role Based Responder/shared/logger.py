import logging
from typing import List

# Setup standard python logger for console output
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

class AgentLogger:
    """
    Custom logger to track the agent flow (Role, Thought, Action, Final).
    Maintains an internal state to return logs as a formatted string for UI display.
    """
    def __init__(self):
        self.logs: List[str] = []
        
    def log(self, category: str, message: str) -> None:
        """
        Record a log entry with a specific category.
        
        Args:
            category (str): The category of the log (e.g., ROLE, THOUGHT, ACTION).
            message (str): The log message content.
        """
        formatted_message = f"[{category.upper()}] {message}"
        self.logs.append(formatted_message)
        logger.info(formatted_message)
        
    def get_logs_as_string(self) -> str:
        """
        Retrieve all collected logs formatted as a single string.
        
        Returns:
            str: The concatenated log history.
        """
        return "\n".join(self.logs)
        
    def clear(self) -> None:
        """Clear the current log history."""
        self.logs.clear()
