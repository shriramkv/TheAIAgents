from shared.logger import AgentLogger

class BaseAgent:
    """
    The Base Agent provides the core loop for interacting with the LLM.
    It standardizes the Think -> Act -> Observe cycle.
    """
    def __init__(self, config: dict):
        """
        Initialize the base agent with configuration parameters.
        
        Args:
            config (dict): Global configuration for the agent.
        """
        self.config = config
        self.logger = AgentLogger()

    def think(self, user_input: str) -> str:
        """
        Generate reasoning about the input before taking action.
        This provides a transparent trace for the user.
        """
        thought = f"Analyzing intent for input: '{user_input}'"
        self.logger.log("THOUGHT", thought)
        return thought

    def act(self, thought: str, user_input: str) -> str:
        """
        Call the LLM using the formulated thought and original input.
        Must be implemented by subclasses to define actual LLM calling mechanics.
        """
        action = "Executing default action (BaseAgent placeholder)."
        self.logger.log("ACTION", action)
        return "Base Response"

    def observe(self, response: str) -> str:
        """
        Process the generated response from the LLM.
        """
        self.logger.log("FINAL", "Response generated successfully.")
        return response

    def run(self, user_input: str) -> tuple[str, str]:
        """
        The core agent execution loop.
        Input → Think → Act → Observe → Output
        
        Returns:
            tuple[str, str]: A tuple containing (final_response, formatted_logs).
        """
        try:
            self.logger.clear()
            thought = self.think(user_input)
            raw_response = self.act(thought, user_input)
            final_response = self.observe(raw_response)
            
            return final_response, self.logger.get_logs_as_string()
        except Exception as e:
            error_message = f"Agent encountered an error: {e}"
            self.logger.log("ERROR", error_message)
            return error_message, self.logger.get_logs_as_string()
