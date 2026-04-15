from shared.llm import call_llm
from shared.utils import load_config, load_prompt
from shared.logger import Logger
import os

class ModelRouter:
    """
    Handles classifying queries and routing to the optimal LLM configuration parameters.
    """
    def __init__(self, logger: Logger):
        self.config = load_config()
        self.router_prompt = load_prompt(os.path.join("prompts", "router.txt"))
        self.logger = logger
        
        # Primary routing setup
        self.primary_model = self.config.get("primary_model", "gpt-4o-mini")
        self.fallback_model = self.config.get("fallback_model", "gpt-4o-mini")
        
        self.configs = {
            "SIMPLE": {
                "temperature": self.config.get("temperature_simple", 0.2),
                "max_tokens": self.config.get("max_tokens_simple", 200)
            },
            "MEDIUM": {
                "temperature": self.config.get("temperature_medium", 0.3),
                "max_tokens": self.config.get("max_tokens_medium", 500)
            },
            "COMPLEX": {
                "temperature": self.config.get("temperature_complex", 0.5),
                "max_tokens": self.config.get("max_tokens_complex", 800)
            }
        }

    def classify_query(self, user_input: str) -> str:
        """
        Uses LLM to classify query complexity based on the router prompt.
        """
        try:
            # We use a very fast/cheap model to do routing classification
            classification = call_llm(
                prompt=user_input,
                system_prompt=self.router_prompt,
                model="gpt-4o-mini",
                max_tokens=10, # Keep it extremely short
                temperature=0.1
            ).strip().upper()
            
            # Clean possible markdown surrounding
            if classification not in ["SIMPLE", "MEDIUM", "COMPLEX"]:
                if "SIMPLE" in classification: classification = "SIMPLE"
                elif "COMPLEX" in classification: classification = "COMPLEX"
                else: classification = "MEDIUM" # Safe default
                
            self.logger.log_classification(classification)
            return classification
            
        except Exception as e:
            # If router logic fails entirely, default to safely process it as MEDIUM
            self.logger.log(f"[WARNING] Classification failed: {e}. Defaulting to MEDIUM")
            self.logger.log_classification("MEDIUM")
            return "MEDIUM"

    def select_model(self, complexity: str) -> dict:
        """
        Selects model configuration params based on classification.
        """
        selected_config = self.configs.get(complexity, self.configs["MEDIUM"])
        
        self.logger.log_model_selected(
            self.primary_model, 
            f"Temp: {selected_config['temperature']}, Tokens: {selected_config['max_tokens']}"
        )
        
        return {
            "model": self.primary_model,
            "temperature": selected_config["temperature"],
            "max_tokens": selected_config["max_tokens"],
            "retries": self.config.get("max_retries", 3),
            "timeout_seconds": self.config.get("timeout_seconds", 10)
        }
