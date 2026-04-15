"""
Main Agent implementation.
"""
import re
from typing import Tuple
from shared.base_agent import BaseAgent
from shared.llm import LLMInterface
from shared.utils import is_math_query, is_string_query
from tools.calculator import calculate
from tools.string_tools import reverse_string

class HelloAgent(BaseAgent):
    """
    A basic agent that can perform math operations, string operations,
    or fallback to generating an answer using an LLM.
    """
    def __init__(self):
        super().__init__()
        self.llm = LLMInterface()

    def run(self, user_input: str) -> Tuple[str, str]:
        """
        Runs the exact agent logic according to requirements.
        Returns final answer and formatted logs.
        """
        # Clear logs from previous runs
        self.logger.clear()
        
        try:
            if is_math_query(user_input):
                self.logger.log("THOUGHT", "Detecting math query")
                self.logger.log("ACTION", "Calling calculator")
                
                # Extract the math expression from the input
                # Find all numbers and math operators
                expression_match = re.search(r'([\d\s\+\-\*\/\(\)\.]+)', user_input)
                if expression_match and any(char.isdigit() for char in expression_match.group(1)):
                    expr = expression_match.group(1).strip()
                    result = calculate(expr)
                    self.logger.log("OBSERVATION", f"Result = {result}")
                    final_answer = f"The answer is {result}"
                else:
                    self.logger.log("OBSERVATION", "Could not parse math expression.")
                    final_answer = "I could not understand the math expression."
                    
            elif is_string_query(user_input):
                self.logger.log("THOUGHT", "Detecting string manipulation query")
                self.logger.log("ACTION", "Calling string tool (reverse)")
                
                result = reverse_string(user_input)
                self.logger.log("OBSERVATION", f"Result = {result}")
                final_answer = f"The reversed string is '{result}'"
                
            else:
                self.logger.log("THOUGHT", "Query does not require specialized tools. Falling back to LLM.")
                self.logger.log("ACTION", "Calling LLM")
                
                result = self.llm.generate(user_input)
                self.logger.log("OBSERVATION", "LLM response received.")
                final_answer = result

            self.logger.log("FINAL", final_answer)
            return final_answer, self.logger.get_logs_string()
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.logger.log("OBSERVATION", error_msg)
            self.logger.log("FINAL", error_msg)
            return error_msg, self.logger.get_logs_string()
