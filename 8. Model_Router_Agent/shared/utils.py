import yaml
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads YAML configuration from a given path.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

def load_prompt(prompt_path: str) -> str:
    """
    Loads a prompt text from the corresponding path.
    """
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
