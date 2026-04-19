from typing import Any, Dict

def mock_calculator(input_str: str) -> str:
    """
    A mock calculator that can handle simple multiplication and addition.
    """
    try:
        # Simple sandbox-like eval for demo purposes
        # In production, use a safe math parser
        result = eval(input_str, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"ERROR: Invalid input for calculator. {str(e)}"

def mock_search(query: str) -> str:
    """
    A mock search tool that returns canned responses.
    """
    canned_responses = {
        "capital of france": "Paris",
        "weather in london": "Rainy, 15°C",
        "who is the ceo of apple": "Tim Cook"
    }
    
    query_lower = query.lower()
    for key, val in canned_responses.items():
        if key in query_lower:
            return val
            
    return "Search result: Content not found in mock database."

def mock_weather(city: str) -> str:
    """
    A mock weather tool.
    """
    return f"The weather in {city} is sunny and 25°C."

# Registry of mock tools
MOCK_TOOLS = {
    "calculator": mock_calculator,
    "web_search": mock_search,
    "get_weather": mock_weather
}
