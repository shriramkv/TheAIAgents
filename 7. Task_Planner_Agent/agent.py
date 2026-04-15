from pathlib import Path
from shared.base_agent import BaseAgent
from shared.vector_store import VectorStore
from shared.logger import get_logger
from shared.utils import load_config, load_prompt, parse_steps
from shared.llm import call_llm
import traceback

logger = get_logger(__name__)

class TaskPlannerAgent(BaseAgent):
    """
    Agent that breaks a goal into steps, executes them using memory, and synthesizes a final result.
    """
    def __init__(self, root_dir: str):
        self.root_path = Path(root_dir)
        self.config = load_config(self.root_path)
        
        # Load Prompts
        self.planner_prompt = load_prompt(self.root_path, "planner")
        self.executor_prompt = load_prompt(self.root_path, "executor")
        self.summarizer_prompt = load_prompt(self.root_path, "summarizer")
        
        # Initialize Memory
        memory_dir = self.root_path / "memory"
        self.memory = VectorStore(str(memory_dir))
        
        # Log store for UI tracing
        self.logs = []
        
    def _log(self, message: str):
        """Helper to append to local logs and standard logger"""
        logger.info(message)
        self.logs.append(message)
        
    def plan(self, goal: str) -> list[str]:
        """
        Calls planner prompt to break the goal into steps and parses them.
        """
        self._log(f"[INPUT]\nGoal: {goal}")
        
        try:
            plan_response = call_llm(
                prompt=goal,
                system_prompt=self.planner_prompt,
                config=self.config
            )
            
            steps = parse_steps(plan_response)
            
            self._log("\n[PLAN]")
            for i, step in enumerate(steps, 1):
                self._log(f"Step {i}: {step}")
                
            return steps
        except Exception as e:
            self._log(f"Failed to plan: {e}")
            return []

    def retrieve_memory(self, query: str) -> str:
        """
        Fetches relevant past context from the vector database.
        """
        past_memories = self.memory.similarity_search(query, k=3)
        if past_memories:
            return "\n".join(past_memories)
        return "No relevant past memory found."

    def store_memory(self, text: str):
        """
        Saves text (usually step outputs) in the vector DB.
        """
        self.memory.add_documents([text])

    def execute_step(self, step: str, goal: str) -> str:
        """
        Calls executor prompt for a specific step.
        """
        # Retrieve context relevant to this step
        context = self.retrieve_memory(step)
        
        prompt = self.executor_prompt.format(
            goal=goal,
            step=step,
            memory=context
        )
        
        try:
            result = call_llm(
                prompt=prompt,
                system_prompt="You are a capable execution agent. Follow the instructions precisely.",
                config=self.config
            )
            return result
        except Exception as e:
            return f"Error executing step: {str(e)}"

    def summarize(self, goal: str, results: list[str]) -> str:
        """
        Combines all step outputs using the summarizer prompt.
        """
        results_text = "\n\n".join([f"Step {i+1} Result:\n{r}" for i, r in enumerate(results)])
        prompt = self.summarizer_prompt.format(
            goal=goal,
            results=results_text
        )
        
        try:
            final_output = call_llm(
                prompt=prompt,
                system_prompt="You are a summarizing agent. Combine the results cleanly.",
                config=self.config
            )
            return final_output
        except Exception as e:
            return f"Error summarizing: {str(e)}"

    def run(self, goal: str) -> tuple[str, str, str, str]:
        """
        Full Execution Flow.
        Returns:
            plan_str, steps_result_str, final_output, logs_str
        """
        self.logs = [] # clear logs for new run
        
        # 1. PLAN
        steps = self.plan(goal)
        if not steps:
            return "Failed to generate plan.", "", "Error during planning stage.", "\n".join(self.logs)
            
        plan_str = "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])
        
        # 2. EXECUTE
        self._log("\n[EXECUTION]")
        results = []
        for i, step in enumerate(steps, 1):
            self._log(f"Executing Step {i}...")
            result = self.execute_step(step, goal)
            self._log(f"Step {i} Result: {result}")
            results.append(result)
            
            # 3. STORE
            self.store_memory(f"Step: {step}\nResult: {result}")
            
        steps_result_str = "\n\n".join([f"Step {i+1}: {steps[i]}\nResult: {r}" for i, r in enumerate(results)])
        
        # 4. SUMMARIZE
        self._log("\n[FINAL OUTPUT]")
        final_answer = self.summarize(goal, results)
        self._log(final_answer)
        
        logs_str = "\n".join(self.logs)
        
        return plan_str, steps_result_str, final_answer, logs_str
