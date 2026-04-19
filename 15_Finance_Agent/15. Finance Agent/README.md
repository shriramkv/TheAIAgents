# 📊 Financial Analyst Agent

An intelligent Agentic AI system that performs deep financial analysis on stocks, retrieves recent news, calculates key ratios, and generates structured investment memos with citations.

## 🚀 Overview

The **Financial Analyst Agent** is designed to assist investors by automating the time-consuming process of data gathering and synthesis. It uses real-market data from Yahoo Finance and leverages GPT-4o-mini to provide human-like reasoning over complex financial metrics.

## 🏗️ Architecture

1.  **Input**: User provides a stock ticker (e.g., "AAPL").
2.  **Data Fetching**:
    *   `yfinance` retrieves real-time pricing and fundamentals.
    *   Mock system provides recent news headlines and summaries.
3.  **Analysis Pipeline**:
    *   **Ratios**: Calculations for P/E, Debt-to-Equity, and Profit Margins.
    *   **Fundamentals**: Heuristic checks for profitability and risk levels.
4.  **LLM Synthesis**: GPT-4o-mini processes the data into a structured Markdown memo.
5.  **UI**: A clean Gradio interface for interaction and log transparency.

## 📂 Project Structure

```text
financial_analyst_agent/
├── agent.py               # Main pipeline orchestrator
├── app.py                 # Gradio UI
├── config.yaml            # Model & app settings
├── README.md              # Documentation
├── .env.example           # Environment template
│
├── tools/                 # Data fetching tools
│   ├── stock_data.py
│   ├── news_fetcher.py
│   └── data_formatter.py
│
├── analysis/              # Numerical analysis
│   ├── ratios.py
│   └── fundamentals.py
│
├── prompts/               # LLM prompt templates
│   └── memo_generator.txt
│
└── shared/                # Core utilities
    ├── llm.py             # OpenAI wrapper
    ├── base_agent.py      # Abstract agent class
    ├── logger.py          # Unified logging
    └── utils.py           # Config loaders
```

## 🛠️ Setup

1.  **Clone the project**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure environment**:
    *   Copy `.env.example` to `.env`.
    *   Add your `OPENAI_API_KEY`.
4.  **Run the app**:
    ```bash
    python app.py
    ```

## 🎯 Learning Objectives

*   **Domain-Specific AI**: Applying LLMs to specialized financial tasks.
*   **Modular Architecture**: Building extensible tool-based agents.
*   **Structured Reporting**: Generating professional documentation with grounded citations.

## 📜 License

MIT
