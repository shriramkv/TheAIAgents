from typing import List, Tuple
from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.utils import load_prompt

class PlannerExecutorVerifierAgent(BaseAgent):
    """
    Agent that orchestrates Planning, Executing, and Verifying steps.
    """
    def __init__(self):
        super().__init__()
        # Load system prompts
        self.planner_prompt = load_prompt("prompts/planner.txt")
        self.executor_prompt = load_prompt("prompts/executor.txt")
        self.verifier_prompt = load_prompt("prompts/verifier.txt")
        
    def plan(self, user_input: str) -> List[str]:
        """
        Calls planner prompt to break input into ordered steps.
        """
        self.logger.log("INPUT", user_input)
        self.logger.log("SYSTEM", "Generating initial plan...", level="INFO")
        response = call_llm(user_input, self.planner_prompt, logger=self.logger)
        
        # Parse into list of steps
        steps = []
        for line in response.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                steps.append(line)

        # Fallback if parsing fails but content exists
        if not steps and response.strip():
            self.logger.log("SYSTEM", "Standard parsing failed, using simple line split.", level="WARNING")
            steps = [line.strip() for line in response.split("\n") if line.strip()]
            
        self.logger.log("PLAN", f"Derived {len(steps)} steps:\n" + "\n".join(steps))
        return steps

    def execute(self, user_input: str, steps: List[str]) -> List[str]:
        """
        Executes each step by calling the LLM executor prompt.
        """
        self.logger.log("SYSTEM", f"Starting execution of {len(steps)} steps.", level="INFO")
        results = []
        exec_log = []
        for i, step in enumerate(steps, 1):
            self.logger.log("EXECUTION", f"Executing Step {i}: {step}", level="INFO")
            prompt = f"Original Task: {user_input}\nStep to Execute: {step}"
            res = call_llm(prompt, self.executor_prompt, logger=self.logger)
            results.append(res)
            exec_log.append(f"Step {i} Result: {res}")
            
        return results

    def combine(self, results: List[str]) -> str:
        """
        Combines execution results into a drafted answer.
        """
        self.logger.log("SYSTEM", "Combining all step results into a draft...", level="INFO")
        return "\n\n".join(results)

    def verify(self, user_input: str, answer: str) -> str:
        """
        Verifies the combined drafted answer using the verifier prompt.
        """
        self.logger.log("SYSTEM", "Sending draft to verifier...", level="INFO")
        prompt = f"Original Task: {user_input}\nDraft Answer:\n{answer}"
        verdict_raw = call_llm(prompt, self.verifier_prompt, logger=self.logger)
        
        if "INVALID" in verdict_raw.upper():
            self.logger.log("VERIFICATION", f"INVALID! Feedback: {verdict_raw}", level="WARNING")
            return verdict_raw
        else:
            self.logger.log("VERIFICATION", "VALID - Answer meets criteria.", level="INFO")
            return "VALID"

    def process(self, user_input: str) -> Tuple[str, str, str, str, str]:
        """
        Runs the full reasoning pipeline: Plan -> Execute -> Verify -> Refine.
        """
        self.reset()
        self.logger.log("SYSTEM", "New process session started.", level="INFO")
        
        # 1. PLAN
        steps = self.plan(user_input)
        plan_str = "\n".join(steps)
        
        exec_str = ""
        verify_str = ""
        final_answer = ""
        
        # Retry loop for Verification constraint
        for attempt in range(self.max_retries):
            self.logger.log("SYSTEM", f"Cycle {attempt + 1} of {self.max_retries}...", level="INFO")
            
            # 2. EXECUTE
            results = self.execute(user_input, steps)
            exec_str = "\n\n".join([f"Step {i+1} Result: {res}" for i, res in enumerate(results)])
            
            # 3. COMBINE
            draft_answer = self.combine(results)
            
            # 4. VERIFY
            verdict = self.verify(user_input, draft_answer)
            verify_str = verdict
            
            # 5. REFINE OR RETURN
            if "INVALID" in verdict.upper():
                if attempt < self.max_retries - 1:
                    feedback = f"Attempt {attempt + 1} failed. Review Feedback: {verdict}"
                    self.logger.log("SYSTEM", f"Verification failed. Initiating refinement attempt {attempt + 2}...", level="WARNING")
                    if steps:
                        steps[0] = f"{steps[0]}\nImportant Context/Feedback: {feedback}"
                else:
                    self.logger.log("SYSTEM", "Critical: Maximum retries reached. Returning latest draft.", level="CRITICAL")
                    final_answer = f"Max retries reached. Output may be incomplete.\n\nLatest Result:\n{draft_answer}"
                    self.logger.log("FINAL OUTPUT", "Incomplete result returned.")
                    break
            else:
                self.logger.log("SYSTEM", "Success: Output verified and finalized.", level="INFO")
                final_answer = draft_answer
                self.logger.log("FINAL OUTPUT", "Completed successfully.")
                break
                
        return plan_str, exec_str, verify_str, final_answer, self.logger.get_logs()
