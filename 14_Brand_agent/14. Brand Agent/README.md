# 📡 Brand Monitoring Agent

A production-quality Agentic AI system built with Python, OpenAI, and Gradio. This agent monitors social platforms for brand mentions, analyzes sentiment, detects anomalies, and generates structured reports.

## 🌟 Overview

The Brand Monitoring Agent is designed to help companies stay on top of their online presence. By automating the collection and analysis of social media data, it provides real-time insights into public perception and alerts teams to potential PR crises or spikes in negative sentiment.

## 🏗️ Architecture

1.  **User Input**: User provides a brand keyword via the Gradio UI.
2.  **Data Collection**: The agent fetches mentions from Twitter and Reddit (using mock data for development).
3.  **Data Cleaning**: Text is normalized by removing URLs, hashtags, and special characters.
4.  **Sentiment Analysis**: Each post is classified as Positive, Neutral, or Negative using `gpt-4o-mini`.
5.  **Anomaly Detection**: The system checks for unusual increases in negative sentiment.
6.  **Report Generation**: An LLM synthesizes the data into a professional, structured report.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd brand_monitoring_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`.
   - Add your `OPENAI_API_KEY` to the `.env` file.

### Running the App

```bash
python app.py
```

The Gradio UI will be available at `http://127.0.0.1:7860`.

## 📈 Example

**Input**: "Tesla"

**Output**:
- **Mentions**: Cleaned posts from Twitter/Reddit.
- **Sentiment**: Breakdown (e.g., 2 Positive, 1 Neutral, 2 Negative).
- **Anomaly**: "Sentiment levels are within normal range."
- **Report**: A structured summary with issues and recommendations.

## 🎯 Learning Objectives

- Building modular NLP pipelines.
- Integrating LLMs for sentiment classification and summarization.
- Designing interactive UIs for Agentic AI systems.
- Implementing robust logging and configuration management.

## 🛠️ Project Structure

```
brand_monitoring_agent/
├── agent.py            # Main agent orchestration
├── app.py              # Gradio UI
├── config.yaml         # Configuration settings
├── data/               # Mock data directory
├── tools/              # Data ingestion & cleaning
├── analysis/           # Sentiment & anomaly detection
├── prompts/            # LLM prompt templates
└── shared/             # LLM, logger, and utility modules
```

---
Built with ⚡ by Antigravity
