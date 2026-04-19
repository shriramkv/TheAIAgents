import yaml
import os

def load_config(config_path: str = "config.yaml"):
    """
    Load project configuration from YAML file
    """
    if not os.path.exists(config_path):
        # Fallback to absolute path from current project root
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def calculate_cost(input_tokens: int, output_tokens: int, model_pricing: dict) -> float:
    """
    Calculate cost based on input/output tokens and pricing (per 1M tokens)
    """
    input_cost = (input_tokens / 1_000_000) * model_pricing['input_cost_per_1m']
    output_cost = (output_tokens / 1_000_000) * model_pricing['output_cost_per_1m']
    return input_cost + output_cost
