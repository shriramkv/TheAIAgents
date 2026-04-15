from typing import Tuple, List
import os
from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.logger import setup_logger
from shared.utils import load_config
from ingestion.loader import load_txt, load_pdf
from ingestion.chunker import chunk_text
from ingestion.indexer import index_documents
from retrieval.retriever import retrieve_context

logger = setup_logger(__name__)
config = load_config()

class RAGAgent(BaseAgent):
    """
    RAG Agent implementation that retrieves relevant chunks from a vector DB
    and uses them to generate a grounded answer using a language model.
    """
    def __init__(self):
        self.model_name = config.get("model", "gpt-4o-mini")

    def ingest_document(self, file_path: str) -> bool:
        """
        One-time or on-demand ingestion flow.
        Loads -> Chunks -> Embeds -> Stores.

        Args:
            file_path (str): The file path to ingest.

        Returns:
            bool: Success status of the ingestion.
        """
        logger.info(f"Starting ingestion process for: {file_path}")
        
        # 1. Load document based on extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            text = load_txt(file_path)
        elif ext == '.pdf':
            text = load_pdf(file_path)
        else:
            logger.error(f"Unsupported file format: {ext}")
            return False
            
        if not text:
            logger.error("Failed to extract textual content from file.")
            return False

        # 2. Chunk text
        chunks = chunk_text(text)
        
        if not chunks:
            logger.error("Failed to generate chunks from the document.")
            return False

        # 3. Embed & Store in vector DB
        index_documents(chunks)
        
        logger.info("Ingestion completed successfully.")
        return True

    def run(self, query: str) -> Tuple[str, str, str]:
        """
        Query flow for the agent.
        Accepts query -> Retrieves context -> Builds prompt -> Calls LLM.

        Args:
            query (str): The user's question.

        Returns:
            Tuple[str, str, str]: 
            1. Raw context string used.
            2. Final formatted answer.
            3. A string representation of logs/trace.
        """
        logger.info(f"Processing query: {query}")
        
        # 1. Accept query and Retrieve Context
        context_chunks = retrieve_context(query)
        
        # Format the context for prompt and output
        context_str = "\\n\\n".join([f"Chunk {i+1}: {chunk}" for i, chunk in enumerate(context_chunks)])
        
        # Generate trace/logs
        logs = f"[INPUT]\\n{query}\\n\\n[RETRIEVED CONTEXT]\\n{context_str}\\n\\n"

        if not context_chunks:
            answer = "I could not find any relevant context in my knowledge base to answer your question."
            logs += f"[FINAL ANSWER]\\n{answer}"
            logger.warning("No context chunks retrieved.")
            return context_str, answer, logs

        # 2. Build Prompt
        prompt = f"Answer the question using ONLY the context below:\\n\\n<context>\\n{context_str}\\n</context>\\n\\nQuestion: {query}"
        
        # 3. Call LLM
        answer = call_llm(prompt, model_name=self.model_name)
        
        # 4. Attach LLM output to logs and Return
        logs += f"[FINAL ANSWER]\\n{answer}"
        logger.info("Successfully generated grounded response.")
        
        return context_str, answer, logs
