# Tool-Calling Agent 🛠

## Overview
This project demonstrates a production-quality, modular Python architecture for an Agentic AI system relying on **Tool-Augmented Reasoning**. By leveraging function calling, the agent acts semi-autonomously: accepting natural language, planning out what specialized tools to run, executing them, evaluating the returned values, and providing a final conclusive answer.

## Architecture
**User → ToolCallingAgent (LLM) → Tool Execution → LLM loop → Output**

- `agent.py`: Houses the continuous thought-action loop and passes history to the LLM until no further tools are requested.
- `tools/`: A suite containing actual tool python functions as well as a centralized `tool_registry.py` for exporting JSON schemas understandable by OpenAI models.
- `shared/`: Generic logic utilities, standardized logging functions (providing the "reasoning trace"), and an LLM abstraction layer.
- `app.py`: The user entry point providing an easy-to-use Gradio interface.

## Example Interaction
**Input**: `"What is 25 * 18 and reverse the word hello?"`

**System Trace**:
1. `[THOUGHT]` Agent analyzes query.
2. `[ACTION]` Agent selects `calculator` with `25 * 18`.
3. `[OBSERVATION]` Executed tool returns `450`.
4. `[ACTION]` Agent selects `reverse_string` with `text='hello'`.
5. `[OBSERVATION]` Executed tool returns `olleh`.
6. `[FINAL]` Agent synthesizes observations and returns: "The result of 25 * 18 is 450, and reversing 'hello' gives 'olleh'."

## Setup
1. Define `.env` locally using `.env.example` template: `OPENAI_API_KEY=your_key`
2. Install dependencies: `pip install -r requirements.txt`
3. Optionally adjust parameters in `config.yaml`
4. Run locally: `python app.py`

## Learning Objectives
- Understanding standard OpenAI Function Calling formats.
- Implementing an endless iterative tool loop.
- Keeping core agent logic independent of specific physical tools.
- Rendering a completely transparent execution trace for debugging/users.
