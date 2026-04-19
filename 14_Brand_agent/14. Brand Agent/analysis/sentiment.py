import os
from shared.llm import call_llm
from shared.logger import logger

def classify_sentiment(text: str) -> str:
    """
    Classifies the sentiment of a text using an LLM.
    """
    prompt_path = os.path.join("prompts", "sentiment.txt")
    
    if not os.path.exists(prompt_path):
        logger.warning(f"Sentiment prompt file not found at {prompt_path}")
        return "Neutral"
        
    with open(prompt_path, "r") as f:
        template = f.read()
    
    prompt = template.format(text=text)
    
    try:
        sentiment = call_llm(prompt, system_prompt="You are a sentiment analysis specialist.")
        # Ensure only valid labels are returned
        valid_labels = ["Positive", "Neutral", "Negative"]
        if sentiment in valid_labels:
            return sentiment
        else:
            # Fallback for unexpected LLM output
            for label in valid_labels:
                if label.lower() in sentiment.lower():
                    return label
            return "Neutral"
    except Exception as e:
        logger.error(f"Sentiment classification failed: {e}")
        return "Neutral"
