"""
Logger utility for the Hello Agent system.
Provides formatted logging for Thoughts, Actions, Observations, and Final answers.
"""
from typing import List

class AgentLogger:
    """
    Logs agent trace steps and provides string representation for UI.
    """
    def __init__(self):
        self.logs: List[str] = []

    def log(self, step_type: str, message: str) -> None:
        """Appends a log step string and prints it."""
        log_entry = f"{step_type.upper()}: {message}"
        self.logs.append(log_entry)
        print(log_entry)

    def get_logs_string(self) -> str:
        """Returns all logs as a single new-line separated string."""
        return "\n".join(self.logs)

    def clear(self) -> None:
        """Clears the logger state."""
        self.logs = []
