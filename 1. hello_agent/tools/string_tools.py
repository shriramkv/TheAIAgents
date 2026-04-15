"""
Tools for string manipulation.
"""

def reverse_string(text: str) -> str:
    """
    Reverses the given string.
    
    Args:
        text (str): The input string to reverse.
        
    Returns:
        str: The reversed string.
    """
    # Remove 'reverse ' command if present at start
    prefix = "reverse "
    if text.lower().startswith(prefix):
        text = text[len(prefix):].strip()
        
    # Strip quotes if they exist around the target word
    text = text.strip("\"'")
    
    return text[::-1]
