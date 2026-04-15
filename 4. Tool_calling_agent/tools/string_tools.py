def reverse_string(text: str) -> str:
    """
    Reverse a string
    
    Args:
        text: The string to be reversed.
        
    Returns:
        The reversed string, or an error message if invalid.
    """
    try:
        return text[::-1]
    except Exception as e:
        return f"Error reversing string: {str(e)}"
