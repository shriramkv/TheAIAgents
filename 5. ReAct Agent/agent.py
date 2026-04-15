import os
from typing import Tuple

from shared.base_agent import BaseAgent
from shared.llm import LLMService
from shared.logger import AgentLogger
from shared.utils import parse_react_output
from tools.tool_registry import ToolRegistry

class ReActAgent(BaseAgent):
    """
    Implements a ReAct (Reason + Act) loop agent.
    Iteratively calls the LLM, parses actions, calls tools, and updates the prompt.
    """
    def __init__(self):
        super().__init__()
        self.llm = LLMService()
        self.logger = AgentLogger()
        self.registry = ToolRegistry()
        
        # Load the base prompt
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "react_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are a reasoning agent. Provide 'Final Answer: <answer>' when done."
            
        # Append available tools dynamically to the prompt
        tools_info = f"\n\nAvailable tools:\n{self.registry.get_tool_descriptions()}"
        self.system_prompt += tools_info

    def run(self, user_input: str) -> Tuple[str, str]:
        """
        Executes the main ReAct loop over the user_input.
        """
        # Re-initialize logger for each run to keep trace clean per execution
        self.logger = AgentLogger()
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        max_steps = 10  # Prevent infinite loops
        step = 1
        
        while step <= max_steps:
            # 1. Call LLM
            try:
                response = self.llm.call_llm(messages)
            except Exception as e:
                self.logger.log_error(f"LLM API Error: {str(e)}")
                return f"Error: {e}", self.logger.get_full_trace()
                
            # append Assistant trace back into memory
            messages.append({"role": "assistant", "content": response})

            # 2. Parse ReAct blocks
            thought, action, action_input, final_answer = parse_react_output(response)
            
            # 3. Stop Condition check
            if final_answer is not None:
                self.logger.log_final_answer(final_answer)
                return final_answer, self.logger.get_full_trace()
                
            # Formatting validation: if it didn't output Final Answer, it must have Action
            if not action or not action_input:
                err = "Formatting Error: Could not determine next action or final answer from output."
                self.logger.log_error(f"{err}\nRaw Model Output:\n{response}")
                # Force observation asking to fix formatting
                observation = "Observation: Formatting error. You must output Thought, Action, Action Input, or Final Answer."
                messages.append({"role": "user", "content": observation})
                step += 1
                continue

            # 4. Action Execution
            observation = self.registry.execute_tool(action, action_input)
            
            # Log the full step
            self.logger.log_step(step, thought or "None", action, action_input, str(observation))
            
            # 5. Provide tool output back as user message
            obs_message = f"Observation: {observation}"
            messages.append({"role": "user", "content": obs_message})
            
            step += 1
            
        # Reached max steps
        err_msg = "Error: Reached maximum loop limit without final answer."
        self.logger.log_error(err_msg)
        return err_msg, self.logger.get_full_trace()
