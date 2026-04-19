from typing import List, Dict, Any
from tools.mock_data import get_mock_flights

def search_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """
    Returns list of flights:
    [
        {
            "airline": "...",
            "price": ...,
            "duration": "...",
            "layovers": ...,
            "departure": "...",
            "arrival": "..."
        }
    ]
    """
    # For now, we use mock data. 
    # In a real system, this would call an external Travel API.
    return get_mock_flights(origin, destination, date)
