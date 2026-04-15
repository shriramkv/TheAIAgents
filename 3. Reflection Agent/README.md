# Reflection Agent

A clean, modular, production-quality Python project demonstrating the **Reflection Pattern** in Agentic AI using the OpenAI SDK and Gradio for UI. 

## Overview
The Reflection Pattern allows an AI agent to self-correct its own work. Instead of simply generating a final answer, the agent generates an initial response, passes it to a "reviewer" persona which critiques the output, and finally leverages that critique to generate a higher-quality improved response.

## Architecture

The system executes the following steps sequentially:
1. **User Input** → *Generate (initial)*
2. **Initial Response** → *Critique*
3. **Initial Response + Critique** → *Improve*
4. **Final Output** (displayed via Gradio UI)

## Example

- **User Input:** "Write a blog on AI"
- **Initial Response:** Generates a generic, high-level overview.
- **Critique:** Highlights that the text lacks depth, specific use-cases, and an engaging tone.
- **Improved Response:** Produces a detailed, well-structured blog post with concrete examples and improved writing style.

## Learning Objectives

- **Self-Improving Agents:** See how prompting a model to reflect improves final outcomes.
- **Multi-step Reasoning:** Understand how breaking a task into steps (generate, critique, improve) provides greater control.
- **Prompt Chaining:** Learn how outputs from one LLM call can be utilized as context/inputs in subsequent calls.

## Getting Started

### 1. Installation
Ensure you have Python 3.8+ installed. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Copy `.env.example` to `.env` and add your valid OpenAI API key.
```bash
cp .env.example .env
```
Ensure you provide a key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application
Launch the Gradio interface:
```bash
python app.py
```
Open the provided local URL in your browser to interact with the Reflection Agent.
