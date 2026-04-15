import yaml
import os

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Loads configuration from a YAML file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration parameters.
    """
    if not os.path.exists(config_path):
        return {}
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    return config or {}
