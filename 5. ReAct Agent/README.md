# 🔍 ReAct Loop Tracer

A production-quality Python project demonstrating an Agentic AI system built using the **ReAct pattern (Reason + Act)**.

The system utilizes `gpt-4o-mini` from the OpenAI SDK and displays the agent's internal monologue and tool observations via a Gradio web interface.

## 🌟 Overview

The **ReAct** (Reasoning and Acting) pattern is a framework for language models that allows them to interact with external tools and augment their context dynamically. It enforces strict structural outputs so that models articulate their logic (`Thought`), select a tool (`Action`), provide arguments to that tool (`Action Input`), and digest the results (`Observation`) before determining a `Final Answer`.

## 🏗 Architecture

The ReAct loop operates via the following life cycle:

1. **User Query**: User provides an initial problem.
2. **Thought**: The Agent figures out what it needs to do.
3. **Action**: The Agent chooses from an array of available tools.
4. **Action Input**: The Agent formats parameters for the tool.
5. **Tool Execution**: The system parses the Action and Input, runs the designated Python tool, and yields an `Observation`.
6. **Observation**: The Agent reads the tool output and adds it to its context.
7. **Repeat**: Steps 2-6 repeat until the objective goal is reached.
8. **Final Answer**: Output is served gracefully to the user.

## 📝 Example

**User Input:** "What is (25 * 4) + 10?"

**ReAct Trace:**
```text
Thought: I need to solve a mathematical equation. I'll use the calculator.
Action: calculator
Action Input: (25 * 4) + 10
Observation: 110
Thought: I have the mathematical result.
Final Answer: 110
```

## 🎯 Learning Objectives

- **Interpretable Reasoning**: Reveal black-box LLM thought processes for auditing.
- **Debugging Agents**: Easily isolate hallucinations vs tool execution failures.
- **Multi-Step Problem Solving**: Allowing AI to iteratively work rather than 'one-shotting' answers.

## ⚙️ Setup & Usage

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Duplicate `.env.example` to `.env` and provide your API Key:
   ```bash
   OPENAI_API_KEY=sk-xxxx
   ```

3. Run the Gradio App:
   ```bash
   python app.py
   ```

4. View the user interface by visiting `http://localhost:7860` or `http://127.0.0.1:7860` in your web browser.
