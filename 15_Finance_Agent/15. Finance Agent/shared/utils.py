import yaml
import os
from pathlib import Path
from typing import Any, Dict
from shared.logger import logger

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    """
    try:
        # Check if file exists
        if not os.path.exists(config_path):
            logger.warning(f"Config file not found at {config_path}. Using default empty config.")
            return {}

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            logger.info(f"Successfully loaded configuration from {config_path}")
            return config if config else {}
    except Exception as e:
        logger.error(f"Error loading config at {config_path}: {e}")
        return {}

def ensure_dir(path: str):
    """
    Ensures that a directory exists.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
