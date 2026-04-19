from shared.logger import logger

class CostAwareRouter:
    def __init__(self, config: dict):
        self.config = config
        self.switch_threshold = config['router']['switch_to_lightweight_pct']
        self.primary_model = config['models']['primary']['name']
        self.lightweight_model = config['models']['lightweight']['name']

    def select_model(self, budget_usage_pct: float) -> str:
        """
        Decide:
        - high budget remaining → primary model
        - low budget remaining → lightweight model
        """
        if budget_usage_pct > self.switch_threshold:
            logger.info(f"[MODEL SELECTED] {self.lightweight_model} (Budget usage: {budget_usage_pct:.1%})")
            return self.lightweight_model
        
        logger.info(f"[MODEL SELECTED] {self.primary_model} (Budget usage: {budget_usage_pct:.1%})")
        return self.primary_model
