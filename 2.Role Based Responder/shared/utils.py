import yaml
from typing import Dict, Any

def load_yaml(path: str) -> Dict[str, Any]:
    """
    Safely load a YAML file from the given path.
    
    Args:
        path (str): The file path to the YAML file.
    
    Returns:
        dict: The parsed YAML data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file contains invalid YAML.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at: {path}")
    except yaml.YAMLError as exc:
        raise ValueError(f"Error parsing YAML file {path}: {exc}")
