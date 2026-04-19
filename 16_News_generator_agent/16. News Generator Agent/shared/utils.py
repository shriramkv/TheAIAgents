import os

def read_prompt(filename: str) -> str:
    """
    Reads a prompt template from the prompts directory.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    
    with open(prompt_path, "r") as f:
        return f.read().strip()

def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncates text to a specified length for easier reading in logs.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
