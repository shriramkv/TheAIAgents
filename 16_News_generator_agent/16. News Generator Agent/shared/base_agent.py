from abc import ABC, abstractmethod
from shared.logger import logger

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """
    def __init__(self, name: str):
        self.name = name
        self.logs = []
        logger.info(f"Initialized agent: {self.name}")

    def log_step(self, step_name: str, data: str):
        """
        Record a step in the agent's execution for transparency.
        """
        log_entry = f"[{step_name.upper()}]\n{data}\n"
        self.logs.append(log_entry)
        logger.info(f"Step completed: {step_name}")

    def get_logs(self) -> str:
        """
        Return the accumulated logs as a single string.
        """
        return "\n".join(self.logs)

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Main execution loop to be implemented by child classes.
        """
        pass
