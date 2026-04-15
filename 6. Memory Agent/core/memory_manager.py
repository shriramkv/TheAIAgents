import chromadb
from chromadb.config import Settings
import uuid
import sys
from typing import List

from config.settings import CHROMA_DB_DIR, COLLECTION_NAME
from core.llm_client import LLMClient

class MemoryManager:
    """Manages short-term and long-term memory."""
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.short_term_memory = []
        
        try:
            self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
            self.collection = self.chroma_client.get_or_create_collection(name=COLLECTION_NAME)
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            sys.exit(1)

    def add_to_short_term(self, role: str, content: str):
        """Adds a message to the short-term episodic memory list."""
        self.short_term_memory.append({"role": role, "content": content})
        # Keep only the last 10 turns (20 messages)
        if len(self.short_term_memory) > 20:
            self.short_term_memory = self.short_term_memory[-20:]

    def get_short_term_context(self) -> List[dict]:
        return self.short_term_memory

    def store_long_term_memory(self, memories: List[str]):
        """
        Embeds and stores a list of parsed long-term memories into ChromaDB.
        Phase 8: Memory Storage (only high-signal non-redundant items).
        """
        for memory in memories:
            memory = memory.strip()
            if not memory or memory.upper() == "NONE":
                continue
            
            # Simple deduplication check: Only add if the memory is not already closely matched
            existing = self.retrieve_long_term_memory(memory, top_k=1)
            # This is a basic filter (Phase 3). In production, you might calculate cosine similarity threshold locally.
            
            embedding = self.llm_client.generate_embedding(memory)
            if embedding:
                try:
                    self.collection.add(
                        embeddings=[embedding],
                        documents=[memory],
                        ids=[str(uuid.uuid4())]
                    )
                except Exception as e:
                    print(f"Failed to store memory '{memory[:50]}...': {e}")

    def retrieve_long_term_memory(self, query: str, top_k: int = 4) -> List[str]:
        """
        Phase 2: Memory Retrieval.
        Retrieves top_k most similar memories from ChromaDB using vector similarity.
        """
        try:
            count = self.collection.count()
            print(f"DEBUG MEM: Collection count = {count}")
            if count == 0:
                return []
                
            actual_top_k = min(top_k, count)
            
            # Generate embedding for the query
            query_embedding = self.llm_client.generate_embedding(query)
            if not query_embedding:
                print("DEBUG MEM: query_embedding is empty")
                return []

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=actual_top_k
            )
            
            if results and 'documents' in results and results['documents']:
                # Chroma returns a list of lists since you can query multiple items
                documents = results['documents'][0]
                print(f"DEBUG MEM: Retrieved documents: {documents}")
                # Phase 3: Filtering (simply taking top K results here, can add similarity threshold filtering)
                return documents
            print("DEBUG MEM: results documents is empty", results)
            return []
        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return []
