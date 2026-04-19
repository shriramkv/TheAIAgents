import yaml
import os
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load project configuration from a YAML file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_env_var(var_name: str, default: str = None) -> str:
    """
    Get an environment variable or return a default value.
    """
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is required but not set.")
    return value
