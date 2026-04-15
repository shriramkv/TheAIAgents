# Task Planner Agent

## Overview

The Task Planner Agent is an advanced planning-based AI system built to tackle complex goals by breaking them down into actionable steps. Rather than generating a single monolithic response, the agent decomposes the task, executes each piece iteratively equipped with contextual memory, and finally synthesizes the entire execution trace into a comprehensive structured output. 

This multi-step reasoning mimics human problem-solving and enables robust, traceable agent workflows.

## Architecture

The project architecture relies on the following sequential pipeline:
1. **User Goal formulation**
2. **Planner**: Breaks the goal into a sequentially ordered list of executable steps.
3. **Memory Retrieval**: For each step, it retrieves relevant past execution trace from a Vector DB (ChromaDB) to leverage earlier context.
4. **Executor**: Solves a specific sub-goal using the memory context. The result is then stored back into the Vector DB.
5. **Summarizer**: Combines all execution traces into a clean, synthesized answer.

**Data Flow Pipeline:**
`User → Planner → Executor → Memory → Summarizer → Output`

## Example Run

**Input:** `"Build a startup"`

**Plan:**
1. Market research (Identify target audience and competitors)
2. Define product (Write down MVP specifications)
3. Business model (Create monetization and structural strategy)

**Execution:**
* *Step 1 Output*: Target audience profile and 3 major competitors discovered...
* *Step 2 Output*: MVP consists of a web platform for...
* *Step 3 Output*: Subscription-based business model...

**Final Answer:**
* Structured plan combining the market research, product definition, and business model into a single unified business proposal.

## Features Let Down
- **Tenacity Retry & Fallback**: Intelligent error handling that automatically downgrades to a more restrictive or secondary configuration to handle failures gracefully.
- **ChromaDB Vector Store**: Semantic memory providing execution steps awareness of prior context.
- **Gradio Tracing UI**: Interactive interface demonstrating exactly what happened continuously providing detailed logs.

## Learning Objectives

- **Task Decomposition**: Breaking monolithic prompts into directed action items.
- **Multi-step Reasoning**: Utilizing sequential generation contexts.
- **Agent Pipelines**: Orchestrating Planner/Executor/Summarizer flows seamlessly.

## Getting Started

1. Set up a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the `.env.example` file and configure your API key:
   ```bash
   cp .env.example .env
   # Edit .env and insert your OPENAI_API_KEY
   ```
3. Run the Gradio App:
   ```bash
   python app.py
   ```
