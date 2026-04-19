import logging
import sys
import time
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("mcp_tool_server")

def log_tool_call(tool_name: str, parameters: Dict[str, Any], response: Any, duration: float):
    """
    Logs tool execution Details in the requested format.
    """
    logger.info("-" * 40)
    logger.info(f"[REQUEST] tool={tool_name}")
    logger.info(f"[PARAMS] {parameters}")
    logger.info(f"[RESPONSE] {response}")
    logger.info(f"[TIME TAKEN] {duration:.4f}s")
    logger.info("-" * 40)
