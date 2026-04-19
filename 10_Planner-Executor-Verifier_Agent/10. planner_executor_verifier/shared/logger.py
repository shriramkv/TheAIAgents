import datetime

class AgentLogger:
    """
    A unified logger to capture the step-by-step reasoning and actions of the agent pipeline.
    """
    def __init__(self):
        self.logs = []

    def _get_timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, section: str, message: str = "", level: str = "INFO"):
        """
        Logs a specific section or detail with timestamp and level.
        """
        timestamp = self._get_timestamp()
        if message:
            log_entry = f"[{timestamp}] [{level}] [{section.upper()}]\n{message}\n"
        else:
            log_entry = f"[{timestamp}] [{level}] [{section.upper()}]\n"
        
        self.logs.append(log_entry)
        # Also print to console for real-time tracking during development
        print(log_entry.strip())

    def append(self, message: str):
        """Appends a string directly to the last log, or generally."""
        self.logs.append(message)

    def get_logs(self) -> str:
        """Returns the full formatted log string."""
        return "\n".join(self.logs)

    def clear(self):
        """Clears the current session logs."""
        self.logs.clear()
