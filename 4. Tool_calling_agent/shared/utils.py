import yaml
import os
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration settings from the specified YAML file.
    Provides fallback defaults if file doesn't exist.
    """
    if not os.path.exists(config_path):
        return {
            "model": "gpt-4o-mini",
            "temperature": 0.2,
            "max_tokens": 500
        }
        
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
