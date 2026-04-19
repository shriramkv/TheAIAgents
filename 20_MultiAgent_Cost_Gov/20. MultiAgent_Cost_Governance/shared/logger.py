import logging
import sys
import os

def setup_logger(name: str = "CostGovernor"):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
        
        # Create console handler with a specific format
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Format for cost tracking transparency
        formatter = logging.Formatter(
            '[%(name)s] %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Singleton-like instance access
logger = setup_logger()
