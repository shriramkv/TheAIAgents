import json
import os
from typing import List, Dict, Any
from shared.logger import logger
from shared.utils import load_config

def fetch_news(ticker: str, limit: int = 5) -> List[Dict[str, str]]:
    """
    Fetches recent news for a given ticker.
    Currently uses mock data but designed for easy API integration.
    """
    try:
        logger.info(f"Retrieving news for {ticker}...")
        
        # In a real scenario, you'd call NewsAPI or similar here
        # For this agent, we use a mock data generator to ensure stability
        
        mock_news = [
            {
                "title": f"{ticker} reports strong quarterly earnings",
                "summary": f"{ticker} has exceeded analyst expectations in the most recent quarter, showing 15% YoY growth.",
                "url": f"https://finance.example.com/news/{ticker}-earnings"
            },
            {
                "title": f"New product launch from {ticker}",
                "summary": f"The latest innovation from {ticker} is expected to disrupt the market and drive future revenue.",
                "url": f"https://news.example.com/{ticker}-product"
            },
            {
                "title": f"Market volatility affects {ticker} stock",
                "summary": f"Broader market trends are impacting {ticker}'s share price despite strong fundamentals.",
                "url": f"https://analysis.example.com/{ticker}-volatility"
            },
            {
                "title": f"Strategic partnership for {ticker}",
                "summary": f"{ticker} announces a new collaboration with a major industry player to expand its reach.",
                "url": f"https://business.example.com/{ticker}-partnership"
            },
            {
                "title": f"Analyst upgrade for {ticker}",
                "summary": "Major investment banks have upgraded their rating for the company citing strong cash flow.",
                "url": f"https://invest.example.com/{ticker}-upgrade"
            }
        ]
        
        return mock_news[:limit]
        
    except Exception as e:
        logger.error(f"Error fetching news for {ticker}: {e}")
        return []

if __name__ == "__main__":
    # Test execution
    print(fetch_news("AAPL"))
