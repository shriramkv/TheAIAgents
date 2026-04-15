def calculator(expression: str) -> str:
    """
    Safely evaluate math expressions
    
    Args:
        expression: A string representing a mathematical expression (e.g. "25 * 18")
        
    Returns:
        The result of the calculation as a string, or an error message.
    """
    try:
        # Note: eval is used here for demonstration purposes.
        # In a real production system, use a safe parser or ast.literal_eval.
        # We limit the globals and locals to basic math symbols if needed, but here it's empty.
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
