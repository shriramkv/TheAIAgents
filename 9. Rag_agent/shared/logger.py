import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger instance tailored for the RAG agent, outputting to stdout.

    Args:
        name (str): The name of the logger, usually __name__.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
