from shared.logger import logger

class DecisionEngine:
    def decide(self, current_cost: float, budget: float, task_completed: bool = False):
        """
        Decide:
        - continue
        - switch model (handled by router, but engine can flag)
        - stop execution
        """
        if task_completed:
            logger.info("[DECISION] stop (Task completed)")
            return "stop"

        if current_cost >= budget:
            logger.warning(f"[DECISION] stop (Budget exceeded: ${current_cost:.4f} >= ${budget:.4f})")
            return "stop"
        
        usage_pct = current_cost / budget if budget > 0 else 1.0
        
        if usage_pct > 0.9:
            logger.warning(f"[DECISION] continue (Critical budget level: {usage_pct:.1%})")
        else:
            logger.info(f"[DECISION] continue (Usage: {usage_pct:.1%})")
            
        return "continue"
