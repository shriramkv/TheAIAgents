# Human-in-the-Loop (HITL) Agent

## Overview
This project implements a modular, production-quality **Human-in-the-Loop (HITL) Agent**. The system is designed to execute tasks autonomously but identifies **high-risk actions** (like sending emails or deleting data) and pauses execution until a human provides approval via Slack, Email, or the built-in Dashboard.

## Architecture
The system follows a strict state-controlled workflow:
**User Input** → **LLM (Action Generation)** → **Risk Evaluator** → **Approval Notifier** (if risky) → **Wait for Human** → **Execution/Abort**

- **Risk Evaluator**: Scans planned actions for sensitive keywords and destructive patterns.
- **Approval System**: Integrates with Slack and SMTP to notify a human of pending actions.
- **Gradio UI**: Provides a visual interface to monitor the agent's reasoning and approve/reject actions in real-time.

## Project Structure
```
human_in_the_loop_agent/
│
├── agent.py               # Core HITL Agent logic
├── app.py                 # Gradio UI Dashboard
├── config.yaml            # Configuration (model, risk keywords)
├── .env.example           # Environment variables template
│
├── approval/
│   ├── slack_notifier.py  # Slack API integration
│   ├── email_notifier.py  # SMTP integration
│   └── approval_handler.py # Logic for waiting on human input
│
├── risk/
│   └── risk_evaluator.py  # Risk detection logic
│
├── prompts/
│   └── agent.txt          # System prompts for the agent
│
└── shared/
    ├── llm.py             # LLM service wrapper
    ├── base_agent.py      # Abstract agent class
    ├── logger.py          # Structured logging
    └── utils.py           # Configuration helpers
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env` and fill in your API keys:
   - `OPENAI_API_KEY`
   - `SLACK_BOT_TOKEN` & `SLACK_CHANNEL_ID` (Optional)
   - `SMTP_SERVER` & `SMTP_PASSWORD` (Optional)

3. **Run the Dashboard**:
   ```bash
   python app.py
   ```

## Example Workflow
1. **Input**: "Delete the 'production_db' folder."
2. **Agent**: Generates action `ACTION: Delete the folder 'production_db'`.
3. **Risk Detection**: Evaluator detects 'delete' keyword → **RISK: YES**.
4. **Approval**: Agent sends request to Slack and waits.
5. **Decision**: Human clicks "Reject" in the UI.
6. **Result**: Agent aborts the action safely.

## Learning Objectives
- Implementing safe AI deployment patterns.
- Designing modular human-in-the-loop systems.
- Managing risk in automated agentic workflows.
助力助
