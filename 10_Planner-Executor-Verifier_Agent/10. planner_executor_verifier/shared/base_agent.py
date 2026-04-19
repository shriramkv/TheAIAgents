from shared.utils import load_environment, load_config
from shared.logger import AgentLogger

class BaseAgent:
    """
    Foundation agent class initializing context like config, logger, and environment.
    """
    def __init__(self):
        # Load environment variables (e.g. OPENAI_API_KEY)
        load_environment()
        
        # Load yaml config
        self.config = load_config()
        self.max_retries = self.config.get("max_retries", 3)
        
        # Initialize logger
        self.logger = AgentLogger()
        
    def reset(self):
        """Resets the state of the agent for a fresh run."""
        self.logger.clear()
