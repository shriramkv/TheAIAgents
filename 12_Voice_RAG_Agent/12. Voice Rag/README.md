# 🎤 Voice RAG Agent

A modular, production-quality AI agent that supports voice interactions (STT and TTS) integrated with a Retrieval-Augmented Generation (RAG) pipeline.

## 🌟 Overview
The Voice RAG Agent allows users to interact with a knowledge base using their voice. It bridge the gap between spoken language and structured knowledge retrieval, providing grounded and audible responses.

## 🏗️ Architecture
The system follows a clean, modular flow:
1. **Audio Input**: User speaks via microphone or uploads an audio file (WAV/MP3).
2. **STT (Speech-to-Text)**: OpenAI Whisper transcribes the audio into text.
3. **Retrieval**: The transcript is used to query a FAISS vector database for relevant context.
4. **LLM (GPT-4o-mini)**: A grounded answer is generated using ONLY the retrieved context.
5. **TTS (Text-to-Speech)**: The answer is converted back to speech using gTTS.
6. **Output**: The user receives the transcript, retrieved context, text answer, and audio response.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Add your OpenAI API Key to .env
   ```

### Running the App
```bash
python app.py
```

## 📂 Project Structure
- `audio/`: STT and TTS modules.
- `ingestion/`: Document loading, chunking, and indexing logic.
- `retrieval/`: Context retrieval logic.
- `shared/`: LLM, embeddings, vector store, and logging utilities.
- `data/`: Sample documents for RAG.
- `agent.py`: Core orchestrator.
- `app.py`: Gradio web interface.

## 🎓 Learning Objectives
- Implementing speech processing (Whisper & gTTS).
- Building modular multimodal agentic loops.
- Integrating RAG with voice interfaces.

## 🧾 Logging
The agent provides a transparent reasoning trace:
- `[AUDIO INPUT RECEIVED]`
- `[TRANSCRIPT] ...`
- `[RETRIEVED CONTEXT] ...`
- `[ANSWER GENERATED]`
- `[AUDIO RESPONSE CREATED]`
