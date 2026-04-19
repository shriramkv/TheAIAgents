# 🌐 Web Research Summarizer Agent

A clean, modular, production-quality Python project for an Agentic AI system that performs automated web research, content extraction, and synthesis.

## 🚀 Overview

The **Web Research Summarizer Agent** is designed to take a high-level research query and transform it into a structured markdown report. It automates the tedious process of searching, reading multiple pages, and combining findings.

## 🏗️ Architecture

The agent follows a multi-step pipeline:
1.  **Query Expansion**: The LLM rewrites the user query into multiple search-engine friendly terms.
2.  **Web Search**: Uses the `duckduckgo-search` tool to find relevant URLs.
3.  **Scraping**: Fetches raw HTML from the top results.
4.  **Content Extraction**: Cleans HTML to extract main prose using `BeautifulSoup`.
5.  **Summarization**: Each source is summarized individually by the LLM.
6.  **Synthesis**: Multiple summaries are combined into a final structured report with Overview, Key Insights, Trends, and Conclusion.

## 📁 Project Structure

```text
web_research_summarizer/
│
├── agent.py               # Main WebResearchAgent class
├── app.py                 # Gradio UI application
├── config.yaml            # System configuration
├── README.md              # Documentation
├── .env.example           # Environment variables template
├── requirements.txt       # Dependencies
│
├── tools/                 # Tooling for the agent
│   ├── search_tool.py     # DuckDuckGo search integration
│   ├── scraper.py         # HTML fetching
│   └── content_extractor.py # HTML cleaning and text extraction
│
├── prompts/               # LLM prompt templates
│   ├── query_expansion.txt
│   ├── summarizer.txt
│   └── synthesizer.txt
│
└── shared/                # Shared utilities
    ├── llm.py             # OpenAI API wrapper
    ├── base_agent.py      # Abstract agent base class
    ├── logger.py          # Custom logging for trace visibility
    └── utils.py           # Helper functions
```

## 🛠️ Setup & Installation

1.  **Clone the project**
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment**:
    -   Rename `.env.example` to `.env`.
    -   Add your `OPENAI_API_KEY`.
5.  **Run the application**:
    ```bash
    python app.py
    ```

## 🎯 Learning Objectives

-   Building multi-step agentic pipelines.
-   Integrating external tools (search, scraping).
-   Handling information synthesis from multiple sources.
-   Designing clean, modular AI software architecture.

## 📝 Example

**Input**: "Future of Quantum Computing in 2025"

**Output**:
-   A structured Markdown report.
-   List of sources used.
-   A full reasoning trace showing the expansion, search, and synthesis steps.
