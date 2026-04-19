from typing import Dict, List, Any
from shared.logger import logger

def analyze_fundamentals(data: Dict[str, Any], ratios: Dict[str, Any]) -> List[str]:
    """
    Performs fundamental analysis by checking key metrics against thresholds.
    Why: Provides a baseline reasoning layer before the LLM generates the final memo.
    """
    insights = []
    
    # Check Profitability
    margin_str = ratios.get("profit_margin", "0%")
    try:
        margin = float(margin_str.strip('%'))
        if margin > 20:
            insights.append("Strong profitability with margins over 20%.")
        elif margin < 5:
            insights.append("Low profitability margins; potentially a high-volume, low-margin business.")
    except (ValueError, TypeError):
        pass

    # Check Debt Risk
    de = ratios.get("debt_to_equity")
    if isinstance(de, (int, float)):
        if de > 2:
            insights.append("High debt-to-equity ratio indicating potential financial risk.")
        elif de < 0.5:
            insights.append("Conservative debt levels; strong balance sheet.")

    # Check Valuation
    pe = ratios.get("pe_ratio")
    if isinstance(pe, (int, float)):
        if pe > 40:
            insights.append("High P/E ratio suggests the stock might be overvalued or high growth is expected.")
        elif pe < 15:
            insights.append("Low P/E ratio indicates potential undervaluation or market skepticism.")

    if not insights:
        insights.append("Fundamentals appear stable; no extreme outliers detected.")

    logger.info(f"Generated {len(insights)} fundamental insights.")
    return insights
