import time
from typing import Any, Dict

def format_agent_logs(input_text: str, response_text: str, time_taken: float) -> str:
    """
    Formats the interaction logs as requested.
    """
    return (
        f"[INPUT]\n{input_text}\n\n"
        f"[RESPONSE]\n{response_text}\n\n"
        f"[TIME TAKEN]\n{time_taken:.4f}s"
    )

def get_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
