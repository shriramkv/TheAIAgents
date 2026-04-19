import json
from typing import List, Dict, Any, Tuple
from shared.base_agent import BaseAgent
from shared.llm import call_llm

class CoordinatorAgent(BaseAgent):
    """
    Agent responsible for selecting the best flight and explaining why.
    """
    def __init__(self):
        super().__init__("Coordinator")

    def run(self, valid_flights: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], str]:
        if not valid_flights:
            self.logger.warning("No valid flights to coordinate.")
            return None, "No flights met your criteria."
            
        self.logger.info(f"Selecting best flight from {len(valid_flights)} options...")
        
        # We'll use the LLM to help make the decision and provide reasoning
        prompt = f"""
        Here is a list of validated flight options:
        {json.dumps(valid_flights, indent=2)}
        
        Please select the best flight and explain your reasoning clearly. 
        Focus on value for money, travel time, and convenience.
        """
        
        explanation = call_llm(prompt, self.system_prompt)
        
        # For simplicity in this demo, we'll pick the first one as the 'best' object 
        # but the LLM provides the real logic in the explanation.
        # In a real system, we'd have the LLM return a JSON with the ID of the chosen flight.
        best_flight = valid_flights[0] 
        
        self.logger.info("Coordinator selected the best flight.")
        return best_flight, explanation
