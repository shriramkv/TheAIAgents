from typing import List

class Logger:
    """
    Centralized logger to track routing process visually in Gradio or terminal.
    """
    def __init__(self):
        self.logs: List[str] = []

    def log(self, message: str):
        """Append a log message."""
        self.logs.append(message)
    
    def log_input(self, text: str):
        self.log(f"[INPUT]\n{text}")

    def log_classification(self, cls: str):
        self.log(f"[CLASSIFICATION] {cls}")

    def log_model_selected(self, model: str, config: str):
        self.log(f"[MODEL SELECTED] {model} ({config})")

    def log_fallback(self, reason: str, model: str):
        self.log(f"[FALLBACK USED] Reason: {reason} | Model: {model}")

    def log_response(self, response: str):
        self.log(f"[RESPONSE]\n{response}")

    def get_logs(self) -> str:
        """Returns format ready for UI output."""
        return "\n\n".join(self.logs)

    def clear(self):
        self.logs.clear()
