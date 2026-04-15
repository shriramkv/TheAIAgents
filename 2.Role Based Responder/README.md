# 🎭 Role-Based Responder

## Overview
The Role-Based Responder is an agentic AI system designed to demonstrate how system prompts and varying personas influence the outputs of a Large Language Model (LLM). Built using the OpenAI SDK and Gradio, it introduces clear separation of concerns by dynamically loading different agent roles via YAML definitions.

## Architecture
**User Flow:** User Input & Role Selector → Agent Operator → LLM Injection → Parsed Output

1. **Role Selector:** Retrieves configuration from the `roles/` directory.
2. **Agent (`agent.py`):** Acts as the orchestrator, adopting the selected persona.
3. **LLM (`shared/llm.py`):** Handles model connection safely using the OpenAI SDK.
4. **Output (`app.py`):** Displays both the finalized reasoning logs and the LLM's response side-by-side using Gradio UI.

## Example Use Cases
### Query: "Explain blockchain"
- **Teacher:** Provides a simple explanation with analogies suitable for standard learning.
- **Lawyer:** Framed with legal, risk, and compliance implications.
- **Startup Founder:** Explains the business use case, scalability factors, and potential monetization loops.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure settings:
   Copy `.env.example` to `.env` and fill in your OpenAI API Key.
3. Run the interface:
   ```bash
   python app.py
   ```
