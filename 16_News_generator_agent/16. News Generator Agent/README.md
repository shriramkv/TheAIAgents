# 📰 News Generator Agent

An intelligent agentic system that aggregates, deduplicates, clusters, and summarizes news into a tailored newsletter using OpenAI's GPT-4o-mini and Gradio.

## 🚀 Overview

The News Generator Agent automates the process of creating daily newsletters. It fetches news from multiple sources (mock data provided), removes redundant/similar stories using TF-IDF similarity, groups articles by topic, and uses an LLM to generate concise summaries. Finally, it synthesizes all content into a formatted newsletter with customizable tone and length.

## 🏗️ Architecture

The system follows a modular pipeline:
1.  **Fetch**: Retrieve articles from sources (Mock JSON implementation).
2.  **Deduplicate**: Filter out near-duplicate content using TF-IDF vectorization and cosine similarity.
3.  **Cluster**: Group articles into relevant topics.
4.  **Summarize**: Map each article to a bulleted summary using GPT-4o-mini.
5.  **Generate**: Reduce all summaries into a cohesive, styled newsletter.

## 🛠️ Installation

1.  Clone the repository and navigate to the project folder.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up your `.env` file with your OpenAI API Key:
    ```bash
    cp .env.example .env
    # Add your key to .env
    ```

## 🖥️ Usage

Run the Gradio application:
```bash
python app.py
```

### Example Input
- **Category**: Tech
- **Tone**: Gen Z
- **Length**: Short

### Example Output
A short, punchy newsletter with Gen Z slang covering the latest tech headlines.

## 🎯 Learning Objectives
- Building multi-stage content aggregation pipelines.
- Implementing text transformation and deduplication logic.
- Achieving controlled text generation through structured prompts.

## ⚙️ Configuration
Modify `config.yaml` to change the model, temperature, or similarity thresholds.
