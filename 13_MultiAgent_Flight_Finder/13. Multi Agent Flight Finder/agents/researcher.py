import json
from typing import List, Dict, Any
from shared.base_agent import BaseAgent
from shared.llm import call_llm
from tools.flight_search import search_flights

class ResearcherAgent(BaseAgent):
    """
    Agent responsible for finding flight options.
    """
    def __init__(self):
        super().__init__("Researcher")

    def run(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        self.logger.info(f"Searching for flights from {origin} to {destination} on {date}...")
        
        # 1. Use the search tool to get raw data
        raw_flights = search_flights(origin, destination, date)
        
        # 2. Use LLM to structure/summarize if needed, 
        # but here we can just return the structured data directly for efficiency.
        # We can also use the LLM to provide a nice natural language summary of found options.
        prompt = f"Found {len(raw_flights)} flights from {origin} to {destination} on {date}. Raw data: {json.dumps(raw_flights)}"
        
        # In a real scenario, the LLM might process the raw data to ensure it's in a specific format.
        # For this prototype, we return the raw list as it's already well-formatted by the tool.
        self.logger.info(f"Researcher found {len(raw_flights)} options.")
        return raw_flights
