import json
from typing import Dict, Any, Tuple
from agents.researcher import ResearcherAgent
from agents.validator import ValidatorAgent
from agents.coordinator import CoordinatorAgent
from shared.logger import get_logger

class FlightFinderAgent:
    """
    Main orchestrator for the Multi-Agent Flight Finder system.
    """
    def __init__(self):
        self.logger = get_logger("Orchestrator")
        self.researcher = ResearcherAgent()
        self.validator = ValidatorAgent()
        self.coordinator = CoordinatorAgent()

    def find_flights(self, origin: str, destination: str, date: str, budget: float, max_layovers: int) -> Dict[str, Any]:
        """
        Executes the full multi-agent flight finding pipeline.
        """
        logs = []
        
        # 1. RESEARCHER finds all flights
        logs.append(f"--- [RESEARCHER START] ---")
        logs.append(f"Searching for flights: {origin} -> {destination} on {date}")
        all_flights = self.researcher.run(origin, destination, date)
        logs.append(f"Found {len(all_flights)} potential flights.")
        logs.append(json.dumps(all_flights, indent=2))
        
        # 2. VALIDATOR filters based on constraints
        logs.append(f"\n--- [VALIDATOR START] ---")
        constraints = {"budget": budget, "max_layovers": max_layovers}
        logs.append(f"Applying constraints: {constraints}")
        valid_flights = self.validator.run(all_flights, constraints)
        logs.append(f"Kept {len(valid_flights)} flights after validation.")
        logs.append(json.dumps(valid_flights, indent=2))
        
        # 3. COORDINATOR selects best and explains
        logs.append(f"\n--- [COORDINATOR START] ---")
        best_flight, explanation = self.coordinator.run(valid_flights)
        
        if best_flight:
            logs.append(f"Recommendation complete.")
        else:
            logs.append(f"No recommendation possible.")

        return {
            "all_flights": all_flights,
            "filtered_flights": valid_flights,
            "best_flight": best_flight,
            "explanation": explanation,
            "logs": "\n".join(logs)
        }
