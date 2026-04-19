import yaml
import os
from datetime import datetime

def load_config(config_path: str = "config.yaml"):
    """
    Loads configuration from a YAML file.
    """
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_timestamp():
    """
    Returns current timestamp in ISO format.
    """
    return datetime.now().isoformat()

def ensure_directory(path: str):
    """
    Ensures that a directory exists.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
