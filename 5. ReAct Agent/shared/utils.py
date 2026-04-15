import yaml
import os
import re
from typing import Dict, Any, Optional, Tuple

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads YAML configuration.
    """
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def parse_react_output(text: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Parses LLM output into Thought, Action, Action Input, and Final Answer.
    Uses regex to extract blocks flexibly.
    
    Returns:
        tuple (thought, action, action_input, final_answer)
    """
    thought = None
    action = None
    action_input = None
    final_answer = None

    # Parse final answer if present
    final_answer_match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL | re.IGNORECASE)
    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()
        return None, None, None, final_answer

    # Parse ReAct components
    thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|Final Answer:|$)", text, re.DOTALL | re.IGNORECASE)
    if thought_match:
        thought = thought_match.group(1).strip()

    action_match = re.search(r"Action:\s*(.*?)(?=Action Input:|$)", text, re.DOTALL | re.IGNORECASE)
    if action_match:
        action = action_match.group(1).strip()

    input_match = re.search(r"Action Input:\s*(.*?)(?=Observation:|$)", text, re.DOTALL | re.IGNORECASE)
    if input_match:
        action_input = input_match.group(1).strip()

    return thought, action, action_input, final_answer
