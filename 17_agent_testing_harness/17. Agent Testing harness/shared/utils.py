import yaml
import json
import os
from typing import Any, Dict

def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Loads a YAML file and returns a dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def save_json(data: Dict[str, Any], file_path: str):
    """
    Saves a dictionary to a JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def ensure_dir(directory: str):
    """
    Ensures that a directory exists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
