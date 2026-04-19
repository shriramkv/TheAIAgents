# ✈️ Multi-Agent Flight Finder

A modular, production-quality Multi-Agent system that demonstrates collaborative AI for flight searching, validation, and recommendation.

## 🚀 Overview
The system uses three specialized agents to help users find the best flight options based on their constraints.

1.  **Researcher Agent**: Finds flight options using the `flight_search` tool.
2.  **Validator Agent**: Filters flights based on budget and layover constraints.
3.  **Coordinator Agent**: Selects the best flight and provides a reasoning for the recommendation.

## 🏗️ Architecture
`User` → `Researcher` → `Validator` → `Coordinator` → `Gradio UI`

## 🛠️ Tech Stack
-   **Model**: OpenAI `gpt-4o-mini`
-   **SDK**: OpenAI Python SDK
-   **UI**: Gradio
-   **Configuration**: YAML
-   **Environment**: Python Dotenv

## 📂 Project Structure
-   `agents/`: Individual agent implementations.
-   `tools/`: Helper modules for data retrieval (mock flight data).
-   `shared/`: Common utilities (logger, llm, base_agent).
-   `prompts/`: Externalized system prompts for agents.
-   `agent.py`: Orchestration logic.
-   `app.py`: Main entry point (Gradio UI).

## 🚦 Getting Started
1. Create a `.env` file from `.env.example` and add your `OPENAI_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## 🎯 Learning Objectives
-   Understanding **Agentic Workflows** (Search -> Filter -> Rank).
-   Implementing **Role Specialization** in AI Agents.
-   Building **Transparent Reasoning Traces** in AI systems.
-   Modular **Project Architecture** for production AI systems.

## 📝 Example
**Input:**
- Origin: BLR
- Destination: DEL
- Budget: ₹5000
- Max Layovers: 1

**Output:**
- List of all found flights.
- List of flights under ₹5000 with <= 1 layover.
- Best selected flight with explanation.
