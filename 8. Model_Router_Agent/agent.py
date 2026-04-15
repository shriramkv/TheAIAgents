from typing import Tuple
from shared.base_agent import BaseAgent
from shared.router import ModelRouter
from shared.llm import call_llm
from shared.logger import Logger

class ModelRouterAgent(BaseAgent):
    """
    Agent that utilizes a router to dynamically select optimal LLM configuration
    based on the complexity of the query.
    """
    def __init__(self):
        self.logger = Logger()
        self.router = ModelRouter(self.logger)
    
    def run(self, user_input: str) -> Tuple[str, str, str]:
        """
        Executes the main routing logic:
        1. Log input
        2. Classify
        3. Route model
        4. Call LLM
        5. Handle fallbacks
        6. Return results
        
        Returns: Tuple of (response, routing_info, logs)
        """
        self.logger.clear()
        self.logger.log_input(user_input)
        
        try:
            # 1. Classify the query logic
            complexity = self.router.classify_query(user_input)
            
            # 2. Base model selection
            config = self.router.select_model(complexity)
            
            # 3. Call LLM with primary routing params
            try:
                response = call_llm(
                    prompt=user_input,
                    model=config["model"],
                    temperature=config["temperature"],
                    max_tokens=config["max_tokens"],
                    retries=config["retries"],
                    timeout_seconds=config["timeout_seconds"],
                    system_prompt="You are a helpful assistant."
                )
                self.logger.log_response(response)
                
            except Exception as primary_error:
                # 4. Fallback Execution
                fallback_model = self.router.fallback_model
                self.logger.log_fallback(str(primary_error), fallback_model)
                
                # Execute fallback logic with slight penalty/static params
                response = call_llm(
                    prompt=user_input,
                    model=fallback_model,
                    temperature=0.3, # reliable standard temperature
                    max_tokens=500,  # reliable standard length
                    retries=1,       # single fallback try to prevent infinite loop
                    timeout_seconds=config["timeout_seconds"],
                    system_prompt="You are a helpful assistant."
                )
                self.logger.log_response(response)
                
        except Exception as e:
            # Total failure catcher
            response = f"Critical Failure: {str(e)}"
            self.logger.log_response(response)

        # Build clean output returns
        final_logs = self.logger.get_logs()
        final_routing_info = f"Complexity Classified: {complexity}\nPrimary Model Params used: {config}"
        
        return response, final_routing_info, final_logs
