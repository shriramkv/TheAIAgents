import logging
from typing import Any

# Configure standard logging to output cleanly
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

class AgentLogger:
    """
    Utility class to format and log agent reasoning steps.
    """

    @staticmethod
    def log_thought(content: str) -> str:
        msg = f"[THOUGHT] {content}"
        logger.info(msg)
        return msg
        
    @staticmethod
    def log_action(tool_name: str, args: Any) -> str:
        msg = f"[ACTION] Selected tool '{tool_name}' with args: {args}"
        logger.info(msg)
        return msg
        
    @staticmethod
    def log_observation(result: Any) -> str:
        msg = f"[OBSERVATION] Tool result: {result}"
        logger.info(msg)
        return msg
        
    @staticmethod
    def log_final(answer: str) -> str:
        msg = f"[FINAL] {answer}"
        logger.info(msg)
        return msg
