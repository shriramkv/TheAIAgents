import os
from shared.base_agent import BaseAgent
from shared.logger import AgentLogger
from shared.llm import call_llm
from shared.utils import load_prompt

class ReflectionAgent(BaseAgent):
    """
    An agent that implements the Reflection Pattern.
    It generates an initial response, critiques its own response,
    and then improves the response based on the critique.
    """
    
    def __init__(self):
        super().__init__()
        # Initialize logger for tracking reasoning steps
        self.logger = AgentLogger()
        
        # Load the external prompts (MUST be present in prompts/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.generation_prompt = load_prompt(os.path.join(base_dir, "prompts", "generation.txt"))
        self.critique_prompt = load_prompt(os.path.join(base_dir, "prompts", "critique.txt"))
        self.improve_prompt = load_prompt(os.path.join(base_dir, "prompts", "improve.txt"))

    def generate(self, user_input: str) -> str:
        """Step 1: Generate initial response."""
        self.logger.log("[INPUT]", user_input)
        response = call_llm(user_input, self.generation_prompt)
        self.logger.log("[INITIAL RESPONSE]", response)
        return response

    def critique(self, initial_response: str) -> str:
        """Step 2: Critique the generated response."""
        response = call_llm(initial_response, self.critique_prompt)
        self.logger.log("[CRITIQUE]", response)
        return response

    def improve(self, original_response: str, critique_text: str) -> str:
        """Step 3: Improve original response using the critique."""
        # Combine the original response and the critique to give context to the LLM
        context = f"Original Response:\n{original_response}\n\nCritique:\n{critique_text}\n\nImprove the response based on the critique above."
        
        response = call_llm(context, self.improve_prompt)
        self.logger.log("[IMPROVED RESPONSE]", response)
        return response

    def run(self, user_input: str) -> tuple[str, str, str, str]:
        """
        Main operation flow for the Reflection Agent.
        
        Returns:
            tuple: (initial_response, critique, improved_response, full_logs)
        """
        # Clear previous logs for a fresh run
        self.logger.clear()
        
        # Sequentially execute the reflection pattern steps
        initial_response = self.generate(user_input)
        critique_text = self.critique(initial_response)
        improved_response = self.improve(initial_response, critique_text)
        
        # Retrieve all aggregated logs
        full_logs = self.logger.get_logs()
        
        return initial_response, critique_text, improved_response, full_logs
