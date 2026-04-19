from duckduckgo_search import DDGS
from typing import List, Dict

def search_web(query: str, num_results=5) -> List[Dict[str, str]]:
    """
    Performs a web search using DuckDuckGo.
    Returns:
    [
        {"title": "...", "url": "...", "snippet": "..."}
    ]
    """
    results = []
    try:
        with DDGS() as ddgs:
            ddgs_results = ddgs.text(query, max_results=num_results)
            for r in ddgs_results:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        print(f"Error during DuckDuckGo search: {e}")
        # Fallback to empty list or other search logic if needed
    
    return results
