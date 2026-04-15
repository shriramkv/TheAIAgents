import json
from typing import Tuple

from shared.base_agent import BaseAgent
from shared.llm import call_llm_with_tools
from shared.logger import AgentLogger
from shared.utils import load_config
from tools.tool_registry import TOOLS, execute_tool

class ToolCallingAgent(BaseAgent):
    """
    An intelligent agent that iterates with an LLM and dynamically calls available tools
    until a final conclusive answer is generated. 
    """
    
    def __init__(self):
        super().__init__()
        # Load params from config or use defaults
        self.config = load_config()
        self.model = self.config.get("model", "gpt-4o-mini")
        self.temperature = self.config.get("temperature", 0.2)
        self.max_tokens = self.config.get("max_tokens", 500)
        
    def run(self, user_input: str) -> Tuple[str, str]:
        """
        Executes the main tool-calling reasoning loop.
        
        Args:
            user_input: The user's goal or query.
            
        Returns:
            Tuple containing the final LLM string answer and a detailed reasoning log.
        """
        trace_logs = []
        
        def log_and_record(step: str) -> None:
            """Captures the standard log and appends it to trace."""
            trace_logs.append(step)
            
        # 1. Initialize messages
        messages = [
            {"role": "system", "content": "You are a helpful AI that can use tools to answer questions. Use the available tools when necessary. If no tools are required, answer directly."},
            {"role": "user", "content": user_input}
        ]
        
        log_and_record(AgentLogger.log_thought(f"Received user task: '{user_input}'"))
        
        # 2. Main reasoning loop
        while True:
            # Call LLM with tools
            response_message = call_llm_with_tools(
                messages=messages,
                tools=TOOLS,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Check if LLM requests a tool call
            if response_message.tool_calls:
                # We need to append the model's message so conversation history aligns
                # Using model_dump() handles nested tool_call schema correctly for OpenAI V1 API
                messages.append(response_message.model_dump(exclude_none=True))
                
                # Iterate through all requested tool calls
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        function_args = {}
                        
                    # Log the tool action selection
                    log_and_record(AgentLogger.log_action(function_name, function_args))
                    
                    # Execute corresponding Python function
                    tool_result = execute_tool(function_name, function_args)
                    
                    # Log observation result
                    log_and_record(AgentLogger.log_observation(tool_result))
                    
                    # Append result back to the messages to feed into next LLM inference
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": tool_result
                    })
            else:
                # No more tools requested; LLM provided its final natural language answer
                final_answer = response_message.content
                log_and_record(AgentLogger.log_final(final_answer))
                
                # Terminate loop and return output
                break
                
        return final_answer, "\n".join(trace_logs)
