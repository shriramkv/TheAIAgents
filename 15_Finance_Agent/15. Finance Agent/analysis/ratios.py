from typing import Dict, Any, Optional
from shared.logger import logger

def calculate_pe_ratio(price: Optional[float], earnings: Optional[float]) -> Optional[float]:
    """Calculates Price-to-Earnings Ratio."""
    if price and earnings and earnings != 0:
        return price / (earnings / 1) # Simplified for current stock price
    # Note: Stock price / (Net Income / Shares Outstanding) = P/E
    # Here we assume the input raw data might already have P/E, or we use price / earnings per unit if available.
    return None

def calculate_debt_to_equity(debt: Optional[float], equity: Optional[float]) -> Optional[float]:
    """Calculates Debt-to-Equity Ratio."""
    if debt is not None and equity is not None and equity != 0:
        return debt / equity
    return None

def calculate_profit_margin(net_income: Optional[float], revenue: Optional[float]) -> Optional[float]:
    """Calculates Net Profit Margin percentage."""
    if net_income is not None and revenue is not None and revenue != 0:
        return (net_income / revenue) * 100
    return None

def get_all_ratios(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes all key financial ratios.
    Returns: Dict with P/E, D/E, and Profit Margin.
    """
    logger.info("Calculating financial ratios...")
    
    # We use the raw data (floats) for calculation
    # P/E is usually provided directly by yfinance, but we can verify it if we had EPS
    pe = data.get("pe_ratio") 
    de = calculate_debt_to_equity(data.get("debt"), data.get("equity"))
    margin = calculate_profit_margin(data.get("net_income"), data.get("revenue"))
    
    return {
        "pe_ratio": round(pe, 2) if pe else "N/A",
        "debt_to_equity": round(de, 2) if de else "N/A",
        "profit_margin": f"{round(margin, 2)}%" if margin else "N/A"
    }
