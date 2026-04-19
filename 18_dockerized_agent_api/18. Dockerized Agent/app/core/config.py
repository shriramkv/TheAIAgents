import os
import yaml
from typing import Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and config.yaml.
    """
    # Environment Variables
    OPENAI_API_KEY: str = ""
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True
    
    # Config YAML values (default placeholders)
    MODEL_NAME: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 500

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @classmethod
    def load_from_yaml(cls, yaml_path: str = "config.yaml") -> "Settings":
        """
        Custom loader to merge YAML config with Env vars.
        """
        settings = cls()
        if os.path.exists(yaml_path):
            with open(yaml_path, "r") as f:
                yaml_data = yaml.safe_load(f)
                if yaml_data:
                    settings.MODEL_NAME = yaml_data.get("model", settings.MODEL_NAME)
                    settings.TEMPERATURE = yaml_data.get("temperature", settings.TEMPERATURE)
                    settings.MAX_TOKENS = yaml_data.get("max_tokens", settings.MAX_TOKENS)
        return settings

# Initialize settings
settings = Settings.load_from_yaml()
