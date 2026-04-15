class AgentLogger:
    """
    A logger to record the stages of agent execution.
    Outputs logs as a string and prints to the console for debugging.
    """
    
    def __init__(self):
        self._logs = []

    def log(self, stage: str, content: str):
        """
        Record a log entry for a specific stage.
        
        Args:
            stage (str): The bracketed label for the stage (e.g., '[INITIAL RESPONSE]').
            content (str): The internal content/result to log.
        """
        log_entry = f"{stage}\n{content}\n"
        self._logs.append(log_entry)
        print(f"\n{'='*50}\n{log_entry}{'='*50}\n")

    def get_logs(self) -> str:
        """
        Return the aggregated logs as a single formatted string.
        """
        return "\n".join(self._logs)

    def clear(self):
        """
        Clear all logs. Useful for repeated runs.
        """
        self._logs = []
