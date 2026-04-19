from typing import Dict, Any

def query_internal_db(query: str) -> Dict[str, Any]:
    """
    Simulates an internal database query.
    
    Args:
        query (str): The natural language query or SQL command.
        
    Returns:
        dict: Query results or mock dataset.
    """
    # Simple keyword-based mock responses
    query_lower = query.lower()
    
    if "inventory" in query_lower:
        return {
            "results": [
                {"item": "Laptop X1", "stock": 45, "warehouse": "East-01"},
                {"item": "Monitor 4K", "stock": 12, "warehouse": "West-04"}
            ],
            "status": "Success"
        }
    elif "revenue" in query_lower:
        return {
            "q1_revenue": "$1.2M",
            "q2_forecast": "$1.5M",
            "growth": "+15%"
        }
    
    return {
        "message": f"Query executed: {query}",
        "results": [],
        "hint": "Try querying 'inventory' or 'revenue' for mock data."
    }
