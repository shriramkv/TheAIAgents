from typing import List, Dict
from shared.logger import logger
from shared.utils import load_config

def detect_spike(sentiments: List[str]) -> Dict:
    """
    Detects unusual increase in negative sentiment.
    Returns:
    {
        "spike_detected": bool,
        "explanation": str
    }
    """
    if not sentiments:
        return {"spike_detected": False, "explanation": "No data to analyze."}
    
    config = load_config()
    threshold = config.get("anomaly_threshold", 0.5)
    min_posts = config.get("min_posts_for_analysis", 5)
    
    total = len(sentiments)
    negative_count = sentiments.count("Negative")
    
    if total < min_posts:
        return {
            "spike_detected": False, 
            "explanation": f"Insufficient data for anomaly detection (Need {min_posts}, got {total})."
        }
    
    negative_ratio = negative_count / total
    
    if negative_ratio > threshold:
        return {
            "spike_detected": True,
            "explanation": f"Spike detected! {negative_ratio:.1%} of analyzed posts are negative, exceeding the threshold of {threshold:.1%}."
        }
    else:
        return {
            "spike_detected": False,
            "explanation": f"Sentiment levels are within normal range ({negative_ratio:.1%} negative)."
        }
core_detector = detect_spike # Alias for internal use
