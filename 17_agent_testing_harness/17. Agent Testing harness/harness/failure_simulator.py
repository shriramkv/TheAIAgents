import random
import time
from typing import Any, Callable, Optional, Dict

class FailureSimulator:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Simulates failures in agent tools.
        """
        self.config = config or {}
        # Default failure rates
        self.failure_rate = self.config.get("failure_rate", 0.0)
        self.timeout_chance = self.config.get("timeout_chance", 0.0)
        self.latency_range = self.config.get("latency_range", [0.1, 2.0])

    def inject_failure(self, tool_name: str, tool_func: Callable) -> Callable:
        """
        Wraps a tool function with failure simulation logic.
        """
        def wrapped(*args, **kwargs):
            # Check for specific tool config or global config
            tool_config = self.config.get("tools", {}).get(tool_name, {})
            fail_rate = tool_config.get("failure_rate", self.failure_rate)
            to_chance = tool_config.get("timeout_chance", self.timeout_chance)
            
            # Simulate latency
            if "latency" in tool_config:
                time.sleep(tool_config["latency"])
            elif fail_rate > 0 or to_chance > 0:
                # Random latency for realism if failure is possible
                time.sleep(random.uniform(*self.latency_range))

            # Roll for timeout
            if random.random() < to_chance:
                raise TimeoutError(f"Tool {tool_name} timed out simulation.")

            # Roll for generic failure
            if random.random() < fail_rate:
                return "ERROR: Tool execution failed (Simulated)"

            return tool_func(*args, **kwargs)

        return wrapped
