from shared.base_agent import BaseAgent
from shared.utils import load_config, calculate_cost
from shared.logger import logger
from supervisor.cost_tracker import CostTracker
from supervisor.budget_manager import BudgetManager
from supervisor.router import CostAwareRouter
from supervisor.decision_engine import DecisionEngine
from agents.primary_agent import PrimaryAgent
from agents.lightweight_agent import LightweightAgent
from typing import Dict, Any, List

class CostGovernorAgent(BaseAgent):
    def __init__(self, budget: float = None):
        super().__init__("CostGovernorAgent")
        self.config = load_config()
        
        # Override budget if provided
        limit = budget if budget is not None else self.config['budget']['default_limit_usd']
        
        # Initialize supervisor components
        self.cost_tracker = CostTracker()
        self.budget_manager = BudgetManager(limit)
        self.router = CostAwareRouter(self.config)
        self.decision_engine = DecisionEngine()
        
        # Initialize worker agents
        self.primary_worker = PrimaryAgent(self.config['models']['primary']['name'])
        self.lightweight_worker = LightweightAgent(self.config['models']['lightweight']['name'])
        
        self.logs = []

    def _log_event(self, event: str):
        self.logs.append(event)
        # logger already prints to console

    def run(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Main execution loop for the Cost Governor Agent
        """
        logger.info(f"[INPUT] {prompt}")
        self._log_event(f"Input: {prompt}")
        
        # Simulate a 3-step reasoning process to demonstrate the loop
        steps = [
            f"Step 1: Analyze the core requirements of: {prompt}",
            f"Step 2: Research potential solutions for: {prompt}",
            f"Step 3: Synthesize a final response for: {prompt}"
        ]
        
        final_response_parts = []
        task_completed = False
        
        for i, step_prompt in enumerate(steps):
            # 1. Check remaining budget
            current_cost = self.cost_tracker.get_total_cost()
            usage_pct = self.budget_manager.get_budget_usage_pct(current_cost)
            
            # 2. Router selects model
            model_name = self.router.select_model(usage_pct)
            
            # 3. Call selected agent
            worker = self.primary_worker if model_name == self.config['models']['primary']['name'] else self.lightweight_worker
            
            try:
                result = worker.run(step_prompt)
                
                # 4. Update cost
                pricing = self.config['models']['primary'] if model_name == self.config['models']['primary']['name'] else self.config['models']['lightweight']
                step_cost = calculate_cost(result['input_tokens'], result['output_tokens'], pricing)
                
                self.cost_tracker.update(
                    result['input_tokens'], 
                    result['output_tokens'], 
                    step_cost, 
                    model_name
                )
                
                final_response_parts.append(result['response'])
                
                # 5. Decision engine decides
                is_last_step = (i == len(steps) - 1)
                decision = self.decision_engine.decide(
                    self.cost_tracker.get_total_cost(), 
                    self.budget_manager.budget,
                    task_completed=is_last_step
                )
                
                self._log_event(f"[STEP {i+1}] Model: {model_name}, Cost: ${step_cost:.6f}, Decision: {decision}")
                
                if decision == "stop":
                    break
                    
            except Exception as e:
                logger.error(f"Execution failed at step {i+1}: {str(e)}")
                self._log_event(f"Error at step {i+1}: {str(e)}")
                break

        final_cost = self.cost_tracker.get_total_cost()
        logger.info(f"[FINAL COST] ${final_cost:.6f}")
        
        return {
            "response": "\n\n".join(final_response_parts),
            "total_cost": final_cost,
            "tokens": self.cost_tracker.total_input_tokens + self.cost_tracker.total_output_tokens,
            "history": self.cost_tracker.get_history(),
            "decision_logs": self.logs
        }
