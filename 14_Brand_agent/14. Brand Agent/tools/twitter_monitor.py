import json
import os
from datetime import datetime
from shared.logger import logger

def fetch_twitter_posts(keyword: str, limit: int = 20) -> list:
    """
    Simulates fetching Twitter posts for a given keyword.
    In a real scenario, this would use the Tweepy or Twitter API v2.
    """
    logger.info(f"Fetching Twitter posts for: {keyword}")
    
    # Path to mock data
    mock_data_path = os.path.join("data", "mock_posts.json")
    
    if not os.path.exists(mock_data_path):
        logger.warning("Mock data file not found.")
        return []
        
    with open(mock_data_path, "r") as f:
        posts = json.load(f)
        
    # Filter by keyword (case-insensitive) and platform
    filtered_posts = [
        post for post in posts 
        if keyword.lower() in post["text"].lower() and post["platform"] == "twitter"
    ]
    
    # Sort by timestamp (desc)
    filtered_posts.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return filtered_posts[:limit]
