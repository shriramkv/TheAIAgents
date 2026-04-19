import logging
import sys

def setup_logger(name: str = "web_research_agent") -> logging.Logger:
    """
    Sets up a logger that outputs to both console and a list (for Gradio).
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if called multiple times
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

    return logger

class AgentLogger:
    """
    A simple logger to capture agent trace for UI display.
    """
    def __init__(self):
        self.logs = []

    def info(self, message: str):
        formatted_message = f"[INFO] {message}"
        print(formatted_message)
        self.logs.append(formatted_message)

    def error(self, message: str):
        formatted_message = f"[ERROR] {message}"
        print(formatted_message)
        self.logs.append(formatted_message)

    def get_logs(self) -> str:
        return "\n".join(self.logs)

    def clear(self):
        self.logs = []
