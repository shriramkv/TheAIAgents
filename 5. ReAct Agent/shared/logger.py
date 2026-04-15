import logging
import os
from typing import List

class AgentLogger:
    def __init__(self, trace_file: str = "react_trace.txt"):
        self.trace_file = trace_file
        # Clear out any previous run trace
        if os.path.exists(self.trace_file):
            open(self.trace_file, "w").close()
            
        self.in_memory_logs: List[str] = []

    def log_step(self, step_num: int, thought: str, action: str, action_input: str, observation: str) -> None:
        """
        Logs a single ReAct step
        """
        log_str = (
            f"\n[STEP {step_num}]\n"
            f"THOUGHT: {thought}\n"
            f"ACTION: {action}\n"
            f"INPUT: {action_input}\n"
            f"OBSERVATION: {observation}\n"
        )
        self._write_and_store(log_str)

    def log_final_answer(self, final_answer: str) -> None:
        """
        Logs the final answer block
        """
        log_str = f"\n[FINAL ANSWER]\n{final_answer}\n"
        self._write_and_store(log_str)
        
    def log_error(self, error_msg: str) -> None:
        """
        Logs an error smoothly in the trace.
        """
        log_str = f"\n[ERROR]\n{error_msg}\n"
        self._write_and_store(log_str)

    def _write_and_store(self, text: str) -> None:
        self.in_memory_logs.append(text)
        print(text)
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(text)

    def get_full_trace(self) -> str:
        """
        Returns all logs as a single formatted string.
        """
        return "".join(self.in_memory_logs)
