from typing import Dict, Any, Optional

class CostTracker:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Tracks token usage and calculates costs.
        """
        self.config = config or {}
        self.cost_per_token = self.config.get("cost_per_token", 0.00001)
        self.total_tokens = 0
        self.total_cost = 0.0

    def track(self, response_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts token usage from response metadata and updates running totals.
        
        :param response_metadata: Metadata containing 'usage' or 'total_tokens'
        :returns: Dict with usage for this specific call
        """
        # Support different common metadata formats
        tokens = 0
        if "usage" in response_metadata:
            tokens = response_metadata["usage"].get("total_tokens", 0)
        elif "total_tokens" in response_metadata:
            tokens = response_metadata["total_tokens"]
        
        cost = tokens * self.cost_per_token
        
        self.total_tokens += tokens
        self.total_cost += cost
        
        return {
            "tokens_used": tokens,
            "cost": cost
        }

    def get_totals(self) -> Dict[str, Any]:
        return {
            "total_tokens": self.total_tokens,
            "total_overall_cost": self.total_cost
        }

    def reset(self):
        self.total_tokens = 0
        self.total_cost = 0.0
