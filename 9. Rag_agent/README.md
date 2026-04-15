# 📚 Agentic RAG (Retrieval-Augmented Generation)

## Overview
Retrieval-Augmented Generation (RAG) is a technique that enhances large language models (LLMs) by providing them with external knowledge retrieved from a specialized database (usually a Vector DB). This project implements an Agentic RAG system capable of ingesting documents, vectorizing them, retrieving them based on semantic similarity to a user query, and generating precise, knowledge-grounded answers.

## Architecture
The system consists of two primary pipelines:
1. **Ingestion Pipeline**: 
   `Document → Chunk (Token-aware) → Embed (OpenAI) → Store (FAISS)`
2. **Retrieval & Query Pipeline**: 
   `Query → Embed → Retrieve Top-K Chunks → Build Prompt → Call LLM (OpenAI) → Return Answer`

## Example Example
**Query**: "What is water quality monitoring?"

**Agent Execution**:
1. *Retrieves* relevant chunks from the loaded documents.
2. *Constructs* a prompt limiting the LLM to only use the retrieved context.
3. *Answers* the user's query and displays the raw retrieved context and reasoning logs alongside it.

## Learning Objectives
By exploring this project, you will understand:
- **Retrieval Systems**: How to pull relevant data based on semantic meaning rather than exact keywords.
- **Vector Databases**: How tools like FAISS store numerical representations of text for rapid querying.
- **Grounded AI**: How to tie an AI's text generation rigidly to a verified source, drastically reducing hallucinations.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: Copy `.env.example` to `.env` and set your `OPENAI_API_KEY`.
3. Launch UI: Execute `python app.py` and open the local URL in your browser.
