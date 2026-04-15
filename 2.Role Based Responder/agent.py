from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.utils import load_yaml
import os

class RoleBasedAgent(BaseAgent):
    """
    RoleBasedAgent inherits from BaseAgent and dynamically loads 
    its system prompt configuration from a dedicated role YAML file.
    """
    def __init__(self, config: dict, role_name: str):
        """
        Initializes the agent by loading the specific role.
        
        Args:
            config (dict): Global agent configuration.
            role_name (str): The name of the role (e.g., 'Teacher', 'Lawyer').
        """
        super().__init__(config)
        self.role_name = role_name
        self.system_prompt = self._load_role()
        
    def _load_role(self) -> str:
        """
        Loads the YAML configuration for the specific role to get the system prompt.
        
        Returns:
            str: The system prompt for the role.
        """
        # Format filename from the readable name (e.g., "Startup Founder" -> "startup_founder")
        filename = self.role_name.lower().replace(" ", "_").replace("-", "_") + ".yaml"
        # Since this executes from the root directory, path is roles/{filename}
        file_path = os.path.join("roles", filename)
        
        try:
            role_data = load_yaml(file_path)
            # Default to harmless prompt if for some reason the structure is missing
            prompt = role_data.get("system_prompt", "You are a helpful assistant.")
            self.logger.log("ROLE", f"Loaded persona: {role_data.get('role_name', self.role_name)}")
            return prompt
        except FileNotFoundError:
            # Fallback to default if the specific role is missing
            self.logger.log("ROLE", f"Role file {filename} not found. Falling back to default.")
            default_data = load_yaml("roles/default.yaml")
            return default_data.get("system_prompt", "You are a helpful assistant.")

    def think(self, user_input: str) -> str:
        """
        Overrides BaseAgent think to add role-specific reasoning context.
        """
        thought = f"User wants an explanation or response for: '{user_input}'"
        self.logger.log("THOUGHT", thought)
        return thought

    def act(self, thought: str, user_input: str) -> str:
        """
        Calls the LLM with the loaded role persona.
        """
        action = f"Calling LLM with {self.role_name.lower()} persona based on: '{thought}'"
        self.logger.log("ACTION", action)
        
        # Actual LLM call using our shared utility
        response = call_llm(user_input, self.system_prompt, self.config)
        return response
