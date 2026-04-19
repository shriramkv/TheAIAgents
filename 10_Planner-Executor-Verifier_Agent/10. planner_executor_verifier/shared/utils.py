import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

def load_environment():
    """Loads environment variables from .env file."""
    print("[SYSTEM] Loading environment variables...")
    load_dotenv()

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """Loads YAML configuration from the given path."""
    print(f"[SYSTEM] Loading configuration from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_prompt(path: str) -> str:
    """Reads a text file and returns its content as a string."""
    print(f"[SYSTEM] Loading prompt from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
