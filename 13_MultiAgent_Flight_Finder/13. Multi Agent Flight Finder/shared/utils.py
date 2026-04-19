import yaml
from pathlib import Path
from typing import Any, Dict

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_prompt(prompt_name: str) -> str:
    """
    Loads a prompt from the prompts directory.
    """
    prompt_path = Path("prompts") / f"{prompt_name}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found at {prompt_path}")
    
    with open(prompt_path, "r") as f:
        return f.read().strip()
