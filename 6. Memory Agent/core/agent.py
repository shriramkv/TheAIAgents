import yaml
from pathlib import Path
from typing import Dict, Any, Tuple

from core.llm_client import LLMClient
from core.memory_manager import MemoryManager
from config.settings import BASE_DIR

class MemoryReflectionAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.memory_manager = MemoryManager(self.llm_client)
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        prompt_path = BASE_DIR / "config" / "prompts.yaml"
        if not prompt_path.exists():
            print(f"Prompt file not found at {prompt_path}")
            return {}
        with open(prompt_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def process_query(self, user_query: str) -> Tuple[str, str, list, list]:
        """
        Executes the 8-Phase Memory + Reflection Workflow.
        Returns (Final Answer, Reflection Summary, Retrieved Memories, Stored Memories).
        """
        # Phase 1: Understand (We add to short-term)
        self.memory_manager.add_to_short_term("user", user_query)
        
        # Phase 2 & 3: Memory Retrieval and Filtering
        retrieved_memories = self.memory_manager.retrieve_long_term_memory(user_query, top_k=4)
        
        # Phase 4: Context Augmentation
        context_block = "Relevant Memory:\n"
        if retrieved_memories:
            for mem in retrieved_memories:
                context_block += f"- {mem}\n"
        else:
            context_block += "None\n"
        
        prompt_with_context = f"{context_block}\nUser Query:\n{user_query}"
        
        # Phase 5: Initial Response (Generation)
        draft_messages = [
            {"role": "system", "content": self.prompts.get("generator_prompt", "You are a helpful assistant.")},
            {"role": "user", "content": prompt_with_context}
        ]
        # Include short term memory context
        short_term = self.memory_manager.get_short_term_context()
        # We replace the last user message with our augmented one
        messages_to_send = [{"role": "system", "content": self.prompts.get("generator_prompt", "You are a helpful assistant.")}]
        messages_to_send.extend(short_term[:-1])  # Exclude the latest user turn
        messages_to_send.append({"role": "user", "content": prompt_with_context})
        
        draft_response = self.llm_client.generate_chat_completion(messages_to_send)
        
        # Phase 6: Reflection (Critic)
        reflection_messages = [
            {"role": "system", "content": self.prompts.get("reflection_prompt", "Critique this response.")},
            {"role": "user", "content": f"User Query: {user_query}\n\nDraft Answer: {draft_response}\n\nRelevant Memories:\n{context_block}"}
        ]
        reflection_feedback = self.llm_client.generate_chat_completion(reflection_messages)
        
        # Phase 7: Refinement
        refinement_messages = [
            {"role": "system", "content": self.prompts.get("refinement_prompt", "Refine the response based on critic feedback.")},
            {"role": "user", "content": f"Original Query: {user_query}\n\nDraft Answer: {draft_response}\n\nCritic Feedback: {reflection_feedback}"}
        ]
        final_answer = self.llm_client.generate_chat_completion(refinement_messages)
        
        # Phase 8: Memory Storage
        extraction_messages = [
            {"role": "system", "content": self.prompts.get("memory_extraction_prompt", "Extract memories.")},
            {"role": "user", "content": f"Conversation snippet:\nUser: {user_query}\nAgent: {final_answer}\n\nExtract important memories."}
        ]
        extracted_memory_text = self.llm_client.generate_chat_completion(extraction_messages)
        
        stored_memories = []
        if "NONE" not in extracted_memory_text.upper():
            # Parse bullet points
            lines = extracted_memory_text.splitlines()
            for line in lines:
                line = line.strip()
                if line.startswith("-") or line.startswith("*"):
                    stored_memories.append(line.lstrip("-*").strip())
            
            # Store in manager
            if stored_memories:
                self.memory_manager.store_long_term_memory(stored_memories)
                
        # Add assistant final answer to short-term memory
        self.memory_manager.add_to_short_term("assistant", final_answer)

        return final_answer, reflection_feedback, retrieved_memories, stored_memories
