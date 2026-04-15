import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# ChromaDB Settings
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", str(BASE_DIR / "data" / "chroma_db"))
COLLECTION_NAME = "agent_memory"
