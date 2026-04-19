import json
import os
from shared.logger import logger

def fetch_news(category: str, limit: int = 10) -> list:
    """
    Fetches news articles from a mock source or API.
    Returns:
    [
        {
            "title": "...",
            "content": "...",
            "source": "...",
            "url": "..."
        }
    ]
    """
    logger.info(f"Fetching news for category: {category}")
    
    # Path to mock data
    mock_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "mock_news.json")
    
    if os.path.exists(mock_data_path):
        with open(mock_data_path, "r") as f:
            all_news = json.load(f)
            # Filter by category if category is not 'all'
            if category.lower() != "all":
                filtered_news = [n for n in all_news if n.get("category", "").lower() == category.lower()]
            else:
                filtered_news = all_news
                
            return filtered_news[:limit]
    else:
        logger.warning("Mock news data not found. Returning empty list.")
        return []
