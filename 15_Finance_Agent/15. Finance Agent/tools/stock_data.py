import yfinance as yf
from typing import Dict, Any
from shared.logger import logger

def fetch_stock_data(ticker: str) -> Dict[str, Any]:
    """
    Fetches real-time financial data for a given ticker using yfinance.
    Why: Provides the 'raw truth' from market data to ground the analysis.
    """
    try:
        logger.info(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract relevant metrics
        # Some keys might be missing depending on the ticker/API state
        data = {
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "revenue": info.get("totalRevenue"),
            "net_income": info.get("netIncomeToCommon"),
            "debt": info.get("totalDebt"),
            "equity": info.get("totalStockholderEquity")
        }
        
        # Fallback logic for basic fields if nested or renamed
        if data["net_income"] is None:
            data["net_income"] = info.get("netIncome")
            
        logger.info(f"Successfully fetched data for {ticker}")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {e}")
        # Return empty structure to avoid crashing
        return {
            "price": None, "market_cap": None, "pe_ratio": None, 
            "revenue": None, "net_income": None, "debt": None, "equity": None
        }

if __name__ == "__main__":
    # Test execution
    print(fetch_stock_data("AAPL"))
