import os
from typing import Dict, Any, List
from shared.base_agent import BaseAgent
from shared.llm import llm
from shared.logger import logger
from tools.stock_data import fetch_stock_data
from tools.news_fetcher import fetch_news
from tools.data_formatter import clean_financial_data
from analysis.ratios import get_all_ratios
from analysis.fundamentals import analyze_fundamentals

class FinancialAnalystAgent(BaseAgent):
    """
    Main Agent that coordinates data fetching, analysis, and report generation.
    """
    def __init__(self):
        super().__init__(name="FinancialAnalystAgent")
        self.memo_prompt_path = "prompts/memo_generator.txt"

    def _load_prompt_template(self) -> str:
        """Loads the memo generation prompt from file."""
        if os.path.exists(self.memo_prompt_path):
            with open(self.memo_prompt_path, "r") as f:
                return f.read()
        return "Generate an investment memo for {ticker}. Data: {fundamentals}, {ratios}, {news}"

    def run(self, ticker: str) -> Dict[str, Any]:
        """
        Executes the full financial analysis pipeline.
        1. Fetch Stock Data
        2. Fetch News
        3. Clean Data
        4. Calculate Ratios
        5. Analyze Fundamentals
        6. Generate Memo via LLM
        """
        logs = []
        
        def log_step(msg: str):
            logger.info(msg)
            logs.append(f"[{msg.split('...')[0].upper()}] {msg}")

        # 1. Fetch Data
        log_step(f"Fetching stock data for {ticker}...")
        raw_stock_data = fetch_stock_data(ticker)
        
        log_step(f"Fetching news for {ticker}...")
        news_data = fetch_news(ticker)

        # 2. Clean Data
        log_step("Normalizing financial metrics...")
        cleaned_data = clean_financial_data(raw_stock_data)

        # 3. Calculate Ratios
        log_step("Calculating key financial ratios...")
        ratios = get_all_ratios(raw_stock_data)

        # 4. Analyze Fundamentals
        log_step("Generating fundamental insights...")
        insights = analyze_fundamentals(raw_stock_data, ratios)

        # 5. Generate Memo
        log_step("Synthesizing data into investment memo...")
        prompt_template = self._load_prompt_template()
        
        # Format inputs for LLM
        prompt = prompt_template.format(
            ticker=ticker,
            fundamentals=cleaned_data,
            ratios=ratios,
            news=news_data
        )
        
        memo = llm.call_llm(prompt)
        log_step("Final memo generated successfully.")

        return {
            "ticker": ticker,
            "stock_data": cleaned_data,
            "ratios": ratios,
            "news": news_data,
            "insights": insights,
            "memo": memo,
            "logs": "\n".join(logs)
        }

if __name__ == "__main__":
    # Test Run
    agent = FinancialAnalystAgent()
    result = agent.run("AAPL")
    print(result["memo"])
    print("\nLOGS:\n", result["logs"])
