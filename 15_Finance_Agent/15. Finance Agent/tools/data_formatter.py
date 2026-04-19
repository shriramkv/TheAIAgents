from typing import Dict, Any, Union
from shared.logger import logger

def format_currency(value: Union[int, float, None]) -> str:
    """
    Formats large numbers into readable currency (e.g., $1.2B).
    """
    if value is None:
        return "N/A"
    
    if abs(value) >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    elif abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    else:
        return f"${value:,.2f}"

def clean_financial_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes and cleans financial metrics.
    Why: Ensures the LLM receives structured, readable text rather than raw large integers.
    """
    try:
        cleaned = {
            "price": f"${data['price']:.2f}" if data.get('price') else "N/A",
            "market_cap": format_currency(data.get('market_cap')),
            "pe_ratio": f"{data['pe_ratio']:.2f}" if data.get('pe_ratio') else "N/A",
            "revenue": format_currency(data.get('revenue')),
            "net_income": format_currency(data.get('net_income')),
            "debt": format_currency(data.get('debt')),
            "equity": format_currency(data.get('equity'))
        }
        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")
        return {k: "N/A" for k in data.keys()}

if __name__ == "__main__":
    # Test execution
    test_data = {
        "price": 150.0,
        "market_cap": 2500000000000,
        "pe_ratio": 25.5,
        "revenue": 100000000000,
        "net_income": 20000000000,
        "debt": 10000000000,
        "equity": 50000000000
    }
    print(clean_financial_data(test_data))
