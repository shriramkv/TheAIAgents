import os
import yaml

def load_prompt(file_path: str) -> str:
    """
    Load prompt text from a text file.
    
    Args:
        file_path (str): The relative or absolute path to the prompt file.
        
    Returns:
        str: The content of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def load_config(file_path: str = "config.yaml") -> dict:
    """
    Load configuration from a YAML file.
    
    Args:
        file_path (str): The path to the config file.
        
    Returns:
        dict: The parsed configuration.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
