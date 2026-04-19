# 🛡️ Multi-Agent Cost Governor

A production-quality Agentic AI system that manages real-time token usage and enforces budget constraints by dynamically routing tasks between high-end and lightweight models.

## 🌟 Features

- **Real-time Cost Tracking**: Accurate estimation of USD cost per LLM call using configurable pricing.
- **Adaptive Model Routing**: Automatically switches from Primary (`gpt-4o`) to Lightweight (`gpt-4o-mini`) models when budget thresholds are reached.
- **Budget Enforcer**: Stops execution immediately if the total cost exceeds the user-defined limit.
- **Decision Engine**: Multi-step reasoning loop that evaluates state at every turn.
- **Gradio Dashboard**: Interactive UI with cumulative cost charts and step-by-step decision logs.

## 📁 Project Structure

```text
multi_agent_cost_governor/
├── agent.py               # Core orchestrator (CostGovernorAgent)
├── app.py                 # Gradio UI & Visualization
├── config.yaml            # Model pricing & Budget thresholds
├── supervisor/            # Governance components
│   ├── cost_tracker.py    # Multi-turn token & cost state
│   ├── budget_manager.py  # Limit enforcement
│   ├── router.py          # Model selection logic
│   └── decision_engine.py # Loop control (continue/stop)
├── agents/                # Worker implementations
│   ├── primary_agent.py   # High-quality agent (GPT-4o)
│   └── lightweight_agent.py # Cheap/Fast agent (GPT-4o-mini)
└── shared/                # Common utilities
    ├── llm.py             # OpenAI wrapper with usage tracking
    ├── base_agent.py      # Abstract agent interface
    ├── logger.py          # Formatted system logs
    └── utils.py           # Config & calculation helpers
```

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install openai gradio plotly pandas pyyaml python-dotenv
   ```

2. **Setup Credentials**:
   Create a `.env` file and add your OpenAI API key:
   ```text
   OPENAI_API_KEY=your_sk_...
   ```

3. **Run the Dashboard**:
   ```bash
   python app.py
   ```

## ⚙️ How it Works

The system implements a **Governance Loop**:

1. **Input**: User submits a complex query.
2. **Router**: Checks remaining budget. If > 30% remains, selects `gpt-4o`.
3. **Execution**: Worker Agent performs a specific step of the task.
4. **Tracker**: Captured token usage and calculates cost based on `config.yaml`.
5. **Decision**: Engine checks if the total cost is still safe to continue or if it should stop.

---
Built with 🛡️ by [Antigravity]
