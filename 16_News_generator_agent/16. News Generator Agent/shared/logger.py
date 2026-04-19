import logging
import sys

def setup_logger(name: str = "news_agent") -> logging.Logger:
    """
    Sets up a structured logger for the news agent.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()
