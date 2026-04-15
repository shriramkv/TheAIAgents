# Model Router Agent 🔀

An intelligent, dynamically routed agent that balances cost and reliability by directing user queries to specific LLM configurations depending on complexity.

## 🎯 Overview

The Model Router Agent automatically evaluates user inputs and routes them to different inference configurations to optimize token usage, response times, and general costs without sacrificing quality. It categorizes inputs into three configurable tiers: 
- **SIMPLE**: Factual, low-reasoning questions. Output generates rapidly and uses low token constraints and tight temperatures.
- **MEDIUM**: Multi-step queries requiring nuanced but straightforward answers. Standard constraints are applied.
- **COMPLEX**: Requests requiring deep analysis or extensive detail. Expanded constraints (higher max tokens, higher temperature) are automatically utilized.

Additionally, this agent acts defensively by deploying a **fallback tracking system**. If the preferred primary model or configuration fails via timeouts or API issues, it degrades gracefully to a reliable fallback pattern—maximizing operational uptime.

## 🏗️ Architecture

```text
User Input 
   │
   ▼
[ Router Classifier ] ──▶ SIMPLE / MEDIUM / COMPLEX
   │
   ▼
[ Model Selector ] ──▶ Loads parameters (temp/tokens) from config.yaml
   │                   for primary_model (e.g. gpt-4o-mini)
   ▼
[ LLM Caller ] ──▶ (Runs primary execution)
   │
   ├──▶ (Success) ──▶ Output to User
   │
   └──▶ (Failure) ──▶ [ Fallback Module ] ──▶ Executes secondary model parameters
                                 │
                                 ▼
                         Output to User (with fallback recorded in logs)
```

## 🛠️ Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Rename `.env.example` to `.env` and assign your OpenAI API Key.
   ```
   OPENAI_API_KEY=your_key_here
   ```

3. **Run the Interface**
   ```bash
   python app.py
   ```

## 🧠 Example Routing Interactions

**Input:** `"What is 2+2?"`
* **Route:** `SIMPLE`
* **Execution:** High efficiency constraints (Temperature: 0.2, Max Tokens: 200). Generates the factual answer fast with strict boundaries.

**Input:** `"Explain the intricacies of quantum entanglement and its implications on cryptography."`
* **Route:** `COMPLEX`
* **Execution:** Deep-insight constraints (Temperature: 0.5, Max Tokens: 800). Permits the LLM more creative fluidity and token generation length to cover the topic appropriately.

**Failure Scenario:** (Primary model hangs / network disruption)
* **Response:** Primary generation aborts after configurable limits timeout/retries. Invokes specified `fallback_model` configuration to guarantee a finalized output string.

## 📓 Learning Objectives
This project demonstrates several advanced AI system design concepts:
- **Cost Optimization:** Using cheap routing models to determine boundaries for costlier generation passes.
- **Reliability Design:** Wrapping primary functions in deliberate retry decorators and failure handlers.
- **Dynamic Routing:** Programmatically adjusting temperature and context thresholds rather than relying strictly on single fixed states.
