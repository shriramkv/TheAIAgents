import logging
import sys

def setup_logger(name: str = "agent-harness") -> logging.Logger:
    """
    Sets up a structured logger for the harness.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(levelname)s] [%(name)s] %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()
