from typing import List, Dict, Any, Optional

class LoopDetector:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Detects loops in agent steps.
        """
        self.config = config or {}
        self.max_steps = self.config.get("max_steps", 10)
        self.loop_threshold = self.config.get("loop_threshold", 3)

    def check(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes steps to detect infinite loops or excessive iterations.
        
        :param steps: List of step dictionaries (must containing 'action' and 'input')
        :returns: Dict with 'loop_detected' (bool) and 'reason' (str)
        """
        if not steps:
            return {"loop_detected": False, "reason": "No steps recorded."}

        # Check total steps
        if len(steps) > self.max_steps:
            return {
                "loop_detected": True, 
                "reason": f"Total steps ({len(steps)}) exceeded max limit ({self.max_steps})."
            }

        # Check for repeated actions with same input
        action_counts = {}
        for step in steps:
            action = step.get("action")
            action_input = str(step.get("input", ""))
            key = f"{action}:{action_input}"
            
            action_counts[key] = action_counts.get(key, 0) + 1
            if action_counts[key] >= self.loop_threshold:
                return {
                    "loop_detected": True,
                    "reason": f"Action '{action}' with input '{action_input}' repeated {action_counts[key]} times."
                }

        return {"loop_detected": False, "reason": "No loops detected."}
