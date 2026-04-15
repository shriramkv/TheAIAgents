def search(query: str) -> str:
    """
    Mock search tool returning predefined results based on the query keywords.
    """
    query_lower = query.lower()
    
    # Pre-defined mock database
    db = {
        "capital of france": "The capital of France is Paris.",
        "ai agent": "An AI agent is a system that can perceive its environment and act to achieve goals.",
        "react pattern": "ReAct stands for Reason + Act, a framework for combining reasoning and acting in LLMs.",
        "highest mountain": "Mount Everest is the highest mountain on Earth.",
        "speed of light": "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
    }
    
    # fuzzy matching mock
    for key, val in db.items():
        if key in query_lower:
            return val
            
    return "No search results found for the given query."
