# 🤖 Hello Agent

A clean, modular, production-quality Python project for a basic Agentic AI system.

This agent can:
1. Accept user input via UI
2. Detect if a tool is needed (math/string ops)
3. Call the appropriate tool if required
4. Otherwise, fallback to a large language model (LLM)
5. Display the final answer and step-by-step reasoning logs

## Project Structure

```text
hello_agent/
│
├── agent.py              # Main Agent logic
├── app.py                # Gradio UI entrypoint
├── config.yaml           # Configuration parameters
├── README.md             # Project documentation
├── .env.example          # Example environment variables
│
├── tools/
│   ├── calculator.py     # Math evaluation tool
│   └── string_tools.py   # String manipulation tools (e.g. reverse)
│
└── shared/
    ├── llm.py            # LLM interface (OpenAI)
    ├── base_agent.py     # Base agent abstract class
    ├── logger.py         # Formatted logger for thoughts/actions
    └── utils.py          # Utility functions and detectors
```

## Setup Instructions

1. Clone or download the repository.
2. Navigate to the project directory:
   ```bash
   cd hello_agent
   ```
3. Create a python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up your environment variables by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
6. Add your OpenAI API key to the `.env` file!

## UI Demo

Run:

```bash
python app.py
```

Then open your browser to the local Gradio link provided in your terminal and interact with the agent!

## Examples to Try
- "25 * 18"
- "reverse hello"
- "What is AI?"
