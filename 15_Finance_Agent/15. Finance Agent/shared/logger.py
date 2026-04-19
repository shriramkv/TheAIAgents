import logging
import sys

def setup_logger(name: str = "FinancialAnalyst") -> logging.Logger:
    """
    Sets up a standardized logger for the project.
    """
    logger = logging.getLogger(name)
    
    # Only add handlers if they don't already exist to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler with a specific format
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Global logger instance
logger = setup_logger()
