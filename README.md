# 🤖 The AI Agents -  24 Hands-On Projects

> **Work through them in order. Each one builds intuition that the next one depends on.**

A structured, progressive collection of **24 fully working AI agent projects** -  from a basic ReAct loop to production-grade multi-agent systems with governance, audit trails, and human oversight.

Built from scratch. No fluff. Every project is self-contained, runnable, and teaches one thing well.

---

## 📖 About This Repository

This repository was built over weekends as part of a personal learning journey and as the hands-on companion to the book **"Agentic AI: Design, Build, Deploy"**.

Most people read about agents. Few actually build them. This repo is designed to close that gap -  project by project.

---

## 🗂️ Repository Structure

| Section | Projects | Focus |
|---------|----------|-------|
| [Section 1](#-section-1-core-agent-foundations) | 1–5 | Core Agent Foundations |
| [Section 2](#-section-2-memory-planning--routing) | 6–10 | Memory, Planning & Routing |
| [Section 3](#-section-3-real-world-domain-agents) | 11–16 | Real-World Domain Agents |
| [Section 4](#-section-4-production-grade-agent-systems) | 17–24 | Production-Grade Agent Systems |

---

## 🟦 Section 1: Core Agent Foundations | Projects 1–5

> Understanding the agent loop before adding complexity.

| # | Project | What You Learn |
|---|---------|----------------|
| 1 | **Hello Agent** | The ReAct loop -  reason, act, observe, respond |
| 2 | **Role-Based Responder** | How system prompt shapes agent persona and output |
| 3 | **Reflection Agent** | Generate → Critique → Improve for better outputs |
| 4 | **Tool-Calling Agent** | Connecting agents to real-world APIs and live data |
| 5 | **ReAct Loop Tracer** | Logging every step for transparency and debugging |

**Section Goal:** By the end of Project 5, you should be able to build, run, and debug a basic agent loop from scratch -  and understand exactly what happens at each reasoning step.

---

## 🟩 Section 2: Memory, Planning & Routing | Projects 6–10

> Making agents smarter and more reliable.

| # | Project | What You Learn |
|---|---------|----------------|
| 6 | **Memory-Augmented Q&A** | Short-term + vector DB memory for context continuity |
| 7 | **Task Decomposition Planner** | Breaking complex goals into sequential subtasks |
| 8 | **Fallback Model Router** | Multi-model routing for cost and latency management |
| 9 | **RAG Research Agent** | Retrieval-augmented generation to eliminate hallucination |
| 10 | **Planner–Executor–Verifier** | 3-agent pipeline for reliable complex reasoning |

**Section Goal:** Agents that remember, plan, and route intelligently -  the three capabilities that separate toy agents from useful ones.

---

## 🟧 Section 3: Real-World Domain Agents | Projects 11–16

> Agents solving actual business and research problems.

| # | Project | What You Learn |
|---|---------|----------------|
| 11 | **Web Research Summarizer** | Crawl → Extract → Summarize automated pipelines |
| 12 | **Voice RAG Agent** | Speech-to-text + retrieval + text-to-speech full loop |
| 13 | **Multi-Agent Flight Finder** | Researcher + validator agent collaboration |
| 14 | **Brand Monitoring Agent** | Social scraping + NLP sentiment classification |
| 15 | **Financial Analyst Agent** | Data + news + analytics for investment reporting |
| 16 | **News Generator Agent** | Multi-source ingestion, ranking, and rewriting |

**Section Goal:** See how agents apply to real domains -  research, finance, travel, and media -  and learn to adapt the patterns to your own use case.

---

## 🟥 Section 4: Production-Grade Agent Systems | Projects 17–24

> Deployment, safety, governance, and trust.

| # | Project | What You Learn |
|---|---------|----------------|
| 17 | **Agent Testing Harness** | Mock tools + test framework for agent evaluation |
| 18 | **Dockerized Agent API** | FastAPI + Docker for production deployment |
| 19 | **Human-in-the-Loop Agent** | Approval checkpoints for risky autonomous actions |
| 20 | **Multi-Agent Cost Governor** | Supervisor agent for token cost optimization |
| 21 | **Audit-Trail Agent Pipeline** | Structured JSON logging for full traceability |
| 22 | **MCP Tool Server** | MCP-compliant tool server for agent integration |
| 23 | **Code Review Agent** | Static analysis + LLM reasoning for code quality |
| 24 | **Interview Practice Agent** | Conversational agent with evaluation and feedback |

**Section Goal:** Build agents you can actually deploy, monitor, audit, and trust in production environments.

---

## 🚀 How to Use This Repo

**If you are a beginner** -  start at Project 1 and work forward. Do not skip the foundations.

**If you have agent experience** -  jump to the section most relevant to your current challenge. Each project is self-contained.

**For every project, follow this pattern:**

1. 📄 **Read the problem statement** -  understand *why* this agent exists
2. 🏗️ **Study the architecture** -  understand *how* it is structured
3. 🔁 **Trace the workflow** -  understand *what* happens step by step
4. ▶️ **Run it** -  see the sample input produce the sample output
5. 🔧 **Modify one thing** -  change a tool, a prompt, or a workflow step and observe the effect

---

## ⚙️ Prerequisites

```bash
Python 3.9+
OpenAI API key (or compatible LLM provider)
pip install -r requirements.txt
```

Set your API key:
```bash
export OPENAI_API_KEY=your_key_here
```

---

## 📬 Connect

Built by **Dr. Shriram Vasudevan, Dr. Sini Raj Pulari, Giridhararajan R and Dr. Vimal**
📘 Author -  *Agentic AI: Design, Build, Deploy*
🔗 [YouTube](https://www.youtube.com/shriramvasudevan) | [GitHub](https://github.com/shriramkv)

---

> *"Build five of these and you will stand out in any room you walk into. Not because you memorised the theory. Because you have done the work."*

⭐ If this helped you, give the repo a star -  it helps others find it too!
