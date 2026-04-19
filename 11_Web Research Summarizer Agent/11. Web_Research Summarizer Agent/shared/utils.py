import os
import yaml
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    """
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def read_prompt(file_path: str) -> str:
    """
    Reads a prompt from a text file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    with open(file_path, 'r') as f:
        return f.read().strip()

def clean_text(text: str) -> str:
    """
    Basic text cleaning to remove excessive whitespace.
    """
    return " ".join(text.split())
