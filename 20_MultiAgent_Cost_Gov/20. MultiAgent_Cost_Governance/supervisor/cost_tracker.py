from shared.logger import logger

class CostTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.history = []

    def update(self, input_tokens: int, output_tokens: int, cost: float, model: str):
        """
        Update running token and cost totals
        """
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost += cost
        
        entry = {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "cumulative_cost": self.total_cost
        }
        self.history.append(entry)
        
        logger.info(f"[COST UPDATE] model={model}, tokens={input_tokens+output_tokens}, cost=${cost:.6f}, total=${self.total_cost:.6f}")

    def get_total_cost(self) -> float:
        return self.total_cost

    def get_history(self) -> list:
        return self.history
