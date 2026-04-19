from typing import List
from shared.utils import load_config
from shared.logger import logger

def is_high_risk(action: str) -> bool:
    """
    Identify risky actions such as:
    - sending emails
    - deleting data
    - financial transactions
    
    This implementation uses a combination of keyword matching and logic.
    In a more advanced version, this could call an LLM to evaluate risk.
    """
    config = load_config()
    high_risk_keywords: List[str] = config.get("high_risk_keywords", [])
    
    action_lower = action.lower()
    
    # Check for keywords
    for keyword in high_risk_keywords:
        if keyword in action_lower:
            logger.info(f"Risk Evaluation: Action '{action}' contains high-risk keyword '{keyword}'")
            return True
            
    # Additional logic for financial transactions or destructive patterns
    destructive_patterns = ["drop table", "format c:", "rm -rf"]
    for pattern in destructive_patterns:
        if pattern in action_lower:
            logger.info(f"Risk Evaluation: Action '{action}' contains destructive pattern '{pattern}'")
            return True
            
    return False
