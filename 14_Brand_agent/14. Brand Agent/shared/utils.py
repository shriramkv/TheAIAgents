import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Loads configuration from a YAML file.
    """
    if not os.path.exists(config_path):
        return {}
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_env_var(name: str, default: str = None) -> str:
    """
    Safely retrieves an environment variable.
    """
    return os.getenv(name, default)
