import os
import yaml
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads the YAML configuration file.
    """
    if not os.path.exists(config_path):
        # Default config if file missing
        return {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "approval_timeout": 60,
            "high_risk_keywords": ["delete", "send email", "transaction"]
        }
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_env_var(name: str, default: Any = None) -> Any:
    """
    Returns an environment variable or default.
    """
    return os.getenv(name, default)
