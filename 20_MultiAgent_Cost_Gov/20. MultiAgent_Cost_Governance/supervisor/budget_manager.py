from shared.logger import logger

class BudgetManager:
    def __init__(self, budget: float):
        self.budget = budget
        logger.info(f"[BUDGET INITIALIZED] Limit: ${self.budget:.4f}")

    def is_within_budget(self, current_cost: float) -> bool:
        """
        Check if cost is within allowed budget
        """
        return current_cost < self.budget

    def get_remaining_budget(self, current_cost: float) -> float:
        return max(0.0, self.budget - current_cost)

    def get_budget_usage_pct(self, current_cost: float) -> float:
        if self.budget == 0:
            return 1.0
        return (current_cost / self.budget)
