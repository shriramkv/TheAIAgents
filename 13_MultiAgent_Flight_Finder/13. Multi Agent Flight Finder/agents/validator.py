import json
from typing import List, Dict, Any
from shared.base_agent import BaseAgent
from shared.llm import call_llm

class ValidatorAgent(BaseAgent):
    """
    Agent responsible for filtering flights based on constraints.
    """
    def __init__(self):
        super().__init__("Validator")

    def run(self, flights: List[Dict[str, Any]], constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.logger.info(f"Validating {len(flights)} flights against constraints: {constraints}...")
        
        budget = constraints.get("budget", float('inf'))
        max_layovers = constraints.get("max_layovers", float('inf'))
        
        # Filtering logic
        valid_flights = [
            f for f in flights 
            if f['price'] <= budget and f['layovers'] <= max_layovers
        ]
        
        self.logger.info(f"Validator kept {len(valid_flights)} out of {len(flights)} flights.")
        return valid_flights
